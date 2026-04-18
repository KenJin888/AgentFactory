<template>
  <div class="rounded-lg border border-slate-200 bg-slate-50 p-3 space-y-2 text-xs text-slate-700">
    <div class="flex items-center gap-2 font-medium text-slate-600">
      <PanelTop :size="14" />
      MCP UI 资源
    </div>
    <div v-if="resource?.uri" class="break-all">
      <a :href="resource.uri" target="_blank" class="text-blue-600 underline">
        {{ resource.uri }}
      </a>
    </div>
    <div v-else-if="resource?.text" class="whitespace-pre-wrap">{{ resource.text }}</div>
    <div v-else-if="resource?.blob" class="whitespace-pre-wrap">{{ resource.blob }}</div>
    <div v-else class="text-slate-400">暂无内容</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { PanelTop } from 'lucide-vue-next'
import type { AssistantMessageBlock } from '../../types/chat'

const props = defineProps<{
  block: AssistantMessageBlock
}>()

const resource = computed(() => props.block.mcp_ui_resource)
</script>
