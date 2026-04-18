import request from "@/utils/request";
import type {AxiosResponse} from "axios";

const API_PATH = "/ai/ai_agent";

const AiAgentAPI = {
  // 列表查询
  listAiAgent(query: AiAgentPageQuery) {
    return request<ApiResponse<PageResult<AiAgentTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 我的私有智能体列表
  listMyAiAgent(query: AiAgentPageQuery) {
    return request<ApiResponse<PageResult<AiAgentTable[]>>>({
      url: `${API_PATH}/my/list`,
      method: "get",
      params: query,
    });
  },

  // 企业广场智能体列表
  listSquareAiAgent(query: AiAgentPageQuery) {
    return request<ApiResponse<PageResult<AiAgentTable[]>>>({
      url: `${API_PATH}/square/list`,
      method: "get",
      params: query,
    });
  },

  // 我的收藏智能体列表
  listFavoriteAiAgent() {
    return request<ApiResponse<AiAgentTable[]>>({
      url: `${API_PATH}/favorite/list`,
      method: "get",
    });
  },

    // 当前用户可绑定知识库列表
    listAvailableKnowledgeDatasets(query: { page?: number; page_size?: number }) {
        return request<ApiResponse<AiAgentKnowledgeDataset[]>>({
            url: `${API_PATH}/knowledge/datasets`,
            method: "get",
            params: query,
        });
    },

  // 详情查询
  detailAiAgent(id: number): Promise<AxiosResponse<ApiResponse<AiAgentTable>>> {
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

  // 发布
    publishAiAgent(id: number, body: AiAgentPublishPayload) {
    return request<ApiResponse<AiAgentTable>>({
      url: `${API_PATH}/${id}/publish`,
      method: "post",
        data: body,
    });
    },

    // 管理广场智能体
    manageAiAgent(id: number, body: AiAgentManagePayload) {
        return request<ApiResponse<AiAgentTable>>({
            url: `${API_PATH}/${id}/manage`,
            method: "put",
            data: body,
    });
  },

  // 下线
  offlineAiAgent(id: number) {
    return request<ApiResponse<AiAgentTable>>({
      url: `${API_PATH}/${id}/offline`,
      method: "post",
    });
  },

    // 克隆
    cloneAiAgent(id: number) {
    return request<ApiResponse<AiAgentTable>>({
        url: `${API_PATH}/${id}/clone`,
      method: "post",
    });
  },

  // 私有删除
  deletePrivateAiAgent(id: number) {
    return request<ApiResponse>({
      url: `${API_PATH}/${id}/delete`,
      method: "delete",
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
    created_id?: string | number;
    updated_id?: string | number;
  name?: string;
  description?: string;
  type?: string;
  visibility_scope?: "private" | "public" | string;
    publish_status?: "draft" | "published" | "offline" | "delete" | "clone" | string;
  version_no?: number;
  public_agent_id?: number;
    current_right?: 0 | 1 | 2;
    can_view?: boolean;
    can_clone?: boolean;
    can_manage?: boolean;
    is_owner?: boolean;
    is_admin?: boolean;
    auth_rules?: AiAgentAuthRule[];
  config?: string; // 智能体配置 AiAgentConfig JSON 格式
  prompt_template?: string;
  model?: string; // 模型配置 {modelId: "gpt-3.5-turbo", providerId: "openai"}
  cover?: string; 
  created_by?: CommonType;
  updated_by?: CommonType;
}

export type AiAgentConfig = {
  mcp?: AiAgentMcpConfig,
  url?: string,
  welcome?: string,
  enableSearch?: boolean,
  enableUpload?: boolean,
  enableChat?: boolean,
  enableVoice?: boolean,
}


export type AiAgentMcpConfig = {
  activeSkills?: string[],
  internalTools?: string[],
  externalTools?: string[], // MCP工具名称列表
  knowledge?: KnowledgeItem[],
}

export type KnowledgeItem = {
  name: string;
  dataset_id: string;
}

export interface AiAgentKnowledgeDataset {
    dataset_id: string;
    name?: string;
    description?: string;
    document_count?: number;
}

// 新增/修改/详情表单参数
export interface AiAgentForm extends BaseFormType {
  name?: string;
  description?: string;
  type?: string;
  config?: string;
  prompt_template?: string;
  model?: string;
  cover?: string;
}

export interface AiAgentAuthRule {
    id?: number;
    target_type: "global" | "role" | "user";
    target_value?: string | null;
    target_label?: string | null;
    target_right: 1 | 2;
    granted_by?: number | null;
    granted_at?: string | null;
}

export interface AiAgentPublishPayload {
    name: string;
    description?: string;
    type: string;
    auth_rules: AiAgentAuthRule[];
}

export type AiAgentManagePayload = AiAgentPublishPayload;
