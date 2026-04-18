<template>
  <div class="min-h-screen bg-slate-50 p-8 overflow-y-auto">
    <div class="max-w-6xl mx-auto">
      <!-- 页面标题 -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">Token 统计报表</h1>
          <p class="mt-1 text-sm text-slate-500">查看系统 Token 消耗趋势与统计排行。</p>
        </div>
      </div>

      <!-- 查询条件 -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 mb-6 overflow-hidden">
        <div class="p-6">
          <div class="flex flex-wrap items-center gap-5">
            <!-- 日期范围 -->
            <div class="flex items-center gap-2">
              <CalendarIcon class="w-4 h-4 text-slate-400" />
              <div class="flex items-center gap-2">
                <input
                  v-model="startDate"
                  type="date"
                  class="px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-4 focus:ring-indigo-50 focus:border-indigo-400 transition-all"
                  :disabled="loading"
                />
                <span class="text-slate-400">至</span>
                <input
                  v-model="endDate"
                  type="date"
                  class="px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-4 focus:ring-indigo-50 focus:border-indigo-400 transition-all"
                  :disabled="loading"
                />
              </div>
            </div>

            <!-- 部门筛选 -->
            <div class="flex items-center gap-2">
              <Building2Icon class="w-4 h-4 text-slate-400" />
              <select
                v-model="filters.dept_id"
                class="px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-4 focus:ring-indigo-50 focus:border-indigo-400 transition-all cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed appearance-none"
                :disabled="loading"
              >
                <option :value="undefined">所有部门</option>
                <option v-for="dept in deptList" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
              </select>
            </div>

            <!-- 岗位筛选 -->
            <div class="flex items-center gap-2">
              <BriefcaseIcon class="w-4 h-4 text-slate-400" />
              <select
                v-model="filters.position_id"
                class="px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-4 focus:ring-indigo-50 focus:border-indigo-400 transition-all cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed appearance-none"
                :disabled="loading"
              >
                <option :value="undefined">所有岗位</option>
                <option v-for="pos in positionList" :key="pos.id" :value="pos.id">{{ pos.name }}</option>
              </select>
            </div>

            <!-- 搜索按钮 -->
            <button
              @click="handleSearch"
              class="ml-auto px-6 py-2.5 bg-slate-900 text-white text-sm font-bold rounded-xl hover:bg-slate-800 transition-all shadow-sm hover:shadow flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="loading"
            >
              <SearchIcon class="w-4 h-4" />
              查询
            </button>
          </div>
        </div>
      </div>

      <!-- 统计卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-6">
        <!-- 总Token消耗 -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 flex items-center gap-4">
          <div class="w-14 h-14 rounded-xl bg-indigo-50 flex items-center justify-center flex-shrink-0">
            <TrendingUpIcon class="w-7 h-7 text-indigo-600" />
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm text-slate-500 mb-0.5">总 Token 消耗</p>
            <p class="text-2xl font-bold text-slate-900">{{ formatNumber(overviewData.total_tokens) }} <span class="text-sm font-normal text-slate-400">Tokens</span></p>
          </div>
        </div>

        <!-- 总对话数 -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 flex items-center gap-4">
          <div class="w-14 h-14 rounded-xl bg-emerald-50 flex items-center justify-center flex-shrink-0">
            <MessageSquareIcon class="w-7 h-7 text-emerald-600" />
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm text-slate-500 mb-0.5">对话总数</p>
            <p class="text-2xl font-bold text-slate-900">{{ formatNumber(overviewData.total_chats) }} <span class="text-sm font-normal text-slate-400">次对话</span></p>
          </div>
        </div>

        <!-- 活跃智能体 -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 flex items-center gap-4">
          <div class="w-14 h-14 rounded-xl bg-amber-50 flex items-center justify-center flex-shrink-0">
            <BotIcon class="w-7 h-7 text-amber-600" />
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm text-slate-500 mb-0.5">活跃智能体</p>
            <p class="text-2xl font-bold text-slate-900">{{ overviewData.active_agents }} <span class="text-sm font-normal text-slate-400">Agents</span></p>
          </div>
        </div>

        <!-- 活跃用户数 -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 flex items-center gap-4">
          <div class="w-14 h-14 rounded-xl bg-rose-50 flex items-center justify-center flex-shrink-0">
            <UsersIcon class="w-7 h-7 text-rose-600" />
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm text-slate-500 mb-0.5">活跃用户数</p>
            <p class="text-2xl font-bold text-slate-900">{{ overviewData.active_users }} <span class="text-sm font-normal text-slate-400">Users</span></p>
          </div>
        </div>
      </div>

      <!-- 图表区域 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Token消耗趋势分析 -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-1 h-4 bg-indigo-500 rounded-full"></div>
            <h3 class="font-semibold text-slate-900">Token 消耗趋势分析 (每日)</h3>
          </div>
          <div v-if="loading" class="h-72 flex items-center justify-center">
            <div class="flex flex-col items-center gap-3">
              <div class="w-8 h-8 border-3 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
              <span class="text-sm text-slate-400">加载中...</span>
            </div>
          </div>
          <div v-else ref="tokenTrendChartRef" class="h-72"></div>
        </div>

        <!-- 对话趋势分析 -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-1 h-4 bg-emerald-500 rounded-full"></div>
            <h3 class="font-semibold text-slate-900">对话趋势分析 (每日)</h3>
          </div>
          <div v-if="loading" class="h-72 flex items-center justify-center">
            <div class="flex flex-col items-center gap-3">
              <div class="w-8 h-8 border-3 border-emerald-200 border-t-emerald-600 rounded-full animate-spin"></div>
              <span class="text-sm text-slate-400">加载中...</span>
            </div>
          </div>
          <div v-else ref="chatTrendChartRef" class="h-72"></div>
        </div>

        <!-- 部门消耗排行 -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-1 h-4 bg-indigo-500 rounded-full"></div>
            <h3 class="font-semibold text-slate-900">部门消耗排行 (Top 5)</h3>
          </div>
          <div v-if="loading" class="h-72 flex items-center justify-center">
            <div class="flex flex-col items-center gap-3">
              <div class="w-8 h-8 border-3 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
              <span class="text-sm text-slate-400">加载中...</span>
            </div>
          </div>
          <div v-else ref="deptRankChartRef" class="h-72"></div>
        </div>

        <!-- 个人消耗排行 -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-1 h-4 bg-indigo-500 rounded-full"></div>
            <h3 class="font-semibold text-slate-900">个人消耗排行 (Top 5)</h3>
          </div>
          <div v-if="loading" class="h-72 flex items-center justify-center">
            <div class="flex flex-col items-center gap-3">
              <div class="w-8 h-8 border-3 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
              <span class="text-sm text-slate-400">加载中...</span>
            </div>
          </div>
          <div v-else ref="userRankChartRef" class="h-72"></div>
        </div>

        <!-- 模型消耗占比 -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-1 h-4 bg-indigo-500 rounded-full"></div>
            <h3 class="font-semibold text-slate-900">模型消耗占比</h3>
          </div>
          <div v-if="loading" class="h-72 flex items-center justify-center">
            <div class="flex flex-col items-center gap-3">
              <div class="w-8 h-8 border-3 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
              <span class="text-sm text-slate-400">加载中...</span>
            </div>
          </div>
          <div v-else ref="modelPieChartRef" class="h-72"></div>
        </div>

        <!-- 智能体消耗排名 -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-1 h-4 bg-indigo-500 rounded-full"></div>
            <h3 class="font-semibold text-slate-900">智能体消耗排名</h3>
          </div>
          <div v-if="loading" class="h-72 flex items-center justify-center">
            <div class="flex flex-col items-center gap-3">
              <div class="w-8 h-8 border-3 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
              <span class="text-sm text-slate-400">加载中...</span>
            </div>
          </div>
          <div v-else ref="agentRankChartRef" class="h-72"></div>
        </div>
      </div>

      <!-- 详细消耗明细 -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-2">
            <SearchIcon class="w-4 h-4 text-slate-400" />
            <h3 class="font-semibold text-slate-900">详细消耗明细</h3>
          </div>
          <span class="text-xs text-slate-400">显示最近 10 条记录</span>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="py-12 text-center">
          <div class="inline-block w-6 h-6 border-2 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
          <p class="text-sm text-slate-400 mt-2">加载中...</p>
        </div>

        <!-- 数据表格 -->
        <div v-else class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-slate-100">
                <th class="px-4 py-3 text-left text-sm font-medium text-slate-500">时间</th>
                <th class="px-4 py-3 text-left text-sm font-medium text-slate-500">部门</th>
                <th class="px-4 py-3 text-left text-sm font-medium text-slate-500">姓名</th>
                <th class="px-4 py-3 text-left text-sm font-medium text-slate-500">智能体</th>
                <th class="px-4 py-3 text-left text-sm font-medium text-slate-500">岗位</th>
                <th class="px-4 py-3 text-right text-sm font-medium text-slate-500">消耗 (Tokens)</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(row, index) in detailData"
                :key="index"
                class="border-b border-slate-50 hover:bg-slate-50/50 transition-colors"
              >
                <td class="px-4 py-3 text-sm text-slate-600">{{ row.date }}</td>
                <td class="px-4 py-3">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-50 text-indigo-700">
                    {{ row.dept_name }}
                  </span>
                </td>
                <td class="px-4 py-3 text-sm text-slate-900">{{ row.user_name }}</td>
                <td class="px-4 py-3">
                  <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                    <span class="text-sm text-slate-700">{{ row.agent_name || '-' }}</span>
                  </div>
                </td>
                <td class="px-4 py-3 text-sm text-slate-600">{{ row.position_name }}</td>
                <td class="px-4 py-3 text-sm font-medium text-slate-900 text-right">{{ formatNumber(row.tokens) }}</td>
              </tr>
              <tr v-if="detailData.length === 0">
                <td colspan="6" class="px-4 py-12 text-center text-sm text-slate-400">
                  暂无数据
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue'
import {
  CalendarIcon,
  Building2Icon,
  BriefcaseIcon,
  TrendingUpIcon,
  MessageSquareIcon,
  BotIcon,
  UsersIcon,
  SearchIcon
} from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import AiChatTokenStatsAPI from '@/services/fastApi/module_ai/ai_chat_token_stats'
import type {
  TokenStatsQuery,
  TokenOverviewOut,
  TokenTrendItem,
  ChatTrendItem,
  DeptTokenRankItem,
  UserTokenRankItem,
  AgentTokenRankItem,
  ModelConsumptionItem,
  UserTokenDetailItem
} from '@/services/fastApi/module_ai/ai_chat_token_stats'
import DeptAPI from '@/services/fastApi/module_system/dept'
import PositionAPI from '@/services/fastApi/module_system/position'

