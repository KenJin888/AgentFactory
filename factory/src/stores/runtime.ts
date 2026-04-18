import { defineStore } from 'pinia'
import { CrossMessage } from '@/utils/crossMessage'

export type RuntimeEnv = {
  appName: string
  appId: string
  windowId: number
  tabId: number
}

// 页面 嵌入运行 页面智能体
export type RunMode = 'Web' | 'Embed' | 'WebAgent'

const initialEnv: RuntimeEnv = {
  appName: '',
  appId: '',
  windowId: 0,
  tabId: 0
}

export const useRuntimeStore = defineStore('runtime', {
  state: () => ({
    env: { ...initialEnv } as RuntimeEnv,
    runMode: 'Web' as RunMode}),
  actions: {
    updateEnv(payload: Partial<RuntimeEnv>) {
      this.env = { ...this.env, ...payload }
    },
    async initEnv() {
      if (typeof window === 'undefined') return false
      const routePath = (window.location.hash || "#/")
        .replace(/^#/, "")
        .split("?")[0];
      if (/^\/agent\/\d+$/.test(routePath)) {
        this.runMode = "WebAgent";
        return true;
      }
      if (window.parent === window) return false

      // 判断是否嵌入运行
      const response = await CrossMessage.request('INIT_APP')
      const payload = response && typeof response === 'object' ? (response as any) : null
      const nextEnv: Partial<RuntimeEnv> = {}
      if (payload && typeof payload === 'object') {
        if (typeof payload.appName === 'string') nextEnv.appName = payload.appName
        if (typeof payload.appId === 'string') nextEnv.appId = payload.appId
        if (typeof payload.windowId === 'number') nextEnv.windowId = payload.windowId
        if (typeof payload.tabId === 'number') nextEnv.tabId = payload.tabId
      }
      if (Object.keys(nextEnv).length > 0) {
        this.updateEnv(nextEnv)
        this.runMode = 'Embed'
        return true
      }
      return false
    }
  }
})
