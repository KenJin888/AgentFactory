<template>
  <div
    @click="$emit('click')"
    @contextmenu.prevent="handleContextMenu"
    :class="[
      'group bg-white rounded-xl p-4 border border-gray-100 shadow-sm hover:shadow-lg hover:border-blue-200 transition-all duration-200 cursor-pointer',
      isSelected
        ? 'bg-blue-50 border-blue-200 ring-2 ring-blue-100'
        : 'hover:bg-slate-50'
    ]"
  >
    <div class="flex items-start gap-3">
      <!-- 图标 -->
      <div
        class="flex-shrink-0 w-12 h-12 rounded-lg flex items-center justify-center"
        :class="item.type === 'directory' ? 'bg-blue-50 text-blue-600' : 'bg-slate-50 text-slate-600'"
      >
        <Folder v-if="item.type === 'directory'" :size="24" class="text-blue-500" />
        <File v-else :size="24" class="text-slate-500" />
      </div>

      <!-- 内容 -->
      <div class="flex-1 min-w-0">
        <!-- 文件名 -->
        <div class="font-medium text-slate-800 text-sm line-clamp-1 group-hover:text-blue-600 transition-colors">
          {{ item.name }}
        </div>

        <!-- 文件信息 -->
        <div class="text-xs text-slate-500 mt-1 flex items-center gap-2">
          <!-- 类型标签 -->
          <span
            class="px-1.5 py-0.5 rounded text-xs"
            :class="item.type === 'directory' ? 'bg-blue-100 text-blue-700' : 'bg-slate-100 text-slate-700'"
          >
            {{ item.type === 'directory' ? '目录' : '文件' }}
          </span>

          <!-- 文件大小 -->
          <span v-if="item.type === 'file' && item.size" class="text-slate-400">
            {{ formatFileSize(item.size) }}
          </span>

          <!-- 修改时间 -->
          <span class="text-slate-400 flex-1 text-right">
            {{ formatDate(item.modified) }}
          </span>
        </div>

        <!-- 操作按钮（悬停显示） -->
        <div class="mt-2 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
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
            v-if="item.canRename"
            @click.stop="$emit('action', 'rename', item)"
            class="p-1 text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 rounded"
            title="重命名"
          >
            <Pencil :size="12" />
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
    </div>
  </div>
</template>

<script setup lang="ts">
import { Folder, File, Download, Trash2, Pencil, Eye } from 'lucide-vue-next'
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
      day: '2-digit'
    })
  } catch {
    return '-'
  }
}
</script>