<template>
  <CrudPageShell
    title="公告管理"
    subtitle="维护系统的公告信息。"
    :loading="loading"
    :total="total"
    v-model:current-page="currentPage"
    v-model:page-size="pageSize"
    :selected-count="selectedIds.length"
    :show-export="true"
    :export-perm="PERMS.export"
    :show-refresh="true"
    :refreshing="loading"
    :show-column-settings="true"
    :column-options="columnOptions"
    :show-batch-actions="true"
    :show-batch-delete="true"
    :batch-delete-perm="PERMS.delete"
    :show-batch-enable="true"
    :batch-enable-perm="PERMS.update"
    :show-batch-disable="true"
    :batch-disable-perm="PERMS.update"
    add-button-text="新增公告"
    :create-perm="PERMS.create"
    @add="handleCreate"
    @export="handleExport"
    @refresh="handleRefresh"
    @column-change="handleColumnChange"
    @batch-delete="handleBatchDelete"
    @batch-enable="handleBatchEnable"
    @batch-disable="handleBatchDisable"
  >
    <!-- 搜索区 -->
    <template #search>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <!-- 标题 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">标题</label>
          <div class="relative">
            <input
              v-model="queryParams.notice_title"
              type="text"
              placeholder="请输入标题"
              class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
              @keyup.enter="handleSearch"
            />
            <TypeIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          </div>
        </div>
        <!-- 公告类型 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">公告类型</label>
          <select
            v-model="queryParams.notice_type"
            class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all appearance-none cursor-pointer"
          >
            <option value="">全部</option>
            <option value="1">通知</option>
            <option value="2">公告</option>
          </select>
        </div>
        <!-- 状态 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">状态</label>
          <select
            v-model="queryParams.status"
            class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all appearance-none cursor-pointer"
          >
            <option value="">全部</option>
            <option value="1">正常</option>
            <option value="0">停用</option>
          </select>
        </div>
        <!-- 操作按钮列 -->
        <div class="flex items-end">
          <div class="flex items-center gap-2">
            <button
              @click="handleSearch"
              class="bg-slate-900 text-white px-6 py-2.5 rounded-xl hover:bg-slate-800 transition-all shadow-sm hover:shadow flex items-center justify-center gap-2 whitespace-nowrap"
            >
              <SearchIcon class="w-4 h-4" />
              查询
            </button>
            <button
              @click="handleReset"
              class="bg-white text-slate-600 border border-slate-200 px-6 py-2.5 rounded-xl hover:bg-slate-50 hover:border-slate-300 transition-all whitespace-nowrap"
            >
              重置
            </button>
            <button
              @click="isExpand = !isExpand"
              class="px-3 py-2.5 text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-xl transition-all flex items-center justify-center gap-1 flex-shrink-0"
              :title="isExpand ? '收起筛选' : '展开筛选'"
            >
              <ChevronUpIcon v-if="isExpand" class="w-4 h-4" />
              <ChevronDownIcon v-else class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      <!-- 展开的搜索条件 -->
      <div v-if="isExpand" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mt-5 pt-5 border-t border-slate-100">
        <!-- 创建人 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">创建人</label>
          <div class="flex items-center gap-2">
            <div class="relative flex-1">
              <input
                v-model="createdByName"
                type="text"
                placeholder="点击选择创建人"
                readonly
                @click="showUserSelector = true"
                class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 cursor-pointer transition-all"
              />
              <UserIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            </div>
            <button
              v-if="queryParams.created_id"
              @click="queryParams.created_id = undefined; createdByName = ''"
              class="p-2.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all"
            >
              <XIcon class="w-4 h-4" />
            </button>
          </div>
        </div>
        <!-- 创建时间 -->
        <div class="md:col-span-2">
          <label class="block text-sm font-medium text-slate-700 mb-2">创建时间</label>
          <div class="flex items-center gap-3">
            <input
              v-model="startTime"
              type="date"
              class="flex-1 px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
            />
            <span class="text-slate-400">至</span>
            <input
              v-model="endTime"
              type="date"
              class="flex-1 px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
            />
          </div>
        </div>
      </div>
    </template>

    <!-- 表格区 -->
    <template #table>
      <table class="w-full text-sm" style="min-width: 1200px;">
        <thead class="bg-slate-50 text-slate-600 font-medium border-b border-slate-200">
          <tr>
            <th class="px-5 py-4 w-12 text-center">
              <input type="checkbox" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" @change="toggleAllSelection" :checked="isAllSelected" />
            </th>
            <th v-if="getColumnVisible('index')" class="px-5 py-4 text-center">序号</th>
            <th v-if="getColumnVisible('title')" class="px-5 py-4 text-center">标题</th>
            <th v-if="getColumnVisible('type')" class="px-5 py-4 text-center">公告类型</th>
            <th v-if="getColumnVisible('content')" class="px-5 py-4 text-center">内容</th>
            <th v-if="getColumnVisible('status')" class="px-5 py-4 text-center">状态</th>
            <th v-if="getColumnVisible('created_time')" class="px-5 py-4 text-center">创建时间</th>
            <th v-if="getColumnVisible('created_by')" class="px-5 py-4 text-center">创建人</th>
            <th v-if="getColumnVisible('action')" class="px-5 py-4 text-center fixed-col">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-if="loading" class="animate-pulse">
            <td :colspan="visibleColumnCount" class="px-6 py-12 text-center text-slate-400">
              <div class="flex flex-col items-center gap-3">
                <Loader2Icon class="w-8 h-8 animate-spin text-blue-500" />
                <span>加载中...</span>
              </div>
            </td>
          </tr>
          <tr v-else-if="dataList.length === 0">
            <td :colspan="visibleColumnCount" class="px-6 py-12 text-center text-slate-400">
              <div class="flex flex-col items-center gap-3">
                <InboxIcon class="w-12 h-12 text-slate-300" />
                <span>暂无数据</span>
              </div>
            </td>
          </tr>
          <tr v-else v-for="notice in dataList" :key="notice.id" class="hover:bg-slate-50/80 transition-colors group">
            <td class="px-5 py-4 text-center">
              <input type="checkbox" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" :value="notice.id" v-model="selectedIds" />
            </td>
            <td v-if="getColumnVisible('index')" class="px-5 py-4 text-center text-slate-500">
              {{ (currentPage - 1) * pageSize + dataList.indexOf(notice) + 1 }}
            </td>
            <td v-if="getColumnVisible('title')" class="px-5 py-4 text-center">
              <div class="max-w-[200px] truncate font-medium text-slate-900" :title="notice.notice_title">{{ notice.notice_title || '-' }}</div>
            </td>
            <td v-if="getColumnVisible('type')" class="px-5 py-4 text-center">
              <span
                class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                :class="notice.notice_type === '1' ? 'bg-blue-50 text-blue-700 border border-blue-200' : 'bg-purple-50 text-purple-700 border border-purple-200'"
              >
                {{ notice.notice_type === '1' ? '通知' : '公告' }}
              </span>
            </td>
            <td v-if="getColumnVisible('content')" class="px-5 py-4 text-center">
              <div class="max-w-[300px] truncate text-slate-600" :title="stripHtml(notice.notice_content)">{{ stripHtml(notice.notice_content) || '-' }}</div>
            </td>
            <td v-if="getColumnVisible('status')" class="px-5 py-4 text-center">
              <span
                class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                :class="notice.status === '1' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-600 border border-slate-200'"
              >
                {{ notice.status === '1' ? '正常' : '停用' }}
              </span>
            </td>
            <td v-if="getColumnVisible('created_time')" class="px-5 py-4 text-center text-slate-500 whitespace-nowrap text-xs">
              {{ formatDate(notice.created_time) }}
            </td>
            <td v-if="getColumnVisible('created_by')" class="px-5 py-4 text-center text-slate-600">{{ notice.created_by?.name || '-' }}</td>
            <td v-if="getColumnVisible('action')" class="px-5 py-4 text-center fixed-col">
              <div class="flex items-center justify-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  :disabled="!canDetail"
                  @click="handleView(notice)"
                  class="p-2 text-slate-800 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-transparent disabled:hover:text-slate-800"
                  :title="canDetail ? '详情' : '无权限'"
                >
                  <EyeIcon class="w-4 h-4" />
                </button>
                <button
                  :disabled="!canUpdate"
                  @click="handleEdit(notice)"
                  class="p-2 text-slate-800 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-transparent disabled:hover:text-slate-800"
                  :title="canUpdate ? '编辑' : '无权限'"
                >
                  <PencilIcon class="w-4 h-4" />
                </button>
                <button
                  :disabled="!canDelete"
                  @click="handleDelete(notice)"
                  class="p-2 text-slate-800 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-transparent disabled:hover:text-slate-800"
                  :title="canDelete ? '删除' : '无权限'"
                >
                  <TrashIcon class="w-4 h-4" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </template>
  </CrudPageShell>

  <!-- User Selector Dialog -->
  <UserSelector
    v-model:visible="showUserSelector"
    title="选择创建人"
    :multiple="false"
    :initial-selected="selectedUserForSelector"
    @confirm="handleUserSelect"
  />

  <!-- Export Dialog -->
  <ExportDialog
    v-model:visible="showExportDialog"
    title="导出公告"
    :fields="exportFields"
    :selected-count="selectedIds.length"
    @confirm="handleExportConfirm"
  />

  <!-- View Modal (Readonly) -->
  <div v-if="viewDialogVisible" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-3xl max-h-[90vh] overflow-hidden flex flex-col">
      <div class="px-6 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
        <h2 class="text-xl font-bold text-slate-900">公告详情</h2>
        <button @click="closeViewDialog" class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all">
          <XIcon class="w-5 h-5" />
        </button>
      </div>

      <div class="flex-1 overflow-y-auto p-6">
        <div class="space-y-5">
          <div class="grid grid-cols-2 gap-5">
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">标题</div>
              <div class="font-medium text-slate-900">{{ viewData.notice_title || '-' }}</div>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">公告类型</div>
              <span
                class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                :class="viewData.notice_type === '1' ? 'bg-blue-50 text-blue-700 border border-blue-200' : 'bg-purple-50 text-purple-700 border border-purple-200'"
              >
                {{ viewData.notice_type === '1' ? '通知' : '公告' }}
              </span>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-5">
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">状态</div>
              <span
                class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                :class="viewData.status === '1' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-600 border border-slate-200'"
              >
                {{ viewData.status === '1' ? '正常' : '停用' }}
              </span>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">创建人</div>
              <div class="font-medium text-slate-900">{{ viewData.created_by?.name || '-' }}</div>
            </div>
          </div>

          <div class="p-4 bg-slate-50 rounded-xl">
            <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">描述</div>
            <div class="font-medium text-slate-900">{{ (viewData as any).description || '-' }}</div>
          </div>

          <div class="p-4 bg-slate-50 rounded-xl">
            <div class="text-xs text-slate-500 mb-2 uppercase tracking-wide">内容</div>
            <div class="bg-white border border-slate-200 rounded-xl p-4 prose prose-sm max-w-none" v-html="viewData.notice_content || '<p class=\'text-slate-400\'>无内容</p>'"></div>
          </div>

          <div class="grid grid-cols-2 gap-5">
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">创建时间</div>
              <div class="font-medium text-slate-900">{{ formatDate(viewData.created_time) }}</div>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">更新时间</div>
              <div class="font-medium text-slate-900">{{ formatDate(viewData.updated_time) }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="px-6 py-4 border-t border-slate-100 flex justify-end gap-3 bg-slate-50/30">
        <button
          @click="closeViewDialog"
          class="px-5 py-2.5 bg-slate-900 text-white rounded-xl hover:bg-slate-800 transition-all shadow-sm"
        >
          确定
        </button>
      </div>
    </div>
  </div>

  <!-- Create/Edit Modal -->
  <div v-if="dialogVisible" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col">
      <div class="px-6 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
        <h2 class="text-xl font-bold text-slate-900">{{ isEdit ? '编辑公告' : '新增公告' }}</h2>
        <button @click="closeDialog" class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all">
          <XIcon class="w-5 h-5" />
        </button>
      </div>

      <div class="flex-1 overflow-y-auto p-6">
        <div class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">标题 <span class="text-red-500">*</span></label>
            <input
              v-model="formData.notice_title"
              type="text"
              placeholder="请输入标题"
              class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
            />
          </div>

          <div class="grid grid-cols-2 gap-5">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">公告类型 <span class="text-red-500">*</span></label>
              <select
                v-model="formData.notice_type"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all appearance-none cursor-pointer"
              >
                <option value="1">通知</option>
                <option value="2">公告</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">状态 <span class="text-red-500">*</span></label>
              <select
                v-model="formData.status"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all appearance-none cursor-pointer"
              >
                <option value="1">正常</option>
                <option value="0">停用</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">描述</label>
            <textarea
              v-model="formData.description"
              rows="3"
              placeholder="请输入描述"
              class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all resize-none"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">内容 <span class="text-red-500">*</span></label>
            <RichEditor
              v-model="formData.notice_content"
              height="300px"
              placeholder="请输入公告内容..."
            />
          </div>
        </div>
      </div>

      <div class="px-6 py-4 border-t border-slate-100 flex justify-end gap-3 bg-slate-50/30">
        <button
          @click="closeDialog"
          class="px-5 py-2.5 bg-white text-slate-600 border border-slate-200 rounded-xl hover:bg-slate-50 transition-all"
        >
          取消
        </button>
        <button
          @click="handleSubmit"
          class="px-5 py-2.5 bg-slate-900 text-white rounded-xl hover:bg-slate-800 transition-all shadow-sm"
        >
          确定
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import type { ExportOptions } from '@/components/common/ExportDialog.vue'
import ExportDialog from '@/components/common/ExportDialog.vue'
import UserSelector from '@/components/common/UserSelector.vue'
import RichEditor from '@/components/common/RichEditor.vue'
import { CrudPageShell } from '@/components/crud'
import { useCrudPage } from '@/composables/useCrudPage'
import { useCrudAuth } from '@/composables/useCrudAuth'
import {
  ChevronDown as ChevronDownIcon,
  ChevronUp as ChevronUpIcon,
  Eye as EyeIcon,
  Inbox as InboxIcon,
  Loader2 as Loader2Icon,
  Pencil as PencilIcon,
  Search as SearchIcon,
  TrashIcon,
  Type as TypeIcon,
  User as UserIcon,
  X as XIcon,
} from 'lucide-vue-next'
import { api } from '@/services/api'
import message from '@/components/common/message'
import { dialog } from '@/components/common/dialog'
import type { NoticeForm, NoticePageQuery, NoticeTable } from '@/services/fastApi/module_system/notice'
import type { User } from '@/types/user'

// 权限配置
const PERMS = {
  query: 'module_system:notice:query',
  create: 'module_system:notice:create',
  update: 'module_system:notice:update',
  delete: 'module_system:notice:delete',
  export: 'module_system:notice:export',
  detail: 'module_system:notice:detail',
} as const

// 使用 useCrudAuth 判断行内按钮权限
const detailAuth = useCrudAuth({ detail: PERMS.detail })
const updateAuth = useCrudAuth({ update: PERMS.update })
const deleteAuth = useCrudAuth({ delete: PERMS.delete })

const canDetail = computed(() => detailAuth.can('detail'))
const canUpdate = computed(() => updateAuth.can('update'))
const canDelete = computed(() => deleteAuth.can('delete'))

// 使用 CRUD Page composable
const {
  loading,
  currentPage,
  pageSize,
  total,
  queryParams,
  dataList,
  selectedIds,
  fetchData,
  handleSearch,
  handleReset,
  handleRefresh,
} = useCrudPage<NoticeTable, NoticePageQuery>({
  initialQuery: {
    page_no: 1,
    page_size: 10,
    notice_type: '',
    notice_title: '',
    status: '',
    created_id: undefined,
  },
  fetchList: async (params) => {
    const res = await api.notice.listNotice(params)
    return {
      items: res?.data?.items || [],
      total: res?.data?.total || 0,
    }
  },
})

// 其他状态
const isExpand = ref(false)
const dialogVisible = ref(false)
const viewDialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref<number | null>(null)
const viewData = ref<NoticeTable>({} as NoticeTable)

// User selector
const startTime = ref('')
const endTime = ref('')
const createdByName = ref('')
const showUserSelector = ref(false)
const showExportDialog = ref(false)

interface ExportField {
  key: string
  label: string
  checked: boolean
}

const exportFields = ref<ExportField[]>([
  { key: 'title', label: '标题', checked: true },
  { key: 'type', label: '公告类型', checked: true },
  { key: 'content', label: '内容', checked: true },
  { key: 'status', label: '状态', checked: true },
  { key: 'created_time', label: '创建时间', checked: true },
  { key: 'updated_time', label: '更新时间', checked: false },
  { key: 'created_by', label: '创建人', checked: false },
])

const columnOptions = ref([
  { key: 'index', label: '序号', visible: true },
  { key: 'title', label: '标题', visible: true },
  { key: 'type', label: '公告类型', visible: true },
  { key: 'content', label: '内容', visible: true },
  { key: 'status', label: '状态', visible: true },
  { key: 'created_time', label: '创建时间', visible: true },
  { key: 'created_by', label: '创建人', visible: false },
  { key: 'action', label: '操作', visible: true },
])

const getColumnVisible = (key: string) => {
  const col = columnOptions.value.find((c) => c.key === key)
  return col ? col.visible : true
}

const handleColumnChange = (key: string, visible: boolean) => {
  const col = columnOptions.value.find((c) => c.key === key)
  if (col) {
    col.visible = visible
  }
}

const visibleColumnCount = computed(() => {
  return columnOptions.value.filter((c) => c.visible).length + 1
})

const isAllSelected = computed(() => {
  return dataList.value.length > 0 && dataList.value.every((n) => selectedIds.value.includes(n.id!))
})

const toggleAllSelection = (e: Event) => {
  const checked = (e.target as HTMLInputElement).checked
  if (checked) {
    selectedIds.value = dataList.value.map((n) => n.id!).filter((id) => id !== undefined)
  } else {
    selectedIds.value = []
  }
}

const selectedUserForSelector = computed(() => {
  if (!queryParams.created_id) return []
  return [{ id: queryParams.created_id, name: createdByName.value }] as User[]
})

const handleUserSelect = (users: User[]) => {
  if (users.length > 0) {
    const user = users[0]
    queryParams.created_id = user.id
    createdByName.value = user.name
  } else {
    queryParams.created_id = undefined
    createdByName.value = ''
  }
  showUserSelector.value = false
}

const formatDate = (dateStr?: string) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString()
}

