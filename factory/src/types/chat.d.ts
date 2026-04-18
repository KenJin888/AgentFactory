export type CONVERSATION_SETTINGS = { 
   systemPrompt?: string 
   temperature?: number 
   contextLength?: number 
   maxTokens?: number 
   providerId?: string 
   modelId?: string 
   artifacts?: 0 | 1
    enabledMcpToolIds?: number[]
   thinkingBudget?: number 
   enableSearch?: boolean 
   forcedSearch?: boolean 
   searchStrategy?: 'turbo' | 'max' 
   reasoningEffort?: 'minimal' | 'low' | 'medium' | 'high' 
   verbosity?: 'low' | 'medium' | 'high' 
   acpWorkdirMap?: Record<string, string | null> 
   chatMode?: 'chat' | 'agent' | 'acp agent' 
   agentWorkspacePath?: string | null 
   selectedVariantsMap?: Record<string, string> 
   activeSkills?: string[] 
   
   // 增加：
   agentId?: string
   enableThinking?: boolean // 废弃
   enableUpload?: boolean 
   enableVoice?: boolean
 }

 export type CONVERSATION = {
  id: string
  title: string
  settings: CONVERSATION_SETTINGS
  createdAt?: number
  updatedAt?: number
  is_new?: number
  artifacts?: number
  is_pinned?: number
  parentConversationId?: string | null
  parentMessageId?: string | null
  parentSelection?: ParentSelection | null
}

export type MESSAGE_STATUS = 'sent' | 'pending' | 'error'
export type MESSAGE_ROLE = 'user' | 'assistant' | 'system' | 'function' | 'agent'

export type MESSAGE_METADATA = {
  totalTokens: number
  inputTokens: number
  outputTokens: number
  generationTime: number
  firstTokenTime: number
  tokensPerSecond: number
  contextUsage: number
  model?: string
  provider?: string
  reasoningStartTime?: number
  reasoningEndTime?: number
}

export interface MESSAGE {
  id: string
  conversation_id?: string
  content: string | UserMessageContent | AssistantMessageBlock[]
  role: MESSAGE_ROLE
  parent_id?: string
  status: MESSAGE_STATUS
  created_at?: number
  updated_at?: number
  metadata?: MESSAGE_METADATA
  is_variant?: boolean
  is_context_edge?: boolean
  timestamp?: number
}

// 数据存储格式： AssistantMessageBlock[] ?
export type AssistantMessageBlock = {
  type:
    | 'content'
    | 'search'
    | 'reasoning_content'
    | 'plan'
    | 'error'
    | 'tool_call'
    | 'action'
    | 'image'
    | 'artifact-thinking'
    | 'mcp_ui_resource'
  id?: string
  content?: string
  extra?: any  // Todo
  status:
    | 'success'
    | 'loading'
    | 'cancel'
    | 'error'
    | 'reading'
    | 'optimizing'
    | 'pending'
    | 'granted'
    | 'denied'
  timestamp?: number
  artifact?: {
    identifier: string
    title: string
    type:
      | 'application/vnd.ant.code'
      | 'text/markdown'
      | 'text/html'
      | 'image/svg+xml'
      | 'application/vnd.ant.mermaid'
      | 'application/vnd.ant.react'
    language?: string
  }
  mcp_ui_resource?: {
    uri: string
    mimeType: 'text/html' | 'text/uri-list' | 'application/vnd.mcp-ui.remote-dom'
    text?: string
    blob?: string
    _meta?: Record<string, unknown>
  }
  tool_call?: {
    id?: string
    name?: string
    params?: string
    response?: string
    server_name?: string
    server_icons?: string
    server_description?: string
  }
  action_type?: 'tool_call_permission' | 'maximum_tool_calls_reached' | 'rate_limit'
  image_data?: {
    data: string
    mimeType: string
  }
  reasoning_time?: {
    start: number
    end: number
  }
}

export interface FileMetaData {
  fileName: string
  fileSize: number
  fileDescription?: string
  fileCreated: Date
  fileModified: Date
}

export type MessageFile = {
  name: string
    content?: string
    mimeType?: string
  metadata?: FileMetaData
    token?: number
    path?: string
  thumbnail?: string
}

export type UserMessageContent = {
  think?: boolean
  search?: boolean
  text: string
  continue?: boolean
  files?:MessageFile[]
  resources?: any[] // ResourceListEntryWithClient[]
  prompts?: any[] // PromptWithClient[]
  links?: string[]
  content?: any //  (UserMessageTextBlock | UserMessageMentionBlock | UserMessageCodeBlock)[]
}

// MCP related type definitions
export interface MCPServerConfig {
  command: string
  args: string[]
  env: Record<string, unknown>
  descriptions: string
  icons: string
  autoApprove: string[]
  disable?: boolean
  baseUrl?: string
  customHeaders?: Record<string, string>
  customNpmRegistry?: string
  type: 'sse' | 'stdio' | 'inmemory' | 'http'
  source?: string // Source identifier: "mcprouter" | "modelscope" | undefined(for manual)
  sourceId?: string // Source ID: mcprouter uuid or modelscope mcpServer.id
}

export interface MCPConfig {
  mcpServers: Record<string, MCPServerConfig>
  defaultServers: string[]
  mcpEnabled: boolean
  ready: boolean
}

export interface MCPToolDefinition {
  type: string
  function: {
    name: string
    description: string
    parameters: {
      type: string
      properties: Record<string, any>
      required?: string[]
    }
  }
  server: {
    name: string
    icons: string
    description: string
  }
}

export type ChatMessageRole = 'system' | 'user' | 'assistant' | 'tool'

export type ChatMessageToolCall = {
  id: string
  type: 'function'
  function: { name: string; arguments: string }
}

export type ChatMessageContent =
  | { type: 'text'; text: string }
  | { type: 'image_url'; image_url: { url: string; detail?: 'auto' | 'low' | 'high' } }

export type ChatMessage = {
  role: ChatMessageRole
  content?: string | ChatMessageContent[]
  tool_calls?: ChatMessageToolCall[]
  tool_call_id?: string
}
