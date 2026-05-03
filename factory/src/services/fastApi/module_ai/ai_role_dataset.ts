import request from "@/utils/request";

const API_PATH = "/ai/ai_role_dataset";

const AiRoleDatasetAPI = {
  // 列表查询
  listAiRoleDataset(query: AiRoleDatasetPageQuery) {
    return request<ApiResponse<PageResult<AiRoleDatasetTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailAiRoleDataset(id: number) {
    return request<ApiResponse<AiRoleDatasetTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createAiRoleDataset(body: AiRoleDatasetForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateAiRoleDataset(id: number, body: AiRoleDatasetForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteAiRoleDataset(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchAiRoleDataset(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportAiRoleDataset(query: AiRoleDatasetPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateAiRoleDataset() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importAiRoleDataset(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: {"Content-Type": "multipart/form-data"},
    });
  },
};

export default AiRoleDatasetAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface AiRoleDatasetPageQuery extends PageQuery {
  role_id?: string;
  datasets_id?: string;
  permission?: string;
  status?: string;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface AiRoleDatasetTable extends BaseType {
  role_id?: string;
  datasets_id?: string;
  permission?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface AiRoleDatasetForm extends BaseFormType {
  role_id?: string;
  datasets_id?: string;
  permission?: string;
}
