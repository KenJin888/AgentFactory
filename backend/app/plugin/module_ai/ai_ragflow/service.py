import asyncio
import os
import uuid
from typing import Any, AsyncGenerator, Dict, List, Optional, Union

import httpx
from dotenv import load_dotenv
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)

from app.api.v1.module_system.auth.schema import AuthSchema
from app.config.setting import settings
from app.core.exceptions import CustomException
from app.core.logger import log
from app.plugin.module_ai.ai_chat.service import AiChatService
from app.plugin.module_ai.ai_dataset_auth.schema import (
    AiDatasetAuthRuleOutSchema,
    AiDatasetAuthRuleSchema,
)
from app.plugin.module_ai.ai_dataset_auth.service import AiDatasetAuthService
from .schema import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ListDatasetsResponse,
    ListDocumentsResponse,
    RAGFlowResponse,
    RetrieveChunkItem,
    RetrieveChunksResponse,
)

# Load environment variables
load_dotenv()

# Constants
RAGFLOW_API_BASE = "http://localhost/api/v1"
DEFAULT_TIMEOUT = 30
DOCUMENT_RUN_STATUS_MAP = {
    "0": "UNSTART",
    "1": "RUNNING",
    "2": "CANCEL",
    "3": "DONE",
    "4": "FAIL",
    "UNSTART": "UNSTART",
    "RUNNING": "RUNNING",
    "CANCEL": "CANCEL",
    "DONE": "DONE",
    "FAIL": "FAIL",
}


class RAGFlowAPIError(Exception):
    """Exception raised for non-2xx responses from RAGFlow API."""

    def __init__(
            self,
            http_code: int,
            error_code: Optional[str] = None,
            error_msg: Optional[str] = None,
            trace_id: Optional[str] = None,
    ):
        self.http_code = http_code
        self.error_code = error_code
        self.error_msg = error_msg
        self.trace_id = trace_id
        super().__init__(f"RAGFlow API Error {http_code}: {error_msg} (Trace ID: {trace_id})")


