<template>
  <div class="h-full flex flex-col bg-gray-50 overflow-hidden relative">
    <div v-if="isCreatingSession" class="absolute inset-0 bg-white/50 backdrop-blur-sm z-50 flex items-center justify-center">
      <div class="flex flex-col items-center gap-2">
        <Loader2 class="animate-spin text-blue-600" :size="32" />
        <p class="text-sm font-medium text-slate-600">正在进入会话...</p>
      </div>
    </div>
    <div class="px-8 py-6 bg-slate-50 border-b border-gray-100 flex-shrink-0">
      <div class="max-w-6xl mx-auto flex flex-col md:flex-row gap-4 items-center justify-between">
        <div class="w-full md:w-auto flex-shrink-0">
          <h1 class="text-2xl font-bold text-slate-900">我的空间</h1>
          <p class="mt-1 text-sm text-slate-500">管理个人会话与专属智能体。</p>
        </div>
        <div class="w-full md:w-auto flex flex-col md:flex-row items-stretch md:items-center gap-3 md:justify-end">
          <input
            ref="fileInput"
            type="file"
            accept=".json"
            class="hidden"
            @change="handleFileSelect"
          />
          <div class="relative group h-11">
            <button
              @click="handleCreateClick"
              :class="`h-full px-5 text-white rounded-xl font-bold shadow-lg transition-all flex items-center gap-2 active:scale-95 bg-slate-900 hover:bg-slate-800`"
            >
              <Plus :size="18" />
              创建智能体
              <ChevronDown :size="18" class="ml-1 -mr-1 opacity-80" />
            </button>
            <div class="absolute right-0 top-full pt-2 w-40 hidden group-hover:block z-50">
              <div class="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden py-1">
                <button
                  class="w-full px-4 py-2.5 text-left text-slate-600 hover:bg-slate-50 hover:text-blue-600 font-medium transition-all flex items-center gap-2"
                  @click="handleCreateClick"
                >
                  <Bot :size="16" />
                  新智能体
                </button>
                <button
                  class="w-full px-4 py-2.5 text-left text-slate-600 hover:bg-slate-50 hover:text-blue-600 font-medium transition-all flex items-center gap-2"
                  @click="handleImportClick"
                >
                  <Upload :size="16" />
                  从文件导入
                </button>
                <button
                  class="w-full px-4 py-2.5 text-left text-slate-600 hover:bg-slate-50 hover:text-blue-600 font-medium transition-all flex items-center gap-2"
                  @click="handleSmartCreateClick"
                >
                  <Sparkles :size="16" />
                  智能创建
                </button>
                <div class="h-px bg-slate-100 my-1 mx-2"></div>
                <button
                  class="w-full px-4 py-2.5 text-left text-slate-600 hover:bg-slate-50 hover:text-blue-600 font-medium transition-all flex items-center gap-2"
                  @click="handleRefreshPage"
                >
                  <RefreshCw :size="16" />
                  刷新页面
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="loading" class="flex-1 flex items-center justify-center">
      <div class="text-center text-gray-500">正在加载智能体...</div>
    </div>
    <div v-else class="flex-1 overflow-y-auto p-8">
      <div class="max-w-6xl mx-auto">
        <!-- 统计卡片 -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-10">
          <!-- 本周Token消耗 -->
          <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 flex items-center gap-4">
            <div class="w-14 h-14 rounded-xl bg-indigo-50 flex items-center justify-center flex-shrink-0">
              <TrendingUp class="w-7 h-7 text-indigo-600" />
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between mb-0.5">
                <p class="text-sm text-slate-500">本周 Token 消耗</p>
              </div>
              <p v-if="statsLoading" class="text-2xl font-bold text-slate-300">--</p>
              <p v-else class="text-2xl font-bold text-slate-900">{{ formatNumber(weekStats.weekTokens) }} <span class="text-sm font-normal text-slate-400">Tokens</span></p>
            </div>
          </div>

          <!-- 本周会话次数 -->
          <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 flex items-center gap-4">
            <div class="w-14 h-14 rounded-xl bg-emerald-50 flex items-center justify-center flex-shrink-0">
              <MessageSquare class="w-7 h-7 text-emerald-600" />
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between mb-0.5">
                <p class="text-sm text-slate-500">本周会话次数</p>
              </div>
              <p v-if="statsLoading" class="text-2xl font-bold text-slate-300">--</p>
              <p v-else class="text-2xl font-bold text-slate-900">{{ formatNumber(weekStats.weekChats) }} <span class="text-sm font-normal text-slate-400">次对话</span></p>
            </div>
          </div>

          <!-- 总Token消耗 -->
          <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 flex items-center gap-4">
            <div class="w-14 h-14 rounded-xl bg-blue-50 flex items-center justify-center flex-shrink-0">
              <Database class="w-7 h-7 text-blue-600" />
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm text-slate-500 mb-0.5">总 Token 消耗</p>
              <p v-if="statsLoading" class="text-2xl font-bold text-slate-300">--</p>
              <p v-else class="text-2xl font-bold text-slate-900">{{ formatNumber(overviewData.total_tokens) }} <span class="text-sm font-normal text-slate-400">Tokens</span></p>
            </div>
          </div>

          <!-- 总会话次数 -->
          <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 flex items-center gap-4">
            <div class="w-14 h-14 rounded-xl bg-amber-50 flex items-center justify-center flex-shrink-0">
              <History class="w-7 h-7 text-amber-600" />
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm text-slate-500 mb-0.5">总会话次数</p>
              <p v-if="statsLoading" class="text-2xl font-bold text-slate-300">--</p>
              <p v-else class="text-2xl font-bold text-slate-900">{{ formatNumber(overviewData.total_chats) }} <span class="text-sm font-normal text-slate-400">次对话</span></p>
            </div>
          </div>
        </div>

        <!-- 现有的智能体区 -->
        <div>
          <div 
            class="flex items-center gap-2 mb-4 cursor-pointer select-none text-slate-800 hover:text-blue-600 transition-colors w-fit group"
            @click="isEditExpanded = !isEditExpanded"
          >
            <component :is="isEditExpanded ? ChevronDown : ChevronRight" :size="20" class="text-slate-400 group-hover:text-blue-500 transition-colors" />
            <h2 class="text-lg font-bold">我的智能体</h2>
          </div>
          <div v-show="isEditExpanded">
            <div v-if="filteredAgents.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              <AgentCard
                v-for="agent in filteredAgents"
                :key="agent.id"
                :agent="agent"
                :onClick="() => handleAgentClick(agent)"
                :onEdit="handleEditClick"
                :onPublish="handlePublishAgent"
                :onDelete="handleDeleteAgent"
              />
            </div>
            <div v-else class="py-12 flex flex-col items-center justify-center text-slate-500 bg-white rounded-2xl border border-slate-200 border-dashed transition-colors hover:bg-slate-50/50">
              <FileEdit :size="48" class="text-slate-300 mb-3" />
              <p class="text-[15px] font-medium text-slate-500">请点击右上按钮创建智能体。</p>
            </div>
          </div>
        </div>

        <!-- 详细消耗明细 -->
        <div class="mt-10 mb-6">
          <div
            class="flex items-center gap-2 mb-4 cursor-pointer select-none text-slate-800 hover:text-blue-600 transition-colors w-fit group"
            @click="isDetailExpanded = !isDetailExpanded"
          >
            <component :is="isDetailExpanded ? ChevronDown : ChevronRight" :size="20" class="text-slate-400 group-hover:text-blue-500 transition-colors" />
            <h2 class="text-lg font-bold">会话历史</h2>
          </div>
          <div v-show="isDetailExpanded" class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6">
            <!-- 加载状态 -->
            <div v-if="detailLoading" class="py-12 text-center">
              <div class="inline-block w-6 h-6 border-2 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
              <p class="text-sm text-slate-400 mt-2">加载中...</p>
            </div>

            <!-- 数据表格 -->
            <div v-else class="overflow-x-auto">
              <table class="w-full">
                <thead>
                  <tr class="border-b border-slate-100">
                    <th class="px-4 py-3 text-left text-sm font-medium text-slate-500">时间</th>
                    <th class="px-4 py-3 text-left text-sm font-medium text-slate-500">标题</th>
                    <th class="px-4 py-3 text-left text-sm font-medium text-slate-500">智能体</th>
                    <th class="px-4 py-3 text-left text-sm font-medium text-slate-500">模型</th>
                    <th class="px-4 py-3 text-right text-sm font-medium text-slate-500">消耗 (Tokens)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(row, index) in detailData"
                    :key="index"
                    class="border-b border-slate-50 hover:bg-slate-50/50 transition-colors cursor-pointer"
                    @click="handleDetailRowClick(row)"
                  >
                    <td class="px-4 py-3 text-sm text-slate-600">{{ row.date }}</td>
                    <td class="px-4 py-3 text-sm text-slate-700">{{ row.title || '-' }}</td>
                    <td class="px-4 py-3">
                      <div class="flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                        <span class="text-sm text-slate-700">{{ row.agent_name || '会话' }}</span>
                      </div>
                    </td>
                    <td class="px-4 py-3">
                      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-50 text-indigo-700">
                        {{ row.model_name || '-' }}
                      </span>
                    </td>
                    <td class="px-4 py-3 text-sm font-medium text-slate-900 text-right">{{ formatNumber(row.tokens) }}</td>
                  </tr>
                  <tr v-if="detailData.length === 0">
                    <td colspan="5" class="px-4 py-12 text-center text-sm text-slate-400">
                      暂无数据
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- 分页 -->
            <div v-if="detailPagination.total > 0" class="flex items-center justify-between mt-4 pt-4 border-t border-slate-100">
              <div class="flex items-center gap-2 text-sm text-slate-500">
                <span>每页</span>
                <select
                  v-model="detailPagination.page_size"
                  class="px-2 py-1 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-50 focus:border-blue-400"
                  @change="handleDetailSizeChange(detailPagination.page_size)"
                >
                  <option :value="10">10</option>
                  <option :value="20">20</option>
                  <option :value="50">50</option>
                </select>
                <span>条 共 {{ detailPagination.total }} 条记录</span>
              </div>
              <div class="flex items-center gap-2">
                <button
                  :disabled="detailPagination.page_no <= 1"
                  class="px-3 py-1.5 text-sm font-medium rounded-lg transition-all"
                  :class="detailPagination.page_no <= 1 ? 'text-slate-300 cursor-not-allowed' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'"
                  @click="handleDetailPageChange(detailPagination.page_no - 1)"
                >
                  上一页
                </button>
                <span class="px-3 py-1.5 text-sm font-medium text-slate-900 bg-slate-100 rounded-lg">
                  {{ detailPagination.page_no }}
                </span>
                <button
                  :disabled="detailPagination.page_no >= Math.ceil(detailPagination.total / detailPagination.page_size)"
                  class="px-3 py-1.5 text-sm font-medium rounded-lg transition-all"
                  :class="detailPagination.page_no >= Math.ceil(detailPagination.total / detailPagination.page_size) ? 'text-slate-300 cursor-not-allowed' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'"
                  @click="handleDetailPageChange(detailPagination.page_no + 1)"
                >
                  下一页
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <CreateAgentModal
      v-if="isModalOpen"
      :initial-data="editingAgent"
      :user-status="userStatus"
      :is-admin-mode="false"
      @close="isModalOpen = false"
      @success="handleCreateSuccess"
    />

    <PublishAgentModal
      v-if="isPublishModalOpen"
      :agent="publishingAgent"
      :loading="publishingLoading"
      mode="publish"
      @close="closePublishModal"
      @confirm="handlePublishConfirm"
    />

    <!-- 智能创建弹窗 -->
    <div v-if="isSmartCreateModalOpen" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
          <h3 class="text-lg font-bold text-slate-800">智能创建</h3>
          <button @click="isSmartCreateModalOpen = false" class="text-slate-400 hover:text-slate-600 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
        <div class="p-6">
          <p class="text-sm text-slate-500 mb-3">请输入您想要智能体需求，例如："一个能帮我写周报的助手，能联网搜索"</p>
          <textarea
            v-model="smartCreatePrompt"
            rows="4"
            placeholder="描述您的需求..."
            class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-4 focus:ring-blue-50 focus:border-blue-500 outline-none transition-all resize-none"
          ></textarea>
        </div>
        <div class="px-6 py-4 bg-slate-50 flex justify-end gap-3">
          <button
            @click="isSmartCreateModalOpen = false"
            class="px-5 py-2 text-slate-600 font-medium hover:bg-slate-200 rounded-xl transition-colors"
          >
            取消
          </button>
          <button
            @click="handleSmartCreateConfirm"
            :disabled="!smartCreatePrompt.trim()"
            :class="['px-5 py-2 font-medium rounded-xl transition-all shadow-sm', smartCreatePrompt.trim() ? 'bg-blue-600 text-white hover:bg-blue-700 hover:shadow-md active:scale-95' : 'bg-blue-300 text-white/80 cursor-not-allowed']"
          >
            确认创建
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed, onMounted, ref} from 'vue'
import {
  Bot,
  ChevronDown,
  ChevronRight,
  Database,
  FileEdit,
  History,
  Loader2,
  MessageSquare,
  Plus,
  RefreshCw,
  Sparkles,
  TrendingUp,
  Upload
} from 'lucide-vue-next'
import AgentCard from '../components/agent/AgentCard.vue'
import CreateAgentModal from '../components/agent/CreateAgentModal.vue'
import PublishAgentModal from '../components/agent/PublishAgentModal.vue'
import {SubscriptionStatus} from '../types'
import {api} from '../services/api'
import type {AiAgentPublishPayload, AiAgentTable} from '../services/fastApi/module_ai/ai_agent'
import {useChatStore} from '../stores/chat'
import {useModelProviderStore} from '@/stores/modelProviders'
import {MAX_SESSION_TABS, useTagsViewStore} from '@/stores/tagsView'
import {useUserStore} from '@/stores/user'
import type {MODEL_META} from '@/types/model'
import dialog from '@/components/common/dialog'
import {message} from '@/components/common/message'
import {useRouter} from 'vue-router'
import type {TokenOverviewOut, UserTokenDetailItem} from '@/services/fastApi/module_ai/ai_chat_token_stats'
import AiChatTokenStatsAPI from '@/services/fastApi/module_ai/ai_chat_token_stats'