// 去除HTML标签，返回纯文本
const stripHtml = (html?: string) => {
  if (!html) return ''
  const tmp = document.createElement('div')
  tmp.innerHTML = html
  return tmp.textContent || tmp.innerText || ''
}

const formData = reactive<NoticeForm & { description?: string }>({
  notice_title: '',
  notice_type: '1',
  notice_content: '',
  status: '1',
  description: '',
})

// Methods
const handleExport = () => {
  showExportDialog.value = true
}

const handleExportConfirm = async (options: ExportOptions) => {
  try {
    const selectedFieldKeys = options.fields
    if (selectedFieldKeys.length === 0) {
      message.warning('请至少选择一个导出字段')
      return
    }

    const selectedFields = exportFields.value.filter((f: ExportField) => selectedFieldKeys.includes(f.key))

    message.info('正在导出，请稍候...')

    let allData: NoticeTable[] = []

    if (options.range === 'selected' && selectedIds.value.length > 0) {
      allData = dataList.value.filter((n) => selectedIds.value.includes(n.id!))
    } else if (options.range === 'current') {
      allData = [...dataList.value]
    } else {
      const exportParams: NoticePageQuery = {
        page_no: 1,
        page_size: 10000,
      }
      if (queryParams.notice_type) exportParams.notice_type = queryParams.notice_type
      if (queryParams.notice_title) exportParams.notice_title = queryParams.notice_title
      if (queryParams.status) exportParams.status = queryParams.status

      const res = await api.notice.listNotice(exportParams)
      if (res?.data?.items) {
        allData = res.data.items
      }
    }

    const headers = selectedFields.map((f: ExportField) => f.label)
    const keys = selectedFieldKeys
    const timeFields = ['created_time', 'updated_time']

    if (options.format === 'csv') {
      const csvContent = [
        headers.join(','),
        ...allData.map((row: NoticeTable) =>
          keys
            .map((key: string) => {
              let value = (row as any)[key]
              if (key === 'type') {
                value = value === '1' ? '通知' : '公告'
              } else if (key === 'status') {
                value = value === '1' ? '正常' : '停用'
              } else if (key === 'created_by' || key === 'updated_by') {
                value = value?.name || ''
              } else {
                if (value === null || value === undefined) value = ''
                value = String(value)
              }
              if (timeFields.includes(key) && value) {
                value = ' ' + value
              }
              if (value.includes(',') || value.includes('"') || value.includes('\n')) {
                value = `"${value.replace(/"/g, '""')}"`
              }
              return value
            })
            .join(',')
        ),
      ].join('\n')

      const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `公告列表_${new Date().toISOString().slice(0, 10)}.csv`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } else {
      try {
        const XLSX = await import('xlsx')
        const exportData = allData.map((row: NoticeTable) => {
          const obj: any = {}
          keys.forEach((key: string, index: number) => {
            let value = (row as any)[key]
            if (key === 'type') {
              value = value === '1' ? '通知' : '公告'
            } else if (key === 'status') {
              value = value === '1' ? '正常' : '停用'
            } else if (key === 'created_by' || key === 'updated_by') {
              value = value?.name || ''
            }
            obj[headers[index]] = value
          })
          return obj
        })

        const ws = XLSX.utils.json_to_sheet(exportData)
        const wb = XLSX.utils.book_new()
        XLSX.utils.book_append_sheet(wb, ws, '公告列表')
        XLSX.writeFile(wb, `公告列表_${new Date().toISOString().slice(0, 10)}.xlsx`)
      } catch (xlsxError) {
        message.error('Excel 导出失败，请确保已安装 xlsx 库')
        console.error('XLSX export failed:', xlsxError)
        return
      }
    }

    message.success('导出成功')
  } catch (error) {
    console.error('Export failed:', error)
    message.error('导出失败')
  }
}

