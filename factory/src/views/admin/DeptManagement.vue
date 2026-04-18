<template>
  <div class="min-h-screen bg-slate-50 p-8 overflow-y-auto">
    <div class="max-w-6xl mx-auto">
      <!-- 顶部导航栏 -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">部门管理</h1>
          <p class="mt-1 text-sm text-slate-500">维护组织架构与部门信息。</p>
        </div>
        <div class="flex gap-3">
          <button
            @click="handleAdd()"
            class="px-6 py-3 bg-slate-900 text-white rounded-xl font-bold hover:bg-slate-800 shadow-lg flex items-center gap-2 transition-transform active:scale-95"
          >
              <PlusIcon :size="20" /> 新增部门
          </button>
        </div>
      </div>

      <!-- Search & Filter Card -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 mb-6 overflow-hidden">
        <div class="p-6">
          <!-- 第一行：四个等分列 -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
            <!-- 部门名称 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">部门名称</label>
              <div class="relative">
                <input
                  v-model="queryParams.name"
                  type="text"
                  placeholder="请输入部门名称"
                  class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                  @keyup.enter="handleSearch"
                />
                <BuildingIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              </div>
            </div>
            <!-- 状态 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">状态</label>
              <select 
                v-model="queryParams.status" 
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all appearance-none cursor-pointer"
              >
                <option value="">全部</option>
                <option value="0">启用</option>
                <option value="1">停用</option>
              </select>
            </div>
            <!-- 占位 -->
            <div></div>
            <!-- 操作按钮列 -->
            <div class="flex items-end">
              <div class="flex items-center gap-2 min-w-[280px]">
                <button
                  @click="handleSearch"
                  class="flex-1 bg-slate-900 text-white px-4 py-2.5 rounded-xl hover:bg-slate-800 transition-all shadow-sm hover:shadow flex items-center justify-center gap-2 whitespace-nowrap"
                >
                  <SearchIcon class="w-4 h-4" />
                  查询
                </button>
                <button
                  @click="handleReset"
                  class="flex-1 bg-white text-slate-600 border border-slate-200 px-4 py-2.5 rounded-xl hover:bg-slate-50 hover:border-slate-300 transition-all whitespace-nowrap"
                >
                  重置
                </button>
                <button
                  @click="isExpand = !isExpand"
                  class="px-3 py-2.5 text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-xl transition-all flex items-center justify-center gap-1 flex-shrink-0"
                  :title="isExpand ? '收起筛选' : '展开筛选'"
                >
                  <ChevronUpIcon v-if="isExpand" class="w-4 h-4" />
                  <ChevronDownIcon v-else class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>

          <!-- 展开的搜索条件 -->
          <div v-if="isExpand" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mt-5 pt-5 border-t border-slate-100">
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-slate-700 mb-2">创建时间</label>
              <div class="flex items-center gap-3">
                <input
                  v-model="queryParams.start_time"
                  type="date"
                  class="flex-1 px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
                <span class="text-slate-400">至</span>
                <input
                  v-model="queryParams.end_time"
                  type="date"
                  class="flex-1 px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Dept Table (Tree) -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
        <!-- 表格工具栏 -->
        <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
          <div class="flex items-center gap-3">
            <div class="flex items-center gap-3 text-sm">
              <span class="text-slate-500">已选择</span>
              <span class="font-semibold text-slate-900 bg-blue-50 px-2.5 py-0.5 rounded-full">{{ selectedIds.length }}</span>
              <span class="text-slate-500">项</span>
            </div>
            <!-- 批量操作按钮 -->
            <div v-if="selectedIds.length > 0" class="flex items-center gap-1 ml-4 pl-4 border-l border-slate-200">
              <button
                @click="handleBatchDelete"
                class="p-2 text-slate-700 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all"
                title="批量删除"
              >
                <TrashIcon class="w-4 h-4" />
              </button>
              <button
                @click="handleBatchStatus('0')"
                class="p-2 text-slate-700 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg transition-all"
                title="批量启用"
              >
                <PlayIcon class="w-4 h-4" />
              </button>
              <button
                @click="handleBatchStatus('1')"
                class="p-2 text-slate-700 hover:text-amber-600 hover:bg-amber-50 rounded-lg transition-all"
                title="批量停用"
              >
                <PauseIcon class="w-4 h-4" />
              </button>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <button
              @click="handleRefresh"
              class="p-2.5 text-slate-600 hover:bg-slate-100 rounded-xl transition-all"
              title="刷新"
            >
              <RefreshCwIcon class="w-5 h-5" />
            </button>
            <div class="relative" ref="columnSettingsRef">
              <button
                @click.stop="showColumnSettings = !showColumnSettings"
                class="p-2.5 text-slate-600 hover:bg-slate-100 rounded-xl transition-all"
                title="列设置"
              >
                <SettingsIcon class="w-5 h-5" />
              </button>
              <div 
                v-if="showColumnSettings"
                ref="columnSettingsDropdownRef"
                class="fixed bg-white border border-slate-200 rounded-xl shadow-xl z-50 p-4 min-w-[180px]"
                :style="{ top: dropdownPosition.top + 'px', right: dropdownPosition.right + 'px' }"
                @click.stop
              >
                <div class="text-sm font-semibold text-slate-800 mb-3">列展示</div>
                <div class="space-y-2 max-h-48 overflow-y-auto">
                  <label 
                    v-for="col in columnOptions" 
                    :key="col.key" 
                    class="flex items-center gap-3 cursor-pointer p-1.5 rounded-lg hover:bg-slate-50 transition-colors"
                  >
                    <input 
                      type="checkbox" 
                      v-model="col.visible" 
                      class="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span class="text-sm text-slate-600">{{ col.label }}</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="overflow-x-auto">
          <table class="w-full text-sm" style="min-width: 900px;">
            <thead class="bg-slate-50 text-slate-600 font-medium border-b border-slate-200">
              <tr>
                <th class="px-5 py-4 w-12 text-center">
                  <input type="checkbox" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" @change="toggleAllSelection" :checked="isAllSelected" />
                </th>
                <th v-if="getColumnVisible('index')" class="px-5 py-4 text-center">序号</th>
                <th v-if="getColumnVisible('name')" class="px-5 py-4 text-center">部门名称</th>
                <th v-if="getColumnVisible('code')" class="px-5 py-4 text-center">部门编码</th>
                <th v-if="getColumnVisible('status')" class="px-5 py-4 text-center">状态</th>
                <th v-if="getColumnVisible('order')" class="px-5 py-4 text-center">排序</th>
                <th v-if="getColumnVisible('description')" class="px-5 py-4 text-center">描述</th>
                <th v-if="getColumnVisible('created_time')" class="px-5 py-4 text-center">创建时间</th>
                <th v-if="getColumnVisible('updated_time')" class="px-5 py-4 text-center">更新时间</th>
                <th v-if="getColumnVisible('action')" class="px-5 py-4 text-center fixed-col">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <template v-if="loading">
                <tr>
                  <td :colspan="visibleColumnCount" class="px-6 py-12 text-center text-slate-400">
                    <div class="flex flex-col items-center gap-3">
                      <Loader2Icon class="w-8 h-8 animate-spin text-blue-500" />
                      <span>加载中...</span>
                    </div>
                  </td>
                </tr>
              </template>
              <template v-else-if="deptList.length === 0">
                <tr>
                  <td :colspan="visibleColumnCount" class="px-6 py-12 text-center text-slate-400">
                    <div class="flex flex-col items-center gap-3">
                      <InboxIcon class="w-12 h-12 text-slate-300" />
                      <span>暂无数据</span>
                    </div>
                  </td>
                </tr>
              </template>
              <template v-else>
                <DeptTreeRow 
                  v-for="dept in deptList"
                  :key="dept.id" 
                  :dept="dept" 
                  :selected-ids="selectedIds"
                  :column-options="columnOptions"
                  @toggle-select="handleToggleSelect"
                  @add-child="handleAddChild"
                  @view="handleView"
                  @edit="handleEdit"
                  @delete="handleDelete"
                />
              </template>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="dialogVisible" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg max-h-[90vh] overflow-hidden flex flex-col">
        <div class="px-6 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
          <h2 class="text-xl font-bold text-slate-900">{{ dialogTitle }}</h2>
          <button @click="closeDialog" class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all">
            <XIcon class="w-5 h-5" />
          </button>
        </div>
        
        <!-- Detail View -->
        <div v-if="dialogType === 'detail'" class="p-6">
          <div class="grid grid-cols-2 gap-5">
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">部门名称</div>
              <div class="font-semibold text-slate-900">{{ detailData.name }}</div>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">部门编码</div>
              <div class="font-medium text-slate-900">{{ detailData.code || '-' }}</div>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">上级部门</div>
              <div class="font-medium text-slate-900">{{ detailData.parent_name || '-' }}</div>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">排序</div>
              <div class="font-medium text-slate-900">{{ detailData.order }}</div>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">状态</div>
              <span :class="detailData.status === '0' ? 'bg-emerald-100 text-emerald-700 border border-emerald-200' : 'bg-red-100 text-red-700 border border-red-200'" class="px-2.5 py-1 rounded-lg text-xs font-medium">
                {{ detailData.status === '0' ? '启用' : '停用' }}
              </span>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">创建时间</div>
              <div class="font-medium text-slate-900">{{ formatDate(detailData.created_time) }}</div>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">更新时间</div>
              <div class="font-medium text-slate-900">{{ formatDate(detailData.updated_time) }}</div>
            </div>
            <div class="col-span-2 p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">描述</div>
              <div class="font-medium text-slate-900">{{ detailData.description || '-' }}</div>
            </div>
          </div>
        </div>

        <!-- Form -->
        <div v-else class="flex-1 overflow-y-auto p-6 space-y-5">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">部门名称 <span class="text-red-500">*</span></label>
            <input
              v-model="form.name"
              type="text"
              class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
              placeholder="请输入部门名称"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">部门编码 <span class="text-red-500">*</span></label>
            <input
              v-model="form.code"
              type="text"
              class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
              placeholder="请输入部门编码"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">上级部门</label>
            <select v-model="form.parent_id" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all">
              <option :value="undefined">请选择上级部门</option>
              <option v-for="dept in flatDeptOptions" :key="dept.id" :value="dept.id">
                {{ dept.tree_name || dept.name }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">排序</label>
            <input
              v-model.number="form.order"
              type="number"
              min="1"
              max="999"
              class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
              placeholder="请输入排序号"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">状态</label>
            <select v-model="form.status" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all">
              <option value="0">启用</option>
              <option value="1">停用</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">描述</label>
            <textarea
              v-model="form.description"
              rows="3"
              class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all resize-none"
              placeholder="请输入描述信息"
            ></textarea>
          </div>
        </div>

        <div class="px-6 py-4 border-t border-slate-100 flex justify-end gap-3 bg-slate-50/30">
          <button
            @click="closeDialog"
            class="px-5 py-2.5 border border-slate-200 rounded-xl text-slate-700 hover:bg-white hover:border-slate-300 transition-all"
          >
            取消
          </button>
          <button
            v-if="dialogType !== 'detail'"
            @click="submitForm"
            :disabled="submitting"
            class="px-5 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-all disabled:opacity-50 flex items-center gap-2 shadow-sm"
          >
            <Loader2Icon v-if="submitting" class="w-4 h-4 animate-spin" />
            {{ submitting ? '保存中...' : '保存' }}
          </button>
          <button
            v-else
            @click="closeDialog"
            class="px-5 py-2.5 bg-slate-900 text-white rounded-xl hover:bg-slate-800 transition-all shadow-sm"
          >
            确定
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, computed, watch, nextTick, defineComponent, h } from 'vue';
import { useRouter } from 'vue-router';
import { 
  Plus as PlusIcon, 
  Trash2 as TrashIcon, 
  Edit as EditIcon, 
  Eye as EyeIcon,
  Building as BuildingIcon,
  ChevronRight,
  ChevronDown,
  ChevronUp as ChevronUpIcon,
  ChevronDown as ChevronDownIcon,
  RefreshCw as RefreshCwIcon,
  Settings as SettingsIcon,
  Search as SearchIcon,
  X as XIcon,
  Loader2 as Loader2Icon,
  Inbox as InboxIcon,
  Play as PlayIcon,
  Pause as PauseIcon
} from 'lucide-vue-next';
import { api } from '@/services/api';
import message from '@/components/common/message';
import { dialog } from '@/components/common/dialog';
import type { DeptTable, DeptForm } from '@/services/fastApi/module_system/dept';

