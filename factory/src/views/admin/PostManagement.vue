<template>
  <div class="min-h-screen bg-slate-50 p-8 overflow-y-auto">
    <div class="max-w-6xl mx-auto">
      <!-- 顶部导航栏 -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">岗位管理</h1>
          <p class="mt-1 text-sm text-slate-500">维护岗位信息与可用状态。</p>
        </div>
        <div class="flex gap-3">
          <button
            @click="handleAdd"
            class="px-6 py-3 bg-slate-900 text-white rounded-xl font-bold hover:bg-slate-800 shadow-lg flex items-center gap-2 transition-transform active:scale-95"
          >
              <PlusIcon :size="20" /> 新增岗位
          </button>
        </div>
      </div>

      <!-- Search & Filter Card -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 mb-6 overflow-hidden">
        <div class="p-6">
          <!-- 第一行：四个等分列 -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
            <!-- 岗位名称 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">岗位名称</label>
              <div class="relative">
                <input
                  v-model="queryParams.name"
                  type="text"
                  placeholder="请输入岗位名称"
                  class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                  @keyup.enter="handleSearch"
                />
                <BriefcaseIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
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
            <!-- 创建人 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">创建人</label>
              <div class="flex items-center gap-2">
                <div class="relative flex-1">
                  <input
                    v-model="createdByName"
                    type="text"
                    placeholder="点击选择创建人"
                    readonly
                    @click="showUserSelector = true"
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
          </div>
        </div>
      </div>

      <!-- Position Table -->
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
                class="fixed bg-white border border-slate-100 rounded-xl shadow-xl z-50 p-4 min-w-[180px]"
                :style="{ top: dropdownPosition.top + 'px', right: dropdownPosition.right + 'px' }"
                @click.stop
              >
                <div class="text-sm font-semibold text-slate-800 mb-3">列展示</div>
                <div class="space-y-2 max-h-48 overflow-y-auto">
                  <label 
                    v-for="col in columnOptions.filter(c => c.key !== 'checkbox')" 
                    :key="col.key" 
                    class="flex items-center gap-2 cursor-pointer hover:bg-slate-50 p-1.5 rounded-lg transition-colors"
                  >
                    <input 
                      type="checkbox" 
                      v-model="col.visible" 
                      class="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500/20"
                    />
                    <span class="text-sm text-slate-600">{{ col.label }}</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="overflow-hidden rounded-b-2xl">
          <div class="overflow-x-auto">
          <table class="w-full text-sm text-left" style="min-width: 1000px;">
            <thead class="bg-slate-50 text-slate-700 font-medium border-b border-slate-200">
              <tr>
                <th v-if="getColumnVisible('checkbox')" class="px-6 py-4 w-12 text-center">
                  <input type="checkbox" class="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500/20" @change="toggleAllSelection" :checked="isAllSelected" />
                </th>
                <th v-if="getColumnVisible('index')" class="px-6 py-4 text-center text-slate-500 font-medium">序号</th>
                <th v-if="getColumnVisible('name')" class="px-6 py-4 text-left text-slate-500 font-medium">岗位名称</th>
                <th v-if="getColumnVisible('order')" class="px-6 py-4 text-center text-slate-500 font-medium">岗位排序</th>
                <th v-if="getColumnVisible('status')" class="px-6 py-4 text-center text-slate-500 font-medium">状态</th>
                <th v-if="getColumnVisible('description')" class="px-6 py-4 text-left text-slate-500 font-medium">描述</th>
                <th v-if="getColumnVisible('created_time')" class="px-6 py-4 text-center text-slate-500 font-medium">创建时间</th>
                <th v-if="getColumnVisible('updated_time')" class="px-6 py-4 text-center text-slate-500 font-medium">更新时间</th>
                <th v-if="getColumnVisible('created_by')" class="px-6 py-4 text-center text-slate-500 font-medium">创建人</th>
                <th v-if="getColumnVisible('updated_by')" class="px-6 py-4 text-center text-slate-500 font-medium">更新人</th>
                <th v-if="getColumnVisible('action')" class="px-6 py-4 text-center text-slate-500 font-medium fixed-col">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-if="loading" class="animate-pulse">
                <td :colspan="visibleColumnCount" class="px-6 py-12 text-center text-slate-400">
                  <div class="flex items-center justify-center gap-2">
                    <div class="w-5 h-5 border-2 border-slate-200 border-t-indigo-500 rounded-full animate-spin"></div>
                    加载中...
                  </div>
                </td>
              </tr>
              <tr v-else-if="positions.length === 0">
                <td :colspan="visibleColumnCount" class="px-6 py-12 text-center text-slate-400">
                  <div class="flex flex-col items-center gap-2">
                    <div class="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center">
                      <InboxIcon class="w-6 h-6 text-slate-400" />
                    </div>
                    暂无数据
                  </div>
                </td>
              </tr>
              <tr v-else v-for="(position, index) in positions" :key="position.id" class="hover:bg-slate-50/80 transition-colors group">
                <td v-if="getColumnVisible('checkbox')" class="px-6 py-4 text-center">
                  <input type="checkbox" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" :value="position.id" v-model="selectedIds" />
                </td>
                <td v-if="getColumnVisible('index')" class="px-6 py-4 text-center text-slate-500">
                  {{ (currentPage - 1) * pageSize + index + 1 }}
                </td>
                <td v-if="getColumnVisible('name')" class="px-6 py-4 text-center">
                  <div class="font-semibold text-slate-900">{{ position.name }}</div>
                </td>
                <td v-if="getColumnVisible('order')" class="px-6 py-4 text-center">
                  <div class="text-slate-600">{{ position.order }}</div>
                </td>
                <td v-if="getColumnVisible('status')" class="px-6 py-4 text-center">
                  <span
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border"
                    :class="position.status === '0' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-red-50 text-red-700 border-red-200'"
                  >
                    <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="position.status === '0' ? 'bg-emerald-500' : 'bg-red-500'"></span>
                    {{ position.status === '0' ? '启用' : '停用' }}
                  </span>
                </td>
                <td v-if="getColumnVisible('description')" class="px-6 py-4 text-center">
                  <div class="text-slate-600 max-w-[150px] truncate">{{ position.description || '-' }}</div>
                </td>
                <td v-if="getColumnVisible('created_time')" class="px-6 py-4 text-center text-slate-500 whitespace-nowrap text-xs">
                  {{ formatDate(position.created_time) }}
                </td>
                <td v-if="getColumnVisible('updated_time')" class="px-6 py-4 text-center text-slate-500 whitespace-nowrap text-xs">
                  {{ formatDate(position.updated_time) }}
                </td>
                <td v-if="getColumnVisible('created_by')" class="px-6 py-4 text-center text-slate-600">
                  {{ position.created_by?.name || '-' }}
                </td>
                <td v-if="getColumnVisible('updated_by')" class="px-6 py-4 text-center text-slate-600">
                  {{ position.updated_by?.name || '-' }}
                </td>
                <td v-if="getColumnVisible('action')" class="px-6 py-4 text-center fixed-col">
                  <div class="flex items-center justify-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      @click="handleView(position)"
                      class="p-2 text-slate-800 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all"
                      title="详情"
                    >
                      <EyeIcon class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleEdit(position)"
                      class="p-2 text-slate-800 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all"
                      title="编辑"
                    >
                      <EditIcon class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleDelete(position)"
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
        </div>
        
        <!-- User Selector Dialog -->
        <UserSelector
          v-model:visible="showUserSelector"
          title="选择创建人"
          :multiple="false"
          :initial-selected="selectedUserForSelector"
          @confirm="handleUserSelect"
        />
        
        <!-- Export Dialog -->
        <ExportDialog
          v-model:visible="showExportDialog"
          title="导出岗位"
          :fields="exportFields"
          :selected-count="selectedIds.length"
          @confirm="handleExportConfirm"

        />
        
        <!-- Pagination -->
        <div class="px-6 py-4 border-t border-slate-100 flex items-center justify-between bg-slate-50/30 rounded-b-2xl">
          <div class="flex items-center gap-4">
            <span class="text-sm text-slate-500">共 <span class="font-semibold text-slate-700">{{ total }}</span> 条记录</span>
            <select 
              v-model="pageSize" 
              @change="handlePageSizeChange"
              class="px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
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
              class="px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm text-slate-600 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50 hover:border-slate-300 transition-all"
            >
              上一页
            </button>
            <span class="text-sm text-slate-700 px-3">第 {{ currentPage }} 页</span>
            <button
              @click="changePage(currentPage + 1)"
              :disabled="positions.length < pageSize"
              class="px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm text-slate-600 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50 hover:border-slate-300 transition-all"
            >
              下一页
            </button>
          </div>
        </div>
      </div>

      <!-- Add/Edit Modal -->
      <div v-if="dialogVisible" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
          <div class="px-6 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
            <h2 class="text-lg font-bold text-slate-800">{{ dialogTitle }}</h2>
            <button @click="closeDialog" class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all">
              <XIcon class="w-5 h-5" />
            </button>
          </div>
          
          <!-- Detail View -->
          <div v-if="dialogType === 'detail'" class="p-6">
            <div class="grid grid-cols-2 gap-5">
              <div class="bg-slate-50 p-4 rounded-xl">
                <div class="text-xs text-slate-500 mb-1">岗位名称</div>
                <div class="font-semibold text-slate-800">{{ detailData.name }}</div>
              </div>
              <div class="bg-slate-50 p-4 rounded-xl">
                <div class="text-xs text-slate-500 mb-1">岗位排序</div>
                <div class="font-semibold text-slate-800">{{ detailData.order }}</div>
              </div>
              <div class="bg-slate-50 p-4 rounded-xl">
                <div class="text-xs text-slate-500 mb-1">状态</div>
                <span :class="detailData.status === '0' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-red-50 text-red-700 border border-red-200'" class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium">
                  <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="detailData.status === '0' ? 'bg-emerald-500' : 'bg-red-500'"></span>
                  {{ detailData.status === '0' ? '启用' : '停用' }}
                </span>
              </div>
              <div class="bg-slate-50 p-4 rounded-xl">
                <div class="text-xs text-slate-500 mb-1">创建人</div>
                <div class="font-semibold text-slate-800">{{ detailData.created_by?.name || '-' }}</div>
              </div>
              <div class="bg-slate-50 p-4 rounded-xl">
                <div class="text-xs text-slate-500 mb-1">更新人</div>
                <div class="font-semibold text-slate-800">{{ detailData.updated_by?.name || '-' }}</div>
              </div>
              <div class="bg-slate-50 p-4 rounded-xl">
                <div class="text-xs text-slate-500 mb-1">创建时间</div>
                <div class="font-semibold text-slate-800">{{ formatDate(detailData.created_time) }}</div>
              </div>
              <div class="bg-slate-50 p-4 rounded-xl">
                <div class="text-xs text-slate-500 mb-1">更新时间</div>
                <div class="font-semibold text-slate-800">{{ formatDate(detailData.updated_time) }}</div>
              </div>
              <div class="col-span-2 bg-slate-50 p-4 rounded-xl">
                <div class="text-xs text-slate-500 mb-1">描述</div>
                <div class="font-semibold text-slate-800">{{ detailData.description || '-' }}</div>
              </div>
            </div>
          </div>

          <!-- Form -->
          <div v-else class="p-6 space-y-5">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">岗位名称 <span class="text-red-500">*</span></label>
              <input
                v-model="form.name"
                type="text"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
                placeholder="请输入岗位名称"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">岗位排序</label>
              <input
                v-model.number="form.order"
                type="number"
                min="1"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
                placeholder="请输入排序号"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">状态</label>
              <select v-model="form.status" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all">
                <option value="0">启用</option>
                <option value="1">停用</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">描述</label>
              <textarea
                v-model="form.description"
                rows="3"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all resize-none"
                placeholder="请输入描述信息"
              ></textarea>
            </div>
          </div>

          <div class="px-6 py-5 border-t border-slate-100 flex justify-end gap-3">
            <button
              @click="closeDialog"
              class="px-5 py-2.5 border border-slate-200 rounded-xl text-slate-600 hover:bg-slate-50 hover:border-slate-300 transition-all"
            >
              取消
            </button>
            <button
              v-if="dialogType !== 'detail'"
              @click="submitForm"
              :disabled="submitting"
              class="px-5 py-2.5 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition-all shadow-sm shadow-indigo-200 disabled:opacity-50 flex items-center gap-2"
            >
              <span v-if="submitting" class="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></span>
              {{ submitting ? '保存中...' : '保存' }}
            </button>
            <button
              v-else
              @click="closeDialog"
              class="px-5 py-2.5 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition-all shadow-sm shadow-indigo-200"
            >
              确定
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, computed, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import ExportDialog from '@/components/common/ExportDialog.vue';
import UserSelector from '@/components/common/UserSelector.vue';
import type { ExportOptions } from '@/components/common/ExportDialog.vue';
import type { User } from '@/types/user';
import { 
  Plus as PlusIcon, 
  Trash2 as TrashIcon, 
  Edit as EditIcon, 
  Eye as EyeIcon,
  ChevronUp as ChevronUpIcon,
  ChevronDown as ChevronDownIcon,
  Download as DownloadIcon,
  RefreshCw as RefreshCwIcon,
  Settings as SettingsIcon,
  X as XIcon,
  Search as SearchIcon,
  Inbox as InboxIcon,
  Briefcase as BriefcaseIcon,
  User as UserIcon,
  Play as PlayIcon,
  Pause as PauseIcon
} from 'lucide-vue-next';
import { api } from '@/services/api';
import message from '@/components/common/message';
import { dialog } from '@/components/common/dialog';
import type { PositionTable, PositionForm } from '@/services/fastApi/module_system/position';

