import request from "@/utils/request";

const API_PATH = "/ai/ai_ragflow";

const AiRagflowAPI = {
  // List datasets
  listDatasets(query: DatasetPageQuery) {
    return request<ListDatasetsResponse>({
      url: `${API_PATH}/datasets`,
      method: "get",
      params: query,
    });
  },

  createDataset(body: Record<string, any>) {
    return request<RAGFlowResponse>({
      url: `${API_PATH}/datasets`,
      method: "post",
      data: body,
    });
  },

  deleteDatasets(body: Record<string, any>) {
    return request<RAGFlowResponse>({
      url: `${API_PATH}/datasets`,
      method: "delete",
      data: body,
    });
  },

  updateDataset(datasetId: string, body: Record<string, any>) {
    return request<RAGFlowResponse>({
      url: `${API_PATH}/datasets/${datasetId}`,
      method: "put",
      data: body,
    });
  },

  uploadDocuments(datasetId: string, formData: FormData) {
    return request<RAGFlowResponse>({
      url: `${API_PATH}/datasets/${datasetId}/documents`,
      method: "post",
      data: formData,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  updateDocument(datasetId: string, documentId: string, body: Record<string, any>) {
    return request<RAGFlowResponse>({
      url: `${API_PATH}/datasets/${datasetId}/documents/${documentId}`,
      method: "put",
      data: body,
    });
  },

  downloadDocument(datasetId: string, documentId: string) {
    return request<Blob>({
      url: `${API_PATH}/datasets/${datasetId}/documents/${documentId}/download`,
      method: "get",
      responseType: "blob",
    });
  },

  listDocuments(datasetId: string, query: DocumentPageQuery) {
    return request<ListDocumentsResponse>({
      url: `${API_PATH}/datasets/${datasetId}/documents`,
      method: "get",
      params: query,
    });
  },

    listDatasetAuthRules(datasetId: string) {
        return request<RAGFlowResponse<DatasetAuthRule[]>>({
            url: `${API_PATH}/datasets/${datasetId}/auth`,
            method: "get",
        });
    },

    updateDatasetAuthRules(datasetId: string, body: DatasetAuthRulesPayload) {
        return request<RAGFlowResponse<DatasetAuthRule[]>>({
            url: `${API_PATH}/datasets/${datasetId}/auth`,
            method: "put",
            data: body,
        });
    },

  deleteDocuments(datasetId: string, body: Record<string, any>) {
    console.log("deleteDocuments body:", body);
    return request<RAGFlowResponse>({
      url: `${API_PATH}/datasets/${datasetId}/documents`,
      method: "delete",
      data: body,
    });
  },

  parseDocuments(datasetId: string, body: Record<string, any>) {
    return request<RAGFlowResponse>({
      url: `${API_PATH}/datasets/${datasetId}/chunks`,
      method: "post",
      data: body,
    });
  },

  stopParsingDocuments(datasetId: string, body: Record<string, any>) {
    return request<RAGFlowResponse>({
      url: `${API_PATH}/datasets/${datasetId}/chunks/stop`,
      method: "delete",
      data: body,
    });
  },

  addChunk(datasetId: string, documentId: string, body: Record<string, any>) {
    return request<RAGFlowResponse>({
      url: `${API_PATH}/datasets/${datasetId}/documents/${documentId}/chunks`,
      method: "post",
      data: body,
    });
  },

  listChunks(datasetId: string, documentId: string, query: ChunkListQuery = {}) {
    return request<RAGFlowResponse>({
      url: `${API_PATH}/datasets/${datasetId}/documents/${documentId}/chunks`,
      method: "get",
      params: query,
    });
  },

  deleteChunks(datasetId: string, documentId: string, body: Record<string, any>) {
    return request<RAGFlowResponse>({
      url: `${API_PATH}/datasets/${datasetId}/documents/${documentId}/chunks`,
      method: "delete",
      data: body,
    });
  },

  updateChunk(datasetId: string, documentId: string, chunkId: string, body: Record<string, any>) {
    return request<RAGFlowResponse>({
      url: `${API_PATH}/datasets/${datasetId}/documents/${documentId}/chunks/${chunkId}`,
      method: "put",
      data: body,
    });
  },

  retrieveChunks(body: Record<string, any>) {
    return request<RAGFlowResponse>({
      url: `${API_PATH}/retrieval`,
      method: "post",
      data: body,
    });
  },

  // Create chat completion
  chatCompletions(body: ChatCompletionRequest) {
    return request<ChatCompletionResponse | any>({
      url: `${API_PATH}/chat/completions`,
      method: "post",
      data: body,
      // If handling stream, the caller needs to handle the response appropriately
    });
  },
};

export default AiRagflowAPI;

// ------------------------------
// TS Type Declarations
// ------------------------------

export interface DatasetPageQuery {
  page?: number;
  page_size?: number;
}

export interface DocumentPageQuery {
  page?: number;
  page_size?: number;
  run?: string[];
}

export interface ChunkListQuery {
  page?: number;
  page_size?: number;
  keywords?: string;
  id?: string;
}

export interface Dataset {
  id: string;
  name: string;
  avatar?: string;
  tenant_id?: string;
  description?: string;
  language?: string;
  document_count?: number;
  chunk_count?: number;
  parse_method?: string;
  create_date?: string;
  update_date?: string;
  created_by?: string;
  updated_by?: string;
    current_right?: 0 | 1 | 2;
    can_view?: boolean;
    can_write?: boolean;
    can_manage?: boolean;
    is_admin?: boolean;
  [key: string]: any;
}

export interface DatasetAuthRule {
    id?: number | null;
    target_type: "global" | "role" | "user";
    target_value?: string | null;
    target_label?: string | null;
    target_right: 1 | 2;
    granted_by?: number | null;
    granted_at?: string | null;
    is_default?: boolean;
}

export interface DatasetAuthRulesPayload {
    auth_rules: Array<{
        target_type: "global" | "role" | "user";
        target_value?: string | null;
        target_right: 1 | 2;
    }>;
}

// Response wrapper matching Python's ListDatasetsResponse
export interface ListDatasetsResponse {
  code: number;
  message: string;
  data: Dataset[];
}

export interface RAGFlowResponse<T = any> {
  code: number;
  message: string;
  data: T;
}

export interface Document {
  id: string;
  name?: string;
  run?: string;
  progress?: number;
  status?: string;
  size?: number;
  chunk_count?: number;
  create_date?: string;
  update_date?: string;
  [key: string]: any;
}

export interface ListDocumentsResponse {
  code: number;
  message: string;
  data: Document[];
}

export interface ChatMessage {
  role: string;
  content: string;
}

export interface ChatCompletionRequest {
  model: string;
  messages: ChatMessage[];
  stream?: boolean;
  temperature?: number;
  max_tokens?: number;
}

export interface ChoiceDelta {
  content?: string;
  role?: string;
}

export interface Choice {
  index: number;
  message?: ChatMessage;
  delta?: ChoiceDelta;
  finish_reason?: string;
}

export interface Usage {
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
}

export interface ChatCompletionResponse {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: Choice[];
  usage?: Usage;
}
