export type ModelType = 'chat' | 'embedding' | 'rerank' | 'imageGeneration' | 'stt' | 'tts'

export enum ApiEndpointType {
  Chat = 'chat',
  Image = 'image',
  Video = 'video'
}

export type MODEL_META = {
  id: string
  name: string
  group?: string
  providerId: string
  enabled?: boolean
  isCustom?: boolean
  vision?: boolean
  functionCall?: boolean
  reasoning?: boolean
  enableSearch?: boolean
  type?: ModelType
  contextLength?: number
  maxTokens?: number
  userConfig?: ModelConfig
  description?: string
}

export type LLM_PROVIDER = {
  id: string
  name: string
  apiType?: string
  apiKey: string
  apiUrl?: string
  copilotClientId?: string
  baseUrl: string
  models?: MODEL_META[]
  customModels?: MODEL_META[]
  enable: boolean
  enabledModels?: string[]
  disabledModels?: string[]
  custom?: boolean
  authMode?: 'apikey' | 'oauth'
  oauthToken?: string
  rateLimit?: {
    enabled: boolean
    qpsLimit: number
  }
  rateLimitConfig?: {
    enabled: boolean
    qpsLimit: number
  }
}

export type ModelConfig = {
  maxTokens?: number
  contextLength?: number
  temperature?: number
  vision?: boolean // 视觉能力
  functionCall?: boolean // 函数调用
  reasoning?: boolean  // 推理能力
  type?: ModelType  // 模型类型
  apiEndpoint?: string // 生成内容 默认： '' / 'chat',  'image', 'video'
}

export interface PermissionRequestPayload {
  toolName: string
  serverName: string
  permissionType: 'read' | 'write' | 'all' | 'command'
  description: string
  command?: string
  commandSignature?: string
  commandInfo?: {
    command: string
    riskLevel: 'low' | 'medium' | 'high' | 'critical'
    suggestion: string
    signature?: string
    baseCommand?: string
  }
  conversationId?: string
}

export interface MCPToolResponse {
  /** Unique identifier for tool call */
  toolCallId: string

  /**
   * Tool call response content
   * Can be simple string or structured content array
   */
  content: string | any[]  // todo!!

  /** Optional metadata */
  _meta?: Record<string, any>

  /** Whether an error occurred */
  isError?: boolean

  /** When using compatibility mode, may directly return tool results */
  toolResult?: unknown

  /** Whether permission is required */
  requiresPermission?: boolean

  /** Permission request information */
  permissionRequest?: PermissionRequestPayload
}

export type LLMResponse = {
  content: string
  reasoning_content?: string
  tool_call_name?: string
  tool_call_params?: string
  tool_call_response?: string
  tool_call_id?: string
  tool_call_server_name?: string
  tool_call_server_icons?: string
  tool_call_server_description?: string
  tool_call_response_raw?: MCPToolResponse
  maximum_tool_calls_reached?: boolean
  totalUsage?: {
    prompt_tokens: number
    completion_tokens: number
    total_tokens: number
  }
}
export type LLMResponseStream = {
  content?: string
  reasoning_content?: string
  image_data?: {
    data: string
    mimeType: string
  }
  tool_call?: 'start' | 'end' | 'error'
  tool_call_name?: string
  tool_call_params?: string
  tool_call_response?: string
  tool_call_id?: string
  tool_call_server_name?: string
  tool_call_server_icons?: string
  tool_call_server_description?: string
  tool_call_response_raw?: MCPToolResponse
  maximum_tool_calls_reached?: boolean
  totalUsage?: {
    prompt_tokens: number
    completion_tokens: number
    total_tokens: number
  }
}

export type StreamEventType =
  | 'text'
  | 'reasoning'
  | 'tool_call_start'
  | 'tool_call_chunk'
  | 'tool_call_end'
  | 'permission'
  | 'error'
  | 'usage'
  | 'stop'
  | 'image_data'
  | 'rate_limit'

