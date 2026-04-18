<template>
  <div class="h-full flex flex-col bg-gray-50 overflow-hidden relative">
    <!-- 顶部导航栏 -->
    <div class="px-8 py-6 bg-slate-50 border-b border-gray-100 flex-shrink-0">
      <div class="max-w-6xl mx-auto flex flex-col md:flex-row gap-4 items-center justify-between">
        <div class="w-full md:w-auto flex-shrink-0">
          <h1 class="text-2xl font-bold text-slate-900">系统概况</h1>
          <p class="mt-1 text-sm text-slate-500">全局监控与系统配置中心</p>
        </div>
      </div>
    </div>

    <!-- 内容区 -->
    <div class="flex-1 overflow-y-auto p-8">
      <div class="max-w-6xl mx-auto">
        <!-- 统计卡片 - 改为可点击按钮 -->
        <div v-if="loading" class="text-center py-10">
          <div class="text-slate-400">加载统计数据...</div>
        </div>
        <div v-else-if="stats" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
        <!-- 总用户数 - 点击进入用户管理 -->
        <button @click="navigateTo('/system/user')" class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex items-center gap-4 hover:shadow-md hover:border-blue-200 transition-all text-left">
          <div class="w-14 h-14 rounded-xl bg-blue-50 flex items-center justify-center flex-shrink-0">
            <Users class="w-7 h-7 text-blue-500" />
          </div>
          <div>
            <div class="text-sm text-slate-500 mb-1">用户数</div>
            <div class="text-2xl font-bold text-slate-900">{{ stats.user_count }}</div>
          </div>
        </button>

        <!-- 部门数 - 点击进入部门管理 -->
        <button @click="navigateTo('/system/dept')" class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex items-center gap-4 hover:shadow-md hover:border-emerald-200 transition-all text-left">
          <div class="w-14 h-14 rounded-xl bg-emerald-50 flex items-center justify-center flex-shrink-0">
            <Building class="w-7 h-7 text-emerald-500" />
          </div>
          <div>
            <div class="text-sm text-slate-500 mb-1">部门数</div>
            <div class="text-2xl font-bold text-slate-900">{{ stats.dept_count }}</div>
          </div>
        </button>

        <!-- 角色数 - 点击进入角色管理 -->
        <button @click="navigateTo('/system/role')" class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex items-center gap-4 hover:shadow-md hover:border-amber-200 transition-all text-left">
          <div class="w-14 h-14 rounded-xl bg-amber-50 flex items-center justify-center flex-shrink-0">
            <UserCog class="w-7 h-7 text-amber-500" />
          </div>
          <div>
            <div class="text-sm text-slate-500 mb-1">角色数</div>
            <div class="text-2xl font-bold text-slate-900">{{ stats.role_count }}</div>
          </div>
        </button>

        <!-- 智能体数 - 进入智能体 -->
        <button @click="navigateTo('/agent-square')" class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex items-center gap-4 hover:shadow-md hover:border-purple-200 transition-all text-left">
          <div class="w-14 h-14 rounded-xl bg-purple-50 flex items-center justify-center flex-shrink-0">
            <Bot class="w-7 h-7 text-purple-500" />
          </div>
          <div>
            <div class="text-sm text-slate-500 mb-1">智能体数</div>
            <div class="text-2xl font-bold text-slate-900">{{ stats.agent_count }}</div>
          </div>
        </button>

        <!-- 对话数 - 进入最近对话的第一条 -->
        <button class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex items-center gap-4 hover:shadow-md hover:border-cyan-200 transition-all text-left">
          <div class="w-14 h-14 rounded-xl bg-cyan-50 flex items-center justify-center flex-shrink-0">
            <MessageSquare class="w-7 h-7 text-cyan-500" />
          </div>
          <div>
            <div class="text-sm text-slate-500 mb-1">会话数</div>
            <div class="text-2xl font-bold text-slate-900">{{ stats.chat_count }}</div>
          </div>
        </button>

        <!-- 消息数 - 暂不跳转 -->
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex items-center gap-4">
          <div class="w-14 h-14 rounded-xl bg-rose-50 flex items-center justify-center flex-shrink-0">
            <Activity class="w-7 h-7 text-rose-500" />
          </div>
          <div>
            <div class="text-sm text-slate-500 mb-1">消息数</div>
            <div class="text-2xl font-bold text-slate-900">{{ stats.msg_count }}</div>
          </div>
        </div>

        <!-- 岗位数 - 点击进入岗位管理 -->
        <button @click="navigateTo('/system/position')" class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex items-center gap-4 hover:shadow-md hover:border-indigo-200 transition-all text-left">
          <div class="w-14 h-14 rounded-xl bg-indigo-50 flex items-center justify-center flex-shrink-0">
            <Layers class="w-7 h-7 text-indigo-500" />
          </div>
          <div>
            <div class="text-sm text-slate-500 mb-1">岗位数</div>
            <div class="text-2xl font-bold text-slate-900">{{ stats.position_count || 0 }}</div>
          </div>
        </button>

        <!-- MCP数 - 暂不跳转 -->
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex items-center gap-4">
          <div class="w-14 h-14 rounded-xl bg-orange-50 flex items-center justify-center flex-shrink-0">
            <McpIcon class="w-7 h-7 text-orange-500" />
          </div>
          <div>
            <div class="text-sm text-slate-500 mb-1">MCP数</div>
            <div class="text-2xl font-bold text-slate-900">{{ stats.mcp_count || 0 }}</div>
          </div>
        </div>

        <!-- 累计Token - 点击进入Token分析 -->
        <button @click="navigateTo('/admin/token-analysis')" class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex items-center gap-4 hover:shadow-md hover:border-teal-200 transition-all text-left">
          <div class="w-14 h-14 rounded-xl bg-teal-50 flex items-center justify-center flex-shrink-0">
            <Coins class="w-7 h-7 text-teal-500" />
          </div>
          <div>
            <div class="text-sm text-slate-500 mb-1">累计Token</div>
            <div class="text-2xl font-bold text-slate-900">{{ formatNumber(stats.total_tokens || 0) }}</div>
          </div>
        </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  Users, Bot, MessageSquare, Activity,
  UserCog, Building, Cpu,
  Layers, Cpu as McpIcon, Coins,
  BookOpen as DictIcon, KeyRound
} from 'lucide-vue-next'
import { chatApi } from '@/services/api/chat'
import type { AiChatStats } from '@/services/fastApi/module_ai/ai_chat'
import { useUserStore } from '@/stores/user'
import { usePermissionStore } from '@/stores/permission'
import { message } from '@/components/common/message'

