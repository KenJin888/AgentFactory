<template>
  <div class="space-y-6">
    <div class="border-b border-slate-100 pb-4 flex items-center justify-between">
      <div>
        <h2 class="text-xl font-semibold text-slate-900">{{ title }}</h2>
        <p class="text-sm text-slate-500 mt-1">{{ subtitle }}</p>
      </div>
      <div class="flex items-center gap-3">
        <span class="text-sm" :class="props.provider.isEnabled ? 'text-green-600' : 'text-slate-500'">
          {{ props.provider.isEnabled ? '已启用' : '未启用' }}
        </span>
        <button 
          @click="toggleProviderStatus"
          type="button"
          :class="[
            'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none',
            props.provider.isEnabled ? 'bg-green-600' : 'bg-slate-200'
          ]"
        >
          <span 
            aria-hidden="true" 
            :class="[
              'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
              props.provider.isEnabled ? 'translate-x-5' : 'translate-x-0'
            ]"
          />
        </button>
      </div>
    </div>

    <div class="space-y-4">
      <div class="space-y-2">
        <label class="text-sm font-medium text-slate-700">API Key</label>
        <input 
          type="password" 
          v-model="config.apiKey"
          class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors"
        />
        <p v-if="props.provider.config.apiUrl" class="text-xs text-slate-500 mt-1">
          请前往 <a :href="props.provider.config.apiUrl" target="_blank" class="text-blue-600 hover:underline">{{ props.provider.name }}</a> 获取API Key
        </p>
      </div>

      <div class="space-y-2">
        <label class="text-sm font-medium text-slate-700">Base URL</label>
        <input 
          type="text" 
          v-model="config.baseUrl"
          :placeholder="baseUrlPlaceholder"
          class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors"
        />
        <p class="text-xs text-slate-400">如果您使用代理或中转服务，请修改此地址</p>
      </div>

      <div class="space-y-2">
        <div class="flex items-center justify-between">
          <label class="text-sm font-medium text-slate-700">模型列表</label>
          <button 
            type="button"
            @click="openAddModal" 
            class="text-blue-600 hover:text-blue-700 text-sm flex items-center gap-1"
          >
            <Plus :size="14" /> 自定义
          </button>
        </div>
        <div class="flex flex-col gap-2 min-h-[42px] max-h-64 overflow-y-auto p-3 bg-slate-50 rounded-lg border border-slate-200">
          <div 
            v-for="model in sortedModels" 
            :key="model.id"
            class="flex items-center justify-between px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm text-slate-700 hover:border-blue-200 transition-colors"
          >
            <div class="flex items-center gap-2">
              <span :class="{ 'text-slate-400': !model.enabled }">{{ model.id }}</span>
              <span 
                class="px-1.5 py-0.5 text-xs rounded border"
                :class="getTypeColor(model.type)"
              >
                {{ getTypeLabel(model.type) }}
              </span>
              <button 
                v-if="model.isCustom"
                type="button"
                @click="openDeleteConfirm(model)"
                class="text-slate-400 hover:text-red-600 transition-colors p-1"
                title="删除模型"
              >
                <Trash2 :size="14" />
              </button>
            </div>
            <div class="flex items-center gap-2">
              <label class="flex items-center gap-2 cursor-pointer select-none">
                <span class="text-xs" :class="model.enabled ? 'text-blue-600' : 'text-slate-400'">
                  {{ model.enabled ? '已启用' : '已禁用' }}
                </span>
                <div class="relative inline-flex items-center">
                  <input 
                    type="checkbox" 
                    v-model="model.enabled" 
                    class="sr-only peer"
                  >
                  <div class="w-9 h-5 bg-slate-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-blue-600"></div>
                </div>
              </label>
              <button
                type="button"
                @click="openUserConfig(model.id)"
                class="text-slate-400 hover:text-blue-600 transition-colors p-1"
                title="配置模型参数"
              >
                <Settings :size="16" />
              </button>
            </div>
          </div>
          <div v-if="config.models.length === 0" class="flex items-center justify-center h-full text-slate-400 text-sm py-4">
            未选择模型
          </div>
        </div>
      </div>
    </div>

    <div class="pt-4 flex justify-end items-center gap-3">
      <span v-if="saved" class="text-green-600 text-sm font-medium">保存成功</span>
      <button @click="handleSave" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
        保存配置
      </button>
    </div>
  </div>

  <ModelAdd 
    v-model:visible="isAddModalOpen"
    :existing-models="existingModelIds"
    @confirm="handleAddModel"
  />

  <Teleport to="body">
    <div v-if="isUserConfigOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden flex flex-col">
        <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
          <h3 class="text-lg font-semibold text-slate-900">模型参数配置</h3>
          <button @click="closeUserConfig" class="text-slate-400 hover:text-slate-600">
            ×
          </button>
        </div>
        <div class="p-6 space-y-4 max-h-[70vh] overflow-y-auto">
          <div class="space-y-2">
            <label class="text-sm font-medium text-slate-700">模型</label>
            <div class="w-full px-4 py-2 border border-slate-200 rounded-lg bg-slate-50 text-slate-700">
              {{ userConfigModelId }}
            </div>
          </div>
          <div class="space-y-2">
            <label class="text-sm font-medium text-slate-700">温度</label>
            <input
              v-model.number="userConfigForm.temperature"
              type="number"
              min="0"
              max="2"
              step="0.1"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors"
            />
            <p class="text-xs text-slate-500">控制输出的随机性，大部分模型0-1，部分支持0-2之间，越高越随机。</p>
          </div>
          <div class="space-y-2">
            <label class="text-sm font-medium text-slate-700">上下文长度</label>
            <input
              v-model.number="userConfigForm.contextLength"
              type="number"
              min="1"
              step="1"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors"
            />
          </div>
          <div class="space-y-2">
            <label class="text-sm font-medium text-slate-700">最大输出Token数量</label>
            <input
              v-model.number="userConfigForm.maxTokens"
              type="number"
              min="1"
              step="1"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors"
            />
          </div>
          <div class="space-y-2">
            <label class="text-sm font-medium text-slate-700">视觉能力</label>
            <div class="flex items-center justify-between">
              <span
                class="text-xs"
                :class="userConfigForm.vision === undefined ? 'text-slate-400' : userConfigForm.vision ? 'text-blue-600' : 'text-slate-400'"
              >
                {{ userConfigForm.vision === undefined ? '未设置' : userConfigForm.vision ? '已开启' : '已关闭' }}
              </span>
              <label class="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  v-model="userConfigForm.vision"
                  class="sr-only peer"
                >
                <div class="w-9 h-5 bg-slate-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>
          </div>
          <div class="space-y-2">
            <label class="text-sm font-medium text-slate-700">函数调用</label>
            <div class="flex items-center justify-between">
              <span
                class="text-xs"
                :class="userConfigForm.functionCall === undefined ? 'text-slate-400' : userConfigForm.functionCall ? 'text-blue-600' : 'text-slate-400'"
              >
                {{ userConfigForm.functionCall === undefined ? '未设置' : userConfigForm.functionCall ? '已开启' : '已关闭' }}
              </span>
              <label class="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  v-model="userConfigForm.functionCall"
                  class="sr-only peer"
                >
                <div class="w-9 h-5 bg-slate-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>
          </div>
          <div class="space-y-2">
            <label class="text-sm font-medium text-slate-700">推理能力</label>
            <div class="flex items-center justify-between">
              <span
                class="text-xs"
                :class="userConfigForm.reasoning === undefined ? 'text-slate-400' : userConfigForm.reasoning ? 'text-blue-600' : 'text-slate-400'"
              >
                {{ userConfigForm.reasoning === undefined ? '未设置' : userConfigForm.reasoning ? '已开启' : '已关闭' }}
              </span>
              <label class="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  v-model="userConfigForm.reasoning"
                  class="sr-only peer"
                >
                <div class="w-9 h-5 bg-slate-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>
          </div>
          <div class="space-y-2">
            <label class="text-sm font-medium text-slate-700">模型类型</label>
            <select
              v-model="userConfigForm.type"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors"
            >
              <option value="chat">对话 Chat</option>
              <option value="embedding">向量 Embedding</option>
              <option value="rerank">重排序 Rerank</option>
              <option value="imageGeneration">生图 Image</option>
            </select>
          </div>
          <div class="space-y-2">
            <label class="text-sm font-medium text-slate-700">生成内容接口</label>
            <select
              v-model="userConfigForm.apiEndpoint"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors"
            >
              <option value="chat">文本</option>
              <option value="image">图像</option>
              <option value="video">视频</option>
            </select>
          </div>
        </div>
        <div class="px-6 py-4 border-t border-slate-100 flex justify-end gap-3 bg-slate-50/30">
          <button
            @click="closeUserConfig"
            class="px-4 py-2 text-slate-600 hover:bg-slate-200 rounded-lg text-sm font-medium transition-colors"
          >
            取消
          </button>
          <button
            @click="resetUserConfig"
            class="px-4 py-2 text-slate-600 hover:bg-slate-200 rounded-lg text-sm font-medium transition-colors"
          >
            恢复默认值
          </button>
          <button
            @click="saveUserConfig"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
          >
            保存
          </button>
        </div>
      </div>
    </div>
  </Teleport>
  

