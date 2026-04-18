import request from "@/utils/request";

const API_PATH = "/ai/ai";

const AiAgentAPI = {
  // 列表查询
  listAiAgent(query: AiAgentPageQuery) {
    return request<ApiResponse<PageResult<AiAgentTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailAiAgent(id: number) {
    return request<ApiResponse<AiAgentTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createAiAgent(body: AiAgentForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateAiAgent(id: number, body: AiAgentForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteAiAgent(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchAiAgent(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportAiAgent(query: AiAgentPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateAiAgent() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importAiAgent(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default AiAgentAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface AiAgentPageQuery extends PageQuery {
  status?: string;
  created_id?: number;
  updated_id?: number;
  name?: string;
  type?: string;
  config?: string;
  prompt_template?: string;
  model?: string;
  cover?: string;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface AiAgentTable extends BaseType {
  created_id?: string;
  updated_id?: string;
  name?: string;
  type?: string;
  config?: string;
  prompt_template?: string;
  model?: string;
  cover?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface AiAgentForm extends BaseFormType {
  name?: string;
  type?: string;
  config?: string;
  prompt_template?: string;
  model?: string;
  cover?: string;
}
