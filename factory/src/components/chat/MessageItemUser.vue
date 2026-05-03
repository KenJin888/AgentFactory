<template>
  <div :data-message-id="message.id" class="flex flex-row-reverse pt-5 pl-11 gap-3 w-full justify-start">
    <div class="w-8 h-8 rounded-md flex items-center justify-center flex-shrink-0 shadow-sm overflow-hidden" :class="avatarClass">
      <img v-if="userAvatarUrl" :src="userAvatarUrl" alt="User" class="w-full h-full object-cover" />
      <User v-else :size="20" class="text-slate-500" />
    </div>
    <div class="flex flex-col w-full items-end space-y-1.5">
      <div class="text-sm bg-slate-50 border border-slate-200 rounded-lg p-3 shadow-sm text-slate-800 w-fit max-w-[85%] lg:max-w-[75%]">
        <div class="flex flex-col gap-2" data-message-content="true">
          <!-- 文件列表 - 使用 FileItem 组件展示 -->
          <div v-if="fileList.length > 0" class="flex flex-wrap gap-2">
            <FileItem
              v-for="(file, idx) in fileList"
              :key="idx"
              :file-name="file.name"
              :deletable="false"
              :mime-type="file.mimeType"
              :tokens="file.token"
              :thumbnail="file.thumbnail"
              context="message"
              @click="previewFile(file.path)"
            />
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
import FileItem from './FileItem.vue'
import type {MESSAGE, UserMessageContent, MessageFile} from '../../types/chat'
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

// 文件列表 - 转换为 FileItem 需要的格式
const fileList = computed(() => {
  const files = userContent.value?.files || []
  return files.map((file) => ({
    name: file?.name || '文件',
    mimeType: file?.mimeType || 'application/octet-stream',
    token: file?.token || 0,
    thumbnail: file?.thumbnail,
    path: file?.path
  }))
})

const linkList = computed(() => {
  return userContent.value?.links || []
})

// 预览文件
const previewFile = (path: string | undefined) => {
  if (path) {
    window.open(path, '_blank')
  }
}
</script>