</template>

<script setup lang="ts">
import {computed, ref, watch} from 'vue'
import {type ModelProvider, useModelProviderStore} from '@/stores/modelProviders'
import type {MODEL_META, ModelConfig, ModelType} from '@/types/model'
import {Plus, Settings, Trash2} from 'lucide-vue-next'
import ModelAdd from './ModelAdd.vue'
import {dialog} from '@/components/common/dialog'

const props = defineProps<{
  provider: ModelProvider
}>()

const modelProviderStore = useModelProviderStore()

const title = computed(() => `${props.provider.name} 配置`)
const subtitle = computed(() => props.provider.description || `配置 ${props.provider.name} 的 API 密钥和模型参数`)
const baseUrlPlaceholder = computed(() => props.provider.config.baseUrl || '')

type ConfigDraft = {
  apiKey: string
  baseUrl: string
  models: MODEL_META[]
}

const createConfigDraft = (provider: ModelProvider): ConfigDraft => ({
  apiKey: provider.config.apiKey ?? '',
  baseUrl: provider.config.baseUrl ?? '',
  models: (provider.config.models ?? []).map((model) => ({
    ...model,
    userConfig: model.userConfig ? {...model.userConfig} : model.userConfig
  }))
})

const config = ref<ConfigDraft>(createConfigDraft(props.provider))
const saved = ref(false)
let savedTimer: ReturnType<typeof setTimeout> | null = null

