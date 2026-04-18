<template>
  <div class="w-full h-full relative min-h-0">
    <div ref="scrollContainerRef" class="message-list-container relative flex-1 scrollbar-hide overflow-y-auto w-full h-full">
      <div class="max-w-6xl mx-auto px-8 pt-4">
        <template v-for="(msg, idx) in messages" :key="msg.id || idx">
          <MessageItemUser
            v-if="msg.role === 'user'"
            :message="msg"
            :user-avatar-url="userAvatarUrl"
          />
          <div v-else class="flex flex-col w-full">
            <MessageItemAssistant :message="msg" :agent-config="agentConfig" />
            <MessageToolbar v-if="msg.id !== 'welcome-welcome'"
              :content="getMessageContent(msg)"
              :metadata="msg.metadata || {}"
              @retry="$emit('retry', msg.id)"
              @share="$emit('share', msg.id)"
            />
          </div>
        </template>
        <div v-if="msgLoading" class="flex gap-2 items-center pl-6 pt-4 text-xs text-slate-400">
          <Loader2 :size="14" class="animate-spin" /> AI 正在思考...
        </div>
        <div :ref="messagesEndRef" class="h-8" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Loader2 } from 'lucide-vue-next'
import type { MESSAGE, AssistantMessageBlock } from '../../types/chat'
import MessageItemAssistant from './MessageItemAssistant.vue'
import MessageItemUser from './MessageItemUser.vue'
import MessageToolbar from './MessageToolbar.vue'

type AgentConfig = {
  creator_id?: string | number
}

defineProps<{
  messages: MESSAGE[]
  msgLoading: boolean
  userAvatarUrl: string | undefined
  agentConfig: AgentConfig
  messagesEndRef: any
}>()

defineEmits<{
  'retry': [messageId: string]
  'share': [messageId: string]
}>()

const scrollContainerRef = ref<HTMLDivElement | null>(null)

defineExpose({
  scrollContainerRef
})

const getMessageContent = (msg: MESSAGE) => {
  if (typeof msg.content === 'string') return msg.content
  if (Array.isArray(msg.content)) {
    return (msg.content as AssistantMessageBlock[])
      .filter(block => block.type === 'content' && block.content)
      .map(block => block.content)
      .join('\n')
  }
  return ''
}
</script>
