<template>
  <div class="min-h-screen bg-slate-50 p-8 overflow-y-auto">
    <div class="max-w-7xl mx-auto">
      <!-- 顶部导航栏 -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">公告管理</h1>
          <p class="mt-1 text-sm text-slate-500">维护系统的公告信息。</p>
        </div>
        <div class="flex gap-3">
          <button
            @click="handleCreate"
            class="px-6 py-3 bg-slate-900 text-white rounded-xl font-bold hover:bg-slate-800 shadow-lg flex items-center gap-2 transition-transform active:scale-95"
          >
            <PlusIcon :size="20" /> 新增公告
          </button>
        </div>
      </div>

      <!-- Search & Filter Card -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 mb-6 overflow-hidden">
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-5">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">标题</label>
              <div class="relative">
                <input
                  v-model="queryParams.notice_title"
                  type="text"
                  placeholder="请输入标题"
                  class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                  @keyup.enter="handleSearch"
                />
                <TypeIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">公告类型</label>
              <select
                v-model="queryParams.notice_type"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all appearance-none cursor-pointer"
              >
                <option value="">全部</option>
                <option value="1">通知</option>
                <option value="2">公告</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">状态</label>
              <select
                v-model="queryParams.status"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all appearance-none cursor-pointer"
              >
                <option value="">全部</option>
                <option value="1">正常</option>
                <option value="0">停用</option>
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

          <div v-if="isExpand" class="grid grid-cols-1 md:grid-cols-4 gap-5 mt-5 pt-5 border-t border-slate-100">
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

      <!-- Notice Table Card -->
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
                @click="handleBatchEnable"
                class="p-2 text-slate-700 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg transition-all"
                title="批量启用"
              >
                <PlayIcon class="w-4 h-4" />
              </button>
              <button
                @click="handleBatchDisable"
                class="p-2 text-slate-700 hover:text-amber-600 hover:bg-amber-50 rounded-lg transition-all"
                title="批量停用"
              >
                <PauseIcon class="w-4 h-4" />
              </button>
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
          <table class="w-full text-sm" style="min-width: 1200px;">
            <thead class="bg-slate-50 text-slate-600 font-medium border-b border-slate-200">
              <tr>
                <th class="px-5 py-4 w-12 text-center">
                  <input type="checkbox" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" @change="toggleAllSelection" :checked="isAllSelected" />
                </th>
                <th v-if="getColumnVisible('index')" class="px-5 py-4 text-center">序号</th>
                <th v-if="getColumnVisible('title')" class="px-5 py-4 text-center">标题</th>
                <th v-if="getColumnVisible('type')" class="px-5 py-4 text-center">公告类型</th>
                <th v-if="getColumnVisible('content')" class="px-5 py-4 text-center">内容</th>
                <th v-if="getColumnVisible('status')" class="px-5 py-4 text-center">状态</th>
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
              <tr v-else-if="notices.length === 0">
                <td :colspan="visibleColumnCount" class="px-6 py-12 text-center text-slate-400">
                  <div class="flex flex-col items-center gap-3">
                    <InboxIcon class="w-12 h-12 text-slate-300" />
                    <span>暂无数据</span>
                  </div>
                </td>
              </tr>
              <tr v-else v-for="notice in notices" :key="notice.id" class="hover:bg-slate-50/80 transition-colors group">
                <td class="px-5 py-4 text-center">
                  <input type="checkbox" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" :value="notice.id" v-model="selectedIds" />
                </td>
                <td v-if="getColumnVisible('index')" class="px-5 py-4 text-center text-slate-500">
                  {{ (currentPage - 1) * pageSize + notices.indexOf(notice) + 1 }}
                </td>
                <td v-if="getColumnVisible('title')" class="px-5 py-4 text-center">
                  <div class="max-w-[200px] truncate font-medium text-slate-900" :title="notice.notice_title">{{ notice.notice_title || '-' }}</div>
                </td>
                <td v-if="getColumnVisible('type')" class="px-5 py-4 text-center">
                  <span
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                    :class="notice.notice_type === '1' ? 'bg-blue-50 text-blue-700 border border-blue-200' : 'bg-purple-50 text-purple-700 border border-purple-200'"
                  >
                    {{ notice.notice_type === '1' ? '通知' : '公告' }}
                  </span>
                </td>
                <td v-if="getColumnVisible('content')" class="px-5 py-4 text-center">
                  <div class="max-w-[300px] truncate text-slate-600" :title="stripHtml(notice.notice_content)">{{ stripHtml(notice.notice_content) || '-' }}</div>
                </td>
                <td v-if="getColumnVisible('status')" class="px-5 py-4 text-center">
                  <span
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                    :class="notice.status === '1' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-600 border border-slate-200'"
                  >
                    {{ notice.status === '1' ? '正常' : '停用' }}
                  </span>
                </td>
                <td v-if="getColumnVisible('created_time')" class="px-5 py-4 text-center text-slate-500 whitespace-nowrap text-xs">
                  {{ formatDate(notice.created_time) }}
                </td>
                <td v-if="getColumnVisible('created_by')" class="px-5 py-4 text-center text-slate-600">{{ notice.created_by?.name || '-' }}</td>
                <td v-if="getColumnVisible('action')" class="px-5 py-4 text-center fixed-col">
                  <div class="flex items-center justify-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      @click="handleView(notice)"
                      class="p-2 text-slate-800 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all"
                      title="详情"
                    >
                      <EyeIcon class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleEdit(notice)"
                      class="p-2 text-slate-800 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all"
                      title="编辑"
                    >
                      <PencilIcon class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleDelete(notice)"
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
              :disabled="notices.length < pageSize"
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

    <!-- Export Dialog -->
    <ExportDialog
      v-model:visible="showExportDialog"
      title="导出公告"
      :fields="exportFields"
      :selected-count="selectedIds.length"
      @confirm="handleExportConfirm"
    />
    
    <!-- View Modal (Readonly) -->
    <div v-if="viewDialogVisible" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-3xl max-h-[90vh] overflow-hidden flex flex-col">
        <div class="px-6 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
          <h2 class="text-xl font-bold text-slate-900">公告详情</h2>
          <button @click="closeViewDialog" class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all">
            <XIcon class="w-5 h-5" />
          </button>
        </div>

        <div class="flex-1 overflow-y-auto p-6">
          <div class="space-y-5">
            <div class="grid grid-cols-2 gap-5">
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">标题</div>
                <div class="font-medium text-slate-900">{{ viewData.notice_title || '-' }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">公告类型</div>
                <span
                  class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                  :class="viewData.notice_type === '1' ? 'bg-blue-50 text-blue-700 border border-blue-200' : 'bg-purple-50 text-purple-700 border border-purple-200'"
                >
                  {{ viewData.notice_type === '1' ? '通知' : '公告' }}
                </span>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-5">
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">状态</div>
                <span
                  class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                  :class="viewData.status === '1' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-600 border border-slate-200'"
                >
                  {{ viewData.status === '1' ? '正常' : '停用' }}
                </span>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">创建人</div>
                <div class="font-medium text-slate-900">{{ viewData.created_by?.name || '-' }}</div>
              </div>
            </div>

            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">描述</div>
              <div class="font-medium text-slate-900">{{ (viewData as any).description || '-' }}</div>
            </div>

            <div class="p-4 bg-slate-50 rounded-xl">
              <div class="text-xs text-slate-500 mb-2 uppercase tracking-wide">内容</div>
              <div class="bg-white border border-slate-200 rounded-xl p-4 prose prose-sm max-w-none" v-html="viewData.notice_content || '<p class=\'text-slate-400\'>无内容</p>'"></div>
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
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col">
        <div class="px-6 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
          <h2 class="text-xl font-bold text-slate-900">{{ isEdit ? '编辑公告' : '新增公告' }}</h2>
          <button @click="closeDialog" class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all">
            <XIcon class="w-5 h-5" />
          </button>
        </div>
        
        <div class="flex-1 overflow-y-auto p-6">
          <div class="space-y-5">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">标题 <span class="text-red-500">*</span></label>
              <input
                v-model="formData.notice_title"
                type="text"
                placeholder="请输入标题"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
              />
            </div>

            <div class="grid grid-cols-2 gap-5">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">公告类型 <span class="text-red-500">*</span></label>
                <select
                  v-model="formData.notice_type"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all appearance-none cursor-pointer"
                >
                  <option value="1">通知</option>
                  <option value="2">公告</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">状态 <span class="text-red-500">*</span></label>
                <select
                  v-model="formData.status"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all appearance-none cursor-pointer"
                >
                  <option value="1">正常</option>
                  <option value="0">停用</option>
                </select>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">描述</label>
              <textarea
                v-model="formData.description"
                rows="3"
                placeholder="请输入描述"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all resize-none"
              ></textarea>
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">内容 <span class="text-red-500">*</span></label>
              <RichEditor
                v-model="formData.notice_content"
                height="300px"
                placeholder="请输入公告内容..."
              />
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
import UserSelector from '@/components/common/UserSelector.vue';
import RichEditor from '@/components/common/RichEditor.vue';
import type { ExportOptions } from '@/components/common/ExportDialog.vue';
import type { User } from '@/types/user';
import { api } from '@/services/api';
import type { NoticeTable, NoticePageQuery, NoticeForm } from '@/services/fastApi/module_system/notice';
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
  TypeIcon,
  UserIcon,
  EyeIcon,
  PlayIcon,
  PauseIcon
} from 'lucide-vue-next';

