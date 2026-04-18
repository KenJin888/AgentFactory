from typing import Any, Dict, List, Optional
from urllib.parse import quote, unquote

from fastapi import APIRouter, HTTPException, Depends, Body, UploadFile, File, Query, Request
from fastapi.responses import Response

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.dependencies import AuthPermission
from app.core.exceptions import CustomException
from app.plugin.module_ai.ai_dataset_auth.schema import (
    AiDatasetAuthRulesPayload,
    AiDatasetAuthRulesResponse,
)
from .schema import (
    AgentRetrieveChunksPayload,
    ListDatasetsResponse,
    ListDocumentsResponse,
    RAGFlowResponse,
    RetrieveChunksResponse,
    RetrieveChunksPayload,
)
from .service import AiRagflowService, RAGFlowAPIError

router = APIRouter(prefix='/ai_ragflow', tags=["ai_ragflow模块"])


def _sanitize_ascii_filename(filename: str, fallback: str = "download") -> str:
    cleaned = "".join(
        ch if 32 <= ord(ch) < 127 and ch not in {'"', "\\"} else "_" for ch in filename
    )
    cleaned = cleaned.strip(" ._")
    return cleaned or fallback


def _build_content_disposition(filename: str) -> str:
    raw_name = unquote(filename)
    ascii_name = _sanitize_ascii_filename(raw_name)
    quoted_name = quote(raw_name, safe="")
    return f'attachment; filename="{ascii_name}"; filename*=UTF-8\'\'{quoted_name}'


def _raise_ragflow_http_exception(exc: RAGFlowAPIError) -> None:
    raise HTTPException(
        status_code=exc.http_code,
        detail={
            "error_code": exc.error_code,
            "error_msg": exc.error_msg,
            "trace_id": exc.trace_id,
        },
    )


def _get_required_positive_int_header(request: Request, header_name: str, error_message: str) -> int:
    raw_value = str(request.headers.get(header_name) or "").strip()
    if not raw_value:
        raise HTTPException(status_code=400, detail=error_message)

    try:
        value = int(raw_value)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=error_message) from exc

    if value <= 0:
        raise HTTPException(status_code=400, detail=error_message)

    return value


