<template>
  <div class="rounded-lg border border-slate-200 bg-white p-2">
    <img v-if="imageSrc" :src="imageSrc" class="max-w-full rounded-md" />
    <div v-else class="text-xs text-slate-400">图片不可用</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { AssistantMessageBlock } from '../../types/chat'

const props = defineProps<{
  block: AssistantMessageBlock
}>()

const imageSrc = computed(() => {
  const data = props.block.image_data?.data
  if (!data) return ''
  if (data.startsWith('data:') || data.startsWith('http') || data.startsWith('blob:')) {
    return data
  }
  const mimeType = props.block.image_data?.mimeType
  if (mimeType) return `data:${mimeType};base64,${data}`
  return data
})
</script>
