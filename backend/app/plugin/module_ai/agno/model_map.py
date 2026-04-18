from typing import Any

from agno.models.ollama import Ollama
from agno.models.openai import OpenAIChat
from agno.models.openai.like import OpenAILike
from agno.models.siliconflow import Siliconflow

_PROVIDER_MODEL_MAP: dict[str, type[Any]] = {
    "openai": OpenAIChat,
    "deepseek": OpenAILike,
    "doubao": OpenAILike,
    "modelscope": OpenAILike,
    "alibaba-cn": OpenAILike,
    "xiaomi": OpenAILike,
    "opencode": OpenAILike,
    "minimax-cn": OpenAILike,
    "moonshot": OpenAILike,
    "bailing": OpenAILike,
    "zhipuai": OpenAILike,
    "siliconflow": Siliconflow,
    "ollama": Ollama,
    "openai_compatible": OpenAILike,
}

'''
    "huggingface": HuggingFace,
    "claude": Claude,
    "gemini": Gemini,
    "v0": V0,
    "xai": xAI,
    "vllm": VLLM,
    "lmstudio": LMStudio,
    "openrouter": OpenRouter, 
'''


def create_model(
        provider: str | None = None,
        model: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        temperature: float | None = None,
) -> Any:
    if not provider:
        raise ValueError("AI provider is required")
    provider_key = provider.strip().lower().replace("-", "_")
    model_class = _PROVIDER_MODEL_MAP.get(provider_key)
    if model_class is None:
        supported = ", ".join(sorted(_PROVIDER_MODEL_MAP.keys()))
        raise ValueError(f"Unsupported AI provider: {provider}. Supported providers: {supported}")

    return model_class(
        api_key=api_key,
        id=model,
        base_url=base_url,
        temperature=temperature,
    )
