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
          <h1 class="text-2xl font-bold text-slate-900">智能体广场</h1>
          <p class="mt-1 text-sm text-slate-500">发现并使用各类智能体助手。</p>
        </div>
        <div class="relative w-full md:w-96 group">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-blue-500" :size="20" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="查找智能体..."
            class="w-full pl-10 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-4 focus:ring-blue-50 outline-none transition-all"
          />
        </div>
      </div>
    </div>
    <div class="px-8 pt-4 pb-2 flex-shrink-0">
      <div class="max-w-6xl mx-auto flex items-center justify-between gap-4">
        <div class="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
        <button
          v-for="cat in CATEGORIES"
          :key="cat.id"
          @click="selectedCategory = cat.id"
          :class="`px-4 py-2 rounded-full text-sm font-bold whitespace-nowrap transition-all ${selectedCategory === cat.id ? 'bg-blue-600 text-white shadow-md' : 'bg-white text-slate-600 hover:bg-slate-100'}`"
        >
          {{ cat.label }}
        </button>
        </div>
        <button
          @click="showFavoritesOnly = !showFavoritesOnly"
          :class="`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-bold whitespace-nowrap transition-all flex-shrink-0 ${showFavoritesOnly ? 'bg-amber-100 text-amber-700 ring-2 ring-amber-300' : 'bg-white text-slate-600 hover:bg-slate-100'}`"
        >
          <Heart :size="16" :class="showFavoritesOnly ? 'fill-amber-500 text-amber-500' : 'text-slate-400'" />
          收藏
        </button>
      </div>
    </div>
    <div v-if="loading" class="flex-1 flex items-center justify-center">
      <div class="text-center text-gray-500">正在加载智能体...</div>
    </div>
    <div v-else class="flex-1 overflow-y-auto p-8">
      <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <AgentCard
          v-for="agent in filteredAgents"
          :key="agent.id"
          :agent="agent"
          :onClick="() => handleAgentClick(agent)"
          :onClone="handleCloneClick"
          :onFavorite="handleFavoriteClick"
          :onMaintain="handleMaintainClick"
          :isFavorite="isFavoriteAgent(agent)"
          :isFavoriteLoading="isFavoriteUpdating(agent)"
        />
      </div>
    </div>
    <PublishAgentModal
      v-if="maintainDialogVisible && maintainingAgent"
      :agent="maintainingAgent"
      :loading="maintainUpdateLoading || maintainOfflineLoading"
      :show-offline="true"
      mode="manage"
      @close="closeMaintainDialog"
      @confirm="handleMaintainConfirm"
      @offline="handleOfflineClick"
    />
    <div
      v-if="forkDialogVisible && forkingAgent"
      class="absolute inset-0 z-40 bg-black/30 backdrop-blur-[1px] flex items-center justify-center p-4"
      @click.self="closeForkDialog"
    >
      <div class="w-full max-w-lg bg-white rounded-2xl shadow-xl border border-slate-100 p-6">
        <h3 class="text-lg font-bold text-slate-900">复制智能体</h3>
        <template v-if="forkDialogMode === 'sameCreator'">
          <p class="mt-2 text-sm text-slate-600">
            您是该智能体的创建者，可根据场景选择复制方式：
          </p>
          <div class="mt-4 space-y-3 rounded-xl bg-slate-50 p-4 text-sm text-slate-700">
            <p>
              <span class="font-semibold text-slate-900">全新副本：</span>
              与当前版本完全独立，后续修改和发布互不影响。
            </p>
            <p>
              <span class="font-semibold text-slate-900">可更新版本：</span>
              保留与当前公用版本的关联，后续发布可用于更新该智能体。
            </p>
          </div>
          <div class="mt-6 flex items-center justify-end gap-2">
            <button
              @click="closeForkDialog"
              :disabled="forkSubmitting !== 'none'"
              class="px-4 py-2 rounded-xl text-sm font-semibold text-slate-600 bg-slate-100 hover:bg-slate-200 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
            >
              取消
            </button>
            <button
              @click="copyIndependentVersion"
              :disabled="forkSubmitting !== 'none'"
              class="px-4 py-2 rounded-xl text-sm font-semibold text-slate-700 bg-slate-200 hover:bg-slate-300 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {{ forkSubmitting === 'independent' ? '复制中...' : '复制全新副本' }}
            </button>
            <button
              @click="copyUpdatableVersion"
              :disabled="forkSubmitting !== 'none'"
              class="px-4 py-2 rounded-xl text-sm font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {{ forkSubmitting === 'updatable' ? '复制中...' : '复制可更新版本' }}
            </button>
          </div>
        </template>
        <template v-else>
          <p class="mt-2 text-sm text-slate-600">
            该智能体由「{{ forkingAgent.created_by?.name || '原作者' }}」创建。
          </p>
          <p class="mt-2 text-sm text-slate-600">
            复制后会生成全新副本，您可以在“我的空间”独立修改和发布，不会影响原智能体。
          </p>
          <div class="mt-6 flex items-center justify-end gap-2">
            <button
              @click="closeForkDialog"
              :disabled="forkSubmitting !== 'none'"
              class="px-4 py-2 rounded-xl text-sm font-semibold text-slate-600 bg-slate-100 hover:bg-slate-200 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
            >
              取消
            </button>
            <button
              @click="copyIndependentVersion"
              :disabled="forkSubmitting !== 'none'"
              class="px-4 py-2 rounded-xl text-sm font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {{ forkSubmitting === 'independent' ? '复制中...' : '确认复制全新副本' }}
            </button>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed, onMounted, ref} from 'vue'
