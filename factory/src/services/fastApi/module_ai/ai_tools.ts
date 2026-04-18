import request from "@/utils/request";

const API_PATH = "/ai/ai_tools";

const AiToolsAPI = {
  // 列出内置工具列表
  listInternalTools(forceRefresh: boolean = false) {
    return request<ApiResponse<InternalToolsResponse>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: { force_refresh: forceRefresh },
    });
  },
};

export default AiToolsAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 内置工具列表响应
export interface InternalToolsResponse {
  tools: InternalToolItem[];
}

// 内置工具项
export interface InternalToolItem {
  name: string;
  description: string;
}
