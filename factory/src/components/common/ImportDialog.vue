<template>
  <div v-if="visible" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden">
      <div class="px-6 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
        <h2 class="text-xl font-bold text-slate-900">{{ title }}</h2>
        <button @click="handleCancel" class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all">
          <XIcon class="w-5 h-5" />
        </button>
      </div>
      <div class="p-6">
        <div class="mb-5">
          <p class="text-sm text-slate-600 mb-3">{{ description }}</p>
          <a 
            href="#" 
            @click.prevent="handleDownloadTemplate"
            class="text-blue-600 hover:text-blue-700 text-sm font-medium inline-flex items-center gap-1"
          >
            <DownloadIcon class="w-4 h-4" />
            下载导入模板
          </a>
        </div>
        
        <!-- 拖拽上传区域 -->
        <div 
          class="border-2 border-dashed border-slate-300 rounded-xl p-8 text-center transition-all cursor-pointer"
          :class="{ 
            'border-blue-400 bg-blue-50/30': isDragging,
            'hover:border-blue-400 hover:bg-blue-50/30': !uploadFileName 
          }"
          @click="fileInput?.click()"
          @dragenter.prevent="isDragging = true"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleDrop"
        >
          <input 
            ref="fileInput"
            type="file" 
            :accept="accept"
            @change="handleFileChange"
            class="hidden" 
          />
          <UploadIcon class="w-12 h-12 text-slate-400 mx-auto mb-3" />
          <p class="text-sm text-slate-600 mb-2">点击或拖拽文件到此处上传</p>
          <p class="text-xs text-slate-400">{{ acceptText }}</p>
          
          <!-- 已选择文件显示 -->
          <div v-if="uploadFileName" class="mt-3 flex items-center justify-center gap-2">
            <span class="text-sm font-medium text-slate-700 bg-slate-100 px-3 py-1.5 rounded-lg inline-flex items-center gap-2">
              <FileIcon class="w-4 h-4 text-slate-500" />
              {{ uploadFileName }}
              <button 
                @click.stop="clearFile"
                class="ml-1 p-0.5 hover:bg-slate-200 rounded-full transition-colors"
                title="移除文件"
              >
                <XIcon class="w-3 h-3 text-slate-500" />
              </button>
            </span>
          </div>
        </div>

        <!-- 错误提示 -->
        <div v-if="errorMessage" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-xl">
          <div class="flex items-start gap-2">
            <AlertCircleIcon class="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0" />
            <div>
              <p class="text-sm font-medium text-red-800">导入失败</p>
              <p class="text-xs text-red-600 mt-1">{{ errorMessage }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <div class="px-6 py-4 border-t border-slate-100 flex justify-end gap-3 bg-slate-50/30">
        <button
          @click="handleCancel"
          class="px-5 py-2.5 border border-slate-200 rounded-xl text-slate-700 hover:bg-white hover:border-slate-300 transition-all"
        >
          取消
        </button>
        <button
          @click="handleImportSubmit"
          :disabled="!uploadFile || importing"
          class="px-5 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 shadow-sm"
        >
          <Loader2Icon v-if="importing" class="w-4 h-4 animate-spin" />
          {{ importing ? '导入中...' : '导入' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { XIcon, UploadIcon, DownloadIcon, Loader2Icon, FileIcon, AlertCircleIcon } from 'lucide-vue-next';

const props = defineProps<{
  visible: boolean;
  title: string;
  description?: string;
  accept?: string;
  acceptText?: string;
  importing?: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void;
  (e: 'import', file: File): void;
  (e: 'downloadTemplate'): void;
  (e: 'cancel'): void;
}>();

const fileInput = ref<HTMLInputElement | null>(null);
const uploadFile = ref<File | null>(null);
const uploadFileName = ref('');
const isDragging = ref(false);
const errorMessage = ref('');

// 监听 visible 变化，重置状态
watch(() => props.visible, (newVal) => {
  if (newVal) {
    errorMessage.value = '';
  }
});

const handleFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file) {
    setFile(file);
  }
};

const handleDrop = (e: DragEvent) => {
  isDragging.value = false;
  const file = e.dataTransfer?.files[0];
  if (file) {
    // 检查文件类型
    const acceptTypes = props.accept?.split(',').map(t => t.trim()) || [];
    const isValidType = acceptTypes.length === 0 || acceptTypes.some(type => {
      if (type.includes('*')) {
        return file.type.match(type.replace('/*', '')) || file.name.endsWith(type.replace('/*', ''));
      }
      return file.name.endsWith(type);
    });
    
    if (isValidType) {
      setFile(file);
    } else {
      errorMessage.value = `不支持的文件格式，请上传 ${props.acceptText || '指定格式'} 的文件`;
    }
  }
};

const setFile = (file: File) => {
  uploadFile.value = file;
  uploadFileName.value = file.name;
  errorMessage.value = '';
};

const clearFile = () => {
  uploadFile.value = null;
  uploadFileName.value = '';
  errorMessage.value = '';
  if (fileInput.value) {
    fileInput.value.value = '';
  }
};

const handleDownloadTemplate = () => {
  emit('downloadTemplate');
};

const handleCancel = () => {
  clearFile();
  emit('update:visible', false);
  emit('cancel');
};

const handleImportSubmit = () => {
  if (!uploadFile.value) return;
  errorMessage.value = '';
  emit('import', uploadFile.value);
};

// 暴露方法给父组件设置错误信息
defineExpose({
  setError: (msg: string) => {
    errorMessage.value = msg;
  },
  clearFile
});
</script>
