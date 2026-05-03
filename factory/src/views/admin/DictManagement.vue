<template>
  <CrudPageShell
    title="字典管理"
    subtitle="维护系统字典类型与字典项。"
    :loading="loading"
    :total="total"
    v-model:current-page="currentPage"
    v-model:page-size="pageSize"
    :selected-count="selectedIds.length"
    :show-export="true"
    :export-perm="PERMS.export"
    :show-refresh="true"
    :refreshing="loading"
    :show-column-settings="true"
    :column-options="columnOptions"
    :show-batch-actions="true"
    :show-batch-delete="true"
    :batch-delete-perm="PERMS.delete"
    :show-batch-enable="true"
    :batch-enable-perm="PERMS.patch"
    :show-batch-disable="true"
    :batch-disable-perm="PERMS.patch"
    add-button-text="新增字典"
    :create-perm="PERMS.create"
    @add="handleAdd"
    @export="handleExport"
    @refresh="handleRefresh"
    @column-change="handleColumnChange"
    @batch-delete="handleBatchDelete"
    @batch-enable="handleBatchStatus('0')"
    @batch-disable="handleBatchStatus('1')"
  >
    <!-- 搜索区 -->
    <template #search>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <!-- 字典名称 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">字典名称</label>
          <div class="relative">
            <input
              v-model="queryParams.dict_name"
              type="text"
              placeholder="请输入字典名称"
              class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
              @keyup.enter="handleSearch"
            />
            <BookIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          </div>
        </div>
        <!-- 字典类型 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">字典类型</label>
          <div class="relative">
            <input
              v-model="queryParams.dict_type"
              type="text"
              placeholder="请输入字典类型"
              class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
              @keyup.enter="handleSearch"
            />
            <TagIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
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
        <!-- 创建时间 -->
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
    </template>

    <!-- 表格区 -->
    <template #table>
      <table class="w-full text-sm" style="min-width: 1200px;">
        <thead class="bg-slate-50 text-slate-600 font-medium border-b border-slate-200">
          <tr>
            <th class="px-5 py-4 w-12 text-center">
              <input type="checkbox" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" @change="toggleAllSelection" :checked="isAllSelected" />
            </th>
            <th v-if="getColumnVisible('index')" class="px-5 py-4 text-center">序号</th>
            <th v-if="getColumnVisible('dict_name')" class="px-5 py-4 text-center">字典名称</th>
            <th v-if="getColumnVisible('dict_type')" class="px-5 py-4 text-center">字典类型</th>
            <th v-if="getColumnVisible('status')" class="px-5 py-4 text-center">状态</th>
            <th v-if="getColumnVisible('description')" class="px-5 py-4 text-center">描述</th>
            <th v-if="getColumnVisible('created_time')" class="px-5 py-4 text-center">创建时间</th>
            <th v-if="getColumnVisible('updated_time')" class="px-5 py-4 text-center">更新时间</th>
            <th v-if="getColumnVisible('action')" class="px-5 py-4 text-center fixed-col">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-if="loading" class="animate-pulse">
            <td :colspan="visibleColumnCount" class="px-6 py-12 text-center text-slate-400">
              <div class="flex flex-col items-center gap-3">
                <Loader2Icon class="w-8 h-8 animate-spin text-blue-500" />
                <span>加载中...</span>
              </div>
            </td>
          </tr>
          <tr v-else-if="dictList.length === 0">
            <td :colspan="visibleColumnCount" class="px-6 py-12 text-center text-slate-400">
              <div class="flex flex-col items-center gap-3">
                <InboxIcon class="w-12 h-12 text-slate-300" />
                <span>暂无数据</span>
              </div>
            </td>
          </tr>
          <tr v-else v-for="dict in dictList" :key="dict.id" class="hover:bg-slate-50/80 transition-colors group">
            <td class="px-5 py-4 text-center">
              <input type="checkbox" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" :value="dict.id" v-model="selectedIds" />
            </td>
            <td v-if="getColumnVisible('index')" class="px-5 py-4 text-center text-slate-500">
              {{ (currentPage - 1) * pageSize + dictList.indexOf(dict) + 1 }}
            </td>
            <td v-if="getColumnVisible('dict_name')" class="px-5 py-4 text-center">
              <div class="text-slate-900">{{ dict.dict_name }}</div>
            </td>
            <td v-if="getColumnVisible('dict_type')" class="px-5 py-4 text-center">
              <span class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium bg-blue-50 text-blue-700 border border-blue-100">
                {{ dict.dict_type }}
              </span>
            </td>
            <td v-if="getColumnVisible('status')" class="px-5 py-4 text-center">
              <span
                class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                :class="dict.status === '0' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-red-50 text-red-700 border border-red-200'"
              >
                <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="dict.status === '0' ? 'bg-emerald-500' : 'bg-red-500'"></span>
                {{ dict.status === '0' ? '启用' : '停用' }}
              </span>
            </td>
            <td v-if="getColumnVisible('description')" class="px-5 py-4 text-center text-slate-600">{{ dict.description || '-' }}</td>
            <td v-if="getColumnVisible('created_time')" class="px-5 py-4 text-center text-slate-500 whitespace-nowrap text-xs">
              {{ formatDate(dict.created_time) }}
            </td>
            <td v-if="getColumnVisible('updated_time')" class="px-5 py-4 text-center text-slate-500 whitespace-nowrap text-xs">
              {{ formatDate(dict.updated_time) }}
            </td>
            <td v-if="getColumnVisible('action')" class="px-5 py-4 text-center fixed-col">
              <div class="flex items-center justify-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  :disabled="!canData"
                  @click="handleDictData(dict)"
                  class="p-2 text-slate-800 hover:text-amber-600 hover:bg-amber-50 rounded-xl transition-all disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-transparent disabled:hover:text-slate-800"
                  :title="canData ? '字典数据' : '无权限'"
                >
                  <FileTextIcon class="w-4 h-4" />
                </button>
                <button
                  :disabled="!canDetail"
                  @click="handleView(dict)"
                  class="p-2 text-slate-800 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-transparent disabled:hover:text-slate-800"
                  :title="canDetail ? '详情' : '无权限'"
                >
                  <EyeIcon class="w-4 h-4" />
                </button>
                <button
                  :disabled="!canUpdate"
                  @click="handleEdit(dict)"
                  class="p-2 text-slate-800 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-transparent disabled:hover:text-slate-800"
                  :title="canUpdate ? '编辑' : '无权限'"
                >
                  <EditIcon class="w-4 h-4" />
                </button>
                <button
                  :disabled="!canDelete"
                  @click="handleDelete(dict)"
                  class="p-2 text-slate-800 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-transparent disabled:hover:text-slate-800"
                  :title="canDelete ? '删除' : '无权限'"
                >
                  <TrashIcon class="w-4 h-4" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </template>
  </CrudPageShell>

  <!-- Add/Edit/Detail Modal -->
  <div v-if="dialogVisible" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col">
      <div class="px-6 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
        <h2 class="text-xl font-bold text-slate-900">{{ dialogTitle }}</h2>
        <button @click="closeDialog" class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all">
          <XIcon class="w-5 h-5" />
        </button>
      </div>

      <div class="flex-1 overflow-y-auto p-6">
        <!-- Detail View -->
        <div v-if="dialogType === 'detail'" class="space-y-6">
          <div class="grid grid-cols-2 gap-5">
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">字典名称</div>
              <div class="font-medium text-slate-900">{{ detailData.dict_name }}</div>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">字典类型</div>
              <div class="font-medium text-slate-900">
                <span class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium bg-blue-50 text-blue-700 border border-blue-100">
                  {{ detailData.dict_type }}
                </span>
              </div>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">状态</div>
              <span :class="detailData.status === '0' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'" class="px-2.5 py-1 rounded-lg text-xs font-medium">
                {{ detailData.status === '0' ? '启用' : '停用' }}
              </span>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">描述</div>
              <div class="font-medium text-slate-900">{{ detailData.description || '-' }}</div>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">创建时间</div>
              <div class="font-medium text-slate-900">{{ formatDate(detailData.created_time) }}</div>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">更新时间</div>
              <div class="font-medium text-slate-900">{{ formatDate(detailData.updated_time) }}</div>
            </div>
          </div>
        </div>

        <!-- Form -->
        <div v-else class="space-y-5">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">字典名称 <span class="text-red-500">*</span></label>
              <input
                v-model="form.dict_name"
                type="text"
                placeholder="请输入字典名称"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">字典类型 <span class="text-red-500">*</span></label>
              <input
                v-model="form.dict_type"
                type="text"
                placeholder="请输入字典类型"
                :disabled="isEdit"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 disabled:bg-slate-100 disabled:text-slate-500 transition-all"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">状态</label>
              <select v-model="form.status" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all">
                <option value="0">启用</option>
                <option value="1">停用</option>
              </select>
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-slate-700 mb-2">描述</label>
              <textarea
                v-model="form.description"
                rows="3"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all resize-none"
                placeholder="请输入描述"
              ></textarea>
            </div>
          </div>
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

  <!-- Dict Data Drawer -->
  <DictDataDrawer
    v-if="dataDrawerVisible"
    v-model="dataDrawerVisible"
    :dict-type="currentDictType"
    :dict-label="currentDictLabel"
    :dict-type-id="currentDictTypeId"
    @close="dataDrawerVisible = false"
  />

  <!-- Export Dialog -->
  <ExportDialog
    v-model:visible="showExportDialog"
    title="导出字典"
    :fields="exportFields"
    :selected-count="selectedIds.length"
    @confirm="handleExportConfirm"
  />
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import { useRouter } from 'vue-router';
import ExportDialog from '@/components/common/ExportDialog.vue';
import DictDataDrawer from './DictDataDrawer.vue';
import type { ExportOptions } from '@/components/common/ExportDialog.vue';
import { CrudPageShell } from '@/components/crud';
import { useCrudPage } from '@/composables/useCrudPage';
import { useCrudAuth } from '@/composables/useCrudAuth';
import {
  Plus as PlusIcon,
  Trash2 as TrashIcon,
  Edit as EditIcon,
  BookOpen as BookIcon,
  Eye as EyeIcon,
  X as XIcon,
  ChevronUp as ChevronUpIcon,
  ChevronDown as ChevronDownIcon,
  Search as SearchIcon,
  Loader2 as Loader2Icon,
  Inbox as InboxIcon,
  FileText as FileTextIcon,
  Tag as TagIcon,
} from 'lucide-vue-next';
import DictAPI from '@/services/fastApi/module_system/dict';
import type { DictTable, DictForm } from '@/services/fastApi/module_system/dict';
import message from '@/components/common/message';
import { dialog } from '@/components/common/dialog';

