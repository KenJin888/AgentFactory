<template>
  <Teleport to="body">
    <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div class="bg-white rounded-xl w-full max-w-md shadow-2xl overflow-hidden border border-slate-100 flex flex-col animate-in zoom-in-95 duration-200" @click.stop>
        <!-- Header -->
        <div class="px-6 py-4 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
          <h3 class="text-lg font-semibold text-slate-900">{{ title }}</h3>
          <button @click="handleCancel" class="text-slate-400 hover:text-slate-600 transition-colors p-1 rounded-full hover:bg-slate-100">
            <X :size="20" />
          </button>
        </div>

        <!-- Content -->
        <div class="p-6 text-slate-600 text-sm leading-relaxed whitespace-pre-wrap">
          <slot>{{ message }}</slot>
        </div>

        <!-- Footer -->
        <div class="px-6 py-4 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
          <button 
            @click="handleCancel" 
            class="px-4 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 hover:text-slate-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500 transition-all"
          >
            {{ cancelText }}
          </button>
          <button 
            @click="handleConfirm" 
            :class="[
              'px-4 py-2 text-sm font-medium text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 transition-all shadow-sm',
              type === 'danger' 
                ? 'bg-red-600 hover:bg-red-700 focus:ring-red-500 active:bg-red-800' 
                : 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500 active:bg-blue-800'
            ]"
          >
            {{ confirmText }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { X } from 'lucide-vue-next'

const props = withDefaults(defineProps<{
  visible: boolean
  title?: string
  message?: string
  confirmText?: string
  cancelText?: string
  type?: 'primary' | 'danger'
}>(), {
  title: '确认操作',
  message: '',
  confirmText: '确认',
  cancelText: '取消',
  type: 'primary'
})

const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void
  (e: 'confirm'): void
  (e: 'cancel'): void
}>()

const handleCancel = () => {
  emit('update:visible', false)
  emit('cancel')
}

const handleConfirm = () => {
  emit('confirm')
  emit('update:visible', false)
}
</script>
