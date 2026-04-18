<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
    <div class="bg-white rounded-3xl w-full max-w-2xl shadow-2xl overflow-hidden border border-slate-100 flex flex-col max-h-[90vh]">
      <!-- Header -->
      <div class="px-8 py-6 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
        <div>
          <h2 class="text-xl font-bold flex items-center gap-2 text-slate-900">
            <Wrench :size="20" class="text-blue-500" />
            创建新技能
          </h2>
          <p class="text-sm opacity-70 mt-1">上传技能压缩包或通过 URL 导入</p>
        </div>
        <button type="button" @click="$emit('close')" class="p-2 rounded-full hover:bg-black/10 transition-colors"><X :size="20" /></button>
      </div>

      <!-- Form -->
      <div class="flex-1 overflow-y-auto p-8 custom-scrollbar">
          <form id="skill-form" @submit.prevent="handleSubmit" class="space-y-6">
              <!-- 基础设定 -->
              <div class="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
                  <div>
                      <label class="block text-sm font-bold text-slate-700 mb-2">技能名称</label>
                      <input
                          required
                          v-model="form.name"
                          class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-500"
                          placeholder="例如：数据分析工具"
                      />
                  </div>

                  <!-- 导入方式选择 -->
                  <div>
                      <label class="block text-sm font-bold text-slate-700 mb-2">导入方式</label>
                      <div class="flex gap-4">
                          <label class="flex items-center gap-2 cursor-pointer">
                              <input type="radio" v-model="importMethod" value="file" />
                              <span>上传压缩包</span>
                          </label>
                          <label class="flex items-center gap-2 cursor-pointer">
                              <input type="radio" v-model="importMethod" value="url" />
                              <span>URL 导入</span>
                          </label>
                      </div>
                  </div>

                  <!-- 文件上传 -->
                  <div v-if="importMethod === 'file'">
                      <label class="block text-sm font-bold text-slate-700 mb-2">上传 ZIP 文件</label>
                      <div class="border-2 border-dashed border-slate-200 rounded-2xl p-8 text-center transition-all hover:border-blue-400 hover:bg-blue-50/30">
                          <input
                              type="file"
                              ref="fileInput"
                              @change="handleFileSelect"
                              accept=".zip"
                              class="hidden"
                              required
                          />
                          <div v-if="!selectedFile" @click="triggerFileInput" class="cursor-pointer">
                              <UploadCloud :size="48" class="mx-auto text-slate-400 mb-4" />
                              <p class="text-slate-600 font-medium mb-2">点击或拖拽文件到此区域</p>
                              <p class="text-sm text-slate-500">支持 .zip 格式，包含 SKILL.md 文件</p>
                          </div>
                          <div v-else @click="triggerFileInput" class="cursor-pointer">
                              <FileArchive :size="48" class="mx-auto text-green-500 mb-4" />
                              <p class="text-green-600 font-medium mb-2">{{ selectedFile.name }}</p>
                              <p class="text-sm text-slate-500">点击重新选择文件</p>
                          </div>
                      </div>
                  </div>

                  <!-- URL 导入 -->
                  <div v-if="importMethod === 'url'" class="space-y-4">
                      <div>
                          <label class="block text-sm font-bold text-slate-700 mb-2">ZIP 文件 URL</label>
                          <input
                              type="url"
                              v-model="form.url"
                              class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-500"
                              placeholder="https://example.com/skill.zip"
                              required
                          />
                      </div>
                      <div class="p-4 bg-blue-50 text-blue-700 rounded-xl text-sm">
                          <Info :size="16" class="inline-block mr-2" />
                          确保 URL 指向一个包含 SKILL.md 文件的 ZIP 压缩包
                      </div>
                  </div>

                  <!-- 技能描述 -->
                  <div>
                      <label class="block text-sm font-bold text-slate-700 mb-2">技能描述 (可选)</label>
                      <textarea
                          rows="3"
                          v-model="form.description"
                          class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-500 resize-none"
                          placeholder="简要描述该技能的功能..."
                      />
                  </div>
              </div>

              <div v-if="error" class="p-4 bg-red-50 text-red-600 rounded-xl text-sm flex items-center gap-2">
                  <AlertCircle :size="16" />
                  {{ error }}
              </div>
          </form>
      </div>

      <!-- Footer -->
      <div class="px-8 py-6 border-t border-gray-100 bg-gray-50/50 flex justify-end gap-3">
          <button type="button" @click="$emit('close')" class="px-6 py-3 text-slate-600 font-medium hover:bg-slate-100 rounded-xl">取消</button>
          <button
              form="skill-form"
              type="submit"
              :disabled="loading"
              class="px-8 py-3 text-white font-bold rounded-xl shadow-lg flex items-center gap-2 bg-slate-900"
          >
            <Loader2 v-if="loading" :size="18" class="animate-spin" />
            立即创建
          </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { X, Wrench, UploadCloud, FileArchive, AlertCircle, Loader2, Info } from 'lucide-vue-next'
import AISkillsAPI from '../../services/fastApi/module_ai/ai_skills'
import message from '@/components/common/message'

// 定义组件事件
const emit = defineEmits<{
  'close': []
  'success': []
}>()

// 响应式数据
const loading = ref(false)
const error = ref('')
const importMethod = ref<'file' | 'url'>('file')
const selectedFile = ref<File | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)

const form = reactive({
  name: '',
  url: '',
  description: ''
})

// 触发文件输入
const triggerFileInput = () => {
  if (fileInput.value) {
    fileInput.value.click()
  }
}

// 处理文件选择
const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    selectedFile.value = target.files[0]
  }
}

// 提交表单
const handleSubmit = async () => {
  error.value = ''
  loading.value = true

  try {
    if (importMethod.value === 'file') {
      if (!selectedFile.value) {
        throw new Error('请选择要上传的 ZIP 文件')
      }
      await AISkillsAPI.createSkillWithFile(form.name, selectedFile.value)
    } else {
      if (!form.url) {
        throw new Error('请输入 ZIP 文件的 URL')
      }
      await AISkillsAPI.createSkillWithUrl(form.name, form.url)
    }

    message.success('技能创建成功')
    emit('success')
  } catch (err: any) {
    console.error('Create skill error:', err)
    error.value = err.message || '创建失败'
    message.error(error.value)
  } finally {
    loading.value = false
  }
}
</script>