// 路由
const router = useRouter()

// 加载状态
const loading = ref(false)

// 日期范围（使用原生 date input，格式为 YYYY-MM-DD）
const startDate = ref('')
const endDate = ref('')

// 筛选条件
const filters = reactive<TokenStatsQuery>({
  start_date: '',
  end_date: '',
  dept_id: undefined,
  position_id: undefined,
  page_no: 1,
  page_size: 10
})

// 部门列表
const deptList = ref<{ id: number; name: string }[]>([])
// 岗位列表
const positionList = ref<{ id: number; name: string }[]>([])

// 统计数据
const overviewData = ref<TokenOverviewOut>({
  total_tokens: 0,
  total_chats: 0,
  active_agents: 0,
  active_users: 0
})

// 图表数据
const tokenTrendData = ref<TokenTrendItem[]>([])
const chatTrendData = ref<ChatTrendItem[]>([])
const deptRankData = ref<DeptTokenRankItem[]>([])
const userRankData = ref<UserTokenRankItem[]>([])
const agentRankData = ref<AgentTokenRankItem[]>([])
const modelConsumptionData = ref<ModelConsumptionItem[]>([])
const detailData = ref<UserTokenDetailItem[]>([])

// 图表引用
const tokenTrendChartRef = ref<HTMLElement>()
const chatTrendChartRef = ref<HTMLElement>()
const deptRankChartRef = ref<HTMLElement>()
const userRankChartRef = ref<HTMLElement>()
const modelPieChartRef = ref<HTMLElement>()
const agentRankChartRef = ref<HTMLElement>()

