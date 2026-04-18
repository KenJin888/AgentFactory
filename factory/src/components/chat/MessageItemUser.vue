<template>
  <div :data-message-id="message.id" class="flex flex-row-reverse pt-5 pl-11 gap-3 w-full justify-start">
    <div class="w-8 h-8 rounded-md flex items-center justify-center flex-shrink-0 shadow-sm overflow-hidden" :class="avatarClass">
      <img v-if="userAvatarUrl" :src="userAvatarUrl" alt="User" class="w-full h-full object-cover" />
      <User v-else :size="20" class="text-slate-500" />
    </div>
    <div class="flex flex-col w-full items-end space-y-1.5">
      <div class="text-sm bg-slate-50 border border-slate-200 rounded-lg p-3 shadow-sm text-slate-800 w-fit max-w-[85%] lg:max-w-[75%]">
        <div class="flex flex-col gap-2" data-message-content="true">
          <div v-if="fileList.length > 0" class="flex flex-wrap gap-2">
            <div
                v-for="(file, idx) in fileList"
                :key="idx"
                class="w-full text-xs px-2 py-2 bg-white border border-slate-200 rounded"
            >
              <div class="font-medium text-slate-700 break-all">{{ file.name }}</div>
            </div>
          </div>
          <div class="whitespace-pre-wrap">{{ textContent }}</div>
          <div v-if="linkList.length > 0" class="flex flex-col gap-1 text-xs text-blue-600">
            <a v-for="(link, idx) in linkList" :key="idx" :href="link" target="_blank" class="underline break-all">
              {{ link }}
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed} from 'vue'
import {User} from 'lucide-vue-next'
import type {MESSAGE, UserMessageContent} from '../../types/chat'
import {parseUserStoredContent} from '../../utils/chatMessage'

const props = defineProps<{
  message: MESSAGE
  userAvatarUrl?: string
}>()

const avatarClass = computed(() => {
  return props.userAvatarUrl ? 'bg-white' : 'bg-slate-200'
})

const userContent = computed<UserMessageContent | null>(() => {
  const content = props.message.content
  if (typeof content === 'string' || (content && typeof content === 'object' && !Array.isArray(content))) {
    return parseUserStoredContent(content)
  }
  return null
})

const textContent = computed(() => {
  return userContent.value?.text || ''
})

const fileList = computed(() => {
  const files = userContent.value?.files || []
  return files.map((file) => ({
    name: file?.name || '文件'
  }))
})

const linkList = computed(() => {
  return userContent.value?.links || []
})
</script>
