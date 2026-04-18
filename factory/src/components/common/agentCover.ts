import type { Component } from 'vue'
import {
  LayoutGrid, Sparkles, Bot, MessageSquare, FileText, Globe, Mic, Server, Wrench,
  Brain, Cpu, Code2, PenTool, ChartBar, BookOpen, Calendar, Clock3, Mail, ShoppingCart,
  Briefcase, GraduationCap, LayoutDashboard, ChartNoAxesCombined,Heart, Image, Music2, Compass, Box, User, Users, Settings, Search, Bell, HelpCircle,
  ChartPie, ChartLine, CircuitBoard, Link, Menu, ShieldCheck, Database,
} from 'lucide-vue-next'

export type AgentCoverConfig = {
  icon?: string
  color?: string
}

export const DEFAULT_AGENT_COVER_ICON = 'layout-grid'
export const DEFAULT_AGENT_COVER_COLOR = '#2563EB'

export const AGENT_COVER_ICON_MAP = {
  'shield-check': ShieldCheck,
  'database': Database,
  'menu': Menu,
  'link': Link,
  'circuit-board': CircuitBoard,
  'chart-line': ChartLine,
  'chart-no-axes-combined': ChartNoAxesCombined,
  'chart-pie': ChartPie,
  'layout-grid': LayoutGrid,
  compass: Compass,
  'layout-dashboard': LayoutDashboard,
  box: Box,
  sparkles: Sparkles,
  bot: Bot,
  user: User,
  users: Users,
  settings: Settings,
  search: Search,
  bell: Bell,
  'help-circle': HelpCircle,
  'message-square': MessageSquare,
  'file-text': FileText,
  globe: Globe,
  mic: Mic,
  server: Server,
  wrench: Wrench,
  brain: Brain,
  cpu: Cpu,
  'code-2': Code2,
  'pen-tool': PenTool,
  'chart-bar': ChartBar,
  'book-open': BookOpen,
  calendar: Calendar,
  'clock-3': Clock3,
  mail: Mail,
  'shopping-cart': ShoppingCart,
  briefcase: Briefcase,
  'graduation-cap': GraduationCap,
  heart: Heart,
  image: Image,
  'music-2': Music2
} as const

export const AGENT_COVER_ICON_OPTIONS = [
  { id: 'layout-grid', label: '网格', component: LayoutGrid },
  { id: 'compass', label: '导航', component: Compass },
  { id: 'box', label: '盒子', component: Box },
  { id: 'sparkles', label: '灵感', component: Sparkles },
  { id: 'bot', label: '机器人', component: Bot },
  { id: 'user', label: '用户', component: User },
  { id: 'users', label: '团队', component: Users },
  { id: 'settings', label: '设置', component: Settings },
  { id: 'search', label: '检索', component: Search },
  { id: 'bell', label: '提醒', component: Bell },
  { id: 'help-circle', label: '帮助', component: HelpCircle },
  { id: 'message-square', label: '对话', component: MessageSquare },
  { id: 'file-text', label: '文档', component: FileText },
  { id: 'globe', label: '搜索', component: Globe },
  { id: 'mic', label: '语音', component: Mic },
  { id: 'server', label: '服务', component: Server },
  { id: 'wrench', label: '工具', component: Wrench },
  { id: 'brain', label: '思考', component: Brain },
  { id: 'cpu', label: '计算', component: Cpu },
  { id: 'code-2', label: '代码', component: Code2 },
  { id: 'pen-tool', label: '创作', component: PenTool },
  { id: 'chart-bar', label: '分析', component: ChartBar },
  { id: 'menu', label: '菜单', component: Menu },
  { id: 'book-open', label: '知识', component: BookOpen },
  { id: 'calendar', label: '日程', component: Calendar },
  { id: 'clock-3', label: '时间', component: Clock3 },
  { id: 'mail', label: '邮件', component: Mail },
  { id: 'shopping-cart', label: '电商', component: ShoppingCart },
  { id: 'briefcase', label: '商务', component: Briefcase },
  { id: 'graduation-cap', label: '教育', component: GraduationCap },
  { id: 'layout-dashboard', label: '看板', component: LayoutDashboard },
  { id: 'heart', label: '心', component: Heart },
  { id: 'image', label: '图片', component: Image },
  { id: 'music-2', label: '音乐', component: Music2 },
  { id: 'circuit-board', label: '线路', component: CircuitBoard },
  { id: 'chart-line', label: '线图', component: ChartLine },
  { id: 'chart-no-axes-combined', label: '图表', component: ChartNoAxesCombined },
  { id: 'chart-pie', label: '饼图', component: ChartPie },
  { id: 'link', label: '链接', component: Link },
  { id: 'database', label: '数据库', component: Database },
  { id: 'shield-check', label: '安全', component: ShieldCheck },
] as const

export const AGENT_COVER_COLOR_OPTIONS = [
  '#2563EB', // Blue 600 (默认，经典蓝)
  '#0EA5E9', // Sky 500 (明亮的天蓝)
  '#0F766E', // Teal 700 (深邃的青蓝)
  '#10B981', // Emerald 500 (明亮的翠绿)
  '#65A30D', // Lime 600 (偏暖的黄绿)
  '#D97706', // Amber 600 (沉稳的琥珀黄)
  '#F97316', // Orange 500 (活力的橙色)
  '#DC2626', // Red 600 (经典的正红)
  '#BE123C', // Rose 700 (深邃的玫瑰红)
  '#A855F7', // Purple 500 (明亮的紫色)
  '#4338CA', // Indigo 700 (深沉的靛蓝)
  '#475569'  // Slate 600 (中性的板岩灰)
]

export const parseAgentCover = (value?: string | AgentCoverConfig | null): AgentCoverConfig => {
  if (!value) return {}
  if (typeof value === 'string') {
    try {
      const parsed = JSON.parse(value)
      return typeof parsed === 'object' && parsed ? parsed : {}
    } catch {
      return {}
    }
  }
  return typeof value === 'object' ? value : {}
}

export const normalizeAgentCover = (value?: string | AgentCoverConfig | null) => {
  const parsed = parseAgentCover(value)
  return {
    icon: parsed.icon || DEFAULT_AGENT_COVER_ICON,
    color: parsed.color || DEFAULT_AGENT_COVER_COLOR
  }
}

const normalizeIconKey = (icon?: string) => {
  const raw = String(icon || '').trim()
  if (!raw) {
    return DEFAULT_AGENT_COVER_ICON
  }
  return raw
    .replace(/([a-z0-9])([A-Z])/g, '$1-$2')
    .replace(/^el-icon-/i, '')
    .replace(/^lucide:/i, '')
    .replace(/_+/g, '-')
    .replace(/-icon$/i, '')
    .toLowerCase()
}

export const getAgentCoverIconComponent = (icon?: string): Component => {
  const iconKey = normalizeIconKey(icon)
  return AGENT_COVER_ICON_MAP[iconKey as keyof typeof AGENT_COVER_ICON_MAP] || LayoutGrid
}

export const stringifyAgentCover = (value: AgentCoverConfig) =>
  JSON.stringify({
    icon: value.icon || DEFAULT_AGENT_COVER_ICON,
    color: value.color || DEFAULT_AGENT_COVER_COLOR
  })
