<template>
  <div :data-message-id="message.id" class="flex flex-row pl-4 pt-5 pr-11 gap-3 w-full justify-start">
    <div
      class="w-10 h-10 rounded-md flex items-center justify-center flex-shrink-0 shadow-sm overflow-hidden"
      :class="assistantAvatarClass"
    >
      <Bot :size="24" />
    </div>
    <div class="flex flex-col w-full space-y-1.5">
      <div class="text-sm bg-white border border-gray-100 rounded-lg p-3 shadow-sm text-slate-800">
        <div class="markdown-body prose prose-sm max-w-none prose-p:leading-relaxed prose-pre:bg-gray-800 prose-pre:text-gray-100 flex flex-col gap-2" data-message-content="true">
          <template v-for="(block, idx) in contentBlocks" :key="block.id || `${message.id}-${idx}`">
            <MessageBlockContent v-if="block.type === 'content'" :block="block" />
            <MessageBlockReasoning v-else-if="block.type === 'reasoning_content'" :block="block" />
            <MessageBlockArtifactThinking v-else-if="block.type === 'artifact-thinking'" :block="block" />
            <MessageBlockSearch v-else-if="block.type === 'search'" :block="block" />
            <MessageBlockPlan v-else-if="block.type === 'plan'" :block="block" />
            <MessageBlockToolCall v-else-if="block.type === 'tool_call'" :block="block" />
            <MessageBlockAction v-else-if="block.type === 'action'" :block="block" />
            <MessageBlockImage v-else-if="block.type === 'image'" :block="block" />
            <MessageBlockMcpUi v-else-if="block.type === 'mcp_ui_resource'" :block="block" />
            <MessageBlockError v-else-if="block.type === 'error'" :block="block" />
            <div v-else class="text-xs text-slate-400">暂不支持的消息块</div>
          </template>
          <div v-if="contentBlocks.length === 0" class="text-xs text-slate-400">暂无内容</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed} from 'vue'
import {Bot} from 'lucide-vue-next'
import type {AssistantMessageBlock, MESSAGE} from '../../types/chat'
import MessageBlockContent from './MessageBlockContent.vue'
import MessageBlockReasoning from './MessageBlockReasoning.vue'
import MessageBlockArtifactThinking from './MessageBlockArtifactThinking.vue'
import MessageBlockSearch from './MessageBlockSearch.vue'
import MessageBlockPlan from './MessageBlockPlan.vue'
import MessageBlockToolCall from './MessageBlockToolCall.vue'
import MessageBlockAction from './MessageBlockAction.vue'
import MessageBlockImage from './MessageBlockImage.vue'
import MessageBlockMcpUi from './MessageBlockMcpUi.vue'
import MessageBlockError from './MessageBlockError.vue'
import {parseAssistantStoredContent} from '@/utils/chatMessage'

type AgentConfig = {
  creator_id?: string | number
}

const props = defineProps<{
  message: MESSAGE
  agentConfig: AgentConfig
}>()

const assistantAvatarClass = computed(() => {
  return props.agentConfig.creator_id ? 'bg-blue-500 text-white' : 'bg-blue-600 text-white'
})

const contentBlocks = computed<AssistantMessageBlock[]>(() => {
  const content = props.message.content
    if (Array.isArray(content)) return content
  if (typeof content === 'string' && content.trim()) {
    const parsed = parseAssistantStoredContent(
        content,
        props.message.updated_at || props.message.created_at || Date.now()
    )
    if (parsed.content.length > 0) return parsed.content
  }
  return []
})
</script>
