import {createApp} from 'vue'
import {createPinia} from 'pinia'
import App from './App.vue'
import '@fontsource/inter/latin-300.css'
import '@fontsource/inter/latin-400.css'
import '@fontsource/inter/latin-500.css'
import '@fontsource/inter/latin-600.css'
import '@fontsource/inter/latin-700.css'
import './index.css'

// 导入路由配置
import router from './router'
import { useRuntimeStore } from '@/stores/runtime'
import { useConfigStore } from '@/stores/config'
import { setupDirectives } from '@/directives'

const app = createApp(App)

// 使用插件
const pinia = createPinia()
app.use(pinia)
setupDirectives(app)
app.use(router)

// 挂载应用
app.mount('#app')

useRuntimeStore(pinia).initEnv()

const initSystemConfig = async () => {
  try {
    const configStore = useConfigStore(pinia)
    await configStore.getConfig()

    const webTitle = configStore.getConfigValue('sys_web_title')
    const webFavicon = configStore.getConfigValue('sys_web_favicon')

    if (webTitle) {
      document.title = webTitle
    }

    if (webFavicon) {
      const favicon = document.querySelector('link[rel="icon"]')
      if (favicon instanceof HTMLLinkElement) {
        favicon.href = webFavicon
      }
    }
  } catch (error) {
    console.error('Failed to init system config:', error)
  }
}

initSystemConfig()
