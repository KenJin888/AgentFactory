<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
    <div class="bg-white rounded-3xl w-full max-w-4xl shadow-2xl overflow-hidden border border-slate-100 flex flex-col max-h-[90vh]">
      <!-- Header -->
      <div class="px-8 py-6 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
        <div>
          <h2 class="text-xl font-bold flex items-center gap-2 text-slate-900">
            <Wrench :size="20" class="text-blue-500" />
            {{ skillName }} - 技能详情
          </h2>
          <p class="text-sm opacity-70 mt-1">查看技能文件和内容</p>
        </div>
        <button type="button" @click="$emit('close')" class="p-2 rounded-full hover:bg-black/10 transition-colors">
          <X :size="20" />
        </button>
      </div>

      <!-- Content -->
      <div class="flex-1 overflow-y-auto p-8 custom-scrollbar">
        <div v-if="loading" class="flex items-center justify-center py-12">
          <div class="text-center text-gray-500 flex flex-col items-center gap-2">
            <Loader2 class="animate-spin" />
            <span>正在加载技能详情...</span>
          </div>
        </div>

        <div v-else class="space-y-6">
          <!-- 技能名称和信息 -->
          <div class="bg-blue-50/30 border border-blue-100 rounded-2xl p-6">
            <div class="flex items-center gap-4">
              <div class="w-16 h-16 rounded-xl flex items-center justify-center text-white shadow-lg bg-gradient-to-br from-blue-500 to-cyan-600">
                <Wrench :size="28" />
              </div>
              <div class="flex-1">
                <h3 class="text-xl font-bold text-slate-900">{{ skillName }}</h3>
                <div class="flex items-center gap-4 mt-2">
                  <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
                    <span class="text-sm text-slate-600">AI 技能</span>
                  </div>
                  <div class="text-sm text-slate-500">
                    最后更新：{{ lastUpdated }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 文件列表 -->
          <div class="border border-slate-200 rounded-2xl overflow-hidden">
            <div class="bg-slate-50 px-6 py-4 border-b border-slate-200 flex items-center justify-between">
              <div class="flex items-center gap-2">
                <Folder :size="20" class="text-slate-500" />
                <div class="flex flex-col gap-1">
                  <div class="flex items-center gap-1 text-sm">
                    <span class="font-medium text-slate-700">路径：</span>
                    <div class="flex items-center gap-1">
                      <div
                        v-for="(crumb, index) in pathBreadcrumbs"
                        :key="crumb.path"
                        class="flex items-center"
                      >
                        <button
                          @click.stop="handleBreadcrumbClick(crumb, index)"
                          class="hover:text-blue-600 transition-colors"
                          :class="{ 'font-medium text-slate-800': index === pathBreadcrumbs.length - 1, 'text-slate-600': index !== pathBreadcrumbs.length - 1 }"
                        >
                          {{ crumb.name }}
                        </button>
                        <span
                          v-if="index < pathBreadcrumbs.length - 1"
                          class="text-slate-400 ml-1"
                        >
                          /
                        </span>
                      </div>
                    </div>
                  </div>
                  <!-- 完整路径显示 - API返回的原始路径 -->
                  <div class="text-xs text-slate-500 font-mono bg-slate-50 px-2 py-1 rounded border border-slate-100">
                    {{ apiCurrentPathRaw || currentPath }}
                  </div>
                </div>
              </div>
              <div class="flex items-center gap-4">
                <!-- 文件统计信息 -->
                <div v-if="!filesLoading && files.length > 0" class="flex items-center gap-2 text-xs text-slate-500">
                  <span class="bg-slate-100 px-2 py-1 rounded">
                    共 {{ fileStats.total }} 项
                  </span>
                  <span class="bg-blue-50 text-blue-600 px-2 py-1 rounded">
                    {{ fileStats.fileCount }} 文件
                  </span>
                  <span class="bg-green-50 text-green-600 px-2 py-1 rounded">
                    {{ fileStats.dirCount }} 目录
                  </span>
                </div>
                <button
                  v-if="!isRootDirectory"
                  @click.stop="goToParentDirectory"
                  class="p-1.5 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-full transition-colors flex items-center gap-1"
                  title="返回上级目录"
                >
                  <ChevronLeft :size="16" />
                  <span class="text-xs">返回</span>
                </button>
              </div>
            </div>

            <div v-if="filesLoading" class="p-8 flex items-center justify-center">
              <div class="text-center text-gray-500 flex flex-col items-center gap-2">
                <Loader2 class="animate-spin" />
                <span>正在加载文件列表...</span>
              </div>
            </div>

            <div v-else-if="files.length === 0" class="p-8 text-center text-slate-400">
              <FolderOpen :size="48" class="mx-auto mb-4 opacity-50" />
              <p>技能目录为空</p>
            </div>

            <div v-else class="divide-y divide-slate-100">
              <div
                v-for="file in files"
                :key="file.name"
                @click="() => handleFileClick(file)"
                class="px-6 py-4 hover:bg-slate-50 cursor-pointer transition-colors flex items-center gap-3"
                :class="{ 'bg-blue-50': selectedFile?.name === file.name }"
              >
                <File v-if="file.type === 'file'" :size="18" class="text-slate-500 flex-shrink-0" />
                <Folder v-else :size="18" class="text-slate-500 flex-shrink-0" />
                <div class="flex-1">
                  <div class="flex items-center gap-2">
                    <span class="font-medium text-slate-900">{{ file.name }}</span>
                    <span v-if="file.type === 'file' && file.size" class="text-xs text-slate-500">
                      {{ formatFileSize(file.size) }}
                    </span>
                  </div>
                </div>
                <ChevronRight v-if="file.type === 'directory'" :size="16" class="text-slate-400" />
              </div>
            </div>
          </div>

          <!-- 文件内容查看器 -->
          <div v-if="isFileSelected" class="border border-slate-200 rounded-2xl overflow-hidden">
            <div class="bg-slate-50 px-6 py-4 border-b border-slate-200 flex items-center justify-between">
              <div class="flex items-center gap-2">
                <FileText :size="20" class="text-slate-500" />
                <span class="font-medium text-slate-700">{{ selectedFile?.name }}</span>
              </div>
              <button
                @click="selectedFile = null"
                class="p-1 text-slate-400 hover:text-slate-600 rounded-full transition-colors"
              >
                <X :size="16" />
              </button>
            </div>

            <div v-if="contentLoading" class="p-8 flex items-center justify-center">
              <div class="text-center text-gray-500 flex flex-col items-center gap-2">
                <Loader2 class="animate-spin" />
                <span>正在加载文件内容...</span>
              </div>
            </div>

            <div v-else class="p-6 bg-slate-50">
              <!-- 文件内容显示 -->
              <div class="font-mono text-sm whitespace-pre-wrap overflow-x-auto max-h-[400px] overflow-y-auto">
                {{ fileContent }}
              </div>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="flex justify-end gap-3 pt-4 border-t border-slate-100">
            <button
              @click="$emit('close')"
              class="px-6 py-3 text-slate-600 font-medium hover:bg-slate-100 rounded-xl border border-slate-200"
            >
              关闭
            </button>
          </div>
        </div>

        <div v-if="error" class="p-4 bg-red-50 text-red-600 rounded-xl text-sm flex items-center gap-2 mt-6">
          <AlertCircle :size="16" />
          {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { X, Wrench, FileText, Folder, FolderOpen, ChevronRight, ChevronLeft, Loader2, Trash2, AlertCircle, File } from 'lucide-vue-next'
import AISkillsAPI from '../../services/fastApi/module_ai/ai_skills'
import { dialog } from '@/components/common/dialog'
import message from '@/components/common/message'

// 定义组件属性
const props = defineProps<{
  skillName: string
}>()

// 定义组件事件
const emit = defineEmits<{
  'close': []
  'deleted': []
}>()

// 统一的文件项接口
interface FileItem {
  name: string
  type: 'file' | 'directory'
  size?: number
}

// 路径工具类 - 统一处理所有路径操作
class PathUtils {
  // 规范化路径：移除首尾斜杠
  static normalize(path: string): string {
    return path.replace(/^\/+/, '').replace(/\/+$/, '')
  }

  // 连接多个路径部分
  static join(...parts: string[]): string {
    return parts.map(p => this.normalize(p)).filter(p => p.length > 0).join('/')
  }

  // 生成面包屑导航
  static breadcrumbs(path: string): Array<{name: string, path: string}> {
    const normalized = this.normalize(path)
    if (!normalized) return []

    const parts = normalized.split('/')
    return parts.map((part, i) => ({
      name: part,
      path: this.join(...parts.slice(0, i + 1))
    }))
  }

  // 获取父目录路径
  static parent(path: string): string {
    const normalized = this.normalize(path)
    const parts = normalized.split('/')
    parts.pop()
    return parts.length > 0 ? parts.join('/') : ''
  }

  // 检查是否为目录类型 - 支持多种数据格式
  // 检查是否为目录类型 - 简化版本
  static isDirectory(file: FileItem | null | undefined): boolean {
    return file?.type === 'directory'
  }

  // 将API返回的文件项转换为统一格式
  static normalizeFileItem(item: any): FileItem {
    console.log('[normalizeFileItem] 原始数据:', item)

    // API可能返回 {name, type, is_dir, size} 或 {name, is_dir, size}
    let type: 'file' | 'directory' = 'file'

    if (item.type) {
      // 有type字段
      const typeStr = String(item.type).toLowerCase()
      if (typeStr === 'directory' || typeStr === 'dir' || typeStr === 'folder') {
        type = 'directory'
      } else {
        type = 'file'
      }
    } else if (item.is_dir !== undefined) {
      // 有is_dir字段
      type = item.is_dir === true ? 'directory' : 'file'
    }
    // 否则默认为文件

    console.log('[normalizeFileItem] 转换结果:', { name: item.name, type, size: item.size })
    return {
      name: item.name,
      type: type,
      size: item.size
    }
  }
}

// 响应式数据
const loading = ref(true)
const error = ref('')
const filesLoading = ref(false)
const contentLoading = ref(false)
const files = ref<FileItem[]>([])
const selectedFile = ref<FileItem | null>(null)
const fileContent = ref('')
const currentPath = ref(PathUtils.normalize(props.skillName))
const apiCurrentPathRaw = ref<string>('')  // API返回的原始路径

// 计算属性
const lastUpdated = computed(() => {
  return new Date().toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
})

// 检查是否为根目录
const isRootDirectory = computed(() => {
  return PathUtils.normalize(currentPath.value) === PathUtils.normalize(props.skillName)
})

// 路径面包屑
const pathBreadcrumbs = computed(() => {
  return PathUtils.breadcrumbs(currentPath.value)
})

// 文件统计信息
const fileStats = computed(() => {
  const total = files.value.length
  const fileCount = files.value.filter(f => f.type === 'file').length
  const dirCount = files.value.filter(f => f.type === 'directory').length
  return { total, fileCount, dirCount }
})

// 检查选中的是否为文件
const isFileSelected = computed(() => {
  const isFile = selectedFile.value?.type === 'file'
  console.log('[isFileSelected] selectedFile:', selectedFile.value, 'isFile:', isFile)
  return isFile
})

// 格式化文件大小
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}


// 获取技能文件列表
const fetchSkillFiles = async () => {
  filesLoading.value = true
  const requestPath = currentPath.value
  console.log('[fetchSkillFiles] 开始请求，路径:', requestPath, '时间:', new Date().toISOString())

  try {
    const res = await AISkillsAPI.listSkillFiles(requestPath)
    console.log('[fetchSkillFiles] API响应:', res.data)
    console.log('[fetchSkillFiles] 响应状态:', res.status, '路径:', requestPath)

    // API返回结构: { current_path: string, items: Array<{ name, type, size? }> }
    const apiData = res.data?.data
    if (apiData) {
      console.log('[fetchSkillFiles] API数据:', apiData)
      console.log('[fetchSkillFiles] 返回项目数:', apiData.items?.length || 0)

      files.value = (apiData.items || []).map(PathUtils.normalizeFileItem)
      console.log('[fetchSkillFiles] 设置文件列表:', files.value)

      // 使用API返回的current_path确保路径一致
      if (apiData.current_path) {
        console.log('[fetchSkillFiles] API返回路径:', apiData.current_path, '请求路径:', requestPath)
        currentPath.value = PathUtils.normalize(apiData.current_path)
        apiCurrentPathRaw.value = apiData.current_path  // 保存原始路径
        console.log('[fetchSkillFiles] 更新后路径:', currentPath.value)
      }
    } else {
      console.warn('[fetchSkillFiles] API返回数据为空')
      files.value = []
      apiCurrentPathRaw.value = ''
    }
  } catch (err: any) {
    console.error('[fetchSkillFiles] 请求失败:', err)
    console.error('[fetchSkillFiles] 错误详情:', err.response?.data || err.message)
    error.value = err.message || '获取文件列表失败'
    message.error(error.value)
    apiCurrentPathRaw.value = ''
  } finally {
    filesLoading.value = false
    console.log('[fetchSkillFiles] 请求完成，时间:', new Date().toISOString())
  }
}

// 获取技能详情和文件列表
const fetchSkillDetail = async () => {
  loading.value = true
  error.value = ''
  selectedFile.value = null
  fileContent.value = ''

  try {
    await fetchSkillFiles()
  } catch (err: any) {
    console.error('Error fetching skill detail:', err)
    error.value = err.message || '获取技能详情失败'
    message.error(error.value)
  } finally {
    loading.value = false
  }
}

// 处理面包屑点击
const handleBreadcrumbClick = async (crumb: { name: string; path: string }, index: number) => {
  // 如果点击的是当前路径，不执行任何操作
  if (crumb.path === currentPath.value) {
    return
  }

  currentPath.value = crumb.path
  selectedFile.value = null
  fileContent.value = ''
  await fetchSkillFiles()
}

// 返回上级目录
const goToParentDirectory = async () => {
  if (isRootDirectory.value) {
    return // 已经在根目录
  }

  // 获取父目录路径
  const parentPath = PathUtils.parent(currentPath.value)
  if (!parentPath) {
    // 已经是根目录，回到技能名称
    currentPath.value = PathUtils.normalize(props.skillName)
  } else {
    currentPath.value = parentPath
  }

  selectedFile.value = null
  fileContent.value = ''
  await fetchSkillFiles()
}

// 进入目录
const enterDirectory = async (dirName: string) => {
  const newPath = PathUtils.join(currentPath.value, dirName)
  console.log('[enterDirectory] 进入目录:', dirName, '原路径:', currentPath.value, '新路径:', newPath, '时间:', new Date().toISOString())
  currentPath.value = newPath
  selectedFile.value = null
  fileContent.value = ''
  try {
    await fetchSkillFiles()
    console.log('[enterDirectory] 目录加载完成，文件数:', files.value.length)
  } catch (err) {
    console.error('[enterDirectory] 进入目录失败:', err)
    message.error('进入目录失败')
  }
}

// 选择文件并读取内容
const selectFile = async (fileName: string) => {
  console.log('[selectFile] 开始处理文件:', fileName)
  console.log('[selectFile] 当前selectedFile (之前):', selectedFile.value)

  // 设置选中的文件
  selectedFile.value = { name: fileName, type: 'file' }
  console.log('[selectFile] selectedFile设置完成 (之后):', selectedFile.value)
  console.log('[selectFile] isFileSelected应该为:', selectedFile.value?.type === 'file')

  // 确保Vue响应式更新
  await nextTick()
  console.log('[selectFile] nextTick后，检查DOM更新')

  contentLoading.value = true
  const filePath = PathUtils.join(currentPath.value, fileName)
  console.log('[selectFile] 开始读取文件:', fileName, '路径:', filePath, '时间:', new Date().toISOString())

  try {
    const res = await AISkillsAPI.readSkillFile(filePath)
    console.log('[selectFile] API响应:', res.data)
    console.log('[selectFile] 响应状态:', res.status, '完整响应:', res.data)

    // 处理API响应：现在可能返回url而不是content
    const apiData = res.data?.data
    console.log('[selectFile] API数据详情:', apiData)
    console.log('[selectFile] 检查字段:', 'content字段:', apiData?.content, 'url字段:', apiData?.url)

    // 检查是否返回了url而不是content
    if (apiData?.url) {
      console.log('[selectFile] API返回了url，开始从url获取内容:', apiData.url)
      try {
        // 从url获取文件内容
        const response = await fetch("/api/v1" + apiData.url)
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`)
        }
        const textContent = await response.text()
        console.log('[selectFile] 从url获取内容成功，长度:', textContent.length)
        fileContent.value = textContent
      } catch (fetchErr: any) {
        console.error('[selectFile] 从url获取内容失败:', fetchErr)
        message.error('从服务器获取文件内容失败')
        fileContent.value = `无法加载文件内容: ${fetchErr.message}`
      }
    } else if (apiData?.content) {
      // 向后兼容：如果API仍然返回content字段
      console.log('[selectFile] Content字段长度:', apiData.content.length || 0)
      fileContent.value = apiData.content || ''
    } else {
      console.warn('[selectFile] API没有返回content或url字段')
      fileContent.value = '文件内容为空或无法获取'
    }
  } catch (err: any) {
    console.error('[selectFile] 读取文件失败:', err)
    console.error('[selectFile] 错误详情:', err.response?.data || err.message)
    message.error('读取文件内容失败')
  } finally {
    contentLoading.value = false
    console.log('[selectFile] 请求完成，时间:', new Date().toISOString())
  }
}

// 处理文件点击
const handleFileClick = async (file: FileItem) => {
  console.log('[handleFileClick] 点击文件:', file, '完整对象:', JSON.stringify(file), '当前路径:', currentPath.value, '时间:', new Date().toISOString())
  console.log('[handleFileClick] file.type值:', file.type, '等于"file"吗?:', file.type === 'file', '等于"directory"吗?:', file.type === 'directory')

  // 直接使用类型字段
  if (file.type === 'directory') {
    console.log('[handleFileClick] 识别为目录，调用enterDirectory')
    await enterDirectory(file.name)
  } else if (file.type === 'file') {
    console.log('[handleFileClick] 识别为文件，调用selectFile', '文件名:', file.name)
    await selectFile(file.name)
  } else {
    console.error('[handleFileClick] 未知文件类型:', file.type, '完整对象:', file)
    // 尝试作为文件处理
    console.log('[handleFileClick] 尝试作为文件处理')
    await selectFile(file.name)
  }
}

// 监听 skillName 变化
watch(() => props.skillName, fetchSkillDetail)

onMounted(() => {
  fetchSkillDetail()
})
</script>
