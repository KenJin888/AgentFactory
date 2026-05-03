<template>
  <CrudPageShell
    title="角色管理"
    subtitle="配置角色权限与访问范围。"
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
    add-button-text="新增角色"
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
        <!-- 角色名称 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">角色名称</label>
          <div class="relative">
            <input
              v-model="queryParams.name"
              type="text"
              placeholder="请输入角色名称"
              class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
              @keyup.enter="handleSearch"
            />
            <ShieldIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
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
    </template>

    <!-- 表格区 -->
    <template #table>
      <table class="w-full text-sm" style="min-width: 1000px;">
        <thead class="bg-slate-50 text-slate-600 font-medium border-b border-slate-200">
          <tr>
            <th class="px-5 py-4 w-12 text-center">
              <input
                type="checkbox"
                class="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                @change="toggleAllSelection"
                :checked="isAllSelected"
              />
            </th>
            <th v-if="getColumnVisible('index')" class="px-5 py-4 text-center">序号</th>
            <th v-if="getColumnVisible('name')" class="px-5 py-4 text-center">角色名称</th>
            <th v-if="getColumnVisible('code')" class="px-5 py-4 text-center">角色编码</th>
            <th v-if="getColumnVisible('order')" class="px-5 py-4 text-center">排序</th>
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
          <tr v-else-if="dataList.length === 0">
            <td :colspan="visibleColumnCount" class="px-6 py-12 text-center text-slate-400">
              <div class="flex flex-col items-center gap-3">
                <InboxIcon class="w-12 h-12 text-slate-300" />
                <span>暂无数据</span>
              </div>
            </td>
          </tr>
          <tr v-else v-for="role in dataList" :key="role.id" class="hover:bg-slate-50/80 transition-colors group">
            <td class="px-5 py-4 text-center">
              <input
                type="checkbox"
                class="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                :value="role.id"
                v-model="selectedIds"
                :disabled="role.id === 1"
              />
            </td>
            <td v-if="getColumnVisible('index')" class="px-5 py-4 text-center text-slate-500">
              {{ (currentPage - 1) * pageSize + dataList.indexOf(role) + 1 }}
            </td>
            <td v-if="getColumnVisible('name')" class="px-5 py-4 text-center">
              <div class="font-semibold text-slate-900">{{ role.name }}</div>
            </td>
            <td v-if="getColumnVisible('code')" class="px-5 py-4 text-center">
              <div class="text-slate-600">{{ role.code || '-' }}</div>
            </td>
            <td v-if="getColumnVisible('order')" class="px-5 py-4 text-center">
              <div class="text-slate-600">{{ role.order }}</div>
            </td>
            <td v-if="getColumnVisible('status')" class="px-5 py-4 text-center">
              <span
                class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border"
                :class="role.status === '0' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-red-50 text-red-700 border-red-200'"
              >
                <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="role.status === '0' ? 'bg-emerald-500' : 'bg-red-500'"></span>
                {{ role.status === '0' ? '启用' : '停用' }}
              </span>
            </td>
            <td v-if="getColumnVisible('description')" class="px-5 py-4 text-center">
              <div class="text-slate-600 max-w-[150px] truncate">{{ role.description || '-' }}</div>
            </td>
            <td v-if="getColumnVisible('created_time')" class="px-5 py-4 text-center text-slate-500 whitespace-nowrap text-xs">
              {{ formatDate(role.created_time) }}
            </td>
            <td v-if="getColumnVisible('updated_time')" class="px-5 py-4 text-center text-slate-500 whitespace-nowrap text-xs">
              {{ formatDate(role.updated_time) }}
            </td>
            <td v-if="getColumnVisible('action')" class="px-5 py-4 text-center fixed-col">
              <div class="flex items-center justify-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  :disabled="role.id === 1 || !canPermission"
                  @click="handleAssignPerm(role)"
                  class="p-2 text-slate-800 hover:text-purple-600 hover:bg-purple-50 rounded-xl transition-all disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-transparent disabled:hover:text-slate-800"
                  :title="role.id === 1 ? '系统默认角色' : (canPermission ? '分配权限' : '无权限')"
                >
                  <ShieldIcon class="w-4 h-4" />
                </button>
                <button
                  :disabled="!canDetail"
                  @click="handleView(role)"
                  class="p-2 text-slate-800 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-transparent disabled:hover:text-slate-800"
                  :title="canDetail ? '详情' : '无权限'"
                >
                  <EyeIcon class="w-4 h-4" />
                </button>
                <button
                  :disabled="role.id === 1 || !canUpdate"
                  @click="handleEdit(role)"
                  class="p-2 text-slate-800 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-transparent disabled:hover:text-slate-800"
                  :title="role.id === 1 ? '系统默认角色' : (canUpdate ? '编辑' : '无权限')"
                >
                  <EditIcon class="w-4 h-4" />
                </button>
                <button
                  :disabled="role.id === 1 || !canDelete"
                  @click="handleDelete(role)"
                  class="p-2 text-slate-800 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-transparent disabled:hover:text-slate-800"
                  :title="role.id === 1 ? '系统默认角色' : (canDelete ? '删除' : '无权限')"
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

  <!-- Export Dialog -->
  <ExportDialog
    v-model:visible="showExportDialog"
    title="导出角色"
    :fields="exportFields"
    :selected-count="selectedIds.length"
    @confirm="handleExportConfirm"
  />

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
            <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">角色名称</div>
            <div class="font-semibold text-slate-900">{{ detailData.name }}</div>
          </div>
          <div class="p-4 bg-slate-50 rounded-xl">
            <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">排序</div>
            <div class="font-medium text-slate-900">{{ detailData.order }}</div>
          </div>
          <div class="p-4 bg-slate-50 rounded-xl">
            <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">角色编码</div>
            <div class="font-medium text-slate-900">{{ detailData.code || '-' }}</div>
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
          <label class="block text-sm font-medium text-slate-700 mb-2">角色名称 <span class="text-red-500">*</span></label>
          <input
            v-model="form.name"
            type="text"
            class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
            placeholder="请输入角色名称"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">角色编码 <span class="text-red-500">*</span></label>
          <input
            v-model="form.code"
            type="text"
            class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
            placeholder="请输入角色编码"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">排序</label>
          <input
            v-model.number="form.order"
            type="number"
            min="0"
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

  <!-- Permission Drawer -->
  <div v-if="permDrawerVisible" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex">
    <div class="bg-white w-[500px] ml-auto h-full shadow-2xl flex flex-col">
      <div class="px-6 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
        <h2 class="text-xl font-bold text-slate-900">分配权限 - {{ currentRole.name }}</h2>
        <button @click="permDrawerVisible = false" class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all">
          <XIcon class="w-5 h-5" />
        </button>
      </div>
      <div class="flex-1 overflow-y-auto p-6">
        <div class="mb-4 p-3 bg-slate-50 rounded-xl border border-slate-200">
          <label class="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" v-model="checkAll" @change="handleCheckAll" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500 w-4 h-4" />
            <span class="text-sm font-semibold text-slate-700">全选/取消</span>
          </label>
        </div>
        <div class="space-y-3">
          <div v-for="menu in menuTree" :key="menu.id" class="border border-slate-200 rounded-xl p-4 hover:border-blue-200 transition-colors">
            <label class="flex items-center gap-3 font-medium cursor-pointer">
              <input
                type="checkbox"
                :checked="isMenuChecked(menu.id)"
                :indeterminate="isMenuIndeterminate(menu)"
                @change="(e) => handleMenuCheck(menu, (e.target as HTMLInputElement).checked)"
                class="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
              />
              <span class="text-slate-800">{{ menu.title }}</span>
            </label>
            <div v-if="menu.children && menu.children.length > 0" class="ml-6 mt-3 space-y-2">
              <div v-for="child in menu.children" :key="child.id" class="border border-slate-100 rounded-lg p-3 bg-slate-50/50">
                <label class="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    :checked="isMenuChecked(child.id)"
                    :indeterminate="isMenuIndeterminate(child)"
                    @change="(e) => handleMenuCheck(child, (e.target as HTMLInputElement).checked)"
                    class="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span class="text-sm text-slate-700">{{ child.title }}</span>
                </label>
                <div v-if="child.children && child.children.length > 0" class="ml-6 mt-2 space-y-1">
                  <label v-for="grandChild in child.children" :key="grandChild.id" class="flex items-center gap-3 cursor-pointer">
                    <input
                      type="checkbox"
                      :checked="isMenuChecked(grandChild.id)"
                      @change="(e) => handleMenuCheck(grandChild, (e.target as HTMLInputElement).checked)"
                      class="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span class="text-sm text-slate-600">{{ grandChild.title }}</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="px-6 py-4 border-t border-slate-100 flex justify-end gap-3 bg-slate-50/30">
        <button
          @click="permDrawerVisible = false"
          class="px-5 py-2.5 border border-slate-200 rounded-xl text-slate-700 hover:bg-white hover:border-slate-300 transition-all"
        >
          取消
        </button>
        <button
          @click="savePermissions"
          :disabled="permSubmitting"
          class="px-5 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-all disabled:opacity-50 flex items-center gap-2 shadow-sm"
        >
          <Loader2Icon v-if="permSubmitting" class="w-4 h-4 animate-spin" />
          {{ permSubmitting ? '保存中...' : '保存' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import type { ExportOptions } from '@/components/common/ExportDialog.vue'
import ExportDialog from '@/components/common/ExportDialog.vue'
import { CrudPageShell } from '@/components/crud'
import { useCrudPage } from '@/composables/useCrudPage'
import { useCrudAuth } from '@/composables/useCrudAuth'
import {
  ChevronDown as ChevronDownIcon,
  ChevronUp as ChevronUpIcon,
  Edit as EditIcon,
  Eye as EyeIcon,
  Inbox as InboxIcon,
  Loader2 as Loader2Icon,
  Search as SearchIcon,
  Shield as ShieldIcon,
  Trash2 as TrashIcon,
  X as XIcon,
} from 'lucide-vue-next'
import { api } from '@/services/api'
import message from '@/components/common/message'
import { dialog } from '@/components/common/dialog'
import type { RoleForm, RoleTable } from '@/services/fastApi/module_system/role'

// 权限配置
const PERMS = {
  query: 'module_system:role:query',
  create: 'module_system:role:create',
  update: 'module_system:role:update',
  delete: 'module_system:role:delete',
  export: 'module_system:role:export',
  patch: 'module_system:role:patch',
  detail: 'module_system:role:detail',
  permission: 'module_system:role:permission',
} as const

// 使用 useCrudAuth 判断行内按钮权限
const permissionAuth = useCrudAuth({ permission: PERMS.permission })
const detailAuth = useCrudAuth({ detail: PERMS.detail })
const updateAuth = useCrudAuth({ update: PERMS.update })
const deleteAuth = useCrudAuth({ delete: PERMS.delete })

const canPermission = computed(() => permissionAuth.can('permission'))
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
  dataList,
  selectedIds,
  fetchData,
  handleSearch,
  handleReset,
  handleRefresh,
} = useCrudPage<RoleTable, { name: string; status: string; start_time: string; end_time: string }>({
  initialQuery: {
    name: '',
    status: '',
    start_time: '',
    end_time: '',
  },
  fetchList: async (params) => {
    const queryParamsExport: any = {
      page_no: params.page_no,
      page_size: params.page_size,
    }
    if (params.name) queryParamsExport.name = params.name
    if (params.status) queryParamsExport.status = params.status
    if (params.start_time || params.end_time) {
      const startTime = params.start_time ? params.start_time + ' 00:00:00' : ''
      const endTime = params.end_time ? params.end_time + ' 23:59:59' : ''
      if (startTime || endTime) {
        queryParamsExport.created_time = [startTime, endTime].filter(Boolean)
      }
    }

    const res = await api.role.listRole(queryParamsExport)
    return {
      items: res?.data?.items || [],
      total: res?.data?.total || 0,
    }
  },
})

// 其他状态
const isExpand = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogType = ref<'create' | 'edit' | 'detail'>('create')
const detailData = ref<any>({})

// Permission drawer
const permDrawerVisible = ref(false)
const permSubmitting = ref(false)
const currentRole = ref<RoleTable>({} as RoleTable)
const menuTree = ref<any[]>([])
const selectedMenus = ref<number[]>([])
const checkAll = ref(false)

const showExportDialog = ref(false)

interface ExportField {
  key: string
  label: string
  checked: boolean
}

const exportFields = ref<ExportField[]>([
  { key: 'name', label: '角色名称', checked: true },
  { key: 'code', label: '角色编码', checked: true },
  { key: 'order', label: '排序', checked: true },
  { key: 'status', label: '状态', checked: true },
  { key: 'description', label: '描述', checked: true },
  { key: 'created_time', label: '创建时间', checked: true },
  { key: 'updated_time', label: '更新时间', checked: true },
])

const columnOptions = ref([
  { key: 'index', label: '序号', visible: true },
  { key: 'name', label: '角色名称', visible: true },
  { key: 'code', label: '角色编码', visible: true },
  { key: 'order', label: '排序', visible: true },
  { key: 'status', label: '状态', visible: true },
  { key: 'description', label: '描述', visible: true },
  { key: 'created_time', label: '创建时间', visible: false },
  { key: 'updated_time', label: '更新时间', visible: false },
  { key: 'action', label: '操作', visible: true },
])

const getColumnVisible = (key: string) => {
  const col = columnOptions.value.find((c) => c.key === key)
  return col ? col.visible : true
}

const handleColumnChange = (key: string, visible: boolean) => {
  const col = columnOptions.value.find((c) => c.key === key)
  if (col) {
    col.visible = visible
  }
}

const visibleColumnCount = computed(() => {
  return columnOptions.value.filter((c) => c.visible).length + 1
})

const defaultForm: RoleForm = {
  name: '',
  code: '',
  order: 1,
  status: '0',
  description: '',
}

const form = reactive<RoleForm>({ ...defaultForm })

// Computed
const isAllSelected = computed(() => {
  const selectableRoles = dataList.value.filter((r) => r.id !== 1)
  return selectableRoles.length > 0 && selectableRoles.every((r) => selectedIds.value.includes(r.id!))
})

const dialogTitle = computed(() => {
  if (dialogType.value === 'detail') return '角色详情'
  if (dialogType.value === 'edit') return '编辑角色'
  return '新增角色'
})

const isEdit = computed(() => dialogType.value === 'edit')

// Methods
const handleExport = () => {
  showExportDialog.value = true
}

const handleExportConfirm = async (options: ExportOptions) => {
  try {
    const selectedFieldKeys = options.fields
    if (selectedFieldKeys.length === 0) {
      message.warning('请至少选择一个导出字段')
      return
    }

    const selectedFields = exportFields.value.filter((f: ExportField) => selectedFieldKeys.includes(f.key))

    message.info('正在导出，请稍候...')

    let allData: any[] = []

    if (options.range === 'selected' && selectedIds.value.length > 0) {
      allData = dataList.value.filter((r) => selectedIds.value.includes(r.id!))
    } else if (options.range === 'current') {
      allData = [...dataList.value]
    } else {
      const queryParamsExport: any = {
        page_no: 1,
        page_size: 10000,
      }
      if (queryParams.name) queryParamsExport.name = queryParams.name
      if (queryParams.status) queryParamsExport.status = queryParams.status
      if (queryParams.start_time) queryParamsExport.start_time = queryParams.start_time
      if (queryParams.end_time) queryParamsExport.end_time = queryParams.end_time

      const res = await api.role.listRole(queryParamsExport)
      const resData = res as any
      if (resData?.items) {
        allData = resData.items
      } else if (resData?.data?.items) {
        allData = resData.data.items
      }
    }

    const headers = selectedFields.map((f: ExportField) => f.label)
    const keys = selectedFieldKeys
    const timeFields = ['created_time', 'updated_time', 'created_at', 'updated_at']

    if (options.format === 'csv') {
      const csvContent = [
        headers.join(','),
        ...allData.map((row: any) =>
          keys
            .map((key: string) => {
              let value = row[key]
              if (value === null || value === undefined) value = ''
              value = String(value)
              if (timeFields.includes(key) && value) {
                value = ' ' + value
              }
              if (value.includes(',') || value.includes('"') || value.includes('\n')) {
                value = `"${value.replace(/"/g, '""')}"`
              }
              return value
            })
            .join(',')
        ),
      ].join('\n')

      const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `角色列表_${new Date().toISOString().slice(0, 10)}.csv`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } else {
      try {
        const XLSX = await import('xlsx')
        const exportData = allData.map((row: any) => {
          const obj: any = {}
          keys.forEach((key: string, index: number) => {
            obj[headers[index]] = row[key]
          })
          return obj
        })

        const ws = XLSX.utils.json_to_sheet(exportData)
        const wb = XLSX.utils.book_new()
        XLSX.utils.book_append_sheet(wb, ws, '角色列表')
        XLSX.writeFile(wb, `角色列表_${new Date().toISOString().slice(0, 10)}.xlsx`)
      } catch (xlsxError) {
        message.error('Excel 导出失败，请确保已安装 xlsx 库')
        console.error('XLSX export failed:', xlsxError)
        return
      }
    }

    message.success('导出成功')
  } catch (error) {
    console.error('Export failed:', error)
    message.error('导出失败')
  }
}

const handleAdd = () => {
  dialogType.value = 'create'
  Object.assign(form, defaultForm)
  dialogVisible.value = true
}

const handleEdit = (role: RoleTable) => {
  if (role.id === 1) {
    message.warning('系统默认角色，不可操作')
    return
  }
  dialogType.value = 'edit'
  Object.assign(form, {
    ...defaultForm,
    ...role,
  })
  dialogVisible.value = true
}

const handleView = async (role: RoleTable) => {
  dialogType.value = 'detail'
  if (role.id) {
    try {
      const res = await api.role.detailRole(role.id)
      detailData.value = res?.data || {}
    } catch (error) {
      console.error('Failed to fetch role detail:', error)
    }
  }
  dialogVisible.value = true
}

const closeDialog = () => {
  dialogVisible.value = false
  Object.assign(form, defaultForm)
}

const submitForm = async () => {
  if (!form.name || !form.code) {
    message.warning('请填写必填项')
    return
  }

  submitting.value = true
  try {
    if (isEdit.value) {
      if (form.id) {
        await api.role.updateRole(form.id, form)
      }
    } else {
      await api.role.createRole(form)
    }
    closeDialog()
    fetchData()
    message.success('操作成功')
  } catch (error: any) {
    console.error('Operation failed:', error)
    const msg = error.data?.msg || error.message || '操作失败，请重试'
    message.error(msg)
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (role: RoleTable) => {
  if (role.id === 1) {
    message.warning('系统默认角色，不可操作')
    return
  }
  try {
    await dialog.confirm(`确定要删除角色 ${role.name} 吗？`)
    if (role.id) {
      await api.role.deleteRole([role.id])
      fetchData()
      message.success('删除成功')
    }
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error('Delete failed:', error)
    message.error('删除失败')
  }
}

const handleBatchDelete = async () => {
  if (selectedIds.value.length === 0) return

  const hasSystemRole = selectedIds.value.includes(1)
  if (hasSystemRole) {
    message.warning('系统默认角色，不可操作')
    return
  }

  try {
    await dialog.confirm(`确定要删除选中的 ${selectedIds.value.length} 个角色吗？`)
    await api.role.deleteRole(selectedIds.value as number[])
    fetchData()
    message.success('批量删除成功')
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error('Batch delete failed:', error)
    message.error('批量删除失败')
  }
}

const handleBatchStatus = async (status: string) => {
  if (selectedIds.value.length === 0) return

  const hasSystemRole = selectedIds.value.includes(1)
  if (hasSystemRole) {
    message.warning('系统默认角色，不可操作')
    return
  }

  try {
    const statusText = status === '0' ? '启用' : '停用'
    await dialog.confirm(`确定要${statusText}选中的 ${selectedIds.value.length} 个角色吗？`)
    await api.role.batchRole({ ids: selectedIds.value as number[], status })
    fetchData()
    message.success(`批量${statusText}成功`)
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error('Batch status change failed:', error)
    message.error('操作失败')
  }
}

// Permission assignment
const handleAssignPerm = async (role: RoleTable) => {
  if (role.id === 1) {
    message.warning('系统默认角色，不可操作')
    return
  }
  currentRole.value = role
  selectedMenus.value = []

  try {
    const res = await api.menu.listMenu({})
    if (res?.data) {
      menuTree.value = res.data || []
    }
    const roleRes = await api.role.detailRole(role.id!)
    if (roleRes?.data?.menus) {
      selectedMenus.value = roleRes.data.menus.map((m: any) => m.id)
    }
    updateCheckAllState()
  } catch (error) {
    console.error('Failed to load permission data:', error)
  }

  permDrawerVisible.value = true
}

// 获取所有子节点ID（递归）
const getAllChildrenIds = (menu: any): number[] => {
  let ids: number[] = [menu.id]
  if (menu.children && menu.children.length > 0) {
    menu.children.forEach((child: any) => {
      ids = ids.concat(getAllChildrenIds(child))
    })
  }
  return ids
}

// 获取所有父节点ID（递归向上）
const getAllParentIds = (menuId: number, menus: any[], parentChain: number[] = []): number[] => {
  for (const menu of menus) {
    if (menu.id === menuId) {
      return parentChain
    }
    if (menu.children && menu.children.length > 0) {
      const result = getAllParentIds(menuId, menu.children, [...parentChain, menu.id])
      if (result.length > 0 || menu.children.some((c: any) => c.id === menuId)) {
        return result
      }
    }
  }
  return []
}

// 检查菜单是否被选中
const isMenuChecked = (menuId: number): boolean => {
  return selectedMenus.value.includes(menuId)
}

// 检查菜单是否有子节点被选中（半选状态）
const isMenuIndeterminate = (menu: any): boolean => {
  if (!menu.children || menu.children.length === 0) {
    return false
  }
  const childrenIds = getAllChildrenIds(menu).filter((id) => id !== menu.id)
  const checkedChildren = childrenIds.filter((id) => selectedMenus.value.includes(id))
  const isChecked = selectedMenus.value.includes(menu.id)

  return (!isChecked && checkedChildren.length > 0) || (isChecked && checkedChildren.length > 0 && checkedChildren.length < childrenIds.length)
}

// 处理菜单选中/取消
const handleMenuCheck = (menu: any, checked: boolean) => {
  const menuId = menu.id

  if (checked) {
    const allIds = getAllChildrenIds(menu)
    allIds.forEach((id) => {
      if (!selectedMenus.value.includes(id)) {
        selectedMenus.value.push(id)
      }
    })

    const parentIds = getAllParentIds(menuId, menuTree.value)
    parentIds.forEach((id) => {
      if (!selectedMenus.value.includes(id)) {
        selectedMenus.value.push(id)
      }
    })
  } else {
    const allIds = getAllChildrenIds(menu)
    selectedMenus.value = selectedMenus.value.filter((id) => !allIds.includes(id))
  }

  updateCheckAllState()
}

// 更新全选状态
const updateCheckAllState = () => {
  const allIds = getAllMenuIds(menuTree.value)
  if (allIds.length === 0) {
    checkAll.value = false
    return
  }
  checkAll.value = allIds.every((id) => selectedMenus.value.includes(id))
}

// 获取所有菜单ID
const getAllMenuIds = (menus: any[]): number[] => {
  let ids: number[] = []
  menus.forEach((m) => {
    ids.push(m.id)
    if (m.children) {
      ids = ids.concat(getAllMenuIds(m.children))
    }
  })
  return ids
}

const handleCheckAll = () => {
  if (checkAll.value) {
    selectedMenus.value = getAllMenuIds(menuTree.value)
  } else {
    selectedMenus.value = []
  }
}

const savePermissions = async () => {
  permSubmitting.value = true
  try {
    await api.role.assignRolePerm(currentRole.value.id!, { menu_ids: selectedMenus.value })
    permDrawerVisible.value = false
    message.success('权限分配成功')
  } catch (error: any) {
    console.error('Failed to save permissions:', error)
    message.error(error.data?.msg || '保存失败')
  } finally {
    permSubmitting.value = false
  }
}

const formatDate = (dateStr?: string) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString()
}

const toggleAllSelection = (e: Event) => {
  const checked = (e.target as HTMLInputElement).checked
  if (checked) {
    selectedIds.value = dataList.value.map((r) => r.id!).filter((id) => id !== undefined && id !== 1)
  } else {
    selectedIds.value = []
  }
}

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
