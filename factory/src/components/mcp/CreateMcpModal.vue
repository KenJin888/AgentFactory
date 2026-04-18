<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
    <div class="bg-white rounded-3xl w-full max-w-2xl shadow-2xl overflow-hidden border border-slate-100 flex flex-col max-h-[90vh]">
      <!-- Header -->
      <div class="px-8 py-6 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
        <div>
          <h2 class="text-xl font-bold flex items-center gap-2 text-slate-900">
            <Box :size="20" class="text-blue-500" />
            {{ isEditMode ? '编辑 MCP' : '创建新 MCP' }}
          </h2>
          <p class="text-sm opacity-70 mt-1">配置 MCP 工具与参数</p>
        </div>
        <button type="button" @click="$emit('close')" class="p-2 rounded-full hover:bg-black/10 transition-colors"><X :size="20" /></button>
      </div>

      <!-- Form -->
      <div class="flex-1 overflow-y-auto p-8 custom-scrollbar">
          <form id="mcp-form" @submit.prevent="handleSubmit" class="space-y-6">
              <!-- 基础设定 -->
              <div class="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
                  <div>
                      <label class="block text-sm font-bold text-slate-700 mb-2">MCP 名称</label>
                      <input 
                          required 
                          v-model="form.name"
                          class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-500" 
                          placeholder="例如：天气查询" 
                      />
                  </div>
                  <div class="grid grid-cols-2 gap-4">
                      <div>
                          <label class="block text-sm font-bold text-slate-700 mb-2">类型</label>
                          <select 
                              v-model="form.type"
                              class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-500" 
                          >
                              <option value="" disabled>选择类型</option>
                              <option value="sse">sse</option>
                              <option value="stdio">stdio</option>
                              <option value="http">http</option>
                          </select>
                      </div>
                      <div>
                          <label class="block text-sm font-bold text-slate-700 mb-2">分类</label>
                          <select 
                              v-model="form.category"
                              class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-500" 
                          >
                              <option value="" disabled>选择分类</option>
                              <option value="浏览器自动化">浏览器自动化</option>
                              <option value="搜索工具">搜索工具</option>
                              <option value="交流协作">交流协作</option>
                              <option value="开发者工具">开发者工具</option>
                              <option value="娱乐和多媒体">娱乐和多媒体</option>
                              <option value="文件系统">文件系统</option>
                              <option value="其他">其他</option>
                          </select>
                      </div>
                  </div>
                  <div>
                      <label class="block text-sm font-bold text-slate-700 mb-2">简介</label>
                      <textarea 
                          rows="3" 
                          v-model="form.abstract"
                          class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-500 resize-none" 
                          placeholder="简要描述该 MCP 的功能..."
                      />
                  </div>
                  <div>
                      <label class="block text-sm font-bold text-slate-700 mb-2">配置 (JSON)</label>
                      <textarea 
                          rows="4" 
                          v-model="form.config"
                          class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-500 font-mono text-sm" 
                          placeholder="{ ... }"
                      />
                  </div>
              </div>
              <div v-if="error" class="p-4 bg-red-50 text-red-600 rounded-xl text-sm flex items-center gap-2"><AlertCircle :size="16" />{{ error }}</div>
          </form>
      </div>

      <!-- Footer -->
      <div class="px-8 py-6 border-t border-gray-100 bg-gray-50/50 flex justify-end gap-3">
          <button type="button" @click="$emit('close')" class="px-6 py-3 text-slate-600 font-medium hover:bg-slate-100 rounded-xl">取消</button>
          <button 
              form="mcp-form" 
              type="submit" 
              :disabled="loading" 
              :class="`px-8 py-3 text-white font-bold rounded-xl shadow-lg flex items-center gap-2 ${isAdminMode ? 'bg-blue-600' : 'bg-slate-900'}`"
          >
            <Loader2 v-if="loading" :size="18" class="animate-spin" />
            {{ isEditMode ? '保存修改' : '立即创建' }}
          </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import { X, Box, AlertCircle, Loader2 } from 'lucide-vue-next'
import AiMcpAPI, { type AiMcpForm, type AiMcpTable } from '../../services/fastApi/module_ai/ai_mcp'
import message from '../common/message'