import {Heart, Loader2, Search} from 'lucide-vue-next'
import AgentCard from '../components/agent/AgentCard.vue'
import PublishAgentModal from '../components/agent/PublishAgentModal.vue'
import {api} from '../services/api'
import type {AiAgentManagePayload, AiAgentTable} from '../services/fastApi/module_ai/ai_agent'
import {useChatStore} from '../stores/chat'
import { useUserStore } from '@/stores/user'
import {useModelProviderStore} from '@/stores/modelProviders'
import {MAX_SESSION_TABS, useTagsViewStore} from '@/stores/tagsView'
import type {MODEL_META} from '@/types/model'
import {useRouter} from 'vue-router'
import DictAPI from '@/services/fastApi/module_system/dict'
import ExUserPreferenceAPI from '@/services/fastApi/module_ex/ex_user_preference'
import message from '@/components/common/message'
import dialog from '@/components/common/dialog'

const userStore = useUserStore()

const CATEGORIES = ref<{ id: string; label: string }[]>([
  { id: '', label: '全部' }
])

const squareAgents = ref<AiAgentTable[]>([])
const loading = ref(true)
const searchQuery = ref('')
const selectedCategory = ref('')
const showFavoritesOnly = ref(false)
const isCreatingSession = ref(false)
const favoriteAgentIds = ref<string[]>([])
const favoriteUpdatingIds = ref<string[]>([])
const maintainDialogVisible = ref(false)
const maintainingAgent = ref<AiAgentTable | null>(null)
const maintainUpdateLoading = ref(false)
const maintainOfflineLoading = ref(false)
const forkDialogVisible = ref(false)
const forkingAgent = ref<AiAgentTable | null>(null)
const forkDialogMode = ref<'sameCreator' | 'differentCreator'>('differentCreator')
const forkSubmitting = ref<'none' | 'independent' | 'updatable'>('none')
const FAVORITE_PREF_KEY = 'agent_square_favorite_ids'

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

const filteredAgents = computed(() => {
  return squareAgents.value.filter(agent => {
    const agentId = String(agent.id ?? '')
    const name = agent.name || ''
    const promptTemplate = agent.prompt_template || ''
    const matchesSearch = name.toLowerCase().includes(searchQuery.value.toLowerCase()) || promptTemplate.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory = selectedCategory.value === '' || agent.type === selectedCategory.value
    const matchesFavorite = !showFavoritesOnly.value || (Boolean(agentId) && favoriteAgentIds.value.includes(agentId))
    return matchesSearch && matchesCategory && matchesFavorite
  })
})

