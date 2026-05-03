import request from "@/utils/request";
import {Auth} from "@/utils/auth";
import type {AiChatMsgPageQuery, AiChatMsgTable} from "./ai_chat_msg";
import {ChatMessage, UserMessageContent} from "@/types/chat";

const API_PATH = "/ai/ai_chat";

const AiChatAPI = {
  // 列表查询
  listAiChat(query: AiChatPageQuery) {
    return request<ApiResponse<PageResult<AiChatTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  cancelChatCompletions(body: AiChatCompletionStopForm) {
    return request<ApiResponse<{ conversation_id: string | number; stopped: boolean }>>({
      url: `${API_PATH}/chat/completions/stop`,
      method: "post",
      data: body,
    });
  },
  saveChatCompletions(body: AiChatCompletionSaveForm) {
    return request<ApiResponse<{ saved: boolean; chat_id: number; msg_id: number }>>({
      url: `${API_PATH}/chat/completions/save`,
      method: "post",
      data: body,
    });
  },
  listAiChatMsg(query: AiChatMsgPageQuery) {
    return request<ApiResponse<PageResult<AiChatMsgTable[]>>>({
      url: `/ai/ai_chat_msg/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailAiChat(id: number) {
    return request<ApiResponse<AiChatTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createAiChat(body: AiChatForm) {
    return request<ApiResponse<AiChatTable>>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateAiChat(id: number, body: AiChatForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteAiChat(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchAiChat(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 聊天补全
  async chatCompletions(body: AiChatCompletionForm, onChunk?: (chunk: string) => void, signal?: AbortSignal) {
    if (onChunk) {
      const token = Auth.getAccessToken();
      const response = await fetch(
        (import.meta.env.VITE_APP_BASE_API || "") + `${API_PATH}/chat/completions`,
        {
          method: "post",
          signal,
          headers: {
            "Content-Type": "application/json",
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
          },
          body: JSON.stringify(body),
        }
      );

      if (!response.ok) {
        throw new Error("请求失败");
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error("无法获取响应流");
      }

      const decoder = new TextDecoder("utf-8");
      let done = false;

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          console.log("Received chunk:", chunk);
          onChunk(chunk);
        }
      }
      return;
    }

    return request<any>({
      url: `${API_PATH}/chat/completions`,
      method: "post",
      data: body,
    });
  },

  // 核心流式处理方法
  // 使用 multipart/form-data 上传文件，由后端处理
  async *handleChatCompletion(
    body: AiChatCompletionForm,
    files: File[] = [],
    signal?: AbortSignal
  ): AsyncGenerator<string> {
      const token = Auth.getAccessToken();
      const hasFiles = files.length > 0

      // 构建 FormData
      const formData = new FormData();
      
      // 将请求体作为 JSON 字符串放入 body 字段
      formData.append('body', JSON.stringify(body));

      // 添加文件
      if (hasFiles) {
        for (const file of files) {
          formData.append('files', file, file.name);
        }
      }

      const response = await fetch(
        (import.meta.env.VITE_APP_BASE_API || "") + `${API_PATH}/chat/completions`,
        {
          method: "post",
          signal,
          headers: {
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
          },
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("请求失败");
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error("无法获取响应流");
      }

      const decoder = new TextDecoder("utf-8");
      let done = false;

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          yield chunk;
        }
      }
  },


  // 导出
  exportAiChat(query: AiChatPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateAiChat() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importAiChat(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  // 获取统计数据
  getStats(forceRefresh?: boolean) {
    return request<ApiResponse<AiChatStats>>({
      url: `${API_PATH}/stats`,
      method: "get",
      params: forceRefresh !== undefined ? { force_refresh: forceRefresh } : undefined,
    });
  },
};

export default AiChatAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface AiChatPageQuery extends PageQuery {
  status?: string;
  created_id?: number;
  updated_id?: number;
  user_id?: string;
  agent_id?: string;
  title?: string;
  model_info?: string;
  tokens?: string;
  model_id?: string;
  provider_id?: string;
  parent_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface AiChatTable extends BaseType {
  created_id?: string;
  updated_id?: string;
  user_id?: string;
  agent_id?: string;
  title?: string;
  model_info?: string;
  tokens?: string;
  model_id?: string;
  provider_id?: string;
  parent_id?: number;
  created_by?: CommonType;
  updated_by?: CommonType;
  description?: string;
}

// 新增/修改/详情表单参数
export interface AiChatForm extends BaseFormType {
  user_id?: string;
  agent_id?: string;
  title?: string;
  model_info?: string;
  tokens?: string;
  model_id?: string;
  provider_id?: string;
  parent_id?: number;
}

// 聊天补全消息
export interface AiChatCompletionMessage {
  role: string;
  content: string;
}

export interface AiChatResponseSchema {
  schema_key?: string;
  json_schema?: Record<string, unknown>;
}

// 聊天补全表单参数
export interface AiChatCompletionForm {
  provider?: string;
  model?: string;
  conversation_id?: string;
  system_prompt?: string;
  context_length?: number;
  userMessage?: UserMessageContent;
  messages?: ChatMessage[]; // 取消？
  temperature?: number;
  response_schema?: AiChatResponseSchema;
}

export interface AiChatCompletionStopForm {
  conversation_id: string | number;
}

export interface AiChatCompletionSaveForm {
  conversation_id: string | number;
  role: string;
  content: string;
  token_count?: number;
  input_tokens?: number;
  output_tokens?: number;
}

// 统计数据响应
export interface AiChatStats {
  statistical_time: string;
  user_count: number;
  dept_count: number;
  role_count: number;
  agent_count: number;
  chat_count: number;
  msg_count: number;
  position_count?: number;
  mcp_count?: number;
  total_tokens?: number;
}
