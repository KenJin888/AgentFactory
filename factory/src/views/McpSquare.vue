<template>
  <div class="h-full flex flex-col bg-gray-50 overflow-hidden relative">
    <!-- 顶部搜索和创建按钮区域 -->
    <div class="px-8 py-6 bg-slate-50 border-b border-gray-100 flex-shrink-0">
      <div class="max-w-6xl mx-auto flex flex-col md:flex-row gap-4 items-center justify-between">
        <div class="w-full md:w-auto flex-shrink-0">
          <h1 class="text-2xl font-bold text-slate-900">工具</h1>
          <p class="mt-1 text-sm text-slate-500">管理并维护 MCP 工具服务。</p>
        </div>
        <div class="w-full md:w-auto flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-end">
          <div class="relative w-full md:w-96 group">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-blue-500" :size="20" />
            <input 
              type="text" 
              placeholder="查找工具..."
              v-model="searchQuery"
              class="w-full pl-10 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-4 focus:ring-blue-50 outline-none transition-all"
            />
          </div>
          <div  class="relative group h-11">
            <button
              @click="handleCreateClick()"
              class="h-full px-5 text-white rounded-xl font-bold shadow-lg transition-all flex items-center gap-2 active:scale-95 bg-slate-900 hover:bg-slate-800"
            >
              <Plus :size="18" />
              创建工具
              <ChevronDown :size="18" class="ml-1 -mr-1 opacity-80" />
            </button>
            <div class="absolute right-0 top-full pt-2 w-40 hidden group-hover:block z-50">
              <div class="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden py-1">
                <button
                  v-has-perm="PERMS.create"
                  class="w-full px-4 py-2.5 text-left text-slate-600 hover:bg-slate-50 hover:text-blue-600 font-medium transition-all flex items-center gap-2"
                  @click="handleCreateClick"
                >
                  <Plus :size="16" />
                  创建工具
                </button>
                <button
                  class="w-full px-4 py-2.5 text-left text-slate-600 hover:bg-slate-50 hover:text-blue-600 font-medium transition-all flex items-center gap-2"
                  @click="handleImportClick"
                >
                  <Upload :size="16" />
                  导入
                </button>
                <button
                  class="w-full px-4 py-2.5 text-left text-slate-600 hover:bg-slate-50 hover:text-blue-600 font-medium transition-all flex items-center gap-2"
                  @click="handleExportClick"
                  :disabled="exporting"
                >
                  <Loader2 v-if="exporting" class="animate-spin" :size="16" />
                  <Download v-else :size="16" />
                  导出
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分类筛选标签 (Optional, can be added later if needed) -->
    <!-- 
    <div class="px-8 pt-4 pb-2 flex-shrink-0">
      ...
    </div>
    -->

    <!-- MCP 卡片列表 -->
    <div v-if="loading" class="flex-1 flex items-center justify-center">
      <div class="text-center text-gray-500 flex flex-col items-center gap-2">
        <Loader2 class="animate-spin" />
        <span>正在加载工具列表...</span>
      </div>
    </div>
    <div v-else class="flex-1 overflow-y-auto p-8 custom-scrollbar">
      <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <McpCard 
          v-for="mcp in filteredMcps" 
          :key="mcp.id"
          :mcp="mcp"
          :onClick="() => handleMcpClick(mcp)"
          :onEdit="canUpdate ? handleEditClick : undefined"
          :onDelete="canDelete ? handleDeleteMcp : undefined"
        />
        
        <!-- 空状态 -->
        <div v-if="filteredMcps.length === 0" class="col-span-full flex flex-col items-center justify-center py-20 text-slate-400">
          <Box :size="48" class="mb-4 opacity-50" />
          <p>暂无工具数据</p>
        </div>
      </div>
    </div>

    <!-- 创建/编辑 MCP 模态框 -->
    <CreateMcpModal 
      v-if="isModalOpen"
      :initial-data="editingMcp"
      :is-admin-mode="isAdmin"
      :existing-names="existingNames"
      @close="isModalOpen = false"
      @success="handleCreateSuccess"
    />
    <ImportDialog
      :visible="importModalVisible"
      title="导入工具"
      description="请上传模板格式文件"
      accept=".xlsx,.xls,.csv"
      acceptText="支持 .xlsx, .xls, .csv 格式"
      :importing="importing"
      @update:visible="importModalVisible = $event"
      @import="handleImportUpload"
      @downloadTemplate="handleDownloadTemplate"
    />
    <ExportDialog
      :visible="exportDialogVisible"
      title="导出工具"
      :fields="exportFields"
      @update:visible="exportDialogVisible = $event"
      @confirm="handleExportConfirm"
    />
  </div>