const router = useRouter();

// 权限配置
const PERMS = {
  query: 'module_system:dict:query',
  create: 'module_system:dict:create',
  update: 'module_system:dict:update',
  delete: 'module_system:dict:delete',
  export: 'module_system:dict:export',
  patch: 'module_system:dict:patch',
  detail: 'module_system:dict:detail',
  data: 'module_system:dict:data',
} as const

// 使用 useCrudAuth 判断行内按钮权限
const dataAuth = useCrudAuth({ data: PERMS.data })
const detailAuth = useCrudAuth({ detail: PERMS.detail })
const updateAuth = useCrudAuth({ update: PERMS.update })
const deleteAuth = useCrudAuth({ delete: PERMS.delete })

const canData = computed(() => dataAuth.can('data'))
const canDetail = computed(() => detailAuth.can('detail'))
const canUpdate = computed(() => updateAuth.can('update'))
const canDelete = computed(() => deleteAuth.can('delete'))

// 使用 CRUD Page composable
const {
  loading,
  currentPage,
  pageSize,
  total,
  queryParams,
  dataList: dictList,
  selectedIds,
  fetchData,
  handleSearch,
  handleReset,
  handleRefresh,
} = useCrudPage<DictTable, { dict_name: string; dict_type: string; status: string; start_time: string; end_time: string }>({
  initialQuery: {
    dict_name: '',
    dict_type: '',
    status: '',
    start_time: '',
    end_time: '',
  },
  fetchList: async (params) => {
    const queryParamsExport: any = {
      page_no: params.page_no,
      page_size: params.page_size,
    }
    if (params.dict_name) queryParamsExport.dict_name = params.dict_name
    if (params.dict_type) queryParamsExport.dict_type = params.dict_type
    if (params.status) queryParamsExport.status = params.status

    const res = await DictAPI.listDictType(queryParamsExport)
    return {
      items: res?.data?.data?.items || [],
      total: res?.data?.data?.total || 0,
    }
  },
})

