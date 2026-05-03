<template>
  <div
    class="p-4 bg-white border-t border-gray-100 flex-shrink-0"
    @dragenter.prevent="handleDragEnter"
    @dragover.prevent="handleDragOver"
    @drop.prevent="handleDrop"
    @dragleave.prevent="handleDragLeave"
    @paste="handlePaste"
  >
    <div class="max-w-6xl mx-auto px-8">
      <!-- 拖拽提示 -->
      <div
        v-if="isDragging"
        class="mb-2 p-4 border-2 border-dashed border-blue-400 bg-blue-50 rounded-lg text-center text-blue-600"
      >
        释放以上传文件
      </div>

      <div v-if="isUploading" class="mb-2 text-xs text-blue-600 flex items-center gap-1">
        <Loader2 className="animate-spin" :size="12" />
        上传中...
      </div>

      <!-- 文件预览列表（统一使用 FileItem 组件，包括图片） -->
      <div v-if="files.selectedFiles.value.length > 0" class="mb-2 flex flex-wrap items-center gap-2">
        <FileItem
          v-for="(file, idx) in files.selectedFiles.value"
          :key="file.name + idx"
          :file-name="file.name"
          :deletable="true"
          :mime-type="file.type || 'application/octet-stream'"
          :tokens="0"
          :thumbnail="file.type?.startsWith('image/') ? files.getThumbnail(file.name) : undefined"
          context="input"
          @delete="files.deleteFileByName(file.name)"
        />
      </div>

      <div :class="`bg-slate-50 p-2 rounded-3xl border transition-all ${isRecording ? 'border-red-400 ring-2 ring-red-50' : 'border-slate-200 focus-within:border-blue-400'}`">
        <div class="flex items-end gap-2">
          <template v-if="agentConfig.enable_upload">
            <input
              type="file"
              ref="fileInputEl"
              class="hidden"
              @change="files.handleFileSelect"
              multiple
              accept=".pdf,.doc,.docx,.txt,.ppt,.pptx,.xlsx,.xls,image/*,.js,.ts,.vue,.py,.java,.cpp,.c,.h,.go,.rs,.json,.md,.html,.css"
            />
            <button @click="triggerFileInput" class="p-3 text-slate-400 hover:text-blue-600 rounded-full hover:bg-white" title="上传文件">
              <Paperclip :size="20" />
            </button>
          </template>
          <button
            v-if="agentConfig.enable_search"
            @click="emit('update:enableWebSearch', !enableWebSearch)"
            :class="`p-3 rounded-full transition-all ${enableWebSearch ? 'text-blue-600 bg-blue-50' : 'text-slate-400 hover:bg-slate-100'}`"
            title="联网开关"
          >
            <Globe :size="20" />
          </button>
          <textarea
            class="flex-1 bg-transparent border-none outline-none py-3 px-2 max-h-32 text-sm resize-none"
            placeholder="输入消息..."
            rows="1"
            :value="input"
            @input="emit('update:input', ($event.target as HTMLTextAreaElement).value)"
            @keydown.enter.exact.prevent="handleSend"
            @keydown.enter.shift.prevent
          />
          <button
            v-if="agentConfig.enable_voice"
            @click="emit('toggle-recording')"
            :class="`p-3 rounded-full ${isRecording ? 'bg-red-500 text-white animate-pulse' : 'text-slate-400 hover:text-blue-600 hover:bg-white'}`"
          >
            <div v-if="isRecording" class="w-2 h-2 bg-white rounded-sm" />
            <Mic v-else :size="20" />
          </button>
          <button
            v-if="msgLoading"
            @click="emit('stop')"
            :disabled="stopLoading"
            class="p-3 bg-red-500 text-white rounded-full hover:bg-red-600 disabled:opacity-50"
          >
            <Square :size="20" />
          </button>
          <button
            v-else
            @click="handleSend"
            :disabled="(!input.trim() && !files.hasFiles()) || isUploading || files.isProcessing.value"
            class="p-3 bg-slate-900 text-white rounded-full hover:bg-blue-600 disabled:opacity-50"
          >
            <Send :size="20" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Send, Paperclip, Mic, Globe, Loader2, Square } from 'lucide-vue-next'
import FileItem from './FileItem.vue'
import { usePromptInputFiles } from '../../composables/usePromptInputFiles'
import type { UserMessageContent } from '../../types/chat'

type AgentConfig = {
  enable_upload?: boolean
  enable_search?: boolean
  enable_voice?: boolean
}

const props = defineProps<{
  agentConfig: AgentConfig
  isUploading: boolean
  isRecording: boolean
  enableWebSearch: boolean
  msgLoading: boolean
  stopLoading: boolean
  input: string
}>()

const emit = defineEmits<{
  (e: 'update:input', value: string): void
  (e: 'update:enableWebSearch', value: boolean): void
  (e: 'send', content: UserMessageContent, files: File[]): void
  (e: 'stop'): void
  (e: 'toggle-recording'): void
}>()

const fileInputEl = ref<HTMLInputElement | null>(null)
const isDragging = ref(false)

// 统一文件上传处理 - 使用 usePromptInputFiles
const files = usePromptInputFiles({
  maxCount: 10,
  maxSize: 20 * 1024 * 1024
})

const triggerFileInput = () => {
  fileInputEl.value?.click()
}

// 拖拽处理
const handleDragEnter = () => {
  isDragging.value = true
}

const handleDragOver = () => {
  isDragging.value = true
}

const handleDragLeave = () => {
  isDragging.value = false
}

const handleDrop = async (e: DragEvent) => {
  isDragging.value = false
  const droppedFiles = e.dataTransfer?.files
  if (droppedFiles && droppedFiles.length > 0) {
    await files.handleDrop(droppedFiles)
  }
}

// 粘贴处理
const handlePaste = async (e: ClipboardEvent) => {
  await files.handlePaste(e)
}

// 处理发送 - 构建 UserMessageContent 对象
const handleSend = async () => {
  const text = props.input.trim()

  // 检查是否有内容可发送
  if ((!text && !files.hasFiles()) || props.isUploading || files.isProcessing.value) {
    return
  }

  // 构建消息内容对象
  // 图片作为 files 的一部分传递，后端通过 mimeType 识别图片
  const messageContent: UserMessageContent = {
    text: text,
    links: [],
    think: false,
    search: props.enableWebSearch
  }

  // 发送消息内容和文件
  // 图片文件和非图片文件都通过 files 传递
  emit('send', messageContent, files.selectedFiles.value)

  // 清空输入和文件
  emit('update:input', '')
  files.clearFiles()
}
</script>
