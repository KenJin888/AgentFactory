<template>
  <div 
    class="group bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:shadow-xl hover:border-blue-100 transition-all relative overflow-hidden flex flex-col h-full"
  >
    <!-- 顶部标签 -->
    <div  class="flex justify-between items-start mb-4">
      <AgentCoverIcon
        :cover="agent.cover || ''"
        :size="24"
        @click="handleClick"
        container-class="w-12 h-12 cursor-pointer rounded-xl flex items-center justify-center text-white shadow-lg bg-gradient-to-br"
      />
      
      <!-- 右上角操作区 -->
      <div class="flex gap-1">
              <!-- 编辑按钮 -->
              <button 
                  v-if="onEdit" 
                  @click="handleEditClick"
                  class="p-2 text-slate-300 hover:text-blue-600 hover:bg-blue-50 rounded-full transition-colors"
                  title="编辑"
              >
                  <Pencil :size="16" />
              </button>
              <!-- 删除按钮 -->
              <button 
                  v-if="onDelete" 
                  @click="handleDeleteClick"
                  class="p-2 text-slate-300 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors"
                  title="删除"
              >
                  <Trash2 :size="16" />
              </button>
              <button 
                  v-if="onPublish" 
                  @click="handlePublishClick"
                  class="p-2 text-slate-300 hover:text-emerald-600 hover:bg-emerald-50 rounded-full transition-colors"
                  title="发布到广场"
              >
                  <Send :size="16" />
              </button>
              <button 
                  v-if="onFavorite"
                  @click="handleFavoriteClick"
                  :disabled="isFavoriteLoading"
                  :class="`p-2 rounded-full transition-colors ${isFavorite ? 'text-amber-500 bg-amber-50 hover:bg-amber-100' : 'text-slate-300 hover:text-amber-500 hover:bg-amber-50'} ${isFavoriteLoading ? 'opacity-60 cursor-not-allowed' : ''}`"
                  :title="isFavorite ? '取消收藏' : '收藏'"
              >
                  <Star :size="16" :fill="isFavorite ? 'currentColor' : 'none'" />
              </button>
              <button
                  v-if="canShowClone"
                  title="复制到我的智能体"
                  class="p-2 text-slate-300 hover:text-indigo-600 hover:bg-indigo-50 rounded-full transition-colors"
                  @click="handleCloneClick"
              >
                  <Copy :size="16" />
              </button>
              <button
                  v-if="canShowMaintain" 
                  @click="handleMaintainClick"
                  class="p-2 text-slate-300 hover:text-orange-600 hover:bg-orange-50 rounded-full transition-colors"
                  title="维护"
              >
                  <Settings :size="16" />
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
          <span v-if="agent.visibility_scope === 'public'" class="text-xs text-slate-400 font-medium truncate max-w-[100px]" :title="creatorName">
              @{{ creatorName }} 创建
          </span>
          <span v-if="agent.visibility_scope === 'public'" class="text-xs text-slate-300 font-medium bg-slate-100 px-1.5 py-0.5 rounded">
              V{{ agent.version_no || 1 }}
          </span>
          <span v-if="agent.visibility_scope === 'private' && statusLabel" :class="['text-xs font-medium px-1.5 py-0.5 rounded', statusBadgeClass]">
              {{ statusLabel }}
          </span>
      </div>
      <div @click="handleClick" class="w-8 h-8 cursor-pointer rounded-full bg-slate-50 flex items-center justify-center text-slate-300 group-hover:bg-blue-600 group-hover:text-white transition-all transform group-hover:translate-x-1">
          <ArrowRight :size="16" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed} from 'vue'
import {ArrowRight, Copy, Pencil, Send, Settings, Star, Trash2} from 'lucide-vue-next'
import type {AiAgentTable} from '../../services/fastApi/module_ai/ai_agent'
import AgentCoverIcon from '@/components/common/AgentCoverIcon.vue'

// 定义组件属性
const props = defineProps<{
  agent: AiAgentTable
  onClick: () => void
  onEdit?: (agent: AiAgentTable) => void
  onDelete?: (agent: AiAgentTable) => void
  onPublish?: (agent: AiAgentTable) => void
  onClone?: (agent: AiAgentTable) => void
  onFavorite?: (agent: AiAgentTable) => void
  onMaintain?: (agent: AiAgentTable) => void
  isFavorite?: boolean
  isFavoriteLoading?: boolean
}>()

// 计算属性
const isSystem = computed(() => !props.agent.created_id)
const displayName = computed(() => props.agent.name || '未命名智能体')
const description = computed(() => {
  return props.agent.description || props.agent.prompt_template || '暂无描述'
})
const statusLabel = computed(() => {
  if (props.agent.publish_status === 'published') return '已发布'
  if (props.agent.publish_status === 'clone') return '副本'
  // if (props.agent.publish_status === 'offline') return '已下线'
  if (props.agent.publish_status === 'draft') return '个人'
  return ''
})
const statusBadgeClass = computed(() => {
  switch (props.agent.publish_status) {
    case 'published':
      return 'bg-emerald-50 text-emerald-700 border border-emerald-200'
    case 'clone':
      return 'bg-indigo-50 text-indigo-700 border border-indigo-200'
    case 'offline':
      return 'bg-amber-50 text-amber-700 border border-amber-200'
    case 'draft':
      // return 'bg-violet-50 text-violet-700 border border-violet-200'
    default:
      return 'bg-slate-100 text-slate-700 border border-slate-200'
  }
})
const creatorName = computed(() => {
  return props.agent.created_by?.name || (isSystem.value ? '系统' : '未知')
})
const isFavorite = computed(() => Boolean(props.isFavorite))
const isFavoriteLoading = computed(() => Boolean(props.isFavoriteLoading))
const canShowClone = computed(() => Boolean(props.onClone) && Boolean(props.agent.can_clone))
const canShowMaintain = computed(() => Boolean(props.onMaintain) && Boolean(props.agent.can_manage))

// 点击事件
const handleClick = () => {
  props.onClick()
}

// 编辑按钮点击事件
const handleEditClick = (event: MouseEvent) => {
  event.stopPropagation()
  if (props.onEdit) {
    props.onEdit(props.agent)
  }
}

// 删除按钮点击事件
const handleDeleteClick = (event: MouseEvent) => {
  event.stopPropagation() // 防止触发卡片跳转
  if (props.onDelete) {
    props.onDelete(props.agent)
  }
}

const handlePublishClick = (event: MouseEvent) => {
  event.stopPropagation()
  if (props.onPublish) {
    props.onPublish(props.agent)
  }
}

const handleCloneClick = (event: MouseEvent) => {
  event.stopPropagation()
  if (props.onClone) {
    props.onClone(props.agent)
  }
}

const handleFavoriteClick = (event: MouseEvent) => {
  event.stopPropagation()
  if (props.onFavorite && !isFavoriteLoading.value) {
    props.onFavorite(props.agent)
  }
}

const handleMaintainClick = (event: MouseEvent) => {
  event.stopPropagation()
  if (props.onMaintain) {
    props.onMaintain(props.agent)
  }
}
</script>
