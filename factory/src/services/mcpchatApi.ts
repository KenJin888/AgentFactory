import {CrossMessage} from '@/utils/crossMessage'
import type {AssistantMessageBlock, CONVERSATION_SETTINGS, UserMessageContent} from '@/types/chat'
import AiAgentAPI from '@/services/fastApi/module_ai/ai_agent'
import AiMcpAPI from '@/services/fastApi/module_ai/ai_mcp'

export class McpChatApiService {
  private handleMessage: null | ((payload: any) => void);

  constructor() {
    this.handleMessage = null
    CrossMessage.on('STREAM_RESPONSE', (payload) => {
      if(this.handleMessage) this.handleMessage(payload);
    });
  }

  async createThread(title: string, settings: Partial<CONVERSATION_SETTINGS>) {
    try {
      if (settings.agentId && Number(settings.agentId) > 0) {
        try {
          const res = await AiAgentAPI.detailAiAgent(Number(settings.agentId))
          if (res.data?.data) {
            const agentData = res.data.data
            let config: any = {}
            try {
              config = agentData.config ? JSON.parse(agentData.config) : {}
            } catch (e) {
              console.warn('Failed to parse agent config', e)
            }

            // Merge systemPrompt
            const agentSystemPrompt = agentData.prompt_template || ''
            if (agentSystemPrompt) {
              settings.systemPrompt = agentSystemPrompt
            }

            // Merge externalTools
            const agentTools = (config.mcp?.externalTools || [])
              .filter((item: unknown): item is string => typeof item === 'string' && item.trim().length > 0)
              .map((item: string) => item.trim())
            settings.externalTools = Array.from(new Set(agentTools))
            
            // Merge activeSkills
            const agentSkills = config.mcp?.activeSkills || []
            settings.activeSkills = Array.from(agentSkills)
          }
        } catch (error) {
          console.error('Failed to fetch agent config:', error)
        }
      }

      const payload = {
        title,
        settings
      }
      const response = await CrossMessage.request('CREATE_THREAD', payload, 10000)
      // Todo: 根据返回结果进行工具安装 
      if (response && typeof response === 'object' && (response as any).threadId) {
        return (response as any).threadId
      }
      return null
    } catch (error) {
      console.error('Failed to create thread:', error)
      throw error
    }
  }

  async getMcpConfigsByNames(names: string[]): Promise<Array<{ id: number; name: string; config: any }> | null> {
    const uniqueNames = Array.from(
      new Set(
        (names || [])
          .filter((item): item is string => typeof item === 'string' && item.trim().length > 0)
          .map(item => item.trim())
      )
    )
    if (uniqueNames.length === 0) return null

    const results: Array<{ id: number; name: string; config: any }> = []
    try {
      const res = await AiMcpAPI.listAiMcp({
        page_no: 1,
        page_size: 200,
        status: '0'
      })
      const allItems = res.data?.data?.items || []
      const targetItems = allItems.filter(item => item.name && uniqueNames.includes(item.name))
      for (const target of targetItems) {
        let parsedConfig: any = null
        if (target.config) {
          try {
            parsedConfig = JSON.parse(target.config)
          } catch (error) {
            console.error(`Failed to parse MCP config: ${target.name || target.id}`, error)
            continue
          }
        }
        const id = Number(target.id)
        if (!Number.isInteger(id) || id <= 0) continue
        results.push({id, name: target.name || '', config: parsedConfig})
      }
    } catch (error) {
      console.error('Failed to fetch MCP config list:', error)
    }

    return results.length > 0 ? results : null
  }

  async sendMessage(threadId: string, content: UserMessageContent | AssistantMessageBlock[],
    handleMessage: (payload: any) => void
  ) {
    this.handleMessage = handleMessage
    try {
      const payload = {
        content,
        threadId
      }
      const response = await CrossMessage.request('SEND_MESSAGE', payload, 30000)
      return response ?? null
    } catch (error) {
      console.error('Failed to send message:', error)
      throw error
    }
  }

  async getAgentWorkspacePath(threadId: string): Promise<string | null> {
    try {
      console.log('getAgentWorkspacePath called with threadId:', threadId)
      const response = await CrossMessage.request('GET_AGENT_WORKSPACE_PATH', { threadId }, 5000)
      console.log('getAgentWorkspacePath response:', response)
      if (response && typeof response === 'object' && 'agentWorkspacePath' in response) {
        console.log('agentWorkspacePath:', (response as any).agentWorkspacePath)
        return (response as any).agentWorkspacePath
      }
      console.log('No agentWorkspacePath in response or response is invalid')
      return null
    } catch (error) {
      console.error('Failed to get agent workspace path:', error)
      return null
    }
  }

  async getHtmlFilesInWorkspace(threadId: string): Promise<any | null> {
    try {
      console.log('getHtmlFilesInWorkspace called with threadId:', threadId)
      const response = await CrossMessage.request('GET_HTML_FILES_IN_WORKSPACE', { threadId }, 10000)
      console.log('getHtmlFilesInWorkspace response:', response)
      return response ?? null
    } catch (error) {
      console.error('Failed to get HTML files in workspace:', error)
      return null
    }
  }
}

export const mcpChatApi = new McpChatApiService()
