import {AssistantMessageBlock, MESSAGE} from '@/types/chat'
import {LLMAgentEvent, LLMAgentEventData} from '@/types/model';
import AiChatAPI from '../fastApi/module_ai/ai_chat';
import {serializeAssistantStoredContent} from '@/utils/chatMessage';

export class LLMEventHandler {
  // private readonly generatingMessages: Map<string, GeneratingMessageState>
  private generatingMessage: MESSAGE
  private messages: MESSAGE[]
  private messageBuffer: MESSAGE[] = []
  private onMessageChanged?: (msgs:MESSAGE[]) => void
  private onMessageDone?: () => void 
  private onMessageError?: (error: Error) => void
  // private readonly onConversationUpdated?: ConversationUpdateHandler

  constructor(options: {
    messages: MESSAGE[],
    generatingMessage: MESSAGE,
    onMessageChanged?: (msgs:MESSAGE[]) => void,
    onMessageDone?: () => void ,
    onMessageError?: (error: Error) => void,
    // onConversationUpdated?: ConversationUpdateHandler
  }) {
    this.generatingMessage = options.generatingMessage
    this.onMessageChanged = options.onMessageChanged
    this.onMessageDone = options.onMessageDone
    this.onMessageError = options.onMessageError
    this.messages = options.messages
    this.callback = this.callback.bind(this)
    // this.onConversationUpdated = options.onConversationUpdated
    //this.contentBufferHandler = options.contentBufferHandler
    //this.toolCallHandler = options.toolCallHandler
    //this.streamUpdateScheduler = options.streamUpdateScheduler
  }

  getLastMessage(): MESSAGE {
    this.messageBuffer = [...this.messages]
    return this.messageBuffer[this.messageBuffer.length - 1]
  }

  async handleLLMAgentResponse(msg: LLMAgentEventData): Promise<void> {
    const currentTime = Date.now()
    const {
      eventId,
      content,
      reasoning_content,
      tool_call_id,
      tool_call_name,
      tool_call_params,
      maximum_tool_calls_reached,
      tool_call_server_name,
      tool_call_server_icons,
      tool_call_server_description,
      tool_call_response_raw,
      tool_call_response,
      tool_call,
      question_request,
      question_error,
      totalUsage,
      image_data
    } = msg

    const lastMsg = this.getLastMessage()
    const contentArray = lastMsg.content as AssistantMessageBlock[]
    console.log('handleLLMAgentResponse', msg)
    if (totalUsage && lastMsg.metadata) {
      lastMsg.metadata.totalTokens += totalUsage.total_tokens
      lastMsg.metadata.inputTokens += totalUsage.prompt_tokens
      lastMsg.metadata.outputTokens += totalUsage.completion_tokens
      //this.generatingMessage.metadata.totalUsage = totalUsage
      //state.promptTokens = totalUsage.prompt_tokens
    }

    if (question_error) {
      this.finalizeLastBlock()
      contentArray.push({
        type: 'error',
        content: question_error,
        status: 'error',
        timestamp: currentTime
      })
    }
    
    const lastBlock = contentArray[contentArray.length - 1]

    if (tool_call === 'end') {
      // 找到记录
      const toolCallBlock = contentArray.find((block) => block.type === 'tool_call' && block.tool_call?.id === tool_call_id)
      if (toolCallBlock && toolCallBlock.tool_call) {
        toolCallBlock.tool_call.response = tool_call_response as string
        toolCallBlock.tool_call.params = tool_call_params || ''
        toolCallBlock.status = 'success'
        toolCallBlock.timestamp = currentTime
      }
    }

    if (tool_call  == "start") {
      // 处理工具调用
        this.finalizeLastBlock()
        contentArray.push({
          type: 'tool_call',
          content: '',
          tool_call:{
                id: tool_call_id,
                name: tool_call_name,
                response: tool_call_response as string,
                params: tool_call_params
          },
          status: 'loading',
          timestamp: currentTime
        })
    }

    if (image_data?.data) {
      
    }

    if (content) {
      if (!lastBlock || lastBlock.type !== 'content' || lastBlock.status !== 'loading') {
        this.finalizeLastBlock()
        contentArray.push({
          type: 'content',
          content: content || '',
          status: 'loading',
          timestamp: currentTime
        })
      } else if (lastBlock.type === 'content') {
        lastBlock.content += content
      }
    }

    if (reasoning_content) {
      // Re-get lastBlock in case new blocks were added above
      const currentLastBlock = contentArray[contentArray.length - 1]
      if (!currentLastBlock || currentLastBlock.type !== 'reasoning_content') {
        this.finalizeLastBlock()
        const reasoningStartTime = currentTime
        contentArray.push({
          type: 'reasoning_content',
          content: reasoning_content || '',
          status: 'loading',
          timestamp: currentTime,
          reasoning_time: {
            start: reasoningStartTime,
            end: currentTime
          }
        })
      } else if (currentLastBlock.type === 'reasoning_content') {
        currentLastBlock.content += reasoning_content
        // Update reasoning_time.end in real-time during streaming
        if (currentLastBlock.reasoning_time) {
          currentLastBlock.reasoning_time.end = currentTime
        } else {
          const reasoningStartTime = currentLastBlock.timestamp ?? currentTime
          currentLastBlock.reasoning_time = {
            start: reasoningStartTime,
            end: currentTime
          }
        }
      }
    }
    
    this.onMessageChanged?.(this.messageBuffer)
  }

