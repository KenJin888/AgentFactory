// 对接fast api 接口

import { LLM_PROVIDER, LLMCoreStreamEvent, ApiEndpointType, TextStreamEvent, ReasoningStreamEvent, ToolCallStartEvent, ToolCallChunkEvent, ToolCallEndEvent, PermissionRequestEvent, PermissionRequestPayload, ErrorStreamEvent, UsageStreamEvent, StopStreamEvent, ImageDataStreamEvent, RateLimitStreamEvent, ToolCallEvent, LLMAgentEvent } from '@/types/model'
import { BaseLLMProvider, createStreamEvent, SUMMARY_TITLES_PROMPT } from './index'
import { AssistantMessageBlock, ChatMessage, CONVERSATION, MCPToolDefinition, MESSAGE, UserMessageContent } from '@/types/chat'
import AiChatAPI, { AiChatCompletionForm } from '../fastApi/module_ai/ai_chat'

export class FastProvider extends BaseLLMProvider {
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
    if (!this.isInitialized) throw new Error('Provider not initialized')
    const modelId = conversation.settings?.modelId || ''
    const model = this.provider.models?.find((item) => item.id === modelId)
    if(!model) throw new Error(`Model ${modelId} not found`)

    const apiEndpoint = model.userConfig?.apiEndpoint || ApiEndpointType.Chat

