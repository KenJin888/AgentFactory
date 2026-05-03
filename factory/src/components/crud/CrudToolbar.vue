<template>
  <div class="flex items-center justify-between w-full">
    <!-- 左侧：批量操作区 -->
    <div class="flex items-center gap-3">
      <div class="flex items-center gap-3 text-sm">
        <span class="text-slate-500">已选择</span>
        <span class="font-semibold text-slate-900 bg-blue-50 px-2.5 py-0.5 rounded-full">{{ selectedCount }}</span>
        <span class="text-slate-500">项</span>
      </div>
      <!-- 批量操作按钮 -->
      <div v-if="selectedCount > 0 && showBatchActions" class="flex items-center gap-1 ml-4 pl-4 border-l border-slate-200">
        <slot name="batch-actions">
          <button
            v-if="showBatchDelete"
            :disabled="!canBatchDelete"
            @click="$emit('batch-delete')"
            class="p-2 text-slate-700 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-transparent disabled:hover:text-slate-700"
            :title="canBatchDelete ? '批量删除' : '无权限'"
          >
            <TrashIcon class="w-4 h-4" />
          </button>
          <button
            v-if="showBatchEnable"
            :disabled="!canBatchEnable"
            @click="$emit('batch-enable')"
            class="p-2 text-slate-700 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg transition-all disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-transparent disabled:hover:text-slate-700"
            :title="canBatchEnable ? '批量启用' : '无权限'"
          >
            <PlayIcon class="w-4 h-4" />
          </button>
          <button
            v-if="showBatchDisable"
            :disabled="!canBatchDisable"
            @click="$emit('batch-disable')"
            class="p-2 text-slate-700 hover:text-amber-600 hover:bg-amber-50 rounded-lg transition-all disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-transparent disabled:hover:text-slate-700"
            :title="canBatchDisable ? '批量停用' : '无权限'"
          >
            <PauseIcon class="w-4 h-4" />
          </button>
        </slot>
      </div>
    </div>

    <!-- 右侧：功能按钮区 -->
    <div class="flex items-center gap-2">
      <!-- 导入按钮 -->
      <button
        v-if="showImport"
        :disabled="!canImport"
        @click="$emit('import')"
        class="p-2.5 text-slate-600 hover:bg-slate-100 rounded-xl transition-all disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-transparent"
        :title="canImport ? '导入' : '无权限'"
      >
        <UploadIcon class="w-5 h-5" />
      </button>

      <!-- 导出按钮 -->
      <button
        v-if="showExport"
        :disabled="!canExport"
        @click="$emit('export')"
        class="p-2.5 text-slate-600 hover:bg-slate-100 rounded-xl transition-all disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-transparent"
        :title="canExport ? '导出' : '无权限'"
      >
        <DownloadIcon class="w-5 h-5" />
      </button>

      <!-- 刷新按钮 -->
      <button
        v-if="showRefresh"
        @click="$emit('refresh')"
        class="p-2.5 text-slate-600 hover:bg-slate-100 rounded-xl transition-all"
        title="刷新"
        :disabled="refreshing"
      >
        <RefreshCwIcon class="w-5 h-5" :class="{ 'animate-spin': refreshing }" />
      </button>

      <!-- 列设置按钮 -->
      <div v-if="showColumnSettings" class="relative" ref="columnSettingsRef">
        <button
          @click.stop="toggleColumnSettings"
          class="p-2.5 text-slate-600 hover:bg-slate-100 rounded-xl transition-all"
          title="列设置"
        >
          <SettingsIcon class="w-5 h-5" />
        </button>
        <div
          v-if="showColumnDropdown"
          ref="columnSettingsDropdownRef"
          class="fixed bg-white border border-slate-200 rounded-xl shadow-xl z-50 p-4 min-w-[180px]"
          :style="{ top: dropdownPosition.top + 'px', right: dropdownPosition.right + 'px' }"
          @click.stop
        >
          <div class="text-sm font-semibold text-slate-800 mb-3">列展示</div>
          <div class="space-y-2 max-h-48 overflow-y-auto">
            <label
              v-for="col in columnOptions"
              :key="col.key"
              class="flex items-center gap-3 cursor-pointer p-1.5 rounded-lg hover:bg-slate-50 transition-colors"
            >
              <input
                type="checkbox"
                v-model="col.visible"
                class="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                @change="$emit('column-change', col.key, col.visible)"
              />
              <span class="text-sm text-slate-600">{{ col.label }}</span>
            </label>
          </div>
        </div>
      </div>

      <!-- 额外插槽 -->
      <slot name="extra" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, toRef } from 'vue'
import {
  TrashIcon,
  PlayIcon,
  PauseIcon,
  UploadIcon,
  DownloadIcon,
  RefreshCwIcon,
  SettingsIcon
} from 'lucide-vue-next'
import { useCrudAuth } from '@/composables/useCrudAuth'

export interface ColumnOption {
  key: string
  label: string
  visible: boolean
}

interface Props {
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
}

const props = withDefaults(defineProps<Props>(), {
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
  columnOptions: () => []
})

const emit = defineEmits<{
  'batch-delete': []
  'batch-enable': []
  'batch-disable': []
  'import': []
  'export': []
  'refresh': []
  'column-change': [key: string, visible: boolean]
}>()

// 使用 useCrudAuth 判断权限 - 使用 toRef 确保响应式
const batchDeleteAuth = useCrudAuth(toRef(() => ({ delete: props.batchDeletePerm })))
const batchEnableAuth = useCrudAuth(toRef(() => ({ update: props.batchEnablePerm })))
const batchDisableAuth = useCrudAuth(toRef(() => ({ update: props.batchDisablePerm })))
const importAuth = useCrudAuth(toRef(() => ({ import: props.importPerm })))
const exportAuth = useCrudAuth(toRef(() => ({ export: props.exportPerm })))

// 计算权限
const canBatchDelete = computed(() => batchDeleteAuth.canDelete.value)
const canBatchEnable = computed(() => batchEnableAuth.canUpdate.value)
const canBatchDisable = computed(() => batchDisableAuth.canUpdate.value)
const canImport = computed(() => importAuth.canImport.value)
const canExport = computed(() => exportAuth.canExport.value)

// 列设置下拉框
const showColumnDropdown = ref(false)
const columnSettingsRef = ref<HTMLElement | null>(null)
const columnSettingsDropdownRef = ref<HTMLElement | null>(null)
const dropdownPosition = ref({ top: 0, right: 0 })

const updateDropdownPosition = () => {
  if (columnSettingsRef.value) {
    const rect = columnSettingsRef.value.getBoundingClientRect()
    dropdownPosition.value = {
      top: rect.bottom + 8,
      right: window.innerWidth - rect.right
    }
  }
}

const toggleColumnSettings = () => {
  if (!showColumnDropdown.value) {
    updateDropdownPosition()
  }
  showColumnDropdown.value = !showColumnDropdown.value
}

const handleClickOutside = (e: MouseEvent) => {
  if (
    showColumnDropdown.value &&
    columnSettingsRef.value &&
    !columnSettingsRef.value.contains(e.target as Node) &&
    columnSettingsDropdownRef.value &&
    !columnSettingsDropdownRef.value.contains(e.target as Node)
  ) {
    showColumnDropdown.value = false
  }
}

const handleResize = () => {
  if (showColumnDropdown.value) {
    updateDropdownPosition()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('resize', handleResize)
})
</script>