  async handleLLMAgentError(msg: LLMAgentEventData): Promise<void> {
    // 处理错误
    const { eventId, question_error } = msg
    const contentArray = this.getLastMessage().content as AssistantMessageBlock[]
    if (contentArray) {
      this.finalizeLastBlock()
      contentArray.push({
        type: 'error',
        content: question_error || '',
        status: 'error',
        timestamp: Date.now()
      })
      this.onMessageChanged?.(this.messageBuffer)
      if(this.onMessageError) {
        this.onMessageError(new Error(question_error || ''))
      }
    }

  }

  async handleLLMAgentEnd(msg: LLMAgentEventData): Promise<void> {
    const message = this.getLastMessage()
    const contentArray = message.content as AssistantMessageBlock[]
    contentArray.forEach((block) => {
      if (
        block.type === 'action'
      ) {
        return
      }
      block.status = 'success'
    })
    this.onMessageChanged?.(this.messageBuffer)
    const conversationId = Number(message.conversation_id || 0)
      const content = serializeAssistantStoredContent(message)
    if (conversationId > 0 && content) {
      const metadata = message.metadata
      try {
        AiChatAPI.saveChatCompletions({
          conversation_id: conversationId,
          role: message.role,
          content,
          token_count: metadata?.totalTokens || 0,
          input_tokens: metadata?.inputTokens || 0,
          output_tokens: metadata?.outputTokens || 0
        })
      } catch (error) {
        console.error('save chat message failed', error)
      }
    }
    if(this.onMessageDone) {
      this.onMessageDone()
    }

    /**   处理 统计数据； 发送完成事件 
    const metadata: Partial<MESSAGE_METADATA> = {
      totalTokens,
      inputTokens: state.promptTokens,
      outputTokens: completionTokens,
      generationTime,
      firstTokenTime: state.firstTokenTime ? state.firstTokenTime - state.startTime : 0,
      tokensPerSecond,
      contextUsage
    } */

  }

  finalizeLastBlock(): void {
    const blocks = this.generatingMessage.content as AssistantMessageBlock[]
    if (!blocks?.length) {
      return
    }

    const lastBlock = blocks[blocks.length - 1]

    if (!lastBlock) {
      return
    }

    if (
      lastBlock.type === 'action' 
    ) {
      return
    }

    if (lastBlock.type === 'tool_call' && lastBlock.status === 'loading') {
      return
    }

    if (lastBlock.status === 'loading') {
      lastBlock.status = 'success'
    }
  }

  async consume(stream: AsyncGenerator<LLMAgentEvent, void, unknown>): Promise<void> {
    for await (const event of stream) {
      // console.log("consume event", event)
      const msg = event.data
      if (event.type === 'response') {
        await this.handleLLMAgentResponse(msg)
      } else if (event.type === 'error') {
        await this.handleLLMAgentError(msg)
      } else if (event.type === 'end') {
        await this.handleLLMAgentEnd(msg)
      }
    }
  }

  async callback(event: LLMAgentEvent): Promise<void> {
    const msg = event.data
    if (event.type === 'response') {
        await this.handleLLMAgentResponse(msg)
      } else if (event.type === 'error') {
        await this.handleLLMAgentError(msg)
      } else if (event.type === 'end') {
        await this.handleLLMAgentEnd(msg)
      }
  }
}