const handleCreate = () => {
  isEdit.value = false
  editId.value = null
  formData.notice_title = ''
  formData.notice_type = '1'
  formData.notice_content = ''
  formData.status = '1'
  formData.description = ''
  dialogVisible.value = true
}

const handleEdit = (notice: NoticeTable) => {
  isEdit.value = true
  editId.value = notice.id || null
  formData.notice_title = notice.notice_title || ''
  formData.notice_type = notice.notice_type || '1'
  formData.notice_content = notice.notice_content || ''
  formData.status = notice.status || '1'
  formData.description = (notice as any).description || ''
  dialogVisible.value = true
}

const handleView = (notice: NoticeTable) => {
  viewData.value = { ...notice }
  viewDialogVisible.value = true
}

const closeViewDialog = () => {
  viewDialogVisible.value = false
  viewData.value = {} as NoticeTable
}

const closeDialog = () => {
  dialogVisible.value = false
  isEdit.value = false
  editId.value = null
}

const handleSubmit = async () => {
  if (!formData.notice_title?.trim()) {
    message.warning('请输入标题')
    return
  }
  if (!formData.notice_content?.trim()) {
    message.warning('请输入内容')
    return
  }

  try {
    if (isEdit.value && editId.value) {
      await api.notice.updateNotice(editId.value, formData)
      message.success('更新成功')
    } else {
      await api.notice.createNotice(formData)
      message.success('创建成功')
    }
    closeDialog()
    fetchData()
  } catch (error) {
    console.error('Submit failed:', error)
    message.error(isEdit.value ? '更新失败' : '创建失败')
  }
}