const userStore = useUserStore()

// 统计数据
const statsLoading = ref(false)
const overviewData = ref<TokenOverviewOut>({
  total_tokens: 0,
  total_chats: 0,
  active_agents: 0,
  active_users: 0
})

// 本周统计数据
const weekStats = ref({
  weekTokens: 0,
  weekChats: 0
})

// 详细消耗明细
const detailData = ref<UserTokenDetailItem[]>([])
const detailLoading = ref(false)
const detailPagination = ref({
  page_no: 1,
  page_size: 10,
  total: 0
})

const formatNumber = (num: number): string => {
  if (!num) return '0'
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toLocaleString()
}

// 格式化日期为 YYYY-MM-DD
const formatDate = (date: Date): string => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 获取本周起始日期
const getWeekRange = () => {
  const now = new Date()
  const dayOfWeek = now.getDay() || 7
  const start = new Date(now)
  start.setDate(now.getDate() - dayOfWeek + 1)
  start.setHours(0, 0, 0, 0)
  const end = new Date(now)
  end.setHours(23, 59, 59, 999)
  return { start: formatDate(start), end: formatDate(end) }
}

// 加载统计数据
const loadStats = async () => {
  statsLoading.value = true
  try {
    const { start, end } = getWeekRange()

    // 加载个人总览数据（全部时间，不传日期参数）
    const overviewRes = await AiChatTokenStatsAPI.getPersonalTokenOverview()
    if (overviewRes.data?.data) {
      overviewData.value = overviewRes.data.data
    }

    // 加载本周数据
    const weekRes = await AiChatTokenStatsAPI.getPersonalTokenOverview({
      start_date: start,
      end_date: end
    })
    if (weekRes.data?.data) {
      weekStats.value = {
        weekTokens: weekRes.data.data.total_tokens,
        weekChats: weekRes.data.data.total_chats
      }
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  } finally {
    statsLoading.value = false
  }
}

// 加载详细消耗明细
const loadDetailData = async () => {
  detailLoading.value = true
  try {
    const res = await AiChatTokenStatsAPI.getPersonalTokenDetail({
      page_no: detailPagination.value.page_no,
      page_size: detailPagination.value.page_size
    })
    if (res.data?.data) {
      detailData.value = res.data.data.items
      detailPagination.value.total = res.data.data.total
    }
  } catch (error) {
    console.error('加载消耗明细失败:', error)
  } finally {
    detailLoading.value = false
  }
}

// 处理分页变化
const handleDetailPageChange = (page: number) => {
  detailPagination.value.page_no = page
  loadDetailData()
}

// 处理每页条数变化
const handleDetailSizeChange = (size: number) => {
  detailPagination.value.page_size = size
  detailPagination.value.page_no = 1
  loadDetailData()
}

// 跳转到会话详情
const handleDetailRowClick = (row: UserTokenDetailItem) => {
  if (row.conversation_id) {
    router.push(`/chat/${row.conversation_id}`)
  }
}

const myAgents = ref<AiAgentTable[]>([])
const loading = ref(true)
const isModalOpen = ref(false)
const editingAgent = ref<AiAgentTable | null>(null)
const isCreatingSession = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)
const isEditExpanded = ref(true)
const isDetailExpanded = ref(true)
const isPublishModalOpen = ref(false)
const publishingAgent = ref<AiAgentTable | null>(null)
const publishingLoading = ref(false)