const router = useRouter();

// State
const loading = ref(false);
const submitting = ref(false);
const deptList = ref<DeptTable[]>([]);
const flatDeptOptions = ref<any[]>([]);
const dialogVisible = ref(false);
const dialogType = ref<'create' | 'edit' | 'detail'>('create');
const selectedIds = ref<number[]>([]);
const detailData = ref<any>({});

const queryParams = reactive({
  name: '',
  status: '',
  start_time: '',
  end_time: ''
});

const isExpand = ref(false);
const showColumnSettings = ref(false);
const columnSettingsRef = ref<HTMLElement | null>(null);
const dropdownPosition = ref({ top: 0, right: 0 });

// 计算下拉菜单位置
const updateDropdownPosition = () => {
  if (columnSettingsRef.value) {
    const rect = columnSettingsRef.value.getBoundingClientRect();
    dropdownPosition.value = {
      top: rect.bottom + 8,
      right: window.innerWidth - rect.right
    };
  }
};

// 点击外部关闭列设置
const handleClickOutside = (e: MouseEvent) => {
  if (columnSettingsRef.value && !columnSettingsRef.value.contains(e.target as Node)) {
    showColumnSettings.value = false;
  }
};

// 监听窗口大小变化
const handleResize = () => {
  if (showColumnSettings.value) {
    updateDropdownPosition();
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  window.removeEventListener('resize', handleResize);
});