class RAGFlowService:
    """Service for interacting with RAGFlow API."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the RAGFlow service.

        Args:
            api_key: The API key for authentication. Defaults to env var RAGFLOW_API_KEY.
            base_url: The base URL for the API. Defaults to env var RAGFLOW_API_BASE.
        """
        self.api_key = api_key or settings.RAGFLOW_API_KEY or os.getenv("RAGFLOW_API_KEY")
        if not self.api_key:
            log.warning("RAGFLOW_API_KEY not set. API calls may fail.")

        self.base_url = base_url or settings.RAGFLOW_API_BASE or os.getenv("RAGFLOW_API_BASE", RAGFLOW_API_BASE)
        self.timeout = int(os.getenv("RAGFLOW_TIMEOUT", settings.RAGFLOW_TIMEOUT or DEFAULT_TIMEOUT))
        self._verify = self.base_url.lower().startswith("https://")
        self._client: Optional[httpx.AsyncClient] = None
        self._client_lock = asyncio.Lock()

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create the shared AsyncClient."""
        if self._client and not self._client.is_closed:
            return self._client

        async with self._client_lock:
            if self._client and not self._client.is_closed:
                return self._client

            timeout = httpx.Timeout(self.timeout)
            limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)
            self._client = httpx.AsyncClient(
                timeout=timeout,
                limits=limits,
                trust_env=False,
                verify=self._verify,
            )
            return self._client

    async def close(self) -> None:
        """Close the shared AsyncClient."""
        async with self._client_lock:
            if self._client and not self._client.is_closed:
                await self._client.aclose()
            self._client = None

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for the request."""
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        else:
            log.warning("API Key is missing in _get_headers")
        return headers

    async def _request_json(
            self,
            method: str,
            url: str,
            params: Optional[Dict[str, Any]] = None,
            json_body: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None,
            files: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        headers = headers or self._get_headers()
        client = await self._get_client()
        response = await client.request(
            method, url, headers=headers, params=params, json=json_body, data=data, files=files
        )
        trace_id = response.headers.get("X-Trace-Id", str(uuid.uuid4()))
        if response.status_code not in (200, 201):
            try:
                error_data = response.json()
                error_code = error_data.get("code")
                error_msg = error_data.get("message")
            except Exception:
                error_code = "UNKNOWN"
                error_msg = response.text
            log.error(
                f"api_error status={response.status_code} error_code={error_code} error_msg={error_msg} trace_id={trace_id}"
            )
            raise RAGFlowAPIError(
                http_code=response.status_code,
                error_code=str(error_code),
                error_msg=str(error_msg),
                trace_id=trace_id,
            )
        try:
            data = response.json()
        except Exception:
            raise RAGFlowAPIError(
                http_code=response.status_code,
                error_code="INVALID_RESPONSE",
                error_msg=response.text,
                trace_id=trace_id,
            )
        if data.get("code") == 0 and isinstance(data.get("data"), bool) and not data.get("data"):
            raise RAGFlowAPIError(
                http_code=response.status_code,
                error_code="AUTH_ERROR",
                error_msg=data.get("message", "Unknown error"),
                trace_id=trace_id,
            )
        return data

    async def list_datasets(
            self, page: int = 1, page_size: int = 1024
    ) -> ListDatasetsResponse:
        """
        List datasets from RAGFlow.
        """
        url = f"{self.base_url}/datasets"
        params = {"page": page, "page_size": page_size}
        data = await self._request_json("GET", url, params=params)
        if isinstance(data.get("data"), dict):
            if "datasets" in data["data"]:
                data["data"] = data["data"].get("datasets") or []
            elif "data" in data["data"]:
                data["data"] = data["data"].get("data") or []
        data["data"] = [
            {
                "dataset_id": str(item.get("id") or ""),
                "name": item.get("name") or "",
                "description": item.get("description"),
                "document_count": item.get("document_count"),
            }
            for item in (data.get("data") or [])
        ]
        return ListDatasetsResponse(**data)

    async def create_dataset(self, payload: Dict[str, Any]) -> RAGFlowResponse:
        url = f"{self.base_url}/datasets"
        data = await self._request_json("POST", url, json_body=payload)
        return RAGFlowResponse(**data)

    async def delete_datasets(self, payload: Dict[str, Any]) -> RAGFlowResponse:
        url = f"{self.base_url}/datasets"
        data = await self._request_json("DELETE", url, json_body=payload)
        return RAGFlowResponse(**data)

    async def update_dataset(self, dataset_id: str, payload: Dict[str, Any]) -> RAGFlowResponse:
        url = f"{self.base_url}/datasets/{dataset_id}"
        data = await self._request_json("PUT", url, json_body=payload)
        return RAGFlowResponse(**data)

    async def upload_documents(self, dataset_id: str, files: List[Any]) -> RAGFlowResponse:
        url = f"{self.base_url}/datasets/{dataset_id}/documents"
        headers = self._get_headers()
        headers.pop("Content-Type", None)
        upload_files = [("file", (f.filename, f.file, f.content_type)) for f in files]
        data = await self._request_json("POST", url, files=upload_files, headers=headers)
        return RAGFlowResponse(**data)

    async def update_document(self, dataset_id: str, document_id: str, payload: Dict[str, Any]) -> RAGFlowResponse:
        url = f"{self.base_url}/datasets/{dataset_id}/documents/{document_id}"
        data = await self._request_json("PUT", url, json_body=payload)
        return RAGFlowResponse(**data)

    async def download_document(self, dataset_id: str, document_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/datasets/{dataset_id}/documents/{document_id}"
        headers = self._get_headers()
        client = await self._get_client()
        response = await client.get(url, headers=headers)
        trace_id = response.headers.get("X-Trace-Id", str(uuid.uuid4()))
        if response.status_code not in (200, 201):
            try:
                error_data = response.json()
                error_code = error_data.get("code")
                error_msg = error_data.get("message")
            except Exception:
                error_code = "UNKNOWN"
                error_msg = response.text
            log.error(
                f"api_error status={response.status_code} error_code={error_code} error_msg={error_msg} trace_id={trace_id}"
            )
            raise RAGFlowAPIError(
                http_code=response.status_code,
                error_code=str(error_code),
                error_msg=str(error_msg),
                trace_id=trace_id,
            )
        content_type = response.headers.get("Content-Type", "application/octet-stream")
        content_disposition = response.headers.get("Content-Disposition")
        filename = self._extract_filename(content_disposition, f"{document_id}")
        return {
            "content": response.content,
            "content_type": content_type,
            "filename": filename,
        }

    async def list_documents(
            self,
            dataset_id: str,
            page: int = 1,
            page_size: int = 1024,
            run: Optional[List[str]] = None,
    ) -> ListDocumentsResponse:
        url = f"{self.base_url}/datasets/{dataset_id}/documents"
        params = {"page": page, "page_size": page_size}
        if run:
            params["run"] = run
        data = await self._request_json("GET", url, params=params)
        if isinstance(data.get("data"), dict):
            if "docs" in data["data"]:
                data["data"] = data["data"].get("docs") or []
        data["data"] = [self._normalize_document(item) for item in (data.get("data") or [])]
        return ListDocumentsResponse(**data)

    @staticmethod
    def _normalize_document(item: Any) -> Any:
        if not isinstance(item, dict):
            return item

        normalized_item = dict(item)
        raw_run = normalized_item.get("run", normalized_item.get("status"))
        normalized_run = RAGFlowService._normalize_document_run(raw_run)
        if normalized_run is not None:
            normalized_item["run"] = normalized_run

        progress = RAGFlowService._normalize_progress(normalized_item.get("progress"))
        if progress is not None:
            normalized_item["progress"] = progress

        return normalized_item

    @staticmethod
    def _normalize_document_run(run: Any) -> Optional[str]:
        if run is None:
            return None

        normalized = str(run).strip().upper()
        if not normalized:
            return None

        return DOCUMENT_RUN_STATUS_MAP.get(normalized, normalized)

    @staticmethod
    def _normalize_progress(progress: Any) -> Optional[float]:
        if progress is None or progress == "":
            return None
        try:
            return float(progress)
        except (TypeError, ValueError):
            return None

    async def delete_documents(self, dataset_id: str, payload: Dict[str, Any]) -> RAGFlowResponse:
        url = f"{self.base_url}/datasets/{dataset_id}/documents"
        data = await self._request_json("DELETE", url, json_body=payload)
        return RAGFlowResponse(**data)

    async def parse_documents(self, dataset_id: str, payload: Dict[str, Any]) -> RAGFlowResponse:
        url = f"{self.base_url}/datasets/{dataset_id}/chunks"
        data = await self._request_json("POST", url, json_body=payload)
        return RAGFlowResponse(**data)

    async def stop_parsing_documents(self, dataset_id: str, payload: Dict[str, Any]) -> RAGFlowResponse:
        url = f"{self.base_url}/datasets/{dataset_id}/chunks"
        data = await self._request_json("DELETE", url, json_body=payload)
        return RAGFlowResponse(**data)

    async def add_chunk(self, dataset_id: str, document_id: str, payload: Dict[str, Any]) -> RAGFlowResponse:
        url = f"{self.base_url}/datasets/{dataset_id}/documents/{document_id}/chunks"
        data = await self._request_json("POST", url, json_body=payload)
        return RAGFlowResponse(**data)

    async def list_chunks(
            self,
            dataset_id: str,
            document_id: str,
            keywords: Optional[str] = None,
            page: int = 1,
            page_size: int = 1024,
            chunk_id: Optional[str] = None,
    ) -> RAGFlowResponse:
        url = f"{self.base_url}/datasets/{dataset_id}/documents/{document_id}/chunks"
        params: Dict[str, Any] = {"page": page, "page_size": page_size}
        if keywords:
            params["keywords"] = keywords
        if chunk_id:
            params["id"] = chunk_id
        data = await self._request_json("GET", url, params=params)
        return RAGFlowResponse(**data)

    async def delete_chunks(self, dataset_id: str, document_id: str, payload: Dict[str, Any]) -> RAGFlowResponse:
        url = f"{self.base_url}/datasets/{dataset_id}/documents/{document_id}/chunks"
        data = await self._request_json("DELETE", url, json_body=payload)
        return RAGFlowResponse(**data)

    async def update_chunk(
            self, dataset_id: str, document_id: str, chunk_id: str, payload: Dict[str, Any]
    ) -> RAGFlowResponse:
        url = f"{self.base_url}/datasets/{dataset_id}/documents/{document_id}/chunks/{chunk_id}"
        data = await self._request_json("PUT", url, json_body=payload)
        return RAGFlowResponse(**data)

    async def retrieve_chunks(self, payload: Dict[str, Any]) -> RAGFlowResponse:
        url = f"{self.base_url}/retrieval"
        data = await self._request_json("POST", url, json_body=payload)
        return RAGFlowResponse(**data)

    def _extract_filename(self, content_disposition: Optional[str], fallback: str) -> str:
        if not content_disposition:
            return fallback
        parts = content_disposition.split(";")
        for part in parts:
            item = part.strip()
            if item.lower().startswith("filename*="):
                value = item.split("=", 1)[1]
                if value.lower().startswith("utf-8''"):
                    return value[7:]
                return value.strip('"')
            if item.lower().startswith("filename="):
                return item.split("=", 1)[1].strip('"')
        return fallback

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, asyncio.TimeoutError)),
        before_sleep=before_sleep_log(log, "warning"),
        reraise=True,
    )
    async def create_chat_completion(
            self, request: ChatCompletionRequest
    ) -> Union[ChatCompletionResponse, AsyncGenerator[str, None]]:
        """
        Create a chat completion asynchronously.
        """
        url = f"{self.base_url}/chat/completions"
        headers = self._get_headers()

        log.info(f"sending_request url={url} model={request.model} stream={request.stream}")

        client = await self._get_client()
        response: Optional[httpx.Response] = None

        try:
            if request.stream:
                req = client.build_request("POST", url, headers=headers, json=request.model_dump(exclude_none=True))
                response = await client.send(req, stream=True)
            else:
                response = await client.post(url, headers=headers, json=request.model_dump(exclude_none=True))

            trace_id = response.headers.get("X-Trace-Id", str(uuid.uuid4()))

            if response.status_code != 200:
                await self._handle_error(response, trace_id)

            if request.stream:
                return self._stream_generator(response)
            else:
                data = response.json()
                return ChatCompletionResponse(**data)

        except Exception as e:
            log.error(f"request_failed error={e}")
            raise
        finally:
            if response is not None and not request.stream:
                await response.aclose()

    async def _handle_error(self, response: httpx.Response, trace_id: str):
        try:
            # If we are streaming, we need to read the body first to get error details
            await response.aread()
            error_data = response.json()
            error_code = error_data.get("code")
            error_msg = error_data.get("message")
        except Exception:
            error_code = "UNKNOWN"
            error_msg = response.text

        await response.aclose()

        log.error(
            f"api_error status={response.status_code} error_code={error_code} error_msg={error_msg} trace_id={trace_id}")
        raise RAGFlowAPIError(
            http_code=response.status_code,
            error_code=str(error_code),
            error_msg=str(error_msg),
            trace_id=trace_id
        )

    async def _stream_generator(self, response: httpx.Response) -> AsyncGenerator[str, None]:
        """Yield lines from the response and close resources when done."""
        try:
            async for line in response.aiter_lines():
                if line.startswith("data: ") and line != "data: [DONE]":
                    yield line[6:]
        finally:
            await response.aclose()

    def create_chat_completion_sync(
            self, request: ChatCompletionRequest
    ) -> Union[ChatCompletionResponse, List[str]]:
        """
        Create a chat completion synchronously.
        For stream=True, returns a list of chunks (buffering), as sync generators 
        wrapping async sources are complex without external libraries.
        """
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            # If we are already in a loop (e.g. inside a callback), we can't use run_until_complete
            # This simple sync wrapper assumes it's called from a synchronous context.
            # If called from async context, user should use the async method.
            raise RuntimeError("Cannot call sync method from inside a running event loop.")

        if request.stream:
            async def _collect():
                gen = await self.create_chat_completion(request)
                results = []
                async for chunk in gen:
                    results.append(chunk)
                return results

            return loop.run_until_complete(_collect())
        else:
            return loop.run_until_complete(self.create_chat_completion(request))


