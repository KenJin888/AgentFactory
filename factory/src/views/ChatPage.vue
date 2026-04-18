<template>
  <div class="flex flex-col h-full min-h-0 bg-slate-50 relative">
    <!-- 页面加载状态 -->
    <div v-if="pageLoading" class="flex h-full items-center justify-center text-slate-400">
      <Loader2 class="animate-spin mr-2" /> 加载会话...
    </div>

    <!-- 聊天界面 -->
    <div v-else class="flex flex-col h-full min-h-0">

      <!-- 顶部导航栏 -->
      <div class="h-16 bg-white border-b border-gray-100 flex items-center justify-between flex-shrink-0 z-10 shadow-sm">
        <div class="max-w-6xl mx-auto w-full px-8 flex items-center justify-between">
          <div class="flex items-center gap-3">
              <button v-if="!isAgentEntryMode" @click="navigateTo('/')" class="md:hidden p-2 text-slate-500"><ArrowLeft :size="20" /></button>
  <div
    class="w-10 h-10 rounded-xl flex items-center justify-center text-white font-bold shadow-sm bg-blue-600"
  >
    <AgentCoverIcon
      v-if="currentAgentId !== '0'"
      :cover="currentAgentCoverRaw"
      :size="20"
      container-class="w-10 h-10 rounded-xl flex items-center justify-center text-white font-bold shadow-sm"
    />
    <span v-else>{{ currentConversation.title?.[0] || '新' }}</span>
  </div>
              <div>
                  <h2 class="font-bold text-slate-800 flex items-center gap-2">{{ currentConversation?.title || '新对话' }}</h2>
                  <!-- 模型选择 -->
                  <ModelSelector v-if="currentConversation" v-model="currentModel" mode="dropdown" placement="bottom" class="shrink-0" />
              </div>
          </div>
          
          <!-- 右侧操作栏 -->
          <div v-if="!isAgentEntryMode" class="flex items-center gap-2">
              <button
                v-if="isDev"
                @click="insertFixedAiReply"
                class="p-2 text-slate-500 hover:text-blue-600 hover:bg-slate-50 rounded-lg transition-colors"
                title="插入AI回复"
              >
                <BotMessageSquare :size="20" />
              </button>
              <button
                @click="handleNewChat"
                class="p-2 text-slate-500 hover:text-blue-600 hover:bg-slate-50 rounded-lg transition-colors"
                title="新对话"
              >
                <Plus :size="20" />
              </button>
              <button
                @click="toggleHistory"
                :class="[
                  'p-2 rounded-lg transition-colors',
                  showHistory ? 'text-blue-600 bg-blue-50' : 'text-slate-500 hover:text-blue-600 hover:bg-slate-50'
                ]"
                title="历史记录"
              >
                <History :size="20" />
              </button>
          </div>
        </div>
      </div>

      <MessageList
        ref="messageListRef"
        :messages="messages"
        :msg-loading="msgLoading"
        :user-avatar-url="userAvatarUrl"
        :agent-config="agentConfig"
        :messages-end-ref="messagesEndRef"
      />

      <ChatInput
        v-model:input="input"
        v-model:uploadFiles="uploadFiles"
        v-model:enableWebSearch="enableWebSearch"
        :agent-config="agentConfig"
        :is-uploading="isUploading"
        :is-recording="isRecording"
        :msg-loading="msgLoading"
        :stop-loading="isStoppingMessage"
        @send="handleSend"
        @stop="handleStop"
        @file-select="handleFileSelect"
        @toggle-recording="toggleRecording"
      />
    </div>
    <!-- 历史记录侧边栏 -->
    <div v-if="showHistory && !isAgentEntryMode" class="absolute inset-0 z-50 flex justify-end">
      <!-- 遮罩层 -->
      <div class="absolute inset-0 bg-black/20 backdrop-blur-sm" @click="showHistory = false"></div>
      
      <!-- 侧边栏内容 -->
      <div class="relative w-80 bg-white h-full shadow-2xl flex flex-col animate-in slide-in-from-right duration-200">
        <div class="p-4 border-b border-gray-100 flex items-center justify-between bg-slate-50/50">
          <h3 class="font-bold text-slate-700 flex items-center gap-2">
            <History :size="18" /> 历史对话
          </h3>
          <button @click="showHistory = false" class="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg">
            <X :size="18" />
          </button>
        </div>
        
        <div class="flex-1 overflow-y-auto p-3 space-y-2">
          <div v-if="historyLoading" class="flex justify-center py-8 text-slate-400">
            <Loader2 class="animate-spin" />
          </div>
          
          <template v-else>
            <div 
              v-for="session in historySessions" 
              :key="session.id"
              @click="switchToConversation(session)"
              :class="[
                'group p-3 rounded-xl cursor-pointer border transition-all hover:shadow-sm',
                currentConversation?.id === String(session.id)
                  ? 'bg-blue-50 border-blue-200 ring-1 ring-blue-100'
                  : 'bg-white border-gray-100 hover:border-blue-200 hover:bg-slate-50'
              ]"
            >
              <div class="mb-1 flex items-start justify-between gap-2">
                <div class="font-medium text-slate-800 text-sm line-clamp-1 flex-1">{{ session.title || '无标题对话' }}</div>
                <button
                  :disabled="deletingHistoryId === String(session.id)"
                  class="p-1 text-slate-300 hover:text-red-500 hover:bg-red-50 rounded-md opacity-0 group-hover:opacity-100 transition-all disabled:opacity-60"
                  title="删除会话"
                  @click.stop="handleDeleteHistorySession(session)"
                >
                  <Loader2 v-if="deletingHistoryId === String(session.id)" class="animate-spin" :size="12" />
                  <Trash2 v-else :size="12" />
                </button>
              </div>
              <div class="flex items-center justify-between text-xs text-slate-400">
                 <span class="flex items-center gap-1">
                   <MessageSquare :size="12" />
                   {{ session.settings?.modelId || 'Default' }}
                 </span>
                 <span class="flex items-center gap-1">
                   <Clock :size="12" />
                   {{ new Date(session.updated_time || session.created_time).toLocaleDateString() }}
                 </span>
              </div>
            </div>
            
            <div v-if="historySessions.length === 0" class="text-center py-10 text-slate-400 text-sm">
              暂无历史记录
            </div>
          </template>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import {computed, nextTick, onBeforeUnmount, onMounted, ref, watch, onDeactivated} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {storeToRefs} from 'pinia'