// 监听显示状态，更新位置
watch(showColumnSettings, (newVal) => {
  if (newVal) {
    nextTick(() => {
      updateDropdownPosition();
    });
  }
});

const columnOptions = ref([
  { key: 'index', label: '序号', visible: true },
  { key: 'name', label: '部门名称', visible: true },
  { key: 'code', label: '部门编码', visible: true },
  { key: 'status', label: '状态', visible: true },
  { key: 'order', label: '排序', visible: true },
  { key: 'description', label: '描述', visible: true },
  { key: 'created_time', label: '创建时间', visible: false },
  { key: 'updated_time', label: '更新时间', visible: false },
  { key: 'action', label: '操作', visible: true },
]);

const getColumnVisible = (key: string) => {
  const col = columnOptions.value.find(c => c.key === key);
  return col ? col.visible : true;
};

const visibleColumnCount = computed(() => {
  return columnOptions.value.filter(c => c.visible).length + 1;
});

const defaultForm: DeptForm = {
  name: '',
  code: '',
  order: 1,
  parent_id: undefined,
  status: '0',
  description: ''
};

const form = reactive<DeptForm>({ ...defaultForm });

// Computed
const isAllSelected = computed(() => {
  const allIds = getAllDeptIds(deptList.value);
  return allIds.length > 0 && selectedIds.value.length === allIds.length;
});

