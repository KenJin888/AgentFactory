import {defineStore} from 'pinia'
import {api} from '@/services/api'
import type {
  AssistantMessageBlock,
  CONVERSATION,
  CONVERSATION_SETTINGS,
  MESSAGE,
  MESSAGE_ROLE,
  MESSAGE_STATUS,
  UserMessageContent
} from '../types/chat'
import {useModelProviderStore} from './modelProviders'
import {useRuntimeStore} from './runtime'
import {AgentLoopHandler} from '@/services/LLMProvider/agentLoopHandler'
import {LLMEventHandler} from '@/services/LLMProvider/llmEventHandler'
import {parseAssistantStoredContent, parseUserStoredContent} from '@/utils/chatMessage'

export { CONVERSATION_SETTINGS }

// 辅助函数：解析助手消息内容
export const parseAssistantMessage = (msg: any): MESSAGE => {
    const rawContent = typeof msg?.content === 'string' ? msg.content : msg?.content
    const {content, metadata} = parseAssistantStoredContent(rawContent)

  return {
    id: String(msg.id),
    conversation_id: String(msg.chat_id),
    role: 'assistant',
    content,
    metadata,
    status: (msg.status || 'sent') as MESSAGE_STATUS,
    created_at: new Date(msg.created_time).getTime(),
    updated_at: new Date(msg.updated_time).getTime(),
    parent_id: msg.parent_id ? String(msg.parent_id) : undefined
  }
}

const buildUserMessageFiles = (
    selectedFiles: SelectedUploadFile[]
): NonNullable<UserMessageContent['files']> => {
    return selectedFiles.map((selectedFile) => {
        const file = selectedFile.file
        const modifiedAt = file ? new Date(file.lastModified || Date.now()) : new Date()
        return {
            name: selectedFile.name || file?.name || '文件',
            mimeType: file?.type || '',
            token: 0,
            path: selectedFile.url || '',
            metadata: {
                fileName: selectedFile.name || file?.name || '文件',
                fileSize: file?.size || 0,
                fileCreated: modifiedAt,
                fileModified: modifiedAt,
            }
        }
    })
}

type SelectedUploadFile = {
  name: string
  url?: string
  file?: File
}