import {MAX_SESSION_TABS, useTagsViewStore} from '@/stores/tagsView'
import { ArrowLeft, BotMessageSquare, Clock, History, Loader2, MessageSquare, Plus, Trash2, X } from 'lucide-vue-next'
import type {MESSAGE, UserMessageContent} from '../types/chat'
import {api} from '../services/api'
import MessageList from '../components/chat/MessageList.vue'
import ChatInput from '../components/chat/ChatInput.vue'
import {useChatStore} from '../stores/chat'
import {useUserStore} from '../stores/user'
import type {MODEL_META} from '@/types/model'
import {useModelProviderStore} from '../stores/modelProviders'
import ModelSelector from '@/components/common/ModelSelector.vue'
import AgentCoverIcon from '@/components/common/AgentCoverIcon.vue'
import AiAgentAPI, { type AiAgentConfig } from '@/services/fastApi/module_ai/ai_agent'
import { message } from '@/components/common/message'
import { dialog } from '@/components/common/dialog'
// import { Agent } from 'http'

// 用户 store
const userStore = useUserStore()


// Vue Router 实例
const router = useRouter()
const route = useRoute()
const tagsViewStore = useTagsViewStore()
// Freeze route params since component is not reused across different paths
const initialConversationId = route.params.conversationId as string
const initialAgentId = route.params.agentid as string | undefined
const conversationId = ref(initialConversationId)
const agentIdFromRoute = ref(initialAgentId)
const isAgentEntryMode = ref(route.name === 'AgentEntry')

// 响应式数据
const storeId = conversationId.value || agentIdFromRoute.value || 'default'
const chatStore = useChatStore(storeId)
const {currentConversation, messages, msgLoading } = storeToRefs(chatStore)
const modelProviderStore = useModelProviderStore()
const { providers } = storeToRefs(modelProviderStore)

// 当前用户 - 从 store 获取
const currentUser = computed(() => userStore.userInfo)

const availableModels = computed<MODEL_META[]>(() =>
  providers.value
    .filter((provider) => provider.isEnabled)
    .flatMap((provider) =>
      provider.config.models
        .filter((model) => model.enabled !== false)
        .map((model) => ({...model, group: provider.name, providerId: provider.id}))
    )
)