    switch (apiEndpoint) {
      case ApiEndpointType.Chat:
      default:
        yield* this.handleChatCompletion(conversation, messages, userMssage, files, signal)
    }
  }

  async coreCallback(eventId:string,conversation: CONVERSATION, messages: MESSAGE[], userMssage: UserMessageContent, files: File[], callback: (event: LLMAgentEvent) => void): Promise<void> {
    
  }

  async *handleChatCompletion(
    conversation: CONVERSATION, messages: MESSAGE[], userMssage: UserMessageContent, files: File[] = [], signal?: AbortSignal
  ): AsyncGenerator<LLMCoreStreamEvent> {
    //-----------------------------------------------------------------------------------------------------
    // 1. 构建请求参数
    //-----------------------------------------------------------------------------------------------------
    // 移除推理模型的温度参数  Todo
    //if(modelConfig?.reasoning) delete requestParams.temperature

    // response_schema: {"schema_key":"formschema"}
    // 

    const requestParams: AiChatCompletionForm = {
      conversation_id: conversation.id || '',
      model: conversation.settings?.modelId,
      provider: conversation.settings?.providerId,
      userMessage: userMssage,
      temperature: 0.1,
      // response_schema: {"schema_key":"formschema"},
      // response_schema: {json_schema: {'$defs': {'InputRule': {'properties': {'field': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'description': '字段名：必须用英文、snake_case 或 camelCase，语义清晰、无空格、无特殊字符。示例：user_name、email_addres', 'title': 'Field'}, 'title': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'description': '用户看到的中文标签/标题，保持文档中的原始表述，简洁准确', 'title': 'Title'}, 'info': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'description': '组件的提 示信息', 'title': 'Info'}, 'value': {'anyOf': [{}, {'type': 'null'}], 'description': '组件的默认值', 'title': 'Value'}, 'style': {'anyOf': [{'type': 'string'}, {'additionalProperties': true, 'type': 'object'}, {'type': 'null'}], 'description': "组件的内联样式, 格式为 {'key': 'value', 'key': 'value'}。示例：{'height': '40px'}", 'title': 'Style'}, '$required': {'anyOf': [{'type': 'boolean'}, {'type': 'string'}, {'type': 'null'}], 'default': null, 'description': '是否必填', 'title': '$Required'}, 'type': {'default': 'input', 'enum': ['input', 'textarea'], 'title': 'Type', 'type': 'string'}, 'props': {'anyOf': [{'additionalProperties': true, 'type': 'object'}, {'type': 'null'}], 'description': '组件额外属性。可以包含合理的 placeholder（如果文档中有暗示）。其他根据上下文添加', 'title': 'Props'}}, 'required': ['field', 'title', 'info', 'value', 'style', 'props'], 'title': 'InputRule', 'type': 'object'}, 'SelectOption': {'properties': {'label': {'description': "选项显示的 文本，例如 '男'", 'title': 'Label', 'type': 'string'}, 'value': {'anyOf': [{'type': 'string'}, {'type': 'integer'}, {'type': 'number'}, {'type': 'boolean'}], 'description': "选项对应的值，例如 'male'", 'title': 'Value'}}, 'required': ['label', 'value'], 'title': 'SelectOption', 'type': 'object'}, 'SelectRule': {'properties': {'field': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'description': '字段名：必须用英文、snake_case 或 camelCase，语义清晰、无空格、无特殊字符。示例：user_name、email_addres', 'title': 'Field'}, 'title': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'description': '用户看到的中文标签/标题，保持文档中的原始表述，简洁准确', 'title': 'Title'}, 'info': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'description': '组件的提示信息', 'title': 'Info'}, 'value': {'anyOf': [{}, {'type': 'null'}], 'description': '组件的默认值', 'title': 'Value'}, 'style': {'anyOf': [{'type': 'string'}, {'additionalProperties': true, 'type': 'object'}, {'type': 'null'}], 'description': "组件的内联样式, 格式为 {'key': 'value', 'key': 'value'}。示例：{'height': '40px'}", 'title': 'Style'}, '$required': {'anyOf': [{'type': 'boolean'}, {'type': 'string'}, {'type': 'null'}], 'default': null, 'description': '是否必填', 'title': '$Required'}, 'type': {'default': 'select', 'enum': ['select', 'radio'], 'title': 'Type', 'type': 'string'}, 'options': {'description': '选项列表', 'items': {'$ref': '#/$defs/SelectOption'}, 'title': 'Options', 'type': 'array'}}, 'required': ['field', 'title', 'info', 'value', 'style', 'options'], 'title': 'SelectRule', 'type': 'object'}}, 'properties': {'form_title': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'default': null, 'description': '整个表单的标题，如果文档中有明显标题则提取', 'title': 'Form Title'}, 'rules': {'description': '字段列表', 'items': {'discriminator': {'mapping': {'input': '#/$defs/InputRule', 'radio': '#/$defs/SelectRule', 'select': '#/$defs/SelectRule', 'textarea': '#/$defs/InputRule'}, 'propertyName': 'type'}, 'oneOf': [{'$ref': '#/$defs/InputRule'}, {'$ref': '#/$defs/SelectRule'}]}, 'title': 'Rules', 'type': 'array'}}, 'required': ['rules'], 'title': 'FormSchema', 'type': 'object'}},

    }
    // console.log('requestParams', requestParams)
    let buffer = '' 
    let pendingBuffer = '' // 累积来自 delta.content 的字符，用于匹配标签和内容
    let currentTextOutputBuffer = '' // 用于累积在所有标签之外的纯文本，准备输出
    let stopReason: 'complete' | 'tool_use' | 'max_tokens' | 'error' | '' = ''
    let toolUseDetected = false // 标记是否检测到工具使用（原生或非原生）
    let usage:
      | {
          prompt_tokens: number
          completion_tokens: number
          total_tokens: number
        }
      | undefined = undefined

    //-----------------------------------------------------------------------------------------------------
    // 流处理循环
    const steam = AiChatAPI.handleChatCompletion(requestParams, files, signal)
    for await (const orgLine of steam) {
      buffer += orgLine;
      const lines = buffer.split('\n');
      // Keep the last part which might be incomplete
      // But if chunk ends with \n, pop() gives empty string which is correct
      buffer = lines.pop() || '';
      for (const line of lines) {
        if (line.trim() === '') continue;
        let str = ''
        if (line.startsWith('data: ')) {
          str = line.slice(6);
          if (str === '[DONE]') {
            stopReason = 'complete';
            yield createStreamEvent.stop(stopReason)
            return // 完成！
          }
        }

        // 错误处理？？
        const chunk = JSON.parse(str)
        const choice = chunk.choices[0]
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const delta = choice?.delta as any
        const currentContent = delta?.content || ''
        // 1. 处理非内容事件 (如 usage, reasoning, tool_calls)

        if(chunk.usage){
          // console.log('chunk.usage', chunk)
          yield createStreamEvent.usage(chunk.usage)
        }

        // 原生 reasoning 内容处理（直接产出）
        if (delta?.reasoning_content || delta?.reasoning) {
            yield createStreamEvent.reasoning(delta.reasoning_content || delta.reasoning)
            continue
        }
        if (delta?.tool_calls?.length > 0) {
          toolUseDetected = true
          // console.log('[handleChatCompletion] Handling native tool_calls', JSON.stringify(delta.tool_calls))
          for (const toolCallDelta of delta.tool_calls) {
            const id = toolCallDelta.id ? toolCallDelta.id : toolCallDelta.function?.name
            const index = toolCallDelta.index
            const functionName = toolCallDelta.function?.name
            const argumentChunk = toolCallDelta.function?.arguments
            const result = toolCallDelta.function?.result
  
            let currentToolCallId: string | undefined = id
  
            if (currentToolCallId) {
              if(!argumentChunk && !result) {
                yield createStreamEvent.toolCallStart(
                  currentToolCallId, functionName)
              }else{
                yield createStreamEvent.toolCall(
                  currentToolCallId, functionName, argumentChunk, result)
              }


            }
          }
          continue // 处理完原生工具调用后继续下一个 chunk
        }

        yield createStreamEvent.text(currentContent)
      }
      // 处理图片数据（OpenRouter Gemini 格式） Todo
    }
  }
}

