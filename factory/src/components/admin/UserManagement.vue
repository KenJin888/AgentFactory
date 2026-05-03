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
             <UserIcon class="text-blue-600" /> 用户管理
          </h1>
        </div>
        <div class="flex gap-3">
          <button
            @click="handleAdd"
            class="px-6 py-3 bg-blue-600 text-white rounded-xl font-bold hover:bg-blue-700 shadow-lg flex items-center gap-2 transition-transform active:scale-95"
          >
              <PlusIcon :size="20" /> 新增用户
          </button>
        </div>
      </div>

      <!-- Search & Filter Card -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 mb-6 overflow-hidden">
        <div class="p-6">
          <!-- 第一行：四个等分列 -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
            <!-- 账号 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">账号</label>
              <div class="relative">
                <input
                  v-model="queryParams.username"
                  type="text"
                  placeholder="请输入账号"
                  class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                  @keyup.enter="handleSearch"
                />
                <UserIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              </div>
            </div>
            <!-- 用户名 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">用户名</label>
              <div class="relative">
                <input
                  v-model="queryParams.name"
                  type="text"
                  placeholder="请输入用户名"
                  class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                  @keyup.enter="handleSearch"
                />
                <UserIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
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
            <!-- 部门 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">部门</label>
              <select
                v-model="queryParams.dept_id"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all appearance-none cursor-pointer"
              >
                <option value="">全部</option>
                <option v-for="dept in deptTree" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
              </select>
            </div>
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
          </div>
        </div>
      </div>

      <!-- User Table Card -->
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
              @click="showImportDialog = true"
              class="p-2.5 text-slate-600 hover:bg-slate-100 rounded-xl transition-all"
              title="导入"
            >
              <UploadIcon class="w-5 h-5" />
            </button>
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
                <th v-if="getColumnVisible('avatar')" class="px-5 py-4 text-center">头像</th>
                <th v-if="getColumnVisible('username')" class="px-5 py-4 text-center">账号</th>
                <th v-if="getColumnVisible('name')" class="px-5 py-4 text-center">用户名</th>
                <th v-if="getColumnVisible('dept')" class="px-5 py-4 text-center">部门</th>
                <th v-if="getColumnVisible('gender')" class="px-5 py-4 text-center">性别</th>
                <th v-if="getColumnVisible('role')" class="px-5 py-4 text-center">角色</th>
                <th v-if="getColumnVisible('position')" class="px-5 py-4 text-center">岗位</th>
                <th v-if="getColumnVisible('status')" class="px-5 py-4 text-center">状态</th>
                <th v-if="getColumnVisible('is_superuser')" class="px-5 py-4 text-center">是否超管</th>
                <th v-if="getColumnVisible('mobile')" class="px-5 py-4 text-center">手机号</th>
                <th v-if="getColumnVisible('email')" class="px-5 py-4 text-center">邮箱</th>
                <th v-if="getColumnVisible('created_time')" class="px-5 py-4 text-center">创建时间</th>
                <th v-if="getColumnVisible('updated_time')" class="px-5 py-4 text-center">更新时间</th>
                <th v-if="getColumnVisible('created_by')" class="px-5 py-4 text-center">创建人</th>
                <th v-if="getColumnVisible('updated_by')" class="px-5 py-4 text-center">更新人</th>
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
              <tr v-else-if="users.length === 0">
                <td :colspan="visibleColumnCount" class="px-6 py-12 text-center text-slate-400">
                  <div class="flex flex-col items-center gap-3">
                    <InboxIcon class="w-12 h-12 text-slate-300" />
                    <span>暂无数据</span>
                  </div>
                </td>
              </tr>
              <tr v-else v-for="user in users" :key="user.id" class="hover:bg-slate-50/80 transition-colors group">
                <td class="px-5 py-4 text-center">
                  <input type="checkbox" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" :value="user.id" v-model="selectedIds" :disabled="user.is_superuser" />
                </td>
                <td v-if="getColumnVisible('index')" class="px-5 py-4 text-center text-slate-500">
                  {{ (currentPage - 1) * pageSize + users.indexOf(user) + 1 }}
                </td>
                <td v-if="getColumnVisible('avatar')" class="px-5 py-4 text-center">
                  <div class="w-9 h-9 rounded-full bg-gradient-to-br from-blue-100 to-blue-50 flex items-center justify-center overflow-hidden mx-auto ring-2 ring-white shadow-sm">
                    <img v-if="user.avatar" :src="user.avatar" alt="avatar" class="w-full h-full object-cover" />
                    <UserIcon v-else class="w-4 h-4 text-blue-500" />
                  </div>
                </td>
                <td v-if="getColumnVisible('username')" class="px-5 py-4 text-center">
                  <div class="font-semibold text-slate-900">{{ user.username }}</div>
                </td>
                <td v-if="getColumnVisible('name')" class="px-5 py-4 text-center">
                  <div class="text-slate-700">{{ user.name }}</div>
                </td>
                <td v-if="getColumnVisible('dept')" class="px-5 py-4 text-center">
                  <span v-if="user.dept?.name" class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium bg-blue-50 text-blue-700 border border-blue-100">
                    {{ user.dept.name }}
                  </span>
                  <span v-else class="text-slate-400">-</span>
                </td>
                <td v-if="getColumnVisible('gender')" class="px-5 py-4 text-center">
                  <span
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                    :class="getGenderClass(user.gender)"
                  >
                    {{ getGenderText(user.gender) }}
                  </span>
                </td>
                <td v-if="getColumnVisible('role')" class="px-5 py-4 text-center">
                  <div class="flex flex-wrap gap-1 justify-center">
                    <template v-if="user.role_names && user.role_names.length > 0">
                      <span v-for="role in user.role_names" :key="role" class="inline-flex items-center px-2 py-0.5 rounded-lg text-xs font-medium bg-purple-50 text-purple-700 border border-purple-100">
                        {{ role }}
                      </span>
                    </template>
                    <template v-else-if="user.roles && user.roles.length > 0">
                      <span v-for="role in user.roles" :key="role.id" class="inline-flex items-center px-2 py-0.5 rounded-lg text-xs font-medium bg-purple-50 text-purple-700 border border-purple-100">
                        {{ role.name }}
                      </span>
                    </template>
                    <span v-else class="text-slate-400">-</span>
                  </div>
                </td>
                <td v-if="getColumnVisible('position')" class="px-5 py-4 text-center">
                  <div class="flex flex-wrap gap-1 justify-center">
                    <template v-if="user.position_names && user.position_names.length > 0">
                      <span v-for="pos in user.position_names" :key="pos" class="inline-flex items-center px-2 py-0.5 rounded-lg text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-100">
                        {{ pos }}
                      </span>
                    </template>
                    <template v-else-if="user.positions && user.positions.length > 0">
                      <span v-for="pos in user.positions" :key="pos.id" class="inline-flex items-center px-2 py-0.5 rounded-lg text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-100">
                        {{ pos.name }}
                      </span>
                    </template>
                    <span v-else class="text-slate-400">-</span>
                  </div>
                </td>
                <td v-if="getColumnVisible('status')" class="px-5 py-4 text-center">
                  <span
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                    :class="user.status === '0' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-red-50 text-red-700 border border-red-200'"
                  >
                    <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="user.status === '0' ? 'bg-emerald-500' : 'bg-red-500'"></span>
                    {{ user.status === '0' ? '启用' : '停用' }}
                  </span>
                </td>
                <td v-if="getColumnVisible('is_superuser')" class="px-5 py-4 text-center">
                  <span
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                    :class="user.is_superuser ? 'bg-amber-50 text-amber-700 border border-amber-200' : 'bg-slate-100 text-slate-600 border border-slate-200'"
                  >
                    {{ user.is_superuser ? '是' : '否' }}
                  </span>
                </td>
                <td v-if="getColumnVisible('mobile')" class="px-5 py-4 text-center text-slate-600">{{ user.mobile || '-' }}</td>
                <td v-if="getColumnVisible('email')" class="px-5 py-4 text-center text-slate-600">{{ user.email || '-' }}</td>
                <td v-if="getColumnVisible('created_time')" class="px-5 py-4 text-center text-slate-500 whitespace-nowrap text-xs">
                  {{ formatDate(user.created_time) }}
                </td>
                <td v-if="getColumnVisible('updated_time')" class="px-5 py-4 text-center text-slate-500 whitespace-nowrap text-xs">
                  {{ formatDate(user.updated_time) }}
                </td>
                <td v-if="getColumnVisible('created_by')" class="px-5 py-4 text-center text-slate-600">{{ user.created_by?.name || '-' }}</td>
                <td v-if="getColumnVisible('updated_by')" class="px-5 py-4 text-center text-slate-600">{{ user.updated_by?.name || '-' }}</td>
                <td v-if="getColumnVisible('action')" class="px-5 py-4 text-center fixed-col">
                  <div class="flex items-center justify-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      @click="handleResetPassword(user)"
                      class="p-2 text-slate-800 hover:text-amber-600 hover:bg-amber-50 rounded-xl transition-all"
                      title="重置密码"
                    >
                      <KeyIcon class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleView(user)"
                      class="p-2 text-slate-800 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all"
                      title="详情"
                    >
                      <EyeIcon class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleEdit(user)"
                      class="p-2 rounded-xl transition-all"
                      :class="user.is_superuser ? 'text-slate-300 cursor-not-allowed' : 'text-slate-800 hover:text-blue-600 hover:bg-blue-50'"
                      title="编辑"
                      :disabled="user.is_superuser"
                    >
                      <EditIcon class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleDelete(user)"
                      class="p-2 rounded-xl transition-all"
                      :class="user.is_superuser ? 'text-slate-300 cursor-not-allowed' : 'text-slate-800 hover:text-red-600 hover:bg-red-50'"
                      title="删除"
                      :disabled="user.is_superuser"
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
              :disabled="users.length < pageSize"
              class="px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-sm disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-50 hover:border-slate-300 transition-all"
            >
              下一页
            </button>
          </div>
        </div>
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

    <!-- Role Selector Dialog -->
    <RoleSelector
      v-model:visible="showRoleSelector"
      title="选择角色"
      :multiple="true"
      :initial-selected="selectedRolesForSelector"
      @confirm="handleRoleSelect"
    />

    <!-- Import Dialog -->
    <ImportDialog
      ref="importDialogRef"
      v-model:visible="showImportDialog"
      title="导入用户"
      description="请选择要导入的 Excel 文件（.xlsx 或 .xls 格式）"
      accept=".xlsx,.xls"
      acceptText=".xlsx, .xls 格式"
      :importing="importing"
      @import="handleImportSubmit"
      @download-template="handleDownloadTemplate"
    />
    
    <!-- Export Dialog -->
    <ExportDialog
      v-model:visible="showExportDialog"
      title="导出用户"
      :fields="exportFields"
      :selected-count="selectedIds.length"
      @confirm="handleExportConfirm"

    />
    
    <!-- Add/Edit Modal -->
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
            <div class="flex items-center gap-5 mb-6">
              <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-blue-100 to-blue-50 flex items-center justify-center overflow-hidden ring-4 ring-white shadow-lg">
                <img v-if="detailData.avatar" :src="detailData.avatar" alt="avatar" class="w-full h-full object-cover" />
                <UserIcon v-else class="w-10 h-10 text-blue-500" />
              </div>
              <div>
                <div class="text-xl font-bold text-slate-900">{{ detailData.username }}</div>
                <div class="text-slate-500 mt-1">{{ detailData.name }}</div>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-5">
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">性别</div>
                <div class="font-medium text-slate-900">{{ getGenderText(detailData.gender) }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">部门</div>
                <div class="font-medium text-slate-900">{{ detailData.dept_name || '-' }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">角色</div>
                <div class="font-medium text-slate-900">
                  <template v-if="detailData.role_names && detailData.role_names.length > 0">
                    {{ detailData.role_names.join('、') }}
                  </template>
                  <template v-else-if="detailData.roles && detailData.roles.length > 0">
                    {{ detailData.roles.map((r: any) => r.name).join('、') }}
                  </template>
                  <span v-else>-</span>
                </div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">岗位</div>
                <div class="font-medium text-slate-900">
                  <template v-if="detailData.position_names && detailData.position_names.length > 0">
                    {{ detailData.position_names.join('、') }}
                  </template>
                  <template v-else-if="detailData.positions && detailData.positions.length > 0">
                    {{ detailData.positions.map((p: any) => p.name).join('、') }}
                  </template>
                  <span v-else>-</span>
                </div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">邮箱</div>
                <div class="font-medium text-slate-900">{{ detailData.email || '-' }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">手机号</div>
                <div class="font-medium text-slate-900">{{ detailData.mobile || '-' }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">是否超管</div>
                <span :class="detailData.is_superuser ? 'bg-amber-100 text-amber-700' : 'bg-slate-100 text-slate-600'" class="px-2.5 py-1 rounded-lg text-xs font-medium">
                  {{ detailData.is_superuser ? '是' : '否' }}
                </span>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">状态</div>
                <span :class="detailData.status === '0' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'" class="px-2.5 py-1 rounded-lg text-xs font-medium">
                  {{ detailData.status === '0' ? '启用' : '停用' }}
                </span>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">上次登录时间</div>
                <div class="font-medium text-slate-900">{{ detailData.last_login || '-' }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">创建人</div>
                <div class="font-medium text-slate-900">{{ detailData.created_by?.name || '-' }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">更新人</div>
                <div class="font-medium text-slate-900">{{ detailData.updated_by?.name || '-' }}</div>
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
          <div v-else class="space-y-5">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">账号 <span class="text-red-500">*</span></label>
                <input
                  v-model="form.username"
                  type="text"
                  :disabled="isEdit"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 disabled:bg-slate-100 disabled:text-slate-500 transition-all"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">用户名 <span class="text-red-500">*</span></label>
                <input
                  v-model="form.name"
                  type="text"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
              </div>
              
              <div v-if="!isEdit">
                <label class="block text-sm font-medium text-slate-700 mb-2">密码 <span class="text-red-500">*</span></label>
                <input
                  v-model="form.password"
                  type="password"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">邮箱</label>
                <input
                  v-model="form.email"
                  type="email"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">手机号</label>
                <input
                  v-model="form.mobile"
                  type="tel"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">性别</label>
                <select v-model="form.gender" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all">
                  <option value="0">男</option>
                  <option value="1">女</option>
                  <option value="2">未知</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">状态</label>
                <select v-model="form.status" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all">
                  <option value="0">启用</option>
                  <option value="1">停用</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">部门</label>
                <select v-model="form.dept_id" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all">
                  <option value="">请选择部门</option>
                  <option v-for="dept in deptTree" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
                </select>
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-slate-700 mb-2">角色</label>
                <div class="flex flex-wrap gap-2 p-3 bg-slate-50 border border-slate-200 rounded-xl min-h-[50px] cursor-pointer" @click="initRoleSelector(); showRoleSelector = true">
                  <template v-if="selectedRoleNames.length > 0">
                    <span 
                      v-for="name in selectedRoleNames" 
                      :key="name" 
                      class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium bg-purple-50 text-purple-700 border border-purple-100"
                    >
                      {{ name }}
                    </span>
                  </template>
                  <span v-else class="text-slate-400 text-sm">点击选择角色</span>
                </div>
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-slate-700 mb-2">岗位</label>
                <div class="flex flex-wrap gap-2 p-3 bg-slate-50 border border-slate-200 rounded-xl min-h-[50px]">
                  <label v-for="pos in positionOptions" :key="pos.value" class="flex items-center gap-2 cursor-pointer px-3 py-1.5 bg-white rounded-lg border border-slate-200 hover:border-blue-300 hover:shadow-sm transition-all">
                    <input type="checkbox" :value="pos.value" v-model="form.position_ids" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
                    <span class="text-sm text-slate-700">{{ pos.label }}</span>
                  </label>
                </div>
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-slate-700 mb-2">头像</label>
                <div class="flex items-center gap-4">
                  <!-- 头像预览 -->
                  <div class="relative group cursor-pointer" @click="avatarInputRef?.click()">
                    <div class="w-20 h-20 rounded-2xl bg-slate-50 border border-slate-200 overflow-hidden flex items-center justify-center">
                      <img v-if="form.avatar" :src="form.avatar" class="w-full h-full object-cover" alt="avatar" />
                      <UserIcon v-else class="w-8 h-8 text-slate-300" />
                    </div>
                    <!-- 上传中遮罩 -->
                    <div v-if="avatarUploading" class="absolute inset-0 bg-black/50 flex items-center justify-center rounded-2xl">
                      <Loader2Icon class="w-6 h-6 animate-spin text-white" />
                    </div>
                    <!-- Hover 提示 -->
                    <div class="absolute inset-0 bg-black/40 flex flex-col items-center justify-center text-white opacity-0 group-hover:opacity-100 transition-opacity rounded-2xl">
                      <CameraIcon class="w-5 h-5" />
                      <span class="text-xs mt-0.5">上传</span>
                    </div>
                  </div>
                  <!-- 隐藏的文件输入 -->
                  <input
                    ref="avatarInputRef"
                    type="file"
                    class="hidden"
                    accept="image/png, image/jpeg, image/jpg"
                    @change="handleAvatarUpload"
                  />
                  <!-- 操作按钮 -->
                  <div class="flex flex-col gap-2">
                    <button
                      type="button"
                      @click="avatarInputRef?.click()"
                      class="px-4 py-2 bg-slate-900 text-white text-sm rounded-lg hover:bg-slate-800 transition-all flex items-center gap-2"
                    >
                      <UploadIcon class="w-4 h-4" />
                      上传头像
                    </button>
                    <button
                      v-if="form.avatar"
                      type="button"
                      @click="form.avatar = ''"
                      class="px-4 py-2 border border-slate-200 text-slate-600 text-sm rounded-lg hover:bg-slate-50 transition-all"
                    >
                      清除头像
                    </button>
                  </div>
                  <div class="text-xs text-slate-400">
                    支持 JPG/PNG 格式<br>最大 1MB
                  </div>
                </div>
              </div>
              <div class="md:col-span-2">
                <label class="flex items-center gap-3 cursor-pointer p-3 bg-slate-50 rounded-xl border border-slate-200 hover:border-blue-300 hover:bg-blue-50/30 transition-all">
                  <input type="checkbox" v-model="form.is_superuser" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500 w-5 h-5" />
                  <span class="text-sm font-medium text-slate-700">超级管理员</span>
                </label>
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
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, computed, watch, nextTick } from 'vue';
import ExportDialog from '@/components/common/ExportDialog.vue';
import ImportDialog from '@/components/common/ImportDialog.vue';
import UserSelector from '@/components/common/UserSelector.vue';
import RoleSelector from '@/components/common/RoleSelector.vue';
import type { ExportOptions } from '@/components/common/ExportDialog.vue';
import type { User } from '@/types/user';
import type { Role } from '@/components/common/RoleSelector.vue';
import { useRouter } from 'vue-router';
import { 
  ArrowLeft as ArrowLeftIcon,
  Plus as PlusIcon, 
  Trash2 as TrashIcon, 
  Edit as EditIcon, 
  User as UserIcon,
  Eye as EyeIcon,
  Key as KeyIcon,
  X as XIcon,
  ChevronUp as ChevronUpIcon,
  ChevronDown as ChevronDownIcon,
  Upload as UploadIcon,
  Download as DownloadIcon,
  RefreshCw as RefreshCwIcon,
  Settings as SettingsIcon,
  Search as SearchIcon,
  Loader2 as Loader2Icon,
  Inbox as InboxIcon,
  Play as PlayIcon,
  Pause as PauseIcon,
  Camera as CameraIcon
} from 'lucide-vue-next';
import {api} from '@/services/api';
import { useUserStore } from '@/stores/user';
import message from '@/components/common/message';
import { dialog } from '@/components/common/dialog';
import type { UserInfo, UserForm } from '@/services/fastApi/module_system/user';
import type { RoleTable } from '@/services/fastApi/module_system/role';

const router = useRouter();
const userStore = useUserStore();

// State
const loading = ref(false);
const submitting = ref(false);
const users = ref<UserInfo[]>([]);
const total = ref(0);
const currentPage = ref(1);
const pageSize = ref(10);
const dialogVisible = ref(false);
const dialogType = ref<'create' | 'edit' | 'detail'>('create');
const selectedIds = ref<number[]>([]);
const deptTree = ref<any[]>([]);
const roleOptions = ref<Array<{ value: number; label: string; code?: string; disabled?: boolean }>>([]);
const positionOptions = ref<Array<{ value: number; label: string; disabled?: boolean }>>([]);
const detailData = ref<any>({});

const queryParams = reactive({
  username: '',
  name: '',
  status: '',
  dept_id: '' as number | string,
  start_time: '',
  end_time: '',
  created_id: undefined as number | undefined
});

const isExpand = ref(false);
const createdByName = ref('');
const showUserSelector = ref(false);
const showRoleSelector = ref(false);
const showImportDialog = ref(false);
const showExportDialog = ref(false);
const importDialogRef = ref<InstanceType<typeof ImportDialog> | null>(null);
const selectedUserForSelector = ref<User[]>([]);
const selectedRolesForSelector = ref<Role[]>([]);

// Avatar upload
const avatarInputRef = ref<HTMLInputElement | null>(null);
const avatarUploading = ref(false);

interface ExportField {
  key: string;
  label: string;
  checked: boolean;
}

const exportFields = ref<ExportField[]>([
  { key: 'username', label: '账号', checked: true },
  { key: 'name', label: '用户名', checked: true },
  { key: 'dept_name', label: '部门', checked: true },
  { key: 'mobile', label: '手机号', checked: true },
  { key: 'email', label: '邮箱', checked: true },
  { key: 'gender', label: '性别', checked: true },
  { key: 'status', label: '状态', checked: true },
  { key: 'created_time', label: '创建时间', checked: true },
  { key: 'updated_time', label: '更新时间', checked: true },
  { key: 'created_by', label: '创建人', checked: true },
  { key: 'updated_by', label: '更新人', checked: true },
]);

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
  { key: 'avatar', label: '头像', visible: true },
  { key: 'username', label: '账号', visible: true },
  { key: 'name', label: '用户名', visible: true },
  { key: 'dept', label: '部门', visible: true },
  { key: 'gender', label: '性别', visible: true },
  { key: 'role', label: '角色', visible: true },
  { key: 'position', label: '岗位', visible: true },
  { key: 'status', label: '状态', visible: true },
  { key: 'is_superuser', label: '是否超管', visible: true },
  { key: 'mobile', label: '手机号', visible: true },
  { key: 'email', label: '邮箱', visible: false },
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
  return columnOptions.value.filter(c => c.visible).length + 1;
});

// 已选角色名称列表
const selectedRoleNames = computed(() => {
  return form.role_ids?.map((id: number) => {
    const role = roleOptions.value.find(r => r.value === id);
    return role?.label || '';
  }).filter(Boolean) || [];
});



const handleOpenUserSelector = () => {
  // 如果已有选择，初始化到选择器中
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

// 处理角色选择
const handleRoleSelect = (roles: Role[]) => {
  selectedRolesForSelector.value = roles;
  form.role_ids = roles.map(role => role.id);
  showRoleSelector.value = false;
};

// 打开角色选择器时初始化
const initRoleSelector = () => {
  selectedRolesForSelector.value = form.role_ids?.map((id: number) => {
    const role = roleOptions.value.find(r => r.value === id);
    return {
      id: id,
      name: role?.label || '',
      code: role?.code || ''
    } as Role;
  }) || [];
};

const importing = ref(false);

// 处理头像上传
const handleAvatarUpload = async (e: Event) => {
  const target = e.target as HTMLInputElement;
  const file = target.files?.[0];
  if (!file) return;

  // 验证文件类型
  if (!['image/jpeg', 'image/png', 'image/jpg'].includes(file.type)) {
    message.error('仅支持 JPG 或 PNG 格式');
    return;
  }

  // 验证文件大小 (1MB)
  if (file.size > 1024 * 1024) {
    message.error('图片大小不能超过 1MB');
    return;
  }

  avatarUploading.value = true;
  const uploadData = new FormData();
  uploadData.append('file', file);

  try {
    const res = await userStore.uploadAvatar(uploadData);
    // res 是 ApiResponse<UploadFilePath> 结构，实际数据在 res.data 中
    if (res && res.data && res.data.file_url) {
      form.avatar = res.data.file_url;
      message.success('头像上传成功');
    } else {
      message.error('上传失败，请重试');
    }
  } catch (error) {
    console.error('Avatar upload failed:', error);
    message.error('头像上传失败');
  } finally {
    avatarUploading.value = false;
    // 清空 input 值，允许重复选择同一文件
    if (avatarInputRef.value) {
      avatarInputRef.value.value = '';
    }
  }
};

const handleDownloadTemplate = async () => {
  try {
    const res = await userStore.downloadTemplateUser();
    if (res) {
      const blob = new Blob([res as any], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = '用户导入模板.xlsx';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      message.success('模板下载成功');
    }
  } catch (error) {
    console.error('Download template failed:', error);
    message.error('模板下载失败');
  }
};

const handleImportSubmit = async (file: File) => {
  importing.value = true;
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const res = await userStore.importUser(formData);
    if (res?.code === 200 || res?.code === 0) {
      // 显示返回数据中的 data
      const importData = res?.data;
      if (importData) {
        // 将 data 转换为字符串，保留换行符
        const dataStr = typeof importData === 'string' 
          ? importData 
          : JSON.stringify(importData, null, 2);
        dialog.confirm(dataStr, '导入成功', { confirmText: '确定', cancelText: '取消' }).then(() => {
          showImportDialog.value = false;
          importDialogRef.value?.clearFile();
          fetchUsers();
        });
      } else {
        message.success('导入成功');
        showImportDialog.value = false;
        importDialogRef.value?.clearFile();
        fetchUsers();
      }
    } else {
      // 显示详细的错误信息
      const errorMsg = res?.msg || '导入失败';
      importDialogRef.value?.setError(errorMsg);
    }
  } catch (error: any) {
    console.error('Import failed:', error);
    // 显示详细的错误信息
    const errorMsg = error?.response?.data?.msg || error?.message || '导入失败，请检查文件格式或网络连接';
    importDialogRef.value?.setError(errorMsg);
  } finally {
    importing.value = false;
  }
};

const defaultForm: UserForm = {
  username: '',
  name: '',
  password: '',
  email: '',
  mobile: '',
  gender: '2',
  avatar: '',
  is_superuser: false,
  status: '0',
  role_ids: [],
  position_ids: [],
  dept_id: undefined,
  description: ''
};

const form = reactive<UserForm>({ ...defaultForm });

// Computed
const isAllSelected = computed(() => {
  // 排除超级管理员后判断是否全选
  const selectableUsers = users.value.filter(u => !u.is_superuser);
  return selectableUsers.length > 0 && selectableUsers.every(u => selectedIds.value.includes(u.id!));
});

const dialogTitle = computed(() => {
  if (dialogType.value === 'detail') return '用户详情';
  if (dialogType.value === 'edit') return '编辑用户';
  return '新增用户';
});

const isEdit = computed(() => dialogType.value === 'edit');

// Methods
const fetchUsers = async () => {
  loading.value = true;
  try {
    // 获取所有数据用于前端过滤
    const params: any = {
      page_no: 1,
      page_size: 10000,
    };
    if (queryParams.username) params.username = queryParams.username;
    if (queryParams.name) params.name = queryParams.name;
    if (queryParams.status) params.status = queryParams.status;
    if (queryParams.dept_id) params.dept_id = queryParams.dept_id;

    const res = await userStore.getUserList(params);
    let filteredData: UserInfo[] = [];
    if (res?.data?.items) {
      filteredData = res.data.items;
    }

    // 前端过滤 - 创建时间
    if (queryParams.start_time) {
      const startDate = new Date(queryParams.start_time).getTime();
      filteredData = filteredData.filter(user => {
        if (!user.created_time) return false;
        return new Date(user.created_time).getTime() >= startDate;
      });
    }
    if (queryParams.end_time) {
      const endDate = new Date(queryParams.end_time).getTime();
      filteredData = filteredData.filter(user => {
        if (!user.created_time) return false;
        return new Date(user.created_time).getTime() <= endDate;
      });
    }

    // 前端过滤 - 创建人
    if (queryParams.created_id) {
      filteredData = filteredData.filter(user => {
        return user.created_by?.id === queryParams.created_id;
      });
    }

    total.value = filteredData.length;

    // 分页
    const start = (currentPage.value - 1) * pageSize.value;
    const end = start + pageSize.value;
    users.value = filteredData.slice(start, end);
  } catch (error) {
    console.error('Failed to fetch users:', error);
  } finally {
    loading.value = false;
  }
};

const fetchDeptTree = async () => {
  try {
    const res = await api.dept.listDept({});
    if (res?.data) {
      const flattenDeptTree = (depts: any[], prefix = ''): any[] => {
        let result: any[] = [];
        depts.forEach(d => {
          result.push({
            id: d.id,
            name: prefix + d.name
          });
          if (d.children && d.children.length > 0) {
            result = result.concat(flattenDeptTree(d.children, prefix + '　'));
          }
        });
        return result;
      };
      deptTree.value = flattenDeptTree(res.data || []);
    }
  } catch (error) {
    console.error('Failed to fetch dept tree:', error);
  }
};

const fetchRoles = async () => {
  try {
    const res = await api.role.listRole({ page_no: 1, page_size: 9999 });
    if (res?.data?.items) {
      roleOptions.value = res.data.items
        .filter((item: RoleTable) => item.id !== undefined && item.name !== undefined)
        .map((item: RoleTable) => ({
          value: item.id as number,
          label: item.name as string,
          code: item.code as string,
          disabled: item.status === '1'
        }))
        .filter((opt: any) => !opt.disabled);
    } else {
      roleOptions.value = [];
    }
  } catch (error) {
    console.error('Failed to fetch roles:', error);
    roleOptions.value = [];
  }
};

const fetchPositions = async () => {
  try {
    const res = await api.position.listPosition({ page_no: 1, page_size: 9999 });
    if (res?.data?.items) {
      positionOptions.value = res.data.items
        .filter((item: any) => item.id !== undefined && item.name !== undefined)
        .map((item: any) => ({
          value: item.id as number,
          label: item.name as string,
          disabled: item.status === '1'
        }))
        .filter((opt: any) => !opt.disabled);
    } else {
      positionOptions.value = [];
    }
  } catch (error) {
    console.error('Failed to fetch positions:', error);
    positionOptions.value = [];
  }
};

const handleSearch = () => {
  currentPage.value = 1;
  fetchUsers();
};

const handleReset = () => {
  queryParams.username = '';
  queryParams.name = '';
  queryParams.status = '';
  queryParams.dept_id = '';
  queryParams.start_time = '';
  queryParams.end_time = '';
  queryParams.created_id = undefined;
  createdByName.value = '';
  handleSearch();
};

const handleRefresh = () => {
  fetchUsers();
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
      allData = users.value.filter(u => selectedIds.value.includes(u.id!));
    } else if (options.range === 'current') {
      allData = [...users.value];
    } else {
      const queryParamsExport: any = {
        page_no: 1,
        page_size: 10000,
      };
      if (queryParams.username) queryParamsExport.username = queryParams.username;
      if (queryParams.name) queryParamsExport.name = queryParams.name;
      if (queryParams.status) queryParamsExport.status = queryParams.status;
      if (queryParams.dept_id) queryParamsExport.dept_id = queryParams.dept_id;
      if (queryParams.start_time) queryParamsExport.start_time = queryParams.start_time;
      if (queryParams.end_time) queryParamsExport.end_time = queryParams.end_time;
      if (queryParams.created_id) queryParamsExport.created_id = queryParams.created_id;
      
      const res = await userStore.getUserList(queryParamsExport);
      const resData = res as any;
      if (resData?.items) {
        allData = resData.items;
      } else if (resData?.data?.items) {
        allData = resData.data.items;
      }
    }
    
    const headers = selectedFields.map((f: ExportField) => f.label);
    const keys = selectedFieldKeys;
    const timeFields = ['created_time', 'updated_time', 'created_at', 'updated_at', 'login_time', 'logout_time'];
    
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
      link.download = `用户列表_${new Date().toISOString().slice(0, 10)}.csv`;
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
        XLSX.utils.book_append_sheet(wb, ws, '用户列表');
        XLSX.writeFile(wb, `用户列表_${new Date().toISOString().slice(0, 10)}.xlsx`);
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
  fetchUsers();
};

const handlePageSizeChange = () => {
  currentPage.value = 1;
  fetchUsers();
};

const toggleAllSelection = (e: Event) => {
  const checked = (e.target as HTMLInputElement).checked;
  if (checked) {
    // 全选时排除超级管理员
    selectedIds.value = users.value.map(u => u.id!).filter(id => id !== undefined && !users.value.find(u => u.id === id)?.is_superuser);
  } else {
    selectedIds.value = [];
  }
};

const handleAdd = () => {
  dialogType.value = 'create';
  Object.assign(form, defaultForm);
  form.role_ids = [];
  form.position_ids = [];
  fetchDeptTree();
  fetchRoles();
  fetchPositions();
  dialogVisible.value = true;
};

const handleEdit = async (user: UserInfo) => {
  if (user.is_superuser) {
    message.warning('超级管理员不可编辑');
    return;
  }
  dialogType.value = 'edit';
  await fetchDeptTree();
  await fetchRoles();
  await fetchPositions();
  
  if (user.id) {
    try {
      const detail = await userStore.getUserDetail(user.id);
      const detailData = detail?.data;
      if (detailData) {
        Object.assign(form, {
          ...defaultForm,
          ...detailData,
          gender: detailData.gender ? String(detailData.gender) : defaultForm.gender,
          password: '',
          role_ids: (detailData.roles || []).map((item: any) => item.id),
          position_ids: (detailData.positions || []).map((item: any) => item.id)
        });
      }
    } catch (error) {
      console.error('Failed to fetch user detail:', error);
    }
  }
  dialogVisible.value = true;
};

const handleView = async (user: UserInfo) => {
  dialogType.value = 'detail';
  if (user.id) {
    try {
      const detail = await userStore.getUserDetail(user.id);
      detailData.value = detail?.data || {};
    } catch (error) {
      console.error('Failed to fetch user detail:', error);
    }
  }
  dialogVisible.value = true;
};

const closeDialog = () => {
  dialogVisible.value = false;
  Object.assign(form, defaultForm);
  form.role_ids = [];
  form.position_ids = [];
};

const submitForm = async () => {
  if (!form.username || !form.name) {
    message.warning('请填写必填项');
    return;
  }

  if (form.email && !/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(form.email)) {
    message.warning('请输入有效的邮箱地址');
    return;
  }

  if (form.mobile && !/^1[3-9]\d{9}$/.test(form.mobile)) {
    message.warning('请输入有效的手机号码');
    return;
  }
  
  if (!isEdit.value && !form.password) {
    message.warning('请输入密码');
    return;
  }
  
  submitting.value = true;
  const payload: UserForm = {
    ...form,
    gender: form.gender ? String(form.gender) : form.gender,
    mobile: form.mobile && form.mobile.trim() ? form.mobile : null,
    email: form.email && form.email.trim() ? form.email : null
  };
  
  try {
    if (isEdit.value) { 
      if (form.id) {
        await userStore.updateUser(form.id, payload);
      }
    } else {
      await userStore.createUser(payload);
    }
    closeDialog();
    fetchUsers();
    message.success('操作成功');
  } catch (error: any) {
    console.error('Operation failed:', error);
    const msg = error.data?.msg || error.message || '操作失败，请重试';
    message.error(msg);
  } finally {
    submitting.value = false;
  }
};

const handleDelete = async (user: UserInfo) => {
  if (user.is_superuser) {
    message.warning('超级管理员不可删除');
    return;
  }
  try {
    await dialog.confirm(`确定要删除用户 ${user.name || user.username} 吗？`)
    if (user.id) {
      await userStore.deleteUser([user.id]);
      fetchUsers();
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

  // 检查是否包含超级管理员
  const hasSuperUser = selectedIds.value.some(id => users.value.find(u => u.id === id)?.is_superuser);
  if (hasSuperUser) {
    message.warning('超级管理员不可删除');
    return;
  }

  try {
    await dialog.confirm(`确定要删除选中的 ${selectedIds.value.length} 个用户吗？`)
    await userStore.deleteUser(selectedIds.value);
    selectedIds.value = [];
    fetchUsers();
    message.success('批量删除成功');
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error('Batch delete failed:', error);
    message.error('批量删除失败');
  }
};

const handleBatchStatus = async (status: string) => {
  if (selectedIds.value.length === 0) return;

  // 检查是否包含超级管理员
  const hasSuperUser = selectedIds.value.some(id => users.value.find(u => u.id === id)?.is_superuser);
  if (hasSuperUser) {
    message.warning('超级管理员不可操作');
    return;
  }

  try {
    const statusText = status === '0' ? '启用' : '停用';
    await dialog.confirm(`确定要${statusText}选中的 ${selectedIds.value.length} 个用户吗？`)
    await userStore.batchUser({ ids: selectedIds.value, status });
    selectedIds.value = [];
    fetchUsers();
    message.success(`批量${statusText}成功`);
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error('Batch status change failed:', error);
    message.error('操作失败');
  }
};

const handleResetPassword = async (user: UserInfo) => {
  try {
    const newPassword = prompt(`请输入用户 ${user.username} 的新密码（至少6位）`);
    if (!newPassword || newPassword.length < 6) {
      message.warning('密码至少需要6位字符');
      return;
    }
    await userStore.resetUserPassword({ id: user.id!, password: newPassword });
    message.success('密码重置成功');
  } catch (error) {
    console.error('Reset password failed:', error);
    message.error('密码重置失败');
  }
};

const formatDate = (dateStr?: string) => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleString();
};

const getGenderText = (gender?: string) => {
  if (gender === '0') return '男';
  if (gender === '1') return '女';
  return '未知';
};

const getGenderClass = (gender?: string) => {
  if (gender === '0') return 'bg-emerald-50 text-emerald-700 border border-emerald-200';
  if (gender === '1') return 'bg-pink-50 text-pink-700 border border-pink-200';
  return 'bg-slate-100 text-slate-600 border border-slate-200';
};

onMounted(() => {
  fetchUsers();
  fetchDeptTree();
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