// ECharts 实例
let tokenTrendChartInstance: echarts.ECharts | null = null
let chatTrendChartInstance: echarts.ECharts | null = null
let deptRankChartInstance: echarts.ECharts | null = null
let userRankChartInstance: echarts.ECharts | null = null
let modelPieChartInstance: echarts.ECharts | null = null
let agentRankChartInstance: echarts.ECharts | null = null

// 格式化数字
const formatNumber = (num: number): string => {
  if (!num) return '0'
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toLocaleString()
}

// 格式化日期为 YYYY-MM-DD
const formatDate = (date: Date): string => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 处理搜索
const handleSearch = () => {
  if (startDate.value && endDate.value) {
    filters.start_date = startDate.value
    filters.end_date = endDate.value
    loadData()
  }
}

// 加载筛选选项
const loadFilterOptions = async () => {
  try {
    // 加载部门列表
    const deptRes = await DeptAPI.listDept()
    if (deptRes.data?.data) {
      const flattenDepts = (depts: any[], prefix = ''): { id: number; name: string }[] => {
        const result: { id: number; name: string }[] = []
        for (const dept of depts) {
          if (dept.id && dept.name) {
            result.push({ id: dept.id, name: prefix + dept.name })
          }
          if (dept.children && dept.children.length > 0) {
            result.push(...flattenDepts(dept.children, prefix + '　'))
          }
        }
        return result
      }
      deptList.value = flattenDepts(deptRes.data.data)
    }

    // 加载岗位列表
    const positionRes = await PositionAPI.listPosition({ page_no: 1, page_size: 100 })
    if (positionRes.data?.data?.items) {
      positionList.value = positionRes.data.data.items.map((item: any) => ({
        id: item.id,
        name: item.name
      }))
    }
  } catch (error) {
    console.error('加载筛选选项失败:', error)
  }
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    // 并行加载所有数据
    const [
      overviewRes,
      tokenTrendRes,
      chatTrendRes,
      deptRankRes,
      userRankRes,
      agentRankRes,
      modelConsumptionRes,
      detailRes
    ] = await Promise.all([
      // 统计概览
      AiChatTokenStatsAPI.getTokenOverview(filters),
      // Token趋势
      AiChatTokenStatsAPI.getTokenTrend(filters),
      // 对话趋势
      AiChatTokenStatsAPI.getChatTrend(filters),
      // 部门排名
      AiChatTokenStatsAPI.getDeptTokenRank({ ...filters, page_size: 5 }),
      // 人员排名
      AiChatTokenStatsAPI.getUserTokenRank({ ...filters, page_size: 5 }),
      // 智能体排名
      AiChatTokenStatsAPI.getAgentTokenRank({ ...filters, page_size: 5 }),
      // 模型消耗占比
      AiChatTokenStatsAPI.getModelConsumption(filters),
      // 明细数据
      AiChatTokenStatsAPI.getUserTokenDetail({ ...filters, page_size: 10 })
    ])

    // 更新数据
    overviewData.value = overviewRes.data?.data || {
      total_tokens: 0,
      total_chats: 0,
      active_agents: 0,
      active_users: 0
    }
    tokenTrendData.value = tokenTrendRes.data?.data?.items || []
    chatTrendData.value = chatTrendRes.data?.data?.items || []
    deptRankData.value = deptRankRes.data?.data?.items || []
    userRankData.value = userRankRes.data?.data?.items || []
    agentRankData.value = agentRankRes.data?.data?.items || []
    modelConsumptionData.value = modelConsumptionRes.data?.data?.items || []
    detailData.value = detailRes.data?.data?.items || []

    // 渲染图表
    await nextTick()
    setTimeout(() => {
      renderTokenTrendChart()
      renderChatTrendChart()
      renderDeptRankChart()
      renderUserRankChart()
      renderModelPieChart()
      renderAgentRankChart()
    }, 100)
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 渲染Token趋势图
const renderTokenTrendChart = () => {
  if (!tokenTrendChartRef.value) return

  if (tokenTrendChartInstance) {
    tokenTrendChartInstance.dispose()
  }
  tokenTrendChartInstance = echarts.init(tokenTrendChartRef.value)

  const dates = tokenTrendData.value.map(item => {
    const date = item.date
    if (date.includes(' ')) {
      return date.split(' ')[0].slice(5)
    }
    return date.slice(5)
  })
  const values = tokenTrendData.value.map(item => item.total_tokens)

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        const p = params[0]
        return `${p.name}<br/>Token消耗: ${formatNumber(p.value)}`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates,
      axisLine: { lineStyle: { color: '#e5e7eb' } },
      axisLabel: { color: '#9ca3af', fontSize: 11 }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: '#9ca3af',
        fontSize: 11,
        formatter: (value: number): string => {
          if (value >= 1000) return (value / 1000).toFixed(0) + 'k'
          return String(value)
        }
      },
      splitLine: { lineStyle: { color: '#f3f4f6' } }
    },
    series: [{
      name: 'Token消耗',
      type: 'line',
      smooth: true,
      symbol: 'none',
      lineStyle: {
        color: '#6366f1',
        width: 2
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(99, 102, 241, 0.2)' },
          { offset: 1, color: 'rgba(99, 102, 241, 0)' }
        ])
      },
      data: values
    }]
  }

  tokenTrendChartInstance.setOption(option)
}

