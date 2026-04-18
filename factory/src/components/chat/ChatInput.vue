<template>
  <div class="p-4 bg-white border-t border-gray-100 flex-shrink-0">
    <div class="max-w-6xl mx-auto px-8">
      <div v-if="isUploading" class="mb-2 text-xs text-blue-600 flex items-center gap-1">
        <Loader2 className="animate-spin" :size="12" />
        上传中...
      </div>
      <div :class="`bg-slate-50 p-2 rounded-3xl border transition-all ${isRecording ? 'border-red-400 ring-2 ring-red-50' : 'border-slate-200 focus-within:border-blue-400'}`">
        <div v-if="uploadFiles.length" class="px-2 pt-1 pb-2 flex flex-wrap items-center gap-2">
          <div
            v-for="(file, index) in uploadFiles"
            :key="`${file.name}-${index}`"
            class="flex items-center gap-1.5 bg-transparent px-2 py-1 rounded-md text-[11px] text-black border border-gray-300 w-fit"
          >
            <FileText :size="14" />
            {{ file.name }}
            <button @click="removeFile(index)" class="text-slate-400 hover:text-red-500 p-1 rounded">
              <X :size="14" />
            </button>
          </div>
        </div>
        <div class="flex items-end gap-2">
          <template v-if="agentConfig.enable_upload">
            <input
              type="file"
              ref="fileInputEl"
              class="hidden"
              @change="emit('file-select', $event)"
              multiple
              accept=".pdf,.doc,.docx,.txt,.ppt,.pptx,.xlsx,.xls"
            />
            <button @click="triggerFileInput" class="p-3 text-slate-400 hover:text-blue-600 rounded-full hover:bg-white">
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
            @keydown.enter.exact.prevent="emit('send')"
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
            @click="emit('send')"
            :disabled="(!input.trim() && !uploadFiles.length) || isUploading"
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
import { Send, Paperclip, Mic, Globe, X, FileText, Loader2, Square } from 'lucide-vue-next'

type AgentConfig = {
  enable_upload?: boolean
  enable_search?: boolean
  enable_voice?: boolean
}

type SelectedUploadFile = {
  name: string
  url?: string
  file?: File
}

const props = defineProps<{
  agentConfig: AgentConfig
  isUploading: boolean
  uploadFiles: SelectedUploadFile[]
  isRecording: boolean
  enableWebSearch: boolean
  msgLoading: boolean
  stopLoading: boolean
  input: string
}>()

const emit = defineEmits<{
  (e: 'update:input', value: string): void
  (e: 'update:uploadFiles', value: SelectedUploadFile[]): void
  (e: 'update:enableWebSearch', value: boolean): void
  (e: 'send'): void
  (e: 'stop'): void
  (e: 'file-select', event: Event): void
  (e: 'toggle-recording'): void
}>()

const fileInputEl = ref<HTMLInputElement | null>(null)

const triggerFileInput = () => {
  fileInputEl.value?.click()
}

const removeFile = (index: number) => {
  emit('update:uploadFiles', props.uploadFiles.filter((_, i) => i !== index))
}
</script>
