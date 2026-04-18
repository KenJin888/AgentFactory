<template>
  <div class="min-h-screen bg-slate-50 p-8 overflow-y-auto">
    <div class="max-w-7xl mx-auto">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">日志管理</h1>
          <p class="mt-1 text-sm text-slate-500">维护系统的操作日志和登录日志。</p>
        </div>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 mb-6 overflow-hidden">
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">请求路径</label>
              <div class="relative">
                <input
                  v-model="queryParams.request_path"
                  type="text"
                  placeholder="请输入请求路径"
                  class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                  @keyup.enter="handleSearch"
                />
                <LinkIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">日志类型</label>
              <select
                v-model="queryParams.type"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all appearance-none cursor-pointer"
              >
                <option value="">全部</option>
                <option value="1">登录日志</option>
                <option value="2">操作日志</option>
              </select>
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

          <div v-if="isExpand" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mt-5 pt-5 border-t border-slate-100">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">创建人</label>
              <div class="flex items-center gap-2">
                <div class="relative flex-1">
                  <input
                    v-model="createdByName"
                    type="text"
                    placeholder="点击选择创建人"
                    readonly
                    @click="showUserSelector = true; handleOpenUserSelector()"
                    class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 cursor-pointer transition-all"
                  />
                  <UserIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                </div>
                <button
                  v-if="queryParams.created_id"
                  @click="queryParams.created_id = undefined; createdByName = ''"
                  class="p-2.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all"
                >
                  <XIcon class="w-4 h-4" />
                </button>
              </div>
            </div>
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
          <table class="w-full text-sm" style="min-width: 1600px;">
            <thead class="bg-slate-50 text-slate-600 font-medium border-b border-slate-200">
              <tr>
                <th class="px-5 py-4 w-12 text-center">
                  <input type="checkbox" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" @change="toggleAllSelection" :checked="isAllSelected" />
                </th>
                <th v-if="getColumnVisible('index')" class="px-5 py-4 text-center">序号</th>
                <th v-if="getColumnVisible('type')" class="px-5 py-4 text-center">日志类型</th>
                <th v-if="getColumnVisible('request_path')" class="px-5 py-4 text-center">请求路径</th>
                <th v-if="getColumnVisible('request_method')" class="px-5 py-4 text-center">请求方法</th>
                <th v-if="getColumnVisible('response_code')" class="px-5 py-4 text-center">状态码</th>
                <th v-if="getColumnVisible('request_ip')" class="px-5 py-4 text-center">请求IP</th>
                <th v-if="getColumnVisible('process_time')" class="px-5 py-4 text-center">处理时间</th>
                <th v-if="getColumnVisible('request_browser')" class="px-5 py-4 text-center">浏览器</th>
                <th v-if="getColumnVisible('request_os')" class="px-5 py-4 text-center">操作系统</th>
                <th v-if="getColumnVisible('description')" class="px-5 py-4 text-center">描述</th>
                <th v-if="getColumnVisible('created_time')" class="px-5 py-4 text-center">创建时间</th>
                <th v-if="getColumnVisible('created_by')" class="px-5 py-4 text-center">创建人</th>
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
              <tr v-else-if="logs.length === 0">
                <td :colspan="visibleColumnCount" class="px-6 py-12 text-center text-slate-400">
                  <div class="flex flex-col items-center gap-3">
                    <InboxIcon class="w-12 h-12 text-slate-300" />
                    <span>暂无数据</span>
                  </div>
                </td>
              </tr>
              <tr v-else v-for="log in logs" :key="log.id" class="hover:bg-slate-50/80 transition-colors group">
                <td class="px-5 py-4 text-center">
                  <input type="checkbox" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" :value="log.id" v-model="selectedIds" />
                </td>
                <td v-if="getColumnVisible('index')" class="px-5 py-4 text-center text-slate-500">
                  {{ (currentPage - 1) * pageSize + logs.indexOf(log) + 1 }}
                </td>
                <td v-if="getColumnVisible('type')" class="px-5 py-4 text-center">
                  <span
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                    :class="log.type === 1 ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-blue-50 text-blue-700 border border-blue-200'"
                  >
                    {{ log.type === 1 ? '登录日志' : '操作日志' }}
                  </span>
                </td>
                <td v-if="getColumnVisible('request_path')" class="px-5 py-4 text-center">
                  <div class="max-w-[200px] truncate" :title="log.request_path">{{ log.request_path || '-' }}</div>
                </td>
                <td v-if="getColumnVisible('request_method')" class="px-5 py-4 text-center">
                  <span
                    class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium"
                    :class="getMethodClass(log.request_method)"
                  >
                    {{ log.request_method || '-' }}
                  </span>
                </td>
                <td v-if="getColumnVisible('response_code')" class="px-5 py-4 text-center">
                  <span
                    class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium"
                    :class="getStatusCodeClass(log.response_code)"
                  >
                    {{ log.response_code || '-' }}
                  </span>
                </td>
                <td v-if="getColumnVisible('request_ip')" class="px-5 py-4 text-center text-slate-600">
                  <div class="flex items-center justify-center gap-1">
                    <span>{{ log.request_ip || '-' }}</span>
                    <button
                      v-if="log.request_ip"
                      @click="copyToClipboard(log.request_ip)"
                      class="p-1 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded transition-all"
                      title="复制"
                    >
                      <CopyIcon class="w-3 h-3" />
                    </button>
                  </div>
                </td>
                <td v-if="getColumnVisible('process_time')" class="px-5 py-4 text-center text-slate-600">{{ log.process_time || '-' }}</td>
                <td v-if="getColumnVisible('request_browser')" class="px-5 py-4 text-center">
                  <div class="max-w-[150px] truncate" :title="log.request_browser">{{ log.request_browser || '-' }}</div>
                </td>
                <td v-if="getColumnVisible('request_os')" class="px-5 py-4 text-center text-slate-600">{{ log.request_os || '-' }}</td>
                <td v-if="getColumnVisible('description')" class="px-5 py-4 text-center">
                  <div class="max-w-[120px] truncate" :title="log.description">{{ log.description || '-' }}</div>
                </td>
                <td v-if="getColumnVisible('created_time')" class="px-5 py-4 text-center text-slate-500 whitespace-nowrap text-xs">
                  {{ formatDate(log.created_time) }}
                </td>
                <td v-if="getColumnVisible('created_by')" class="px-5 py-4 text-center text-slate-600">{{ log.created_by?.name || '-' }}</td>
                <td v-if="getColumnVisible('action')" class="px-5 py-4 text-center fixed-col">
                  <div class="flex items-center justify-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      @click="handleView(log)"
                      class="p-2 text-slate-800 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all"
                      title="详情"
                    >
                      <EyeIcon class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleDelete(log)"
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
              :disabled="logs.length < pageSize"
              class="px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-sm disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-50 hover:border-slate-300 transition-all"
            >
              下一页
            </button>
          </div>
        </div>
      </div>
    </div>

    <UserSelector
      v-model:visible="showUserSelector"
      title="选择创建人"
      :multiple="false"
      :initial-selected="selectedUserForSelector"
      @confirm="handleUserSelect"
    />

    <ExportDialog
      v-model:visible="showExportDialog"
      title="导出日志"
      :fields="exportFields"
      :selected-count="selectedIds.length"
      @confirm="handleExportConfirm"
    />
    
    <div v-if="dialogVisible" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">
        <div class="px-6 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
          <h2 class="text-xl font-bold text-slate-900">日志详情</h2>
          <button @click="closeDialog" class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all">
            <XIcon class="w-5 h-5" />
          </button>
        </div>
        
        <div class="flex-1 overflow-y-auto p-6">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">日志类型</div>
              <span
                class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                :class="detailData.type === 1 ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-blue-50 text-blue-700 border border-blue-200'"
              >
                {{ detailData.type === 1 ? '登录日志' : '操作日志' }}
              </span>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">请求方法</div>
              <span
                class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium"
                :class="getMethodClass(detailData.request_method)"
              >
                {{ detailData.request_method || '-' }}
              </span>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">状态码</div>
              <span
                class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium"
                :class="getStatusCodeClass(detailData.response_code)"
              >
                {{ detailData.response_code || '-' }}
              </span>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">处理时间</div>
              <div class="font-medium text-slate-900">{{ detailData.process_time || '-' }}</div>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">请求路径</div>
              <div class="font-medium text-slate-900 break-all">{{ detailData.request_path || '-' }}</div>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">请求IP</div>
              <div class="font-medium text-slate-900">{{ detailData.request_ip || '-' }}</div>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">浏览器</div>
              <div class="font-medium text-slate-900">{{ detailData.request_browser || '-' }}</div>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">操作系统</div>
              <div class="font-medium text-slate-900">{{ detailData.request_os || '-' }}</div>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl md:col-span-2">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">登录地点</div>
              <div class="font-medium text-slate-900">{{ detailData.login_location || '-' }}</div>
            </div>
          </div>

          <div class="space-y-4">
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-2 uppercase tracking-wide">请求参数</div>
              <pre class="bg-slate-900 text-slate-100 p-4 rounded-lg text-xs overflow-x-auto max-h-[120px] overflow-y-auto">{{ formatJson(detailData.request_payload) }}</pre>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-2 uppercase tracking-wide">响应数据</div>
              <pre class="bg-slate-900 text-slate-100 p-4 rounded-lg text-xs overflow-x-auto max-h-[200px] overflow-y-auto">{{ formatJson(detailData.response_json) }}</pre>
            </div>
          </div>

          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 pt-6 border-t border-slate-100">
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">描述</div>
              <div class="font-medium text-slate-900">{{ detailData.description || '-' }}</div>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">创建人</div>
              <div class="font-medium text-slate-900">{{ detailData.created_by?.name || '-' }}</div>
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

        <div class="px-6 py-4 border-t border-slate-100 flex justify-end gap-3 bg-slate-50/30">
          <button
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
import { ref, reactive, onMounted, onUnmounted, computed, watch, nextTick } from 'vue';
import ExportDialog from '@/components/common/ExportDialog.vue';
import UserSelector from '@/components/common/UserSelector.vue';
import type { ExportOptions } from '@/components/common/ExportDialog.vue';
import type { User } from '@/types/user';
import { api } from '@/services/api';
import type { LogTable, LogPageQuery } from '@/services/fastApi/module_system/log';
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
  EyeIcon,
  LinkIcon,
  UserIcon,
  CopyIcon
} from 'lucide-vue-next';