// 渲染对话趋势图
const renderChatTrendChart = () => {
  if (!chatTrendChartRef.value) return

  if (chatTrendChartInstance) {
    chatTrendChartInstance.dispose()
  }
  chatTrendChartInstance = echarts.init(chatTrendChartRef.value)

  const dates = chatTrendData.value.map(item => {
    const date = item.date
    if (date.includes(' ')) {
      return date.split(' ')[0].slice(5)
    }
    return date.slice(5)
  })
  const values = chatTrendData.value.map(item => item.chat_count)

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        const p = params[0]
        return `${p.name}<br/>对话次数: ${p.value}`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates,
      axisLine: { lineStyle: { color: '#e5e7eb' } },
      axisLabel: { color: '#9ca3af', fontSize: 11 }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { color: '#9ca3af', fontSize: 11 },
      splitLine: { lineStyle: { color: '#f3f4f6' } }
    },
    series: [{
      name: '对话次数',
      type: 'line',
      smooth: true,
      symbol: 'none',
      lineStyle: {
        color: '#10b981',
        width: 2
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(16, 185, 129, 0.2)' },
          { offset: 1, color: 'rgba(16, 185, 129, 0)' }
        ])
      },
      data: values
    }]
  }

  chatTrendChartInstance.setOption(option)
}