const currentModel = computed({
  get: () => {
    if (!currentConversation.value?.settings) return null
    const { providerId, modelId } = currentConversation.value.settings
    return availableModels.value.find(m => m.providerId === providerId && m.id === modelId) || null
  },
  set: async (model: MODEL_META | null) => {
    if (!currentConversation.value || !model) return
    if (!currentConversation.value.settings) currentConversation.value.settings = {}
    
    currentConversation.value.settings.providerId = model.providerId
    currentConversation.value.settings.modelId = model.id
    
    try {
        await api.chat.updateConversation(
          currentConversation.value.id,
          currentConversation.value.title || "新对话",
          currentConversation.value.settings
        )
    } catch (e) {
      console.error("更新会话模型失败:", e)
    }
  }
})

const agentConfig = computed(() => {
  const s = (currentConversation.value?.settings ?? {}) as Record<string, any>
  return {
    enable_thinking: !!(s.enableThinking || s.enable_thinking),
    enable_upload: true, // !!(s.enableUpload || s.enable_upload),
    enable_search: !!(s.enableSearch || s.enable_search),
    enable_voice: !!(s.enableVoice || s.enable_voice),
    creator_id: currentAgentId.value
  }
})

type SelectedUploadFile = {
  name: string
  url?: string
  file?: File
}

const input = ref('')
const pageLoading = ref(true)
const errorMsg = ref('')
const isStoppingMessage = ref(false)
const streamAbortController = ref<AbortController | null>(null)
const isUploading = ref(false)
const uploadFiles = ref<SelectedUploadFile[]>([])
const isRecording = ref(false)
const enableWebSearch = ref(false)
const showHistory = ref(false)
const historySessions = ref<any[]>([])
const historyLoading = ref(false)
const deletingHistoryId = ref<string | null>(null)

const userAvatarUrl = computed(() => currentUser.value?.avatar)
const currentAgentCoverRaw = ref('')
const currentAgentId = computed(() => {
  const settings = (currentConversation.value?.settings ?? {}) as Record<string, unknown>
  const raw = settings.agentId || settings.agent_id
  return typeof raw === 'string' || typeof raw === 'number' ? String(raw) : ''
})

// DOM 引用
const messageListRef = ref<{ scrollContainerRef: HTMLDivElement | null } | null>(null)
const messagesEndRef = ref<HTMLDivElement | null>(null)

// 语音识别引用
let recognitionRef: any = null

// 导航方法
const navigateTo = (path: string) => {
  router.push(path)
}

const parseModel = (value?: string): MODEL_META | null => {
  if (!value) return null
  try {
    const parsed = JSON.parse(value)
    return typeof parsed === 'object' && parsed ? parsed : null
  } catch {
    return null
  }
}

const parseAgentConfig = (value?: string): AiAgentConfig | null => {
  if (!value) return null
  try {
    const parsed = JSON.parse(value)
    return typeof parsed === 'object' && parsed ? parsed as AiAgentConfig : null
  } catch {
    return null
  }
}

const renderWelcomeMessageIfNeeded = async (preloadedWelcome = '') => {
  if (messages.value.length > 0) return

  const settings = (currentConversation.value?.settings ?? {}) as Record<string, unknown>
  const rawAgentId = settings.agentId || settings.agent_id
  const normalizedAgentId = Number(rawAgentId)
  if (!Number.isInteger(normalizedAgentId) || normalizedAgentId <= 0) return

  let welcomeText = preloadedWelcome.trim()
  if (!welcomeText) {
    try {
      const agentRes = await AiAgentAPI.detailAiAgent(normalizedAgentId)
      const agent = agentRes.data?.data
      const config = parseAgentConfig(agent?.config)
      welcomeText = config?.welcome?.trim() || ''
    } catch (error) {
      console.error('加载智能体开场白失败:', error)
      return
    }
  }

  if (!welcomeText) return

  const now = Date.now()
  const welcomeMessage: MESSAGE = {
    id: `welcome-welcome`, // 开场白
    conversation_id: currentConversation.value?.id || '',
    role: 'assistant',
    content: [
      {
        type: 'content',
        content: welcomeText,
        status: 'success',
        timestamp: now
      }
    ],
    status: 'sent',
    created_at: now,
    updated_at: now
  }
  messages.value = [welcomeMessage]
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    const scrollContainer = messageListRef.value?.scrollContainerRef
    if (scrollContainer) {
      // 使用 scrollTop 强制滚动到底部
      scrollContainer.scrollTop = scrollContainer.scrollHeight
    }
  })
}

