<template>
  <div class="min-h-screen bg-slate-50 p-8 overflow-y-auto">
    <div class="max-w-6xl mx-auto">
      <!-- 顶部导航栏 -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">菜单管理</h1>
          <p class="mt-1 text-sm text-slate-500">维护系统菜单与权限路由配置。</p>
        </div>
        <div class="flex gap-3">
          <div class="relative group h-11">
            <button
              @click="handleAdd"
              class="h-full px-5 text-white rounded-xl font-bold shadow-lg transition-all flex items-center gap-2 active:scale-95 bg-slate-900 hover:bg-slate-800"
            >
              <PlusIcon :size="18" />
              新增菜单
              <ChevronDownIcon :size="18" class="ml-1 -mr-1 opacity-80" />
            </button>
            <div class="absolute right-0 top-full pt-2 w-36 hidden group-hover:block z-50">
              <div class="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden py-1">
                <button
                  class="w-full px-4 py-2.5 text-left text-slate-600 hover:bg-slate-50 hover:text-blue-600 font-medium transition-all flex items-center gap-2"
                  @click="handleAdd"
                >
                  <PlusIcon :size="16" />
                  新增菜单
                </button>
                <div class="h-px bg-slate-100 my-1 mx-2"></div>
                <button
                  class="w-full px-4 py-2.5 text-left text-slate-600 hover:bg-slate-50 hover:text-blue-600 font-medium transition-all flex items-center gap-2"
                  @click="permissionPreviewVisible = true"
                >
                  <KeyIcon :size="16" />
                  权限字
                </button>
                <div class="h-px bg-slate-100 my-1 mx-2"></div>
                <button
                  class="w-full px-4 py-2.5 text-left text-slate-600 hover:bg-slate-50 hover:text-blue-600 font-medium transition-all flex items-center gap-2"
                  @click="handleExport"
                >
                  <DownloadIcon :size="16" />
                  导出配置
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Menu Table Card -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-sm" style="min-width: 1200px;">
            <thead class="bg-slate-50 text-slate-600 font-medium border-b border-slate-200">
              <tr>
                <th class="px-5 py-4 text-left min-w-[200px]">菜单名称</th>
                <th class="px-5 py-4 text-center min-w-[100px]">类型</th>
                <th class="px-5 py-4 text-center w-28">排序</th>
                <th class="px-5 py-4 text-left min-w-[200px]">权限标识</th>
                <th class="px-5 py-4 text-center w-48 fixed-col">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-if="loading" class="animate-pulse">
                <td colspan="5" class="px-6 py-12 text-center text-slate-400">
                  <div class="flex flex-col items-center gap-3">
                    <Loader2Icon class="w-8 h-8 animate-spin text-blue-500" />
                    <span>加载中...</span>
                  </div>
                </td>
              </tr>
              <tr v-else-if="menuList.length === 0">
                <td colspan="5" class="px-6 py-12 text-center text-slate-400">
                  <div class="flex flex-col items-center gap-3">
                    <InboxIcon class="w-12 h-12 text-slate-300" />
                    <span>暂无数据</span>
                  </div>
                </td>
              </tr>
              <template v-else>
                <template v-for="menu in flattenMenuList" :key="menu.id">
                  <tr
                    v-show="isMenuVisible(menu)"
                    class="hover:bg-slate-50/80 transition-colors group"
                    :style="{ backgroundColor: menu.level && menu.level > 0 ? `rgba(248, 250, 252, ${menu.level * 0.3})` : '' }"
                  >
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
                      <span
                        class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium"
                        :class="getMenuTypeClass(menu.type)"
                      >
                        {{ getMenuTypeText(menu.type) }}
                      </span>
                    </td>
                    <td class="px-5 py-4 text-center text-slate-600">{{ menu.order }}</td>
                    <td class="px-5 py-4 text-slate-600">{{ menu.permission || '-' }}</td>
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

    <!-- Permission Preview Modal -->
    <div v-if="permissionPreviewVisible" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-5xl max-h-[90vh] overflow-hidden flex flex-col relative">
        <div class="absolute top-4 right-4 z-10">
          <button @click="permissionPreviewVisible = false" class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-all bg-white/80 backdrop-blur">
            <XIcon class="w-5 h-5" />
          </button>
        </div>
        <div class="flex-1 overflow-y-auto">
          <PermissionPreview />
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
          <!-- Form -->
          <div class="space-y-5">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <!-- 父级菜单 -->
              <div v-if="form.type !== MenuTypeEnum.CATALOG" class="md:col-span-2">
                <label class="block text-sm font-medium text-slate-700 mb-2">父级菜单 <span class="text-red-500">*</span></label>
                <select v-model="form.parent_id" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all">
                  <option value="">请选择父级菜单</option>
                  <option v-for="menu in parentMenuOptions" :key="menu.id" :value="menu.id">
                    {{ '　'.repeat(menu.level) }}{{ menu.name }}
                  </option>
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

              <!-- 路由路径 (EXTLINK类型使用) -->
              <div v-if="form.type === MenuTypeEnum.EXTLINK">
                <label class="block text-sm font-medium text-slate-700 mb-2">
                  路由路径
                  <span class="text-xs text-slate-400 ml-1">(页面访问路径，如：/common/redoc)</span>
                </label>
                <input
                  v-model="form.route_path"
                  type="text"
                  placeholder="如：/common/docs"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                />
              </div>

              <!-- 外链目标地址 -->
              <div v-if="form.type === MenuTypeEnum.EXTLINK">
                <label class="block text-sm font-medium text-slate-700 mb-2">
                  外链目标
                  <span class="text-xs text-slate-400 ml-1">(iframe加载的地址)</span>
                </label>
                <input
                  v-model="form.component_path"
                  type="text"
                  placeholder="如：https://example.com 或 /api/v1/docs"
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
              <div v-if="form.type === MenuTypeEnum.MENU" class="md:col-span-2 relative">
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
                    @focus="componentPathOptionsVisible = true"
                    @blur="handleComponentPathBlur"
                  />
                  <span class="px-3 py-2.5 bg-slate-100 border border-slate-200 border-l-0 rounded-r-xl text-slate-500 text-sm">.vue</span>
                </div>
                <!-- 组件路径下拉面板 -->
                <div
                  v-show="componentPathOptionsVisible && filteredComponentPathOptions.length > 0"
                  class="absolute z-10 w-[calc(100%-8.5rem)] left-[88px] mt-1 bg-white border border-slate-200 rounded-xl shadow-lg max-h-60 overflow-y-auto"
                  @mousedown.prevent
                >
                  <ul class="py-1 text-sm text-slate-700">
                    <li
                      v-for="path in filteredComponentPathOptions"
                      :key="path"
                      @click="selectComponentPath(path)"
                      class="px-4 py-2 hover:bg-blue-50 hover:text-blue-600 cursor-pointer transition-colors"
                    >
                      {{ path }}
                    </li>
                  </ul>
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
              <div v-if="form.type === MenuTypeEnum.BUTTON || form.type === MenuTypeEnum.MENU" class="relative">
                <label class="block text-sm font-medium text-slate-700 mb-2">权限标识</label>
                <input
                  v-model="form.permission"
                  type="text"
                  placeholder="如：sys:user:add"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                  @focus="permissionOptionsVisible = true"
                  @blur="handlePermissionBlur"
                />
                <!-- 权限标识下拉面板 -->
                <div
                  v-show="permissionOptionsVisible && filteredPermissionOptions.length > 0"
                  class="absolute z-10 w-full mt-1 bg-white border border-slate-200 rounded-xl shadow-lg max-h-60 overflow-y-auto"
                  @mousedown.prevent
                >
                  <ul class="py-1 text-sm text-slate-700">
                    <li
                      v-for="perm in filteredPermissionOptions"
                      :key="perm"
                      @click="selectPermission(perm)"
                      class="px-4 py-2 hover:bg-blue-50 hover:text-blue-600 cursor-pointer transition-colors"
                    >
                      {{ perm }}
                    </li>
                  </ul>
                </div>
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

              <!-- 图标 -->
              <div v-if="form.type !== MenuTypeEnum.BUTTON" class="md:col-span-2">
                <label class="block text-sm font-medium text-slate-700 mb-2">图标</label>
                <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-3">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-lg bg-white border border-slate-200 flex items-center justify-center text-slate-700">
                      <component :is="getAgentCoverIconComponent(form.icon)" :size="18" />
                    </div>
                    <span class="text-xs text-slate-500">{{ form.icon || '请选择图标' }}</span>
                    <button
                      v-if="form.icon"
                      type="button"
                      @click="form.icon = ''"
                      class="ml-auto px-2 py-1 text-xs text-slate-500 border border-slate-200 rounded-md hover:bg-white hover:text-slate-700 transition-all"
                    >
                      清空
                    </button>
                  </div>
                  <div class="grid grid-cols-6 sm:grid-cols-8 gap-2 max-h-40 overflow-y-auto pr-1">
                    <button
                      v-for="icon in menuIconOptions"
                      :key="icon.id"
                      type="button"
                      @click="form.icon = icon.id"
                      :title="icon.label"
                      :class="`h-9 rounded-lg border flex items-center justify-center transition-colors ${isMenuIconSelected(icon.id) ? 'border-blue-500 text-blue-600 bg-blue-50' : 'border-slate-200 text-slate-500 bg-white hover:border-slate-300'}`"
                    >
                      <component :is="icon.component" :size="16" />
                    </button>
                  </div>
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
import PermissionPreview from './PermissionPreview.vue';
import {
  Plus as PlusIcon,
  Trash2 as TrashIcon,
  Edit as EditIcon,
  X as XIcon,
  Key as KeyIcon,
  Loader2 as Loader2Icon,
  Inbox as InboxIcon,
  Menu as MenuIcon,
  PlusCircle as PlusCircleIcon,
  MinusCircle as MinusCircleIcon,
  ChevronRight as ChevronRightIcon,
  ChevronDown as ChevronDownIcon,
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
  Download as DownloadIcon
} from 'lucide-vue-next';
import MenuAPI, { MenuForm, MenuTable } from '@/services/fastApi/module_system/menu';
import ExServicesAPI, { type PluginModulePermission } from '@/services/fastApi/module_ex/ex_services';
import { AGENT_COVER_ICON_OPTIONS, getAgentCoverIconComponent } from '@/components/common/agentCover';
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
const dialogVisible = ref(false);
const permissionPreviewVisible = ref(false);
const dialogType = ref<'create' | 'edit' | 'detail'>('create');
const detailData = ref<any>({});
const expandedIds = ref<number[]>([]);

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
const menuIconOptions = AGENT_COVER_ICON_OPTIONS;
const componentPathOptionsVisible = ref(false);
const componentPathOptions = Object.keys(import.meta.glob('/src/views/**/*.vue'))
  .map((path) => path.replace(/^\/src\/views\//, '').replace(/\.vue$/, ''))
  .filter(path => path)
  .sort((a, b) => a.localeCompare(b, 'zh-CN'));

console.log(componentPathOptions,import.meta.glob('/src/views/**/*.vue', { eager: true }));

const permissionOptionsVisible = ref(false);
const permissionOptions = ref<string[]>([]);

const fetchPermissions = async () => {
  try {
    const res = await ExServicesAPI.getPluginPermissions();
    const modules = res.data?.data?.modules || [];
    const perms = new Set<string>();
    modules.forEach(m => {
      m.permissions.forEach(p => perms.add(p));
    });
    permissionOptions.value = Array.from(perms).sort((a, b) => a.localeCompare(b, 'en-US'));
  } catch (error) {
    console.error('Failed to load plugin permissions:', error);
  }
};

// Computed
const filteredComponentPathOptions = computed(() => {
  const val = (form.component_path || '').trim().toLowerCase();
  if (!val) return componentPathOptions;
  return componentPathOptions.filter(path => path.toLowerCase().includes(val));
});

const selectComponentPath = (path: string) => {
  form.component_path = path;
  componentPathOptionsVisible.value = false;
};

const handleComponentPathBlur = () => {
  // 延迟关闭，以便让点击事件有时间触发
  setTimeout(() => {
    componentPathOptionsVisible.value = false;
  }, 150);
};

const filteredPermissionOptions = computed(() => {
  const val = (form.permission || '').trim().toLowerCase();
  if (!val) return permissionOptions.value;
  return permissionOptions.value.filter(p => p.toLowerCase().includes(val));
});

const selectPermission = (perm: string) => {
  form.permission = perm;
  permissionOptionsVisible.value = false;
};

const handlePermissionBlur = () => {
  setTimeout(() => {
    permissionOptionsVisible.value = false;
  }, 150);
};

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

const normalizeMenuIconKey = (icon?: string) => {
  const raw = String(icon || '').trim();
  if (!raw) {
    return '';
  }
  return raw
    .replace(/([a-z0-9])([A-Z])/g, '$1-$2')
    .replace(/^el-icon-/i, '')
    .replace(/^lucide:/i, '')
    .replace(/_+/g, '-')
    .replace(/-icon$/i, '')
    .toLowerCase();
};

const isMenuIconSelected = (iconId: string) => normalizeMenuIconKey(form.icon) === normalizeMenuIconKey(iconId);

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
    const res = await MenuAPI.listMenu({});
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

const handleRefresh = () => {
  fetchMenus();
  message.success('刷新成功');
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

const handleExport = () => {
  if (menuList.value.length === 0) {
    message.warning('没有可导出的数据');
    return;
  }

  const mapMenu = (menus: MenuTable[]): any[] => {
    return menus.map(menu => {
      const result: any = {
        name: menu.name,
        type: menu.type,
        icon: menu.icon || null,
        order: menu.order,
        permission: menu.permission || null,
        route_name: menu.route_name || null,
        route_path: menu.route_path || null,
        component_path: menu.component_path || null,
        status: menu.status || "0",
        keep_alive: !!menu.keep_alive,
        hidden: !!menu.hidden,
        always_show: !!menu.always_show,
        title: menu.title,
        params: menu.params && menu.params.length > 0 ? menu.params : null,
        affix: !!menu.affix,
        redirect: menu.redirect || null,
        description: menu.description || null
      };
      
      if (menu.children && menu.children.length > 0) {
        result.children = mapMenu(menu.children);
      }
      
      return result;
    });
  };

  try {
    const exportData = mapMenu(menuList.value);
    const jsonStr = JSON.stringify(exportData, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'sys_menu.json';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    message.success('配置导出成功');
  } catch (error) {
    console.error('Export failed:', error);
    message.error('导出失败');
  }
};

onMounted(() => {
  fetchMenus();
  fetchPermissions();
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