watch(
    () => props.provider.id,
    () => {
      config.value = createConfigDraft(props.provider)
  },
    {immediate: true}
)

const toggleProviderStatus = () => {
  modelProviderStore.toggleProvider(props.provider.id)
}

const handleSave = () => {
  modelProviderStore.updateProviderConfig(props.provider.id, {
    apiKey: config.value.apiKey,
    baseUrl: config.value.baseUrl,
    models: config.value.models.map(m => m)
  })
  saved.value = true
  if (savedTimer) clearTimeout(savedTimer)
  savedTimer = setTimeout(() => {
    saved.value = false
  }, 2000)
}

const isAddModalOpen = ref(false)
const existingModelIds = computed(() => config.value.models.map(m => m.id))

const sortedModels = computed(() => {
  if (!config.value.models) return []
  return [...config.value.models].sort((a, b) => {
    if (a.enabled === b.enabled) {
      return a.id.localeCompare(b.id)
    }
    return a.enabled ? -1 : 1
  })
})

const openAddModal = () => {
  isAddModalOpen.value = true
}

const handleAddModel = (model: { id: string; type: string; isCustom: boolean }) => {
  const exists = config.value.models.some(m => m.id === model.id)
  if (!exists) {
    config.value.models.push({
      id: model.id,
      name: model.id,
      providerId: props.provider.id,
      type: model.type as ModelType,
      enabled: true,
      isCustom: model.isCustom
    })
  }
  isAddModalOpen.value = false
}

const isUserConfigOpen = ref(false)
const userConfigModelId = ref('')
const defaultConfig = {
  temperature: 0.6 as number | null,
  contextLength: undefined as number | null | undefined,
  maxTokens: undefined as number | null | undefined,
  vision: undefined as boolean | null | undefined,
  functionCall: undefined as boolean | null | undefined,
  reasoning: undefined as boolean | null | undefined,
  type: undefined as ModelType | null | undefined,
  apiEndpoint: undefined as string | null | undefined
}
const userConfigForm = ref(defaultConfig)