// 监听消息变化，自动滚动到底部
watch([messages, msgLoading, uploadFiles], scrollToBottom)
watch(
  currentAgentId,
  async (agentId) => {
    currentAgentCoverRaw.value = ''
    const normalizedAgentId = Number(agentId)
    if (!Number.isInteger(normalizedAgentId) || normalizedAgentId <= 0) return
    try {
      const res = await AiAgentAPI.detailAiAgent(normalizedAgentId)
      currentAgentCoverRaw.value = res.data?.data?.cover || ''
    } catch (error) {
      console.error('加载智能体封面失败:', error)
    }
  },
  { immediate: true }
)

// 初始化数据
const initData = async () => {
  if (!conversationId.value && !isAgentEntryMode.value) return
  
  try {
    pageLoading.value = true
    errorMsg.value = ''

    if (isAgentEntryMode.value) {
      const normalizedAgentId = Number(agentIdFromRoute.value || 0)
      if (!Number.isInteger(normalizedAgentId) || normalizedAgentId <= 0) {
        errorMsg.value = '智能体参数无效'
        pageLoading.value = false
        return
      }
      if (await checkSessionGuard(String(normalizedAgentId))) {
        pageLoading.value = false
        return
      }

      const defaultModel = modelProviderStore.getDefaultModel
      const settings = {
        agentId: String(normalizedAgentId),
        providerId: defaultModel?.providerId,
        modelId: defaultModel?.modelId,
      }
      let conversationTitle = '专属智能体会话'
      let welcomeText = ''

      try {
        const agentRes = await AiAgentAPI.detailAiAgent(normalizedAgentId)
        const agent = agentRes.data?.data
        if (agent) {
          conversationTitle = agent.name || conversationTitle
          const agentModel = parseModel(agent.model)
          const agentConfig = parseAgentConfig(agent.config)
          welcomeText = agentConfig?.welcome?.trim() || ''
          settings.providerId = agentModel?.providerId || settings.providerId
          settings.modelId = agentModel?.id || settings.modelId
        }
      } catch (error) {
        console.error('加载智能体详情失败:', error)
      }

      const conversation = await chatStore.createConversation(
        conversationTitle,
        settings,
        { newConversation: false }
      )
      if (!conversation?.id) {
        errorMsg.value = '无法创建智能体会话'
        pageLoading.value = false
        return
      }

      tagsViewStore.registerConversationAgent(conversation.id, String(normalizedAgentId))
      await chatStore.applyConversation(conversation.id)
      await syncCurrentSessionTag()
      await renderWelcomeMessageIfNeeded(welcomeText)
      return
    }

    try {
      const conversation = await chatStore.applyConversation(conversationId.value)
      // console.log("获取会话:", conversation)
      const canStay = await syncCurrentSessionTag()
      if (!canStay) {
        return
      }
      await renderWelcomeMessageIfNeeded()
    } catch (e: any) {
      console.error("加载会话失败:", e.status, e.message)
      errorMsg.value = e.status === 404 ? "会话不存在或接口未更新 (请重启后端)" : `无法加载会话 (${e.status || '未知'})`
      pageLoading.value = false
      return
    }

  } catch (e: any) {
    console.error("网络错误详情:", e)
    errorMsg.value = "网络连接失败，请检查后端服务是否启动"
  } finally {
    pageLoading.value = false
    scrollToBottom()
  }
}

// 文件选择处理
const handleFileSelect = (event: Event) => {
  const fileInput = event.target as HTMLInputElement
  const files = fileInput.files
  if (!files || files.length === 0) return

  uploadFiles.value = [
    ...uploadFiles.value,
    ...Array.from(files).map((file) => ({
      name: file.name,
      file
    }))
  ]
  fileInput.value = ''
}