const chatStore = useChatStore('default')
const modelProviderStore = useModelProviderStore()
const tagsViewStore = useTagsViewStore()
const router = useRouter()
const currentUser = computed(() => userStore.userInfo)

const parseModel = (value?: string): MODEL_META | null => {
  if (!value) return null
  try {
    const parsed = JSON.parse(value)
    return typeof parsed === 'object' && parsed ? parsed : null
  } catch {
    return null
  }
}

const userStatus = computed(() => currentUser.value?.is_superuser ? SubscriptionStatus.PRO : SubscriptionStatus.FREE)

const filteredAgents = computed(() => {
  return myAgents.value
})

const fetchAgents = async () => {
  loading.value = true
  try {
    myAgents.value = await api.agent.getMyAgents()
  } catch (error) {
    console.error('Error fetching agents:', error)
    if (error instanceof Error && error.message.includes('Unauthorized')) {
      router.push('/login')
    }
  } finally {
    loading.value = false
  }
}

const handleAgentClick = async (agent: AiAgentTable) => {
  if (isCreatingSession.value) return
  isCreatingSession.value = true
  try {
    const normalizedAgentId = tagsViewStore.normalizeAgentId(agent.id)
    const guardResult = tagsViewStore.canOpenSessionTab(normalizedAgentId)
    if (!guardResult.allowed) {
      if (guardResult.reason === 'duplicate') {
        await router.push(guardResult.existingView.fullPath)
      } else {
        message.warning(`最多只能开启 ${MAX_SESSION_TABS} 个会话页签`)
      }
      return
    }
    const defaultModel = modelProviderStore.getDefaultModel
    const agentModel = parseModel(agent.model)
    const conversationSettings = {
      agentId: normalizedAgentId,
      providerId: agentModel?.providerId || defaultModel?.providerId,
      modelId: agentModel?.id || defaultModel?.modelId
    }
    const conversation = await chatStore.createConversation(agent.name || '', conversationSettings, { newConversation: true })
    tagsViewStore.registerConversationAgent(conversation.id, normalizedAgentId)
    // props.refreshSessions()
    await router.push(`/chat/${conversation.id}`)
  } catch (error: any) {
    console.error('启动会话失败:', error)
    return message.error(error?.message || '启动会话失败，请重试')
  } finally {
    isCreatingSession.value = false
  }
}

