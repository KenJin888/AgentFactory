<template>
  <div class="rounded-lg border border-amber-200 bg-amber-50 p-3 text-xs text-amber-800 space-y-1">
    <div class="flex items-center gap-2 font-medium">
      <ShieldAlert :size="14" />
      动作请求
    </div>
    <div class="flex items-center gap-2">
      <span class="text-[10px] uppercase text-amber-600">Type</span>
      <span>{{ block.action_type || 'unknown' }}</span>
    </div>
    <div class="flex items-center gap-2">
      <span class="text-[10px] uppercase text-amber-600">Status</span>
      <span>{{ block.status }}</span>
    </div>
    <div v-if="block.content" class="whitespace-pre-wrap">{{ block.content }}</div>
  </div>
</template>

<script setup lang="ts">
import { ShieldAlert } from 'lucide-vue-next'
import type { AssistantMessageBlock } from '../../types/chat'

defineProps<{
  block: AssistantMessageBlock
}>()
</script>
