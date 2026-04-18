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

            // Merge enabledMcpToolIds
            const agentTools = config.mcp?.enabledMcpToolIds || []
            if(agentTools){
              settings.enabledMcpToolIds = Array.from(agentTools)
            }
            
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

  async getMcpConfigsByIds(ids: number[]): Promise<Array<{ id: number; name: string; config: any }> | null> {
    const uniqueIds = Array.from(
        new Set(
            (ids || [])
                .map(id => Number(id))
                .filter((id) => Number.isInteger(id) && id > 0)
        )
    )
    if (uniqueIds.length === 0) return null

    const results: Array<{ id: number; name: string; config: any }> = []

    for (const id of uniqueIds) {
      try {
        const res = await AiMcpAPI.detailAiMcp(id)
        const target = res.data?.data
        if (!target) continue

        let parsedConfig: any = null
        if (target.config) {
          try {
            parsedConfig = JSON.parse(target.config)
          } catch (error) {
            console.error(`Failed to parse MCP config: ${id}`, error)
            continue
          }
        }

        results.push({
          id,
          name: target.name || '',
          config: parsedConfig
        })
      } catch (error) {
        console.error(`Failed to fetch MCP config by id: ${id}`, error)
      }
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
