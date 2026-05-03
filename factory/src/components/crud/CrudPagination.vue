<template>
  <div class="flex items-center justify-between">
    <div class="text-sm text-slate-600">
      共 <span class="font-medium text-slate-900">{{ total }}</span> 条记录
    </div>

    <div class="flex items-center gap-2">
      <!-- 每页条数选择 -->
      <select
        :value="pageSize"
        @change="$emit('size-change', Number(($event.target as HTMLSelectElement).value))"
        class="px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-50 focus:border-blue-400"
      >
        <option v-for="size in pageSizes" :key="size" :value="size">
          {{ size }} 条/页
        </option>
      </select>

      <!-- 分页按钮 -->
      <div class="flex items-center gap-1">
        <button
          :disabled="currentPage <= 1"
          @click="$emit('page-change', currentPage - 1)"
          class="px-3 py-2 border border-slate-200 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          <ChevronLeftIcon class="w-4 h-4" />
        </button>

        <button
          v-for="page in displayedPages"
          :key="page"
          @click="$emit('page-change', page)"
          :class="[
            'px-3 py-2 border rounded-lg transition-all min-w-[40px]',
            currentPage === page
              ? 'bg-blue-600 border-blue-600 text-white'
              : 'border-slate-200 hover:bg-slate-50 text-slate-700'
          ]"
        >
          {{ page }}
        </button>

        <button
          :disabled="currentPage >= totalPages"
          @click="$emit('page-change', currentPage + 1)"
          class="px-3 py-2 border border-slate-200 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          <ChevronRightIcon class="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ChevronLeftIcon, ChevronRightIcon } from 'lucide-vue-next'

const props = defineProps<{
  currentPage: number
  pageSize: number
  total: number
  pageSizes?: number[]
}>()

defineEmits<{
  'page-change': [page: number]
  'size-change': [size: number]
}>()

const pageSizes = computed(() => props.pageSizes || [10, 20, 50, 100])

const totalPages = computed(() => Math.ceil(props.total / props.pageSize))

const displayedPages = computed(() => {
  const pages: number[] = []
  const maxVisible = 5
  const half = Math.floor(maxVisible / 2)

  let start = Math.max(1, props.currentPage - half)
  let end = Math.min(totalPages.value, start + maxVisible - 1)

  if (end - start < maxVisible - 1) {
    start = Math.max(1, end - maxVisible + 1)
  }

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  return pages
})
</script>
