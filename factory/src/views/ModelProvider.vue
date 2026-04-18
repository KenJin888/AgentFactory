<template>
  <div class="h-screen overflow-hidden bg-slate-50 p-8">
    <div class="max-w-6xl mx-auto h-full flex flex-col">
      <!-- 顶部导航栏 -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">模型服务商</h1>
          <p class="mt-1 text-sm text-slate-500">管理和配置大模型服务提供商。</p>
        </div>
        <button
          @click="showSystemModelConfig = true"
          class="px-6 py-3 bg-slate-900 text-white rounded-xl font-bold hover:bg-slate-800 shadow-lg flex items-center gap-2 transition-transform active:scale-95"
        >
          <Settings :size="20" />
          系统模型
        </button>
      </div>

      <!-- 内容区域：左右分栏布局 -->
      <div class="grid grid-cols-12 gap-6 flex-1 min-h-0">
        <!-- 左侧：服务商列表 -->
        <div class="col-span-4 h-full min-h-0 bg-white rounded-2xl shadow-sm border border-slate-100 flex flex-col overflow-hidden">
          <!-- 列表区域 -->
          <div class="flex-1 overflow-y-auto p-2 space-y-1">
            <div 
              v-for="provider in providers" 
              :key="provider.id"
              @click="selectProvider(provider.id)"
              :class="[
                'flex items-center justify-between p-3 rounded-xl cursor-pointer transition-all duration-200 group',
                selectedProvider?.id === provider.id ? 'bg-blue-50 border-blue-100 ring-1 ring-blue-200' : 'hover:bg-slate-50 border border-transparent'
              ]"
            >
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-white border border-slate-200 flex items-center justify-center shadow-sm">
                  <img :src="getProviderIcon(provider.id)" :alt="provider.name" class="w-6 h-6 object-contain" />
                </div>
                <div>
                  <h3 class="font-medium text-slate-900">{{ provider.name }}</h3>
                  <div class="flex items-center gap-2">
                    <span :class="[
                      'w-2 h-2 rounded-full',
                      provider.isEnabled ? 'bg-green-500' : 'bg-slate-300'
                    ]"></span>
                    <span class="text-xs text-slate-500">{{ provider.isEnabled ? '已启用' : '未启用' }}</span>
                  </div>
                </div>
              </div>
              
              <!-- 切换开关 -->
              <button 
                :class="[
                  'p-1.5 rounded-full transition-colors',
                  provider.isEnabled ? 'text-green-600 bg-green-50 hover:bg-green-100' : 'text-slate-400 hover:bg-slate-100'
                ]"
                title="切换启用状态"
              >
                <Power :size="16" />
              </button>
            </div>
          </div>
        </div>

        <!-- 右侧：详细配置区域 -->
        <div class="col-span-8 h-full min-h-0 bg-white rounded-2xl shadow-sm border border-slate-100 p-8 overflow-y-auto">
          <component 
            v-if="currentProviderWithComponent" 
            :is="currentProviderWithComponent.component" 
            :provider="currentProviderWithComponent"
          />
          <DefaultConfig v-else />
        </div>
      </div>
    </div>

    <!-- 系统模型配置弹窗 -->
    <SystemModelConfig
      v-model:visible="showSystemModelConfig"
      @success="handleSystemModelSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watchEffect } from 'vue'
import { storeToRefs } from 'pinia'
import { Power, Settings } from 'lucide-vue-next'
import { useModelProviderStore, getProviderIcon } from '@/stores/modelProviders'
import SystemModelConfig from './admin/SystemModelConfig.vue'
import message from '@/components/common/message'

// 导入配置组件
import OpenAIConfig from '../components/provider/OpenAIConfig.vue'
import DefaultConfig from '../components/provider/DefaultConfig.vue'

// 系统模型配置弹窗显示状态
const showSystemModelConfig = ref(false)

// 系统模型保存成功回调
const handleSystemModelSuccess = () => {
  message.success('系统模型配置已更新')
}

const modelProviderStore = useModelProviderStore()
const { providers } = storeToRefs(modelProviderStore)
const selectedProviderId = ref<string | null>(null)


const selectedProvider = computed(() => {
  if (!selectedProviderId.value) return null
  return providers.value.find((provider) => provider.id === selectedProviderId.value) ?? null
})

watchEffect(() => {
  if (!selectedProviderId.value && providers.value.length > 0) {
    selectedProviderId.value = providers.value[0].id
  }
})

const currentProviderWithComponent = computed(() => {
  if (!selectedProvider.value) return null
  //const component = providerComponents[selectedProvider.value.id]
  //if (!component) return null
  return { ...selectedProvider.value, component:OpenAIConfig }
})

// 选择服务商
const selectProvider = (providerId: string) => {
  selectedProviderId.value = providerId
}

// 切换启用状态
const toggleProvider = (providerId: string) => {
  modelProviderStore.toggleProvider(providerId)
}
</script>