const loading = ref(false);
const notices = ref<NoticeTable[]>([]);
const total = ref(0);
const currentPage = ref(1);
const pageSize = ref(10);
const dialogVisible = ref(false);
const viewDialogVisible = ref(false);
const isEdit = ref(false);
const selectedIds = ref<number[]>([]);
const editId = ref<number | null>(null);
const viewData = ref<NoticeTable>({});

const queryParams = reactive<NoticePageQuery>({
  page_no: 1,
  page_size: 10,
  notice_type: '',
  notice_title: '',
  status: '',
  created_id: undefined
});

const startTime = ref('');
const endTime = ref('');
const createdByName = ref('');
const showUserSelector = ref(false);
const selectedUserForSelector = ref<User[]>([]);

const formData = reactive<NoticeForm & { description?: string }>({
  notice_title: '',
  notice_type: '1',
  notice_content: '',
  status: '1',
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
  { key: 'title', label: '标题', checked: true },
  { key: 'type', label: '公告类型', checked: true },
  { key: 'content', label: '内容', checked: true },
  { key: 'status', label: '状态', checked: true },
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
  { key: 'title', label: '标题', visible: true },
  { key: 'type', label: '公告类型', visible: true },
  { key: 'content', label: '内容', visible: true },
  { key: 'status', label: '状态', visible: true },
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
  return notices.value.length > 0 && notices.value.every(n => selectedIds.value.includes(n.id!));
});