// 语音输入切换
const toggleRecording = () => {
  if (isRecording.value) {
    try {
      recognitionRef?.stop()
    } catch (e) {
      console.error("停止录音失败:", e)
    }
    isRecording.value = false
    return
  }
  
  // 检查浏览器支持
  const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
  if (!SpeechRecognition) {
    alert("浏览器不支持语音识别")
    return
  }
  
  // 创建语音识别实例
  const rec = new SpeechRecognition()
  rec.lang = 'zh-CN'
  rec.interimResults = true
  
  rec.onstart = () => {
    isRecording.value = true
  }
  
  rec.onend = () => {
    isRecording.value = false
  }
  
  rec.onresult = (e: any) => {
    let txt = ''
    for (let i = e.resultIndex; i < e.results.length; ++i) {
      if (e.results[i].isFinal) {
        txt += e.results[i][0].transcript
      }
    }
    if (txt) {
      input.value += txt
    }
  }
  
  rec.start()
  recognitionRef = rec
}

// 切换历史记录显示
const toggleHistory = () => {
  if (isAgentEntryMode.value) return
  showHistory.value = !showHistory.value
  if (showHistory.value) {
    loadHistory()
  }
}

// 加载历史记录
const loadHistory = async () => {
  if (!currentUser.value?.id) return
  
  try {
    historyLoading.value = true
    const res = await api.chat.getConversations({ 
      user_id: currentUser.value.id,
      agent_id: currentConversation.value?.settings.agentId,
      page_size: 50, // 获取最近50条
      order_by: JSON.stringify([{ updated_time: 'desc' }])
    })
    historySessions.value = res.data?.items || []
  } catch (e) {
    console.error("加载历史记录失败:", e)
  } finally {
    historyLoading.value = false
  }
}

const handleDeleteHistorySession = async (session: any) => {
  const sessionId = String(session?.id || '')
  if (!sessionId || deletingHistoryId.value) return

  try {
    await dialog.confirm(
      `确定删除会话「${session.title || '无标题对话'}」吗？`,
      '删除会话',
      { type: 'danger', confirmText: '删除', cancelText: '取消' }
    )

    deletingHistoryId.value = sessionId
    await api.chat.deleteConversation(sessionId)
    historySessions.value = historySessions.value.filter(item => String(item.id) !== sessionId)
    message.success('会话删除成功')

    if (String(currentConversation.value?.id || '') === sessionId) {
      if (historySessions.value.length > 0) {
        navigateTo(`/chat/${historySessions.value[0].id}`)
      } else {
        await handleNewChat()
      }
      showHistory.value = false
    }
  } catch (error: any) {
    if (error instanceof Error && error.message === 'Cancel') {
      return
    }
    console.error('删除历史会话失败:', error)
    message.error(error?.message || '删除会话失败，请稍后重试')
  } finally {
    deletingHistoryId.value = null
  }
}

