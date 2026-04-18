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
              <label class="block text-xs font-medium text-slate-500 mb-1.5">用户姓名</label>
              <input
                v-model="userSearchKeyword"
                type="text"
                placeholder="请输入用户姓名"
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
          <!-- Left: Department Tree -->
          <div class="w-56 border-r border-slate-100 bg-slate-50/30 flex flex-col">
            <div class="px-4 py-3 border-b border-slate-100">
              <h4 class="text-sm font-semibold text-slate-700">组织架构</h4>
            </div>
            <div class="p-3 border-b border-slate-100">
              <div class="relative">
                <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <input
                  v-model="deptSearchKeyword"
                  type="text"
                  placeholder="请输入部门名称"
                  class="w-full pl-8 pr-3 py-1.5 bg-white border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all text-sm"
                />
              </div>
            </div>
            <div class="flex-1 overflow-y-auto p-2">
              <div v-if="loadingDept" class="flex items-center justify-center py-8">
                <Loader2 class="w-5 h-5 text-slate-400 animate-spin" />
              </div>
              <div v-else-if="filteredDeptTree.length === 0" class="text-center py-8 text-slate-400 text-sm">
                暂无匹配部门
              </div>
              <div v-else>
                <template v-for="dept in filteredDeptTree" :key="dept.id">
                  <DeptTreeNode
                    :dept="dept"
                    :selected-dept-id="selectedDeptId"
                    :expanded-depts="expandedDepts"
                    @select="handleDeptSelect"
                    @toggle-expand="toggleDeptExpand"
                  />
                </template>
              </div>
            </div>
          </div>

          <!-- Middle: User List -->
          <div class="flex-1 flex flex-col border-r border-slate-100">
            <div class="px-4 py-3 border-b border-slate-100 flex justify-between items-center">
              <h4 class="text-sm font-semibold text-slate-700">
                人员选择
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
              <div v-if="loadingUser" class="flex items-center justify-center py-12">
                <Loader2 class="w-6 h-6 text-slate-400 animate-spin" />
              </div>
              <div v-else-if="filteredUserList.length === 0" class="text-center py-12 text-slate-400">
                <div class="flex flex-col items-center gap-2">
                  <div class="w-10 h-10 bg-slate-100 rounded-full flex items-center justify-center">
                    <Users :size="20" class="text-slate-300" />
                  </div>
                  <span class="text-sm">暂无数据</span>
                </div>
              </div>
              <div v-else>
                <div
                  v-for="user in filteredUserList"
                  :key="user.id"
                  @click="handleUserSelect(user)"
                  class="flex items-center gap-3 px-4 py-3 border-b border-slate-50 hover:bg-slate-50 cursor-pointer transition-colors"
                  :class="isSelected(user.id) ? 'bg-blue-50/50' : ''"
                >
                  <!-- 勾选框 -->
                  <div
                    class="w-5 h-5 rounded border-2 flex items-center justify-center transition-all"
                    :class="isSelected(user.id) ? 'bg-blue-600 border-blue-600' : 'border-slate-300 bg-white'"
                  >
                    <Check v-if="isSelected(user.id)" class="w-3.5 h-3.5 text-white" />
                  </div>
                  <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 text-sm font-medium">
                    {{ user.name?.charAt(0) || '?' }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="text-sm font-medium text-slate-700 truncate">{{ user.name }}</div>
                    <div class="text-xs text-slate-400 truncate">{{ user.dept_name || user.dept?.name || '暂无部门' }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right: Selected Users -->
          <div class="flex-1 flex flex-col">
            <div class="px-4 py-3 border-b border-slate-100 flex justify-between items-center">
              <h4 class="text-sm font-semibold text-slate-700">
                已选择人员 <span class="text-blue-600">({{ selectedUsers.length }})</span>
              </h4>
              <button
                v-if="selectedUsers.length > 0"
                @click="clearAllSelected"
                class="text-xs text-slate-500 hover:text-red-600 font-medium"
              >
                全部清空
              </button>
            </div>
            <div class="flex-1 overflow-y-auto">
              <div
                v-for="user in selectedUsers"
                :key="user.id"
                class="flex items-center gap-3 px-4 py-3 border-b border-slate-50 hover:bg-slate-50 transition-colors group"
              >
                <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 text-sm font-medium">
                  {{ user.name?.charAt(0) || '?' }}
                </div>
                <div class="flex-1 min-w-0">
                  <div class="text-sm font-medium text-slate-700 truncate">{{ user.name }}</div>
                  <div class="text-xs text-slate-400 truncate">{{ user.dept_name || user.dept?.name || '暂无部门' }}</div>
                </div>
                <button
                  @click.stop="removeSelected(user.id)"
                  class="p-1.5 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors opacity-0 group-hover:opacity-100"
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
            确定 ({{ selectedUsers.length }})
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { X, Search, Users, Loader2, Check, RotateCcw } from 'lucide-vue-next';
import { api } from '@/services/api';
import { useUserStore } from '@/stores/user';
import DeptTreeNode from './DeptTreeNode.vue';

import type { User, Dept } from '@/types/user';

const props = defineProps<{
  visible: boolean;
  title?: string;
  multiple?: boolean;
  initialSelected?: User[];
}>();

const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void;
  (e: 'confirm', users: User[]): void;
  (e: 'cancel'): void;
}>();

const userStore = useUserStore();

// Loading states
const loadingUser = ref(false);
const loadingDept = ref(false);

// Data
const allUsers = ref<User[]>([]);
const deptTree = ref<Dept[]>([]);

// Search keywords
const userSearchKeyword = ref('');
const deptSearchKeyword = ref('');

// Selection state
const selectedUsers = ref<User[]>([]);
const selectedDeptId = ref<number | null>(null);
const expandedDepts = ref<number[]>([]);

// Fetch users
const fetchUsers = async () => {
  loadingUser.value = true;
  try {
    const res = await userStore.getUserList({
      page_no: 1,
      page_size: 1000,
      status: '0'
    });
    let users: any[] = [];
    const resData = res as any;
    if (resData?.items) {
      users = resData.items;
    } else if (resData?.data?.items) {
      users = resData.data.items;
    }
    allUsers.value = users.map((user: any) => ({
      id: user.id,
      name: user.name,
      username: user.username,
      mobile: user.mobile,
      dept_id: user.dept_id,
      dept_name: user.dept_name || user.dept?.name,
      dept: user.dept
    }));
  } catch (error) {
    console.error('Failed to fetch users:', error);
  } finally {
    loadingUser.value = false;
  }
};

// Fetch department tree
const fetchDeptTree = async () => {
  loadingDept.value = true;
  try {
    const res = await api.dept.listDept({});
    if (res?.data) {
      deptTree.value = res.data || [];
    }
  } catch (error) {
    console.error('Failed to fetch dept tree:', error);
  } finally {
    loadingDept.value = false;
  }
};

// Initialize data when visible
watch(() => props.visible, (newVal) => {
  if (newVal) {
    selectedUsers.value = props.initialSelected ? [...props.initialSelected] : [];
    userSearchKeyword.value = '';
    deptSearchKeyword.value = '';
    selectedDeptId.value = null;
    fetchUsers();
    fetchDeptTree();
  }
});

// 递归过滤部门树 - 只显示匹配的节点
const filterDeptTree = (depts: Dept[], keyword: string): Dept[] => {
  const result: Dept[] = [];
  
  for (const dept of depts) {
    const isMatch = dept.name.toLowerCase().includes(keyword);
    
    // 递归处理子部门
    let filteredChildren: Dept[] = [];
    if (dept.children && dept.children.length > 0) {
      filteredChildren = filterDeptTree(dept.children, keyword);
    }
    
    // 如果当前部门匹配，或有匹配的子部门，则保留
    if (isMatch || filteredChildren.length > 0) {
      result.push({
        ...dept,
        children: filteredChildren
      });
    }
  }
  
  return result;
};

const filteredDeptTree = computed(() => {
  if (!deptSearchKeyword.value) return deptTree.value;
  const keyword = deptSearchKeyword.value.toLowerCase();
  return filterDeptTree(deptTree.value, keyword);
});

// Filtered user list - 前端过滤
const filteredUserList = computed(() => {
  let result = allUsers.value;
  
  // Filter by department
  if (selectedDeptId.value) {
    result = result.filter(user => {
      const userDeptId = user.dept_id || user.dept?.id;
      return userDeptId === selectedDeptId.value;
    });
  }
  
  // Filter by user name - 前端模糊查询
  if (userSearchKeyword.value) {
    const keyword = userSearchKeyword.value.toLowerCase();
    result = result.filter(user => 
      user.name?.toLowerCase().includes(keyword) ||
      user.username?.toLowerCase().includes(keyword)
    );
  }
  
  return result;
});

// Check if user is selected
const isSelected = (userId: number) => {
  return selectedUsers.value.some(u => u.id === userId);
};

// Handle department expand/collapse
const toggleDeptExpand = (deptId: number) => {
  const index = expandedDepts.value.indexOf(deptId);
  if (index > -1) {
    expandedDepts.value.splice(index, 1);
  } else {
    expandedDepts.value.push(deptId);
  }
};

// Handle department select
const handleDeptSelect = (dept: Dept) => {
  selectedDeptId.value = selectedDeptId.value === dept.id ? null : dept.id;
};

// Handle user select - 点击用户行
const handleUserSelect = (user: User) => {
  if (props.multiple) {
    // 多选模式：切换选择状态
    if (isSelected(user.id)) {
      removeSelected(user.id);
    } else {
      selectedUsers.value.push(user);
    }
  } else {
    // 单选模式：直接设置为当前用户（替换已选）
    selectedUsers.value = [user];
  }
};

// Remove selected user
const removeSelected = (userId: number) => {
  const index = selectedUsers.value.findIndex(u => u.id === userId);
  if (index > -1) {
    selectedUsers.value.splice(index, 1);
  }
};

// Select all visible users - 仅多选模式
const selectAll = () => {
  if (!props.multiple) return;
  filteredUserList.value.forEach(user => {
    if (!isSelected(user.id)) {
      selectedUsers.value.push(user);
    }
  });
};

// Unselect all visible users - 仅多选模式
const unselectAll = () => {
  if (!props.multiple) return;
  filteredUserList.value.forEach(user => {
    removeSelected(user.id);
  });
};

// Clear all selected
const clearAllSelected = () => {
  selectedUsers.value = [];
};

// Handle search
const handleSearch = () => {
  // 前端搜索，无需额外操作
};

// Handle reset
const handleReset = () => {
  userSearchKeyword.value = '';
  selectedDeptId.value = null;
};

// Handle cancel
const handleCancel = () => {
  emit('update:visible', false);
  emit('cancel');
};

// Handle confirm
const handleConfirm = () => {
  emit('confirm', selectedUsers.value);
  emit('update:visible', false);
};
</script>