</template>

<script setup lang="ts">
import {computed, onMounted, ref} from 'vue'
import {Box, ChevronDown, Download, Loader2, Plus, Search, Upload} from 'lucide-vue-next'
import McpCard from '../components/mcp/McpCard.vue'
import CreateMcpModal from '../components/mcp/CreateMcpModal.vue'
import ImportDialog from '@/components/common/ImportDialog.vue'
import ExportDialog, {type ExportField, type ExportOptions} from '@/components/common/ExportDialog.vue'
import AiMcpAPI, {type AiMcpTable, isBuiltinRagflowMcp} from '../services/fastApi/module_ai/ai_mcp'
import {useUserStore} from '@/stores/user'
import {dialog} from '@/components/common/dialog'
import message from '@/components/common/message'

// 用户 store
const userStore = useUserStore()

// 响应式数据
const mcps = ref<AiMcpTable[]>([])
const loading = ref(true)
const searchQuery = ref('')
const isModalOpen = ref(false)
const editingMcp = ref<AiMcpTable | null>(null)
const importModalVisible = ref(false)
const exportDialogVisible = ref(false)
const importing = ref(false)
const exporting = ref(false)

const PERMS = {
  create: 'module_ai:ai_mcp:create',
  update: 'module_ai:ai_mcp:update',
  delete: 'module_ai:ai_mcp:delete'
} as const

// 导出字段定义
const exportFields: ExportField[] = [
  { key: 'name', label: '名称', checked: true },
  { key: 'abstract', label: '摘要', checked: true },
  { key: 'type', label: '类型', checked: true },
  { key: 'category', label: '分类', checked: true },
  { key: 'config', label: '配置', checked: false },
  { key: 'tools', label: '工具', checked: false },
  { key: 'created_time', label: '创建时间', checked: true },
  { key: 'updated_time', label: '更新时间', checked: false },
]

// 用户信息 - 从 store 获取
const currentUser = computed(() => userStore.userInfo)
const isAdmin = computed(() => currentUser.value?.is_superuser || false)
const userPerms = computed(() => userStore.prems || [])
const hasWildcardPerm = computed(() => userPerms.value.includes('*:*:*'))
const hasPerm = (perm: string) => isAdmin.value || hasWildcardPerm.value || userPerms.value.includes(perm)
const canCreate = computed(() => hasPerm(PERMS.create))
const canUpdate = computed(() => hasPerm(PERMS.update))
const canDelete = computed(() => hasPerm(PERMS.delete))

// 过滤列表
const filteredMcps = computed(() => {
  return mcps.value.filter(mcp => {
    if (isBuiltinRagflowMcp(mcp)) {
      return false
    }
    const name = mcp.name || ''
    const abstract = mcp.abstract || ''
    const matchesSearch = name.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                         abstract.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesSearch
  })
})

const existingNames = computed(() => mcps.value.map(m => m.name || ''))


// 获取列表
const fetchMcps = async () => {
  loading.value = true
  try {
    const res = await AiMcpAPI.listAiMcp({
      page_no: 1,
      page_size: 100,
    })
    // 假设 API 返回结构
    mcps.value = res.data?.data?.items || []
  } catch (error) {
    console.error('Error fetching MCPs:', error)
  } finally {
    loading.value = false
  }
}

