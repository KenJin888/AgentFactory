<template>
  <Teleport to="body">
    <div v-if="visible" class="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
      <div class="bg-white rounded-xl w-full max-w-md shadow-xl flex flex-col">
        <div class="px-6 py-4 border-b border-slate-100 flex justify-between items-center">
          <h3 class="font-semibold text-slate-900">添加自定义模型</h3>
          <button @click="close" class="text-slate-400 hover:text-slate-600">
            <X :size="20" />
          </button>
        </div>
        
        <div class="p-6 space-y-4">
          <div class="space-y-2">
            <label class="text-sm font-medium text-slate-700">模型 ID</label>
            <input 
              type="text" 
              v-model="form.id"
              placeholder="请输入模型 ID"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors"
              @keydown.enter.prevent="handleConfirm"
            />
            <p v-if="error" class="text-xs text-red-500">{{ error }}</p>
          </div>

          <div class="space-y-2">
            <label class="text-sm font-medium text-slate-700">模型类型</label>
            <select 
              v-model="form.type"
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors bg-white"
            >
              <option value="chat">对话 (Chat)</option>
              <option value="embedding">向量 (Embedding)</option>
              <option value="rerank">重排序 (Rerank)</option>
              <option value="imageGeneration">生图 (Image Generation)</option>
            </select>
          </div>
        </div>

        <div class="px-6 py-4 border-t border-slate-100 flex justify-end gap-3 bg-slate-50 rounded-b-xl">
          <button 
            @click="close" 
            class="px-4 py-2 text-slate-600 hover:bg-slate-200 rounded-lg transition-colors"
          >
            取消
          </button>
          <button 
            @click="handleConfirm" 
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="!form.id.trim()"
          >
            确认
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { X } from 'lucide-vue-next'

const props = defineProps<{
  visible: boolean
  existingModels?: string[]
}>()

const emit = defineEmits<{
  'update:visible': [visible: boolean]
  'confirm': [model: { id: string; type: string; isCustom: boolean }]
}>()

const form = reactive({
  id: '',
  type: 'chat'
})

const error = ref('')

watch(() => props.visible, (newVal) => {
  if (newVal) {
    form.id = ''
    form.type = 'chat'
    error.value = ''
  }
})

const close = () => {
  emit('update:visible', false)
}

const handleConfirm = () => {
  const id = form.id.trim()
  if (!id) return

  if (props.existingModels?.includes(id)) {
    error.value = '该模型 ID 已存在'
    return
  }

  emit('confirm', {
    id,
    type: form.type,
    isCustom: true
  })
  close()
}
</script>
