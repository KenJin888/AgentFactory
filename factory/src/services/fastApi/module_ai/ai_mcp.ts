import request from "@/utils/request";

const API_PATH = "/ai/ai_mcp";

const AiMcpAPI = {
  // 列表查询
  listAiMcp(query: AiMcpPageQuery) {
    return request<ApiResponse<PageResult<AiMcpTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailAiMcp(id: number) {
    return request<ApiResponse<AiMcpTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createAiMcp(body: AiMcpForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateAiMcp(id: number, body: AiMcpForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteAiMcp(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchAiMcp(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportAiMcp(query: AiMcpPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateAiMcp() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importAiMcp(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default AiMcpAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface AiMcpPageQuery extends PageQuery {
  status?: string;
  created_id?: number;
  updated_id?: number;
  name?: string;
  type?: string;
  abstract?: string;
  category?: string;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface AiMcpTable extends BaseType {
  created_id?: string;
  updated_id?: string;
  name?: string;
  type?: string;
  abstract?: string;
  category?: string;
  config?: string;
  tools?: string;
  cover?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface AiMcpForm extends BaseFormType {
  name?: string;
  type?: string;
  abstract?: string;
  category?: string;
  config?: string;
  tools?: string;
  cover?: string;
}

export const BUILTIN_RAGFLOW_MCP_URL = "http://127.0.0.1:9024/mcp";

const normalizeMcpEndpoint = (value?: string): string => {
    return String(value || "").trim().replace(/\/+$/, "").toLowerCase();
};

export const isBuiltinRagflowMcp = (mcp?: Pick<AiMcpTable, "config"> | null): boolean => {
    if (!mcp?.config) return false;

    try {
        const parsed = JSON.parse(mcp.config);
        const servers = parsed?.mcpServers;
        if (!servers || typeof servers !== "object") return false;

        const targetUrl = normalizeMcpEndpoint(BUILTIN_RAGFLOW_MCP_URL);
        return Object.values(servers).some((server: any) => {
            if (!server || typeof server !== "object") return false;
            const endpoint = normalizeMcpEndpoint(server.url || server.baseUrl);
            return endpoint === targetUrl;
        });
    } catch {
        return false;
    }
};
