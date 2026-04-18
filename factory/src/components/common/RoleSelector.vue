<template>
  <Teleport to="body">
    <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div class="bg-white rounded-2xl w-full max-w-4xl h-[80vh] min-h-[450px] overflow-hidden shadow-2xl border border-slate-100 flex flex-col animate-in zoom-in-95 duration-200" @click.stop>
        <!-- Header -->
        <div class="px-6 py-4 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
          <h3 class="text-lg font-semibold text-slate-900">{{ title }}</h3>
          <button @click="handleCancel" class="text-slate-400 hover:text-slate-600 transition-colors p-1 rounded-full hover:bg-slate-100">
            <X :size="20" />
          </button>
        </div>

        <!-- Search Bar -->
        <div class="px-6 py-4 border-b border-slate-100 bg-white">
          <div class="flex gap-4">
            <div class="flex-1">
              <label class="block text-xs font-medium text-slate-500 mb-1.5">角色名称</label>
              <input
                v-model="searchKeyword"
                type="text"
                placeholder="请输入角色名称"
                class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all text-sm"
                @keyup.enter="handleSearch"
              />
            </div>
            <div class="flex items-end gap-2">
              <button
                @click="handleSearch"
                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all shadow-sm flex items-center gap-1.5 text-sm font-medium"
              >
                <Search :size="14" />
                搜索
              </button>
              <button
                @click="handleReset"
                class="px-4 py-2 border border-slate-200 text-slate-600 rounded-lg hover:bg-slate-50 transition-all text-sm font-medium"
              >
                <RotateCcw :size="14" class="inline mr-1" />
                重置
              </button>
            </div>
          </div>
        </div>

        <!-- Content -->
        <div class="flex flex-1 overflow-hidden">
          <!-- Left: Role List -->
          <div class="flex-1 flex flex-col border-r border-slate-100">
            <div class="px-4 py-3 border-b border-slate-100 flex justify-between items-center">
              <h4 class="text-sm font-semibold text-slate-700">
                角色选择
                <span v-if="multiple" class="text-xs text-slate-400 ml-2">(多选)</span>
              </h4>
              <div v-if="multiple" class="flex gap-2">
                <button
                  @click="selectAll"
                  class="text-xs text-blue-600 hover:text-blue-700 font-medium"
                >
                  全选
                </button>
                <span class="text-slate-300">|</span>
                <button
                  @click="unselectAll"
                  class="text-xs text-slate-500 hover:text-slate-600 font-medium"
                >
                  取消全选
                </button>
              </div>
            </div>
            <div class="flex-1 overflow-y-auto">
              <div v-if="loading" class="flex items-center justify-center py-12">
                <Loader2 class="w-6 h-6 text-slate-400 animate-spin" />
              </div>
              <div v-else-if="filteredRoleList.length === 0" class="text-center py-12 text-slate-400">
                <div class="flex flex-col items-center gap-2">
                  <div class="w-10 h-10 bg-slate-100 rounded-full flex items-center justify-center">
                    <Shield :size="20" class="text-slate-300" />
                  </div>
                  <span class="text-sm">暂无数据</span>
                </div>
              </div>
              <div v-else>
                <div
                  v-for="role in filteredRoleList"
                  :key="role.id"
                  @click="handleRoleSelect(role)"
                  class="flex items-center gap-3 px-4 py-3 border-b border-slate-50 hover:bg-slate-50 cursor-pointer transition-colors"
                  :class="isSelected(role.id) ? 'bg-blue-50/50' : ''"
                >
                  <!-- 勾选框 -->
                  <div
                    class="w-5 h-5 rounded border-2 flex items-center justify-center transition-all"
                    :class="isSelected(role.id) ? 'bg-blue-600 border-blue-600' : 'border-slate-300 bg-white'"
                  >
                    <Check v-if="isSelected(role.id)" class="w-3.5 h-3.5 text-white" />
                  </div>
                  <div class="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center text-purple-600 text-sm font-medium">
                    {{ role.name?.charAt(0) || '?' }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="text-sm font-medium text-slate-700 truncate">{{ role.name }}</div>
                    <div class="text-xs text-slate-400 truncate">{{ role.code || '暂无编码' }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right: Selected Roles -->
          <div class="flex-1 bg-slate-50/30 flex flex-col">
            <div class="px-4 py-3 border-b border-slate-100 flex justify-between items-center">
              <h4 class="text-sm font-semibold text-slate-700">
                已选择角色 <span class="text-blue-600">({{ selectedRoles.length }})</span>
              </h4>
              <button
                v-if="selectedRoles.length > 0"
                @click="clearAllSelected"
                class="text-xs text-slate-500 hover:text-red-600 font-medium"
              >
                全部清空
              </button>
            </div>
            <div class="flex-1 overflow-y-auto">
              <div
                v-for="role in selectedRoles"
                :key="role.id"
                class="flex items-center gap-3 px-4 py-3 border-b border-slate-100 hover:bg-slate-100/50 transition-colors group"
              >
                <div class="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center text-purple-600 text-sm font-medium">
                  {{ role.name?.charAt(0) || '?' }}
                </div>
                <div class="flex-1 min-w-0">
                  <div class="text-sm font-medium text-slate-700 truncate">{{ role.name }}</div>
                  <div class="text-xs text-slate-400 truncate">{{ role.code || '暂无编码' }}</div>
                </div>
                <button
                  @click.stop="removeSelected(role.id)"
                  class="p-1 hover:bg-red-50 hover:text-red-600 rounded-full transition-colors opacity-0 group-hover:opacity-100 text-slate-400 ml-1"
                >
                  <X :size="16" />
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="px-6 py-4 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
          <button
            @click="handleCancel"
            class="px-5 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 hover:text-slate-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500 transition-all"
          >
            取消
          </button>
          <button
            @click="handleConfirm"
            class="px-5 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all shadow-sm"
          >
            确定 ({{ selectedRoles.length }})
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { X, Search, Shield, Loader2, Check, RotateCcw } from 'lucide-vue-next';
import { api } from '@/services/api';

export interface Role {
  id: number;
  name: string;
  code?: string;
  status?: string;
  order?: number;
}

const props = defineProps<{
  visible: boolean;
  title?: string;
  multiple?: boolean;
  initialSelected?: Role[];
}>();

const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void;
  (e: 'confirm', roles: Role[]): void;
  (e: 'cancel'): void;
}>();

// Loading state
const loading = ref(false);

// Data
const allRoles = ref<Role[]>([]);

// Search keyword
const searchKeyword = ref('');

// Selection state
const selectedRoles = ref<Role[]>([]);

// Fetch roles
const fetchRoles = async () => {
  loading.value = true;
  try {
    const res = await api.role.listRole({
      page_no: 1,
      page_size: 1000,
    });
    let roles: any[] = [];
    const resData = res as any;
    if (resData?.items) {
      roles = resData.items;
    } else if (resData?.data?.items) {
      roles = resData.data.items;
    }
    allRoles.value = roles.map((role: any) => ({
      id: role.id,
      name: role.name,
      code: role.code,
      status: role.status,
      order: role.order
    }));
  } catch (error) {
    console.error('Failed to fetch roles:', error);
  } finally {
    loading.value = false;
  }
};

// Initialize data when visible
watch(() => props.visible, (newVal) => {
  if (newVal) {
    selectedRoles.value = props.initialSelected ? [...props.initialSelected] : [];
    searchKeyword.value = '';
    fetchRoles();
  }
});

// Filtered role list - 前端过滤
const filteredRoleList = computed(() => {
  let result = allRoles.value;
  
  // Filter by role name - 前端模糊查询
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase();
    result = result.filter(role => 
      role.name?.toLowerCase().includes(keyword) ||
      role.code?.toLowerCase().includes(keyword)
    );
  }
  
  return result;
});

