<template>
  <div class="mb-3 p-3 bg-amber-50 rounded-lg border border-amber-100 text-xs text-amber-800 font-mono whitespace-pre-wrap">
    <div class="font-bold mb-1 flex items-center gap-1">
      <Sparkles :size="12" />
      推理补充
    </div>
    {{ block.content }}
  </div>
</template>

<script setup lang="ts">
import { Sparkles } from 'lucide-vue-next'
import type { AssistantMessageBlock } from '../../types/chat'

defineProps<{
  block: AssistantMessageBlock
}>()
</script>
