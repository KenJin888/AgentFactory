import {CONVERSATION, MESSAGE, UserMessageContent} from "@/types/chat"
import {LLMAgentEvent} from "@/types/model"
import {FastProvider} from "./fastProvider"
import {useModelProviderStore} from '../../stores/modelProviders'
import {BaseLLMProvider} from "."
import {DeepProvider} from "./deepProvider"


export class AgentLoopHandler {

  /**
   * 接收 LLMCoreStreamEvent 转为 LLMAgentEvent
   * 
   * @param llmProviderType 
   * @param eventId 
   * @param conversation 
   * @param messages 
   * @param userMssages 
   */
  async *startStreamCompletion(
    llmProviderType: string,
    eventId:string,
    conversation: CONVERSATION, 
    messages: MESSAGE[], 
    userMssage: UserMessageContent,
    files: File[] = [],
    signal?: AbortSignal
  ): AsyncGenerator<LLMAgentEvent, void, unknown> {
    if(llmProviderType != "fast" && llmProviderType != "deep"){
      throw new Error('Only fast/deep provider is supported')
    }
    const provider = useModelProviderStore().llmProviders.find(p => p.id === conversation.settings?.providerId && p.enable)
    if (!provider) {
      throw new Error('Provider not found')
    }
    let providerInstance:BaseLLMProvider
    if(llmProviderType == "fast"){
      providerInstance = new FastProvider(provider)
    }else{
      providerInstance = new DeepProvider(provider)
    }

    const isUserStop = () => Boolean(signal?.aborted)
    // 准备 模型参数 Todo

    // mssage buffer
    let currentContent = ''
    let currentReasoning = ''
    const currentToolCalls: Array<{
          id: string
          name: string
          arguments: string
        }> = []
    const currentToolChunks: Record<
          string,
          {
            name: string
            arguments_chunk: string
            server_name?: string
            server_icons?: string
            server_description?: string
          }
        > = {}
    const totalUsage: {
        prompt_tokens: number
        completion_tokens: number
        total_tokens: number
        context_length: number
      } = {
        prompt_tokens: 0,
        completion_tokens: 0,
        total_tokens: 0,
        context_length: 0 // modelConfig?.contextLength || 0
      }
    try {
      // Call the provider's core stream method, expecting LLMCoreStreamEvent
      const stream = providerInstance.coreStream(eventId, conversation, messages, userMssage, files, signal)

      // Process the standardized stream events
      for await (const chunk of stream) {
        if (isUserStop()) {
          break
        }
        //if (abortController.signal.aborted) {
        //  break
        //}

        // --- Event Handling (using LLMCoreStreamEvent structure) ---
        switch (chunk.type) {
          case 'text':
            if (chunk.content) {
              currentContent += chunk.content
              yield {
                type: 'response',
                data: {
                  eventId,
                  content: chunk.content
                }
              }
            }
            break
          case 'reasoning':
            if (chunk.reasoning_content) {
              currentReasoning += chunk.reasoning_content
              yield {
                type: 'response',
                data: {
                  eventId,
                  reasoning_content: chunk.reasoning_content
                }
              }
            }
            break
          case 'tool_call_start':
            if (chunk.tool_call_id && chunk.tool_call_name) {
              // Todo : Start Tools
              // Immediately send the start event to indicate the tool call has begun
              yield {
                type: 'response',
                data: {
                  eventId,
                  tool_call: 'start',
                  tool_call_id: chunk.tool_call_id,
                  tool_call_name: chunk.tool_call_name,
                  tool_call_params:  '', // Initial parameters are empty
                  tool_call_server_name: "",
                  tool_call_server_icons: "",
                  tool_call_server_description: ""
                }
              }
            }
            break
          case 'tool_call':
            if (chunk.tool_call_id && chunk.tool_call_name) {
              // Todo : Start Tools
              // Immediately send the start event to indicate the tool call has begun
              yield {
                type: 'response',
                data: {
                  eventId,
                  tool_call: 'end',
                  tool_call_id: chunk.tool_call_id,
                  tool_call_name: chunk.tool_call_name,
                  tool_call_params: chunk.tool_call_arguments, // Initial parameters are empty
                  tool_call_response: chunk.tool_call_result,
                  tool_call_server_name: "",
                  tool_call_server_icons: "",
                  tool_call_server_description: ""
                }
              }
            }
            break
          case 'tool_call_chunk':
            // Todo : Update Tools
            if (
              chunk.tool_call_id &&
              currentToolChunks[chunk.tool_call_id] &&
              chunk.tool_call_arguments_chunk
            ) {
              currentToolChunks[chunk.tool_call_id].arguments_chunk +=
                chunk.tool_call_arguments_chunk

              // Send update event to update parameter content in real-time
              yield {
                type: 'response',
                data: {
                  eventId,
                  tool_call: 'update',
                  tool_call_id: chunk.tool_call_id,
                  tool_call_name: currentToolChunks[chunk.tool_call_id].name,
                  tool_call_params: currentToolChunks[chunk.tool_call_id].arguments_chunk,
                  tool_call_server_name: currentToolChunks[chunk.tool_call_id].server_name,
                  tool_call_server_icons: currentToolChunks[chunk.tool_call_id].server_icons,
                  tool_call_server_description:
                    currentToolChunks[chunk.tool_call_id].server_description
                }
              }
            }
            break
          case 'tool_call_end':
            if (chunk.tool_call_id && currentToolChunks[chunk.tool_call_id]) {
              const completeArgs =
                chunk.tool_call_arguments_complete ??
                currentToolChunks[chunk.tool_call_id].arguments_chunk
              const toolCallName = currentToolChunks[chunk.tool_call_id].name
              const serverName = currentToolChunks[chunk.tool_call_id].server_name
              const serverIcons = currentToolChunks[chunk.tool_call_id].server_icons
              const serverDescription = currentToolChunks[chunk.tool_call_id].server_description

              yield {
                  type: 'response',
                  data: {
                    eventId,
                    tool_call: 'end',
                    tool_call_id: chunk.tool_call_id,
                    tool_call_name: toolCallName,
                    tool_call_params: completeArgs,
                    tool_call_response: completeArgs,
                    tool_call_server_name: serverName,
                    tool_call_server_icons: serverIcons,
                    tool_call_server_description: serverDescription
                  }
                }

                // delete currentToolChunks[chunk.tool_call_id]
            }
            break
          case 'permission': 
            // Todo: 处理权限事件
            break
          case 'usage':
            if (chunk.usage) {
              totalUsage.prompt_tokens += chunk.usage.prompt_tokens
              totalUsage.completion_tokens += chunk.usage.completion_tokens
              totalUsage.total_tokens += chunk.usage.total_tokens
              totalUsage.context_length = 0 // modelConfig.contextLength
            }
            break
          case 'image_data':
            // Todo: 处理图片数据事件
            break
          case 'error':
            console.error(`Provider stream error for event ${eventId}:`, chunk.error_message)
            yield {
              type: 'error',
              data: {
                eventId,
                error: chunk.error_message || 'Provider stream error'
              }
            }
            break // Break inner loop on provider error
          case 'rate_limit':
            if (chunk.rate_limit) {
              yield {
                type: 'response',
                data: {
                  eventId,
                  rate_limit: chunk.rate_limit
                }
              }
            }
            break
          case 'stop':
            console.log(
              `Provider stream stopped for event ${eventId}. Reason: ${chunk.stop_reason}`
            )
            if (chunk.stop_reason === 'tool_use') {
              // Consolidate any remaining tool call chunks
              for (const id in currentToolChunks) {
                currentToolCalls.push({
                  id: id,
                  name: currentToolChunks[id].name,
                  arguments: currentToolChunks[id].arguments_chunk
                })
              }
            } 
            // Stop event itself doesn't need to be yielded here, handled by loop logic
            break
        }
      } // End of inner loop (for await...of stream)

      // if (abortController.signal.aborted) break // Break outer loop if aborted
    } catch(error){
      // Catch errors from the generator setup phase (before the loop)
      if (isUserStop() || (error as any)?.name === 'AbortError') {
        console.log(`Agent loop aborted during outer try-catch for event ${eventId}`)
      } else {
        console.error(`Agent loop outer error for event ${eventId}:`, error)
        yield {
          type: 'error',
          data: {
            eventId,
            error: error instanceof Error ? error.message : String(error)
          }
        }
      }
    } finally{
      // --- Post-Stream Processing ---

      // Finalize stream regardless of how the loop ended (completion, error, abort)
      const userStop = isUserStop()
      if (!userStop) {
        // Yield final aggregated usage if not aborted
        yield {
          type: 'response',
          data: {
            eventId,
            totalUsage
          }
        }
      }
      // Yield the final END event
      yield { type: 'end', data: { eventId, userStop } }
      // Todo: 处理 activeStreams
      // this.options.activeStreams.delete(eventId)
    }
  }

  async startCompletion(
    llmProviderType: string,
    eventId:string,
    conversation: CONVERSATION, 
    messages: MESSAGE[], 
    userMssage: UserMessageContent, 
    files: File[],
    callback: (event: LLMAgentEvent) => void
  ): Promise<void> {
    if( llmProviderType != "deep"){
      throw new Error('Only fast/deep provider is supported')
    }
    const provider = useModelProviderStore().llmProviders.find(p => p.id === conversation.settings?.providerId && p.enable)
    if (!provider) {
      throw new Error('Provider not found')
    }
    let providerInstance:BaseLLMProvider
    providerInstance = new DeepProvider(provider)
    await providerInstance.coreCallback(eventId, conversation, messages, userMssage, files, callback)

  }
}
