<template>
  <div v-if="mode === 'list'" class="grid grid-cols-1 gap-2">
    <template v-if="loading">
       <div class="p-4 text-center text-slate-400 text-sm bg-slate-50 rounded-xl"><Loader2 class="animate-spin inline mr-2" :size="14"/> 正在加载可用模型...</div>
    </template>
    <template v-else>
        <div v-for="group in groupedModels" :key="group.providerId" class="mb-4">
            <div class="flex items-center gap-2 px-1 mb-2 text-xs font-bold text-slate-400">
                <img :src="getProviderIcon(group.providerId as any)" class="w-4 h-4" />
                {{ group.name }}
            </div>
            <div class="space-y-2">
                <div 
                    v-for="model in group.models" 
                    :key="`${model.providerId}-${model.id}`"
                    @click="selectModel(model)"
                    :class="`p-3 rounded-xl border-2 cursor-pointer flex justify-between items-center transition-all ${isSelected(model) ? 'border-blue-500 bg-blue-50' : 'border-slate-200 hover:border-blue-200'}`"
                >
                    <span class="text-sm text-slate-700 font-medium"> {{ model.name || model.id }}</span>
                </div>
            </div>
        </div>
        <div v-if="availableModels.length === 0" class="text-red-500 text-sm">暂无可用模型，请联系管理员配置。</div>
    </template>
  </div>

  <div v-else-if="mode === 'dropdown'" class="relative" ref="dropdownRef">
    <button 
        type="button"
        @click="isOpen = !isOpen"
        class="flex items-center gap-2 p-2 rounded-lg hover:bg-slate-100 transition-colors text-slate-600"
        title="切换模型"
    >
        <div v-if="modelValue" class="flex items-center gap-2 text-sm">
             <img :src="getProviderIcon(modelValue.providerId as any)" class="w-4 h-4" />
             <span class="font-medium max-w-[200px] truncate hidden sm:inline">{{ modelValue.name || modelValue.id }}</span>
        </div>
        <div v-else class="text-sm text-slate-400">选择模型</div>
        <!-- <ChevronUp v-if="isOpen" :size="14" /> -->
        <!-- <ChevronDown v-else :size="14" /> -->
    </button>

    <!-- Backdrop -->
    <div v-if="isOpen" class="fixed inset-0 z-40" @click="isOpen = false"></div>

    <div v-if="isOpen" :class="`absolute ${placement === 'top' ? 'bottom-full mb-2 slide-in-from-bottom-2' : 'top-full mt-2 slide-in-from-top-2'} left-0 w-80 bg-white rounded-xl shadow-xl border border-slate-100 max-h-80 overflow-y-auto z-50 p-2 animate-in fade-in duration-200`">
        <div class="text-xs font-bold text-slate-400 px-2 py-1 mb-1 hidden">选择模型</div>
        <div v-if="loading" class="p-4 text-center text-slate-400 text-xs">
            <Loader2 class="animate-spin inline mr-1" :size="12"/> 加载中...
        </div>
        <div v-else class="space-y-1">
            <div v-for="group in groupedModels" :key="group.providerId" class="mb-2">
                <div class="flex items-center gap-2 px-2 py-1 text-xs font-bold text-slate-400 bg-slate-50 rounded mb-1">
                    <img :src="getProviderIcon(group.providerId as any)" class="w-3 h-3" />
                    {{ group.name }}
                </div>
                <div 
                    v-for="model in group.models" 
                    :key="`${model.providerId}-${model.id}`"
                    @click="selectModel(model); isOpen = false"
                    :class="`p-2 rounded-lg cursor-pointer flex items-center gap-2 text-sm transition-colors ${isSelected(model) ? 'bg-blue-50 text-blue-600' : 'hover:bg-slate-50 text-slate-700'}`"
                >
                    <div class="flex flex-col overflow-hidden w-full">
                        <span class="font-medium truncate">{{ model.name || model.id }}</span>
                    </div>
                    <Check v-if="isSelected(model)" :size="14" class="ml-auto flex-shrink-0" />
                </div>
            </div>
            <div v-if="availableModels.length === 0" class="text-center py-2 text-xs text-slate-400">暂无可用模型</div>
        </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { Loader2, ChevronDown, ChevronUp, Check } from 'lucide-vue-next'
import { useModelProviderStore, getProviderIcon } from '@/stores/modelProviders'
import type { MODEL_META, ModelType } from '@/types/model'

const props = withDefaults(defineProps<{
  modelValue: MODEL_META | null
  mode?: 'list' | 'dropdown'
  placement?: 'top' | 'bottom'
  modelType?: ModelType | null
}>(), {
  mode: 'list',
  placement: 'top',
  modelType: null
})

const emit = defineEmits<{
  'update:modelValue': [model: MODEL_META]
}>()

const isOpen = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)

const modelProviderStore = useModelProviderStore()
const { providers } = storeToRefs(modelProviderStore)

const loading = ref(false)

const availableModels = computed<MODEL_META[]>(() =>
  providers.value
    .filter((provider) => provider.isEnabled)
    .flatMap((provider) =>
      provider.config.models
        .filter((model) => {
          // 过滤未启用的模型
          if (model.enabled === false) return false
          // 如果指定了modelType，按类型过滤
          if (props.modelType) {
            return model.type === props.modelType
          }
          return true
        })
        .map((model) => ({...model, group: provider.name, providerId: provider.id}))
    )
)

const groupedModels = computed(() => {
  const groups: Record<string, { providerId: string, name: string, models: MODEL_META[] }> = {}
  
  availableModels.value.forEach(model => {
    const groupId = model.providerId || 'other'
    if (!groups[groupId]) {
      groups[groupId] = {
        providerId: groupId,
        name: model.group || groupId,
        models: []
      }
    }
    groups[groupId].models.push(model)
  })
  
  return Object.values(groups)
})

const selectModel = (model: MODEL_META) => {
  emit('update:modelValue', model)
}

const isSelected = (model: MODEL_META) => {
  return props.modelValue?.id === model.id && props.modelValue?.providerId === model.providerId
}
</script>
