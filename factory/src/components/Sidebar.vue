<template>
  <div class="w-64 bg-slate-900 text-slate-300 flex flex-col h-full flex-shrink-0 transition-all duration-300 shadow-xl z-20">
    
    <div class="p-6 border-b border-slate-800">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-900/50">
          <img :src="webLogo" :alt="appTitle" class="w-8 h-8 object-contain" />
        </div>
        <div>
            <div class="text-white text-lg tracking-tight leading-tight">{{ appTitle }}</div>
              <div class="text-[10px] text-amber-400 flex items-center gap-1 font-bold mt-0.5">
                <Crown :size="10" fill="currentColor" />
                {{ runtimeStore.runMode === 'Web' ? '网页版' : '桌面版' }}
              </div>
        </div>
      </div>
      
      <button @click="handleNewChat" class="w-full bg-blue-600 hover:bg-blue-500 text-white py-2.5 rounded-xl flex items-center justify-center gap-2 font-medium transition-all active:scale-95 shadow-lg shadow-blue-900/20">
        <Plus :size="18" />
        打开会话
      </button>
    </div>

    <nav class="flex-1 px-4 py-4 space-y-2 overflow-y-auto custom-scrollbar">
      <router-link
        v-for="item in staticNavItems"
        :key="item.name"
        :to="item.to"
        :class="$route.path === item.to || (item.to !== '/' && $route.path.startsWith(item.to)) ? 'bg-blue-600 text-white shadow-md shadow-blue-900/20' : 'hover:bg-slate-800/50 hover:text-white'"
        class="flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-xl transition-all"
      >
        <component :is="resolveIconComponent(item.icon)" :size="20" />
        {{ item.label }}
      </router-link>

      <template v-if="managementTree.length > 0">
        <div class="pt-4 pb-2 px-4 text-xs font-bold text-slate-500 uppercase tracking-wider">管理中心</div>
        <ManagementMenuTree :nodes="managementTree" :level="0" :expanded="managementExpanded" @toggle="toggleManagementNode" />
      </template>

    </nav>

    <div class="p-4 border-t border-slate-800">
      <div class="bg-slate-800/50 rounded-xl p-3 flex items-center gap-3 group border border-transparent hover:border-slate-700 transition-all">
        <div
          @click="navigateTo('/profile')"
          :class="[
            'w-9 h-9 rounded-lg flex-shrink-0 flex items-center justify-center cursor-pointer shadow-lg overflow-hidden',
            avatarUrl
              ? 'bg-white'
              : `text-white font-bold bg-gradient-to-br from-slate-600 to-slate-700`
          ]"
        >
          <template v-if="avatarUrl">
            <img :src="avatarUrl" alt="Avatar" class="w-full h-full object-cover" />
          </template>
          <template v-else>
            {{ username ? username[0].toUpperCase() : 'U' }}
          </template>
        </div>
        
        <div class="flex-1 overflow-hidden">
          <div class="font-medium text-sm text-white truncate cursor-pointer hover:underline" @click="navigateTo('/profile')">
              {{ username }}
          </div>
          
          <div class="flex items-center gap-2">
              <span class="text-xs text-slate-500">
                  {{ isAdmin ? '管理员' :  '用户' }}
              </span>
          </div>
        </div>
        
        <div class="flex flex-col gap-1">
            <button @click="openHelp" class="text-slate-500 hover:text-white transition-colors" title="帮助中心">
              <HelpCircle :size="14" />
            </button>
            <button @click="handleLogout" class="text-slate-500 hover:text-red-400 transition-colors" title="退出">
              <LogOut :size="14" />
            </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import {computed, onMounted, ref, watch} from 'vue'
import {useRouter} from 'vue-router'
import {Crown, HelpCircle, LogOut, Plus} from 'lucide-vue-next'
import defaultLogo from '@/assets/logo.png'
import {useChatStore} from '../stores/chat'
import {useModelProviderStore} from '@/stores/modelProviders'
import {useRuntimeStore} from '@/stores/runtime'
import {MAX_SESSION_TABS, useTagsViewStore} from '@/stores/tagsView'
import {dialog} from '@/components/common/dialog'
import {useUserStore} from '@/stores/user'
import {message} from '@/components/common/message'
import {usePermissionStore} from '@/stores/permission'
import {useConfigStore} from '@/stores/config'
import ManagementMenuTree, {type ManagementMenuNode} from '@/components/common/ManagementMenuTree.vue'
import {getAgentCoverIconComponent} from '@/components/common/agentCover'
import {redirectToAppBase} from '@/utils/navigation'

const userStore = useUserStore()
const permissionStore = usePermissionStore()
const configStore = useConfigStore()
const chatStore = useChatStore('default')
const modelProviderStore = useModelProviderStore()
const tagsViewStore = useTagsViewStore()
const runtimeStore = useRuntimeStore()
const appTitle = computed(() => configStore.getConfigValue('sys_web_title', 'StarCityAI'))
const webLogo = computed(() => configStore.getConfigValue('sys_web_logo', defaultLogo))

// 定义组件属性

// 定义组件事件




// 计算属性 - 从 store 获取用户信息
const userInfo = computed(() => userStore.userInfo)
const isAdmin = computed(() => userInfo.value?.is_superuser || false)
const username = computed(() => userInfo.value?.username || userInfo.value?.name || 'User')
const avatarUrl = computed(() => userInfo.value?.avatar)
const resolveIconComponent = (icon?: string) => getAgentCoverIconComponent(icon)

