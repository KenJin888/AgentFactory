<template>
  <Teleport to="body">
    <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div class="bg-white rounded-2xl w-full max-w-4xl max-h-[85vh] overflow-hidden shadow-2xl border border-slate-100 flex flex-col animate-in zoom-in-95 duration-200" @click.stop>
        <!-- Header -->
        <div class="px-6 py-4 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
          <h3 class="text-lg font-semibold text-slate-900">
            知识库权限管理 - {{ roleName }}
          </h3>
          <button @click="handleCancel" class="text-slate-400 hover:text-slate-600 transition-colors p-1 rounded-full hover:bg-slate-100">
            <X :size="20" />
          </button>
        </div>

        <!-- Search Bar -->
        <div class="px-6 py-4 border-b border-slate-100 bg-white">
          <div class="relative">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" :size="18" />
            <input
              v-model="searchKeyword"
              type="text"
              placeholder="搜索知识库名称"
              class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all text-sm"
              @keyup.enter="handleSearch"
            />
          </div>
        </div>

        <!-- Content -->
        <div class="flex h-[400px] overflow-hidden">
          <!-- Left: Available Datasets -->
          <div class="flex-1 flex flex-col border-r border-slate-100">
            <div class="px-4 py-3 border-b border-slate-100 flex justify-between items-center bg-slate-50/30">
              <h4 class="text-sm font-semibold text-slate-700">
                可选知识库
                <span class="text-xs text-slate-400 ml-2">({{ filteredAvailableDatasets.length }})</span>
              </h4>
              <div class="flex gap-2">
                <button
                  @click="selectAllAvailable"
                  class="text-xs text-blue-600 hover:text-blue-700 font-medium"
                >
                  全选
                </button>
                <span class="text-slate-300">|</span>
                <button
                  @click="unselectAllAvailable"
                  class="text-xs text-slate-500 hover:text-slate-600 font-medium"
                >
                  取消全选
                </button>
              </div>
            </div>
            <div class="flex-1 overflow-y-auto p-3">
              <div v-if="loading" class="flex items-center justify-center py-12">
                <Loader2 class="w-6 h-6 text-slate-400 animate-spin" />
              </div>
              <div v-else-if="filteredAvailableDatasets.length === 0" class="text-center py-12 text-slate-400">
                <div class="flex flex-col items-center gap-2">
                  <div class="w-10 h-10 bg-slate-100 rounded-full flex items-center justify-center">
                    <Database :size="20" class="text-slate-300" />
                  </div>
                  <span class="text-sm">暂无可用知识库</span>
                </div>
              </div>
              <div v-else class="space-y-2">
                <div
                  v-for="dataset in filteredAvailableDatasets"
                  :key="dataset.id"
                  @click="handleDatasetSelect(dataset)"
                  class="flex items-center gap-3 p-3 rounded-xl border cursor-pointer transition-all hover:bg-slate-50"
                  :class="isSelected(dataset.id) ? 'bg-blue-50/50 border-blue-200' : 'bg-white border-slate-100'"
                >
                  <!-- 勾选框 -->
                  <div
                    class="w-5 h-5 rounded border-2 flex items-center justify-center transition-all flex-shrink-0"
                    :class="isSelected(dataset.id) ? 'bg-blue-600 border-blue-600' : 'border-slate-300 bg-white'"
                  >
                    <Check v-if="isSelected(dataset.id)" class="w-3.5 h-3.5 text-white" />
                  </div>
                  <div class="w-8 h-8 rounded-lg bg-indigo-100 flex items-center justify-center text-indigo-600 flex-shrink-0">
                    <Database :size="16" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="text-sm font-medium text-slate-700 truncate">{{ dataset.name }}</div>
                    <div class="text-xs text-slate-400 truncate">
                      {{ dataset.document_count || 0 }} 文档
                      <span v-if="dataset.description" class="ml-1">· {{ dataset.description }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Middle: Actions -->
          <div class="w-16 flex flex-col items-center justify-center gap-3 bg-slate-50/30 px-2">
            <button
              @click="addToSelected"
              :disabled="availableSelection.length === 0"
              class="w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-sm"
              title="添加选中"
            >
              <ChevronRight :size="20" />
            </button>
            <button
              @click="removeFromSelected"
              :disabled="selectedSelection.length === 0"
              class="w-10 h-10 rounded-full bg-slate-200 text-slate-600 flex items-center justify-center hover:bg-slate-300 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
              title="移除选中"
            >
              <ChevronLeft :size="20" />
            </button>
          </div>

          <!-- Right: Selected Datasets with Permission -->
          <div class="flex-1 flex flex-col bg-slate-50/30">
            <div class="px-4 py-3 border-b border-slate-100 flex justify-between items-center">
              <h4 class="text-sm font-semibold text-slate-700">
                已授权知识库
                <span class="text-blue-600">({{ selectedDatasetsWithPerm.length }})</span>
              </h4>
              <button
                v-if="selectedDatasetsWithPerm.length > 0"
                @click="clearAllSelected"
                class="text-xs text-slate-500 hover:text-red-600 font-medium"
              >
                全部清空
              </button>
            </div>
            <div class="flex-1 overflow-y-auto p-3">
              <div v-if="selectedDatasetsWithPerm.length === 0" class="text-center py-12 text-slate-400">
                <div class="flex flex-col items-center gap-2">
                  <div class="w-10 h-10 bg-slate-100 rounded-full flex items-center justify-center">
                    <Shield :size="20" class="text-slate-300" />
                  </div>
                  <span class="text-sm">暂无授权知识库</span>
                  <span class="text-xs text-slate-400">从左侧面板选择知识库</span>
                </div>
              </div>
              <div v-else class="space-y-2">
                <div
                  v-for="item in selectedDatasetsWithPerm"
                  :key="item.dataset.id"
                  @click="toggleSelectedSelection(item.dataset.id)"
                  class="flex items-center gap-3 p-3 rounded-xl border cursor-pointer transition-all"
                  :class="isSelectedInSelected(item.dataset.id) ? 'bg-blue-50 border-blue-200' : 'bg-white border-slate-200'"
                >
                  <!-- 勾选框 -->
                  <div
                    class="w-5 h-5 rounded border-2 flex items-center justify-center transition-all flex-shrink-0"
                    :class="isSelectedInSelected(item.dataset.id) ? 'bg-blue-600 border-blue-600' : 'border-slate-300 bg-white'"
                  >
                    <Check v-if="isSelectedInSelected(item.dataset.id)" class="w-3.5 h-3.5 text-white" />
                  </div>
                  <div class="w-8 h-8 rounded-lg bg-indigo-100 flex items-center justify-center text-indigo-600 flex-shrink-0">
                    <Database :size="16" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="text-sm font-medium text-slate-700 truncate">{{ item.dataset.name }}</div>
                    <div class="flex items-center gap-2 mt-1">
                      <select
                        v-model="item.permission"
                        @click.stop
                        class="text-xs px-2 py-1 bg-white border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                      >
                        <option value="只读">只读</option>
                        <option value="读写">读写</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="px-6 py-4 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
          <button
            @click="handleCancel"
            class="px-5 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-xl hover:bg-slate-50 hover:text-slate-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500 transition-all"
          >
            取消
          </button>
          <button
            @click="handleConfirm"
            :disabled="saving"
            class="px-5 py-2 text-sm font-medium text-white bg-blue-600 rounded-xl hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all shadow-sm flex items-center gap-2"
          >
            <Loader2 v-if="saving" class="w-4 h-4 animate-spin" />
            {{ saving ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { X, Search, Database, Check, ChevronRight, ChevronLeft, Shield, Loader2 } from 'lucide-vue-next';
import { api } from '@/services/api';
import AiRoleDatasetAPI from '@/services/fastApi/module_ai/ai_role_dataset';
import message from '@/components/common/message';

interface Dataset {
  id: string;
  name: string;
  description?: string;
  document_count?: number;
}

interface DatasetWithPermission {
  dataset: Dataset;
  permission: string;
}

const props = defineProps<{
  visible: boolean;
  roleId: number;
  roleName: string;
}>();

const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void;
  (e: 'confirm'): void;
  (e: 'cancel'): void;
}>();

// Loading states
const loading = ref(false);
const saving = ref(false);

// Data
const allDatasets = ref<Dataset[]>([]);
const selectedDatasetsWithPerm = ref<DatasetWithPermission[]>([]);

// Store original permissions for comparison
const originalPermissions = ref<Map<string, { id: number; permission: string }>>(new Map());

// Search keywords
const searchKeyword = ref('');

// Selection state
const availableSelection = ref<string[]>([]);
const selectedSelection = ref<string[]>([]);

// Fetch all datasets
const fetchDatasets = async () => {
  loading.value = true;
  try {
    const res = await api.knowledge.listDatasets({ page: 1, page_size: 1000 });
    allDatasets.value = (res.data || []).map((d: any) => ({
      id: d.id,
      name: d.name,
      description: d.description,
      document_count: d.document_count || 0
    }));
  } catch (error) {
    console.error('Failed to fetch datasets:', error);
    message.error('加载知识库列表失败');
  } finally {
    loading.value = false;
  }
};

// Fetch role's current dataset permissions
const fetchRoleDatasetPermissions = async () => {
  if (!props.roleId) return;
  try {
    const res = await AiRoleDatasetAPI.listAiRoleDataset({
      page_no: 1,
      page_size: 1000,
      role_id: String(props.roleId)
    });
    const permissions = res.data?.data?.items || [];

    // Store original permissions for comparison
    originalPermissions.value = new Map();
    permissions.forEach((perm: any) => {
      if (perm.datasets_id && perm.id) {
        originalPermissions.value.set(perm.datasets_id, {
          id: perm.id,
          permission: perm.permission || '只读'
        });
      }
    });

    // Map permissions to datasets
    selectedDatasetsWithPerm.value = permissions
      .map((perm: any) => {
        const dataset = allDatasets.value.find(d => d.id === perm.datasets_id);
        if (dataset) {
          return {
            dataset,
            permission: perm.permission || '只读'
          };
        }
        return null;
      })
      .filter((item): item is DatasetWithPermission => item !== null);
  } catch (error) {
    console.error('Failed to fetch role dataset permissions:', error);
  }
};

// Initialize data when visible
watch(() => props.visible, async (newVal) => {
  if (newVal) {
    availableSelection.value = [];
    selectedSelection.value = [];
    searchKeyword.value = '';
    await fetchDatasets();
    await fetchRoleDatasetPermissions();
  }
});

// Filtered available datasets (not selected)
const filteredAvailableDatasets = computed(() => {
  const selectedIds = new Set(selectedDatasetsWithPerm.value.map(item => item.dataset.id));
  let result = allDatasets.value.filter(d => !selectedIds.has(d.id));
  
  // Filter by search keyword
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase();
    result = result.filter(d => 
      d.name.toLowerCase().includes(keyword) ||
      (d.description && d.description.toLowerCase().includes(keyword))
    );
  }
  
  return result;
});

// Check if dataset is selected in available list
const isSelected = (datasetId: string) => {
  return availableSelection.value.includes(datasetId);
};

// Check if dataset is selected in selected list
const isSelectedInSelected = (datasetId: string) => {
  return selectedSelection.value.includes(datasetId);
};

// Handle dataset select in available list
const handleDatasetSelect = (dataset: Dataset) => {
  const index = availableSelection.value.indexOf(dataset.id);
  if (index > -1) {
    availableSelection.value.splice(index, 1);
  } else {
    availableSelection.value.push(dataset.id);
  }
};

// Toggle selection in selected list
const toggleSelectedSelection = (datasetId: string) => {
  const index = selectedSelection.value.indexOf(datasetId);
  if (index > -1) {
    selectedSelection.value.splice(index, 1);
  } else {
    selectedSelection.value.push(datasetId);
  }
};

// Select all available datasets
const selectAllAvailable = () => {
  availableSelection.value = filteredAvailableDatasets.value.map(d => d.id);
};

// Unselect all available datasets
const unselectAllAvailable = () => {
  availableSelection.value = [];
};

// Add selected datasets to selected list
const addToSelected = () => {
  const datasetsToAdd = allDatasets.value.filter(d => availableSelection.value.includes(d.id));
  datasetsToAdd.forEach(dataset => {
    selectedDatasetsWithPerm.value.push({
      dataset,
      permission: '只读'
    });
  });
  availableSelection.value = [];
};

// Remove selected datasets from selected list
const removeFromSelected = () => {
  selectedDatasetsWithPerm.value = selectedDatasetsWithPerm.value.filter(
    item => !selectedSelection.value.includes(item.dataset.id)
  );
  selectedSelection.value = [];
};

// Clear all selected datasets
const clearAllSelected = () => {
  selectedDatasetsWithPerm.value = [];
  selectedSelection.value = [];
};

// Handle search
const handleSearch = () => {
  // Frontend search, no additional action needed
};

// Handle cancel
const handleCancel = () => {
  emit('update:visible', false);
  emit('cancel');
};

// Handle confirm - save permissions
const handleConfirm = async () => {
  saving.value = true;
  try {
    // Build current selection map
    const currentSelection = new Map<string, string>();
    selectedDatasetsWithPerm.value.forEach(item => {
      currentSelection.set(item.dataset.id, item.permission);
    });

    // Determine what to add, update, and delete
    const toAdd: { datasets_id: string; permission: string }[] = [];
    const toUpdate: { id: number; datasets_id: string; permission: string }[] = [];
    const toDelete: number[] = [];

    // Check for additions and updates
    currentSelection.forEach((permission, datasetId) => {
      const original = originalPermissions.value.get(datasetId);
      if (!original) {
        // New permission
        toAdd.push({ datasets_id: datasetId, permission });
      } else if (original.permission !== permission) {
        // Permission changed, use update
        toUpdate.push({ id: original.id, datasets_id: datasetId, permission });
      }
    });

    // Check for deletions
    originalPermissions.value.forEach((data, datasetId) => {
      if (!currentSelection.has(datasetId)) {
        toDelete.push(data.id);
      }
    });

    // Execute operations
    // 1. Delete removed permissions
    if (toDelete.length > 0) {
      await AiRoleDatasetAPI.deleteAiRoleDataset(toDelete);
    }

    // 2. Update changed permissions
    for (const item of toUpdate) {
      await AiRoleDatasetAPI.updateAiRoleDataset(item.id, {
        role_id: String(props.roleId),
        datasets_id: item.datasets_id,
        permission: item.permission
      });
    }

    // 3. Create new permissions
    for (const item of toAdd) {
      await AiRoleDatasetAPI.createAiRoleDataset({
        role_id: String(props.roleId),
        datasets_id: item.datasets_id,
        permission: item.permission
      });
    }

    message.success('知识库权限保存成功');
    emit('confirm');
    emit('update:visible', false);
  } catch (error: any) {
    console.error('Failed to save dataset permissions:', error);
    message.error(error.data?.msg || '保存失败');
  } finally {
    saving.value = false;
  }
};
</script>