const loading = ref(false);
const logs = ref<LogTable[]>([]);
const total = ref(0);
const currentPage = ref(1);
const pageSize = ref(10);
const dialogVisible = ref(false);
const selectedIds = ref<number[]>([]);
const detailData = ref<LogTable>({});

const queryParams = reactive<LogPageQuery>({
  page_no: 1,
  page_size: 10,
  type: undefined,
  request_path: '',
  created_id: undefined,
  created_time: undefined,
  start_time: '',
  end_time: ''
});

const isExpand = ref(false);
const createdByName = ref('');
const showUserSelector = ref(false);
const showExportDialog = ref(false);
const selectedUserForSelector = ref<User[]>([]);

interface ExportField {
  key: string;
  label: string;
  checked: boolean;
}

const exportFields = ref<ExportField[]>([
  { key: 'type', label: '日志类型', checked: true },
  { key: 'request_path', label: '请求路径', checked: true },
  { key: 'request_method', label: '请求方法', checked: true },
  { key: 'response_code', label: '状态码', checked: true },
  { key: 'request_ip', label: '请求IP', checked: true },
  { key: 'login_location', label: '登录地点', checked: true },
  { key: 'process_time', label: '处理时间', checked: true },
  { key: 'request_browser', label: '浏览器', checked: true },
  { key: 'request_os', label: '操作系统', checked: true },
  { key: 'description', label: '描述', checked: true },
  { key: 'created_time', label: '创建时间', checked: true },
  { key: 'updated_time', label: '更新时间', checked: false },
  { key: 'created_by', label: '创建人', checked: false },
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
  { key: 'type', label: '日志类型', visible: true },
  { key: 'request_path', label: '请求路径', visible: true },
  { key: 'request_method', label: '请求方法', visible: true },
  { key: 'response_code', label: '状态码', visible: true },
  { key: 'request_ip', label: '请求IP', visible: true },
  { key: 'process_time', label: '处理时间', visible: true },
  { key: 'request_browser', label: '浏览器', visible: false },
  { key: 'request_os', label: '操作系统', visible: false },
  { key: 'description', label: '描述', visible: false },
  { key: 'created_time', label: '创建时间', visible: true },
  { key: 'created_by', label: '创建人', visible: false },
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
  return logs.value.length > 0 && logs.value.every(l => selectedIds.value.includes(l.id!));
});