const router = useRouter();

// State
const loading = ref(false);
const submitting = ref(false);
const positions = ref<PositionTable[]>([]);
const total = ref(0);
const currentPage = ref(1);
const pageSize = ref(10);
const dialogVisible = ref(false);
const dialogType = ref<'create' | 'edit' | 'detail'>('create');
const selectedIds = ref<number[]>([]);
const detailData = ref<any>({});

const queryParams = reactive({
  name: '',
  status: '',
  start_time: '',
  end_time: '',
  created_id: undefined as number | undefined
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

const createdByName = ref('');
const showUserSelector = ref(false);
const showExportDialog = ref(false);

interface ExportField {
  key: string;
  label: string;
  checked: boolean;
}

const exportFields = ref<ExportField[]>([
  { key: 'name', label: '岗位名称', checked: true },
  { key: 'order', label: '岗位排序', checked: true },
  { key: 'status', label: '状态', checked: true },
  { key: 'description', label: '描述', checked: true },
  { key: 'created_time', label: '创建时间', checked: true },
  { key: 'updated_time', label: '更新时间', checked: true },
  { key: 'created_by', label: '创建人', checked: true },
  { key: 'updated_by', label: '更新人', checked: true },
]);

const columnOptions = ref([
  { key: 'index', label: '序号', visible: true },
  { key: 'name', label: '岗位名称', visible: true },
  { key: 'order', label: '岗位排序', visible: true },
  { key: 'status', label: '状态', visible: true },
  { key: 'description', label: '描述', visible: true },
  { key: 'created_time', label: '创建时间', visible: false },
  { key: 'updated_time', label: '更新时间', visible: false },
  { key: 'created_by', label: '创建人', visible: false },
  { key: 'updated_by', label: '更新人', visible: false },
  { key: 'action', label: '操作', visible: true },
]);

const getColumnVisible = (key: string) => {
  const col = columnOptions.value.find(c => c.key === key);
  return col ? col.visible : true;
};

const visibleColumnCount = computed(() => {
  return columnOptions.value.filter(c => c.visible).length;
});

const defaultForm: PositionForm = {
  name: '',
  order: 1,
  status: '0',
  description: ''
};

const form = reactive<PositionForm>({ ...defaultForm });

// Computed
const isAllSelected = computed(() => {
  return positions.value.length > 0 && selectedIds.value.length === positions.value.length && positions.value.every(p => selectedIds.value.includes(p.id!));
});

const dialogTitle = computed(() => {
  if (dialogType.value === 'detail') return '岗位详情';
  if (dialogType.value === 'edit') return '编辑岗位';
  return '新增岗位';
});

const isEdit = computed(() => dialogType.value === 'edit');

// 存储所有岗位数据用于前端过滤
const allPositionsData = ref<PositionTable[]>([]);

// Methods
const fetchPositions = async () => {
  loading.value = true;
  try {
    // 获取所有数据用于前端过滤
    const params: any = {
      page_no: 1,
      page_size: 10000,
    };
    if (queryParams.name) params.name = queryParams.name;
    if (queryParams.status) params.status = queryParams.status;

    const res = await api.position.listPosition(params);
    let filteredData: PositionTable[] = [];
    if (res?.data?.items) {
      filteredData = res.data.items;
    }

    // 前端过滤 - 创建时间
    if (queryParams.start_time) {
      const startDate = new Date(queryParams.start_time).getTime();
      filteredData = filteredData.filter(pos => {
        if (!pos.created_time) return false;
        return new Date(pos.created_time).getTime() >= startDate;
      });
    }
    if (queryParams.end_time) {
      const endDate = new Date(queryParams.end_time).getTime();
      filteredData = filteredData.filter(pos => {
        if (!pos.created_time) return false;
        return new Date(pos.created_time).getTime() <= endDate;
      });
    }

    // 前端过滤 - 创建人
    if (queryParams.created_id) {
      filteredData = filteredData.filter(pos => {
        return pos.created_by?.id === queryParams.created_id;
      });
    }

    allPositionsData.value = filteredData;
    total.value = filteredData.length;

    // 分页
    const start = (currentPage.value - 1) * pageSize.value;
    const end = start + pageSize.value;
    positions.value = filteredData.slice(start, end);
  } catch (error) {
    console.error('Failed to fetch positions:', error);
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  currentPage.value = 1;
  fetchPositions();
};

const handleReset = () => {
  queryParams.name = '';
  queryParams.status = '';
  queryParams.start_time = '';
  queryParams.end_time = '';
  queryParams.created_id = undefined;
  createdByName.value = '';
  handleSearch();
};

const handleRefresh = () => {
  fetchPositions();
  message.success('刷新成功');
};

const handleExport = () => {
  showExportDialog.value = true;
};

const handleExportConfirm = async (options: ExportOptions) => {
  try {
    // 使用组件返回的 fields，而不是从 exportFields 中筛选
    const selectedFieldKeys = options.fields;
    if (selectedFieldKeys.length === 0) {
      message.warning('请至少选择一个导出字段');
      return;
    }
    
    // 根据 key 获取完整的字段信息
    const selectedFields = exportFields.value.filter((f: ExportField) => selectedFieldKeys.includes(f.key));
    
    message.info('正在导出，请稍候...');
    
    let allData: any[] = [];
    
    if (options.range === 'selected' && selectedIds.value.length > 0) {
      allData = positions.value.filter(p => selectedIds.value.includes(p.id!));
    } else if (options.range === 'current') {
      allData = [...positions.value];
    } else {
      const queryParamsExport: any = {
        page_no: 1,
        page_size: 10000,
      };
      if (queryParams.name) queryParamsExport.name = queryParams.name;
      if (queryParams.status) queryParamsExport.status = queryParams.status;
      if (queryParams.start_time) queryParamsExport.start_time = queryParams.start_time;
      if (queryParams.end_time) queryParamsExport.end_time = queryParams.end_time;
      if (queryParams.created_id) queryParamsExport.created_id = queryParams.created_id;
      
      const res = await api.position.listPosition(queryParamsExport);
      if (res?.data?.items) {
        allData = res.data.items;
      } else if (res?.data?.data?.items) {
        allData = res.data.data.items;
      }
    }
    
    const headers = selectedFields.map((f: ExportField) => f.label);
    const keys = selectedFieldKeys;
    const timeFields = ['created_time', 'updated_time', 'created_at', 'updated_at'];
    
    if (options.format === 'csv') {
      // CSV 格式导出
      const csvContent = [
        headers.join(','),
        ...allData.map((row: any) => 
          keys.map((key: string) => {
            let value = row[key];
            if (value === null || value === undefined) value = '';
            value = String(value);
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
      link.download = `岗位列表_${new Date().toISOString().slice(0, 10)}.csv`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } else {
      // Excel 格式导出 (使用 xlsx 库)
      try {
        const XLSX = await import('xlsx');
        const exportData = allData.map((row: any) => {
          const obj: any = {};
          keys.forEach((key: string, index: number) => {
            obj[headers[index]] = row[key];
          });
          return obj;
        });
        
        const ws = XLSX.utils.json_to_sheet(exportData);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, '岗位列表');
        XLSX.writeFile(wb, `岗位列表_${new Date().toISOString().slice(0, 10)}.xlsx`);
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

// 用户选择器相关
const selectedUserForSelector = computed(() => {
  if (!queryParams.created_id) return [];
  return [{ id: queryParams.created_id, name: createdByName.value }] as User[];
});

// 处理用户选择
const handleUserSelect = (users: User[]) => {
  if (users.length > 0) {
    const user = users[0];
    queryParams.created_id = user.id;
    createdByName.value = user.name;
  }
};

const changePage = (page: number) => {
  currentPage.value = page;
  fetchPositions();
};

const handlePageSizeChange = () => {
  currentPage.value = 1;
  fetchPositions();
};

const toggleAllSelection = (e: Event) => {
  const checked = (e.target as HTMLInputElement).checked;
  if (checked) {
    selectedIds.value = positions.value.map(p => p.id!).filter(id => id !== undefined);
  } else {
    selectedIds.value = [];
  }
};

const handleAdd = () => {
  dialogType.value = 'create';
  Object.assign(form, defaultForm);
  dialogVisible.value = true;
};

const handleEdit = (position: PositionTable) => {
  dialogType.value = 'edit';
  Object.assign(form, {
    ...defaultForm,
    ...position
  });
  dialogVisible.value = true;
};

const handleView = async (position: PositionTable) => {
  dialogType.value = 'detail';
  if (position.id) {
    try {
      const res = await api.position.detailPosition(position.id);
      detailData.value = res?.data || {};
    } catch (error) {
      console.error('Failed to fetch position detail:', error);
    }
  }
  dialogVisible.value = true;
};

const closeDialog = () => {
  dialogVisible.value = false;
  Object.assign(form, defaultForm);
};

const submitForm = async () => {
  if (!form.name) {
    message.warning('请填写必填项');
    return;
  }
  
  submitting.value = true;
  try {
    if (isEdit.value) { 
      if (form.id) {
        await api.position.updatePosition(form.id, form);
      }
    } else {
      await api.position.createPosition(form);
    }
    closeDialog();
    fetchPositions();
    message.success('操作成功');
  } catch (error: any) {
    console.error('Operation failed:', error);
    const msg = error.data?.msg || error.message || '操作失败，请重试';
    message.error(msg);
  } finally {
    submitting.value = false;
  }
};

const handleDelete = async (position: PositionTable) => {
  try {
    await dialog.confirm(`确定要删除岗位 ${position.name} 吗？`)
    if (position.id) {
      await api.position.deletePosition([position.id]);
      fetchPositions();
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
    await dialog.confirm(`确定要删除选中的 ${selectedIds.value.length} 个岗位吗？`)
    await api.position.deletePosition(selectedIds.value);
    selectedIds.value = [];
    fetchPositions();
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
    await dialog.confirm(`确定要${statusText}选中的 ${selectedIds.value.length} 个岗位吗？`)
    await api.position.batchPosition({ ids: selectedIds.value, status });
    selectedIds.value = [];
    fetchPositions();
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

onMounted(() => {
  fetchPositions();
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
