import { Auth } from "@/utils/auth";

const baseApi = String(import.meta.env.VITE_APP_BASE_API || "/api/v1");
const API_PATH = "/oh/oh_http";

export interface OhCreateSessionRequest {
  user_id?: string | null;
  metadata?: Record<string, unknown>;
  model?: string | null;
  base_url?: string | null;
  system_prompt?: string | null;
  api_key?: string | null;
  provider?: string | null;
}

export interface OhSessionSnapshot {
  session_id: string;
  user_id?: string | null;
  cwd: string;
  status: "idle" | "running" | "failed";
  model: string;
  message_count: number;
  created_at: number;
  updated_at: number;
  last_error?: string | null;
}

export interface OhMessageSubmitResponse {
  session_id: string;
  assistant_text: string;
  message_count: number;
  usage: Record<string, unknown>;
  events: Array<{
    type: string;
    payload: Record<string, unknown>;
  }>;
}

export interface OhSessionMessagesResponse {
  session_id: string;
  messages: Array<Record<string, unknown>>;
}

export interface OhCancelSessionResponse {
  session_id: string;
  cancelled: boolean;
  detail: string;
}

export interface OhSseEvent {
  type: string;
  payload: Record<string, unknown>;
}

const getHeaders = (jsonBody: boolean) => {
  const token = Auth.getAccessToken();
  const headers: Record<string, string> = {};
  if (jsonBody) {
    headers["Content-Type"] = "application/json";
  }
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  return headers;
};

const parseErrorDetail = async (response: Response) => {
  try {
    const data = (await response.json()) as { detail?: string };
    return data?.detail || `请求失败(${response.status})`;
  } catch {
    return `请求失败(${response.status})`;
  }
};

const requestJson = async <T>(path: string, init?: RequestInit): Promise<T> => {
  const response = await fetch(`${baseApi}${API_PATH}${path}`, init);
  if (!response.ok) {
    throw new Error(await parseErrorDetail(response));
  }
  return (await response.json()) as T;
};

const parseSseBlock = (block: string): OhSseEvent | null => {
  const lines = block
    .split("\n")
    .map((line) => line.trimEnd())
    .filter((line) => line.length > 0);
  if (!lines.length) {
    return null;
  }

  let eventType = "message";
  const dataLines: string[] = [];
  for (const line of lines) {
    if (line.startsWith("event:")) {
      eventType = line.slice(6).trim() || "message";
      continue;
    }
    if (line.startsWith("data:")) {
      dataLines.push(line.slice(5).trim());
    }
  }

  const raw = dataLines.join("\n");
  if (!raw) {
    return { type: eventType, payload: {} };
  }

  try {
    return {
      type: eventType,
      payload: JSON.parse(raw) as Record<string, unknown>,
    };
  } catch {
    return {
      type: eventType,
      payload: { raw },
    };
  }
};

const OhHttpAPI = {
  getResolvedPrefix() {
    return API_PATH;
  },

  async healthz() {
    return requestJson<{ status: string }>("/healthz", {
      method: "GET",
      headers: getHeaders(false),
    });
  },

  async createSession(payload: OhCreateSessionRequest) {
    return requestJson<OhSessionSnapshot>("/sessions", {
      method: "POST",
      headers: getHeaders(true),
      body: JSON.stringify(payload),
    });
  },

  async getSession(sessionId: string) {
    return requestJson<OhSessionSnapshot>(`/sessions/${sessionId}`, {
      method: "GET",
      headers: getHeaders(false),
    });
  },

  async getMessages(sessionId: string) {
    return requestJson<OhSessionMessagesResponse>(`/sessions/${sessionId}/messages`, {
      method: "GET",
      headers: getHeaders(false),
    });
  },

  async submitMessage(sessionId: string, content: string) {
    return requestJson<OhMessageSubmitResponse>(`/sessions/${sessionId}/messages`, {
      method: "POST",
      headers: getHeaders(true),
      body: JSON.stringify({ content }),
    });
  },

  async cancelSession(sessionId: string) {
    return requestJson<OhCancelSessionResponse>(`/sessions/${sessionId}/cancel`, {
      method: "POST",
      headers: getHeaders(false),
    });
  },

  async streamMessage(
    sessionId: string,
    content: string,
    onEvent: (event: OhSseEvent) => void,
    signal?: AbortSignal
  ) {
    const response = await fetch(`${baseApi}${API_PATH}/sessions/${sessionId}/messages/stream`, {
      method: "POST",
      headers: getHeaders(true),
      body: JSON.stringify({ content }),
      signal,
    });

    if (!response.ok) {
      throw new Error(await parseErrorDetail(response));
    }
    if (!response.body) {
      throw new Error("未获取到流式响应");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let buffer = "";
    let done = false;

    while (!done) {
      const result = await reader.read();
      done = result.done;
      if (!result.value) {
        continue;
      }

      buffer += decoder.decode(result.value, { stream: true });
      let splitIndex = buffer.indexOf("\n\n");
      while (splitIndex >= 0) {
        const block = buffer.slice(0, splitIndex);
        buffer = buffer.slice(splitIndex + 2);
        const event = parseSseBlock(block);
        if (event) {
          onEvent(event);
        }
        splitIndex = buffer.indexOf("\n\n");
      }
    }

    const finalBlock = parseSseBlock(buffer);
    if (finalBlock) {
      onEvent(finalBlock);
    }
  },
};

export const ohApi = OhHttpAPI;
export default OhHttpAPI;
