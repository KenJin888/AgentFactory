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
             <MenuIcon class="text-blue-600" /> 菜单管理
          </h1>
        </div>
        <div class="flex gap-3">
          <button
            @click="handleAdd"
            class="px-6 py-3 bg-blue-600 text-white rounded-xl font-bold hover:bg-blue-700 shadow-lg flex items-center gap-2 transition-transform active:scale-95"
          >
              <PlusIcon :size="20" /> 新增菜单
          </button>
        </div>
      </div>

      <!-- Search & Filter Card -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 mb-6 overflow-hidden">
        <div class="p-6">
          <!-- 第一行：四个等分列 -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
            <!-- 菜单名称 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">菜单名称</label>
              <div class="relative">
                <input
                  v-model="queryParams.name"
                  type="text"
                  placeholder="请输入菜单名称"
                  class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                  @keyup.enter="handleSearch"
                />
                <MenuIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
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

      <!-- Menu Table Card -->
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
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-sm" style="min-width: 1800px;">
            <thead class="bg-slate-50 text-slate-600 font-medium border-b border-slate-200">
              <tr>
                <th class="px-5 py-4 w-12 text-center">
                  <input type="checkbox" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" @change="toggleAllSelection" :checked="isAllSelected" />
                </th>
                <th class="px-5 py-4 text-center w-16">序号</th>
                <th class="px-5 py-4 text-left min-w-[200px]">菜单名称</th>
                <th class="px-5 py-4 text-center w-20">图标</th>
                <th class="px-5 py-4 text-center w-20">状态</th>
                <th class="px-5 py-4 text-center w-20">类型</th>
                <th class="px-5 py-4 text-center w-20">排序</th>
                <th class="px-5 py-4 text-left min-w-[150px]">重定向</th>
                <th class="px-5 py-4 text-center w-24">是否缓存</th>
                <th class="px-5 py-4 text-center w-24">是否隐藏</th>
                <th class="px-5 py-4 text-center w-28">显示根路由</th>
                <th class="px-5 py-4 text-center w-24">固定路由</th>
                <th class="px-5 py-4 text-left min-w-[150px]">菜单标题</th>
                <th class="px-5 py-4 text-left min-w-[200px]">权限标识</th>
                <th class="px-5 py-4 text-left min-w-[150px]">路由名称</th>
                <th class="px-5 py-4 text-left min-w-[150px]">路由路径</th>
                <th class="px-5 py-4 text-left min-w-[200px]">组件路径</th>
                <th class="px-5 py-4 text-center w-24">路由参数</th>
                <th class="px-5 py-4 text-left min-w-[200px]">描述</th>
                <th class="px-5 py-4 text-center min-w-[160px]">创建时间</th>
                <th class="px-5 py-4 text-center min-w-[160px]">更新时间</th>
                <th class="px-5 py-4 text-center w-48 fixed-col">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-if="loading" class="animate-pulse">
                <td colspan="22" class="px-6 py-12 text-center text-slate-400">
                  <div class="flex flex-col items-center gap-3">
                    <Loader2Icon class="w-8 h-8 animate-spin text-blue-500" />
                    <span>加载中...</span>
                  </div>
                </td>
              </tr>
              <tr v-else-if="menuList.length === 0">
                <td colspan="22" class="px-6 py-12 text-center text-slate-400">
                  <div class="flex flex-col items-center gap-3">
                    <InboxIcon class="w-12 h-12 text-slate-300" />
                    <span>暂无数据</span>
                  </div>
                </td>
              </tr>
              <template v-else>
                <template v-for="(menu, index) in flattenMenuList" :key="menu.id">
                  <tr
                    v-show="isMenuVisible(menu)"
                    class="hover:bg-slate-50/80 transition-colors group"
                    :style="{ backgroundColor: menu.level && menu.level > 0 ? `rgba(248, 250, 252, ${menu.level * 0.3})` : '' }"
                  >
                    <td class="px-5 py-4 text-center">
                      <input type="checkbox" class="rounded border-slate-300 text-blue-600 focus:ring-blue-500" :value="menu.id" v-model="selectedIds" />
                    </td>
                    <td class="px-5 py-4 text-center text-slate-500">{{ index + 1 }}</td>
                    <td class="px-5 py-4">
                      <div class="flex items-center gap-2">
                        <span :style="{ marginLeft: menu.level * 20 + 'px' }">
                          <!-- 展开/折叠按钮 -->
                          <button
                            v-if="menu.children && menu.children.length > 0"
                            @click="toggleExpand(menu.id!)"
                            class="p-1 hover:bg-slate-200 rounded transition-colors"
                          >
                            <ChevronRightIcon
                              class="w-4 h-4 text-slate-500 transition-transform"
                              :class="{ 'rotate-90': expandedIds.includes(menu.id!) }"
                            />
                          </button>
                          <span v-else class="w-6 inline-block"></span>
                        </span>
                        <span class="font-medium text-slate-900">{{ menu.name }}</span>
                      </div>
                    </td>
                    <td class="px-5 py-4 text-center">
                      <component v-if="menu.icon && getIconComponent(menu.icon)" :is="getIconComponent(menu.icon)" class="w-5 h-5 mx-auto text-slate-600" />
                      <span v-else-if="menu.icon" class="text-slate-600">{{ menu.icon }}</span>
                      <span v-else class="text-slate-300">-</span>
                    </td>
                    <td class="px-5 py-4 text-center">
                      <span
                        class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                        :class="menu.status === '0' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-red-50 text-red-700 border border-red-200'"
                      >
                        <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="menu.status === '0' ? 'bg-emerald-500' : 'bg-red-500'"></span>
                        {{ menu.status === '0' ? '启用' : '停用' }}
                      </span>
                    </td>
                    <td class="px-5 py-4 text-center">
                      <span
                        class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium"
                        :class="getMenuTypeClass(menu.type)"
                      >
                        {{ getMenuTypeText(menu.type) }}
                      </span>
                    </td>
                    <td class="px-5 py-4 text-center text-slate-600">{{ menu.order }}</td>
                    <td class="px-5 py-4 text-slate-600">{{ menu.redirect || '-' }}</td>
                    <td class="px-5 py-4 text-center">
                      <span
                        class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                        :class="menu.keep_alive ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-600 border border-slate-200'"
                      >
                        {{ menu.keep_alive ? '是' : '否' }}
                      </span>
                    </td>
                    <td class="px-5 py-4 text-center">
                      <span
                        class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                        :class="menu.hidden ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-600 border border-slate-200'"
                      >
                        {{ menu.hidden ? '是' : '否' }}
                      </span>
                    </td>
                    <td class="px-5 py-4 text-center">
                      <span
                        class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                        :class="menu.always_show ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-600 border border-slate-200'"
                      >
                        {{ menu.always_show ? '是' : '否' }}
                      </span>
                    </td>
                    <td class="px-5 py-4 text-center">
                      <span
                        class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                        :class="menu.affix ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-600 border border-slate-200'"
                      >
                        {{ menu.affix ? '是' : '否' }}
                      </span>
                    </td>
                    <td class="px-5 py-4 text-slate-600">{{ menu.title || '-' }}</td>
                    <td class="px-5 py-4 text-slate-600">{{ menu.permission || '-' }}</td>
                    <td class="px-5 py-4 text-slate-600">{{ menu.route_name || '-' }}</td>
                    <td class="px-5 py-4 text-slate-600">{{ menu.route_path || '-' }}</td>
                    <td class="px-5 py-4 text-slate-600">{{ menu.component_path || '-' }}</td>
                    <td class="px-5 py-4 text-center">
                      <span v-if="menu.params && menu.params.length > 0" class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium bg-blue-50 text-blue-700 border border-blue-100">
                        {{ menu.params.length }}个
                      </span>
                      <span v-else class="text-slate-400">-</span>
                    </td>
                    <td class="px-5 py-4 text-slate-600">{{ menu.description || '-' }}</td>
                    <td class="px-5 py-4 text-center text-slate-500 whitespace-nowrap text-xs">{{ formatDate(menu.created_time) }}</td>
                    <td class="px-5 py-4 text-center text-slate-500 whitespace-nowrap text-xs">{{ formatDate(menu.updated_time) }}</td>
                    <td class="px-5 py-4 text-center fixed-col">
                      <div class="flex items-center justify-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          v-if="menu.type === MenuTypeEnum.CATALOG || menu.type === MenuTypeEnum.MENU"
                          @click="handleAddChild(menu)"
                          class="p-2 text-slate-800 hover:text-emerald-600 hover:bg-emerald-50 rounded-xl transition-all"
                          title="新增子菜单"
                        >
                          <PlusIcon class="w-4 h-4" />
                        </button>
                        <button
                          @click="handleView(menu)"
                          class="p-2 text-slate-800 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all"
                          title="详情"
                        >
                          <EyeIcon class="w-4 h-4" />
                        </button>
                        <button
                          @click="handleEdit(menu)"
                          class="p-2 text-slate-800 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all"
                          title="编辑"
                        >
                          <EditIcon class="w-4 h-4" />
                        </button>
                        <button
                          @click="handleDelete(menu)"
                          class="p-2 text-slate-800 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all"
                          title="删除"
                        >
                          <TrashIcon class="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                </template>
              </template>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Add/Edit/Detail Modal -->
    <div v-if="dialogVisible" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-3xl max-h-[90vh] overflow-hidden flex flex-col">
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
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">编号</div>
                <div class="font-medium text-slate-900">{{ detailData.id }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">菜单名称</div>
                <div class="font-medium text-slate-900">{{ detailData.name }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">菜单类型</div>
                <span class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium" :class="getMenuTypeClass(detailData.type)">
                  {{ getMenuTypeText(detailData.type) }}
                </span>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">图标</div>
                <component v-if="detailData.icon && getIconComponent(detailData.icon)" :is="getIconComponent(detailData.icon)" class="w-5 h-5 text-slate-600" />
                <span v-else class="text-slate-600">{{ detailData.icon || '-' }}</span>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">排序</div>
                <div class="font-medium text-slate-900">{{ detailData.order }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">权限标识</div>
                <div class="font-medium text-slate-900">{{ detailData.permission || '-' }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">路由名称</div>
                <div class="font-medium text-slate-900">{{ detailData.route_name || '-' }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">路由路径</div>
                <div class="font-medium text-slate-900">{{ detailData.route_path || '-' }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">组件路径</div>
                <div class="font-medium text-slate-900">{{ detailData.component_path || '-' }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">重定向</div>
                <div class="font-medium text-slate-900">{{ detailData.redirect || '-' }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">父级编号</div>
                <div class="font-medium text-slate-900">{{ detailData.parent_id || '-' }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">父级菜单</div>
                <div class="font-medium text-slate-900">{{ detailData.parent_name || '-' }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">是否缓存</div>
                <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium" :class="detailData.keep_alive ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-600 border border-slate-200'">
                  {{ detailData.keep_alive ? '是' : '否' }}
                </span>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">是否显示</div>
                <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium" :class="detailData.hidden ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-600 border border-slate-200'">
                  {{ detailData.hidden ? '是' : '否' }}
                </span>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">是否显示根路由</div>
                <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium" :class="detailData.always_show ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-600 border border-slate-200'">
                  {{ detailData.always_show ? '是' : '否' }}
                </span>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">菜单标题</div>
                <div class="font-medium text-slate-900">{{ detailData.title || '-' }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">路由参数</div>
                <div class="font-medium text-slate-900">{{ detailData.params && detailData.params.length > 0 ? detailData.params.map((p: any) => `${p.key}=${p.value}`).join(', ') : '-' }}</div>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">是否固定路由</div>
                <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium" :class="detailData.affix ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-600 border border-slate-200'">
                  {{ detailData.affix ? '是' : '否' }}
                </span>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">状态</div>
                <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium" :class="detailData.status === '0' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-red-50 text-red-700 border border-red-200'">
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
          <div v-else class="space-y-5">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <!-- 父级菜单 -->
              <div v-if="form.type !== MenuTypeEnum.CATALOG" class="md:col-span-2">
                <label class="block text-sm font-medium text-slate-700 mb-2">父级菜单 <span class="text-red-500">*</span></label>
                <select v-model="form.parent_id" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all">
                  <option value="">请选择父级菜单</option>
                  <option v-for="menu in parentMenuOptions" :key="menu.id" :value="menu.id">{{ menu.name }}</option>
                </select>
              </div>

              <!-- 菜单名称 -->
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">菜单名称 <span class="text-red-500">*</span></label>
                <input
                  v-model="form.name"
                  type="text"
                  placeholder="请输入菜单名称"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
              </div>

              <!-- 菜单标题 -->
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">菜单标题 <span class="text-red-500">*</span></label>
                <input
                  v-model="form.title"
                  type="text"
                  placeholder="请输入菜单标题"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
              </div>

              <!-- 菜单类型 -->
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-slate-700 mb-2">菜单类型 <span class="text-red-500">*</span></label>
                <div class="flex gap-4">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="form.type" :value="MenuTypeEnum.CATALOG" class="text-blue-600 focus:ring-blue-500" />
                    <span class="text-sm text-slate-700">目录</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="form.type" :value="MenuTypeEnum.MENU" class="text-blue-600 focus:ring-blue-500" />
                    <span class="text-sm text-slate-700">菜单</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="form.type" :value="MenuTypeEnum.BUTTON" class="text-blue-600 focus:ring-blue-500" />
                    <span class="text-sm text-slate-700">按钮</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="form.type" :value="MenuTypeEnum.EXTLINK" class="text-blue-600 focus:ring-blue-500" />
                    <span class="text-sm text-slate-700">外链</span>
                  </label>
                </div>
              </div>

              <!-- 外链地址 -->
              <div v-if="form.type === MenuTypeEnum.EXTLINK" class="md:col-span-2">
                <label class="block text-sm font-medium text-slate-700 mb-2">外链地址 <span class="text-red-500">*</span></label>
                <input
                  v-model="form.route_path"
                  type="text"
                  placeholder="请输入外链完整路径"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
              </div>

              <!-- 路由名称 -->
              <div v-if="form.type !== MenuTypeEnum.BUTTON">
                <label class="block text-sm font-medium text-slate-700 mb-2">
                  路由名称
                  <span class="text-xs text-slate-400 ml-1">(需与页面defineOptions中的name一致)</span>
                </label>
                <input
                  v-model="form.route_name"
                  type="text"
                  placeholder="请输入路由名称"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
              </div>

              <!-- 路由路径 -->
              <div v-if="form.type === MenuTypeEnum.CATALOG || form.type === MenuTypeEnum.MENU">
                <label class="block text-sm font-medium text-slate-700 mb-2">
                  路由路径
                  <span class="text-xs text-slate-400 ml-1">(目录以/开头)</span>
                </label>
                <input
                  v-model="form.route_path"
                  type="text"
                  placeholder="如：/system"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
              </div>

              <!-- 组件路径 -->
              <div v-if="form.type === MenuTypeEnum.MENU" class="md:col-span-2">
                <label class="block text-sm font-medium text-slate-700 mb-2">
                  组件路径
                  <span class="text-xs text-slate-400 ml-1">(相对于src/views/，缺省后缀.vue)</span>
                </label>
                <div class="flex gap-2">
                  <span class="px-3 py-2.5 bg-slate-100 border border-slate-200 border-r-0 rounded-l-xl text-slate-500 text-sm">src/views/</span>
                  <input
                    v-model="form.component_path"
                    type="text"
                    placeholder="如：system/user/index"
                    class="flex-1 px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-none focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                  />
                  <span class="px-3 py-2.5 bg-slate-100 border border-slate-200 border-l-0 rounded-r-xl text-slate-500 text-sm">.vue</span>
                </div>
              </div>

              <!-- 路由参数 -->
              <div v-if="form.type === MenuTypeEnum.MENU" class="md:col-span-2">
                <label class="block text-sm font-medium text-slate-700 mb-2">路由参数</label>
                <div v-if="!form.params || form.params.length === 0">
                  <button type="button" @click="form.params = [{ key: '', value: '' }]" class="px-4 py-2 bg-emerald-50 text-emerald-600 border border-emerald-200 rounded-xl hover:bg-emerald-100 transition-all text-sm">
                    添加路由参数
                  </button>
                </div>
                <div v-else class="space-y-2">
                  <div v-for="(item, index) in form.params" :key="index" class="flex items-center gap-2">
                    <input v-model="item.key" type="text" placeholder="参数名" class="w-28 px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-50 focus:border-blue-400" />
                    <span class="text-slate-400">=</span>
                    <input v-model="item.value" type="text" placeholder="参数值" class="w-28 px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-50 focus:border-blue-400" />
                    <button type="button" @click="form.params.push({ key: '', value: '' })" class="p-2 text-emerald-600 hover:bg-emerald-50 rounded-lg transition-all">
                      <PlusCircleIcon class="w-5 h-5" />
                    </button>
                    <button type="button" @click="form.params.splice(index, 1)" class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-all">
                      <MinusCircleIcon class="w-5 h-5" />
                    </button>
                  </div>
                </div>
              </div>

              <!-- 是否隐藏 -->
              <div v-if="form.type !== MenuTypeEnum.BUTTON">
                <label class="block text-sm font-medium text-slate-700 mb-2">是否隐藏</label>
                <div class="flex gap-4">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="form.hidden" :value="true" class="text-blue-600 focus:ring-blue-500" />
                    <span class="text-sm text-slate-700">是</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="form.hidden" :value="false" class="text-blue-600 focus:ring-blue-500" />
                    <span class="text-sm text-slate-700">否</span>
                  </label>
                </div>
              </div>

              <!-- 始终显示 -->
              <div v-if="form.type === MenuTypeEnum.CATALOG || form.type === MenuTypeEnum.MENU">
                <label class="block text-sm font-medium text-slate-700 mb-2">始终显示</label>
                <div class="flex gap-4">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="form.always_show" :value="true" class="text-blue-600 focus:ring-blue-500" />
                    <span class="text-sm text-slate-700">是</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="form.always_show" :value="false" class="text-blue-600 focus:ring-blue-500" />
                    <span class="text-sm text-slate-700">否</span>
                  </label>
                </div>
              </div>

              <!-- 缓存页面 -->
              <div v-if="form.type === MenuTypeEnum.MENU">
                <label class="block text-sm font-medium text-slate-700 mb-2">缓存页面</label>
                <div class="flex gap-4">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="form.keep_alive" :value="true" class="text-blue-600 focus:ring-blue-500" />
                    <span class="text-sm text-slate-700">开启</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="form.keep_alive" :value="false" class="text-blue-600 focus:ring-blue-500" />
                    <span class="text-sm text-slate-700">关闭</span>
                  </label>
                </div>
              </div>

              <!-- 排序 -->
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">排序 <span class="text-red-500">*</span></label>
                <input
                  v-model.number="form.order"
                  type="number"
                  min="1"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
              </div>

              <!-- 权限标识 -->
              <div v-if="form.type === MenuTypeEnum.BUTTON || form.type === MenuTypeEnum.MENU">
                <label class="block text-sm font-medium text-slate-700 mb-2">权限标识</label>
                <input
                  v-model="form.permission"
                  type="text"
                  placeholder="如：sys:user:add"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
              </div>

              <!-- 图标 -->
              <div v-if="form.type !== MenuTypeEnum.BUTTON">
                <label class="block text-sm font-medium text-slate-700 mb-2">图标</label>
                <input
                  v-model="form.icon"
                  type="text"
                  placeholder="请输入图标名称"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
              </div>

              <!-- 重定向 -->
              <div v-if="form.type === MenuTypeEnum.CATALOG || form.type === MenuTypeEnum.MENU">
                <label class="block text-sm font-medium text-slate-700 mb-2">重定向</label>
                <input
                  v-model="form.redirect"
                  type="text"
                  placeholder="请输入重定向路由"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
              </div>

              <!-- 常驻标签栏 -->
              <div v-if="form.type !== MenuTypeEnum.BUTTON">
                <label class="block text-sm font-medium text-slate-700 mb-2">常驻标签栏</label>
                <div class="flex gap-4">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="form.affix" :value="true" class="text-blue-600 focus:ring-blue-500" />
                    <span class="text-sm text-slate-700">是</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="form.affix" :value="false" class="text-blue-600 focus:ring-blue-500" />
                    <span class="text-sm text-slate-700">否</span>
                  </label>
                </div>
              </div>

              <!-- 状态 -->
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">状态 <span class="text-red-500">*</span></label>
                <div class="flex gap-4">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="form.status" value="0" class="text-blue-600 focus:ring-blue-500" />
                    <span class="text-sm text-slate-700">启用</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="radio" v-model="form.status" value="1" class="text-blue-600 focus:ring-blue-500" />
                    <span class="text-sm text-slate-700">禁用</span>
                  </label>
                </div>
              </div>

              <!-- 描述 -->
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-slate-700 mb-2">描述</label>
                <textarea
                  v-model="form.description"
                  rows="3"
                  maxlength="100"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all resize-none"
                  placeholder="请输入描述"
                ></textarea>
                <div class="text-right text-xs text-slate-400 mt-1">{{ form.description?.length || 0 }}/100</div>
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
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import {
  ArrowLeft as ArrowLeftIcon,
  Plus as PlusIcon,
  Trash2 as TrashIcon,
  Edit as EditIcon,
  Eye as EyeIcon,
  X as XIcon,
  RefreshCw as RefreshCwIcon,
  Search as SearchIcon,
  Loader2 as Loader2Icon,
  Inbox as InboxIcon,
  Menu as MenuIcon,
  PlusCircle as PlusCircleIcon,
  MinusCircle as MinusCircleIcon,
  ChevronUp as ChevronUpIcon,
  ChevronDown as ChevronDownIcon,
  ChevronRight as ChevronRightIcon,
  Folder,
  FileText,
  MousePointer,
  ExternalLink,
  LayoutDashboard,
  Settings,
  Users,
  Shield,
  Building,
  Briefcase,
  Home,
  Play as PlayIcon,
  Pause as PauseIcon
} from 'lucide-vue-next';
import MenuAPI, { MenuPageQuery, MenuForm, MenuTable } from '@/services/fastApi/module_system/menu';
import message from '@/components/common/message';
import { dialog } from '@/components/common/dialog';

const router = useRouter();

// 菜单类型枚举
const MenuTypeEnum = {
  CATALOG: 1,  // 目录
  MENU: 2,     // 菜单
  BUTTON: 3,   // 按钮
  EXTLINK: 4   // 外链
};

// State
const loading = ref(false);
const submitting = ref(false);
const menuList = ref<MenuTable[]>([]);
const selectedIds = ref<number[]>([]);
const dialogVisible = ref(false);
const dialogType = ref<'create' | 'edit' | 'detail'>('create');
const detailData = ref<any>({});
const isExpand = ref(false);
const expandedIds = ref<number[]>([]);

const queryParams = reactive<{
  name: string;
  status: string;
  start_time: string;
  end_time: string;
}>({
  name: '',
  status: '',
  start_time: '',
  end_time: ''
});

// 图标映射
const iconMap: Record<string, any> = {
  'dashboard': LayoutDashboard,
  'system': Settings,
  'user': Users,
  'role': Shield,
  'dept': Building,
  'post': Briefcase,
  'menu': MenuIcon,
  'home': Home,
  'folder': Folder,
  'file': FileText,
  'cursor': MousePointer,
  'link': ExternalLink,
};

// 默认表单
const defaultForm: MenuForm = {
  name: '',
  title: '',
  type: MenuTypeEnum.MENU,
  icon: '',
  order: 1,
  permission: '',
  route_name: '',
  route_path: '',
  component_path: '',
  redirect: '',
  parent_id: undefined,
  keep_alive: false,
  hidden: false,
  always_show: false,
  params: [],
  affix: false,
  status: '0',
  description: ''
};

const form = reactive<MenuForm>({ ...defaultForm });

// Computed
const isAllSelected = computed(() => {
  const allIds = flattenMenus(menuList.value).map(m => m.id);
  return allIds.length > 0 && selectedIds.value.length === allIds.length;
});

const dialogTitle = computed(() => {
  if (dialogType.value === 'detail') return '菜单详情';
  if (dialogType.value === 'edit') return '编辑菜单';
  return '新增菜单';
});

// 扁平化菜单列表（用于表格显示）
const flattenMenuList = computed(() => {
  return flattenMenus(menuList.value);
});

// 父级菜单选项（排除按钮类型）
const parentMenuOptions = computed(() => {
  return flattenMenus(menuList.value).filter(m => m.type === MenuTypeEnum.CATALOG || m.type === MenuTypeEnum.MENU);
});

// Methods
const flattenMenus = (menus: MenuTable[], level = 0, parentId?: number): Array<MenuTable & { level: number; parentId?: number }> => {
  const result: Array<MenuTable & { level: number; parentId?: number }> = [];
  menus.forEach(menu => {
    result.push({ ...menu, level, parentId });
    if (menu.children && menu.children.length > 0) {
      result.push(...flattenMenus(menu.children, level + 1, menu.id));
    }
  });
  return result;
};

const toggleExpand = (id: number) => {
  const index = expandedIds.value.indexOf(id);
  if (index > -1) {
    // 折叠时，同时折叠所有子节点
    const childrenIds = getAllChildrenIds(id);
    expandedIds.value = expandedIds.value.filter(expandedId =>
      expandedId !== id && !childrenIds.includes(expandedId)
    );
  } else {
    expandedIds.value.push(id);
  }
};

const getAllChildrenIds = (parentId: number): number[] => {
  const ids: number[] = [];
  const findChildren = (menus: MenuTable[]) => {
    menus.forEach(menu => {
      if (menu.id === parentId && menu.children) {
        menu.children.forEach(child => {
          if (child.id) {
            ids.push(child.id);
            findChildren([child]);
          }
        });
      } else if (menu.children) {
        findChildren(menu.children);
      }
    });
  };
  findChildren(menuList.value);
  return ids;
};

const isMenuVisible = (menu: MenuTable & { level: number; parentId?: number }) => {
  // 顶级菜单始终显示
  if (menu.level === 0) return true;
  // 检查所有父级是否都已展开
  let currentParentId = menu.parentId;
  while (currentParentId !== undefined) {
    if (!expandedIds.value.includes(currentParentId)) {
      return false;
    }
    // 找到当前父级的父级
    const parent = flattenMenuList.value.find(m => m.id === currentParentId);
    currentParentId = parent?.parentId;
  }
  return true;
};

const getIconComponent = (iconName: string) => {
  if (!iconName) return null;
  // 处理 el-icon 前缀
  if (iconName.startsWith('el-icon-')) {
    const name = iconName.replace('el-icon-', '');
    return iconMap[name] || null;
  }
  return iconMap[iconName] || null;
};

const getMenuTypeText = (type?: number | string) => {
  // 将字符串类型转换为数字
  const typeNum = typeof type === 'string' ? parseInt(type, 10) : type;
  switch (typeNum) {
    case MenuTypeEnum.CATALOG: return '目录';
    case MenuTypeEnum.MENU: return '菜单';
    case MenuTypeEnum.BUTTON: return '按钮';
    case MenuTypeEnum.EXTLINK: return '外链';
    default: return '未知';
  }
};

const getMenuTypeClass = (type?: number | string) => {
  // 将字符串类型转换为数字
  const typeNum = typeof type === 'string' ? parseInt(type, 10) : type;
  switch (typeNum) {
    case MenuTypeEnum.CATALOG: return 'bg-amber-50 text-amber-700 border border-amber-200';
    case MenuTypeEnum.MENU: return 'bg-emerald-50 text-emerald-700 border border-emerald-200';
    case MenuTypeEnum.BUTTON: return 'bg-red-50 text-red-700 border border-red-200';
    case MenuTypeEnum.EXTLINK: return 'bg-slate-50 text-slate-700 border border-slate-200';
    default: return 'bg-slate-100 text-slate-600 border border-slate-200';
  }
};

const formatDate = (dateStr?: string) => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleString();
};

const fetchMenus = async () => {
  loading.value = true;
  try {
    const params: MenuPageQuery = {};
    if (queryParams.name) params.name = queryParams.name;
    if (queryParams.status) params.status = queryParams.status;
    if (queryParams.start_time || queryParams.end_time) {
      params.created_time = [queryParams.start_time, queryParams.end_time].filter(Boolean) as string[];
    }

    const res = await MenuAPI.listMenu(params);
    if (res?.data?.data) {
      menuList.value = res.data.data;
    }
  } catch (error) {
    console.error('Failed to fetch menus:', error);
    message.error('获取菜单列表失败');
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  fetchMenus();
};

const handleReset = () => {
  queryParams.name = '';
  queryParams.status = '';
  queryParams.start_time = '';
  queryParams.end_time = '';
  isExpand.value = false;
  fetchMenus();
};

const handleRefresh = () => {
  fetchMenus();
  message.success('刷新成功');
};

const toggleAllSelection = (e: Event) => {
  const checked = (e.target as HTMLInputElement).checked;
  const allIds = flattenMenus(menuList.value).map(m => m.id).filter(id => id !== undefined);
  if (checked) {
    selectedIds.value = allIds as number[];
  } else {
    selectedIds.value = [];
  }
};

const handleAdd = () => {
  dialogType.value = 'create';
  Object.assign(form, defaultForm);
  form.params = [];
  dialogVisible.value = true;
};

const handleAddChild = (menu: MenuTable) => {
  dialogType.value = 'create';
  Object.assign(form, defaultForm);
  form.parent_id = menu.id;
  form.params = [];
  dialogVisible.value = true;
};

const handleEdit = async (menu: MenuTable) => {
  dialogType.value = 'edit';
  if (menu.id) {
    try {
      const res = await MenuAPI.detailMenu(menu.id);
      if (res?.data?.data) {
        const data = res.data.data;
        Object.assign(form, {
          ...defaultForm,
          ...data,
          params: data.params || []
        });
      }
    } catch (error) {
      console.error('Failed to fetch menu detail:', error);
    }
  }
  dialogVisible.value = true;
};

const handleView = async (menu: MenuTable) => {
  dialogType.value = 'detail';
  if (menu.id) {
    try {
      const res = await MenuAPI.detailMenu(menu.id);
      detailData.value = res?.data?.data || {};
    } catch (error) {
      console.error('Failed to fetch menu detail:', error);
    }
  }
  dialogVisible.value = true;
};

const closeDialog = () => {
  dialogVisible.value = false;
  Object.assign(form, defaultForm);
  form.params = [];
};

const submitForm = async () => {
  // 表单验证
  if (!form.name) {
    message.warning('请输入菜单名称');
    return;
  }
  if (!form.title) {
    message.warning('请输入菜单标题');
    return;
  }
  if (form.type !== MenuTypeEnum.CATALOG && !form.parent_id) {
    message.warning('请选择父级菜单');
    return;
  }
  if ((form.type === MenuTypeEnum.CATALOG || form.type === MenuTypeEnum.MENU) && form.route_path && !form.route_path.startsWith('/')) {
    message.warning('目录和菜单路由路径必须以/开头');
    return;
  }

  submitting.value = true;

  try {
    const payload: MenuForm = {
      ...form,
      params: form.params?.filter(p => p.key && p.value) || []
    };

    if (dialogType.value === 'edit' && form.id) {
      await MenuAPI.updateMenu(form.id, payload);
    } else {
      await MenuAPI.createMenu(payload);
    }
    closeDialog();
    fetchMenus();
    message.success('操作成功');
  } catch (error: any) {
    console.error('Operation failed:', error);
    const msg = error.data?.msg || error.message || '操作失败，请重试';
    message.error(msg);
  } finally {
    submitting.value = false;
  }
};

const handleDelete = async (menu: MenuTable) => {
  if (!menu.id) return;
  try {
    await dialog.confirm(`确定要删除菜单 "${menu.name}" 吗？`);
    await MenuAPI.deleteMenu([menu.id]);
    fetchMenus();
    message.success('删除成功');
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return;
    console.error('Delete failed:', error);
    message.error('删除失败');
  }
};

const handleBatchDelete = async () => {
  if (selectedIds.value.length === 0) return;
  try {
    await dialog.confirm(`确定要删除选中的 ${selectedIds.value.length} 个菜单吗？`);
    await MenuAPI.deleteMenu(selectedIds.value);
    selectedIds.value = [];
    fetchMenus();
    message.success('批量删除成功');
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return;
    console.error('Batch delete failed:', error);
    message.error('批量删除失败');
  }
};

const handleBatchStatus = async (status: string) => {
  if (selectedIds.value.length === 0) return;
  try {
    const statusText = status === '0' ? '启用' : '停用';
    await dialog.confirm(`确定要${statusText}选中的 ${selectedIds.value.length} 个菜单吗？`);
    await MenuAPI.batchMenu({ ids: selectedIds.value, status });
    selectedIds.value = [];
    fetchMenus();
    message.success(`批量${statusText}成功`);
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') return;
    console.error('Batch status change failed:', error);
    message.error('操作失败');
  }
};

onMounted(() => {
  fetchMenus();
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
