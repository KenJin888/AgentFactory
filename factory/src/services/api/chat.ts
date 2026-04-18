import AiChatAPI, {AiChatCompletionForm, AiChatStats} from '../fastApi/module_ai/ai_chat';
import type {CONVERSATION, CONVERSATION_SETTINGS} from '@/types/chat';
import { useUserStore } from '@/stores/user';

// import { post, del, upload } from '../http';

const toConversation = (data: any): CONVERSATION => {
  let settingsFromModelInfo: Partial<CONVERSATION_SETTINGS> = {};
  if (data?.model_info) {
    try {
      settingsFromModelInfo = JSON.parse(data.model_info);
    } catch {
      settingsFromModelInfo = {};
    }
  }
  return {
    id: String(data.id ?? ''),
    title: data.title || '',
    settings: {
      systemPrompt: '',
      temperature: 0.7,
      contextLength: 4096,
      maxTokens: 2000,
      artifacts: 0,
      enableSearch: false,
      chatMode: 'chat',
      ...settingsFromModelInfo,
      agentId: data.agent_id || settingsFromModelInfo.agentId || '0',
    },
    createdAt: data.created_time ? new Date(data.created_time).getTime() : undefined,
    updatedAt: data.updated_time ? new Date(data.updated_time).getTime() : undefined,
    parentConversationId: data.parent_id ? String(data.parent_id) : null,
  };
};

export const chatApi = {
    getLatestConversation: async ({ agent_id: agentId }: { agent_id: string }): Promise<CONVERSATION | null> => {
      const userStore = useUserStore();
      const userInfo = userStore.userInfo;
      const userId = userInfo?.id;
      if (!userId) {
        return null;
      }
      const res = await AiChatAPI.listAiChat({
        page_no: 1,
        page_size: 1,
        order_by: JSON.stringify([{ created_time: 'desc' }]),
        agent_id: agentId,
        user_id: String(userId),
      });
      const items = res.data?.data?.items || [];
      const latest = items[0];
      if (!latest) {
        return null;
      }
      return toConversation(latest);
    },
    getConversations: async (query: any = {}) => {
      const res = await AiChatAPI.listAiChat(query);
      return res.data;
    },
    getConversation: async (conversation_id: string | number): Promise<CONVERSATION | null> => {
      const res = await AiChatAPI.detailAiChat(Number(conversation_id));
      const data = res.data?.data;
      if (!data) {
        return null;
      }
      return toConversation(data);
    },
    getMessages: async (chatId: string) => {
      const res = await AiChatAPI.listAiChatMsg({ 
        chat_id: chatId, 
        page_size: 100, 
        order_by: JSON.stringify([{ id: 'asc' }]) 
      });
      return res.data;
    },
    createConversation: async (title: string, data: CONVERSATION_SETTINGS) : Promise<CONVERSATION | null>=> {
      const userStore = useUserStore();
      const userInfo = userStore.userInfo;
      const userId = userInfo?.id;
      if (!userId) {
        return null;
      }
      const res = await AiChatAPI.createAiChat({
        agent_id: data.agentId,
        user_id: String(userId),
        title,
        model_info: JSON.stringify(data),
        model_id: data.modelId,
        provider_id: data.providerId
      });
      const created = res.data?.data;
      if (!created) {
        return null;
      }
      return toConversation(created);
    },
    updateConversation: async (id: string, title: string, data: CONVERSATION_SETTINGS) => {
      const userStore = useUserStore();
      const userInfo = userStore.userInfo;
      const userId = userInfo?.id;
      if (!userId) {
        return null;
      }
      const res = await AiChatAPI.updateAiChat(Number(id), {
        agent_id: data.agentId,
        user_id: String(userId),
        title,
        model_info: JSON.stringify(data),
        model_id: data.modelId,
        provider_id: data.providerId
      });
      return res.data;
    },
    // uploadFile: (sessionId: string, formData: FormData) => upload(`/api/sessions/${sessionId}/files`, formData),
    // streamMessage 准备废弃！！
    streamMessage_Delete: async (
      data: AiChatCompletionForm,
      onMessage: (message: any) => void,
      onError?: (error: Error) => void,
      signal?: AbortSignal
    ) => {
      let aiText = '';
      let buffer = '';
      const id = Date.now().toString();
      const conversationId = (data.conversation_id || 0).toString();
      const timestamp = Date.now();

      try {
        await AiChatAPI.chatCompletions(data, (chunk) => {
          buffer += chunk;
          const lines = buffer.split('\n');
          // Keep the last part which might be incomplete
          // But if chunk ends with \n, pop() gives empty string which is correct
          buffer = lines.pop() || '';

          for (const line of lines) {
            if (line.trim() === '') continue;
            if (line.startsWith('data: ')) {
              const str = line.slice(6);
              console.log("str", str)
              if (str === '[DONE]') return;
              try {
                const json = JSON.parse(str);
                const content = json.choices?.[0]?.delta?.content || json.text || '';

                if (content) {
                  aiText += content;
                  onMessage({
                    id,
                    conversationId,
                    role: 'assistant',
                    content: aiText,
                    timestamp,
                    status: 'pending',
                    error: ''
                  });
                } else if (json.error) {
                  aiText += `\n[系统提示: ${json.error}]`;
                  onMessage({
                    id,
                    conversationId,
                    role: 'assistant',
                    content: aiText,
                    timestamp,
                    status: 'error',
                    error: json.error
                  });
                }
              } catch (e) {
                aiText += str;
                onMessage({
                  id,
                  conversationId,
                  role: 'assistant',
                  content: aiText,
                  timestamp,
                  status: 'pending',
                  error: ''
                });
              }
            }
          }
        }, signal);
      } catch (error: any) {
        if (error?.name === 'AbortError' || signal?.aborted) {
          return;
        }
        if (onError) {
          onError(error instanceof Error ? error : new Error('请求失败'));
          return;
        }
        throw error;
      }
    },
    cancelStreamMessage: async (conversationId: string | number) => {
      if (!conversationId) {
        return null
      }
      const res = await AiChatAPI.cancelChatCompletions({ conversation_id: conversationId })
      return res.data
    },
    deleteConversation: async (conversationId: string | number) => {
      if (!conversationId) {
        return null
      }
      const res = await AiChatAPI.deleteAiChat([Number(conversationId)])
      return res.data
    },
    // 获取AI模块统计数据
    getStats: async (forceRefresh?: boolean): Promise<AiChatStats | null> => {
      const res = await AiChatAPI.getStats(forceRefresh)
      return res.data?.data || null
    },
}