// 渲染部门排名图
const renderDeptRankChart = () => {
  if (!deptRankChartRef.value) return

  if (deptRankChartInstance) {
    deptRankChartInstance.dispose()
  }
  deptRankChartInstance = echarts.init(deptRankChartRef.value)

  const data = deptRankData.value.slice(0, 5).reverse()
  const names = data.map(item => item.dept_name)
  const values = data.map(item => item.total_tokens)

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: (params: any) => {
        const p = params[0]
        return `${p.name}<br/>Token消耗: ${formatNumber(p.value)}`
      }
    },
    grid: {
      left: '3%',
      right: '8%',
      bottom: '3%',
      top: '5%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { show: false },
      splitLine: { show: false }
    },
    yAxis: {
      type: 'category',
      data: names,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { color: '#6b7280', fontSize: 12 }
    },
    series: [{
      name: 'Token消耗',
      type: 'bar',
      barWidth: 20,
      data: values,
      itemStyle: {
        color: '#6366f1',
        borderRadius: [0, 4, 4, 0]
      },
      label: {
        show: true,
        position: 'right',
        formatter: (params: any) => formatNumber(params.value),
        color: '#6b7280',
        fontSize: 11
      }
    }]
  }

  deptRankChartInstance.setOption(option)
}

// 渲染个人排名图
const renderUserRankChart = () => {
  if (!userRankChartRef.value) return

  if (userRankChartInstance) {
    userRankChartInstance.dispose()
  }
  userRankChartInstance = echarts.init(userRankChartRef.value)

  const data = userRankData.value.slice(0, 5).reverse()
  const names = data.map(item => item.user_name)
  const values = data.map(item => item.total_tokens)

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: (params: any) => {
        const p = params[0]
        return `${p.name}<br/>Token消耗: ${formatNumber(p.value)}`
      }
    },
    grid: {
      left: '3%',
      right: '8%',
      bottom: '3%',
      top: '5%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { show: false },
      splitLine: { show: false }
    },
    yAxis: {
      type: 'category',
      data: names,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { color: '#6b7280', fontSize: 12 }
    },
    series: [{
      name: 'Token消耗',
      type: 'bar',
      barWidth: 20,
      data: values,
      itemStyle: {
        color: '#8b5cf6',
        borderRadius: [0, 4, 4, 0]
      },
      label: {
        show: true,
        position: 'right',
        formatter: (params: any) => formatNumber(params.value),
        color: '#6b7280',
        fontSize: 11
      }
    }]
  }

  userRankChartInstance.setOption(option)
}