const isSmartCreateModalOpen = ref(false)
const smartCreatePrompt = ref('')

const handleSmartCreateClick = () => {
  isSmartCreateModalOpen.value = true
}

const handleSmartCreateConfirm = () => {
  if (!smartCreatePrompt.value.trim()) return
  message.info('功能开发中，即将上线')
  isSmartCreateModalOpen.value = false
  smartCreatePrompt.value = ''
}

const handleCreateClick = () => {
  editingAgent.value = null
  isModalOpen.value = true
}

const handleRefreshPage = () => {
  window.location.reload()
}

const handleEditClick = async (agent: AiAgentTable) => {
  editingAgent.value = agent
  isModalOpen.value = true
}

const handlePublishAgent = async (agent: AiAgentTable) => {
  if (!agent.id) return
  publishingLoading.value = true
  try {
    const detail = await api.agent.detailAgent(Number(agent.id))
    publishingAgent.value = detail || agent
    isPublishModalOpen.value = true
  } catch (error: any) {
    console.error('加载发布信息失败:', error)
    return message.error(error?.message || '加载发布信息失败，请重试')
  } finally {
    publishingLoading.value = false
  }
}

const closePublishModal = () => {
  isPublishModalOpen.value = false
  publishingAgent.value = null
}

const handlePublishConfirm = async (payload: AiAgentPublishPayload) => {
  if (!publishingAgent.value?.id) return
  publishingLoading.value = true
  try {
    await api.agent.publishAgent(Number(publishingAgent.value.id), payload)
    await fetchAgents()
    message.success('智能体发布成功！')
    closePublishModal()
  } catch (error: any) {
    console.error('Error publishing agent:', error)
    return message.error(error?.message || '发布失败，请重试')
  } finally {
    publishingLoading.value = false
  }
}

