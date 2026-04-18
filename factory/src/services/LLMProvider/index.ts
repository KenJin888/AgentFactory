import { AssistantMessageBlock, ChatMessage, CONVERSATION, MESSAGE, UserMessageContent } from "@/types/chat"
import { LLM_PROVIDER, LLMCoreStreamEvent, ApiEndpointType, TextStreamEvent, MODEL_META, 
  LLMResponse, ModelConfig,
  ReasoningStreamEvent, ToolCallStartEvent, ToolCallChunkEvent, ToolCallEndEvent, PermissionRequestEvent, PermissionRequestPayload, ErrorStreamEvent, UsageStreamEvent, StopStreamEvent, ImageDataStreamEvent, RateLimitStreamEvent, ToolCallEvent, 
  LLMAgentEvent} from '@/types/model'

/**
 * Base LLM Provider Abstract Class
 *
 * This class defines the interfaces and shared functionality that all LLM providers must implement, including:
 * - Model management (fetch, add, delete, update models)
 * - Unified message format
 * - Tool call handling
 * - Conversation generation and streaming processing
 *
 * All specific LLM providers (such as OpenAI, Anthropic, Gemini, Ollama, etc.) must inherit from this class
 * and implement its abstract methods.
 */
export abstract class BaseLLMProvider {
  // Maximum tool calls limit in a single conversation turn
  protected static readonly MAX_TOOL_CALLS = 12800
  protected static readonly DEFAULT_MODEL_FETCH_TIMEOUT = 12000 // Increased to 12 seconds as universal default

  protected provider: LLM_PROVIDER
  protected isInitialized: boolean = false
  // protected models: MODEL_META[] = []

  protected defaultHeaders: Record<string, string> = {
    'HTTP-Referer': 'https://DeepFast.cn',
    'X-Title': 'DeepFast'
  }

  constructor(provider: LLM_PROVIDER) {
    this.provider = provider
    this.provider.models = this.provider.models || []
  }

  protected async init() {
    this.isInitialized = true
  }

  /**
   * Get the maximum tool calls limit in a single conversation turn
   * @returns Configured maximum tool calls in a single conversation turn
   */
  public static getMaxToolCalls(): number {
    return BaseLLMProvider.MAX_TOOL_CALLS
  }

  /**
   * Get the model fetch timeout configuration
   * @returns Timeout duration (milliseconds)
   */
  protected getModelFetchTimeout(): number {
    return BaseLLMProvider.DEFAULT_MODEL_FETCH_TIMEOUT
  }

  /**
   * 获取所有模型（包括自定义模型）
   * @returns 模型列表
   */
  public getModels(): MODEL_META[] {
    return this.provider.models || []
  }

  /**
   * 获取所有自定义模型
   * @returns 自定义模型列表
   */
  public getCustomModels(): MODEL_META[] {
    return this.getModels().filter((model) => model.isCustom)
  }

    /**
   * [新] 核心流式处理方法
   * 此方法由具体的提供商子类实现，负责单次API调用和事件标准化。
   */
  abstract coreStream(
    eventId:string,
    conversation: CONVERSATION, 
    messages: MESSAGE[], 
    userMssage: UserMessageContent, 
    files: File[],
    signal?: AbortSignal
  ): AsyncGenerator<LLMCoreStreamEvent>

  abstract coreCallback(
    eventId:string,
    conversation: CONVERSATION, 
    messages: MESSAGE[], 
    userMssage: UserMessageContent, 
    files: File[],
    callback: (event: LLMAgentEvent) => void
  ): Promise<void>


  /**
   * 同步获取完整的LLM响应
   *
   * 该方法发送单一请求获取完整的响应内容，适用于后台处理或需要完整结果的场景。
   * 特点：
   * 1. 一次性返回完整的响应结果
   * 2. 包含完整的token使用统计
   * 3. 解析并处理<think>标签，提取reasoning_content
   * 4. 不进行工具调用（工具调用仅在stream版本中处理）
   *
   * @param messages 对话历史消息
   * @param modelId 模型ID
   * @param temperature 温度参数（影响创造性，值越高创造性越强）
   * @param maxTokens 最大生成token数
   * @returns 包含content, reasoning_content和totalUsage的响应对象

  abstract completions(
    messages: ChatMessage[],
    modelId: string,
    temperature?: number,
    maxTokens?: number
  ): Promise<LLMResponse>    */