const syncUserConfigForm = (modelId: string, reset:boolean = false) => {
  const target = config.value.models.find(m => m.id === modelId)
  if (!target) return
  if(reset) delete target.userConfig
  userConfigForm.value = {
    temperature: target.userConfig?.temperature ?? 0.6,
    contextLength: target.userConfig?.contextLength ?? target.contextLength,
    maxTokens: target.userConfig?.maxTokens ?? target.maxTokens,
    vision: target.userConfig?.vision ?? target.vision ?? false,
    functionCall: target.userConfig?.functionCall ?? target.functionCall ?? false,
    reasoning: target.userConfig?.reasoning ?? target.reasoning ?? false,
    type: target.userConfig?.type ?? target.type ?? 'chat',
    apiEndpoint: target.userConfig?.apiEndpoint ?? 'chat'
  }
}

const openUserConfig = (modelId: string) => {
  if (!modelId) return
  userConfigModelId.value = modelId
  syncUserConfigForm(modelId)
  isUserConfigOpen.value = true
}

const closeUserConfig = () => {
  isUserConfigOpen.value = false
}

watch(userConfigModelId, (nextId) => {
  if (nextId) syncUserConfigForm(nextId)
})

const normalizeNumber = (value: number | null | undefined) => {
  return typeof value === 'number' && !Number.isNaN(value) ? value : undefined
}

const normalizeBoolean = (value: boolean | null | undefined) => {
  return typeof value === 'boolean' ? value : undefined
}

const normalizeString = (value: string | null | undefined) => {
  return typeof value === 'string' && value.length > 0 ? value : undefined
}

const normalizeModelType = (value: ModelType | null | undefined): ModelConfig['type'] => {
  return value ? value : undefined
}

const resetUserConfig = async () => {
  if (!userConfigModelId.value) return
  try {
    await dialog.confirm(
      '确认恢复该模型参数到默认值？',
      '恢复默认值',
      {
        confirmText: '确认恢复',
        type: 'primary'
      }
    )
    syncUserConfigForm(userConfigModelId.value, true)
  } catch (e) {
    return
  }
}

const saveUserConfig = () => {
  const target = config.value.models.find(m => m.id === userConfigModelId.value)
  if (!target) return
  target.userConfig = {
    temperature: normalizeNumber(userConfigForm.value.temperature),
    contextLength: normalizeNumber(userConfigForm.value.contextLength),
    maxTokens: normalizeNumber(userConfigForm.value.maxTokens),
    vision: normalizeBoolean(userConfigForm.value.vision),
    functionCall: normalizeBoolean(userConfigForm.value.functionCall),
    reasoning: normalizeBoolean(userConfigForm.value.reasoning),
    type: normalizeModelType(userConfigForm.value.type),
    apiEndpoint: normalizeString(userConfigForm.value.apiEndpoint)
  }
  isUserConfigOpen.value = false
}

const openDeleteConfirm = async (model: { id: string }) => {
  try {
    await dialog.confirm(
      `是否删除 ${model.id} 模型？`,
      '删除模型',
      {
        confirmText: '确认删除',
        type: 'danger'
      }
    )
    config.value.models = config.value.models.filter(m => m.id !== model.id)
  } catch (e) {
    // Cancelled
  }
}

const getTypeColor = (type?: ModelType) => {
  switch (type) {
    case 'chat':
      return 'bg-blue-100 text-blue-700 border-blue-200'
    case 'embedding':
      return 'bg-purple-100 text-purple-700 border-purple-200'
    case 'rerank':
      return 'bg-orange-100 text-orange-700 border-orange-200'
    case 'imageGeneration':
      return 'bg-pink-100 text-pink-700 border-pink-200'
    default:
      return 'bg-slate-100 text-slate-700 border-slate-200'
  }
}

const getTypeLabel = (type?: ModelType) => {
  switch (type) {
    case 'chat': return '对话chat'
    case 'embedding': return '向量embedding'
    case 'rerank': return '重排序rerank'
    case 'imageGeneration': return '生图image'
    default: return type
  }
}
</script>
