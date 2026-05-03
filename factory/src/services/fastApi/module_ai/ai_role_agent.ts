import request from "@/utils/request";

const API_PATH = "/ai/ai_role_agent";

const AiRoleAgentAPI = {
  // 列表查询
  listAiRoleAgent(query: AiRoleAgentPageQuery) {
    return request<ApiResponse<PageResult<AiRoleAgentTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailAiRoleAgent(id: number) {
    return request<ApiResponse<AiRoleAgentTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createAiRoleAgent(body: AiRoleAgentForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateAiRoleAgent(id: number, body: AiRoleAgentForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteAiRoleAgent(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchAiRoleAgent(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportAiRoleAgent(query: AiRoleAgentPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateAiRoleAgent() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importAiRoleAgent(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: {"Content-Type": "multipart/form-data"},
    });
  },
};

export default AiRoleAgentAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface AiRoleAgentPageQuery extends PageQuery {
  role_id?: string;
  agent_id?: string;
  permission?: string;
  status?: string;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface AiRoleAgentTable extends BaseType {
  role_id?: string;
  agent_id?: string;
  permission?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface AiRoleAgentForm extends BaseFormType {
  role_id?: string;
  agent_id?: string;
  permission?: string;
}
