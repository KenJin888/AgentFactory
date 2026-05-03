<template>
  <div class="min-h-screen bg-slate-50 p-8 overflow-y-auto">
    <div class="max-w-6xl mx-auto">
      <!-- 顶部导航栏 -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <button @click="router.back()" class="flex items-center gap-2 text-slate-500 hover:text-slate-900 mb-2">
              <ArrowLeftIcon :size="20" /> 返回
          </button>
          <h1 class="text-3xl font-bold text-slate-900 flex items-center gap-3">
             <BookIcon class="text-blue-600" /> 字典管理
          </h1>
        </div>
        <div class="flex gap-3">
          <button
            @click="handleAdd"
            class="px-6 py-3 bg-blue-600 text-white rounded-xl font-bold hover:bg-blue-700 shadow-lg flex items-center gap-2 transition-transform active:scale-95"
          >
              <PlusIcon :size="20" /> 新增字典
          </button>
        </div>
      </div>

      <!-- Search & Filter Card -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 mb-6 overflow-hidden">
        <div class="p-6">
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
        </div>
      </div>

      <!-- Dict Table Card -->
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
              @click="handleExport"
              class="p-2.5 text-slate-600 hover:bg-slate-100 rounded-xl transition-all"
              title="导出"
            >
              <DownloadIcon class="w-5 h-5" />
            </button>
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
                  <div class="font-semibold text-slate-900">{{ dict.dict_name }}</div>
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
                      @click="handleDictData(dict)"
                      class="p-2 text-slate-800 hover:text-amber-600 hover:bg-amber-50 rounded-xl transition-all"
                      title="字典数据"
                    >
                      <FileTextIcon class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleView(dict)"
                      class="p-2 text-slate-800 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all"
                      title="详情"
                    >
                      <EyeIcon class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleEdit(dict)"
                      class="p-2 text-slate-800 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all"
                      title="编辑"
                    >
                      <EditIcon class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleDelete(dict)"
                      class="p-2 text-slate-800 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all"
                      title="删除"
                    >
                      <TrashIcon class="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Pagination -->
        <div class="px-6 py-4 border-t border-slate-100 flex items-center justify-between bg-slate-50/30">
          <div class="flex items-center gap-4">
            <span class="text-sm text-slate-500">共 <span class="font-semibold text-slate-900">{{ total }}</span> 条记录</span>
            <select 
              v-model="pageSize" 
              @change="handlePageSizeChange"
              class="px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-50 focus:border-blue-400"
            >
              <option :value="10">10 条/页</option>
              <option :value="20">20 条/页</option>
              <option :value="50">50 条/页</option>
              <option :value="100">100 条/页</option>
            </select>
          </div>
          <div class="flex items-center gap-2">
            <button
              @click="changePage(currentPage - 1)"
              :disabled="currentPage === 1"
              class="px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-sm disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-50 hover:border-slate-300 transition-all"
            >
              上一页
            </button>
            <span class="text-sm text-slate-700 px-3">第 {{ currentPage }} 页</span>
            <button
              @click="changePage(currentPage + 1)"
              :disabled="dictList.length < pageSize"
              class="px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-sm disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-50 hover:border-slate-300 transition-all"
            >
              下一页
            </button>
          </div>
        </div>
      </div>
    </div>

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
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, computed, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import ExportDialog from '@/components/common/ExportDialog.vue';
import DictDataDrawer from './DictDataDrawer.vue';
import type { ExportOptions } from '@/components/common/ExportDialog.vue';
import {
  ArrowLeft as ArrowLeftIcon,
  Plus as PlusIcon,
  Trash2 as TrashIcon,
  Edit as EditIcon,
  BookOpen as BookIcon,
  Eye as EyeIcon,
  X as XIcon,
  ChevronUp as ChevronUpIcon,
  ChevronDown as ChevronDownIcon,
  Download as DownloadIcon,
  RefreshCw as RefreshCwIcon,
  Search as SearchIcon,
  Loader2 as Loader2Icon,
  Inbox as InboxIcon,
  Play as PlayIcon,
  Pause as PauseIcon,
  FileText as FileTextIcon,
  Tag as TagIcon,
  Settings as SettingsIcon
} from 'lucide-vue-next';
import DictAPI from '@/services/fastApi/module_system/dict';
import type { DictTable, DictForm } from '@/services/fastApi/module_system/dict';
import message from '@/components/common/message';
import { dialog } from '@/components/common/dialog';

const router = useRouter();

// State
const loading = ref(false);
const submitting = ref(false);
const dictList = ref<DictTable[]>([]);
const total = ref(0);
const currentPage = ref(1);
const pageSize = ref(10);
const dialogVisible = ref(false);
const dialogType = ref<'create' | 'edit' | 'detail'>('create');
const selectedIds = ref<number[]>([]);
const detailData = ref<DictTable>({});
const isExpand = ref(false);
const dataDrawerVisible = ref(false);
const currentDictType = ref('');
const currentDictLabel = ref('');
const currentDictTypeId = ref(0);
const showExportDialog = ref(false);

const queryParams = reactive({
  dict_name: '',
  dict_type: '',
  status: '',
  start_time: '',
  end_time: ''
});

const defaultForm: DictForm = {
  dict_name: '',
  dict_type: '',
  status: '0',
  description: ''
};

const form = reactive<DictForm>({ ...defaultForm });

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

// 列设置
const showColumnSettings = ref(false);
const columnSettingsRef = ref<HTMLElement | null>(null);
const dropdownPosition = ref({ top: 0, right: 0 });

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

const visibleColumnCount = computed(() => {
  return columnOptions.value.filter(c => c.visible).length + 1;
});

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

// 监听显示状态，更新位置
watch(showColumnSettings, (newVal) => {
  if (newVal) {
    nextTick(() => {
      updateDropdownPosition();
    });
  }
});

onMounted(() => {
  fetchDictList();
  document.addEventListener('click', handleClickOutside);
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  window.removeEventListener('resize', handleResize);
});

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
const fetchDictList = async () => {
  loading.value = true;
  try {
    const params: any = {
      page_no: currentPage.value,
      page_size: pageSize.value,
    };
    if (queryParams.dict_name) params.dict_name = queryParams.dict_name;
    if (queryParams.dict_type) params.dict_type = queryParams.dict_type;
    if (queryParams.status) params.status = queryParams.status;

    const res = await DictAPI.listDictType(params);
    if (res?.data?.data) {
      dictList.value = res.data.data.items || [];
      total.value = res.data.data.total || 0;
    }
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  currentPage.value = 1;
  fetchDictList();
};

const handleReset = () => {
  queryParams.dict_name = '';
  queryParams.dict_type = '';
  queryParams.status = '';
  queryParams.start_time = '';
  queryParams.end_time = '';
  handleSearch();
};

const handleRefresh = () => {
  fetchDictList();
  message.success('刷新成功');
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

const changePage = (page: number) => {
  currentPage.value = page;
  fetchDictList();
};

const handlePageSizeChange = () => {
  currentPage.value = 1;
  fetchDictList();
};

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
    fetchDictList();
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
      fetchDictList();
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
    await DictAPI.deleteDictType(selectedIds.value);
    selectedIds.value = [];
    fetchDictList();
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
    await DictAPI.batchDictType({ ids: selectedIds.value, status });
    selectedIds.value = [];
    fetchDictList();
    message.success(`批量${statusText}成功`);
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error(error);
  }
};

const formatDate = (dateStr?: string) => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleString();
};
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
