<template>
  <div
    @click="$emit('click')"
    @contextmenu.prevent="handleContextMenu"
    :class="[
      'flex items-center gap-3 px-3 py-2.5 rounded-lg border transition-all',
      isSelected
        ? 'bg-blue-50 border-blue-200 ring-1 ring-blue-100'
        : 'bg-white border-gray-100 hover:border-blue-200 hover:bg-slate-50'
    ]"
  >
    <!-- 图标 -->
    <div
      class="flex-shrink-0 w-8 h-8 rounded-md flex items-center justify-center"
      :class="item.type === 'directory' ? 'bg-blue-50 text-blue-600' : 'bg-slate-50 text-slate-600'"
    >
      <Folder v-if="item.type === 'directory'" :size="16" class="text-blue-500" />
      <File v-else :size="16" class="text-slate-500" />
    </div>

    <!-- 文件名 -->
    <div class="flex-1 min-w-0">
      <div class="font-medium text-slate-800 text-sm truncate group-hover:text-blue-600 transition-colors">
        {{ item.name }}
      </div>
    </div>

    <!-- 类型 -->
    <div class="w-16">
      <span
        class="px-2 py-0.5 rounded text-xs"
        :class="item.type === 'directory' ? 'bg-blue-100 text-blue-700' : 'bg-slate-100 text-slate-700'"
      >
        {{ item.type === 'directory' ? '目录' : '文件' }}
      </span>
    </div>

    <!-- 大小 -->
    <div class="w-20 text-right text-xs text-slate-500">
      <span v-if="item.type === 'file' && item.size">
        {{ formatFileSize(item.size) }}
      </span>
      <span v-else class="text-slate-300">-</span>
    </div>

    <!-- 修改时间 -->
    <div class="w-28 text-right text-xs text-slate-500">
      {{ formatDate(item.modified) }}
    </div>

    <!-- 操作按钮 -->
    <div class="w-24 flex items-center justify-end gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
      <button
        v-if="item.type === 'file' && item.canDownload"
        @click.stop="$emit('action', 'download', item)"
        class="p-1 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded"
        title="下载"
      >
        <Download :size="12" />
      </button>
      <button
        v-if="item.canDelete"
        @click.stop="$emit('action', 'delete', item)"
        class="p-1 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded"
        title="删除"
      >
        <Trash2 :size="12" />
      </button>
      <button
        v-if="item.type === 'file'"
        @click.stop="$emit('action', 'preview', item)"
        class="p-1 text-slate-400 hover:text-purple-600 hover:bg-purple-50 rounded"
        title="预览"
      >
        <Eye :size="12" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Folder, File, Download, Trash2, Eye } from 'lucide-vue-next'
import type { FileSystemItem } from './types'

defineProps<{
  item: FileSystemItem
  isSelected: boolean
}>()

defineEmits<{
  click: []
  action: [action: string, item: FileSystemItem]
}>()

// 右键菜单处理
const handleContextMenu = (event: MouseEvent) => {
  event.preventDefault()
  // TODO: 实现右键菜单
  console.log('Context menu for:', (event.currentTarget as HTMLElement).dataset)
}

// 格式化工具函数
const formatFileSize = (bytes?: number): string => {
  if (!bytes || bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (date: Date): string => {
  try {
    return date.toLocaleDateString('zh-CN', {
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return '-'
  }
}
</script>