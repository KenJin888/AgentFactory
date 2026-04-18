<template>
  <div v-if="visible" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden">
      <div class="px-6 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
        <h2 class="text-xl font-bold text-slate-900">{{ title }}</h2>
        <button @click="handleCancel" class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all">
          <XIcon class="w-5 h-5" />
        </button>
      </div>
      <div class="p-6 space-y-5 max-h-[60vh] overflow-y-auto">
        <!-- 导出范围 -->
        <div>
          <label class="block text-sm font-semibold text-slate-700 mb-3">导出范围</label>
          <div class="flex gap-3">
            <button
              @click="exportOptions.range = 'current'"
              :class="exportOptions.range === 'current' ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-slate-700 border-slate-200 hover:border-slate-300'"
              class="flex-1 px-4 py-2.5 border rounded-xl transition-all text-sm font-medium"
            >
              当前页
            </button>
            <button
              @click="exportOptions.range = 'all'"
              :class="exportOptions.range === 'all' ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-slate-700 border-slate-200 hover:border-slate-300'"
              class="flex-1 px-4 py-2.5 border rounded-xl transition-all text-sm font-medium"
            >
              全部数据
            </button>
            <button
              v-if="selectedCount && selectedCount > 0"
              @click="exportOptions.range = 'selected'"
              :class="exportOptions.range === 'selected' ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-slate-700 border-slate-200 hover:border-slate-300'"
              class="flex-1 px-4 py-2.5 border rounded-xl transition-all text-sm font-medium"
            >
              选中项 ({{ selectedCount }})
            </button>
          </div>
        </div>

        <!-- 文件格式 -->
        <div>
          <label class="block text-sm font-semibold text-slate-700 mb-3">文件格式</label>
          <div class="flex gap-3">
            <button
              @click="exportOptions.format = 'xlsx'"
              :class="exportOptions.format === 'xlsx' ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-slate-700 border-slate-200 hover:border-slate-300'"
              class="flex-1 px-4 py-2.5 border rounded-xl transition-all text-sm font-medium flex items-center justify-center gap-2"
            >
              <FileSpreadsheetIcon class="w-4 h-4" />
              Excel (.xlsx)
            </button>
            <button
              @click="exportOptions.format = 'csv'"
              :class="exportOptions.format === 'csv' ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-slate-700 border-slate-200 hover:border-slate-300'"
              class="flex-1 px-4 py-2.5 border rounded-xl transition-all text-sm font-medium flex items-center justify-center gap-2"
            >
              <FileTextIcon class="w-4 h-4" />
              CSV (.csv)
            </button>
          </div>
        </div>

        <!-- 导出字段 -->
        <div>
          <div class="flex items-center justify-between mb-3">
            <label class="block text-sm font-semibold text-slate-700">导出字段</label>
            <div class="flex gap-2">
              <button
                @click="selectAllFields"
                class="text-xs text-blue-600 hover:text-blue-700 font-medium"
              >
                全选
              </button>
              <span class="text-slate-300">|</span>
              <button
                @click="unselectAllFields"
                class="text-xs text-slate-500 hover:text-slate-600 font-medium"
              >
                取消全选
              </button>
            </div>
          </div>
          <div class="space-y-2 max-h-48 overflow-y-auto">
            <label
              v-for="(field, index) in internalFields"
              :key="field.key"
              class="flex items-center gap-2.5 cursor-pointer p-2.5 rounded-xl border border-slate-100 hover:border-blue-200 hover:bg-blue-50/20 transition-all"
            >
              <input
                type="checkbox"
                :checked="field.checked"
                @change="toggleField(index)"
                class="rounded border-slate-300 text-blue-600 focus:ring-blue-500 w-4 h-4"
              />
              <span class="text-sm text-slate-700">{{ field.label }}</span>
            </label>
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
          @click="handleConfirm"
          class="px-5 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-all flex items-center gap-2 shadow-sm"
        >
          <DownloadIcon class="w-4 h-4" />
          确认导出
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, ref } from 'vue';
import { XIcon, FileSpreadsheetIcon, FileTextIcon, DownloadIcon } from 'lucide-vue-next';

export interface ExportField {
  key: string;
  label: string;
  checked: boolean;
}

export interface ExportOptions {
  range: 'current' | 'all' | 'selected';
  format: 'xlsx' | 'csv';
  fields: string[];
}

const props = defineProps<{
  visible: boolean;
  title: string;
  fields: ExportField[];
  selectedCount?: number;
}>();

const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void;
  (e: 'confirm', options: ExportOptions): void;
  (e: 'cancel'): void;
}>();

const internalFields = ref<ExportField[]>([]);

const exportOptions = reactive<ExportOptions>({
  range: 'current',
  format: 'xlsx',
  fields: []
});

watch(() => props.visible, (newVal) => {
  if (newVal) {
    exportOptions.range = 'current';
    exportOptions.format = 'xlsx';
    internalFields.value = props.fields.map(f => ({ ...f }));
  }
});

const toggleField = (index: number) => {
  const field = internalFields.value[index];
  internalFields.value[index] = { ...field, checked: !field.checked };
};

const selectAllFields = () => {
  internalFields.value = internalFields.value.map(field => ({ ...field, checked: true }));
};

const unselectAllFields = () => {
  internalFields.value = internalFields.value.map(field => ({ ...field, checked: false }));
};

const handleCancel = () => {
  emit('update:visible', false);
  emit('cancel');
};

const handleConfirm = () => {
  const selectedFields = internalFields.value.filter(f => f.checked);
  if (selectedFields.length === 0) {
    return;
  }
  exportOptions.fields = selectedFields.map(f => f.key);
  emit('confirm', { ...exportOptions });
  emit('update:visible', false);
};
</script>
