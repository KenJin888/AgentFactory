// 对接fast api 接口

import { LLM_PROVIDER, LLMCoreStreamEvent, ApiEndpointType, TextStreamEvent, ReasoningStreamEvent, ToolCallStartEvent, ToolCallChunkEvent, ToolCallEndEvent, PermissionRequestEvent, PermissionRequestPayload, ErrorStreamEvent, UsageStreamEvent, StopStreamEvent, ImageDataStreamEvent, RateLimitStreamEvent, ToolCallEvent, LLMAgentEvent, LLMAgentEventData } from '@/types/model'
import { BaseLLMProvider, createStreamEvent, SUMMARY_TITLES_PROMPT } from './index'
import { AssistantMessageBlock, ChatMessage, CONVERSATION, MCPToolDefinition, MESSAGE, UserMessageContent } from '@/types/chat'
import { mcpChatApi } from '../mcpchatApi'

export class DeepProvider extends BaseLLMProvider {
  threadId: string | '' = ''
  
  constructor(provider: LLM_PROVIDER) {
    super(provider)
    this.init()
  }

  ///////////////////////////////////////////////////////////////////////////////////////////////////////
  /**
   * 核心流处理方法，根据模型、apiEndpoint类型分发请求。
   * @returns AsyncGenerator<LLMCoreStreamEvent> 流式事件。
   */
  async *coreStream(
    eventId:string,
    conversation: CONVERSATION, messages: MESSAGE[], userMssage: UserMessageContent, files: File[] = [], signal?: AbortSignal
  ): AsyncGenerator<LLMCoreStreamEvent> {

  }

  async coreCallback(eventId:string,conversation: CONVERSATION, messages: MESSAGE[], userMssage: UserMessageContent, files: File[], callback: (event: LLMAgentEvent) => void): Promise<void> {
    if (!this.isInitialized) throw new Error('Provider not initialized')
    const modelId = conversation.settings?.modelId || ''
    const model = this.provider.models?.find((item) => item.id === modelId)
    if(!model) throw new Error(`Model ${modelId} not found`)

    const apiEndpoint = model.userConfig?.apiEndpoint || ApiEndpointType.Chat

    switch (apiEndpoint) {
      case ApiEndpointType.Chat:
      default:
        await this.handleChatCompletion( eventId, conversation, messages, userMssage, files, callback)
    }
  }

  async handleChatCompletion(
    eventId:string,
    conversation: CONVERSATION, messages: MESSAGE[], userMssage: UserMessageContent, files: File[] = [], callback: (event: LLMAgentEvent) => void
  ): Promise<void> {
    //-----------------------------------------------------------------------------------------------------
    // 1. 构建请求参数
    //-----------------------------------------------------------------------------------------------------
    // 移除推理模型的温度参数  Todo
    //if(modelConfig?.reasoning) delete requestParams.temperature

    // response_schema: {"schema_key":"formschema"}
    // 

    if(!this.threadId){
      // 如果是 Agent ?
      const result =  await mcpChatApi.createThread(
          conversation.title, 
          conversation.settings)
      if(result){
        this.threadId = result
      } else {
        // 创建线程失败
        callback({type: 'error', data: {eventId: 'createThread', error: '创建会话线程失败',}})
        return
      }
    }
    await mcpChatApi.sendMessage(this.threadId, userMssage, (payload) => {
      const streamPayload = payload as LLMAgentEvent | null | undefined
      console.log('handleChatCompletion_streamPayload', streamPayload)
      if (!streamPayload) {
        return
      }
      callback(streamPayload)
    })
  }
}