const toggleAllSelection = (e: Event) => {
  const checked = (e.target as HTMLInputElement).checked;
  if (checked) {
    selectedIds.value = notices.value.map(n => n.id!).filter(id => id !== undefined);
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

const formatDate = (dateStr?: string) => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleString();
};

// 去除HTML标签，返回纯文本
const stripHtml = (html?: string) => {
  if (!html) return '';
  const tmp = document.createElement('div');
  tmp.innerHTML = html;
  return tmp.textContent || tmp.innerText || '';
};

const fetchNotices = async () => {
  loading.value = true;
  try {
    const params: NoticePageQuery = {
      page_no: currentPage.value,
      page_size: pageSize.value,
    };

    if (queryParams.notice_type) params.notice_type = queryParams.notice_type;
    if (queryParams.notice_title) params.notice_title = queryParams.notice_title;
    if (queryParams.status) params.status = queryParams.status;
    if (queryParams.created_id) params.created_id = queryParams.created_id;

    if (startTime.value || endTime.value) {
      params.created_time = [];
      if (startTime.value) {
        params.created_time.push(startTime.value + ' 00:00:00');
      }
      if (endTime.value) {
        params.created_time.push(endTime.value + ' 23:59:59');
      }
    }

    const res = await api.notice.listNotice(params);
    if (res?.data) {
      notices.value = res.data.items || [];
      total.value = res.data.total || 0;
    }
  } catch (error) {
    console.error('Failed to fetch notices:', error);
    message.error('获取公告列表失败');
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  currentPage.value = 1;
  fetchNotices();
};

const handleReset = () => {
  queryParams.notice_type = '';
  queryParams.notice_title = '';
  queryParams.status = '';
  queryParams.created_id = undefined;
  startTime.value = '';
  endTime.value = '';
  createdByName.value = '';
  currentPage.value = 1;
  fetchNotices();
};

const handleRefresh = () => {
  fetchNotices();
  message.success('刷新成功');
};

const handleCreate = () => {
  isEdit.value = false;
  editId.value = null;
  formData.notice_title = '';
  formData.notice_type = '1';
  formData.notice_content = '';
  formData.status = '1';
  formData.description = '';
  dialogVisible.value = true;
};

const handleEdit = (notice: NoticeTable) => {
  isEdit.value = true;
  editId.value = notice.id || null;
  formData.notice_title = notice.notice_title || '';
  formData.notice_type = notice.notice_type || '1';
  formData.notice_content = notice.notice_content || '';
  formData.status = notice.status || '1';
  formData.description = (notice as any).description || '';
  dialogVisible.value = true;
};

const handleView = (notice: NoticeTable) => {
  viewData.value = { ...notice };
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
  if (!formData.notice_title?.trim()) {
    message.warning('请输入标题');
    return;
  }
  if (!formData.notice_content?.trim()) {
    message.warning('请输入内容');
    return;
  }

  try {
    if (isEdit.value && editId.value) {
      await api.notice.updateNotice(editId.value, formData);
      message.success('更新成功');
    } else {
      await api.notice.createNotice(formData);
      message.success('创建成功');
    }
    closeDialog();
    fetchNotices();
  } catch (error) {
    console.error('Submit failed:', error);
    message.error(isEdit.value ? '更新失败' : '创建失败');
  }
};

const handleDelete = async (notice: NoticeTable) => {
  try {
    await dialog.confirm(`确定要删除该公告吗？`)
    if (notice.id) {
      await api.notice.deleteNotice([notice.id]);
      fetchNotices();
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
    await dialog.confirm(`确定要删除选中的 ${selectedIds.value.length} 条公告吗？`)
    await api.notice.deleteNotice(selectedIds.value);
    selectedIds.value = [];
    fetchNotices();
    message.success('批量删除成功');
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error('Batch delete failed:', error);
    message.error('批量删除失败');
  }
};

const handleBatchEnable = async () => {
  if (selectedIds.value.length === 0) return;

  try {
    await dialog.confirm(`确定要启用选中的 ${selectedIds.value.length} 条公告吗？`)
    // 批量更新状态为启用
    for (const id of selectedIds.value) {
      const notice = notices.value.find(n => n.id === id);
      if (notice) {
        await api.notice.updateNotice(id, {
          ...notice,
          status: '1'
        } as NoticeForm);
      }
    }
    selectedIds.value = [];
    fetchNotices();
    message.success('批量启用成功');
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error('Batch enable failed:', error);
    message.error('批量启用失败');
  }
};

const handleBatchDisable = async () => {
  if (selectedIds.value.length === 0) return;

  try {
    await dialog.confirm(`确定要停用选中的 ${selectedIds.value.length} 条公告吗？`)
    // 批量更新状态为停用
    for (const id of selectedIds.value) {
      const notice = notices.value.find(n => n.id === id);
      if (notice) {
        await api.notice.updateNotice(id, {
          ...notice,
          status: '0'
        } as NoticeForm);
      }
    }
    selectedIds.value = [];
    fetchNotices();
    message.success('批量停用成功');
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error('Batch disable failed:', error);
    message.error('批量停用失败');
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
    
    let allData: NoticeTable[] = [];
    
    if (options.range === 'selected' && selectedIds.value.length > 0) {
      allData = notices.value.filter(n => selectedIds.value.includes(n.id!));
    } else if (options.range === 'current') {
      allData = [...notices.value];
    } else {
      const exportParams: NoticePageQuery = {
        page_no: 1,
        page_size: 10000,
      };
      if (queryParams.notice_type) exportParams.notice_type = queryParams.notice_type;
      if (queryParams.notice_title) exportParams.notice_title = queryParams.notice_title;
      if (queryParams.status) exportParams.status = queryParams.status;

      const res = await api.notice.listNotice(exportParams);
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
        ...allData.map((row: NoticeTable) =>
          keys.map((key: string) => {
            let value = (row as any)[key];
            if (key === 'type') {
              value = value === '1' ? '通知' : '公告';
            } else if (key === 'status') {
              value = value === '1' ? '正常' : '停用';
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
      link.download = `公告列表_${new Date().toISOString().slice(0, 10)}.csv`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } else {
      try {
        const XLSX = await import('xlsx');
        const exportData = allData.map((row: NoticeTable) => {
          const obj: any = {};
          keys.forEach((key: string, index: number) => {
            let value = (row as any)[key];
            if (key === 'type') {
              value = value === '1' ? '通知' : '公告';
            } else if (key === 'status') {
              value = value === '1' ? '正常' : '停用';
            } else if (key === 'created_by' || key === 'updated_by') {
              value = value?.name || '';
            }
            obj[headers[index]] = value;
          });
          return obj;
        });
        
        const ws = XLSX.utils.json_to_sheet(exportData);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, '公告列表');
        XLSX.writeFile(wb, `公告列表_${new Date().toISOString().slice(0, 10)}.xlsx`);
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
  fetchNotices();
};

const handlePageSizeChange = () => {
  currentPage.value = 1;
  fetchNotices();
};

onMounted(() => {
  fetchNotices();
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