const handleDelete = async (notice: NoticeTable) => {
  try {
    await dialog.confirm(`确定要删除该公告吗？`)
    if (notice.id) {
      await api.notice.deleteNotice([notice.id])
      fetchData()
      message.success('删除成功')
    }
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error('Delete failed:', error)
    message.error('删除失败')
  }
}

const handleBatchDelete = async () => {
  if (selectedIds.value.length === 0) return

  try {
    await dialog.confirm(`确定要删除选中的 ${selectedIds.value.length} 条公告吗？`)
    await api.notice.deleteNotice(selectedIds.value as number[])
    selectedIds.value = []
    fetchData()
    message.success('批量删除成功')
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error('Batch delete failed:', error)
    message.error('批量删除失败')
  }
}

const handleBatchEnable = async () => {
  if (selectedIds.value.length === 0) return

  try {
    await dialog.confirm(`确定要启用选中的 ${selectedIds.value.length} 条公告吗？`)
    const updatePromises = (selectedIds.value as number[]).map((id) => {
      const notice = dataList.value.find((n) => n.id === id)
      if (notice) {
        return api.notice.updateNotice(id, {
          ...notice,
          status: '1',
        } as NoticeForm)
      }
      return Promise.resolve()
    })

    const results = await Promise.allSettled(updatePromises)
    const failedCount = results.filter((r) => r.status === 'rejected').length

    selectedIds.value = []
    fetchData()

    if (failedCount > 0) {
      message.warning(`批量启用完成，${failedCount} 条失败`)
    } else {
      message.success('批量启用成功')
    }
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error('Batch enable failed:', error)
    message.error('批量启用失败')
  }
}

const handleBatchDisable = async () => {
  if (selectedIds.value.length === 0) return

  try {
    await dialog.confirm(`确定要停用选中的 ${selectedIds.value.length} 条公告吗？`)
    const updatePromises = (selectedIds.value as number[]).map((id) => {
      const notice = dataList.value.find((n) => n.id === id)
      if (notice) {
        return api.notice.updateNotice(id, {
          ...notice,
          status: '0',
        } as NoticeForm)
      }
      return Promise.resolve()
    })

    const results = await Promise.allSettled(updatePromises)
    const failedCount = results.filter((r) => r.status === 'rejected').length

    selectedIds.value = []
    fetchData()

    if (failedCount > 0) {
      message.warning(`批量停用完成，${failedCount} 条失败`)
    } else {
      message.success('批量停用成功')
    }
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error('Batch disable failed:', error)
    message.error('批量停用失败')
  }
}

// 初始化
fetchData()
</script>

<style scoped>
.fixed-col {
  position: sticky;
  right: 0;
  background-color: white;
  z-index: 1;
}
table thead .fixed-col {
  background-color: #f8fafc;
  z-index: 2;
}
</style>