// Check if role is selected
const isSelected = (roleId: number) => {
  return selectedRoles.value.some(r => r.id === roleId);
};

// Handle role select - 点击角色行
const handleRoleSelect = (role: Role) => {
  if (props.multiple) {
    // 多选模式：切换选择状态
    if (isSelected(role.id)) {
      removeSelected(role.id);
    } else {
      selectedRoles.value.push(role);
    }
  } else {
    // 单选模式：直接设置为当前角色（替换已选）
    selectedRoles.value = [role];
  }
};

// Remove selected role
const removeSelected = (roleId: number) => {
  const index = selectedRoles.value.findIndex(r => r.id === roleId);
  if (index > -1) {
    selectedRoles.value.splice(index, 1);
  }
};

// Select all visible roles - 仅多选模式
const selectAll = () => {
  if (!props.multiple) return;
  filteredRoleList.value.forEach(role => {
    if (!isSelected(role.id)) {
      selectedRoles.value.push(role);
    }
  });
};

// Unselect all visible roles - 仅多选模式
const unselectAll = () => {
  if (!props.multiple) return;
  filteredRoleList.value.forEach(role => {
    removeSelected(role.id);
  });
};

// Clear all selected
const clearAllSelected = () => {
  selectedRoles.value = [];
};

// Handle search
const handleSearch = () => {
  // 前端搜索，无需额外操作
};

// Handle reset
const handleReset = () => {
  searchKeyword.value = '';
};

// Handle cancel
const handleCancel = () => {
  emit('update:visible', false);
  emit('cancel');
};

// Handle confirm
const handleConfirm = () => {
  emit('confirm', selectedRoles.value);
  emit('update:visible', false);
};
</script>