const dialogTitle = computed(() => {
  if (dialogType.value === 'detail') return '部门详情';
  if (dialogType.value === 'edit') return '编辑部门';
  return '新增部门';
});

const isEdit = computed(() => dialogType.value === 'edit');

// Helper to get all dept IDs
const getAllDeptIds = (depts: DeptTable[]): number[] => {
  let ids: number[] = [];
  depts.forEach(d => {
    if (d.id) ids.push(d.id);
    if (d.children) {
      ids = ids.concat(getAllDeptIds(d.children));
    }
  });
  return ids;
};

// Helper to flatten dept tree for select options
const flattenDeptTree = (depts: DeptTable[], prefix = ''): any[] => {
  let result: any[] = [];
  depts.forEach(d => {
    result.push({
      id: d.id,
      name: d.name,
      tree_name: prefix + d.name
    });
    if (d.children) {
      result = result.concat(flattenDeptTree(d.children, prefix + '　'));
    }
  });
  return result;
};

// Methods
const fetchDepts = async () => {
  loading.value = true;
  try {
    const params: any = {};
    if (queryParams.name) params.name = queryParams.name;
    if (queryParams.status) params.status = queryParams.status;

    const res = await api.dept.listDept(params);
    let filteredData: DeptTable[] = [];
    if (res?.data) {
      filteredData = res.data || [];
    }

    // 前端过滤 - 创建时间
    if (queryParams.start_time) {
      const startDate = new Date(queryParams.start_time).getTime();
      filteredData = filteredData.filter(dept => {
        if (!dept.created_time) return false;
        return new Date(dept.created_time).getTime() >= startDate;
      });
    }
    if (queryParams.end_time) {
      const endDate = new Date(queryParams.end_time).getTime();
      filteredData = filteredData.filter(dept => {
        if (!dept.created_time) return false;
        return new Date(dept.created_time).getTime() <= endDate;
      });
    }

    deptList.value = filteredData;
    flatDeptOptions.value = flattenDeptTree(deptList.value);
  } catch (error) {
    console.error('Failed to fetch depts:', error);
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  fetchDepts();
};

const handleReset = () => {
  queryParams.name = '';
  queryParams.status = '';
  queryParams.start_time = '';
  queryParams.end_time = '';
  handleSearch();
};

const handleRefresh = () => {
  fetchDepts();
  message.success('刷新成功');
};

const toggleAllSelection = (e: Event) => {
  const checked = (e.target as HTMLInputElement).checked;
  if (checked) {
    selectedIds.value = getAllDeptIds(deptList.value);
  } else {
    selectedIds.value = [];
  }
};

const handleToggleSelect = (deptId: number) => {
  const index = selectedIds.value.indexOf(deptId);
  if (index > -1) {
    selectedIds.value.splice(index, 1);
  } else {
    selectedIds.value.push(deptId);
  }
};

const handleAdd = (parentId?: number) => {
  dialogType.value = 'create';
  Object.assign(form, defaultForm);
  if (parentId) {
    form.parent_id = parentId;
  }
  dialogVisible.value = true;
};

const handleAddChild = (parentId: number) => {
  handleAdd(parentId);
};

const handleEdit = (dept: DeptTable) => {
  dialogType.value = 'edit';
  Object.assign(form, {
    ...defaultForm,
    ...dept
  });
  dialogVisible.value = true;
};

const handleView = async (dept: DeptTable) => {
  dialogType.value = 'detail';
  if (dept.id) {
    try {
      const res = await api.dept.detailDept(dept.id);
      detailData.value = res?.data || {};
    } catch (error) {
      console.error('Failed to fetch dept detail:', error);
    }
  }
  dialogVisible.value = true;
};

const closeDialog = () => {
  dialogVisible.value = false;
  Object.assign(form, defaultForm);
};

const submitForm = async () => {
  if (!form.name || !form.code) {
    message.warning('请填写必填项');
    return;
  }
  
  submitting.value = true;
  try {
    if (isEdit.value) { 
      if (form.id) {
        await api.dept.updateDept(form.id, form);
      }
    } else {
      await api.dept.createDept(form);
    }
    closeDialog();
    fetchDepts();
    message.success('操作成功');
  } catch (error: any) {
    console.error('Operation failed:', error);
    const msg = error.data?.msg || error.message || '操作失败，请重试';
    message.error(msg);
  } finally {
    submitting.value = false;
  }
};

const handleDelete = async (dept: DeptTable) => {
  try {
    await dialog.confirm(`确定要删除部门 ${dept.name} 吗？`)
    if (dept.id) {
      await api.dept.deleteDept([dept.id]);
      fetchDepts();
      message.success('删除成功');
    }
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error('Delete failed:', error);
    message.error('删除失败');
  }
};

const handleBatchDelete = async () => {
  if (selectedIds.value.length === 0) return;

  try {
    await dialog.confirm(`确定要删除选中的 ${selectedIds.value.length} 个部门吗？`)
    await api.dept.deleteDept(selectedIds.value);
    selectedIds.value = [];
    fetchDepts();
    message.success('批量删除成功');
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error('Batch delete failed:', error);
    message.error('批量删除失败');
  }
};

const handleBatchStatus = async (status: string) => {
  if (selectedIds.value.length === 0) return;

  try {
    const statusText = status === '0' ? '启用' : '停用';
    await dialog.confirm(`确定要${statusText}选中的 ${selectedIds.value.length} 个部门吗？`)
    await api.dept.batchDept({ ids: selectedIds.value, status });
    selectedIds.value = [];
    fetchDepts();
    message.success(`批量${statusText}成功`);
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error('Batch status change failed:', error);
    message.error('操作失败');
  }
};

const formatDate = (dateStr?: string) => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleString();
};