// 其他状态
const isExpand = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogType = ref<'create' | 'edit' | 'detail'>('create')
const detailData = ref<DictTable>({})
const dataDrawerVisible = ref(false)
const currentDictType = ref('')
const currentDictLabel = ref('')
const currentDictTypeId = ref(0)
const showExportDialog = ref(false)

interface ExportField {
  key: string;
  label: string;
  checked: boolean;
}

const exportFields = ref<ExportField[]>([
  { key: 'dict_name', label: '字典名称', checked: true },
  { key: 'dict_type', label: '字典类型', checked: true },
  { key: 'status', label: '状态', checked: true },
  { key: 'description', label: '描述', checked: true },
  { key: 'created_time', label: '创建时间', checked: true },
  { key: 'updated_time', label: '更新时间', checked: true },
]);

const columnOptions = ref([
  { key: 'index', label: '序号', visible: true },
  { key: 'dict_name', label: '字典名称', visible: true },
  { key: 'dict_type', label: '字典类型', visible: true },
  { key: 'status', label: '状态', visible: true },
  { key: 'description', label: '描述', visible: true },
  { key: 'created_time', label: '创建时间', visible: false },
  { key: 'updated_time', label: '更新时间', visible: false },
  { key: 'action', label: '操作', visible: true },
]);

