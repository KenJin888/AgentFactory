import {ref} from 'vue'
import {defineStore} from 'pinia'
import {api} from '@/services/api'
import type {ConfigTable} from '@/services/fastApi/module_system/params'

export type ConfigKey =
  | 'sys_web_title'
  | 'sys_web_version'
  | 'sys_web_slogan1'
  | 'sys_web_slogan2'
  | 'sys_web_description'
  | 'sys_web_favicon'
  | 'sys_web_logo'
  | 'sys_web_copyright'
  | 'ip_black_list'
  | 'demo_enable'
  | 'ip_white_list'

export type ConfigState = Partial<Record<ConfigKey, ConfigTable>>

const CONFIG_KEYS = new Set<ConfigKey>([
  'sys_web_title',
  'sys_web_slogan1',
  'sys_web_slogan2',
  'sys_web_version',
  'sys_web_description',
  'sys_web_favicon',
  'sys_web_logo',
  'sys_web_copyright',
  'ip_black_list',
  'demo_enable',
  'ip_white_list',
])

export const useConfigStore = defineStore('config', () => {
  const configData = ref<ConfigState>({})
  const isConfigLoaded = ref(false)
  const isLoading = ref(false)

  const getConfig = async (force = false): Promise<ConfigState> => {
    if (isConfigLoaded.value && !force) {
      return configData.value
    }

    isLoading.value = true
    try {
      const response = await api.params.getInitConfig()
      const list = response.data || []
      const nextConfig: ConfigState = {}

      list.forEach((item) => {
        const key = item.config_key as ConfigKey | undefined
        if (key && CONFIG_KEYS.has(key) && item.config_value !== undefined) {
          nextConfig[key] = item
        }
      })

      configData.value = nextConfig
      isConfigLoaded.value = true
      return configData.value
    } finally {
      isLoading.value = false
    }
  }

  const getConfigValue = (key: ConfigKey, fallback = ''): string => {
    const value = configData.value[key]?.config_value

    if (!value) {
      return fallback
    }

    if (fallback && /^\/?src\/assets\//.test(value)) {
      return fallback
    }

    return value
  }

  return {
    configData,
    isConfigLoaded,
    isLoading,
    getConfig,
    getConfigValue,
  }
})
