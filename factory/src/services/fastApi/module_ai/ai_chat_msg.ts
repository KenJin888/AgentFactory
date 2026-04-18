import request from "@/utils/request";

const API_PATH = "/ai/ai_chat_msg";

const AiChatMsgAPI = {
  // 列表查询
  listAiChatMsg(query: AiChatMsgPageQuery) {
    return request<ApiResponse<PageResult<AiChatMsgTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailAiChatMsg(id: number) {
    return request<ApiResponse<AiChatMsgTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createAiChatMsg(body: AiChatMsgForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateAiChatMsg(id: number, body: AiChatMsgForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteAiChatMsg(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchAiChatMsg(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportAiChatMsg(query: AiChatMsgPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateAiChatMsg() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importAiChatMsg(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default AiChatMsgAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface AiChatMsgPageQuery extends PageQuery {
  status?: string;
  created_id?: number;
  updated_id?: number;
  chat_id?: string;
  role?: string;
  order_seq?: string;
  token_count?: string;
  parent_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface AiChatMsgTable extends BaseType {
  created_id?: string;
  updated_id?: string;
  chat_id?: string;
  role?: string;
  content?: string;
  order_seq?: string;
  token_count?: string;
  status?: string;
  parent_id?: number;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface AiChatMsgForm extends BaseFormType {
  chat_id?: string;
  role?: string;
  content?: string;
  order_seq?: string;
  token_count?: string;
  status?: string;
  parent_id?: number;
}
