<template>
  <div class="mb-3 rounded-lg border border-slate-200 bg-slate-50 p-3">
    <div 
      class="flex items-center gap-2 font-medium cursor-pointer transition-colors select-none"
      style="color: #61666B"
      @click="isExpanded = !isExpanded"
    >
      <Brain :size="14" />
      <span>思考过程</span>
      <ChevronDown 
        :size="14" 
        class="ml-auto transition-transform duration-200" 
        :class="{ '-rotate-90': !isExpanded }" 
      />
    </div>
    
    <div v-show="isExpanded" class="mt-3" style="color: #61666B">
      <div class="bg-white border border-slate-100 rounded p-3 whitespace-pre-wrap text-xs">{{ block.content }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Brain, ChevronDown } from 'lucide-vue-next'
import type { AssistantMessageBlock } from '../../types/chat'

defineProps<{
  block: AssistantMessageBlock
}>()

const isExpanded = ref(true)
</script>