class AiRagflowService:
    """RAGFlow业务服务。"""

    @staticmethod
    def _get_service() -> RAGFlowService:
        return get_ragflow_service_singleton()

    @staticmethod
    def _normalize_dataset_ids(dataset_ids: list[Any] | None) -> list[str]:
        result: list[str] = []
        seen: set[str] = set()
        for item in dataset_ids or []:
            dataset_id = str(item or "").strip()
            if not dataset_id or dataset_id in seen:
                continue
            seen.add(dataset_id)
            result.append(dataset_id)
        return result

    @staticmethod
    def _serialize_dataset_item(item: Any) -> dict[str, Any]:
        if isinstance(item, dict):
            return {
                "dataset_id": str(item.get("dataset_id") or item.get("id") or "").strip(),
                "name": item.get("name") or "",
                "description": item.get("description"),
                "document_count": item.get("document_count"),
            }

        return {
            "dataset_id": str(getattr(item, "dataset_id", None) or getattr(item, "id", None) or "").strip(),
            "name": getattr(item, "name", "") or "",
            "description": getattr(item, "description", None),
            "document_count": getattr(item, "document_count", None),
        }

    @classmethod
    async def list_datasets_service(
            cls,
            auth: AuthSchema,
            page: int = 1,
            page_size: int = 1024,
    ) -> ListDatasetsResponse:
        result = await cls._get_service().list_datasets(page=page, page_size=page_size)
        raw_items = [cls._serialize_dataset_item(item) for item in (result.data or [])]
        dataset_ids = [item["dataset_id"] for item in raw_items if item.get("dataset_id")]
        right_map = await AiDatasetAuthService.resolve_dataset_right_map(auth=auth, dataset_ids=dataset_ids)
        is_admin = AiDatasetAuthService.is_admin_user(auth)

        filtered_items = []
        for item in raw_items:
            dataset_id = item.get("dataset_id") or ""
            current_right = int(right_map.get(dataset_id, 0))
            if current_right < 1:
                continue
            filtered_items.append(
                {
                    **item,
                    "current_right": current_right,
                    "can_view": current_right >= 1,
                    "can_write": current_right >= 2,
                    "can_manage": bool(is_admin or current_right >= 2),
                    "is_admin": is_admin,
                }
            )

        return ListDatasetsResponse(
            code=result.code,
            message=result.message,
            data=filtered_items,
        )

    @classmethod
    async def create_dataset_service(
            cls,
            auth: AuthSchema,
            payload: Dict[str, Any],
    ) -> RAGFlowResponse:
        result = await cls._get_service().create_dataset(payload)
        dataset_id = ""
        if isinstance(result.data, dict):
            dataset_id = str(result.data.get("id") or result.data.get("dataset_id") or "").strip()
        if dataset_id:
            await AiDatasetAuthService.create_creator_rule(auth=auth, dataset_id=dataset_id)
        return result

    @classmethod
    async def delete_datasets_service(
            cls,
            auth: AuthSchema,
            payload: Dict[str, Any],
    ) -> RAGFlowResponse:
        dataset_ids = [str(dataset_id) for dataset_id in (payload.get("ids") or []) if dataset_id]
        if not dataset_ids:
            raise CustomException(msg="缺少可删除的知识库ID", status_code=400)

        for dataset_id in dataset_ids:
            await AiDatasetAuthService.ensure_dataset_write_permission(auth=auth, dataset_id=dataset_id)

        result = await cls._get_service().delete_datasets({**payload, "ids": dataset_ids})
        await AiDatasetAuthService.delete_dataset_auth_rules_by_dataset_ids(auth=auth, dataset_ids=dataset_ids)
        return result

    @classmethod
    async def update_dataset_service(
            cls,
            auth: AuthSchema,
            dataset_id: str,
            payload: Dict[str, Any],
    ) -> RAGFlowResponse:
        await AiDatasetAuthService.ensure_dataset_write_permission(auth=auth, dataset_id=dataset_id)
        return await cls._get_service().update_dataset(dataset_id, payload)

    @classmethod
    async def upload_documents_service(
            cls,
            auth: AuthSchema,
            dataset_id: str,
            files: List[Any],
    ) -> RAGFlowResponse:
        await AiDatasetAuthService.ensure_dataset_write_permission(auth=auth, dataset_id=dataset_id)
        return await cls._get_service().upload_documents(dataset_id, files)

    @classmethod
    async def update_document_service(
            cls,
            auth: AuthSchema,
            dataset_id: str,
            document_id: str,
            payload: Dict[str, Any],
    ) -> RAGFlowResponse:
        await AiDatasetAuthService.ensure_dataset_write_permission(auth=auth, dataset_id=dataset_id)
        return await cls._get_service().update_document(dataset_id, document_id, payload)

    @classmethod
    async def download_document_service(
            cls,
            auth: AuthSchema,
            dataset_id: str,
            document_id: str,
    ) -> Dict[str, Any]:
        await AiDatasetAuthService.ensure_dataset_read_permission(auth=auth, dataset_id=dataset_id)
        return await cls._get_service().download_document(dataset_id, document_id)

    @classmethod
    async def list_documents_service(
            cls,
            auth: AuthSchema,
            dataset_id: str,
            page: int = 1,
            page_size: int = 1024,
            run: Optional[List[str]] = None,
    ) -> ListDocumentsResponse:
        await AiDatasetAuthService.ensure_dataset_read_permission(auth=auth, dataset_id=dataset_id)
        return await cls._get_service().list_documents(
            dataset_id,
            page=page,
            page_size=page_size,
            run=run,
        )

    @classmethod
    async def delete_documents_service(
            cls,
            auth: AuthSchema,
            dataset_id: str,
            payload: Dict[str, Any],
    ) -> RAGFlowResponse:
        await AiDatasetAuthService.ensure_dataset_write_permission(auth=auth, dataset_id=dataset_id)
        return await cls._get_service().delete_documents(dataset_id, payload)

    @classmethod
    async def parse_documents_service(
            cls,
            auth: AuthSchema,
            dataset_id: str,
            payload: Dict[str, Any],
    ) -> RAGFlowResponse:
        await AiDatasetAuthService.ensure_dataset_write_permission(auth=auth, dataset_id=dataset_id)
        return await cls._get_service().parse_documents(dataset_id, payload)

    @classmethod
    async def stop_parsing_documents_service(
            cls,
            auth: AuthSchema,
            dataset_id: str,
            payload: Dict[str, Any],
    ) -> RAGFlowResponse:
        await AiDatasetAuthService.ensure_dataset_write_permission(auth=auth, dataset_id=dataset_id)
        return await cls._get_service().stop_parsing_documents(dataset_id, payload)

    @classmethod
    async def add_chunk_service(
            cls,
            auth: AuthSchema,
            dataset_id: str,
            document_id: str,
            payload: Dict[str, Any],
    ) -> RAGFlowResponse:
        await AiDatasetAuthService.ensure_dataset_write_permission(auth=auth, dataset_id=dataset_id)
        return await cls._get_service().add_chunk(dataset_id, document_id, payload)

    @classmethod
    async def list_chunks_service(
            cls,
            auth: AuthSchema,
            dataset_id: str,
            document_id: str,
            keywords: Optional[str] = None,
            page: int = 1,
            page_size: int = 1024,
            chunk_id: Optional[str] = None,
    ) -> RAGFlowResponse:
        await AiDatasetAuthService.ensure_dataset_read_permission(auth=auth, dataset_id=dataset_id)
        return await cls._get_service().list_chunks(
            dataset_id=dataset_id,
            document_id=document_id,
            keywords=keywords,
            page=page,
            page_size=page_size,
            chunk_id=chunk_id,
        )

    @classmethod
    async def delete_chunks_service(
            cls,
            auth: AuthSchema,
            dataset_id: str,
            document_id: str,
            payload: Dict[str, Any],
    ) -> RAGFlowResponse:
        await AiDatasetAuthService.ensure_dataset_write_permission(auth=auth, dataset_id=dataset_id)
        return await cls._get_service().delete_chunks(dataset_id, document_id, payload)

    @classmethod
    async def update_chunk_service(
            cls,
            auth: AuthSchema,
            dataset_id: str,
            document_id: str,
            chunk_id: str,
            payload: Dict[str, Any],
    ) -> RAGFlowResponse:
        await AiDatasetAuthService.ensure_dataset_write_permission(auth=auth, dataset_id=dataset_id)
        return await cls._get_service().update_chunk(dataset_id, document_id, chunk_id, payload)

    @classmethod
    async def retrieve_chunks_service(
            cls,
            auth: AuthSchema,
            payload: Dict[str, Any],
    ) -> RetrieveChunksResponse:
        dataset_ids = cls._normalize_dataset_ids(payload.get("dataset_ids"))
        for dataset_id in dataset_ids:
            await AiDatasetAuthService.ensure_dataset_read_permission(auth=auth, dataset_id=dataset_id)

        result = await cls._get_service().retrieve_chunks({**payload, "dataset_ids": dataset_ids})
        chunks = []
        if isinstance(result.data, dict):
            chunks = result.data.get("chunks") or []

        return RetrieveChunksResponse(
            code=result.code,
            message=result.message,
            data=[
                RetrieveChunkItem(
                    chunk_id=str(chunk.get("id") or ""),
                    content=chunk.get("content"),
                    dataset_id=chunk.get("kb_id") or chunk.get("dataset_id"),
                    document_id=chunk.get("document_id"),
                    document_keyword=chunk.get("document_keyword"),
                    similarity=chunk.get("similarity"),
                    positions=chunk.get("positions"),
                )
                for chunk in chunks
            ],
        )

    @classmethod
    async def retrieve_agent_knowledge_chunks_service(
            cls,
            auth: AuthSchema,
            conversation_id: int,
            payload: Dict[str, Any],
    ) -> RetrieveChunksResponse:
        allowed_dataset_ids = cls._normalize_dataset_ids(
            await AiChatService.get_agent_knowledge_dataset_ids_by_conversation(
                auth=auth,
                conversation_id=conversation_id,
            )
        )
        if not allowed_dataset_ids:
            raise CustomException(msg="当前智能体未配置可检索知识库", status_code=400)

        return await cls.retrieve_chunks_service(
            auth=auth,
            payload={
                **payload,
                "dataset_ids": allowed_dataset_ids,
                "document_ids": [],
            }
        )

    @classmethod
    async def list_dataset_auth_rules_service(
            cls,
            auth: AuthSchema,
            dataset_id: str,
    ) -> list[AiDatasetAuthRuleOutSchema]:
        await AiDatasetAuthService.ensure_dataset_write_permission(auth=auth, dataset_id=dataset_id)
        return await AiDatasetAuthService.list_dataset_auth_rules(auth=auth, dataset_id=dataset_id)

    @classmethod
    async def update_dataset_auth_rules_service(
            cls,
            auth: AuthSchema,
            dataset_id: str,
            rules: list[AiDatasetAuthRuleSchema] | None,
    ) -> list[AiDatasetAuthRuleOutSchema]:
        await AiDatasetAuthService.ensure_dataset_write_permission(auth=auth, dataset_id=dataset_id)
        return await AiDatasetAuthService.replace_dataset_auth_rules(
            auth=auth,
            dataset_id=dataset_id,
            rules=rules,
        )


_ragflow_service_singleton: Optional[RAGFlowService] = None


def get_ragflow_service_singleton() -> RAGFlowService:
    """Get the process-local singleton RAGFlowService instance."""
    global _ragflow_service_singleton
    if _ragflow_service_singleton is None:
        _ragflow_service_singleton = RAGFlowService()
    return _ragflow_service_singleton


async def close_ragflow_service_singleton() -> None:
    """Close and clear the process-local singleton RAGFlowService instance."""
    global _ragflow_service_singleton
    if _ragflow_service_singleton is None:
        return
    await _ragflow_service_singleton.close()
    _ragflow_service_singleton = None