const getColumnVisible = (key: string) => {
  const col = columnOptions.value.find(c => c.key === key);
  return col ? col.visible : true;
};

const handleColumnChange = (key: string, visible: boolean) => {
  const col = columnOptions.value.find((c) => c.key === key)
  if (col) {
    col.visible = visible
  }
}

const visibleColumnCount = computed(() => {
  return columnOptions.value.filter(c => c.visible).length + 1;
});

const defaultForm: DictForm = {
  dict_name: '',
  dict_type: '',
  status: '0',
  description: ''
};

const form = reactive<DictForm>({ ...defaultForm });

// Computed
const isAllSelected = computed(() => {
  return dictList.value.length > 0 && dictList.value.every(dict => selectedIds.value.includes(dict.id!));
});

const dialogTitle = computed(() => {
  if (dialogType.value === 'detail') return '字典详情';
  if (dialogType.value === 'edit') return '编辑字典';
  return '新增字典';
});

const isEdit = computed(() => dialogType.value === 'edit');

// Methods
const toggleAllSelection = (e: Event) => {
  const checked = (e.target as HTMLInputElement).checked;
  if (checked) {
    selectedIds.value = dictList.value.map(d => d.id!).filter(id => id !== undefined);
  } else {
    selectedIds.value = [];
  }
};

const handleAdd = () => {
  dialogType.value = 'create';
  Object.assign(form, defaultForm);
  dialogVisible.value = true;
};

const handleEdit = (dict: DictTable) => {
  dialogType.value = 'edit';
  Object.assign(form, {
    ...defaultForm,
    ...dict
  });
  dialogVisible.value = true;
};

const handleView = (dict: DictTable) => {
  dialogType.value = 'detail';
  detailData.value = { ...dict };
  dialogVisible.value = true;
};

const handleDictData = (dict: DictTable) => {
  currentDictType.value = dict.dict_type || '';
  currentDictLabel.value = dict.dict_name || '';
  currentDictTypeId.value = dict.id || 0;
  dataDrawerVisible.value = true;
};

const closeDialog = () => {
  dialogVisible.value = false;
  Object.assign(form, defaultForm);
};