type StaticNavItem = {
  name: string
  to: string
  label: string
  icon?: string
}

const staticNavDefaults: StaticNavItem[] = [
  { name: 'MySpace', to: '/', label: '我的空间', icon: 'compass' },
  { name: 'AgentSquare', to: '/agent-square', label: '智能体广场', icon: 'layout-grid' },
  //{ name: 'McpSquare', to: '/mcp', label: '工具', icon: 'box' },
  //{ name: 'SkillsSquare', to: '/skills', label: '技能', icon: 'wrench' }
]

const staticRouteChildren = computed(() => {
  const layoutRoute = permissionStore.routes.find((item) => item.path === '/')
  const children = Array.isArray(layoutRoute?.children) ? layoutRoute.children : []
  return children
})

const staticNavItems = computed<StaticNavItem[]>(() => {
  return staticNavDefaults.map((item) => {
    const matchedRoute = staticRouteChildren.value.find((route) => String(route.name || '') === item.name)
    const routePath = String(matchedRoute?.path || '')
    const to = routePath ? `/${routePath}`.replace(/\/{2,}/g, '/') : '/'
    return {
      name: item.name,
      to,
      label: String(matchedRoute?.meta?.title || item.label),
      icon: String(matchedRoute?.meta?.icon || item.icon || '').trim() || undefined
    }
  })
})

const reservedManagementRoots = new Set(['', '/', 'agent-square', 'mcp', 'skills', 'oh', 'chat', 'profile'])

const normalizeFullPath = (basePath: string, segment: string) => {
  if (String(segment || '').startsWith('/')) {
    return String(segment || '').replace(/\/{2,}/g, '/')
  }
  const seg = String(segment || '').replace(/^\/+/, '')
  const raw = seg ? `${basePath}/${seg}` : basePath || '/'
  return raw.replace(/\/{2,}/g, '/')
}

const buildManagementTree = (routes: any[], basePath: string, isTopLevel: boolean): ManagementMenuNode[] => {
  const list = Array.isArray(routes) ? [...routes] : []
  list.sort((a, b) => Number(a?.meta?.order ?? 0) - Number(b?.meta?.order ?? 0))
  const result: ManagementMenuNode[] = []
  list.forEach((route) => {
    const hidden = Boolean(route?.meta?.hidden)
    if (hidden) {
      return
    }
    const title = String(route?.meta?.title || route?.name || '').trim()
    if (!title) {
      return
    }
    const fullPath = normalizeFullPath(basePath, route?.path)
    const root = fullPath.replace(/^\//, '').split('/')[0] || ''
    if (isTopLevel && reservedManagementRoots.has(root)) {
      return
    }
    const children = buildManagementTree(route?.children || [], fullPath, false)
    const key = String(route?.name || fullPath)
    const icon = String(route?.meta?.icon || '').trim() || undefined
    result.push({
      key,
      title,
      path: fullPath,
      icon,
      children
    })
  })
  return result
}

const managementTree = computed(() => buildManagementTree(permissionStore.dynamicRoutes as any[], '', true))
const managementExpanded = ref<Record<string, boolean>>({})

watch(
  managementTree,
  (nodes) => {
    const next = { ...managementExpanded.value }
    nodes.forEach((node) => {
      if (next[node.key] === undefined) {
        next[node.key] = false
      }
    })
    managementExpanded.value = next
  },
  { immediate: true }
)

const toggleManagementNode = (key: string) => {
  managementExpanded.value = {
    ...managementExpanded.value,
    [key]: !managementExpanded.value[key]
  }
}

// 组件挂载时加载用户信息
onMounted(() => {
  Promise.resolve(configStore.getConfig()).catch(() => {})
  Promise.resolve(userStore.loadUser()).then(() => permissionStore.generateRoutes()).catch(() => {})
})

// Vue Router 实例
const router = useRouter()

// 导航方法
const navigateTo = (path: string) => {
  router.push(path)
}

const openHelp = () => {
  router.push({ name: 'Help' })
}

// 新建会话
const handleNewChat = async () => {
  console.log(import.meta.glob('/src/views/**/*.vue', { eager: true }));

  try {
    const guardResult = tagsViewStore.canOpenSessionTab('0')
    if (!guardResult.allowed) {
      if (guardResult.reason === 'duplicate') {
        await router.push(guardResult.existingView.fullPath)
      } else {
        message.warning(`最多只能开启 ${MAX_SESSION_TABS} 个会话页签`)
      }
      return
    }
    const defaultModel = modelProviderStore.getDefaultModel
    const conversationSettings = { agentId: '0', providerId: defaultModel?.providerId, modelId: defaultModel?.modelId }
    // 传入 newConversation: true 强制创建新会话，而不是返回已有会话
    const conversation = await chatStore.createConversation("新会话", conversationSettings, { newConversation: true })
    tagsViewStore.registerConversationAgent(conversation.id, '0')
    // 刷新会话列表
    // emit('refresh-sessions')
    await router.push(`/chat/${conversation.id}`)
  } catch (error: any) {
    console.error('Failed to create session:', error)
    message.error(error?.message || '创建会话失败，请稍后重试')
  }
}

// 退出登录
const handleLogout = async () => {
  try {
    await dialog.confirm("确定退出登录？")
    await userStore.loginOut()
    redirectToAppBase()
  } catch {
    // cancelled
  }
}
</script>