// 插入固定 AI 回复
const isDev = false // import.meta.env.DEV
const insertFixedAiReply = () => {
  const now = Date.now()
  const fixedReply: import('../types/chat').MESSAGE = {
    id: `fixed-${now}`,
    role: 'assistant',
    status: 'sent',
    content: [
      {
        type: 'content',
        content: '您好！我是AI助手，有什么可以帮助您的吗？\n我都很乐意协助！请告诉我你想做什么，或者有什么我可以帮你的吗？',
        status: 'success',
        timestamp: now
      },
      {
        type: 'search',
        content: '搜索结果：找到相关文档3篇。',
        status: 'success',
        timestamp: now
      },
      {
        type: 'reasoning_content',
        content: '这是一段推理过程内容，用于展示模型的思考步骤。',
        status: 'success',
        timestamp: now,
        reasoning_time: { start: now - 1000, end: now }
      },
      {
        type: 'plan',
        content: '1. 分析问题\n2. 查找资料\n3. 给出答案',
        status: 'success',
        timestamp: now,
        extra: {
          plan_entries: [
            { title: '分析问题', content: '理解用户需求，明确目标', status: 'done' },
            { title: '查找资料', content: '搜索相关文档和知识库', status: 'completed' },
            { title: '给出答案', content: '整理信息并生成回复', status: 'pending' }
          ]
        } as any
      },
      {
        type: 'error',
        content: '发生了一个错误：请求超时，请重试。',
        status: 'error',
        timestamp: now
      },
      {
        type: 'tool_call',
        content: '调用工具：get_weather',
        status: 'success',
        timestamp: now,
        tool_call: {
          id: 'tool-001',
          name: 'get_weather',
          params: JSON.stringify({ city: '北京' }),
          response: JSON.stringify({ temp: '25°C', weather: '晴' }),
          server_name: 'weather-server',
          server_icons: '',
          server_description: '天气查询服务'
        }
      },
      {
        type: 'action',
        content: '请求工具调用权限',
        status: 'pending',
        timestamp: now,
        action_type: 'tool_call_permission'
      },
      {
        type: 'image',
        content: '图片示例',
        status: 'success',
        timestamp: now,
        image_data: {
          data: 'data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20width%3D%22400%22%20height%3D%22200%22%20viewBox%3D%220%200%20400%20200%22%3E%3Cdefs%3E%3ClinearGradient%20id%3D%22g%22%20x1%3D%220%25%22%20x2%3D%22100%25%22%20y1%3D%220%25%22%20y2%3D%22100%25%22%3E%3Cstop%20offset%3D%220%25%22%20stop-color%3D%22%23dbeafe%22/%3E%3Cstop%20offset%3D%22100%25%22%20stop-color%3D%22%23bfdbfe%22/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect%20width%3D%22400%22%20height%3D%22200%22%20rx%3D%2216%22%20fill%3D%22url(%23g)%22/%3E%3Ctext%20x%3D%22200%22%20y%3D%2290%22%20text-anchor%3D%22middle%22%20font-size%3D%2224%22%20font-family%3D%22Arial%2C%20sans-serif%22%20fill%3D%22%231e3a8a%22%3E%E7%A6%BB%E7%BA%BF%E7%A4%BA%E4%BE%8B%E5%9B%BE%E7%89%87%3C/text%3E%3Ctext%20x%3D%22200%22%20y%3D%22124%22%20text-anchor%3D%22middle%22%20font-size%3D%2214%22%20font-family%3D%22Arial%2C%20sans-serif%22%20fill%3D%22%23334155%22%3EInternal%20Demo%20Image%3C/text%3E%3C/svg%3E',
          mimeType: 'image/svg+xml'
        }
      },
      {
        type: 'artifact-thinking',
        content: '正在生成代码片段，请稍候...',
        status: 'success',
        timestamp: now,
        artifact: {
          identifier: 'artifact-001',
          title: '示例代码',
          type: 'application/vnd.ant.code',
          language: 'typescript'
        }
      },
      {
        type: 'mcp_ui_resource',
        content: 'MCP UI 资源',
        status: 'success',
        timestamp: now,
        mcp_ui_resource: {
          uri: '',
          mimeType: 'text/html',
          text: '<p>Hello MCP UI</p>'
        }
      },
    ],
    created_at: now,
    updated_at: now
  }
  messages.value = [...messages.value, fixedReply]
  scrollToBottom()
}

// 新建对话
const handleNewChat = async () => {
  if (isAgentEntryMode.value) return
  try {
    const settings = currentConversation.value?.settings || {}
    const settingsRecord = settings as Record<string, unknown>
    const normalizedAgentId = tagsViewStore.normalizeAgentId(settingsRecord.agentId || settingsRecord.agent_id || '0') || '0'
    if (await checkSessionGuard(normalizedAgentId)) {
      return
    }
    // 使用当前会话的配置作为默认配置，如果没有则使用默认
    const nextSettings = {
      ...settings,
      agentId: normalizedAgentId
    }
    const conversation = await chatStore.createConversation(
      "新对话", 
      nextSettings, 
      { newConversation: true } // 强制新建
    )
    
    if (conversation && conversation.id) {
      if(String(conversation.id) === String(currentConversation.value?.id)){
        showHistory.value = false
        return
      }
      tagsViewStore.registerConversationAgent(conversation.id, normalizedAgentId)
      await navigateToExistingSession(`/chat/${conversation.id}`, true)
      showHistory.value = false // 关闭历史记录
    }
  } catch (e) {
    console.error("创建新对话失败:", e)
  }
}

// 切换对话
const switchToConversation = async (session: any) => {
  if (session.id === String(currentConversation.value?.id)) {
    showHistory.value = false
    return
  }
  await navigateToExistingSession(`/chat/${session.id}`, true)
  showHistory.value = false
}

