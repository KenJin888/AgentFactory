<template>
  <div class="h-full min-h-[500px] bg-slate-50 p-8 overflow-y-auto">
    <div class="max-w-6xl mx-auto">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">权限字总览</h1>
          <p class="mt-1 text-sm text-slate-500">查看系统权限字并检查菜单权限字差异。</p>
        </div>
        <div class="flex items-center gap-3">
          <button
            @click="exportToMarkdown"
            class="px-4 py-3 bg-white border border-slate-200 text-slate-700 rounded-xl font-bold hover:bg-slate-50 shadow-sm flex items-center gap-2 transition-colors"
          >
            <DownloadIcon class="w-5 h-5" />
            导出 Markdown
          </button>
          <button
            @click="loadAllData"
            :disabled="loadingList || loadingCheck"
            class="px-4 py-3 bg-white border border-slate-200 text-slate-700 rounded-xl font-bold hover:bg-slate-50 shadow-sm flex items-center gap-2 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
          >
            <RefreshCwIcon :class="['w-5 h-5', loadingList || loadingCheck ? 'animate-spin' : '']" />
            刷新全部
          </button>
        </div>
      </div>

      <div class="flex border-b border-slate-200 mb-6">
        <button
          @click="activeTab = 'plugin'"
          :class="['px-6 py-3 font-medium text-sm border-b-2 transition-colors outline-none', activeTab === 'plugin' ? 'border-blue-500 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300']"
        >
          插件权限字
        </button>
        <button
          @click="activeTab = 'check'"
          :class="['px-6 py-3 font-medium text-sm border-b-2 transition-colors outline-none', activeTab === 'check' ? 'border-blue-500 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300']"
        >
          权限字检查
        </button>
      </div>

      <div v-show="activeTab === 'plugin'">
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-4 mb-4">
        <div class="relative">
          <SearchIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            v-model.trim="keyword"
            type="text"
            placeholder="按权限字搜索"
            class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
          />
        </div>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden mb-6">
        <div v-if="loadingList" class="px-6 py-12 text-center text-slate-400">正在加载权限字...</div>
        <div v-else-if="listErrorMessage" class="px-6 py-12 text-center text-red-500">{{ listErrorMessage }}</div>
        <div v-else-if="filteredModules.length === 0" class="px-6 py-12 text-center text-slate-400">暂无匹配权限字</div>
        <div v-else class="divide-y divide-slate-100">
          <div v-for="item in filteredModules" :key="item.module" class="p-6">
            <div class="flex items-center justify-between gap-3 mb-3">
              <h3 class="text-lg font-semibold text-slate-900">{{ item.module }}</h3>
              <span class="text-xs font-medium bg-blue-50 text-blue-700 px-2.5 py-1 rounded-full">
                {{ item.permissions.length }} 条
              </span>
            </div>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="permission in item.permissions"
                :key="permission"
                class="px-2.5 py-1 rounded-lg bg-slate-100 text-slate-700 text-sm"
              >
                {{ permission }}
              </span>
            </div>
          </div>
        </div>
      </div>
      </div>

      <div v-show="activeTab === 'check'">
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">

        <div class="p-6 border-b border-slate-100 bg-slate-50/40">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-3">
            <div class="rounded-xl border border-blue-100 bg-blue-50 p-4">
              <div class="text-xs text-blue-700">系统权限字总数</div>
              <div class="mt-2 text-2xl font-bold text-blue-900">{{ systemPermissions.length }}</div>
            </div>
            <div class="rounded-xl border border-indigo-100 bg-indigo-50 p-4">
              <div class="text-xs text-indigo-700">Menu 权限字总数</div>
              <div class="mt-2 text-2xl font-bold text-indigo-900">{{ menuPermissions.length }}</div>
            </div>
            <div class="rounded-xl border border-amber-100 bg-amber-50 p-4">
              <div class="text-xs text-amber-700">系统有，Menu 没有</div>
              <div class="mt-2 text-2xl font-bold text-amber-900">{{ missingInMenu.length }}</div>
            </div>
            <div class="rounded-xl border border-rose-100 bg-rose-50 p-4">
              <div class="text-xs text-rose-700">Menu 有，系统没有</div>
              <div class="mt-2 text-2xl font-bold text-rose-900">{{ missingInSystem.length }}</div>
            </div>
          </div>

          <div class="mt-4 relative">
            <SearchIcon class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              v-model.trim="checkKeyword"
              type="text"
              placeholder="按权限字过滤检查结果"
              class="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
            />
          </div>
        </div>

        <div class="p-6 bg-slate-50">
          <div v-if="loadingCheck" class="rounded-2xl border border-slate-100 bg-white px-6 py-12 text-center text-slate-500">
            正在检查权限字，请稍候...
          </div>
          <div v-else-if="checkErrorMessage" class="rounded-2xl border border-rose-100 bg-rose-50 px-6 py-12 text-center text-rose-600">
            {{ checkErrorMessage }}
          </div>
          <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div class="rounded-2xl border border-amber-100 bg-white overflow-hidden">
              <div class="px-4 py-3 border-b border-amber-100 bg-amber-50 flex items-center justify-between">
                <h3 class="font-semibold text-amber-800">系统有，Menu 没有</h3>
                <span class="text-xs px-2 py-1 rounded-full bg-amber-100 text-amber-700">{{ filteredMissingInMenu.length }}</span>
              </div>
              <div v-if="filteredMissingInMenu.length === 0" class="px-4 py-8 text-center text-slate-500">
                未发现该类不匹配项
              </div>
              <div v-else class="max-h-[45vh] overflow-y-auto p-4 space-y-2">
                <div
                  v-for="permission in filteredMissingInMenu"
                  :key="`sys-${permission}`"
                  class="px-3 py-2 rounded-lg bg-amber-50 text-amber-800 text-sm break-all"
                >
                  {{ permission }}
                </div>
              </div>
            </div>

            <div class="rounded-2xl border border-rose-100 bg-white overflow-hidden">
              <div class="px-4 py-3 border-b border-rose-100 bg-rose-50 flex items-center justify-between">
                <h3 class="font-semibold text-rose-800">Menu 有，系统没有</h3>
                <span class="text-xs px-2 py-1 rounded-full bg-rose-100 text-rose-700">{{ filteredMissingInSystem.length }}</span>
              </div>
              <div v-if="filteredMissingInSystem.length === 0" class="px-4 py-8 text-center text-slate-500">
                未发现该类不匹配项
              </div>
              <div v-else class="max-h-[45vh] overflow-y-auto p-4 space-y-2">
                <div
                  v-for="permission in filteredMissingInSystem"
                  :key="`menu-${permission}`"
                  class="px-3 py-2 rounded-lg bg-rose-50 text-rose-800 text-sm break-all"
                >
                  {{ permission }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { RefreshCwIcon, SearchIcon, DownloadIcon } from 'lucide-vue-next'
import ExServicesAPI, { type PluginModulePermission } from '@/services/fastApi/module_ex/ex_services'
import MenuAPI, { type MenuTable } from '@/services/fastApi/module_system/menu'

const activeTab = ref('plugin')
const loadingList = ref(false)
const loadingCheck = ref(false)
const listErrorMessage = ref('')
const checkErrorMessage = ref('')
const keyword = ref('')
const checkKeyword = ref('')
const modules = ref<PluginModulePermission[]>([])
const systemPermissions = ref<string[]>([])
const menuPermissions = ref<string[]>([])

const filteredModules = computed(() => {
  const value = keyword.value.trim().toLowerCase()
  if (!value) {
    return modules.value
  }
  return modules.value
    .map(item => {
      // 仅保留匹配的权限字
      const matchedPermissions = item.permissions.filter(permission =>
        permission.toLowerCase().includes(value)
      )
      return {
        ...item,
        permissions: matchedPermissions
      }
    })
    // 过滤掉没有匹配权限字的模块
    .filter(item => item.permissions.length > 0)
})

const missingInMenu = computed(() => {
  const menuSet = new Set(menuPermissions.value)
  return systemPermissions.value.filter(permission => !menuSet.has(permission))
})

const missingInSystem = computed(() => {
  const systemSet = new Set(systemPermissions.value)
  return menuPermissions.value.filter(permission => !systemSet.has(permission))
})

const filteredMissingInMenu = computed(() => {
  const value = checkKeyword.value.trim().toLowerCase()
  if (!value) {
    return missingInMenu.value
  }
  return missingInMenu.value.filter(permission => permission.toLowerCase().includes(value))
})

const filteredMissingInSystem = computed(() => {
  const value = checkKeyword.value.trim().toLowerCase()
  if (!value) {
    return missingInSystem.value
  }
  return missingInSystem.value.filter(permission => permission.toLowerCase().includes(value))
})

const loadPermissions = async () => {
  loadingList.value = true
  listErrorMessage.value = ''
  try {
    const res = await ExServicesAPI.getPluginPermissions()
    const payload = res.data?.data
    modules.value = payload?.modules || []
  } catch (error) {
    modules.value = []
    listErrorMessage.value = '加载权限字失败，请稍后重试'
    console.error('加载权限字失败:', error)
  } finally {
    loadingList.value = false
  }
}

const normalizePermissionValue = (raw: string) => raw.trim()

const splitPermissionValue = (raw?: string) => {
  return String(raw || '')
    .split(/[\n,，;；]/)
    .map(normalizePermissionValue)
    .filter(Boolean)
}

const collectMenuPermissions = (menus: MenuTable[]) => {
  const permissions = new Set<string>()
  const walk = (nodes: MenuTable[]) => {
    nodes.forEach((node) => {
      splitPermissionValue(node.permission).forEach(permission => permissions.add(permission))
      if (node.children?.length) {
        walk(node.children)
      }
    })
  }
  walk(menus)
  return Array.from(permissions).sort((a, b) => a.localeCompare(b, 'en-US'))
}

const loadPermissionCheck = async () => {
  loadingCheck.value = true
  checkErrorMessage.value = ''
  try {
    const [permissionRes, menuRes] = await Promise.all([
      ExServicesAPI.getAllPermissions(),
      MenuAPI.listMenu({})
    ])
    const allPermissions = permissionRes.data?.data?.all_permissions || []
    systemPermissions.value = Array.from(
      new Set(allPermissions.map(permission => normalizePermissionValue(permission)).filter(Boolean))
    ).sort((a, b) => a.localeCompare(b, 'en-US'))
    const menus = menuRes.data?.data || []
    menuPermissions.value = collectMenuPermissions(menus)
  } catch (error) {
    systemPermissions.value = []
    menuPermissions.value = []
    checkErrorMessage.value = '权限字检查失败，请稍后重试'
    console.error('权限字检查失败:', error)
  } finally {
    loadingCheck.value = false
  }
}

const loadAllData = async () => {
  await Promise.all([loadPermissions(), loadPermissionCheck()])
}

const exportToMarkdown = () => {
  let md = '# 权限字总览\n\n'

  md += '## 插件权限字\n\n'
  modules.value.forEach(item => {
    md += `### ${item.module} (${item.permissions.length} 条)\n`
    if (item.permissions.length) {
      md += item.permissions.map(p => `- ${p}`).join('\n') + '\n\n'
    }
  })

  md += '## 权限字检查结果\n\n'
  md += `- 接口权限字总数: ${systemPermissions.value.length}\n`
  md += `- 菜单权限字总数: ${menuPermissions.value.length}\n`
  md += `- 接口有，菜单没有: ${missingInMenu.value.length}\n`
  md += `- 菜单有，接口没有: ${missingInSystem.value.length}\n\n`

  if (missingInMenu.value.length) {
    md += '### 接口有，菜单没有\n'
    md += missingInMenu.value.map(p => `- ${p}`).join('\n') + '\n\n'
  }

  if (missingInSystem.value.length) {
    md += '### 菜单有，接口没有\n'
    md += missingInSystem.value.map(p => `- ${p}`).join('\n') + '\n\n'
  }

  const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `权限字总览_${new Date().toISOString().slice(0, 10)}.md`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

onMounted(() => {
  loadAllData()
})
</script>
