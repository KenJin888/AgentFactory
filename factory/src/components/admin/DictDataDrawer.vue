<template>
  <div v-if="modelValue" class="fixed inset-0 z-50 flex justify-end">
    <!-- 遮罩层 -->
    <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="handleClose"></div>
    
    <!-- 抽屉内容 -->
    <div class="relative w-full max-w-5xl h-full bg-white shadow-2xl flex flex-col animate-in slide-in-from-right duration-300">
      <!-- Header -->
      <div class="px-6 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
        <div>
          <h2 class="text-xl font-bold text-slate-900 flex items-center gap-2">
            <FileTextIcon class="w-5 h-5 text-blue-600" />
            【{{ props.dictLabel }}】字典数据
          </h2>
          <p class="text-sm text-slate-500 mt-1">字典类型: {{ props.dictType }}</p>
        </div>
        <button @click="handleClose" class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all">
          <XIcon class="w-5 h-5" />
        </button>
      </div>

      <!-- Content -->
      <div class="flex-1 overflow-y-auto p-6">
        <!-- Search & Filter -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 mb-6 overflow-hidden">
          <div class="p-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <!-- 字典标签 -->
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">字典标签</label>
                <div class="relative">
                  <input
                    v-model="queryParams.dict_label"
                    type="text"
                    placeholder="请输入字典标签"
                    class="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                    @keyup.enter="handleSearch"
                  />
                  <TagIcon class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                </div>
              </div>
              <!-- 状态 -->
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">状态</label>
                <select
                  v-model="queryParams.status"
                  class="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all appearance-none cursor-pointer"
                >
                  <option value="">全部</option>
                  <option value="0">启用</option>
                  <option value="1">停用</option>
                </select>
              </div>
              <!-- 操作按钮 -->
              <div class="flex items-end">
                <div class="flex items-center gap-2">
                  <button
                    @click="handleSearch"
                    class="bg-slate-900 text-white px-4 py-2 rounded-xl hover:bg-slate-800 transition-all shadow-sm flex items-center gap-2"
                  >
                    <SearchIcon class="w-4 h-4" />
                    查询
                  </button>
                  <button
                    @click="handleReset"
                    class="bg-white text-slate-600 border border-slate-200 px-4 py-2 rounded-xl hover:bg-slate-50 transition-all"
                  >
                    重置
                  </button>
                  <button
                    @click="isExpand = !isExpand"
                    class="px-3 py-2 text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-xl transition-all flex items-center justify-center gap-1"
                    :title="isExpand ? '收起筛选' : '展开筛选'"
                  >
                    <ChevronUpIcon v-if="isExpand" class="w-4 h-4" />
                    <ChevronDownIcon v-else class="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>

            <!-- 展开的搜索条件 -->
            <div v-if="isExpand" class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 pt-4 border-t border-slate-100">
              <!-- 创建时间 -->
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-slate-700 mb-2">创建时间</label>
                <div class="flex items-center gap-3">
                  <input
                    v-model="queryParams.start_time"
                    type="date"
                    class="flex-1 px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                  />
                  <span class="text-slate-400">至</span>
                  <input
                    v-model="queryParams.end_time"
                    type="date"
                    class="flex-1 px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Toolbar -->
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-3">
            <button
              @click="handleAdd"
              class="px-4 py-2 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 shadow-sm flex items-center gap-2 transition-transform active:scale-95"
            >
              <PlusIcon class="w-4 h-4" /> 新增
            </button>
            <div v-if="selectedIds.length > 0" class="flex items-center gap-1 pl-3 border-l border-slate-200">
              <span class="text-sm text-slate-500">已选 {{ selectedIds.length }} 项</span>
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
              class="p-2 text-slate-600 hover:bg-slate-100 rounded-xl transition-all"
              title="导出"
            >
              <DownloadIcon class="w-5 h-5" />
            </button>
            <button
              @click="handleRefresh"
              class="p-2 text-slate-600 hover:bg-slate-100 rounded-xl transition-all"
              title="刷新"
            >
              <RefreshCwIcon class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- Table -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-sm whitespace-nowrap">
              <thead class="bg-slate-50 text-slate-600 font-medium border-b border-slate-200">
                <tr>
                  <th class="px-4 py-3 w-12 min-w-[48px] text-center">
                    <input type="checkbox" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" @change="toggleAllSelection" :checked="isAllSelected" />
                  </th>
                  <th class="px-4 py-3 min-w-[60px] text-center">序号</th>
                  <th class="px-4 py-3 min-w-[120px] text-center">标签</th>
                  <th class="px-4 py-3 min-w-[100px] text-center">类型</th>
                  <th class="px-4 py-3 min-w-[80px] text-center">值</th>
                  <th class="px-4 py-3 min-w-[60px] text-center">排序</th>
                  <th class="px-4 py-3 min-w-[100px] text-center">样式</th>
                  <th class="px-4 py-3 min-w-[100px] text-center">列表样式</th>
                  <th class="px-4 py-3 min-w-[70px] text-center">默认</th>
                  <th class="px-4 py-3 min-w-[80px] text-center">状态</th>
                  <th class="px-4 py-3 min-w-[120px] text-center">描述</th>
                  <th class="px-4 py-3 min-w-[160px] text-center">创建时间</th>
                  <th class="px-4 py-3 min-w-[160px] text-center">更新时间</th>
                  <th class="px-4 py-3 min-w-[100px] text-center fixed-col">操作</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-if="loading" class="animate-pulse">
                  <td colspan="13" class="px-6 py-12 text-center text-slate-400">
                    <div class="flex flex-col items-center gap-3">
                      <Loader2Icon class="w-8 h-8 animate-spin text-blue-500" />
                      <span>加载中...</span>
                    </div>
                  </td>
                </tr>
                <tr v-else-if="dataList.length === 0">
                  <td colspan="13" class="px-6 py-12 text-center text-slate-400">
                    <div class="flex flex-col items-center gap-3">
                      <InboxIcon class="w-12 h-12 text-slate-300" />
                      <span>暂无数据</span>
                    </div>
                  </td>
                </tr>
                <tr v-else v-for="item in dataList" :key="item.id" class="hover:bg-slate-50/80 transition-colors group">
                  <td class="px-4 py-3 text-center">
                    <input type="checkbox" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" :value="item.id" v-model="selectedIds" />
                  </td>
                  <td class="px-4 py-3 text-center text-slate-500">
                    {{ (currentPage - 1) * pageSize + dataList.indexOf(item) + 1 }}
                  </td>
                  <td class="px-4 py-3 text-center">
                    <div class="font-medium text-slate-900">{{ item.dict_label }}</div>
                  </td>
                  <td class="px-4 py-3 text-center">
                    <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-50 text-blue-700 border border-blue-100">
                      {{ item.dict_type }}
                    </span>
                  </td>
                  <td class="px-4 py-3 text-center text-slate-600">{{ item.dict_value }}</td>
                  <td class="px-4 py-3 text-center text-slate-500">{{ item.dict_sort }}</td>
                  <td class="px-4 py-3 text-center">
                    <span v-if="item.css_class" class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium" :style="{ backgroundColor: item.css_class, color: '#fff' }">
                      {{ item.css_class }}
                    </span>
                    <span v-else class="text-slate-400">-</span>
                  </td>
                  <td class="px-4 py-3 text-center">
                    <span v-if="item.list_class" class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium" :class="getListClassStyle(item.list_class)">
                      {{ item.list_class }}
                    </span>
                    <span v-else class="text-slate-400">-</span>
                  </td>
                  <td class="px-4 py-3 text-center">
                    <span v-if="item.is_default" class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
                      是
                    </span>
                    <span v-else class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-600 border border-slate-200">
                      否
                    </span>
                  </td>
                  <td class="px-4 py-3 text-center">
                    <span
                      class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                      :class="item.status === '0' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-red-50 text-red-700 border border-red-200'"
                    >
                      <span class="w-1.5 h-1.5 rounded-full mr-1" :class="item.status === '0' ? 'bg-emerald-500' : 'bg-red-500'"></span>
                      {{ item.status === '0' ? '启用' : '停用' }}
                    </span>
                  </td>
                  <td class="px-4 py-3 text-center text-slate-600 max-w-[150px] truncate">{{ item.description || '-' }}</td>
                  <td class="px-4 py-3 text-center text-slate-500 whitespace-nowrap text-xs">{{ formatDate(item.created_time) }}</td>
                  <td class="px-4 py-3 text-center text-slate-500 whitespace-nowrap text-xs">{{ formatDate(item.updated_time) }}</td>
                  <td class="px-4 py-3 text-center fixed-col">
                    <div class="flex items-center justify-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button
                        @click="handleView(item)"
                        class="p-1.5 text-slate-800 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-all"
                        title="详情"
                      >
                        <EyeIcon class="w-4 h-4" />
                      </button>
                      <button
                        @click="handleEdit(item)"
                        class="p-1.5 text-slate-800 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all"
                        title="编辑"
                      >
                        <EditIcon class="w-4 h-4" />
                      </button>
                      <button
                        @click="handleDelete(item)"
                        class="p-1.5 text-slate-800 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all"
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
                :disabled="dataList.length < pageSize"
                class="px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-sm disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-50 hover:border-slate-300 transition-all"
              >
                下一页
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Export Dialog -->
    <ExportDialog
      v-model:visible="showExportDialog"
      title="导出字典数据"
      :fields="exportFields"
      :selected-count="selectedIds.length"
      @confirm="handleExportConfirm"
    />

    <!-- Add/Edit/Detail Modal -->
    <div v-if="dialogVisible" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-[60] flex items-center justify-center p-4">
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
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">数据标签</div>
                <div class="font-medium text-slate-900">{{ detailData.dict_label }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">数据值</div>
                <div class="font-medium text-slate-900">{{ detailData.dict_value }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">数据类型</div>
                <div class="font-medium text-slate-900">{{ detailData.dict_type }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">排序</div>
                <div class="font-medium text-slate-900">{{ detailData.dict_sort }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">样式属性</div>
                <div class="font-medium text-slate-900">{{ detailData.css_class || '-' }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">列表样式</div>
                <div class="font-medium text-slate-900">{{ detailData.list_class || '-' }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">是否默认</div>
                <span :class="detailData.is_default ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-600'" class="px-2.5 py-1 rounded-lg text-xs font-medium">
                  {{ detailData.is_default ? '是' : '否' }}
                </span>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">状态</div>
                <span :class="detailData.status === '0' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'" class="px-2.5 py-1 rounded-lg text-xs font-medium">
                  {{ detailData.status === '0' ? '启用' : '停用' }}
                </span>
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
                <label class="block text-sm font-medium text-slate-700 mb-2">数据类型</label>
                <input
                  v-model="form.dict_type"
                  type="text"
                  disabled
                  class="w-full px-4 py-2.5 bg-slate-100 border border-slate-200 rounded-xl text-slate-500 transition-all"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">排序 <span class="text-red-500">*</span></label>
                <input
                  v-model.number="form.dict_sort"
                  type="number"
                  min="1"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">数据标签 <span class="text-red-500">*</span></label>
                <input
                  v-model="form.dict_label"
                  type="text"
                  placeholder="请输入数据标签"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">数据值 <span class="text-red-500">*</span></label>
                <input
                  v-model="form.dict_value"
                  type="text"
                  placeholder="请输入数据值"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">样式属性</label>
                <select v-model="form.css_class" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all">
                  <option value="">请选择</option>
                  <option value="#409EFF">蓝色-Primary (#409EFF)</option>
                  <option value="#67C23A">绿色-Success (#67C23A)</option>
                  <option value="#E6A23C">橙色-Warning (#E6A23C)</option>
                  <option value="#F56C6C">红色-Danger (#F56C6C)</option>
                  <option value="#909399">灰色-Info (#909399)</option>
                  <option value="#303133">深灰-文本主要 (#303133)</option>
                  <option value="#606266">灰色-文本常规 (#606266)</option>
                  <option value="#C0C4CC">浅灰-占位文本 (#C0C4CC)</option>
                  <option value="#000000">黑色 (#000000)</option>
                  <option value="#FFFFFF">白色 (#FFFFFF)</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">列表类样式</label>
                <select v-model="form.list_class" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all">
                  <option value="">请选择</option>
                  <option value="default">默认(default)</option>
                  <option value="primary">主要(primary)</option>
                  <option value="success">成功(success)</option>
                  <option value="warning">警告(warning)</option>
                  <option value="danger">危险(danger)</option>
                  <option value="info">信息(info)</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">是否默认</label>
                <div class="flex items-center gap-4 px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="form.is_default" :value="true" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
                    <span class="text-sm text-slate-700">是</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="form.is_default" :value="false" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
                    <span class="text-sm text-slate-700">否</span>
                  </label>
                </div>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">状态</label>
                <div class="flex items-center gap-4 px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="form.status" value="0" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
                    <span class="text-sm text-slate-700">启用</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="form.status" value="1" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
                    <span class="text-sm text-slate-700">停用</span>
                  </label>
                </div>
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
import { ref, reactive, onMounted, computed, watch } from 'vue';
import {
  X as XIcon,
  Plus as PlusIcon,
  Trash2 as TrashIcon,
  Edit as EditIcon,
  Eye as EyeIcon,
  Search as SearchIcon,
  RefreshCw as RefreshCwIcon,
  Loader2 as Loader2Icon,
  Inbox as InboxIcon,
  Play as PlayIcon,
  Pause as PauseIcon,
  FileText as FileTextIcon,
  Tag as TagIcon,
  Download as DownloadIcon,
  ChevronUp as ChevronUpIcon,
  ChevronDown as ChevronDownIcon
} from 'lucide-vue-next';
import ExportDialog from '@/components/common/ExportDialog.vue';
import DictAPI from '@/services/fastApi/module_system/dict';
import type { DictDataTable, DictDataForm } from '@/services/fastApi/module_system/dict';
import message from '@/components/common/message';
import { dialog } from '@/components/common/dialog';
import type { ExportOptions } from '@/components/common/ExportDialog.vue';

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  dictType: {
    type: String,
    required: true,
  },
  dictLabel: {
    type: String,
    required: true,
  },
  dictTypeId: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(['update:modelValue', 'close']);

// State
const loading = ref(false);
const submitting = ref(false);
const dataList = ref<DictDataTable[]>([]);
const total = ref(0);
const currentPage = ref(1);
const pageSize = ref(10);
const dialogVisible = ref(false);
const dialogType = ref<'create' | 'edit' | 'detail'>('create');
const selectedIds = ref<number[]>([]);
const detailData = ref<DictDataTable>({});

const queryParams = reactive({
  dict_label: '',
  status: '',
  start_time: '',
  end_time: ''
});

const isExpand = ref(false);

const showExportDialog = ref(false);

interface ExportField {
  key: string;
  label: string;
  checked: boolean;
}

const exportFields = ref<ExportField[]>([
  { key: 'dict_label', label: '标签', checked: true },
  { key: 'dict_type', label: '类型', checked: true },
  { key: 'dict_value', label: '值', checked: true },
  { key: 'dict_sort', label: '排序', checked: true },
  { key: 'css_class', label: '样式属性', checked: true },
  { key: 'list_class', label: '列表样式', checked: true },
  { key: 'is_default', label: '是否默认', checked: true },
  { key: 'status', label: '状态', checked: true },
  { key: 'description', label: '描述', checked: true },
  { key: 'created_time', label: '创建时间', checked: true },
  { key: 'updated_time', label: '更新时间', checked: true },
]);

const defaultForm: DictDataForm = {
  dict_sort: 1,
  dict_label: '',
  dict_value: '',
  dict_type: '',
  dict_type_id: undefined,
  css_class: '',
  list_class: '',
  is_default: false,
  status: '0',
  description: ''
};

const form = reactive<DictDataForm>({ ...defaultForm });

// Computed
const isAllSelected = computed(() => {
  return dataList.value.length > 0 && dataList.value.every(item => selectedIds.value.includes(item.id!));
});

const dialogTitle = computed(() => {
  if (dialogType.value === 'detail') return '字典数据详情';
  if (dialogType.value === 'edit') return '编辑字典数据';
  return '新增字典数据';
});

// Methods
const fetchDataList = async () => {
  loading.value = true;
  try {
    const params: any = {
      page_no: currentPage.value,
      page_size: pageSize.value,
      dict_type: props.dictType,
    };
    if (queryParams.dict_label) params.dict_label = queryParams.dict_label;
    if (queryParams.status) params.status = queryParams.status;
    if (queryParams.start_time) params.start_time = queryParams.start_time;
    if (queryParams.end_time) params.end_time = queryParams.end_time;

    const res = await DictAPI.listDictData(params);
    if (res?.data?.data) {
      dataList.value = res.data.data.items || [];
      total.value = res.data.data.total || 0;
    }
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};

const handleClose = () => {
  emit('update:modelValue', false);
  emit('close');
};

const handleSearch = () => {
  currentPage.value = 1;
  fetchDataList();
};

const handleReset = () => {
  queryParams.dict_label = '';
  queryParams.status = '';
  queryParams.start_time = '';
  queryParams.end_time = '';
  handleSearch();
};

const handleRefresh = () => {
  fetchDataList();
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
      allData = dataList.value.filter(d => selectedIds.value.includes(d.id!));
    } else if (options.range === 'current') {
      allData = [...dataList.value];
    } else {
      const params: any = {
        page_no: 1,
        page_size: 10000,
        dict_type: props.dictType,
      };
      if (queryParams.dict_label) params.dict_label = queryParams.dict_label;
      if (queryParams.status) params.status = queryParams.status;
      if (queryParams.start_time) params.start_time = queryParams.start_time;
      if (queryParams.end_time) params.end_time = queryParams.end_time;

      const res = await DictAPI.listDictData(params);
      if (res?.data?.data?.items) {
        allData = res.data.data.items;
      }
    }
    
    if (allData.length === 0) {
      message.warning('暂无数据可导出');
      return;
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
            // 转换布尔值和状态为中文
            if (header === '是否默认') value = value ? '是' : '否';
            if (header === '状态') value = value === '0' ? '启用' : '停用';
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
      link.download = `字典数据_${props.dictType}_${new Date().toISOString().slice(0, 10)}.csv`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } else {
      try {
        const XLSX = await import('xlsx');
        const ws = XLSX.utils.json_to_sheet(filteredData);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, '字典数据');
        XLSX.writeFile(wb, `字典数据_${props.dictType}_${new Date().toISOString().slice(0, 10)}.xlsx`);
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
  fetchDataList();
};

const handlePageSizeChange = () => {
  currentPage.value = 1;
  fetchDataList();
};

const toggleAllSelection = (e: Event) => {
  const checked = (e.target as HTMLInputElement).checked;
  if (checked) {
    selectedIds.value = dataList.value.map(item => item.id!).filter(id => id !== undefined);
  } else {
    selectedIds.value = [];
  }
};

const handleAdd = () => {
  dialogType.value = 'create';
  Object.assign(form, {
    ...defaultForm,
    dict_type: props.dictType,
    dict_type_id: props.dictTypeId,
    status: '0'
  });
  dialogVisible.value = true;
};

const handleEdit = (item: DictDataTable) => {
  dialogType.value = 'edit';
  Object.assign(form, {
    ...defaultForm,
    ...item
  });
  dialogVisible.value = true;
};

const handleView = (item: DictDataTable) => {
  dialogType.value = 'detail';
  detailData.value = { ...item };
  dialogVisible.value = true;
};

const closeDialog = () => {
  dialogVisible.value = false;
  Object.assign(form, defaultForm);
};

const submitForm = async () => {
  if (!form.dict_label || !form.dict_value) {
    message.warning('请填写必填项');
    return;
  }

  submitting.value = true;
  
  try {
    if (dialogType.value === 'edit') { 
      if (form.id) {
        await DictAPI.updateDictData(form.id, form);
      }
    } else {
      await DictAPI.createDictData(form);
    }
    closeDialog();
    fetchDataList();
    message.success('操作成功');
  } catch (error) {
    console.error(error);
  } finally {
    submitting.value = false;
  }
};

const handleDelete = async (item: DictDataTable) => {
  try {
    await dialog.confirm(`确定要删除数据 "${item.dict_label}" 吗？`)
    if (item.id) {
      await DictAPI.deleteDictData([item.id]);
      fetchDataList();
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
    await dialog.confirm(`确定要删除选中的 ${selectedIds.value.length} 个数据吗？`)
    await DictAPI.deleteDictData(selectedIds.value);
    selectedIds.value = [];
    fetchDataList();
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
    await dialog.confirm(`确定要${statusText}选中的 ${selectedIds.value.length} 个数据吗？`)
    await DictAPI.batchDictData({ ids: selectedIds.value, status });
    selectedIds.value = [];
    fetchDataList();
    message.success(`批量${statusText}成功`);
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return
    console.error(error);
  }
};

const getListClassStyle = (listClass?: string) => {
  const styles: Record<string, string> = {
    'default': 'bg-slate-100 text-slate-700 border border-slate-200',
    'primary': 'bg-blue-50 text-blue-700 border border-blue-200',
    'success': 'bg-emerald-50 text-emerald-700 border border-emerald-200',
    'warning': 'bg-amber-50 text-amber-700 border border-amber-200',
    'danger': 'bg-red-50 text-red-700 border border-red-200',
    'info': 'bg-cyan-50 text-cyan-700 border border-cyan-200',
  };
  return styles[listClass || ''] || styles['default'];
};

const formatDate = (dateStr?: string) => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleString();
};

// Watch
watch(() => props.modelValue, (val) => {
  if (val) {
    fetchDataList();
  }
});

onMounted(() => {
  if (props.modelValue) {
    fetchDataList();
  }
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