// 定义组件属性
const props = defineProps<{
  initialData?: AiMcpTable | null
  isAdminMode?: boolean
}>()

// 定义组件事件
const emit = defineEmits<{
  'close': []
  'success': [mcp: AiMcpTable, isEdit: boolean]
}>()

// 响应式数据
const loading = ref(false)
const error = ref('')

const isEditMode = computed(() => !!props.initialData?.id)

const form = reactive<AiMcpForm>({
  name: props.initialData?.name || '',
  type: props.initialData?.type || '',
  category: props.initialData?.category || '',
  abstract: props.initialData?.abstract || '',
  config: props.initialData?.config || '',
  tools: props.initialData?.tools || '',
  cover: props.initialData?.cover || '',
})

type McpTransportType = 'sse' | 'stdio' | 'http'

const inferMcpTypeFromServer = (server: any): McpTransportType | '' => {
  if (!server || typeof server !== 'object') return ''

  const explicitType = typeof server.type === 'string' ? server.type.toLowerCase() : ''
  if (explicitType === 'sse' || explicitType === 'stdio' || explicitType === 'http') {
    return explicitType as McpTransportType
  }

  const transportType = typeof server.transport === 'string' ? server.transport.toLowerCase() : ''
  if (transportType === 'sse' || transportType === 'stdio' || transportType === 'http') {
    return transportType as McpTransportType
  }

  if (typeof server.command === 'string' && server.command.trim()) {
    return 'stdio'
  }

  const urlValue =
    typeof server.url === 'string'
      ? server.url
      : typeof server.baseUrl === 'string'
        ? server.baseUrl
        : ''

  if (urlValue) {
    const lowerUrl = urlValue.toLowerCase()
    if (lowerUrl.includes('/sse') || lowerUrl.endsWith('sse')) {
      return 'sse'
    }
    if (lowerUrl.startsWith('http://') || lowerUrl.startsWith('https://')) {
      return 'http'
    }
  }

  return ''
}

// 提交表单
const handleSubmit = async () => {
  error.value = ''
  
  // 验证配置格式
  if (form.config) {
    try {
      const configObj = JSON.parse(form.config)
      
      if (!configObj || typeof configObj !== 'object') {
         const msg = '配置必须是有效的 JSON 对象'
         error.value = msg
         message.error(msg)
         return
      }

      if (!configObj.mcpServers) {
        const msg = '配置必须包含 "mcpServers" 字段'
        error.value = msg
        message.error(msg)
        return
      }
      
      const servers = configObj.mcpServers
      const keys = Object.keys(servers)
      
      if (keys.length !== 1) {
        const msg = 'mcpServers 只能包含一个 key'
        error.value = msg
        message.error(msg)
        return
      }
      
      if (keys[0] !== form.name) {
        const msg = `mcpServers 的 key "${keys[0]}" 必须与 MCP 名称 "${form.name}" 一致`
        error.value = msg
        message.error(msg)
        return
      }

      const serverConfig = servers[keys[0]]
      const inferredType = inferMcpTypeFromServer(serverConfig)
      if (inferredType) {
        form.type = inferredType
      }
    } catch (e) {
      const msg = '配置 JSON 格式无效'
      error.value = msg
      message.error(msg)
      return
    }
  }

  loading.value = true
  
  try {
    let res
    if (isEditMode.value && props.initialData?.id) {
      // 更新
      res = await AiMcpAPI.updateAiMcp(Number(props.initialData.id), form)
    } else {
      // 创建
      res = await AiMcpAPI.createAiMcp(form)
    }
    
    // 这里假设 API 返回包含创建/更新后的对象，或者我们手动构造
    // 如果 ApiResponse 不包含数据，我们需要重新获取或者直接返回 form
    // 根据 ai_mcp.ts, create 返回 ApiResponse, update 返回 ApiResponse
    // 通常 ApiResponse 会有 data 字段
    
    emit('success', { ...props.initialData, ...form } as AiMcpTable, isEditMode.value)
  } catch (err: any) {
    console.error('Submit error:', err)
    error.value = err.message || '操作失败'
  } finally {
    loading.value = false
  }
}
</script>