// 渲染模型占比饼图
const renderModelPieChart = () => {
  if (!modelPieChartRef.value) return

  if (modelPieChartInstance) {
    modelPieChartInstance.dispose()
  }
  modelPieChartInstance = echarts.init(modelPieChartRef.value)

  const colors = ['#f87171', '#10b981', '#6366f1', '#f59e0b', '#8b5cf6', '#ec4899']
  const data = modelConsumptionData.value.map((item, index) => ({
    name: item.model_name,
    value: item.tokens,
    itemStyle: { color: colors[index % colors.length] }
  }))

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        return `${params.name}<br/>Token消耗: ${formatNumber(params.value)}<br/>占比: ${params.percent}%`
      }
    },
    legend: {
      orient: 'horizontal',
      bottom: 0,
      icon: 'circle',
      itemWidth: 8,
      itemHeight: 8,
      textStyle: { color: '#6b7280', fontSize: 11 }
    },
    series: [{
      name: '模型消耗',
      type: 'pie',
      radius: ['45%', '70%'],
      center: ['50%', '45%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 6,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 14,
          fontWeight: 'bold'
        }
      },
      labelLine: { show: false },
      data: data
    }]
  }

  modelPieChartInstance.setOption(option)
}

// 渲染智能体排名图
const renderAgentRankChart = () => {
  if (!agentRankChartRef.value) return

  if (agentRankChartInstance) {
    agentRankChartInstance.dispose()
  }
  agentRankChartInstance = echarts.init(agentRankChartRef.value)

  const data = agentRankData.value.slice(0, 5)
  const names = data.map(item => item.agent_name)
  const values = data.map(item => item.total_tokens)

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: (params: any) => {
        const p = params[0]
        return `${p.name}<br/>Token消耗: ${formatNumber(p.value)}`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: names,
      axisLine: { lineStyle: { color: '#e5e7eb' } },
      axisLabel: {
        color: '#6b7280',
        fontSize: 11,
        interval: 0,
        formatter: (value: string) => {
          if (value.length > 8) {
            return value.substring(0, 8) + '...'
          }
          return value
        }
      },
      axisTick: { show: false }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: '#9ca3af',
        fontSize: 11,
        formatter: (value: number): string => {
          if (value >= 1000) return (value / 1000).toFixed(0) + 'k'
          return String(value)
        }
      },
      splitLine: { lineStyle: { color: '#f3f4f6' } }
    },
    series: [{
      name: 'Token消耗',
      type: 'bar',
      barWidth: 32,
      data: values,
      itemStyle: {
        color: '#6366f1',
        borderRadius: [4, 4, 0, 0]
      }
    }]
  }

  agentRankChartInstance.setOption(option)
}

// 监听窗口大小变化
const handleResize = () => {
  tokenTrendChartInstance?.resize()
  chatTrendChartInstance?.resize()
  deptRankChartInstance?.resize()
  userRankChartInstance?.resize()
  modelPieChartInstance?.resize()
  agentRankChartInstance?.resize()
}

// 初始化
onMounted(() => {
  loadFilterOptions()
  // 设置默认日期范围（最近一周）
  const end = new Date()
  const start = new Date()
  start.setDate(start.getDate() - 6)
  startDate.value = formatDate(start)
  endDate.value = formatDate(end)
  filters.start_date = startDate.value
  filters.end_date = endDate.value
  loadData()
  window.addEventListener('resize', handleResize)
})

// 清理
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  tokenTrendChartInstance?.dispose()
  chatTrendChartInstance?.dispose()
  deptRankChartInstance?.dispose()
  userRankChartInstance?.dispose()
  modelPieChartInstance?.dispose()
  agentRankChartInstance?.dispose()
})
</script>

<style scoped>
/* 日期输入框样式 */
input[type="date"] {
  font-family: inherit;
}

input[type="date"]::-webkit-calendar-picker-indicator {
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.2s;
}

input[type="date"]::-webkit-calendar-picker-indicator:hover {
  opacity: 1;
}

/* select 下拉框样式 */
select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%236b7280' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 8px center;
  background-size: 16px;
  padding-right: 32px;
}

select:focus {
  outline: none;
}
</style>
