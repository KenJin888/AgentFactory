import request from "@/utils/request";

const API_PATH = "/ai/ai_chat_token_stats";

export interface TokenStatsQuery {
  time_range?: "day" | "week" | "month";
  start_date?: string;
  end_date?: string;
  dept_id?: number;
  position_id?: number;
  page_no?: number;
  page_size?: number;
}

export interface DeptTokenRankItem {
  dept_id: number;
  dept_name: string;
  total_tokens: number;
  model_distribution: { model: string; tokens: number }[];
}

export interface AgentTokenRankItem {
  agent_id: number;
  agent_name: string;
  total_tokens: number;
  user_count: number;
  position_distribution: { position: string; tokens: number }[];
}

export interface UserTokenRankItem {
  user_id: number;
  user_name: string;
  dept_name: string;
  position_name: string;
  total_tokens: number;
  agent_count: number;
  position_distribution: { position: string; tokens: number }[];
}

export interface TokenTrendItem {
  date: string;
  total_tokens: number;
  avg_tokens: number;
  user_count: number;
}

export interface UserTokenDetailItem {
  user_id: number;
  user_name: string;
  dept_name: string;
  position_name: string;
  date: string;
  tokens: number;
  title: string;
  model_name: string;
  agent_name: string;
  conversation_id: number;
}

export interface DeptTokenRankOut {
  items: DeptTokenRankItem[];
  total: number;
}

export interface AgentTokenRankOut {
  items: AgentTokenRankItem[];
  total: number;
}

export interface UserTokenRankOut {
  items: UserTokenRankItem[];
  total: number;
}

export interface TokenTrendOut {
  items: TokenTrendItem[];
  dates: string[];
}

export interface UserTokenDetailOut {
  items: UserTokenDetailItem[];
  total: number;
}

export interface TokenOverviewOut {
  total_tokens: number;
  total_chats: number;
  active_agents: number;
  active_users: number;
}

export interface ChatTrendItem {
  date: string;
  chat_count: number;
}

export interface ChatTrendOut {
  items: ChatTrendItem[];
  dates: string[];
}

export interface ModelConsumptionItem {
  model_name: string;
  tokens: number;
  percentage: number;
}

export interface ModelConsumptionOut {
  items: ModelConsumptionItem[];
  total: number;
}

const AiChatTokenStatsAPI = {
  // 部门Token消耗排名
  getDeptTokenRank(query: TokenStatsQuery) {
    return request<ApiResponse<DeptTokenRankOut>>({
      url: `${API_PATH}/dept_rank`,
      method: "get",
      params: query,
    });
  },

  // 智能体Token消耗排名
  getAgentTokenRank(query: TokenStatsQuery) {
    return request<ApiResponse<AgentTokenRankOut>>({
      url: `${API_PATH}/agent_rank`,
      method: "get",
      params: query,
    });
  },

  // 人员Token消耗排名
  getUserTokenRank(query: TokenStatsQuery) {
    return request<ApiResponse<UserTokenRankOut>>({
      url: `${API_PATH}/user_rank`,
      method: "get",
      params: query,
    });
  },

  // Token消耗趋势
  getTokenTrend(query: TokenStatsQuery) {
    return request<ApiResponse<TokenTrendOut>>({
      url: `${API_PATH}/trend`,
      method: "get",
      params: query,
    });
  },

  // 人员Token消耗明细
  getUserTokenDetail(query: TokenStatsQuery) {
    return request<ApiResponse<UserTokenDetailOut>>({
      url: `${API_PATH}/user_detail`,
      method: "get",
      params: query,
    });
  },

  // Token统计概览
  getTokenOverview(query: TokenStatsQuery) {
    return request<ApiResponse<TokenOverviewOut>>({
      url: `${API_PATH}/overview`,
      method: "get",
      params: query,
    });
  },

  // 对话趋势
  getChatTrend(query: TokenStatsQuery) {
    return request<ApiResponse<ChatTrendOut>>({
      url: `${API_PATH}/chat_trend`,
      method: "get",
      params: query,
    });
  },

  // 模型消耗占比
  getModelConsumption(query: TokenStatsQuery) {
    return request<ApiResponse<ModelConsumptionOut>>({
      url: `${API_PATH}/model_consumption`,
      method: "get",
      params: query,
    });
  },

  // 个人Token统计概览
  getPersonalTokenOverview(query?: { start_date?: string; end_date?: string }) {
    return request<ApiResponse<TokenOverviewOut>>({
      url: `${API_PATH}/personal_overview`,
      method: "get",
      params: query,
    });
  },

  // 个人Token消耗明细
  getPersonalTokenDetail(query?: { start_date?: string; end_date?: string; page_no?: number; page_size?: number }) {
    return request<ApiResponse<UserTokenDetailOut>>({
      url: `${API_PATH}/personal_detail`,
      method: "get",
      params: query,
    });
  },
};

export default AiChatTokenStatsAPI;
