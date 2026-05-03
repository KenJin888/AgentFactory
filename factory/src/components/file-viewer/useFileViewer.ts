import { ref, computed } from 'vue'
import type { FileSystemItem, FileContent, ViewMode } from './types'
import { normalizeFileItem, normalizeFileContent } from './types'
import AiKnowledgeBaseAPI from '@/services/fastApi/module_ai/ai_knowledge_base'

export const useFileViewer = (conversationId: number) => {
  // 状态
  const items = ref<FileSystemItem[]>([])
  const selectedFile = ref<FileSystemItem | null>(null)
  const fileContent = ref<FileContent | null>(null)
  const currentPath = ref('')
  const viewMode = ref<ViewMode>('grid')
  const searchQuery = ref('')
  const loading = ref(false)
  const error = ref<string>('')
  const contentLoading = ref(false)
  const contentError = ref<string>('')

  // 计算属性
  const filteredItems = computed(() => {
    if (!searchQuery.value.trim()) {
      return items.value
    }

    const query = searchQuery.value.toLowerCase().trim()
    return items.value.filter(item =>
      item.name.toLowerCase().includes(query) ||
      item.path.toLowerCase().includes(query)
    )
  })

  const breadcrumbPaths = computed(() => {
    if (!currentPath.value) return ['/']

    const parts = currentPath.value.split('/').filter(Boolean)
    const paths: Array<{ name: string, path: string }> = [{ name: '根目录', path: '' }]

    let current = ''
    for (const part of parts) {
      current = current ? `${current}/${part}` : part
      paths.push({ name: part, path: current })
    }

    return paths
  })

  // 方法
  const loadFileList = async (path?: string) => {
    if (!conversationId) {
      error.value = '会话ID无效'
      return
    }

    try {
      loading.value = true
      error.value = ''

      const res = await AiKnowledgeBaseAPI.listDirectory(conversationId, path ? { path } : undefined)
      console.log('API响应:', res)
      console.log('响应数据:', res.data)

      // 处理不同的响应格式
      let rawItems: any[] = []
      if (res.data?.data) {
        rawItems = res.data.data
      } else if (res.data?.code !== undefined) {
        // 其他响应格式
        rawItems = res.data.data || res.data.items || res.data.list || []
      }

      console.log('解析出的rawItems:', rawItems)
      console.log('rawItems类型:', Array.isArray(rawItems))

      // 标准化数据
      const normalizedItems = Array.isArray(rawItems)
        ? rawItems.map(normalizeFileItem)
        : []

      console.log('标准化后的items:', normalizedItems)
      items.value = normalizedItems

      currentPath.value = path || ''
      selectedFile.value = null
      fileContent.value = null
    } catch (err) {
      console.error('加载文件列表失败:', err)
      error.value = `加载失败: ${err instanceof Error ? err.message : String(err)}`
      items.value = []
    } finally {
      loading.value = false
    }
  }

  const selectFile = async (item: FileSystemItem) => {
    if (item.type === 'directory') {
      // 如果是目录，加载该目录内容
      await loadFileList(item.path)
      selectedFile.value = null
      fileContent.value = null
    } else {
      // 如果是文件，选中并加载内容
      selectedFile.value = item
      await loadFileContent(item)
    }
  }

  const loadFileContent = async (item: FileSystemItem) => {
    if (!conversationId || item.type !== 'file') return

    try {
      contentLoading.value = true
      contentError.value = ''

      const res = await AiKnowledgeBaseAPI.readFile(conversationId, { path: item.path })

      // 处理不同的响应格式
      let rawContent: any = {}
      if (res.data?.data) {
        rawContent = res.data.data
      } else if (res.data?.code !== undefined) {
        // 其他响应格式
        rawContent = res.data.data || res.data.content || {}
      }

      fileContent.value = normalizeFileContent({
        ...rawContent,
        path: item.path,
        size: item.size || 0
      })
    } catch (err) {
      console.error('加载文件内容失败:', err)
      contentError.value = `加载失败: ${err instanceof Error ? err.message : String(err)}`
      fileContent.value = null
    } finally {
      contentLoading.value = false
    }
  }

  const goToParentDirectory = () => {
    if (!currentPath.value) return

    const path = currentPath.value
    const lastSlashIndex = path.lastIndexOf('/')

    if (lastSlashIndex === -1) {
      // 已经是根目录下的直接子目录
      loadFileList('')
    } else {
      const parentPath = path.substring(0, lastSlashIndex)
      loadFileList(parentPath)
    }
  }

  const clearSelection = () => {
    selectedFile.value = null
    fileContent.value = null
  }

  const refresh = () => {
    loadFileList(currentPath.value)
  }

  return {
    // 状态
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

    // 计算属性
    filteredItems,
    breadcrumbPaths,

    // 方法
    loadFileList,
    selectFile,
    loadFileContent,
    goToParentDirectory,
    clearSelection,
    refresh
  }
}