const handleStop = async () => {
  if ((!msgLoading.value && !streamAbortController.value) || isStoppingMessage.value) return

  const activeConversationId = currentConversation.value?.id || conversationId.value
  const activeController = streamAbortController.value

  isStoppingMessage.value = true
  streamAbortController.value = null
  activeController?.abort()
  // finalizeAssistantMessage(true)

  if (!activeConversationId) {
    isStoppingMessage.value = false
    return
  }

  try {
    await api.chat.cancelStreamMessage(activeConversationId)
  } catch (e) {
    console.warn('停止对话失败:', e)
  } finally {
    isStoppingMessage.value = false
  }
}

const componentFullPath = route.fullPath
const handleTagClosed = (event: Event) => {
  const customEvent = event as CustomEvent<{ fullPath?: string }>
  if (customEvent.detail?.fullPath === componentFullPath) {
    cleanup()
  }
}

const navigateToExistingSession = async (fullPath: string, removeCurrentTag = false) => {
  if (removeCurrentTag) {
    const currentTag = tagsViewStore.visitedViews.find((item) => item.fullPath === route.fullPath)
    if (currentTag) {
      const removedTags = tagsViewStore.delView(currentTag)
      removedTags.forEach((tag) => {
        window.dispatchEvent(new CustomEvent('tags-view:closed', { detail: { fullPath: tag.fullPath } }))
      })
    }
  }
  if (route.fullPath !== fullPath) {
    await router.replace(fullPath)
  }
}

const checkSessionGuard = async (agentId: unknown, excludeCurrent = false) => {
  // “会话页签守卫”，用于在创建/切换会话前做拦截，避免重复页签和超出上限。
  // 修改为本地打开页签，该功能应该取消？？
  return false
}

const syncCurrentSessionTag = async () => {
  const activeConversationId = currentConversation.value?.id || conversationId.value
  const normalizedAgentId = tagsViewStore.normalizeAgentId(currentAgentId.value || '0') || '0'
  if (!activeConversationId) {
    return true
  }
  tagsViewStore.registerConversationAgent(activeConversationId, normalizedAgentId)
  tagsViewStore.updateVisitedView({
    fullPath: route.fullPath,
    conversationId: activeConversationId,
    agentId: normalizedAgentId
  })
  const duplicatedTab = tagsViewStore.findSessionTabByAgentId(normalizedAgentId, route.fullPath)
  if (duplicatedTab) {
    await navigateToExistingSession(duplicatedTab.fullPath, true)
    return false
  }
  return true
}

let isDisposed = false
const cleanup = () => {
  if (isDisposed) return
  isDisposed = true
  handleStop()
  chatStore.$dispose()
}

onDeactivated(() => {
  // If the component's original fullPath is no longer in visitedViews, this tab was closed
  const isClosed = !tagsViewStore.visitedViews.some(v => v.fullPath === componentFullPath)
  if (isClosed) {
    cleanup()
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('tags-view:closed', handleTagClosed as EventListener)
  cleanup()
})

// 发送消息
const handleSend = async () => {
  if ((!input.value.trim() && uploadFiles.value.length === 0) || msgLoading.value || isUploading.value ) return;

  const userText = input.value;
  const filePayloads = [...uploadFiles.value];

  // 如果是第一条消息，更新对话标题
  if (messages.value.length === 0 && currentConversation.value && userText.trim()) {
      const newTitle = userText.trim().substring(0, 50);
      currentConversation.value.title = newTitle;
      
      // 异步更新数据库，不阻塞发送流程
      api.chat.updateConversation(
          currentConversation.value.id,
          newTitle,
          currentConversation.value.settings
      ).then(() => {
          // props.refreshSessions?.();
      }).catch(err => console.error("更新会话标题失败:", err));
  }

  const contentPayload: UserMessageContent = {
    text: userText,
    // think: false,
    // search: enableWebSearch.value
  }

  input.value = ''
  uploadFiles.value = []
  isUploading.value = filePayloads.length > 0
  streamAbortController.value = new AbortController()

  try {
    await chatStore.sendMessage(contentPayload, streamAbortController.value.signal, filePayloads)
  } finally {
    isUploading.value = false
    scrollToBottom()
  }
};

// 组件挂载时初始化数据
onMounted(() => {
  window.addEventListener('tags-view:closed', handleTagClosed as EventListener)
  modelProviderStore.initModels().finally(() => {
    initData()
  })
})


</script>
