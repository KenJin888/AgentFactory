<template>
  <div class="min-h-screen bg-slate-50 p-8 overflow-y-auto">
    <div class="max-w-7xl mx-auto">
      <!-- 顶部导航栏 -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">参数管理</h1>
          <p class="mt-1 text-sm text-slate-500">维护系统的配置参数信息。</p>
        </div>
        <div class="flex gap-3">
          <button
            @click="handleCreate"
            class="px-6 py-3 bg-slate-900 text-white rounded-xl font-bold hover:bg-slate-800 shadow-lg flex items-center gap-2 transition-transform active:scale-95"
          >
            <PlusIcon :size="20" /> 新增参数
          </button>
        </div>
      </div>

      <!-- Search & Filter Card -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 mb-6 overflow-hidden">
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">配置名称</label>
              <div class="relative">
                <input
                  v-model="queryParams.config_name"
                  type="text"
                  placeholder="请输入配置名称"
                  class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                  @keyup.enter="handleSearch"
                />
                <SettingsIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">配置键名</label>
              <div class="relative">
                <input
                  v-model="queryParams.config_key"
                  type="text"
                  placeholder="请输入配置键名"
                  class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                  @keyup.enter="handleSearch"
                />
                <KeyIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              </div>
            </div>
            <div class="flex items-end justify-end">
              <div class="flex items-center gap-2">
                <button
                  @click="handleSearch"
                  class="bg-slate-900 text-white px-6 py-2.5 rounded-xl hover:bg-slate-800 transition-all shadow-sm hover:shadow flex items-center justify-center gap-2 whitespace-nowrap"
                >
                  <SearchIcon class="w-4 h-4" />
                  查询
                </button>
                <button
                  @click="handleReset"
                  class="bg-white text-slate-600 border border-slate-200 px-6 py-2.5 rounded-xl hover:bg-slate-50 hover:border-slate-300 transition-all whitespace-nowrap"
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

          <div v-if="isExpand" class="grid grid-cols-1 md:grid-cols-3 gap-5 mt-5 pt-5 border-t border-slate-100">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">系统内置</label>
              <select
                v-model="queryParams.config_type"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all appearance-none cursor-pointer"
              >
                <option value="">全部</option>
                <option value="true">是</option>
                <option value="false">否</option>
              </select>
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-slate-700 mb-2">创建时间</label>
              <div class="flex items-center gap-3">
                <input
                  v-model="startTime"
                  type="date"
                  class="flex-1 px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
                <span class="text-slate-400">至</span>
                <input
                  v-model="endTime"
                  type="date"
                  class="flex-1 px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Param Table Card -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
          <div class="flex items-center gap-3">
            <div class="flex items-center gap-3 text-sm">
              <span class="text-slate-500">已选择</span>
              <span class="font-semibold text-slate-900 bg-blue-50 px-2.5 py-0.5 rounded-full">{{ selectedIds.length }}</span>
              <span class="text-slate-500">项</span>
            </div>
            <div v-if="selectedIds.length > 0" class="flex items-center gap-1 ml-4 pl-4 border-l border-slate-200">
              <button
                @click="handleBatchDelete"
                class="p-2 text-slate-700 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all"
                title="批量删除"
              >
                <TrashIcon class="w-4 h-4" />
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
                <SlidersHorizontalIcon class="w-5 h-5" />
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
                <th v-if="getColumnVisible('config_name')" class="px-5 py-4 text-center">配置名称</th>
                <th v-if="getColumnVisible('config_key')" class="px-5 py-4 text-center">配置键</th>
                <th v-if="getColumnVisible('config_value')" class="px-5 py-4 text-center">配置值</th>
                <th v-if="getColumnVisible('config_type')" class="px-5 py-4 text-center">系统内置</th>
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
              <tr v-else-if="params.length === 0">
                <td :colspan="visibleColumnCount" class="px-6 py-12 text-center text-slate-400">
                  <div class="flex flex-col items-center gap-3">
                    <InboxIcon class="w-12 h-12 text-slate-300" />
                    <span>暂无数据</span>
                  </div>
                </td>
              </tr>
              <tr v-else v-for="param in params" :key="param.id" class="hover:bg-slate-50/80 transition-colors group">
                <td class="px-5 py-4 text-center">
                  <input type="checkbox" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" :value="param.id" v-model="selectedIds" />
                </td>
                <td v-if="getColumnVisible('index')" class="px-5 py-4 text-center text-slate-500">
                  {{ (currentPage - 1) * pageSize + params.indexOf(param) + 1 }}
                </td>
                <td v-if="getColumnVisible('config_name')" class="px-5 py-4 text-center">
                  <div class="max-w-[150px] truncate font-medium text-slate-900" :title="param.config_name">{{ param.config_name || '-' }}</div>
                </td>
                <td v-if="getColumnVisible('config_key')" class="px-5 py-4 text-center">
                  <div class="max-w-[200px] truncate text-slate-600" :title="param.config_key">{{ param.config_key || '-' }}</div>
                </td>
                <td v-if="getColumnVisible('config_value')" class="px-5 py-4 text-center">
                  <div class="max-w-[200px] truncate text-slate-600" :title="param.config_value">{{ param.config_value || '-' }}</div>
                </td>
                <td v-if="getColumnVisible('config_type')" class="px-5 py-4 text-center">
                  <span
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                    :class="param.config_type ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-600 border border-slate-200'"
                  >
                    {{ param.config_type ? '是' : '否' }}
                  </span>
                </td>
                <td v-if="getColumnVisible('description')" class="px-5 py-4 text-center">
                  <div class="max-w-[200px] truncate text-slate-600" :title="param.description">{{ param.description || '-' }}</div>
                </td>
                <td v-if="getColumnVisible('created_time')" class="px-5 py-4 text-center text-slate-500 whitespace-nowrap text-xs">
                  {{ formatDate(param.created_time) }}
                </td>
                <td v-if="getColumnVisible('updated_time')" class="px-5 py-4 text-center text-slate-500 whitespace-nowrap text-xs">
                  {{ formatDate(param.updated_time) }}
                </td>
                <td v-if="getColumnVisible('action')" class="px-5 py-4 text-center fixed-col">
                  <div class="flex items-center justify-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      @click="handleView(param)"
                      class="p-2 text-slate-800 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all"
                      title="详情"
                    >
                      <EyeIcon class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleEdit(param)"
                      class="p-2 text-slate-800 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all"
                      title="编辑"
                    >
                      <PencilIcon class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleDelete(param)"
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
              :disabled="params.length < pageSize"
              class="px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-sm disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-50 hover:border-slate-300 transition-all"
            >
              下一页
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Export Dialog -->
    <ExportDialog
      v-model:visible="showExportDialog"
      title="导出参数"
      :fields="exportFields"
      :selected-count="selectedIds.length"
      @confirm="handleExportConfirm"
    />
    
    <!-- View Modal (Readonly) -->
    <div v-if="viewDialogVisible" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col">
        <div class="px-6 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
          <h2 class="text-xl font-bold text-slate-900">参数详情</h2>
          <button @click="closeViewDialog" class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all">
            <XIcon class="w-5 h-5" />
          </button>
        </div>

        <div class="flex-1 overflow-y-auto p-6">
          <div class="space-y-5">
            <div class="grid grid-cols-2 gap-5">
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">配置名称</div>
                <div class="font-medium text-slate-900">{{ viewData.config_name || '-' }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">系统内置</div>
                <span
                  class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                  :class="viewData.config_type ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-600 border border-slate-200'"
                >
                  {{ viewData.config_type ? '是' : '否' }}
                </span>
              </div>
            </div>

            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">配置键</div>
              <div class="font-medium text-slate-900 break-all">{{ viewData.config_key || '-' }}</div>
            </div>

            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">配置值</div>
              <div class="font-medium text-slate-900 break-all">{{ viewData.config_value || '-' }}</div>
            </div>

            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">描述</div>
              <div class="font-medium text-slate-900">{{ viewData.description || '-' }}</div>
            </div>

            <div class="grid grid-cols-2 gap-5">
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">创建时间</div>
                <div class="font-medium text-slate-900">{{ formatDate(viewData.created_time) }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">更新时间</div>
                <div class="font-medium text-slate-900">{{ formatDate(viewData.updated_time) }}</div>
              </div>
            </div>
          </div>
        </div>

        <div class="px-6 py-4 border-t border-slate-100 flex justify-end gap-3 bg-slate-50/30">
          <button
            @click="closeViewDialog"
            class="px-5 py-2.5 bg-slate-900 text-white rounded-xl hover:bg-slate-800 transition-all shadow-sm"
          >
            确定
          </button>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="dialogVisible" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-xl max-h-[90vh] overflow-hidden flex flex-col">
        <div class="px-6 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
          <h2 class="text-xl font-bold text-slate-900">{{ isEdit ? '编辑参数' : '新增参数' }}</h2>
          <button @click="closeDialog" class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all">
            <XIcon class="w-5 h-5" />
          </button>
        </div>
        
        <div class="flex-1 overflow-y-auto p-6">
          <div class="space-y-5">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">配置名称 <span class="text-red-500">*</span></label>
              <input
                v-model="formData.config_name"
                type="text"
                placeholder="请输入配置名称"
                maxlength="50"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">配置键 <span class="text-red-500">*</span></label>
              <input
                v-model="formData.config_key"
                type="text"
                placeholder="请输入配置键"
                maxlength="50"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">配置值 <span class="text-red-500">*</span></label>
              <input
                v-model="formData.config_value"
                type="text"
                placeholder="请输入配置值"
                maxlength="100"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">系统内置 <span class="text-red-500">*</span></label>
              <div class="flex items-center gap-4">
                <label class="flex items-center gap-2 cursor-pointer">
                  <input
                    v-model="formData.config_type"
                    type="radio"
                    :value="true"
                    class="w-4 h-4 text-blue-600 border-slate-300 focus:ring-blue-500"
                  />
                  <span class="text-sm text-slate-700">是</span>
                </label>
                <label class="flex items-center gap-2 cursor-pointer">
                  <input
                    v-model="formData.config_type"
                    type="radio"
                    :value="false"
                    class="w-4 h-4 text-blue-600 border-slate-300 focus:ring-blue-500"
                  />
                  <span class="text-sm text-slate-700">否</span>
                </label>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">描述</label>
              <textarea
                v-model="formData.description"
                rows="4"
                maxlength="100"
                placeholder="请输入描述"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all resize-none"
              ></textarea>
              <div class="text-xs text-slate-400 mt-1 text-right">{{ formData.description?.length || 0 }}/100</div>
            </div>
          </div>
        </div>

        <div class="px-6 py-4 border-t border-slate-100 flex justify-end gap-3 bg-slate-50/30">
          <button
            @click="closeDialog"
            class="px-5 py-2.5 bg-white text-slate-600 border border-slate-200 rounded-xl hover:bg-slate-50 transition-all"
          >
            取消
          </button>
          <button
            @click="handleSubmit"
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
import { ref, reactive, onMounted, onUnmounted, computed, watch, nextTick } from 'vue';
import ExportDialog from '@/components/common/ExportDialog.vue';
import type { ExportOptions } from '@/components/common/ExportDialog.vue';
import { api } from '@/services/api';
import type { ConfigTable, ConfigPageQuery, ConfigForm } from '@/services/fastApi/module_system/params';
import message from '@/components/common/message';
import { dialog } from '@/components/common/dialog';
import { 
  TrashIcon, 
  XIcon,
  ChevronUpIcon,
  ChevronDownIcon,
  DownloadIcon,
  RefreshCwIcon,
  SettingsIcon,
  SearchIcon,
  Loader2Icon,
  InboxIcon,
  PencilIcon,
  PlusIcon,
  EyeIcon,
  KeyIcon,
  SlidersHorizontalIcon
} from 'lucide-vue-next';

const loading = ref(false);
const params = ref<ConfigTable[]>([]);
const total = ref(0);
const currentPage = ref(1);
const pageSize = ref(10);
const dialogVisible = ref(false);
const viewDialogVisible = ref(false);
const isEdit = ref(false);
const selectedIds = ref<number[]>([]);
const editId = ref<number | null>(null);
const viewData = ref<ConfigTable>({});

const queryParams = reactive({
  page_no: 1,
  page_size: 10,
  config_name: '',
  config_key: '',
  config_type: '' as '' | 'true' | 'false'
});

const startTime = ref('');
const endTime = ref('');

const formData = reactive<ConfigForm>({
  config_name: '',
  config_key: '',
  config_value: '',
  config_type: false,
  description: ''
});

const isExpand = ref(false);
const showExportDialog = ref(false);

interface ExportField {
  key: string;
  label: string;
  checked: boolean;
}

const exportFields = ref<ExportField[]>([
  { key: 'config_name', label: '配置名称', checked: true },
  { key: 'config_key', label: '配置键', checked: true },
  { key: 'config_value', label: '配置值', checked: true },
  { key: 'config_type', label: '系统内置', checked: true },
  { key: 'description', label: '描述', checked: true },
  { key: 'created_time', label: '创建时间', checked: true },
  { key: 'updated_time', label: '更新时间', checked: false },
]);

const showColumnSettings = ref(false);
const columnSettingsRef = ref<HTMLElement | null>(null);
const dropdownPosition = ref({ top: 0, right: 0 });

const updateDropdownPosition = () => {
  if (columnSettingsRef.value) {
    const rect = columnSettingsRef.value.getBoundingClientRect();
    dropdownPosition.value = {
      top: rect.bottom + 8,
      right: window.innerWidth - rect.right
    };
  }
};

const handleClickOutside = (e: MouseEvent) => {
  if (columnSettingsRef.value && !columnSettingsRef.value.contains(e.target as Node)) {
    showColumnSettings.value = false;
  }
};

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

watch(showColumnSettings, (newVal) => {
  if (newVal) {
    nextTick(() => {
      updateDropdownPosition();
    });
  }
});

const columnOptions = ref([
  { key: 'index', label: '序号', visible: true },
  { key: 'config_name', label: '配置名称', visible: true },
  { key: 'config_key', label: '配置键', visible: true },
  { key: 'config_value', label: '配置值', visible: true },
  { key: 'config_type', label: '系统内置', visible: true },
  { key: 'description', label: '描述', visible: true },
  { key: 'created_time', label: '创建时间', visible: true },
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

const isAllSelected = computed(() => {
  return params.value.length > 0 && params.value.every(p => selectedIds.value.includes(p.id!));
});

const toggleAllSelection = (e: Event) => {
  const checked = (e.target as HTMLInputElement).checked;
  if (checked) {
    selectedIds.value = params.value.map(p => p.id!).filter(id => id !== undefined);
  } else {
    selectedIds.value = [];
  }
};

const formatDate = (dateStr?: string) => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleString();
};

const fetchParams = async () => {
  loading.value = true;
  try {
    const query: ConfigPageQuery = {
      page_no: currentPage.value,
      page_size: pageSize.value,
    };

    if (queryParams.config_name) query.config_name = queryParams.config_name;
    if (queryParams.config_key) query.config_key = queryParams.config_key;
    if (queryParams.config_type !== '') {
      query.config_type = queryParams.config_type === 'true';
    }

    if (startTime.value || endTime.value) {
      query.created_time = [];
      if (startTime.value) {
        query.created_time.push(startTime.value + ' 00:00:00');
      }
      if (endTime.value) {
        query.created_time.push(endTime.value + ' 23:59:59');
      }
    }

    const res = await api.params.listParams(query);
    if (res?.data) {
      params.value = res.data.items || [];
      total.value = res.data.total || 0;
    }
  } catch (error) {
    console.error('Failed to fetch params:', error);
    message.error('获取参数列表失败');
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  currentPage.value = 1;
  fetchParams();
};

const handleReset = () => {
  queryParams.config_name = '';
  queryParams.config_key = '';
  queryParams.config_type = '';
  startTime.value = '';
  endTime.value = '';
  currentPage.value = 1;
  fetchParams();
};

const handleRefresh = () => {
  fetchParams();
  message.success('刷新成功');
};

const handleCreate = () => {
  isEdit.value = false;
  editId.value = null;
  formData.config_name = '';
  formData.config_key = '';
  formData.config_value = '';
  formData.config_type = false;
  formData.description = '';
  dialogVisible.value = true;
};

const handleEdit = (param: ConfigTable) => {
  isEdit.value = true;
  editId.value = param.id || null;
  formData.config_name = param.config_name || '';
  formData.config_key = param.config_key || '';
  formData.config_value = param.config_value || '';
  formData.config_type = param.config_type || false;
  formData.description = param.description || '';
  dialogVisible.value = true;
};

const handleView = (param: ConfigTable) => {
  viewData.value = { ...param };
  viewDialogVisible.value = true;
};

const closeViewDialog = () => {
  viewDialogVisible.value = false;
  viewData.value = {};
};

const closeDialog = () => {
  dialogVisible.value = false;
  isEdit.value = false;
  editId.value = null;
};

const handleSubmit = async () => {
  if (!formData.config_name?.trim()) {
    message.warning('请输入配置名称');
    return;
  }
  if (!formData.config_key?.trim()) {
    message.warning('请输入配置键');
    return;
  }
  if (!formData.config_value?.trim()) {
    message.warning('请输入配置值');
    return;
  }

  try {
    if (isEdit.value && editId.value) {
      await api.params.updateParams(editId.value, formData);
      message.success('更新成功');
    } else {
      await api.params.createParams(formData);
      message.success('创建成功');
    }
    closeDialog();
    fetchParams();
  } catch (error) {
    console.error('Submit failed:', error);
    message.error(isEdit.value ? '更新失败' : '创建失败');
  }
};

const handleDelete = async (param: ConfigTable) => {
  try {
    await dialog.confirm(`确定要删除该参数吗？`)
    if (param.id) {
      await api.params.deleteParams([param.id]);
      fetchParams();
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
    await dialog.confirm(`确定要删除选中的 ${selectedIds.value.length} 条参数吗？`)
    await api.params.deleteParams(selectedIds.value);
    selectedIds.value = [];
    fetchParams();
    message.success('批量删除成功');
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error('Batch delete failed:', error);
    message.error('批量删除失败');
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
    
    let allData: ConfigTable[] = [];
    
    if (options.range === 'selected' && selectedIds.value.length > 0) {
      allData = params.value.filter(p => selectedIds.value.includes(p.id!));
    } else if (options.range === 'current') {
      allData = [...params.value];
    } else {
      const exportParams: ConfigPageQuery = {
        page_no: 1,
        page_size: 10000,
      };
      if (queryParams.config_name) exportParams.config_name = queryParams.config_name;
      if (queryParams.config_key) exportParams.config_key = queryParams.config_key;
      
      const res = await api.params.listParams(exportParams);
      if (res?.data?.items) {
        allData = res.data.items;
      }
    }
    
    const headers = selectedFields.map((f: ExportField) => f.label);
    const keys = selectedFieldKeys;
    const timeFields = ['created_time', 'updated_time'];

    if (options.format === 'csv') {
      const csvContent = [
        headers.join(','),
        ...allData.map((row: ConfigTable) =>
          keys.map((key: string) => {
            let value = (row as any)[key];
            if (key === 'config_type') {
              value = value ? '是' : '否';
            } else {
              if (value === null || value === undefined) value = '';
              value = String(value);
            }
            if (timeFields.includes(key) && value) {
              value = ' ' + value;
            }
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
      link.download = `参数列表_${new Date().toISOString().slice(0, 10)}.csv`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } else {
      try {
        const XLSX = await import('xlsx');
        const exportData = allData.map((row: ConfigTable) => {
          const obj: any = {};
          keys.forEach((key: string, index: number) => {
            let value = (row as any)[key];
            if (key === 'config_type') {
              value = value ? '是' : '否';
            }
            obj[headers[index]] = value;
          });
          return obj;
        });
        
        const ws = XLSX.utils.json_to_sheet(exportData);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, '参数列表');
        XLSX.writeFile(wb, `参数列表_${new Date().toISOString().slice(0, 10)}.xlsx`);
      } catch (xlsxError) {
        message.error('Excel 导出失败，请确保已安装 xlsx 库');
        console.error('XLSX export failed:', xlsxError);
        return;
      }
    }
    
    message.success('导出成功');
  } catch (error) {
    console.error('Export failed:', error);
    message.error('导出失败');
  }
};

const changePage = (page: number) => {
  currentPage.value = page;
  fetchParams();
};

const handlePageSizeChange = () => {
  currentPage.value = 1;
  fetchParams();
};

onMounted(() => {
  fetchParams();
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