// 点击创建按钮
const handleCreateClick = () => {
  if (!canCreate.value) {
    message.warning('暂无创建权限，请联系管理员开通')
    return
  }
  editingMcp.value = null
  isModalOpen.value = true
}

const getFileNameFromHeaders = (contentDisposition?: string) => {
  if (!contentDisposition) return ''
  const utf8Match = contentDisposition.match(/filename\*=UTF-8''([^;]+)/i)
  if (utf8Match?.[1]) {
    return decodeURIComponent(utf8Match[1])
  }
  const normalMatch = contentDisposition.match(/filename="?([^"]+)"?/i)
  return normalMatch?.[1] || ''
}

const downloadBlob = (blob: Blob, fileName: string) => {
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = fileName
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  window.URL.revokeObjectURL(url)
}

const handleImportClick = () => {
  importModalVisible.value = true
}

const handleDownloadTemplate = async () => {
  try {
    const res = await AiMcpAPI.downloadTemplateAiMcp()
    const fileName =
      getFileNameFromHeaders(res.headers?.['content-disposition']) ||
      'import_template.xlsx'
    downloadBlob(res.data, fileName)
  } catch (error) {
    console.error('Download template failed:', error)
    message.error('模板下载失败')
  }
}

const handleImportUpload = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)

  importing.value = true
  try {
    const res = await AiMcpAPI.importAiMcp(formData)
    message.success(res.data?.msg || '导入成功')
    importModalVisible.value = false
    await fetchMcps()
  } catch (error) {
    console.error('Error importing MCPs:', error)
    message.error('导入失败，请重试')
  } finally {
    importing.value = false
  }
}

const handleExportClick = () => {
  exportDialogVisible.value = true
}

const handleExportConfirm = async (options: ExportOptions) => {
  exporting.value = true
  try {
    const query: any = {
      page_no: 1,
      page_size: options.range === 'all' ? 9999 : 100,
    }
    
    if (options.fields?.length) {
      query.fields = options.fields.join(',')
    }

    const res = await AiMcpAPI.exportAiMcp(query)
    const fileName =
      getFileNameFromHeaders(res.headers?.['content-disposition']) ||
      `mcp_${new Date().toISOString().slice(0, 10)}.${options.format}`
    downloadBlob(res.data, fileName)
    message.success('导出成功')
  } catch (error) {
    console.error('Error exporting MCPs:', error)
    message.error('导出失败，请重试')
  } finally {
    exporting.value = false
  }
}

// 点击编辑按钮
const handleEditClick = (mcp: AiMcpTable) => {
  editingMcp.value = mcp
  isModalOpen.value = true
}

// 点击删除按钮
const handleDeleteMcp = async (mcp: AiMcpTable) => {
  try {
    await dialog.confirm(
      mcp.name ? `确定要删除 MCP "${mcp.name}" 吗？` : '确定要删除该 MCP 吗？',
      '删除 MCP',
      { type: 'danger', confirmText: '删除', cancelText: '取消' }
    )
    
    await AiMcpAPI.deleteAiMcp([Number(mcp.id)])
    
    // 从列表中移除
    mcps.value = mcps.value.filter(m => m.id !== mcp.id)
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') {
      return
    }
    console.error('Error deleting MCP:', error)
    alert("删除失败，请重试")
  }
}

// 成功回调
const handleCreateSuccess = () => {
  fetchMcps()
  isModalOpen.value = false
}

// MCP 点击事件 (暂无具体动作，也许查看详情？)
const handleMcpClick = (mcp: AiMcpTable) => {
  if (!canUpdate.value) {
    return
  }
  console.log('Clicked MCP:', mcp)
  // 可以添加详情查看逻辑
  handleEditClick(mcp)
}

onMounted(() => {
  fetchMcps()
})
</script>
