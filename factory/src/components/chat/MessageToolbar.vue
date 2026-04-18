<template>
  <div class="flex items-center gap-1 mt-1 ml-14 pl-1">
    <button
      class="p-1.5 rounded-md hover:bg-gray-100 text-gray-400 hover:text-gray-600 transition-colors"
      title="复制"
      @click="handleCopy"
    >
      <Copy v-if="!copied" :size="14" />
      <Check v-else :size="14" class="text-green-500" />
    </button>
    <button
      class="p-1.5 rounded-md hover:bg-gray-100 text-gray-400 hover:text-gray-600 transition-colors"
      title="重新生成"
      @click="$emit('retry')"
    >
      <RotateCw :size="14" />
    </button>
    <button
      class="p-1.5 rounded-md hover:bg-gray-100 text-gray-400 hover:text-gray-600 transition-colors"
      title="分享"
      @click="$emit('share')"
    >
      <Share2 :size="14" />
    </button>
    <div class="ml-2 flex items-center gap-2 text-xs text-gray-400">
      <span class="inline-flex items-center gap-1" title="输出 Tokens">
        <ArrowUp :size="12" />
        <span>{{ metadata.outputTokens }}</span>
      </span>
      <span class="inline-flex items-center gap-1" title="输入 Tokens">
        <ArrowDown :size="12" />
        <span>{{ metadata.inputTokens }}</span>
      </span>
      <span class="inline-flex items-center gap-1" title="总 Tokens">
        <Sigma :size="12" />
        <span>{{ metadata?.totalTokens }}</span>
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Copy, Check, RotateCw, Share2, ArrowDown, ArrowUp, Sigma } from 'lucide-vue-next'
import message from '../common/message'
import { MESSAGE_METADATA } from '@/types/chat';

const props = defineProps<{
  content: string
  metadata: MESSAGE_METADATA | Partial<MESSAGE_METADATA>
}>()

const emit = defineEmits<{
  'retry': []
  'share': []
}>()

const copied = ref(false)

const handleCopy = async () => {
  if (!props.content) return
  
  try {
    await navigator.clipboard.writeText(props.content)
    copied.value = true
    message.success('已复制到剪贴板')
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy: ', err)
    message.error('复制失败')
  }
}
</script>