@router.get(
    "/datasets",
    response_model=ListDatasetsResponse,
    summary="List datasets",
    description="List datasets from RAGFlow service.",
    operation_id="list_datasets",
)
async def list_datasets(
        page: int = 1,
        page_size: int = 1024,
        auth: AuthSchema = Depends(AuthPermission()),
):
    try:
        return await AiRagflowService.list_datasets_service(auth=auth, page=page, page_size=page_size)
    except RAGFlowAPIError as e:
        _raise_ragflow_http_exception(e)
    except CustomException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/datasets",
    response_model=RAGFlowResponse,
    summary="Create dataset",
    description="Create dataset from RAGFlow service.",
)
async def create_dataset(
        payload: Dict[str, Any] = Body(...),
        auth: AuthSchema = Depends(AuthPermission()),
):
    try:
        return await AiRagflowService.create_dataset_service(auth=auth, payload=payload)
    except RAGFlowAPIError as e:
        _raise_ragflow_http_exception(e)
    except CustomException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/datasets",
    response_model=RAGFlowResponse,
    summary="Delete datasets",
    description="Delete datasets from RAGFlow service.",
)
async def delete_datasets(
        payload: Dict[str, Any] = Body(...),
        auth: AuthSchema = Depends(AuthPermission()),
):
    try:
        return await AiRagflowService.delete_datasets_service(auth=auth, payload=payload)
    except RAGFlowAPIError as e:
        _raise_ragflow_http_exception(e)
    except CustomException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/datasets/{dataset_id}",
    response_model=RAGFlowResponse,
    summary="Update dataset",
    description="Update dataset from RAGFlow service.",
)
async def update_dataset(
        dataset_id: str,
        payload: Dict[str, Any] = Body(...),
        auth: AuthSchema = Depends(AuthPermission()),
):
    try:
        return await AiRagflowService.update_dataset_service(auth=auth, dataset_id=dataset_id, payload=payload)
    except RAGFlowAPIError as e:
        _raise_ragflow_http_exception(e)
    except CustomException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/datasets/{dataset_id}/documents",
    response_model=RAGFlowResponse,
    summary="Upload documents",
    description="Upload documents to dataset from RAGFlow service.",
)
async def upload_documents(
        dataset_id: str,
        file: List[UploadFile] = File(...),
        auth: AuthSchema = Depends(AuthPermission()),
):
    try:
        return await AiRagflowService.upload_documents_service(auth=auth, dataset_id=dataset_id, files=file)
    except RAGFlowAPIError as e:
        _raise_ragflow_http_exception(e)
    except CustomException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/datasets/{dataset_id}/documents/{document_id}",
    response_model=RAGFlowResponse,
    summary="Update document",
    description="Update document from RAGFlow service.",
)
async def update_document(
        dataset_id: str,
        document_id: str,
        payload: Dict[str, Any] = Body(...),
        auth: AuthSchema = Depends(AuthPermission()),
):
    try:
        return await AiRagflowService.update_document_service(
            auth=auth,
            dataset_id=dataset_id,
            document_id=document_id,
            payload=payload,
        )
    except RAGFlowAPIError as e:
        _raise_ragflow_http_exception(e)
    except CustomException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/datasets/{dataset_id}/documents/{document_id}/download",
    summary="Download document",
    description="Download document from RAGFlow service.",
)
async def download_document(
        dataset_id: str,
        document_id: str,
        auth: AuthSchema = Depends(AuthPermission()),
):
    try:
        result = await AiRagflowService.download_document_service(
            auth=auth,
            dataset_id=dataset_id,
            document_id=document_id,
        )
        headers = {"Content-Disposition": _build_content_disposition(result["filename"])}
        return Response(content=result["content"], media_type=result["content_type"], headers=headers)
    except RAGFlowAPIError as e:
        _raise_ragflow_http_exception(e)
    except CustomException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/datasets/{dataset_id}/documents",
    response_model=ListDocumentsResponse,
    summary="List documents",
    description="List documents from RAGFlow service.",
    operation_id="list_documents",
)
async def list_documents(
        dataset_id: str,
        page: int = 1,
        page_size: int = 1024,
        run: Optional[List[str]] = Query(
            default=None,
            description=(
                    "按文档解析状态过滤，支持数字/文本/混合格式："
                    "0|UNSTART, 1|RUNNING, 2|CANCEL, 3|DONE, 4|FAIL。"
                    "不传则返回全部状态。"
            ),
        ),
        auth: AuthSchema = Depends(AuthPermission()),
):
    try:
        return await AiRagflowService.list_documents_service(
            auth=auth,
            dataset_id=dataset_id,
            page=page,
            page_size=page_size,
            run=run,
        )
    except RAGFlowAPIError as e:
        _raise_ragflow_http_exception(e)
    except CustomException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/datasets/{dataset_id}/documents",
    response_model=RAGFlowResponse,
    summary="Delete documents",
    description="Delete documents from RAGFlow service.",
)
async def delete_documents(
        dataset_id: str,
        payload: Dict[str, Any] = Body(...),
        auth: AuthSchema = Depends(AuthPermission()),
):
    try:
        return await AiRagflowService.delete_documents_service(auth=auth, dataset_id=dataset_id, payload=payload)
    except RAGFlowAPIError as e:
        _raise_ragflow_http_exception(e)
    except CustomException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/datasets/{dataset_id}/chunks",
    response_model=RAGFlowResponse,
    summary="Parse documents",
    description="Parse documents from RAGFlow service.",
)
async def parse_documents(
        dataset_id: str,
        payload: Dict[str, Any] = Body(...),
        auth: AuthSchema = Depends(AuthPermission()),
):
    try:
        return await AiRagflowService.parse_documents_service(auth=auth, dataset_id=dataset_id, payload=payload)
    except RAGFlowAPIError as e:
        _raise_ragflow_http_exception(e)
    except CustomException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/datasets/{dataset_id}/chunks/stop",
    response_model=RAGFlowResponse,
    summary="Stop parsing documents",
    description="Stop parsing documents from RAGFlow service.",
)
async def stop_parsing_documents(
        dataset_id: str,
        payload: Dict[str, Any] = Body(...),
        auth: AuthSchema = Depends(AuthPermission()),
):
    try:
        return await AiRagflowService.stop_parsing_documents_service(
            auth=auth,
            dataset_id=dataset_id,
            payload=payload,
        )
    except RAGFlowAPIError as e:
        _raise_ragflow_http_exception(e)
    except CustomException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/datasets/{dataset_id}/documents/{document_id}/chunks",
    response_model=RAGFlowResponse,
    summary="Add chunk",
    description="Add chunk to document from RAGFlow service.",
)
async def add_chunk(
        dataset_id: str,
        document_id: str,
        payload: Dict[str, Any] = Body(...),
        auth: AuthSchema = Depends(AuthPermission()),
):
    try:
        return await AiRagflowService.add_chunk_service(
            auth=auth,
            dataset_id=dataset_id,
            document_id=document_id,
            payload=payload,
        )
    except RAGFlowAPIError as e:
        _raise_ragflow_http_exception(e)
    except CustomException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/datasets/{dataset_id}/documents/{document_id}/chunks",
    response_model=RAGFlowResponse,
    summary="List chunks",
    description="List chunks in a document from RAGFlow service.",
)
async def list_chunks(
        dataset_id: str,
        document_id: str,
        keywords: Optional[str] = None,
        page: int = 1,
        page_size: int = 1024,
        chunk_id: Optional[str] = Query(default=None, alias="id"),
        auth: AuthSchema = Depends(AuthPermission()),
):
    try:
        return await AiRagflowService.list_chunks_service(
            auth=auth,
            dataset_id=dataset_id,
            document_id=document_id,
            keywords=keywords,
            page=page,
            page_size=page_size,
            chunk_id=chunk_id,
        )
    except RAGFlowAPIError as e:
        _raise_ragflow_http_exception(e)
    except CustomException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/datasets/{dataset_id}/documents/{document_id}/chunks",
    response_model=RAGFlowResponse,
    summary="Delete chunks",
    description="Delete chunks in a document from RAGFlow service.",
)
async def delete_chunks(
        dataset_id: str,
        document_id: str,
        payload: Dict[str, Any] = Body(...),
        auth: AuthSchema = Depends(AuthPermission()),
):
    try:
        return await AiRagflowService.delete_chunks_service(
            auth=auth,
            dataset_id=dataset_id,
            document_id=document_id,
            payload=payload,
        )
    except RAGFlowAPIError as e:
        _raise_ragflow_http_exception(e)
    except CustomException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/datasets/{dataset_id}/documents/{document_id}/chunks/{chunk_id}",
    response_model=RAGFlowResponse,
    summary="Update chunk",
    description="Update a chunk in a document from RAGFlow service.",
)
async def update_chunk(
        dataset_id: str,
        document_id: str,
        chunk_id: str,
        payload: Dict[str, Any] = Body(...),
        auth: AuthSchema = Depends(AuthPermission()),
):
    try:
        return await AiRagflowService.update_chunk_service(
            auth=auth,
            dataset_id=dataset_id,
            document_id=document_id,
            chunk_id=chunk_id,
            payload=payload,
        )
    except RAGFlowAPIError as e:
        _raise_ragflow_http_exception(e)
    except CustomException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/retrieval",
    response_model=RetrieveChunksResponse,
    summary="Retrieve chunks",
    description="Retrieve chunks from datasets/documents in RAGFlow service.",
    operation_id="retrieve_chunks",
)
async def retrieve_chunks(
        payload: RetrieveChunksPayload = Body(...),
        auth: AuthSchema = Depends(AuthPermission()),
):
    try:
        return await AiRagflowService.retrieve_chunks_service(
            auth=auth,
            payload=payload.model_dump(exclude_none=True),
        )
    except RAGFlowAPIError as e:
        _raise_ragflow_http_exception(e)
    except CustomException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/datasets/{dataset_id}/auth",
    response_model=AiDatasetAuthRulesResponse,
    summary="List dataset auth rules",
    description="List auth rules for dataset.",
)
async def list_dataset_auth_rules(
        dataset_id: str,
        auth: AuthSchema = Depends(AuthPermission()),
):
    try:
        return AiDatasetAuthRulesResponse(
            data=await AiRagflowService.list_dataset_auth_rules_service(auth=auth, dataset_id=dataset_id)
        )
    except RAGFlowAPIError as e:
        _raise_ragflow_http_exception(e)
    except CustomException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/datasets/{dataset_id}/auth",
    response_model=AiDatasetAuthRulesResponse,
    summary="Update dataset auth rules",
    description="Replace auth rules for dataset.",
)
async def update_dataset_auth_rules(
        dataset_id: str,
        payload: AiDatasetAuthRulesPayload = Body(...),
        auth: AuthSchema = Depends(AuthPermission()),
):
    try:
        return AiDatasetAuthRulesResponse(
            data=await AiRagflowService.update_dataset_auth_rules_service(
                auth=auth,
                dataset_id=dataset_id,
                rules=payload.auth_rules,
            )
        )
    except RAGFlowAPIError as e:
        _raise_ragflow_http_exception(e)
    except CustomException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/retrieval/agent",
    response_model=RetrieveChunksResponse,
    summary="Retrieve agent knowledge chunks",
    description="Retrieve chunks only from the current conversation agent configured datasets.",
    operation_id="retrieve_agent_knowledge_chunks",
)
async def retrieve_agent_knowledge_chunks(
        request: Request,
        payload: AgentRetrieveChunksPayload = Body(...),
        auth: AuthSchema = Depends(AuthPermission(check_data_scope=False)),
):
    try:
        conversation_id = _get_required_positive_int_header(
            request,
            "X-AI-Conversation-Id",
            "缺少MCP会话上下文",
        )
        return await AiRagflowService.retrieve_agent_knowledge_chunks_service(
            auth=auth,
            conversation_id=conversation_id,
            payload=payload.model_dump(exclude_none=True),
        )
    except RAGFlowAPIError as e:
        _raise_ragflow_http_exception(e)
    except CustomException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

