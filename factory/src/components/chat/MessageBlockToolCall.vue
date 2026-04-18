<template>
  <div class="rounded-lg border border-slate-200 bg-slate-50 p-3 text-xs text-slate-700">
    <div 
      class="flex items-center gap-2 font-medium cursor-pointer transition-colors select-none"
      :class="isSkillCall ? 'text-indigo-600 hover:text-indigo-800' : 'text-slate-600 hover:text-slate-800'"
      @click="isExpanded = !isExpanded"
    >
      <Loader2 v-if="block.status === 'loading'" :size="14" class="animate-spin" />
      <Sparkles v-else-if="isSkillCall" :size="14" />
      <Wrench v-else :size="14" />
      <span>{{ isSkillCall ? (skillInfo?.skill_name ? `技能: ${skillInfo.skill_name}` : '技能') : ('工具: ' + toolCall?.name || '') }}</span>
      <ChevronDown 
        :size="14" 
        class="ml-auto transition-transform duration-200" 
        :class="{ '-rotate-90': !isExpanded }" 
      />
    </div>
    
    <div v-show="isExpanded" class="space-y-2 mt-3">
      <template v-if="isSkillCall">
        <div v-if="skillInfo" class="space-y-1">
          <div class="text-[10px] uppercase text-slate-400">技能信息</div>
          <div class="bg-white border border-slate-100 rounded p-3 space-y-2">
            <div class="font-medium text-slate-800 text-sm">{{ skillInfo.skill_name }}</div>
            <div class="text-slate-600 whitespace-pre-wrap leading-relaxed">{{ skillInfo.description }}</div>
          </div>
        </div>
        <div v-else-if="toolCall?.response" class="space-y-1">
          <div class="text-[10px] uppercase text-slate-400">解析失败</div>
          <pre class="whitespace-pre-wrap break-words bg-white border border-slate-100 rounded p-2 max-h-40 overflow-y-auto">{{ toolCall.response }}</pre>
        </div>
      </template>
      <template v-else>
        <div v-if="toolCall?.params" class="space-y-1">
          <div class="text-[10px] uppercase text-slate-400">参数</div>
          <pre class="whitespace-pre-wrap break-words bg-white border border-slate-100 rounded p-2 max-h-40 overflow-y-auto">{{ toolCall.params }}</pre>
        </div>
        <div v-if="toolCall?.response" class="space-y-1">
          <div class="text-[10px] uppercase text-slate-400">结果</div>
          <pre class="whitespace-pre-wrap break-words bg-white border border-slate-100 rounded p-2 max-h-64 overflow-y-auto">{{ toolCall.response }}</pre>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { Wrench, ChevronDown, Loader2, Sparkles } from 'lucide-vue-next'
import type { AssistantMessageBlock } from '../../types/chat'

const props = defineProps<{
  block: AssistantMessageBlock
}>()

const toolCall = computed(() => props.block.tool_call)
const isExpanded = ref(false)

const isSkillCall = computed(() => toolCall.value?.name === 'get_skill_instructions')

const skillInfo = computed(() => {
  if (!isSkillCall.value || !toolCall.value?.response) return null
  try {
    const parsed = JSON.parse(toolCall.value.response)
    return {
      skill_name: parsed.skill_name || parsed.name || '未知技能',
      description: parsed.description || '暂无描述'
    }
  } catch (e) {
    return null
  }
})
</script>