const submitForm = async () => {
  if (!form.dict_name || !form.dict_type) {
    message.warning('请填写必填项');
    return;
  }

  submitting.value = true;

  try {
    if (isEdit.value) {
      if (form.id) {
        await DictAPI.updateDictType(form.id, form);
      }
    } else {
      await DictAPI.createDictType(form);
    }
    closeDialog();
    fetchData();
    message.success('操作成功');
  } catch (error) {
    console.error(error);
  } finally {
    submitting.value = false;
  }
};

const handleDelete = async (dict: DictTable) => {
  try {
    await dialog.confirm(`确定要删除字典 "${dict.dict_name}" 吗？`)
    if (dict.id) {
      await DictAPI.deleteDictType([dict.id]);
      fetchData();
      message.success('删除成功');
    }
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error(error);
  }
};

const handleBatchDelete = async () => {
  if (selectedIds.value.length === 0) return;

  try {
    await dialog.confirm(`确定要删除选中的 ${selectedIds.value.length} 个字典吗？`)
    await DictAPI.deleteDictType(selectedIds.value as number[]);
    selectedIds.value = [];
    fetchData();
    message.success('批量删除成功');
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error(error);
  }
};

const handleBatchStatus = async (status: string) => {
  if (selectedIds.value.length === 0) return;

  try {
    const statusText = status === '0' ? '启用' : '停用';
    await dialog.confirm(`确定要${statusText}选中的 ${selectedIds.value.length} 个字典吗？`)
    await DictAPI.batchDictType({ ids: selectedIds.value as number[], status });
    selectedIds.value = [];
    fetchData();
    message.success(`批量${statusText}成功`);
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error(error);
  }
};

const handleExport = () => {
  showExportDialog.value = true;
};

const handleExportConfirm = async (options: ExportOptions) => {
  try {
    const selectedFieldKeys = options.fields;
    if (selectedFieldKeys.length === 0) {
      message.warning('请至少选择一个导出字段');
      return;
    }

    const selectedFields = exportFields.value.filter((f: ExportField) => selectedFieldKeys.includes(f.key));

    message.info('正在导出，请稍候...');

    let allData: any[] = [];

    if (options.range === 'selected' && selectedIds.value.length > 0) {
      allData = dictList.value.filter(d => selectedIds.value.includes(d.id!));
    } else if (options.range === 'current') {
      allData = [...dictList.value];
    } else {
      const params: any = {
        page_no: 1,
        page_size: 10000,
      };
      if (queryParams.dict_name) params.dict_name = queryParams.dict_name;
      if (queryParams.dict_type) params.dict_type = queryParams.dict_type;
      if (queryParams.status) params.status = queryParams.status;

      const res = await DictAPI.listDictType(params);
      if (res?.data?.data?.items) {
        allData = res.data.data.items;
      }
    }

    const headers = selectedFields.map((f: ExportField) => f.label);
    const keys = selectedFieldKeys;

    // 根据选择的字段过滤数据
    const filteredData = allData.map((row: any) => {
      const obj: any = {};
      keys.forEach((key: string, index: number) => {
        obj[headers[index]] = row[key];
      });
      return obj;
    });

    if (options.format === 'csv') {
      const csvContent = [
        headers.join(','),
        ...filteredData.map((row: any) =>
          headers.map((header: string) => {
            let value = row[header];
            if (value === null || value === undefined) value = '';
            value = String(value);
            if (value.includes(',') || value.includes('"') || value.includes('\n')) {
              value = `"${value.replace(/"/g, '""')}"`;
            }
            return value;
          }).join(',')
        )
      ].join('\n');

      const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `字典列表_${new Date().toISOString().slice(0, 10)}.csv`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } else {
      try {
        const XLSX = await import('xlsx');
        const ws = XLSX.utils.json_to_sheet(filteredData);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, '字典列表');
        XLSX.writeFile(wb, `字典列表_${new Date().toISOString().slice(0, 10)}.xlsx`);
      } catch (error) {
        console.error(error);
        return;
      }
    }

    message.success('导出成功');
  } catch (error) {
    console.error(error);
  }
};

const formatDate = (dateStr?: string) => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleString();
};

// 初始化
fetchData()
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
