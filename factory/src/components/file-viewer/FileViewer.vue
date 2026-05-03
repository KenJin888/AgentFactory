<template>
  <div class="absolute inset-0 z-50 flex justify-end">
    <!-- 遮罩层 -->
    <div
      class="absolute inset-0 bg-black/20 backdrop-blur-sm"
      @click="$emit('close')"
    ></div>

    <!-- 主容器 -->
    <div class="relative w-[900px] bg-white h-full shadow-2xl flex flex-col animate-in slide-in-from-right duration-200">
      <!-- 标题栏 -->
      <div class="p-4 border-b border-gray-100 flex items-center justify-between bg-slate-50/50">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-blue-50 flex items-center justify-center">
            <Files :size="20" class="text-blue-600" />
          </div>
          <div>
            <h3 class="font-bold text-slate-700 flex items-center gap-2">
              文件管理
            </h3>
            <p v-if="currentPath" class="text-xs text-slate-400 mt-0.5 truncate max-w-md">
              路径: {{ currentPath }}
            </p>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <button
            @click="refresh"
            class="p-2 text-slate-500 hover:text-blue-600 hover:bg-slate-100 rounded-lg transition-colors"
            title="刷新"
            :disabled="loading"
          >
            <RefreshCw :size="18" :class="loading ? 'animate-spin' : ''" />
          </button>
          <button
            @click="$emit('close')"
            class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg"
          >
            <X :size="18" />
          </button>
        </div>
      </div>

      <!-- 工具栏 -->
      <div class="p-3 border-b border-gray-100 bg-white flex items-center justify-between gap-4">
        <!-- 面包屑导航 -->
        <div class="flex items-center gap-1 flex-1 min-w-0">
          <button
            v-if="currentPath"
            @click="goToParentDirectory"
            class="p-1.5 text-slate-500 hover:text-blue-600 hover:bg-slate-100 rounded-lg transition-colors"
            title="返回上级"
          >
            <ArrowUp :size="14" />
          </button>

          <div class="flex items-center gap-1 overflow-x-auto scrollbar-hide">
            <span
              v-for="(crumb, index) in breadcrumbPaths"
              :key="crumb.path"
              class="flex items-center"
            >
              <button
                v-if="index > 0"
                @click="loadFileList(crumb.path)"
                class="px-2 py-1 text-xs text-slate-600 hover:text-blue-600 hover:bg-slate-100 rounded transition-colors truncate max-w-[120px]"
              >
                {{ crumb.name }}
              </button>
              <span v-else class="px-2 py-1 text-xs text-slate-400">
                {{ crumb.name }}
              </span>

              <ChevronRight
                v-if="index < breadcrumbPaths.length - 1"
                :size="12"
                class="text-slate-300 mx-1"
              />
            </span>
          </div>
        </div>

        <!-- 搜索和视图切换 -->
        <div class="flex items-center gap-3">
          <!-- 搜索框 -->
          <div class="relative group">
            <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-blue-500" :size="14" />
            <input
              type="text"
              placeholder="搜索文件..."
              v-model="searchQuery"
              class="w-48 pl-8 pr-3 py-1.5 text-xs bg-white border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-50 focus:border-blue-300 outline-none transition-all"
            />
          </div>

          <!-- 视图切换 -->
          <div class="flex items-center bg-slate-100 rounded-lg p-0.5">
            <button
              @click="viewMode = 'grid'"
              :class="[
                'p-1.5 rounded-md transition-colors',
                viewMode === 'grid'
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-slate-500 hover:text-slate-700'
              ]"
              title="网格视图"
            >
              <Grid3x3 :size="14" />
            </button>
            <button
              @click="viewMode = 'list'"
              :class="[
                'p-1.5 rounded-md transition-colors',
                viewMode === 'list'
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-slate-500 hover:text-slate-700'
              ]"
              title="列表视图"
            >
              <List :size="14" />
            </button>
          </div>
        </div>
      </div>

      <!-- 内容区域 -->
      <div class="flex-1 flex overflow-hidden">
        <!-- 左侧文件列表 -->
        <div class="w-1/2 border-r border-gray-100 flex flex-col">
          <div class="flex-1 overflow-y-auto p-4">
            <!-- 加载状态 -->
            <div v-if="loading" class="flex justify-center py-8 text-slate-400">
              <Loader2 class="animate-spin" :size="20" />
            </div>

            <!-- 错误状态 -->
            <div v-else-if="error" class="text-center py-8">
              <div class="text-red-500 text-sm mb-2">{{ error }}</div>
              <button
                @click="refresh"
                class="px-3 py-1.5 text-xs bg-red-50 text-red-600 rounded-lg hover:bg-red-100"
              >
                重试
              </button>
            </div>

            <!-- 空状态 -->
            <div v-else-if="filteredItems.length === 0" class="text-center py-10 text-slate-400 text-sm">
              <template v-if="searchQuery.trim()">
                <p>未找到匹配 "{{ searchQuery }}" 的文件</p>
                <p class="text-xs mt-1">共 {{ items.length }} 个文件</p>
              </template>
              <template v-else>
                <FolderOpen :size="32" class="mx-auto mb-3 text-slate-300" />
                <p>当前目录为空</p>
              </template>
            </div>

            <!-- 网格视图 -->
            <div v-else-if="viewMode === 'grid'" class="grid grid-cols-2 gap-3">
              <FileGridItem
                v-for="item in filteredItems"
                :key="item.id"
                :item="item"
                :is-selected="selectedFile?.id === item.id"
                @click="selectFile(item)"
                @action="handleFileAction"
              />
            </div>

            <!-- 列表视图 -->
            <div v-else class="space-y-2">
              <FileListItem
                v-for="item in filteredItems"
                :key="item.id"
                :item="item"
                :is-selected="selectedFile?.id === item.id"
                @click="selectFile(item)"
                @action="handleFileAction"
              />
            </div>
          </div>
        </div>

        <!-- 右侧预览面板 -->
        <div class="w-1/2 flex flex-col">
          <div class="p-4 border-b border-gray-100 bg-slate-50/50">
            <h4 class="font-medium text-slate-700 text-sm">文件预览</h4>
            <p v-if="selectedFile" class="text-xs text-slate-400 mt-1 truncate">
              {{ selectedFile.path }}
            </p>
            <p v-else class="text-xs text-slate-400 mt-1">选择文件查看内容</p>
          </div>

          <div class="flex-1 overflow-y-auto p-4">
            <!-- 内容加载状态 -->
            <div v-if="contentLoading" class="flex justify-center py-8 text-slate-400">
              <Loader2 class="animate-spin" :size="20" />
            </div>

            <!-- 内容错误 -->
            <div v-else-if="contentError" class="text-center py-8">
              <div class="text-red-500 text-sm mb-2">{{ contentError }}</div>
              <button
                @click="selectedFile && loadFileContent(selectedFile)"
                class="px-3 py-1.5 text-xs bg-red-50 text-red-600 rounded-lg hover:bg-red-100"
              >
                重试
              </button>
            </div>

            <!-- 文件内容 -->
            <template v-else-if="fileContent">
              <div class="mb-4">
                <div class="text-sm text-slate-500 mb-2">文件信息:</div>
                <div class="text-xs text-slate-400 space-y-1">
                  <div>路径: {{ fileContent.path }}</div>
                  <div>大小: {{ formatFileSize(fileContent.size) }}</div>
                  <div>修改时间: {{ formatDate(fileContent.modified) }}</div>
                </div>
              </div>

              <div class="border-t border-gray-100 pt-4">
                <div class="flex items-center justify-between mb-2">
                  <div class="text-sm text-slate-500">内容预览:</div>
                  <button
                    v-if="selectedFile?.canDownload"
                    class="px-2 py-1 text-xs bg-blue-50 text-blue-600 rounded hover:bg-blue-100"
                    @click="handleDownload"
                  >
                    下载
                  </button>
                </div>
                <pre class="text-sm text-slate-700 bg-slate-50 p-3 rounded-lg border border-gray-200 overflow-x-auto whitespace-pre-wrap break-words max-h-[400px] overflow-y-auto">{{ fileContent.content }}</pre>
              </div>
            </template>

            <!-- 未选择文件 -->
            <div v-else class="text-center py-10 text-slate-400 text-sm">
              <FileText :size="32" class="mx-auto mb-3 text-slate-300" />
              <p>选择左侧文件查看内容</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Files, X, RefreshCw, ArrowUp, ChevronRight, Search, Grid3x3, List, Loader2, FolderOpen, FileText } from 'lucide-vue-next'
import { useFileViewer } from './useFileViewer'
import FileGridItem from './FileGridItem.vue'
import FileListItem from './FileListItem.vue'

const props = defineProps<{
  conversationId: number
}>()

const emit = defineEmits<{
  close: []
}>()

// 使用组合式函数
const {
  items,
  selectedFile,
  fileContent,
  currentPath,
  viewMode,
  searchQuery,
  loading,
  error,
  contentLoading,
  contentError,
  filteredItems,
  breadcrumbPaths,
  loadFileList,
  selectFile,
  loadFileContent,
  goToParentDirectory,
  refresh
} = useFileViewer(props.conversationId)

// 组件挂载时加载文件列表
import { onMounted } from 'vue'
onMounted(() => {
  loadFileList()
})

// 文件操作处理
const handleFileAction = (action: string, item: any) => {
  console.log('File action:', action, item)
  // TODO: 实现文件操作（下载、删除、重命名等）
}

// 下载文件
const handleDownload = () => {
  if (!selectedFile.value) return
  // TODO: 实现下载功能
  console.log('Download file:', selectedFile.value.path)
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
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
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