export const useChatStore = (id = 'default') => {
  const storeDef = defineStore(`chat-${id}`, {
    state: () => ({
      threadId: '',
      currentConversation: {} as CONVERSATION,
      messages: [] as MESSAGE[],
      msgLoading: false
    }),
  actions: {
    // 创建新会话 不影响 currentConversation
    async createConversation(title: string, settings: Partial<CONVERSATION_SETTINGS>,
      options: { newConversation?: boolean } = {}) {
      try {
        const DEFAULT_CONVERSATION_SETTINGS: Partial<CONVERSATION_SETTINGS> = {
            systemPrompt: `You are AiWorks, a highly capable AI assistant. Your goal is to fully complete the user’s requested task before handing the conversation back to them. Keep working autonomously until the task is fully resolved.
Be thorough in gathering information. Before replying, make sure you have all the details necessary to provide a complete solution. Use additional tools or ask clarifying questions when needed, but if you can find the answer on your own, avoid asking the user for help.
When using tools, briefly describe your intended steps first—for example, which tool you’ll use and for what purpose.
Adhere to this in all languages.Always respond in the same language as the user's query.`,
            temperature: 0.7,
            contextLength: 4096,
            maxTokens: 2000,
            artifacts: 0,
            enableSearch: false,
            chatMode: 'chat'
        }
        const normalizedSettings: Partial<CONVERSATION_SETTINGS> = { ...DEFAULT_CONVERSATION_SETTINGS, ...settings }
        const agentId =  normalizedSettings.agentId || '0'
        if(!normalizedSettings.systemPrompt) {
          normalizedSettings.systemPrompt = DEFAULT_CONVERSATION_SETTINGS.systemPrompt || ''
        }
        normalizedSettings.enabledMcpToolIds = normalizedSettings.enabledMcpToolIds || []
        const latestConversation = await api.chat.getLatestConversation({ agent_id: agentId })
        if (!options.newConversation) {
          if (latestConversation) {
            return latestConversation
          }
        }else{
          if(latestConversation?.title === "") {
            return latestConversation
          }
        }
        return await api.chat.createConversation('', normalizedSettings) || {} as CONVERSATION
      } catch (error) {
        console.error('Failed to create thread:', error)
        throw error
      }
    },

    // 获取消息记录
    async getMessages(conversationId: string) {
      try {
        const res = await api.chat.getMessages(conversationId)
        const rawMessages = res.data?.items || []
        
        this.messages = rawMessages.map((msg: any) => {
          if (msg.role === 'assistant') {
            return parseAssistantMessage(msg)
          }

          return {
            id: String(msg.id),
            conversation_id: String(msg.chat_id),
            role: msg.role as MESSAGE_ROLE,
              content: parseUserStoredContent(msg?.content),
            status: (msg.status || 'sent') as MESSAGE_STATUS,
            created_at: new Date(msg.created_time).getTime(),
            updated_at: new Date(msg.updated_time).getTime(),
            parent_id: msg.parent_id ? String(msg.parent_id) : undefined
          } as MESSAGE
        })
        return this.messages
      } catch (e) {
        console.warn("获取消息失败", e)
        throw e
      }
    },

    // 构建对话数据
    async applyConversation(conversationId: string) : Promise<CONVERSATION | null> {
      try {
        this.threadId = ''
        const conversation = await api.chat.getConversation(conversationId)
        if (conversation) {
          const modelProviderStore = useModelProviderStore()
          const { providerId, modelId } = conversation.settings

          const provider = modelProviderStore.llmProviders.find(p => p.id === providerId && p.enable)
          let isValid = false
          
          if (provider && provider.models) {
             isValid = provider.models.some(m => m.id === modelId && m.enabled)
          }

          if (!isValid) {
            const defaultModel = modelProviderStore.getDefaultModel
            if (defaultModel) {
              conversation.settings.providerId = defaultModel.providerId
              conversation.settings.modelId = defaultModel.modelId
              // Update setting file
              await api.chat.updateConversation(conversation.id, conversation.title, conversation.settings)
            }
          }

          this.currentConversation = conversation
          await this.getMessages(conversationId)
          return conversation
        }
        this.currentConversation = {} as CONVERSATION
        return null
      } catch (error) {
        console.error('Failed to get conversation:', error)
        throw error
      }
    },
    async sendMessage(content: UserMessageContent | AssistantMessageBlock[], signal?: AbortSignal, selectedFiles: SelectedUploadFile[] = []) {
      if (!this.currentConversation?.id) return
      const files = selectedFiles
        .map((filePayload) => filePayload.file)
        .filter((file): file is File => Boolean(file))
      const messageFiles = buildUserMessageFiles(selectedFiles)
      const messageText = Array.isArray(content)
        ? content.map((block) => block.content || '').join('')
        : content.text || ''
      const userContent: UserMessageContent = Array.isArray(content)
        ? {
          text: messageText,
          think: false,
          search: false,
              files: messageFiles
        }
          : {
              ...content,
              files: messageFiles.length > 0 ? messageFiles : content.files
          }

      const tempMsg: MESSAGE = {
        id: Date.now().toString(),
        conversation_id: this.currentConversation.id || '',
        role: 'user',
        content: userContent,
        status: 'sent',
        created_at: Date.now(),
        updated_at: Date.now()
      }

      this.messages = [...this.messages, tempMsg]

      try {
        const assistantId = (Date.now() + 1).toString()
        const assistantMsg: MESSAGE = {
          id: assistantId,
          conversation_id: this.currentConversation.id || '',
          role: 'assistant',
          content: [],
          status: 'pending',
          created_at: Date.now(),
          updated_at: Date.now(),
          metadata: {
            inputTokens: 0,
            outputTokens: 0,
            generationTime: 0,
            firstTokenTime: Date.now(),
            totalTokens: 0, 
            tokensPerSecond: 0,
            contextUsage: 0,
          }
        }

        this.messages = [...this.messages, assistantMsg]
        this.msgLoading = true
        const runtimeStore = useRuntimeStore()
        let llmProviderType = "fast"
        if (runtimeStore.runMode === 'Embed') llmProviderType = "deep"
          const loop = new AgentLoopHandler()
          const handle = new LLMEventHandler({
            messages: this.messages,
            generatingMessage: assistantMsg,
            onMessageChanged: (msgs: MESSAGE[]) => {
              this.messages = [...msgs]
            },
            onMessageDone: () => {
              console.log('onMessageDone')
              this.msgLoading = false
            },
            onMessageError: (error: Error) => {
              console.log('onMessageError', error)
              this.msgLoading = false
            }
          })
          if(llmProviderType === "deep"){
            if (signal?.aborted) {
              this.msgLoading = false
              return
            }
            await loop.startCompletion(llmProviderType, 'test_1', this.currentConversation, this.messages, userContent, files, handle.callback)
            return
          }
          const steam = loop.startStreamCompletion(llmProviderType, 'test_1', this.currentConversation, this.messages, userContent, files, signal)
          handle.consume(steam)
      } catch (e) {
        if (signal?.aborted || (e as any)?.name === 'AbortError') {
          this.msgLoading = false
          return
        }
        console.error('Failed to send message:', e)
        const errorMsg: MESSAGE = {
          id: Date.now().toString(),
          conversation_id: this.currentConversation?.id || '',
          role: 'assistant',
          content: [{ type: 'error', content: '[网络错误]', status: 'error', timestamp: Date.now() }],
          status: 'error',
          created_at: Date.now(),
          updated_at: Date.now()
        }
        this.messages = [...this.messages, errorMsg]
      }
    }
  }
  })
  return storeDef()
}
