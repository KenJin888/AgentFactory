from typing import List, Optional, Any

from pydantic import BaseModel, Field, ConfigDict


class ChatMessage(BaseModel):
    role: str = Field(..., description="The role of the message sender (system, user, assistant)")
    content: str = Field(..., description="The content of the message")


class ChatCompletionRequest(BaseModel):
    model: str = Field(..., description="ID of the model to use")
    messages: List[ChatMessage] = Field(..., description="A list of messages comprising the conversation so far")
    stream: Optional[bool] = Field(default=False, description="If set, partial message deltas will be sent")
    temperature: Optional[float] = Field(default=None, description="Sampling temperature")
    max_tokens: Optional[int] = Field(default=None, description="The maximum number of tokens to generate")


class ChoiceDelta(BaseModel):
    content: Optional[str] = None
    role: Optional[str] = None


class Choice(BaseModel):
    index: int
    message: Optional[ChatMessage] = None
    delta: Optional[ChoiceDelta] = None
    finish_reason: Optional[str] = None


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Optional[Usage] = None


class Dataset(BaseModel):
    dataset_id: str
    name: str
    description: Optional[str] = None
    document_count: Optional[int] = None
    current_right: int = 0
    can_view: bool = False
    can_write: bool = False
    can_manage: bool = False
    is_admin: bool = False


class ListDatasetsResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: List[Dataset]


class RetrieveChunkItem(BaseModel):
    chunk_id: str
    content: Optional[str] = None
    dataset_id: Optional[str] = None
    document_id: Optional[str] = None
    document_keyword: Optional[str] = None
    similarity: Optional[float] = None
    positions: Optional[list[Any]] = None


class RetrieveChunksResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: List[RetrieveChunkItem]


class RAGFlowResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: Any = None


class RetrieveChunksPayload(BaseModel):
    question: str = Field(..., description="检索问题")
    dataset_ids: list[str] = Field(default_factory=list, description="知识库ID列表")
    document_ids: list[str] = Field(default_factory=list, description="文档ID列表")
    page: int = Field(default=1, description="页码")
    page_size: int = Field(default=10, description="每页数量")
    similarity_threshold: float = Field(default=0.2, description="相似度阈值")
    vector_similarity_weight: float = Field(default=0.3, description="向量相似度权重")
    top_k: int = Field(default=8, description="召回数量")
    rerank_id: str = Field(default="", description="重排模型ID")
    keyword: bool = Field(default=False, description="是否启用关键词检索")
    highlight: bool = Field(default=False, description="是否高亮")
    cross_languages: list[str] = Field(default_factory=list, description="跨语言列表")
    metadata_condition: dict[str, Any] = Field(default_factory=dict, description="元数据过滤条件")
    use_kg: bool = Field(default=False, description="是否启用知识图谱")


class AgentRetrieveChunksPayload(BaseModel):
    question: str = Field(..., description="检索问题")
    page: int = Field(default=1, description="页码")
    page_size: int = Field(default=10, description="每页数量")
    similarity_threshold: float = Field(default=0.2, description="相似度阈值")
    vector_similarity_weight: float = Field(default=0.3, description="向量相似度权重")
    top_k: int = Field(default=8, description="召回数量")
    rerank_id: str = Field(default="", description="重排模型ID")
    keyword: bool = Field(default=False, description="是否启用关键词检索")
    highlight: bool = Field(default=False, description="是否高亮")
    cross_languages: list[str] = Field(default_factory=list, description="跨语言列表")
    metadata_condition: dict[str, Any] = Field(default_factory=dict, description="元数据过滤条件")
    use_kg: bool = Field(default=False, description="是否启用知识图谱")


class Document(BaseModel):
    id: str
    name: Optional[str] = None
    run: Optional[str] = None
    progress: Optional[float] = None
    status: Optional[str] = None
    size: Optional[int] = None
    chunk_count: Optional[int] = None
    create_date: Optional[str] = None
    update_date: Optional[str] = None

    model_config = ConfigDict(extra="allow")


class ListDocumentsResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: List[Document]