  /**
   * 根据提示生成文本
   *
   * @param prompt 文本提示
   * @param modelId 模型ID
   * @param temperature 温度参数
   * @param maxTokens 最大生成token数
   * @returns 生成的文本响应
  
  abstract generateText(
    prompt: string,
    modelId: string,
    temperature?: number,
    maxTokens?: number
  ): Promise<LLMResponse>  */

  /**
   * 核心流式处理方法
   * 此方法由具体的提供商子类实现，负责单次API调用和事件标准化。
   
  abstract SendMessage(
    conversation: CONVERSATION,
    messages: MESSAGE[],
    userMssage:ChatMessage[],
    assistantMsg: MESSAGE
  ): Promise<any> */

  public parseAssistantMessage(content: string): AssistantMessageBlock[] {
    const blocks: AssistantMessageBlock[] = []
    const thinkStart = content.indexOf('<think>')
    const thinkEnd = content.indexOf('</think>')
  
    if (thinkStart !== -1) {
      if (thinkEnd !== -1) {
        // 完整的思考过程
        blocks.push({
          type: 'reasoning_content',
          content: content.substring(thinkStart + 7, thinkEnd),
          status: 'success',
          timestamp: Date.now()
        })
        // 剩余内容
        const rest = content.substring(0, thinkStart) + content.substring(thinkEnd + 8)
        if (rest) {
          blocks.push({
            type: 'content',
            content: rest,
            status: 'success',
            timestamp: Date.now()
          })
        }
      } else {
        // 不完整的思考过程（正在生成）
        blocks.push({
          type: 'reasoning_content',
          content: content.substring(thinkStart + 7),
          status: 'reading',
          timestamp: Date.now()
        })
        const pre = content.substring(0, thinkStart)
        if (pre) {
          blocks.push({
            type: 'content',
            content: pre,
            status: 'success',
            timestamp: Date.now()
          })
        }
      }
    } else {
      // 没有思考标签，视为普通内容
      if (content) {
        blocks.push({
          type: 'content',
          content: content,
          status: 'success',
          timestamp: Date.now()
        })
      }
    }
    return blocks
  }

}


export const SUMMARY_TITLES_PROMPT = `
You need to summarize the user's conversation into a title of no more than 10 words, with the title language matching the user's primary language, without using punctuation or other special symbols,only output the title,here is the conversation:
`


export const createStreamEvent = {
  text: (content: string): TextStreamEvent => ({ type: 'text', content }),
  reasoning: (reasoning_content: string): ReasoningStreamEvent => ({
    type: 'reasoning',
    reasoning_content
  }),
  toolCallStart: (tool_call_id: string, tool_call_name: string): ToolCallStartEvent => ({
    type: 'tool_call_start',
    tool_call_id,
    tool_call_name
  }),
  toolCallChunk: (tool_call_id: string, tool_call_arguments_chunk: string): ToolCallChunkEvent => ({
    type: 'tool_call_chunk',
    tool_call_id,
    tool_call_arguments_chunk
  }),
  toolCallEnd: (tool_call_id: string, tool_call_arguments_complete?: string): ToolCallEndEvent => ({
    type: 'tool_call_end',
    tool_call_id,
    tool_call_arguments_complete
  }),
  toolCall: (tool_call_id: string, tool_call_name?: string, tool_call_arguments?: string, tool_call_result?: string): ToolCallEvent => ({
    type: 'tool_call',
    tool_call_id,
    tool_call_name, 
    tool_call_arguments,
    tool_call_result

  }),
  permission: (permission: PermissionRequestPayload): PermissionRequestEvent => ({
    type: 'permission',
    permission
  }),
  error: (error_message: string): ErrorStreamEvent => ({ type: 'error', error_message }),
  usage: (usage: {
    prompt_tokens: number
    completion_tokens: number
    total_tokens: number
  }): UsageStreamEvent => ({
    type: 'usage',
    usage
  }),
  stop: (
    stop_reason: 'tool_use' | 'max_tokens' | 'stop_sequence' | 'error' | 'complete'
  ): StopStreamEvent => ({
    type: 'stop',
    stop_reason
  }),
  imageData: (image_data: { data: string; mimeType: string }): ImageDataStreamEvent => ({
    type: 'image_data',
    image_data
  }),
  rateLimit: (rate_limit: {
    providerId: string
    qpsLimit: number
    currentQps: number
    queueLength: number
    estimatedWaitTime?: number
  }): RateLimitStreamEvent => ({
    type: 'rate_limit',
    rate_limit
  })
}
