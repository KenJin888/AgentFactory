<template>
  <div class="rounded-lg border border-blue-100 bg-blue-50 p-3 text-xs text-blue-800 space-y-1">
    <div class="flex items-center gap-2 font-medium">
      <Search :size="14" />
      搜索结果
    </div>
    <div class="whitespace-pre-wrap">{{ block.content }}</div>
  </div>
</template>

<script setup lang="ts">
import { Search } from 'lucide-vue-next'
import type { AssistantMessageBlock } from '../../types/chat'

defineProps<{
  block: AssistantMessageBlock
}>()
</script>
