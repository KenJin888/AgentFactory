import request from "@/utils/request";

const API_PATH = "/ai/knowledge_base";

const AiKnowledgeBaseAPI = {
  // 列出目录内容
  listDirectory(conversationId: number, query?: KnowledgeBaseListQuery) {
    return request<ApiResponse<KnowledgeBaseItem[]>>({
      url: `${API_PATH}/${conversationId}/list`,
      method: "get",
      params: query,
    });
  },

  // 创建目录
  createDirectory(conversationId: number, body: KnowledgeBaseDirectoryCreate) {
    return request<ApiResponse>({
      url: `${API_PATH}/${conversationId}/directory/create`,
      method: "post",
      data: body,
    });
  },

  // 删除文件或目录
  deletePath(conversationId: number, body: KnowledgeBaseDeleteRequest) {
    return request<ApiResponse>({
      url: `${API_PATH}/${conversationId}/delete`,
      method: "delete",
      data: body,
    });
  },

  // 创建文件
  createFile(conversationId: number, body: KnowledgeBaseFileCreate) {
    return request<ApiResponse>({
      url: `${API_PATH}/${conversationId}/file/create`,
      method: "post",
      data: body,
    });
  },

  // 读取文件内容
  readFile(conversationId: number, body: KnowledgeBaseFileRead) {
    return request<ApiResponse<KnowledgeBaseFileContent>>({
      url: `${API_PATH}/${conversationId}/file/read`,
      method: "post",
      data: body,
    });
  },

  // 更新文件内容
  updateFile(conversationId: number, body: KnowledgeBaseFileUpdate) {
    return request<ApiResponse>({
      url: `${API_PATH}/${conversationId}/file/update`,
      method: "put",
      data: body,
    });
  },

  // 上传文件
  uploadFile(conversationId: number, body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/${conversationId}/file/upload`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  // 下载文件
  downloadFile(conversationId: number, query: KnowledgeBaseFileDownload) {
    return request<Blob>({
      url: `${API_PATH}/${conversationId}/file/download`,
      method: "get",
      params: query,
      responseType: "blob",
    });
  },
};

export default AiKnowledgeBaseAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface KnowledgeBaseListQuery {
  path?: string;
}

// 知识库项（文件或目录）
export interface KnowledgeBaseItem {
  // 可能的字段名变体
  name?: string;
  filename?: string;
  file_name?: string;
  title?: string;

  path: string;
  type: "file" | "directory";
  size?: number;
  modified_time?: string;
  modified?: string;
  created_time?: string;
  created?: string;
  is_dir?: boolean;
  is_file?: boolean;
}

// 创建目录请求
export interface KnowledgeBaseDirectoryCreate {
  path: string;
}

// 删除文件/目录请求
export interface KnowledgeBaseDeleteRequest {
  path: string;
}

// 创建文件请求
export interface KnowledgeBaseFileCreate {
  path: string;
  content?: string;
}

// 读取文件请求
export interface KnowledgeBaseFileRead {
  path: string;
}

// 文件内容响应
export interface KnowledgeBaseFileContent {
  content?: string;
  url?: string;
  path: string;
  size: number;
  modified_time: string;
}

// 更新文件请求
export interface KnowledgeBaseFileUpdate {
  path: string;
  content: string;
}

// 下载文件请求
export interface KnowledgeBaseFileDownload {
  path: string;
}