<template>
  <div 
    @click="handleClick"
    class="group bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:shadow-xl hover:border-blue-100 transition-all cursor-pointer relative overflow-hidden flex flex-col h-full"
  >
    <!-- 顶部标签 -->
    <div class="flex justify-between items-start mb-4">
      <div :class="`w-12 h-12 rounded-xl flex items-center justify-center text-white shadow-lg bg-gradient-to-br from-purple-500 to-indigo-600`">
         <Box :size="24" />
      </div>
      
      <!-- 右上角操作区 -->
      <div class="flex gap-1">
              <!-- 编辑按钮 -->
              <button 
                  v-if="onEdit" 
                  @click="handleEditClick"
                  class="p-2 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-full transition-colors"
                  title="编辑"
              >
                  <Pencil :size="16" />
              </button>
              <!-- 删除按钮 -->
              <button 
                  v-if="onDelete" 
                  @click="handleDeleteClick"
                  class="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors"
                  title="删除"
              >
                  <Trash2 :size="16" />
              </button>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="flex-1">
      <h3 class="text-lg font-bold text-slate-900 mb-2 group-hover:text-blue-600 transition-colors line-clamp-1">
          {{ displayName }}
      </h3>
      <p class="text-slate-500 text-sm line-clamp-3 leading-relaxed">
          {{ description }}
      </p>
    </div>

    <!-- 底部信息 -->
    <div class="mt-6 pt-4 border-t border-gray-50 flex items-center justify-between">
      <div class="flex items-center gap-2">
          <span :class="`w-1.5 h-1.5 rounded-full ${isSystem ? 'bg-blue-400' : 'bg-green-400'} animate-pulse`"></span>
          <span class="text-xs text-slate-400 font-medium truncate max-w-[100px]" :title="categoryLabel">
              {{ categoryLabel }}
          </span>
      </div>
      <div :class="`text-xs font-medium px-2.5 py-0.5 rounded-full border ${typeClass}`" :title="typeLabel">
          {{ typeLabel }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ArrowRight, Box, Pencil, Trash2 } from 'lucide-vue-next'
import type { AiMcpTable } from '../../services/fastApi/module_ai/ai_mcp'

// 定义组件属性
const props = defineProps<{
  mcp: AiMcpTable
  onClick: () => void
  onEdit?: (mcp: AiMcpTable) => void
  onDelete?: (mcp: AiMcpTable) => void
}>()

// 计算属性
const isSystem = computed(() => !props.mcp.created_id)
const displayName = computed(() => props.mcp.name || '未命名 MCP')
const description = computed(() => props.mcp.abstract || '暂无描述')
const categoryLabel = computed(() => props.mcp.category || '未分类')
const typeLabel = computed(() => props.mcp.type || '未知类型')

// 类型样式映射
const typeClass = computed(() => {
  const type = (props.mcp.type || '').toLowerCase()
  switch (type) {
    case 'sse':
      return 'bg-indigo-50 text-indigo-600 border-indigo-100'
    case 'stdio':
      return 'bg-purple-50 text-purple-600 border-purple-100'
    case 'http':
      return 'bg-emerald-50 text-emerald-600 border-emerald-100'
    default:
      return 'bg-slate-50 text-slate-500 border-slate-100'
  }
})

// 点击事件
const handleClick = () => {
  props.onClick()
}

// 编辑按钮点击事件
const handleEditClick = (event: MouseEvent) => {
  event.stopPropagation()
  if (props.onEdit) {
    props.onEdit(props.mcp)
  }
}

// 删除按钮点击事件
const handleDeleteClick = (event: MouseEvent) => {
  event.stopPropagation()
  if (props.onDelete) {
    props.onDelete(props.mcp)
  }
}
</script>