const normalizeFavoriteIds = (value?: string | null): string[] => {
  if (!value) return []
  try {
    const parsed = JSON.parse(value)
    if (Array.isArray(parsed)) {
      return Array.from(new Set(parsed.map(item => String(item)).filter(Boolean)))
    }
  } catch {
  }
  return value.split(',').map(item => item.trim()).filter(Boolean)
}

const loadFavoriteAgents = async () => {
  try {
    const response = await ExUserPreferenceAPI.getMyPreference(FAVORITE_PREF_KEY)
    const prefValue = response.data?.data?.pref_value
    favoriteAgentIds.value = normalizeFavoriteIds(prefValue)
  } catch (error) {
    console.error('加载收藏失败:', error)
    favoriteAgentIds.value = []
  }
}

const setFavoriteAgents = async (ids: string[]) => {
  await ExUserPreferenceAPI.setMyPreference(FAVORITE_PREF_KEY, {
    pref_value: JSON.stringify(ids)
  })
}

const isFavoriteAgent = (agent: AiAgentTable) => {
  const agentId = String(agent.id ?? '')
  return Boolean(agentId) && favoriteAgentIds.value.includes(agentId)
}

const isFavoriteUpdating = (agent: AiAgentTable) => {
  const agentId = String(agent.id ?? '')
  return Boolean(agentId) && favoriteUpdatingIds.value.includes(agentId)
}

const fetchAgents = async () => {
  loading.value = true
  try {
    squareAgents.value = await api.agent.getSquareAgents()
  } catch (error) {
    console.error('Error fetching square agents:', error)
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
  } catch (error) {
    console.error('启动会话失败:', error)
    alert('启动会话失败，请重试')
  } finally {
    isCreatingSession.value = false
  }
}

const normalizeUserId = (value: unknown): number => {
  const parsed = Number(value)
  return Number.isFinite(parsed) ? parsed : 0
}

const isSameCreator = (agent: AiAgentTable) => {
  const currentUserId = normalizeUserId(currentUser.value?.id)
  if (!currentUserId) return false
  const creatorId = normalizeUserId(agent.created_id ?? agent.created_by?.id)
  return creatorId > 0 && creatorId === currentUserId
}

const openForkDialog = (agent: AiAgentTable) => {
  forkingAgent.value = agent
  forkDialogMode.value = isSameCreator(agent) ? 'sameCreator' : 'differentCreator'
  forkDialogVisible.value = true
}

const closeForkDialog = () => {
  if (forkSubmitting.value !== 'none') return
  forkDialogVisible.value = false
  forkingAgent.value = null
}

const buildForkName = (name?: string) => {
  const baseName = (name || '未命名智能体').trim()
  return `${baseName}_副本`
}

const copyIndependentVersion = async () => {
  const agent = forkingAgent.value
  if (!agent) return
  forkSubmitting.value = 'independent'
  try {
    await api.agent.createAgent({
      name: buildForkName(agent.name),
      description: agent.description || '',
      type: agent.type || '',
      config: agent.config || '',
      prompt_template: agent.prompt_template || '',
      model: agent.model || '',
      cover: agent.cover || ''
    })
    message.success('全新副本创建成功，可前往“我的空间”继续编辑。')
    forkDialogVisible.value = false
    forkingAgent.value = null
  } catch (error) {
    console.error('创建全新副本失败:', error)
    message.error('复制全新副本失败，请重试')
  } finally {
    forkSubmitting.value = 'none'
  }
}

const copyUpdatableVersion = async () => {
  const agent = forkingAgent.value
  if (!agent?.id) return
  forkSubmitting.value = 'updatable'
  try {
    await api.agent.forkAgent(Number(agent.id))
    message.success('可更新版本创建成功，后续发布可用于更新该智能体。')
    forkDialogVisible.value = false
    forkingAgent.value = null
  } catch (error) {
    console.error('创建可更新版本失败:', error)
    message.error('复制可更新版本失败，请重试')
  } finally {
    forkSubmitting.value = 'none'
  }
}

