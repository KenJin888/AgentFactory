<template>
  <div
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
    <div
        class="bg-white rounded-3xl w-full max-w-2xl shadow-2xl overflow-hidden border border-slate-100 flex flex-col h-[90vh]">
      <!-- Header -->
      <div
          :class="`px-8 py-6 border-b border-gray-100 flex justify-between items-center ${isAdminMode ? 'bg-slate-900 text-white' : 'bg-gray-50/50'}`">
        <div>
          <h2 :class="`text-xl font-bold flex items-center gap-2 ${isAdminMode ? 'text-white' : 'text-slate-900'}`">
            <ShieldCheck v-if="isAdminMode" :size="20" class="text-blue-400"/>
            <Sparkles v-else :size="20" class="text-blue-500"/>
            {{ isEditMode ? '编辑智能体' : '创建新智能体' }}
          </h2>
          <p class="text-sm opacity-70 mt-1">配置角色、工具与技能</p>
        </div>
        <button class="p-2 rounded-full hover:bg-black/10 transition-colors" type="button" @click="$emit('close')">
          <X :size="20"/>
        </button>
      </div>

      <!-- Tabs -->
      <div class="flex border-b border-gray-100 px-8">
        <button
            v-for="tab in tabs"
            :key="tab.id"
            :class="`flex items-center gap-2 px-4 py-4 text-sm font-bold border-b-2 transition-colors ${activeTab === tab.id ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`"
            type="button"
            @click="activeTab = tab.id as any"
        >
          <component :is="tab.icon" :size="14"/>
          {{ tab.label }}
          <span v-if="tab.id === 'skills' || tab.id === 'mcp' || tab.id === 'knowledge'" class="text-xs font-semibold">
                ({{
              tab.id === 'skills' ? selectedSkills.length : tab.id === 'mcp' ? selectedExternalTools.length + selectedInternalTools.length : selectedKnowledge.length
            }})
              </span>
        </button>
      </div>

      <!-- Form -->
      <div class="flex-1 overflow-y-auto p-8 custom-scrollbar">
        <form id="agent-form" class="space-y-6" @submit.prevent="handleSubmit">
          <!-- 基础设定 -->
          <div v-if="activeTab === 'basic'" class="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
            <div>
              <label class="block text-sm font-bold text-slate-700 mb-2">名称</label>
              <input
                  v-model="name"
                  class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-500"
                  placeholder="例如：销售陪练"
                  required
              />
            </div>
            <div>
              <label class="block text-sm font-bold text-slate-700 mb-2">描述</label>
              <input
                  v-model="description"
                  class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-500"
                  placeholder="描述智能体的功能和用途"
              />
            </div>
            <div>
              <label class="block text-sm font-bold text-slate-700 mb-2">开场白</label>
              <input
                  v-model="welcome"
                  class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-500"
                  placeholder="用户进入对话时展示的欢迎语"
              />
            </div>
            <div>
              <label class="block text-sm font-bold text-slate-700 mb-2">系统提示词 (角色设定)</label>
              <textarea
                  v-model="systemPrompt"
                  class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-500 resize-none"
                  placeholder="你是一个..."
                  required
                  rows="5"
              />
            </div>

            <!-- 动态渲染模型列表 -->
            <div>
              <label class="block text-sm font-bold text-slate-700 mb-2">选择模型基座</label>
              <ModelSelector v-model="selectedModel" mode="dropdown" placement="top"/>
            </div>
            <div>
              <label class="block text-sm font-bold text-slate-700 mb-2">封面样式</label>
              <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-4">
                <div class="flex items-center gap-3">
                  <AgentCoverIcon
                      :cover="{ icon: selectedCoverIcon, color: selectedCoverColor }"
                      :size="22"
                      container-class="w-12 h-12 rounded-xl flex items-center justify-center text-white shadow-sm"
                  />
                  <span class="text-xs text-slate-500">用于智能体卡片展示</span>
                </div>
                <div>
                  <div class="text-xs font-semibold text-slate-600 mb-2">图标</div>
                  <div class="grid grid-cols-4 sm:grid-cols-8 gap-2">
                    <button
                        v-for="icon in COVER_ICON_OPTIONS"
                        :key="icon.id"
                        :class="`h-9 rounded-lg border flex items-center justify-center transition-colors ${selectedCoverIcon === icon.id ? 'border-blue-500 text-blue-600 bg-blue-50' : 'border-slate-200 text-slate-500 bg-white hover:border-slate-300'}`"
                        :title="icon.label"
                        type="button"
                        @click="selectedCoverIcon = icon.id"
                    >
                      <component :is="icon.component" :size="16"/>
                    </button>
                  </div>
                </div>
                <div>
                  <div class="text-xs font-semibold text-slate-600 mb-2">颜色</div>
                  <div class="flex flex-wrap gap-2">
                    <button
                        v-for="color in COVER_COLOR_OPTIONS"
                        :key="color"
                        :style="{ backgroundColor: color }"
                        class="h-8 w-8 rounded-lg border border-slate-200 flex items-center justify-center text-white"
                        type="button"
                        @click="selectedCoverColor = color"
                    >
                      <Check v-if="selectedCoverColor === color" :size="14"/>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 能力扩展 -->
          <div v-if="activeTab === 'funcs'" class="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <SkillToggle
                  :active="enableUpload"
                  :icon="FileText"
                  desc="支持 PDF, Word, Txt, Excel, PowerPoint 上传分析"
                  label="文件读取"
                  @change="enableUpload = $event"
              />
              <SkillToggle
                  :active="enableVoice"
                  :icon="Mic"
                  desc="支持语音转文字输入"
                  label="语音输入"
                  @change="enableVoice = $event"
              />
              <SkillToggle
                  :active="enableSearch"
                  :icon="Globe"
                  desc="允许访问互联网获取最新信息"
                  label="联网搜索"
                  @change="enableSearch = $event"
              />
            </div>
          </div>
          <div v-if="activeTab === 'skills'" class="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
            <div v-if="skillsLoading" class="text-sm text-slate-500">技能列表加载中...</div>
            <div v-else-if="skillsLoadError" class="p-4 bg-red-50 text-red-600 rounded-xl text-sm">{{
                skillsLoadError
              }}
            </div>
            <div v-else-if="skillList.length === 0" class="p-4 bg-slate-50 text-slate-500 rounded-xl text-sm">
              暂无可选技能
            </div>
            <div v-else
                 class="max-h-[calc(90vh-22rem)] min-h-40 overflow-y-auto border border-slate-200 rounded-xl divide-y divide-slate-100">
              <label
                  v-for="skill in skillList"
                  :key="skill.name"
                  class="flex items-start gap-3 px-4 py-3 hover:bg-slate-50 cursor-pointer"
              >
                <input
                    v-model="selectedSkills"
                    :disabled="!skill.name"
                    :value="skill.name"
                    class="mt-0.5 h-4 w-4 flex-none rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                    type="checkbox"
                />
                <div class="min-w-0">
                  <div class="text-sm font-semibold text-slate-800 truncate">{{ skill.name || '-' }}</div>
                  <div class="text-xs text-slate-500 whitespace-pre-wrap break-words">{{
                      skill.description || '未设置描述'
                    }}
                  </div>
                </div>
              </label>
            </div>
          </div>
          <div v-if="activeTab === 'mcp'" class="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
            <!-- 内置工具下拉结构 -->
            <div class="border border-slate-200 rounded-xl overflow-hidden">
              <button
                  class="w-full flex items-center justify-between px-4 py-3 bg-slate-50 hover:bg-slate-100 transition-colors"
                  type="button"
                  @click="isInternalToolsExpanded = !isInternalToolsExpanded"
              >
                <div class="flex items-center gap-2">
                  <span class="text-sm font-semibold text-slate-800">内置工具</span>
                  <span v-if="selectedInternalTools.length > 0"
                        class="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">
                        {{ selectedInternalTools.length }}
                      </span>
                </div>
                <ChevronDown
                    :class="{ 'rotate-180': isInternalToolsExpanded }"
                    :size="18"
                    class="text-slate-500 transition-transform duration-200"
                />
              </button>
              <div v-show="isInternalToolsExpanded" class="border-t border-slate-200">
                <div v-if="internalToolsLoading" class="p-4 text-sm text-slate-500">内置工具列表加载中...</div>
                <div v-else-if="internalToolsLoadError" class="p-4 bg-red-50 text-red-600 text-sm">
                  {{ internalToolsLoadError }}
                </div>
                <div v-else-if="internalToolsList.length === 0" class="p-4 bg-slate-50 text-slate-500 text-sm">
                  暂无内置工具
                </div>
                <div v-else class="max-h-60 overflow-y-auto divide-y divide-slate-100">
                  <label
                      v-for="tool in internalToolsList"
                      :key="tool.name"
                      class="flex items-start gap-3 px-4 py-3 hover:bg-slate-50 cursor-pointer"
                  >
                    <input
                        v-model="selectedInternalTools"
                        :value="tool.name"
                        class="mt-0.5 h-4 w-4 flex-none rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                        type="checkbox"
                    />
                    <div class="min-w-0">
                      <div class="text-sm font-semibold text-slate-800 truncate">{{ tool.name || '-' }}</div>
                      <div class="text-xs text-slate-500 whitespace-pre-wrap break-words">{{
                          tool.description || '未设置描述'
                        }}
                      </div>
                    </div>
                  </label>
                </div>
              </div>
            </div>

            <!-- MCP工具下拉结构 -->
            <div class="border border-slate-200 rounded-xl overflow-hidden">
              <button
                  class="w-full flex items-center justify-between px-4 py-3 bg-slate-50 hover:bg-slate-100 transition-colors"
                  type="button"
                  @click="isMcpToolsExpanded = !isMcpToolsExpanded"
              >
                <div class="flex items-center gap-2">
                  <span class="text-sm font-semibold text-slate-800">MCP 工具</span>
                  <span v-if="selectedExternalTools.length > 0"
                        class="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">
                        {{ selectedExternalTools.length }}
                      </span>
                </div>
                <ChevronDown
                    :class="{ 'rotate-180': isMcpToolsExpanded }"
                    :size="18"
                    class="text-slate-500 transition-transform duration-200"
                />
              </button>
              <div v-show="isMcpToolsExpanded" class="border-t border-slate-200">
                <div v-if="mcpLoading" class="p-4 text-sm text-slate-500">MCP 列表加载中...</div>
                <div v-else-if="mcpLoadError" class="p-4 bg-red-50 text-red-600 text-sm">{{ mcpLoadError }}</div>
                <div v-else-if="visibleMcpList.length === 0" class="p-4 bg-slate-50 text-slate-500 text-sm">暂无可选
                  MCP
                </div>
                <div v-else class="max-h-60 overflow-y-auto divide-y divide-slate-100">
                  <label
                      v-for="mcp in visibleMcpList"
                      :key="mcp.id || mcp.name"
                      class="flex items-center gap-3 px-4 py-3 hover:bg-slate-50 cursor-pointer"
                  >
                    <input
                        v-model="selectedExternalTools"
                        :disabled="!mcp.name"
                        :value="mcp.name"
                        class="h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                        type="checkbox"
                    />
                    <div class="min-w-0">
                      <div class="text-sm font-semibold text-slate-800 truncate">{{ mcp.name || '-' }}</div>
                      <div class="text-xs text-slate-500 truncate">{{ mcp.abstract || mcp.type || '未设置描述' }}</div>
                    </div>
                  </label>
                </div>
              </div>
            </div>
          </div>
          <div v-if="activeTab === 'knowledge'" class="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
            <div class="p-3 rounded-xl bg-blue-50 text-blue-700 text-sm border border-blue-100">
              选择知识库后，系统会在对话时自动加载知识库检索工具。
            </div>
            <div v-if="knowledgeLoading" class="text-sm text-slate-500">知识库列表加载中...</div>
            <div v-else-if="knowledgeLoadError" class="p-4 bg-red-50 text-red-600 rounded-xl text-sm">
              {{ knowledgeLoadError }}
            </div>
            <div v-else-if="knowledgeList.length === 0" class="p-4 bg-slate-50 text-slate-500 rounded-xl text-sm">
              暂无可选知识库
            </div>
            <div v-else
                 class="max-h-[calc(90vh-22rem)] min-h-40 overflow-y-auto border border-slate-200 rounded-xl divide-y divide-slate-100">
              <label
                  v-for="dataset in knowledgeList"
                  :key="dataset.dataset_id"
                  class="flex items-start gap-3 px-4 py-3 hover:bg-slate-50 cursor-pointer"
              >
                <input
                    :checked="selectedKnowledge.some(k => k.dataset_id === dataset.dataset_id)"
                    class="mt-0.5 h-4 w-4 flex-none rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                    type="checkbox"
                    @change="(e) => toggleKnowledge(dataset, e.target as HTMLInputElement)"
                />
                <div class="min-w-0">
                  <div class="text-sm font-semibold text-slate-800 truncate">{{ dataset.name || '-' }}</div>
                  <div class="text-xs text-slate-500 whitespace-pre-wrap break-words">{{
                      dataset.description || '未设置描述'
                    }}
                  </div>
                </div>
              </label>
            </div>
          </div>
          <div v-if="error" class="p-4 bg-red-50 text-red-600 rounded-xl text-sm flex items-center gap-2">
            <AlertCircle :size="16"/>
            {{ error }}
          </div>
        </form>
      </div>

      <!-- Footer -->
      <div class="px-8 py-6 border-t border-gray-100 bg-gray-50/50 flex  gap-3">
        <button
            className="text-slate-500 hover:text-blue-600 font-bold text-sm flex items-center gap-2 px-3 py-2 hover:bg-white rounded-lg transition-all"
            title="导出配置"
            type="button"
            @click="handleExport"
        >
          <Download :size="16"/>
          <span className="hidden sm:inline">导出配置</span>
        </button>
        <div class="flex-1"></div>
        <button class="px-6 py-3 text-slate-600 font-medium hover:bg-slate-100 rounded-xl" type="button"
                @click="$emit('close')">取消
        </button>
        <button
            :class="`px-8 py-3 text-white font-bold rounded-xl shadow-lg flex items-center gap-2 ${isAdminMode ? 'bg-blue-600' : 'bg-slate-900'}`"
            :disabled="loading"
            form="agent-form"
            type="submit"
        >
          <Loader2 v-if="loading" :size="18" class="animate-spin"/>
          {{ isEditMode ? '保存修改' : '立即创建' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed, onMounted, ref, watch} from 'vue'
import {
  AlertCircle,
  Box,
  Check,
  ChevronDown,
  Database,
  Download,
  FileText,
  Globe,
  Loader2,
  Mic,
  ShieldCheck,
  Sparkles,
  Wrench,
  X
} from 'lucide-vue-next'
import type {SubscriptionStatus} from '../../types'
import SkillToggle from './SkillToggle.vue'
import ModelSelector from '@/components/common/ModelSelector.vue'
import AgentCoverIcon from '@/components/common/AgentCoverIcon.vue'
import {useModelProviderStore} from '@/stores/modelProviders'
import type {MODEL_META} from '@/types/model'
import {storeToRefs} from 'pinia'
import {api} from '@/services/api'
import AiAgentAPI, {
  type AiAgentConfig,
  type AiAgentForm,
  type AiAgentKnowledgeDataset,
  type AiAgentTable,
  type KnowledgeItem
} from '@/services/fastApi/module_ai/ai_agent'
import AiMcpAPI, {type AiMcpTable, isBuiltinRagflowMcp} from '@/services/fastApi/module_ai/ai_mcp'
import AISkillsAPI from '@/services/fastApi/module_ai/ai_skills'
import AiToolsAPI, {type InternalToolItem} from '@/services/fastApi/module_ai/ai_tools'
import {
  AGENT_COVER_COLOR_OPTIONS,
  AGENT_COVER_ICON_OPTIONS,
  DEFAULT_AGENT_COVER_COLOR,
  DEFAULT_AGENT_COVER_ICON,
  normalizeAgentCover,
  stringifyAgentCover
} from '@/components/common/agentCover'
import {message} from '@/components/common/message'

// 定义组件属性
const props = defineProps<{
  initialData?: AiAgentTable | null
  userStatus: SubscriptionStatus
  isAdminMode?: boolean
}>()

// 定义组件事件
const emit = defineEmits<{
  'close': []
  'success': [agent: AiAgentTable, isEdit: boolean]
}>()


// 标签页定义
const tabs = [
  {id: 'basic', label: '基础设定', icon: Sparkles},
  {id: 'knowledge', label: '知识库', icon: Database},
  {id: 'skills', label: '技能', icon: Wrench},
  {id: 'mcp', label: '工具', icon: Box},
  // { id: 'funcs', label: '输入输出', icon: Zap },
]

// 响应式数据
const modelProviderStore = useModelProviderStore()
const {providers} = storeToRefs(modelProviderStore)
const availableModels = computed<MODEL_META[]>(() =>
    providers.value
        .filter((provider) => provider.isEnabled)
        .flatMap((provider) =>
            provider.config.models
                .filter((model) => model.enabled !== false)
                .map((model) => model)
        )
)
const parseConfig = (value?: string): AiAgentConfig => {
  if (!value) return {}
  try {
    const parsed = JSON.parse(value)
    return typeof parsed === 'object' && parsed ? parsed : {}
  } catch {
    return {}
  }
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
const COVER_ICON_OPTIONS = AGENT_COVER_ICON_OPTIONS
const COVER_COLOR_OPTIONS = AGENT_COVER_COLOR_OPTIONS
const initialConfig = parseConfig(props.initialData?.config)
const initialModel = parseModel(props.initialData?.model || '')
const initialCover = normalizeAgentCover(props.initialData?.cover || '')
const normalizeMcpToolIds = (value: unknown): number[] => {
  if (!Array.isArray(value)) return []
  return Array.from(new Set(
      value
          .map(item => Number(item))
          .filter((id): id is number => Number.isInteger(id) && id > 0)
  ))
}
const normalizeExternalTools = (value: unknown): string[] => {
  if (!Array.isArray(value)) return []
  return Array.from(new Set(
      value
          .filter((item): item is string => typeof item === 'string' && item.trim().length > 0)
          .map(item => item.trim())
  ))
}
const legacyInitialMcpToolIds = normalizeMcpToolIds(initialConfig?.mcp?.enabledMcpToolIds)
const initialExternalTools = normalizeExternalTools(initialConfig?.mcp?.externalTools)
const initialSkills = initialConfig?.mcp?.activeSkills ?? []
const initialKnowledge = initialConfig?.mcp?.knowledge ?? []
const initialInternalTools = initialConfig?.mcp?.internalTools ?? []
const name = ref(props.initialData?.name || '')
const description = ref(props.initialData?.description || '')
const welcome = ref(initialConfig.welcome || '')
const systemPrompt = ref(props.initialData?.prompt_template || '')
const selectedModel = ref(initialModel || null)
const selectedCategory = ref(props.initialData?.type || 'internal')
const selectedCoverIcon = ref(initialCover.icon || DEFAULT_AGENT_COVER_ICON)
const selectedCoverColor = ref(initialCover.color || DEFAULT_AGENT_COVER_COLOR)
const skillList = ref<{ name: string; description: string }[]>([])
const selectedSkills = ref<string[]>(Array.isArray(initialSkills) ? initialSkills : [])
const skillsLoading = ref(false)
const skillsLoadError = ref('')
const mcpList = ref<AiMcpTable[]>([])
const selectedExternalTools = ref<string[]>(initialExternalTools)
const mcpLoading = ref(false)
const mcpLoadError = ref('')
const visibleMcpList = computed(() => mcpList.value.filter(mcp => !isBuiltinRagflowMcp(mcp)))
const pendingLegacyMcpToolIds = ref<number[]>(legacyInitialMcpToolIds)
const enableUpload = ref(initialConfig.enableUpload ?? false)
const enableVoice = ref(initialConfig.enableVoice ?? false)
const enableSearch = ref(initialConfig.enableSearch ?? false)
const loading = ref(false)
const error = ref('')
const activeTab = ref<'basic' | 'funcs' | 'skills' | 'mcp' | 'knowledge'>('basic')

// 知识库相关
const knowledgeList = ref<AiAgentKnowledgeDataset[]>([])
const selectedKnowledge = ref<KnowledgeItem[]>(Array.isArray(initialKnowledge) ? initialKnowledge : [])
const knowledgeLoading = ref(false)
const knowledgeLoadError = ref('')

// 内置工具相关
const internalToolsList = ref<InternalToolItem[]>([])
const selectedInternalTools = ref<string[]>(Array.isArray(initialInternalTools) ? initialInternalTools : [])
const internalToolsLoading = ref(false)
const internalToolsLoadError = ref('')
const isInternalToolsExpanded = ref(false)
const isMcpToolsExpanded = ref(true)

// 计算属性
const isEditMode = computed(() => !!props.initialData)
const isAdminMode = false
const hasConfiguredModel = computed(() => availableModels.value.length > 0 && !!selectedModel.value)

onMounted(() => {
  if (!hasConfiguredModel.value) {
    message.warning('请先配置并启用至少一个模型')
    emit('close')
  }
})

watch(
    availableModels,
    (models) => {
      if (!props.initialData?.model && models.length > 0 && !selectedModel.value) {
        selectedModel.value = models[0]
      }
      if (props.initialData?.model && !selectedModel.value) {
        selectedModel.value = parseModel(props.initialData?.model || '')
      }
    },
    {immediate: true}
)

const loadMcpList = async () => {
  mcpLoading.value = true
  mcpLoadError.value = ''
  try {
    const response = await AiMcpAPI.listAiMcp({
      page_no: 1,
      page_size: 200,
      status: '0'
    })
    mcpList.value = response.data?.data?.items || []
    const visibleMcpNames = new Set(
        visibleMcpList.value
            .map(item => (item.name || '').trim())
            .filter((name): name is string => name.length > 0)
    )
    // 兼容旧配置：首次加载时把 enabledMcpToolIds 映射为 externalTools(name)
    if (selectedExternalTools.value.length === 0 && pendingLegacyMcpToolIds.value.length > 0) {
      const idSet = new Set(pendingLegacyMcpToolIds.value)
      selectedExternalTools.value = visibleMcpList.value
          .filter(item => idSet.has(Number(item.id)))
          .map(item => item.name || '')
          .filter((name): name is string => name.trim().length > 0)
          .map(name => name.trim())
      pendingLegacyMcpToolIds.value = []
    }
    selectedExternalTools.value = selectedExternalTools.value.filter(name => visibleMcpNames.has(name))
  } catch (err: any) {
    mcpLoadError.value = err?.message || 'MCP 列表加载失败'
  } finally {
    mcpLoading.value = false
  }
}

const loadSkillsList = async () => {
  skillsLoading.value = true
  skillsLoadError.value = ''
  try {
    const response = await AISkillsAPI.listSkills()
    skillList.value = response.data?.data?.skills || []
  } catch (err: any) {
    skillsLoadError.value = err?.message || '技能列表加载失败'
  } finally {
    skillsLoading.value = false
  }
}

loadMcpList()
loadSkillsList()

// 加载内置工具列表
const loadInternalToolsList = async () => {
  internalToolsLoading.value = true
  internalToolsLoadError.value = ''
  try {
    const response = await AiToolsAPI.listInternalTools()
    internalToolsList.value = response.data?.data?.tools || []
    // 过滤掉已选择但已不存在的工具
    const availableToolNames = new Set(internalToolsList.value.map(t => t.name))
    selectedInternalTools.value = selectedInternalTools.value.filter(name => availableToolNames.has(name))
  } catch (err: any) {
    internalToolsLoadError.value = err?.message || '内置工具列表加载失败'
  } finally {
    internalToolsLoading.value = false
  }
}

loadInternalToolsList()

// 加载知识库列表
const loadKnowledgeList = async () => {
  knowledgeLoading.value = true
  knowledgeLoadError.value = ''
  try {
    const response = await AiAgentAPI.listAvailableKnowledgeDatasets({
      page: 1,
      page_size: 200
    })
    knowledgeList.value = response.data?.data || []
  } catch (err: any) {
    knowledgeLoadError.value = err?.message || '知识库列表加载失败'
  } finally {
    knowledgeLoading.value = false
  }
}

loadKnowledgeList()

// 切换知识库选择
const toggleKnowledge = (dataset: AiAgentKnowledgeDataset, target: HTMLInputElement) => {
  const isChecked = target.checked
  if (isChecked) {
    // 添加选择
    if (!selectedKnowledge.value.some(k => k.dataset_id === dataset.dataset_id)) {
      selectedKnowledge.value.push({
        name: dataset.name || '',
        dataset_id: dataset.dataset_id
      })
    }
  } else {
    // 移除选择
    selectedKnowledge.value = selectedKnowledge.value.filter(k => k.dataset_id !== dataset.dataset_id)
  }
}


// 导出配置 - 将当前智能体配置导出为JSON文件
const handleExport = () => {
  try {
    const config: AiAgentConfig = {
      mcp: {
        activeSkills: selectedSkills.value,
        externalTools: selectedExternalTools.value,
        internalTools: selectedInternalTools.value,
        knowledge: selectedKnowledge.value
      },
      welcome: welcome.value,
      enableSearch: enableSearch.value,
      enableUpload: enableUpload.value,
      enableVoice: enableVoice.value
    }

    const exportData = {
      name: name.value,
      description: description.value,
      type: selectedCategory.value,
      prompt_template: systemPrompt.value,
      model: selectedModel.value,
      config: config,
      cover: {
        icon: selectedCoverIcon.value,
        color: selectedCoverColor.value
      }
    }

    const blob = new Blob([JSON.stringify(exportData, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${name.value || 'agent'}_config.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  } catch (err: any) {
    error.value = err.message || "导出失败"
  }
}

// 提交表单
const handleSubmit = async () => {
  error.value = ''
  loading.value = true

  try {
    const config: AiAgentConfig = {
      mcp: {
        activeSkills: selectedSkills.value,
        externalTools: selectedExternalTools.value,
        internalTools: selectedInternalTools.value,
        knowledge: selectedKnowledge.value
      },
      welcome: welcome.value,
      enableSearch: enableSearch.value,
      enableUpload: enableUpload.value,
      enableVoice: enableVoice.value
    }
    const body: AiAgentForm = {
      name: name.value,
      description: description.value,
      type: selectedCategory.value,
      prompt_template: systemPrompt.value,
      model: JSON.stringify(selectedModel.value),
      config: JSON.stringify(config),
      cover: stringifyAgentCover({
        icon: selectedCoverIcon.value,
        color: selectedCoverColor.value
      })
    }
    const response = isEditMode.value && props.initialData?.id
        ? await api.agent.updateAgent(Number(props.initialData.id), body)
        : await api.agent.createAgent(body)
    const agent = (response as any)?.data ?? props.initialData ?? ({} as AiAgentTable)
    emit('success', agent, isEditMode.value)
    emit('close')
  } catch (err: any) {
    error.value = err.message || "发生错误"
  } finally {
    loading.value = false
  }
}

</script>