const toggleAllSelection = (e: Event) => {
  const checked = (e.target as HTMLInputElement).checked;
  if (checked) {
    selectedIds.value = logs.value.map(l => l.id!).filter(id => id !== undefined);
  } else {
    selectedIds.value = [];
  }
};

const handleOpenUserSelector = () => {
  if (queryParams.created_id) {
    selectedUserForSelector.value = [{
      id: queryParams.created_id,
      name: createdByName.value
    } as User];
  } else {
    selectedUserForSelector.value = [];
  }
};

const handleUserSelect = (users: User[]) => {
  if (users.length > 0) {
    const user = users[0];
    queryParams.created_id = user.id;
    createdByName.value = user.name;
  } else {
    queryParams.created_id = undefined;
    createdByName.value = '';
  }
  showUserSelector.value = false;
};

const getMethodClass = (method?: string) => {
  if (!method) return 'bg-slate-100 text-slate-600 border border-slate-200';
  switch (method.toUpperCase()) {
    case 'GET':
      return 'bg-blue-50 text-blue-700 border border-blue-200';
    case 'POST':
      return 'bg-emerald-50 text-emerald-700 border border-emerald-200';
    case 'PUT':
    case 'PATCH':
      return 'bg-amber-50 text-amber-700 border border-amber-200';
    case 'DELETE':
      return 'bg-red-50 text-red-700 border border-red-200';
    default:
      return 'bg-slate-100 text-slate-600 border border-slate-200';
  }
};