export interface TextStreamEvent {
  type: 'text'
  content: string
}

export interface ReasoningStreamEvent {
  type: 'reasoning'
  reasoning_content: string
}

export interface ToolCallStartEvent {
  type: 'tool_call_start'
  tool_call_id: string
  tool_call_name: string
}

export interface ToolCallChunkEvent {
  type: 'tool_call_chunk'
  tool_call_id: string
  tool_call_arguments_chunk: string
}

export interface ToolCallEndEvent {
  type: 'tool_call_end'
  tool_call_id: string
  tool_call_arguments_complete?: string
}


export interface ToolCallEvent {
  type: 'tool_call'
  tool_call_id: string
  tool_call_name?: string
  tool_call_arguments?: string
  tool_call_result?: string
}

export interface PermissionRequestEvent {
  type: 'permission'
  permission: PermissionRequestPayload
}

export interface ErrorStreamEvent {
  type: 'error'
  error_message: string
}

export interface UsageStreamEvent {
  type: 'usage'
  usage: {
    prompt_tokens: number
    completion_tokens: number
    total_tokens: number
  }
}

export interface StopStreamEvent {
  type: 'stop'
  stop_reason: 'tool_use' | 'max_tokens' | 'stop_sequence' | 'error' | 'complete'
}

export interface ImageDataStreamEvent {
  type: 'image_data'
  image_data: {
    data: string
    mimeType: string
  }
}

export interface RateLimitStreamEvent {
  type: 'rate_limit'
  rate_limit: {
    providerId: string
    qpsLimit: number
    currentQps: number
    queueLength: number
    estimatedWaitTime?: number
  }
}

export type LLMCoreStreamEvent =
  | TextStreamEvent
  | ReasoningStreamEvent
  | ToolCallStartEvent
  | ToolCallChunkEvent
  | ToolCallEndEvent
  | PermissionRequestEvent
  | ErrorStreamEvent
  | UsageStreamEvent
  | StopStreamEvent
  | ImageDataStreamEvent
  | RateLimitStreamEvent
  | ToolCallEvent


  export interface LLMAgentEventData {
  eventId: string
  conversationId?: string
  parentId?: string
  is_variant?: boolean
  stream_kind?: 'init' | 'delta' | 'final'
  seq?: number
  content?: string
  reasoning_content?: string
  reasoning_time?: { start: number; end: number }
  tool_call_id?: string
  tool_call_name?: string
  tool_call_params?: string
  tool_call_response?: string | Array<unknown>
  maximum_tool_calls_reached?: boolean
  tool_call_server_name?: string
  tool_call_server_icons?: string
  tool_call_server_description?: string
  tool_call_response_raw?: unknown
  tool_call?:
    | 'start'
    | 'running'
    | 'end'
    | 'error'
    | 'update'
    | 'permission-required'
    | 'permission-granted'
    | 'permission-denied'
    | 'continue'
    | 'question-required'
  permission_request?: {
    toolName: string
    serverName: string
    permissionType: 'read' | 'write' | 'all' | 'command'
    description: string
    command?: string
    commandSignature?: string
    commandInfo?: {
      command: string
      riskLevel: 'low' | 'medium' | 'high' | 'critical'
      suggestion: string
      signature?: string
      baseCommand?: string
    }
    providerId?: string
    requestId?: string
    sessionId?: string
    agentId?: string
    agentName?: string
    conversationId?: string
    options?: any
    rememberable?: boolean
  }
  question_request?: any
  question_error?: string
  totalUsage?: any
  image_data?: { data: string; mimeType: string }
  rate_limit?: any
  error?: string
  userStop?: boolean
}

export type LLMAgentEvent =
  | { type: 'response'; data: LLMAgentEventData }
  | { type: 'error'; data: { eventId: string; error: string } }
  | { type: 'end'; data: { eventId: string; userStop: boolean } }

