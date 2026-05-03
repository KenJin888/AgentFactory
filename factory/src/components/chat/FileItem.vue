<template>
  <div class="inline-block">
    <!-- 图片文件在消息中使用特殊布局 -->
    <div
      v-if="isImageFile && thumbnail && context === 'message'"
      class="flex flex-col gap-2 bg-white border border-gray-200 items-center shadow-sm justify-start rounded-md text-xs cursor-pointer select-none hover:bg-gray-50 relative p-2 group"
      @click="$emit('click', fileName)"
    >
      <img :src="thumbnail" class="w-20 h-20 rounded-md border object-cover" />
      <div class="text-center max-w-20">
        <div class="text-xs leading-none pb-1 truncate text-ellipsis whitespace-nowrap text-gray-700">
          {{ fileName }}
        </div>
        <div
          class="text-[10px] leading-none text-gray-500 truncate text-ellipsis whitespace-nowrap"
        >
          {{ mimeType }}
        </div>
      </div>
      <!-- Token 提示 Tooltip -->
      <div
        v-if="tokens > 0"
        class="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 px-2 py-1 bg-gray-800 text-white text-[10px] rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10"
      >
        {{ tokens }} tokens
        <div class="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-gray-800"></div>
      </div>
      <span
        v-if="deletable"
        class="bg-white shadow-sm flex items-center justify-center absolute rounded-full -top-1 -right-1 p-0.5 border border-gray-200 hover:bg-red-50"
        @click.stop.prevent="$emit('delete', fileName)"
      >
        <X class="w-3 h-3 text-gray-400" />
      </span>
    </div>

    <!-- 非图片文件或输入框中的文件使用原有布局 -->
    <div
      v-else
      class="flex py-1.5 pl-1.5 pr-3 gap-2 flex-row bg-white border border-gray-200 items-center shadow-sm justify-start rounded-md text-xs cursor-pointer select-none hover:bg-gray-50 relative group"
      @click="$emit('click', fileName)"
    >
      <!-- 图片缩略图 -->
      <img v-if="thumbnail" :src="thumbnail" class="w-8 h-8 rounded-md border object-cover" />
      <!-- 文件图标 -->
      <div
        v-else
        class="w-8 h-8 text-gray-500 p-1 bg-gray-100 rounded-md border border-gray-200 flex items-center justify-center"
      >
        <FileText v-if="isImageFile" class="w-5 h-5" />
        <FileText v-else-if="isPdf" class="w-5 h-5 text-red-500" />
        <FileSpreadsheet v-else-if="isExcel" class="w-5 h-5 text-green-500" />
        <FileCode v-else-if="isCode" class="w-5 h-5 text-blue-500" />
        <FileText v-else class="w-5 h-5" />
      </div>

      <div class="grow flex-1 max-w-28">
        <div class="text-xs leading-none pb-1 truncate text-ellipsis whitespace-nowrap text-gray-700">
          {{ fileName }}
        </div>
        <div class="flex items-center gap-2">
          <div
            class="text-[10px] leading-none text-gray-500 truncate text-ellipsis whitespace-nowrap"
          >
            {{ mimeType }}
          </div>
        </div>
      </div>

      <!-- Token 提示 Tooltip -->
      <div
        v-if="tokens > 0"
        class="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 px-2 py-1 bg-gray-800 text-white text-[10px] rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10"
      >
        {{ tokens }} tokens
        <div class="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-gray-800"></div>
      </div>

      <span
        v-if="deletable"
        class="bg-white shadow-sm flex items-center justify-center absolute rounded-full -top-1 -right-1 p-0.5 border border-gray-200 hover:bg-red-50"
        @click.stop.prevent="$emit('delete', fileName)"
      >
        <X class="w-3 h-3 text-gray-400" />
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { FileText, FileSpreadsheet, FileCode, X } from 'lucide-vue-next'

const props = withDefaults(
  defineProps<{
    fileName: string
    deletable: boolean
    mimeType?: string
    tokens: number
    thumbnail?: string
    context?: 'input' | 'message'
  }>(),
  {
    mimeType: 'text/plain',
    context: 'message'
  }
)

defineEmits<{
  click: [fileName: string]
  delete: [fileName: string]
}>()

// 是否是图片文件
const isImageFile = computed(() => {
  return props.mimeType?.startsWith('image/') || false
})

// 是否是PDF
const isPdf = computed(() => {
  return props.mimeType?.includes('pdf') || false
})

// 是否是Excel
const isExcel = computed(() => {
  return props.mimeType?.includes('excel') || 
         props.mimeType?.includes('spreadsheet') || 
         props.fileName?.endsWith('.xlsx') || 
         props.fileName?.endsWith('.xls') ||
         false
})

// 是否是代码文件
const isCode = computed(() => {
  const codeExtensions = ['.js', '.ts', '.vue', '.py', '.java', '.cpp', '.c', '.h', '.go', '.rs']
  return codeExtensions.some(ext => props.fileName?.endsWith(ext)) || false
})
</script>