const getStatusCodeClass = (code?: number) => {
  if (code === undefined || code === null) return 'bg-slate-100 text-slate-600 border border-slate-200';
  if (code >= 200 && code < 300) {
    return 'bg-emerald-50 text-emerald-700 border border-emerald-200';
  } else if (code >= 300 && code < 400) {
    return 'bg-amber-50 text-amber-700 border border-amber-200';
  } else if (code >= 400) {
    return 'bg-red-50 text-red-700 border border-red-200';
  }
  return 'bg-slate-100 text-slate-600 border border-slate-200';
};

const copyToClipboard = (text: string) => {
  navigator.clipboard.writeText(text).then(() => {
    message.success('已复制到剪贴板');
  }).catch(() => {
    message.error('复制失败');
  });
};

const formatJson = (json?: string) => {
  if (!json) return '无数据';
  try {
    const parsed = JSON.parse(json);
    return JSON.stringify(parsed, null, 2);
  } catch {
    return json;
  }
};

const formatDate = (dateStr?: string) => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleString();
};

const fetchLogs = async () => {
  loading.value = true;
  try {
    const params: LogPageQuery = {
      page_no: currentPage.value,
      page_size: pageSize.value,
    };
    
    if (queryParams.type) params.type = Number(queryParams.type);
    if (queryParams.request_path) params.request_path = queryParams.request_path;
    if (queryParams.created_id) params.created_id = queryParams.created_id;
    
    if (queryParams.start_time || queryParams.end_time) {
      params.created_time = [];
      if (queryParams.start_time) {
        params.created_time.push(queryParams.start_time);
      }
      if (queryParams.end_time) {
        params.created_time.push(queryParams.end_time);
      }
    }

    const res = await api.log.listLog(params);
    if (res?.data) {
      logs.value = res.data.items || [];
      total.value = res.data.total || 0;
    }
  } catch (error) {
    console.error('Failed to fetch logs:', error);
    message.error('获取日志列表失败');
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  currentPage.value = 1;
  fetchLogs();
};

const handleReset = () => {
  queryParams.type = undefined;
  queryParams.request_path = '';
  queryParams.created_id = undefined;
  queryParams.start_time = '';
  queryParams.end_time = '';
  createdByName.value = '';
  currentPage.value = 1;
  fetchLogs();
};

const handleRefresh = () => {
  fetchLogs();
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
    
    let allData: LogTable[] = [];
    
    if (options.range === 'selected' && selectedIds.value.length > 0) {
      allData = logs.value.filter(l => selectedIds.value.includes(l.id!));
    } else if (options.range === 'current') {
      allData = [...logs.value];
    } else {
      const exportParams: LogPageQuery = {
        page_no: 1,
        page_size: 10000,
      };
      if (queryParams.type) exportParams.type = Number(queryParams.type);
      if (queryParams.request_path) exportParams.request_path = queryParams.request_path;
      if (queryParams.created_id) exportParams.created_id = queryParams.created_id;
      
      const res = await api.log.listLog(exportParams);
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
        ...allData.map((row: LogTable) => 
          keys.map((key: string) => {
            let value = (row as any)[key];
            if (key === 'type') {
              value = value === 1 ? '登录日志' : '操作日志';
            } else if (key === 'created_by' || key === 'updated_by') {
              value = value?.name || '';
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
      link.download = `日志列表_${new Date().toISOString().slice(0, 10)}.csv`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } else {
      try {
        const XLSX = await import('xlsx');
        const exportData = allData.map((row: LogTable) => {
          const obj: any = {};
          keys.forEach((key: string, index: number) => {
            let value = (row as any)[key];
            if (key === 'type') {
              value = value === 1 ? '登录日志' : '操作日志';
            } else if (key === 'created_by' || key === 'updated_by') {
              value = value?.name || '';
            }
            obj[headers[index]] = value;
          });
          return obj;
        });
        
        const ws = XLSX.utils.json_to_sheet(exportData);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, '日志列表');
        XLSX.writeFile(wb, `日志列表_${new Date().toISOString().slice(0, 10)}.xlsx`);
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
  fetchLogs();
};

const handlePageSizeChange = () => {
  currentPage.value = 1;
  fetchLogs();
};

const handleView = async (log: LogTable) => {
  if (log.id) {
    try {
      const res = await api.log.detailLog(log.id);
      detailData.value = res?.data || {};
    } catch (error) {
      console.error('Failed to fetch log detail:', error);
      message.error('获取日志详情失败');
    }
  }
  dialogVisible.value = true;
};

const closeDialog = () => {
  dialogVisible.value = false;
  detailData.value = {};
};

const handleDelete = async (log: LogTable) => {
  try {
    await dialog.confirm(`确定要删除该日志吗？`)
    if (log.id) {
      await api.log.deleteLog([log.id]);
      fetchLogs();
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
    await dialog.confirm(`确定要删除选中的 ${selectedIds.value.length} 条日志吗？`)
    await api.log.deleteLog(selectedIds.value);
    selectedIds.value = [];
    fetchLogs();
    message.success('批量删除成功');
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error('Batch delete failed:', error);
    message.error('批量删除失败');
  }
};

onMounted(() => {
  fetchLogs();
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
