<template>
  <div class="rounded-lg border border-slate-200 bg-white p-3 space-y-2">
    <div class="flex items-center gap-2 text-sm font-medium text-slate-700">
      <ListChecks :size="14" class="text-slate-500" />
      计划
      <span class="text-xs text-slate-400">{{ completedCount }}/{{ totalCount }}</span>
    </div>
    <div v-if="totalCount > 0" class="space-y-1 text-xs text-slate-600">
      <div v-for="(entry, idx) in entries" :key="idx" class="flex items-center gap-2">
        <span
          class="w-1.5 h-1.5 rounded-full"
          :class="entry.status === 'done' || entry.status === 'completed' ? 'bg-emerald-500' : 'bg-slate-300'"
        />
        <span class="flex-1 truncate">{{ entry.title || entry.content || '未命名步骤' }}</span>
        <span class="text-[10px] text-slate-400">{{ entry.status || 'pending' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ListChecks } from 'lucide-vue-next'
import type { AssistantMessageBlock } from '../../types/chat'

const props = defineProps<{
  block: AssistantMessageBlock
}>()

const entries = computed(() => {
  const list = (props.block.extra as { plan_entries?: Array<{ title?: string; content?: string; status?: string }> })
    ?.plan_entries
  return Array.isArray(list) ? list : []
})

const totalCount = computed(() => entries.value.length)

const completedCount = computed(() => {
  return entries.value.filter((entry) => entry.status === 'done' || entry.status === 'completed').length
})
</script>