// Tree row component
const DeptTreeRow = defineComponent({
  name: 'DeptTreeRow',
  props: {
    dept: { type: Object as () => DeptTable, required: true },
    depth: { type: Number, default: 0 },
    selectedIds: { type: Array as () => number[], required: true },
    columnOptions: { type: Array as () => { key: string; visible: boolean }[], required: true }
  },
  emits: ['toggle-select', 'add-child', 'view', 'edit', 'delete'],
  setup(props: any, { emit }: any) {
    const expanded = ref(false);
    const hasChildren = computed(() => props.dept.children && props.dept.children.length > 0);
    const isSelected = computed(() => props.selectedIds.includes(props.dept.id));

    const getColumnVisible = (key: string) => {
      const col = props.columnOptions.find((c: any) => c.key === key);
      return col ? col.visible : true;
    };

    const renderRow = (): any => {
      const cells: any[] = [];
      
      cells.push(
        h('td', { class: 'px-5 py-4 text-center' }, [
          h('input', { 
            type: 'checkbox', 
            class: 'rounded border-slate-300 text-blue-600 focus:ring-blue-500',
            checked: isSelected.value,
            onChange: () => emit('toggle-select', props.dept.id)
          })
        ])
      );

      if (getColumnVisible('index')) {
        cells.push(h('td', { class: 'px-5 py-4 text-center text-slate-500' }, '-'));
      }

      if (getColumnVisible('name')) {
        cells.push(
          h('td', { class: 'px-5 py-4 text-center', style: { paddingLeft: `${props.depth * 24 + 16}px` } }, [
            h('div', { class: 'flex items-center gap-1' }, [
              hasChildren.value 
                ? h('button', {
                    class: 'p-0.5 hover:bg-slate-100 rounded transition-colors',
                    onClick: () => expanded.value = !expanded.value
                  }, expanded.value 
                    ? h(ChevronDown, { class: 'w-4 h-4 text-slate-500' })
                    : h(ChevronRight, { class: 'w-4 h-4 text-slate-500' })
                )
                : h('span', { class: 'w-5' }),
              h('span', { class: 'font-medium text-slate-900' }, props.dept.name)
            ])
          ])
        );
      }

      if (getColumnVisible('code')) {
        cells.push(h('td', { class: 'px-5 py-4 text-center text-slate-600' }, props.dept.code || '-'));
      }

      if (getColumnVisible('status')) {
        cells.push(
          h('td', { class: 'px-5 py-4 text-center' }, 
            h('span', {
              class: `inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border ${props.dept.status === '0' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-red-50 text-red-700 border-red-200'}`
            }, [
              h('span', { class: `w-1.5 h-1.5 rounded-full mr-1.5 ${props.dept.status === '0' ? 'bg-emerald-500' : 'bg-red-500'}` }),
              props.dept.status === '0' ? '启用' : '停用'
            ])
          )
        );
      }

      if (getColumnVisible('order')) {
        cells.push(h('td', { class: 'px-5 py-4 text-center text-slate-600' }, props.dept.order));
      }

      if (getColumnVisible('description')) {
        cells.push(h('td', { class: 'px-5 py-4 text-center text-slate-600 max-w-[150px] truncate' }, props.dept.description || '-'));
      }

      if (getColumnVisible('created_time')) {
        cells.push(h('td', { class: 'px-5 py-4 text-center text-slate-500 whitespace-nowrap text-xs' }, formatDate(props.dept.created_time)));
      }

      if (getColumnVisible('updated_time')) {
        cells.push(h('td', { class: 'px-5 py-4 text-center text-slate-500 whitespace-nowrap text-xs' }, formatDate(props.dept.updated_time)));
      }

      if (getColumnVisible('action')) {
        cells.push(
          h('td', { class: 'px-5 py-4 text-center fixed-col' }, [
            h('div', { class: 'flex items-center justify-center gap-1' }, [
              h('button', {
                class: 'p-2 text-emerald-600 hover:bg-emerald-50 rounded-xl transition-all',
                title: '新增子部门',
                onClick: () => emit('add-child', props.dept.id)
              }, h(PlusIcon, { class: 'w-4 h-4' })),
              h('button', {
                class: 'p-2 text-slate-500 hover:bg-slate-100 rounded-xl transition-all',
                title: '详情',
                onClick: () => emit('view', props.dept)
              }, h(EyeIcon, { class: 'w-4 h-4' })),
              h('button', {
                class: 'p-2 text-blue-600 hover:bg-blue-50 rounded-xl transition-all',
                title: '编辑',
                onClick: () => emit('edit', props.dept)
              }, h(EditIcon, { class: 'w-4 h-4' })),
              h('button', {
                class: 'p-2 text-red-600 hover:bg-red-50 rounded-xl transition-all',
                title: '删除',
                onClick: () => emit('delete', props.dept)
              }, h(TrashIcon, { class: 'w-4 h-4' }))
            ])
          ])
        );
      }

      return h('tr', { class: 'hover:bg-slate-50/80 transition-colors' }, cells);
    };

    const renderChildren = (): any[] => {
      if (!hasChildren.value || !expanded.value || !props.dept.children) {
        return [];
      }
      return props.dept.children.map((child: DeptTable) => 
        h(DeptTreeRow, {
          key: child.id,
          dept: child,
          depth: props.depth + 1,
          selectedIds: props.selectedIds,
          columnOptions: props.columnOptions,
          onToggleSelect: (id: number) => emit('toggle-select', id),
          onAddChild: (id: number) => emit('add-child', id),
          onView: (d: DeptTable) => emit('view', d),
          onEdit: (d: DeptTable) => emit('edit', d),
          onDelete: (d: DeptTable) => emit('delete', d)
        })
      );
    };

    return () => {
      return [
        renderRow(),
        ...renderChildren()
      ];
    };
  }
});

onMounted(() => {
  fetchDepts();
});
</script>

<style scoped>
.fixed-col {
  position: sticky;
  right: 0;
  background-color: white;
  z-index: 1;
}
table thead .fixed-col {
  background-color: #f8fafc;
  z-index: 2;
}
</style>