const handleDeleteAgent = async (agent: AiAgentTable) => {
  try {
    await dialog.confirm(
      agent.name ? `确定要删除智能体 "${agent.name}" 吗？` : '确定要删除该智能体吗？',
      '删除智能体',
      { type: 'danger', confirmText: '删除', cancelText: '取消' }
    )
    if (!agent.id) return
    await api.agent.deletePrivateAgent(agent.id.toString())
    myAgents.value = myAgents.value.filter(a => a.id !== agent.id)
    message.success('智能体删除成功！')
  } catch (error: any) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error('Error deleting agent:', error)
    return message.error(error?.message || '删除失败，请重试')
  }
}

const handleCreateSuccess = () => {
  fetchAgents()
  isModalOpen.value = false
  message.success('智能体创建成功！')
}

// 点击导入按钮，触发文件选择
const handleImportClick = () => {
  fileInput.value?.click()
}

// 定义导入的智能体配置类型
interface ImportedAgentConfig {
  name?: string
  description?: string
  type?: string
  prompt_template?: string
  model?: any
  config?: {
    mcp?: {
      activeSkills?: string[]
      enabledMcpToolIds?: number[]
      knowledge?: { name: string; dataset_id: string }[]
    }
    enableSearch?: boolean
    enableUpload?: boolean
    enableVoice?: boolean
  }
  cover?: {
    icon?: string
    color?: string
  }
}

