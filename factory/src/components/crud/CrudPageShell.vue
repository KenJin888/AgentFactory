<template>
  <div class="min-h-screen bg-slate-50 p-8 overflow-y-auto">
    <div class="max-w-6xl mx-auto">
      <!-- 顶部标题区 -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">{{ title }}</h1>
          <p v-if="subtitle" class="mt-1 text-sm text-slate-500">{{ subtitle }}</p>
        </div>
        <div class="flex gap-3">
          <slot name="header-actions">
            <button
              v-if="showAddButton"
              :disabled="!canCreate"
              @click="$emit('add')"
              class="px-6 py-3 bg-slate-900 text-white rounded-xl font-bold hover:bg-slate-800 shadow-lg flex items-center gap-2 transition-transform active:scale-95 disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-slate-900"
              :title="canCreate ? addButtonText : '无权限'"
            >
              <PlusIcon :size="20" /> {{ addButtonText }}
            </button>
          </slot>
        </div>
      </div>

      <!-- 搜索筛选区 -->
      <div v-if="showSearch" class="bg-white rounded-2xl shadow-sm border border-slate-100 mb-6 overflow-hidden">
        <div class="p-6">
          <slot name="search" />
        </div>
      </div>

      <!-- 表格内容区 -->
      <CrudTableShell
        :loading="loading"
        :total="total"
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :show-pagination="showPagination"
        :current-page-data-count="currentPageDataCount"
        :min-height="tableMinHeight"
        :table-min-width="tableMinWidth"
        @page-change="$emit('pageChange', $event)"
        @size-change="$emit('sizeChange', $event)"
      >
        <template #toolbar>
          <CrudToolbar
            :selected-count="selectedCount"
            :show-batch-actions="showBatchActions"
            :batch-delete-perm="batchDeletePerm"
            :show-batch-delete="showBatchDelete"
            :batch-enable-perm="batchEnablePerm"
            :show-batch-enable="showBatchEnable"
            :batch-disable-perm="batchDisablePerm"
            :show-batch-disable="showBatchDisable"
            :show-import="showImport"
            :import-perm="importPerm"
            :show-export="showExport"
            :export-perm="exportPerm"
            :show-refresh="showRefresh"
            :refreshing="refreshing"
            :show-column-settings="showColumnSettings"
            :column-options="columnOptions"
            @batch-delete="$emit('batch-delete')"
            @batch-enable="$emit('batch-enable')"
            @batch-disable="$emit('batch-disable')"
            @import="$emit('import')"
            @export="$emit('export')"
            @refresh="$emit('refresh')"
            @column-change="(key, visible) => $emit('column-change', key, visible)"
          >
            <template #batch-actions v-if="$slots['batch-actions']">
              <slot name="batch-actions" />
            </template>
            <template #extra v-if="$slots['toolbar-extra']">
              <slot name="toolbar-extra" />
            </template>
          </CrudToolbar>
        </template>

        <template #table>
          <slot name="table" />
        </template>
      </CrudTableShell>

      <!-- 底部插槽 -->
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, toRef } from 'vue'
import { PlusIcon } from 'lucide-vue-next'
import CrudTableShell from './CrudTableShell.vue'
import CrudToolbar, { type ColumnOption } from './CrudToolbar.vue'
import { useCrudAuth } from '@/composables/useCrudAuth'

interface Props {
  // 页面标题
  title: string
  // 副标题
  subtitle?: string
  // 加载状态
  loading?: boolean
  // 数据总数
  total?: number
  // 当前页
  currentPage?: number
  // 每页条数
  pageSize?: number
  // 当前页数据条数
  currentPageDataCount?: number
  // 是否显示分页
  showPagination?: boolean
  // 是否显示搜索区
  showSearch?: boolean
  // 是否显示新增按钮
  showAddButton?: boolean
  // 新增按钮文本
  addButtonText?: string
  // 新增权限
  createPerm?: string
  // 选中数量
  selectedCount?: number
  // 是否显示批量操作
  showBatchActions?: boolean
  // 批量删除权限
  batchDeletePerm?: string
  // 是否显示批量删除
  showBatchDelete?: boolean
  // 批量启用权限
  batchEnablePerm?: string
  // 是否显示批量启用
  showBatchEnable?: boolean
  // 批量停用权限
  batchDisablePerm?: string
  // 是否显示批量停用
  showBatchDisable?: boolean
  // 是否显示导入
  showImport?: boolean
  // 导入权限
  importPerm?: string
  // 是否显示导出
  showExport?: boolean
  // 导出权限
  exportPerm?: string
  // 是否显示刷新
  showRefresh?: boolean
  // 刷新中状态
  refreshing?: boolean
  // 是否显示列设置
  showColumnSettings?: boolean
  // 列选项
  columnOptions?: ColumnOption[]
  // 表格最小高度
  tableMinHeight?: number
  // 表格最小宽度
  tableMinWidth?: string
}

const props = withDefaults(defineProps<Props>(), {
  subtitle: '',
  loading: false,
  total: 0,
  currentPage: 1,
  pageSize: 10,
  currentPageDataCount: 0,
  showPagination: true,
  showSearch: true,
  showAddButton: true,
  addButtonText: '新增',
  createPerm: '',
  selectedCount: 0,
  showBatchActions: true,
  batchDeletePerm: '',
  showBatchDelete: true,
  batchEnablePerm: '',
  showBatchEnable: true,
  batchDisablePerm: '',
  showBatchDisable: true,
  showImport: false,
  importPerm: '',
  showExport: false,
  exportPerm: '',
  showRefresh: true,
  refreshing: false,
  showColumnSettings: false,
  columnOptions: () => [],
  tableMinHeight: 200,
  tableMinWidth: '1600px'
})

const emit = defineEmits<{
  'update:currentPage': [page: number]
  'update:pageSize': [size: number]
  'add': []
  'batch-delete': []
  'batch-enable': []
  'batch-disable': []
  'import': []
  'export': []
  'refresh': []
  'column-change': [key: string, visible: boolean]
  'pageChange': [page: number]
  'sizeChange': [size: number]
}>()

// 使用 useCrudAuth 判断新增权限 - 使用 toRef 确保响应式
const createAuth = useCrudAuth(toRef(() => ({ create: props.createPerm })))
const canCreate = computed(() => createAuth.canCreate.value)

const currentPage = computed({
  get: () => props.currentPage,
  set: (val) => emit('update:currentPage', val)
})

const pageSize = computed({
  get: () => props.pageSize,
  set: (val) => emit('update:pageSize', val)
})
</script>
