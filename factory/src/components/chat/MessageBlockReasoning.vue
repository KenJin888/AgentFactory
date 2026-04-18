<template>
  <div class="mb-3 p-3 bg-purple-50 rounded-lg border border-purple-100 text-xs text-purple-800 font-mono whitespace-pre-wrap">
    <div class="font-bold mb-1 flex items-center gap-1">
      <Brain :size="12" />
      思考过程
    </div>
    {{ block.content }}
  </div>
</template>

<script setup lang="ts">
import { Brain } from 'lucide-vue-next'
import type { AssistantMessageBlock } from '../../types/chat'

defineProps<{
  block: AssistantMessageBlock
}>()
</script>