const router = useRouter()
const userStore = useUserStore()
const permissionStore = usePermissionStore()
const CATCH_ALL_ROUTE_PATH = '/:pathMatch(.*)*'

const syncDynamicRoutesToRouter = () => {
  permissionStore.dynamicRoutes.forEach((route) => {
    if (typeof route.name === 'string' && !router.hasRoute(route.name)) {
      router.addRoute(route)
    }
  })
}

const ensureDynamicRoutesReady = async () => {
  if (!userStore.hasGetRoute) {
    await userStore.loadUser()
  }
  if (permissionStore.isRouteGenerated) {
    syncDynamicRoutesToRouter()
    return
  }
  await permissionStore.generateRoutes()
  syncDynamicRoutesToRouter()
}

const hasRoutePermission = async (path: string) => {
  await ensureDynamicRoutesReady()
  const resolved = router.resolve(path)
  if (resolved.matched.length === 0) {
    return false
  }
  return !resolved.matched.some((record) => record.path === CATCH_ALL_ROUTE_PATH || record.name === 'NotFound')
}

const navigateTo = async (path: string) => {
  const hasPermission = await hasRoutePermission(path)
  if (!hasPermission) {
    // message.warning('当前账号没有该页面访问权限')
    return
  }
  await router.push(path)
}

const formatNumber = (num: number): string => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

// 响应式数据
const stats = ref<AiChatStats | null>(null)
const loading = ref(true)

// 加载数据
const loadData = async () => {
  try {
    loading.value = true
    
    // 获取统计数据
    const res = await chatApi.getStats()
    if (res) {
      stats.value = res
    }
  } catch (err) {
    console.error('加载数据失败:', err)
    // 如果是未授权错误，跳转到登录页
    if (err instanceof Error && err.message.includes('Unauthorized')) {
      router.push('/login')
    }
  } finally {
    loading.value = false
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadData()
})
</script>
