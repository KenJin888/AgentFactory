<template>
  <div @click="$emit('change', !active)" :class="`p-4 rounded-xl border-2 cursor-pointer transition-all flex items-start gap-3 ${active ? 'border-blue-500 bg-blue-50' : 'border-slate-100 bg-white hover:border-slate-200'}`">
      <div :class="`mt-0.5 p-2 rounded-lg ${active ? 'bg-white' : 'bg-slate-100'}`">
        <component :is="icon" size="18" />
      </div>
      <div>
          <div :class="`font-bold text-sm ${active ? 'text-blue-900' : 'text-slate-900'}`">{{ label }}</div>
          <div class="text-xs text-slate-500 mt-0.5">{{ desc }}</div>
      </div>
      <div :class="`ml-auto w-5 h-5 rounded-full border flex items-center justify-center ${active ? 'bg-blue-500 border-blue-500' : 'border-slate-300'}`">
          <Check v-if="active" :size="12" class="text-white" />
      </div>
  </div>
</template>

<script setup lang="ts">
import { Check } from 'lucide-vue-next'

// 定义组件属性
const props = defineProps<{
  icon: any
  label: string
  desc: string
  active: boolean
}>()

// 定义组件事件
const emit = defineEmits<{
  'change': [value: boolean]
}>()
</script>