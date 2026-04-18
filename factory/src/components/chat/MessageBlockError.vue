<template>
  <div class="text-red-600 p-2 bg-red-50 rounded border border-red-100">
    {{ block.content || '出现错误' }}
  </div>
</template>

<script setup lang="ts">
import type { AssistantMessageBlock } from '../../types/chat'

defineProps<{
  block: AssistantMessageBlock
}>()
</script>
