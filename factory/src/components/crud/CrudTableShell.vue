<template>
  <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
    <!-- 工具栏插槽 -->
    <div v-if="$slots.toolbar" class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
      <slot name="toolbar" />
    </div>

    <!-- 表格内容区 -->
    <div class="overflow-x-auto" :style="{ minHeight: minHeight + 'px' }">
      <table class="w-full text-sm" :style="tableStyle">
        <slot name="table" />
      </table>
    </div>

    <!-- 分页区 -->
    <div v-if="showPagination && total > 0" class="px-6 py-4 border-t border-slate-100 flex items-center justify-between bg-slate-50/30">
      <div class="flex items-center gap-4">
        <span class="text-sm text-slate-500">
          共 <span class="font-semibold text-slate-900">{{ total }}</span> 条记录
        </span>
        <select
          :value="pageSize"
          @change="handlePageSizeChange"
          class="px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-50 focus:border-blue-400"
        >
          <option v-for="size in pageSizeOptions" :key="size" :value="size">{{ size }} 条/页</option>
        </select>
      </div>
      <div class="flex items-center gap-2">
        <button
          @click="changePage(currentPage - 1)"
          :disabled="currentPage <= 1"
          class="px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-sm disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-50 hover:border-slate-300 transition-all"
        >
          上一页
        </button>
        <span class="text-sm text-slate-700 px-3">第 {{ currentPage }} 页</span>
        <button
          @click="changePage(currentPage + 1)"
          :disabled="!hasMore"
          class="px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-sm disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-50 hover:border-slate-300 transition-all"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  // 加载状态
  loading?: boolean
  // 数据总数
  total?: number
  // 当前页
  currentPage?: number
  // 每页条数
  pageSize?: number
  // 页码选项
  pageSizeOptions?: number[]
  // 是否显示分页
  showPagination?: boolean
  // 当前页数据条数（用于判断是否还有下一页）
  currentPageDataCount?: number
  // 表格最小高度
  minHeight?: number
  // 表格样式
  tableMinWidth?: string
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  total: 0,
  currentPage: 1,
  pageSize: 10,
  pageSizeOptions: () => [10, 20, 50, 100],
  showPagination: true,
  currentPageDataCount: 0,
  minHeight: 200,
  tableMinWidth: '100%'
})

const emit = defineEmits<{
  'update:currentPage': [page: number]
  'update:pageSize': [size: number]
  'pageChange': [page: number]
  'sizeChange': [size: number]
}>()

const tableStyle = computed(() => ({
  minWidth: props.tableMinWidth
}))

const hasMore = computed(() => {
  // 如果有当前页数据条数，优先使用
  if (props.currentPageDataCount > 0) {
    return props.currentPageDataCount >= props.pageSize
  }
  // 否则根据总数计算
  const totalPages = Math.ceil(props.total / props.pageSize)
  return props.currentPage < totalPages
})

const changePage = (page: number) => {
  if (page < 1) return
  if (props.currentPageDataCount > 0 && page > props.currentPage && !hasMore.value) return
  emit('update:currentPage', page)
  emit('pageChange', page)
}

const handlePageSizeChange = (e: Event) => {
  const size = parseInt((e.target as HTMLSelectElement).value, 10)
  emit('update:pageSize', size)
  emit('update:currentPage', 1)
  emit('sizeChange', size)
}
</script>
