<template>
  <div class="min-h-screen bg-slate-50 p-8 overflow-y-auto">
    <div class="max-w-6xl mx-auto">
      <!-- 顶部导航栏 -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <button @click="router.back()" class="flex items-center gap-2 text-slate-500 hover:text-slate-900 mb-2">
              <ArrowLeftIcon :size="20" /> 返回
          </button>
          <h1 class="text-3xl font-bold text-slate-900 flex items-center gap-3">
             <CpuIcon class="text-blue-600" /> 系统模型配置
          </h1>
        </div>
      </div>

      <!-- 配置表单卡片 -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
        <!-- 加载中状态 -->
        <div v-if="loading" class="p-12 text-center">
          <Loader2Icon class="w-8 h-8 animate-spin text-blue-500 mx-auto mb-3" />
          <div class="text-slate-400">加载配置中...</div>
        </div>
        <div v-else class="p-6">
          <!-- 第一行：系统推理模型 + Embedding模型 -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-5">
            <!-- 系统推理模型 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">
                系统推理模型 <span class="text-red-500">*</span>
              </label>
              <div class="relative">
                <button
                  type="button"
                  @click="openModelSelector('chat')"
                  class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-left focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all flex items-center justify-between"
                  :class="{ 'border-red-300': showValidation && !form.chatModel }"
                >
                  <span v-if="form.chatModel" class="text-slate-700">{{ form.chatModel.name }}</span>
                  <span v-else class="text-slate-400">Select model</span>
                  <ChevronDownIcon class="w-4 h-4 text-slate-400" />
                </button>
                <SparklesIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              </div>
              <p v-if="showValidation && !form.chatModel" class="text-red-500 text-xs mt-1">请选择系统推理模型</p>
            </div>

            <!-- Embedding 模型 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">
                Embedding 模型
              </label>
              <div class="relative">
                <button
                  type="button"
                  @click="openModelSelector('embedding')"
                  class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-left focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all flex items-center justify-between"
                >
                  <span v-if="form.embeddingModel" class="text-slate-700">{{ form.embeddingModel.name }}</span>
                  <span v-else class="text-slate-400">Select model</span>
                  <ChevronDownIcon class="w-4 h-4 text-slate-400" />
                </button>
                <DatabaseIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              </div>
            </div>
          </div>

          <!-- 第二行：Rerank模型 + 语音转文本模型 -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-5">
            <!-- Rerank 模型 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">
                Rerank 模型
              </label>
              <div class="relative">
                <button
                  type="button"
                  @click="openModelSelector('rerank')"
                  class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-left focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all flex items-center justify-between"
                >
                  <span v-if="form.rerankModel" class="text-slate-700">{{ form.rerankModel.name }}</span>
                  <span v-else class="text-slate-400">Select model</span>
                  <ChevronDownIcon class="w-4 h-4 text-slate-400" />
                </button>
                <ListOrderedIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              </div>
            </div>

            <!-- 语音转文本模型 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">
                语音转文本模型 <span class="text-xs text-slate-400 ml-1">(待定)</span>
              </label>
              <div class="relative">
                <button
                  type="button"
                  disabled
                  class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-left flex items-center justify-between opacity-60 cursor-not-allowed"
                >
                  <span v-if="form.sttModel" class="text-slate-700">{{ form.sttModel.name }}</span>
                  <span v-else class="text-slate-400">Select model</span>
                  <ChevronDownIcon class="w-4 h-4 text-slate-400" />
                </button>
                <MicIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              </div>
            </div>
          </div>

          <!-- 第三行：文本转语音模型 -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <!-- 文本转语音模型 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">
                文本转语音模型 <span class="text-xs text-slate-400 ml-1">(待定)</span>
              </label>
              <div class="relative">
                <button
                  type="button"
                  disabled
                  class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-left flex items-center justify-between opacity-60 cursor-not-allowed"
                >
                  <span v-if="form.ttsModel" class="text-slate-700">{{ form.ttsModel.name }}</span>
                  <span v-else class="text-slate-400">Select model</span>
                  <ChevronDownIcon class="w-4 h-4 text-slate-400" />
                </button>
                <Volume2Icon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              </div>
            </div>
          </div>
        </div>

        <!-- 底部操作按钮 -->
        <div v-if="!loading" class="px-6 py-4 border-t border-slate-100 flex justify-end gap-3 bg-slate-50/30">
          <button
            @click="router.back()"
            class="px-5 py-2.5 border border-slate-200 rounded-xl text-slate-700 hover:bg-white hover:border-slate-300 transition-all"
          >
            取消
          </button>
          <button
            @click="handleSave"
            :disabled="saving"
            class="px-5 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-all disabled:opacity-50 flex items-center gap-2 shadow-sm"
          >
            <Loader2Icon v-if="saving" class="w-4 h-4 animate-spin" />
            {{ saving ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 模型选择弹窗 -->
    <div v-if="showSelector" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col">
        <div class="px-6 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
          <h2 class="text-xl font-bold text-slate-900">选择{{ selectorTitle }}</h2>
          <button @click="closeSelector" class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all">
            <XIcon class="w-5 h-5" />
          </button>
        </div>
        <div class="flex-1 overflow-y-auto p-6">
          <ModelSelector
            v-model="selectedModel"
            :model-type="currentModelType"
            mode="list"
          />
        </div>
        <div class="px-6 py-4 border-t border-slate-100 flex justify-end gap-3 bg-slate-50/30">
          <button
            @click="closeSelector"
            class="px-5 py-2.5 border border-slate-200 rounded-xl text-slate-700 hover:bg-white hover:border-slate-300 transition-all"
          >
            取消
          </button>
          <button
            @click="confirmModelSelection"
            class="px-5 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-all shadow-sm"
          >
            确定
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  ArrowLeft as ArrowLeftIcon,
  Cpu as CpuIcon,
  Sparkles as SparklesIcon,
  Database as DatabaseIcon,
  ListOrdered as ListOrderedIcon,
  Mic as MicIcon,
  Volume2 as Volume2Icon,
  ChevronDown as ChevronDownIcon,
  X as XIcon,
  Loader2 as Loader2Icon
} from 'lucide-vue-next'
import ModelSelector from '@/components/common/ModelSelector.vue'
import { api } from '@/services/api'
import message from '@/components/common/message'
import type { MODEL_META, ModelType } from '@/types/model'

const router = useRouter()

// 表单数据
const form = reactive<{
  chatModel: MODEL_META | null
  embeddingModel: MODEL_META | null
  rerankModel: MODEL_META | null
  sttModel: MODEL_META | null
  ttsModel: MODEL_META | null
}>({
  chatModel: null,
  embeddingModel: null,
  rerankModel: null,
  sttModel: null,
  ttsModel: null
})

// 状态
const loading = ref(false)
const saving = ref(false)
const showValidation = ref(false)
const showSelector = ref(false)
const currentModelType = ref<ModelType | null>(null)
const selectedModel = ref<MODEL_META | null>(null)
const currentField = ref<string>('')

// 选择器标题
const selectorTitle = computed(() => {
  const titles: Record<string, string> = {
    chat: '系统推理模型',
    embedding: 'Embedding 模型',
    rerank: 'Rerank 模型',
    stt: '语音转文本模型',
    tts: '文本转语音模型'
  }
  return titles[currentModelType.value || ''] || '模型'
})

// 打开模型选择器
const openModelSelector = (type: ModelType) => {
  currentModelType.value = type
  currentField.value = type + 'Model'
  selectedModel.value = form[currentField.value as keyof typeof form] as MODEL_META | null
  showSelector.value = true
}

// 关闭选择器
const closeSelector = () => {
  showSelector.value = false
  selectedModel.value = null
  currentModelType.value = null
  currentField.value = ''
}

// 确认模型选择
const confirmModelSelection = () => {
  if (currentField.value) {
    (form[currentField.value as keyof typeof form] as MODEL_META | null) = selectedModel.value
  }
  closeSelector()
}

// 加载配置
const loadConfig = async () => {
  loading.value = true
  try {
    const config = await api.sysmodel.getSysModels()
    if (config) {
      if (config.chatModel) form.chatModel = config.chatModel
      if (config.embeddingModel) form.embeddingModel = config.embeddingModel
      if (config.rerankModel) form.rerankModel = config.rerankModel
      if (config.sttModel) form.sttModel = config.sttModel
      if (config.ttsModel) form.ttsModel = config.ttsModel
    }
  } catch (error) {
    console.error('Failed to load sysmodel config:', error)
    message.error('加载配置失败')
  } finally {
    loading.value = false
  }
}

// 保存配置
const handleSave = async () => {
  showValidation.value = true

  // 验证必填项
  if (!form.chatModel) {
    message.warning('请选择系统推理模型')
    return
  }

  saving.value = true
  try {
    const data = {
      chatModel: form.chatModel,
      embeddingModel: form.embeddingModel,
      rerankModel: form.rerankModel,
      sttModel: form.sttModel,
      ttsModel: form.ttsModel
    }
    await api.sysmodel.setSysModels(data)
    message.success('保存成功')
    router.back()
  } catch (error) {
    console.error('Failed to save sysmodel config:', error)
    message.error('保存失败')
  } finally {
    saving.value = false
  }
}

// 组件挂载时加载配置
onMounted(() => {
  loadConfig()
})
</script>