const handleCloneClick = async (agent: AiAgentTable) => {
  if (!agent.id) return
  openForkDialog(agent)
}

const handleMaintainClick = async (agent: AiAgentTable) => {
  if (!agent.id) return
  maintainUpdateLoading.value = true
  try {
    const detail = await api.agent.detailAgent(Number(agent.id))
    maintainingAgent.value = detail || agent
    maintainDialogVisible.value = true
  } catch (error: any) {
    console.error('加载智能体详情失败:', error)
    return message.error(error?.message || '加载智能体详情失败，请重试')
  } finally {
    maintainUpdateLoading.value = false
  }
}

const closeMaintainDialog = () => {
  if (maintainUpdateLoading.value || maintainOfflineLoading.value) return
  maintainDialogVisible.value = false
  maintainingAgent.value = null
}

const handleMaintainConfirm = async (payload: AiAgentManagePayload) => {
  const agent = maintainingAgent.value
  if (!agent?.id) return
  maintainUpdateLoading.value = true
  try {
    await api.agent.manageAgent(Number(agent.id), payload)
    message.success('广场智能体更新成功')
    closeMaintainDialog()
    await fetchAgents()
  } catch (error: any) {
    console.error('更新智能体失败:', error)
    return message.error(error?.message || '更新失败，请重试')
  } finally {
    maintainUpdateLoading.value = false
  }
}

const handleOfflineClick = async () => {
  const agent = maintainingAgent.value
  if (!agent?.id) return
  maintainOfflineLoading.value = true
  try {
    await dialog.confirm(
        agent.name ? `确定要下线智能体 "${agent.name}" 吗？` : '确定要下线该智能体吗？',
        '下线智能体',
        {type: 'danger', confirmText: '下线', cancelText: '取消'}
    )
    await api.agent.offlineAgent(Number(agent.id))
    message.success('下线成功')
    closeMaintainDialog()
    await fetchAgents()
  } catch (error: any) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error('下线失败:', error)
    message.error(error?.message || '下线失败，请重试')
  } finally {
    maintainOfflineLoading.value = false
  }
}

const handleFavoriteClick = async (agent: AiAgentTable) => {
  const agentId = String(agent.id ?? '')
  if (!agentId || favoriteUpdatingIds.value.includes(agentId)) return
  const isRemoving = favoriteAgentIds.value.includes(agentId)
  const previousIds = [...favoriteAgentIds.value]
  const nextIds = isRemoving
    ? favoriteAgentIds.value.filter(id => id !== agentId)
    : Array.from(new Set([...favoriteAgentIds.value, agentId]))
  favoriteAgentIds.value = nextIds
  favoriteUpdatingIds.value = [...favoriteUpdatingIds.value, agentId]
  try {
    await setFavoriteAgents(nextIds)
  } catch (error) {
    favoriteAgentIds.value = previousIds
    console.error('更新收藏失败:', error)
    alert('收藏操作失败，请重试')
  } finally {
    favoriteUpdatingIds.value = favoriteUpdatingIds.value.filter(id => id !== agentId)
  }
}

const loadAgentCategories = async () => {
  try {
    const response = await DictAPI.getInitDict('ai_agent_type')
    const dictData = response.data?.data
    if (Array.isArray(dictData)) {
      const mapped = dictData
        .filter((item: any) => item.status === '0')
        .sort((a: any, b: any) => (a.dict_sort || 0) - (b.dict_sort || 0))
        .map((item: any) => ({
          id: String(item.dict_value),
          label: String(item.dict_label)
        }))
      CATEGORIES.value = [{ id: '', label: '全部' }, ...mapped]
    }
    if (CATEGORIES.value.length === 1) {
      CATEGORIES.value = [
        { id: '', label: '全部' }
      ]
    }
  } catch (error) {
    console.error('加载智能体类型失败:', error)
    CATEGORIES.value = [
      { id: '', label: '全部' }
    ]
  }
}

onMounted(async () => {
  await Promise.all([fetchAgents(), loadAgentCategories(), loadFavoriteAgents()])
})
</script>