const normalizeMcpToolIds = (value: unknown): number[] => {
  if (!Array.isArray(value)) return []
  return value
      .map(item => Number(item))
      .filter(item => Number.isInteger(item) && item > 0)
}

const handleFileSelect = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  try {
    loading.value = true

    // 读取JSON文件内容
    const fileContent = await file.text()
    const importedData: ImportedAgentConfig = JSON.parse(fileContent)

    // 验证必要字段
    if (!importedData.name || !importedData.prompt_template) {
      throw new Error('导入的文件缺少必要的字段（name 或 prompt_template）')
    }

    // 构建创建智能体的请求体
    const config = {
      mcp: {
        activeSkills: importedData.config?.mcp?.activeSkills || [],
        enabledMcpToolIds: normalizeMcpToolIds(importedData.config?.mcp?.enabledMcpToolIds),
        knowledge: importedData.config?.mcp?.knowledge || []
      },
      enableSearch: importedData.config?.enableSearch ?? false,
      enableUpload: importedData.config?.enableUpload ?? false,
      enableVoice: importedData.config?.enableVoice ?? false
    }

    const body = {
      name: importedData.name,
      description: importedData.description || '',
      type: importedData.type || 'internal',
      prompt_template: importedData.prompt_template,
      model: JSON.stringify(importedData.model || null),
      config: JSON.stringify(config),
      cover: JSON.stringify({
        icon: importedData.cover?.icon || 'Bot',
        color: importedData.cover?.color || '#3B82F6'
      })
    }

    // 调用API创建智能体
    await api.agent.createAgent(body)
    await fetchAgents()
    message.success('智能体导入成功！')
  } catch (error: any) {
    console.error('导入智能体失败:', error)
    return message.error(error.message || '导入智能体失败，请检查文件格式是否正确')
  } finally {
    loading.value = false
    if (fileInput.value) {
      fileInput.value.value = ''
    }
  }
}


onMounted(async () => {
  await Promise.all([
    fetchAgents(),
    loadStats(),
    loadDetailData()
  ])
})
</script>
