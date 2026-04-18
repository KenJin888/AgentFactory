import {defineStore} from 'pinia'
import type { LLM_PROVIDER, MODEL_META, ModelConfig, ModelType } from '@/types/model'
import {api} from '@/services/api'
import {decrypt, encrypt} from '@/utils/crypto'
import openaiIcon from '@/assets/llm-icons/openai.svg'
import anthropicIcon from '@/assets/llm-icons/anthropic.svg'
import deepseekIcon from '@/assets/llm-icons/deepseek-color.svg'
import siliconflowIcon from '@/assets/llm-icons/siliconcloud-color.svg'
import ollamaIcon from '@/assets/llm-icons/ollama.svg'
import openaiCompatibleIcon from '@/assets/llm-icons/jiekou-color.svg'
import doubaoIcon from '@/assets/llm-icons/doubao-color.svg'
import qwenIcon from '@/assets/llm-icons/qwen-color.svg'
import modelscopeIcon from '@/assets/llm-icons/modelscope-color.svg'
import alibabaCloudIcon from '@/assets/llm-icons/alibabacloud-color.svg'
import xiaomiIcon from '@/assets/llm-icons/xiaomi.png'
import minimaxIcon from '@/assets/llm-icons/minimax-color.svg'
import kimiIcon from '@/assets/llm-icons/kimi-color.svg'
import zhipuIcon from '@/assets/llm-icons/zhipu-color.svg'
import moonshotIcon from '@/assets/llm-icons/moonshot.svg'
import openrouterIcon from '@/assets/llm-icons/openrouter.svg'
import huggingfaceIcon from '@/assets/llm-icons/huggingface-color.svg'
import antgroupIcon from '@/assets/llm-icons/antgroup-color.svg'
import ai302Icon from '@/assets/llm-icons/302ai.svg'
import ProvidersData from '@/assets/resources/providers.json'


export interface ProviderConfig {
  apiUrl?: string
  apiKey?: string
  baseUrl: string
  models: MODEL_META[]
}

export interface ModelProvider {
  id: string
  name: string
  description: string
  isEnabled: boolean
  config: ProviderConfig
}

export const getProviderIcon = (id: string): string => {
  if(!id) return ''
  const rawProviders = (ProvidersData as any)?.providers ?? ProvidersData
  const provider = rawProviders?.[id]
  const providerName = String(provider?.name ?? provider?.display_name ?? id)
  const normalizedId = id.toLowerCase()
  const normalizedName = providerName.toLowerCase()

  if (normalizedId === 'openai' || normalizedName.includes('openai')) return openaiIcon
  if (normalizedId === 'anthropic' || normalizedName.includes('anthropic')) return anthropicIcon
  if (normalizedId === 'deepseek' || normalizedName.includes('deepseek')) return deepseekIcon
  if (normalizedId === 'siliconflow' || providerName.includes('硅基') || normalizedName.includes('siliconflow')) return siliconflowIcon
  if (normalizedId === 'ollama' || normalizedName.includes('ollama')) return ollamaIcon
  if (normalizedId === 'openai_compatible' || normalizedName.includes('compatible')) return openaiCompatibleIcon
  if (normalizedId === 'doubao' || providerName.includes('豆包') || normalizedName.includes('doubao')) return doubaoIcon
  if (normalizedId === 'modelscope' || providerName.includes('魔搭') || normalizedName.includes('modelscope')) return modelscopeIcon
  if (normalizedId === 'alibaba-cn' || providerName.includes('阿里') || normalizedName.includes('alibaba')) return alibabaCloudIcon
  if (normalizedId === 'xiaomi' || providerName.includes('小米') || normalizedName.includes('xiaomi')) return xiaomiIcon
  if (normalizedId.includes('minimax') || normalizedName.includes('minimax')) return minimaxIcon
  if (normalizedId.includes('kimi') || normalizedName.includes('kimi')) return kimiIcon
  if (normalizedId.includes('zhipu') || providerName.includes('智谱') || normalizedName.includes('zhipu')) return zhipuIcon
  if (normalizedId.includes('moonshot') || normalizedName.includes('moonshot')) return moonshotIcon
  if (normalizedId.includes('openrouter') || normalizedName.includes('openrouter')) return openrouterIcon
  if (normalizedId.includes('huggingface') || normalizedName.includes('hugging face')) return huggingfaceIcon
  if (normalizedId.includes('bailing') || normalizedName.includes('bailing')) return antgroupIcon
  if (normalizedId.includes('302') || normalizedName.includes('302')) return ai302Icon
  if (normalizedId.includes('qwen') || providerName.includes('通义') || normalizedName.includes('qwen')) return qwenIcon

  return openaiCompatibleIcon
}

const buildInitialProviders = (): Record<string, ModelProvider> => {
  const rawProviders = (ProvidersData as any)?.providers ?? ProvidersData
  if (!rawProviders || typeof rawProviders !== 'object') return {}

  return Object.entries(rawProviders as Record<string, any>).reduce<Record<string, ModelProvider>>((acc, [key, provider]) => {
    if (!provider || typeof provider !== 'object') return acc
    const providerId = String(provider.id ?? key)
    const providerName = String(provider.name ?? providerId)
    const description = String(provider.description ?? provider.display_name ?? provider.name ?? provider.doc ?? '')
    const apiUrl = provider.doc ?? provider.apiUrl ?? provider.api_url
    const baseUrl = provider.api ?? provider.baseUrl ?? provider.base_url ?? ''
    const models = Array.isArray(provider.models)
      ? provider.models.map((model: any) => {
          const modelId = String(model?.id ?? '')
          if (!modelId) return null
          const inputModalities = model?.modalities?.input
          const hasVision = Array.isArray(inputModalities) && inputModalities.some((item: string) => item === 'image' || item === 'video')
          return {
            id: modelId,
            name: String(model.display_name ?? model.name ?? modelId),
            providerId: providerId,
            enabled: false,
            type: model.type || 'chat',
            contextLength: model.limit?.context,
            maxTokens: model.limit?.output,
            vision: hasVision || undefined,
            functionCall: model.tool_call ?? undefined,
            reasoning: model.reasoning?.supported ?? undefined,
            description: model.display_name ?? model.name
          } as MODEL_META
        }).filter((model:any) => model !== null) as MODEL_META[]
      : []

    acc[providerId] = {
      id: providerId,
      name: providerName,
      description,
      isEnabled: provider.isEnabled ?? provider.enable ?? providerId === 'openai',
      config: {
        apiUrl,
        baseUrl,
        models
      }
    }

    return acc
  }, {})
}

const initialProviders: Record<string, ModelProvider> = buildInitialProviders()

export const useModelProviderStore = defineStore('modelProvider', {
  state: () => ({
    initProviders: initialProviders as Record<string, ModelProvider>,
    llmProviders: Object.values(initialProviders).map((provider) => ({
      id: provider.id,
      name: provider.name,
      apiKey: "",
      apiUrl: provider.config.apiUrl,
      baseUrl: provider.config.baseUrl,
      models: provider.config.models.map((m) => (m)),
      enable: false
    })) as LLM_PROVIDER[]
  }),
  getters: {
    providers(state): ModelProvider[] {
      return Object.values(state.initProviders).map((init) => {
        const pState = state.llmProviders.find((p) => p.id === init.id)
        if (!pState) return init
        return {
          ...init,
          isEnabled: pState.enable,
          config: {
            ...init.config,
            apiKey: decrypt(pState.apiKey),
            baseUrl: pState.baseUrl,
            models: pState.models ? pState.models.map((m) => m) : init.config.models
          }
        }
      })
    },
    getDefaultModel(state): { providerId: string; modelId: string } | null {
      const provider = state.llmProviders.find((p) => p.enable)
      if (!provider || !provider.models) return null
      const model = provider.models.find((m) => m.enabled)
      if (!model) return null
      return { providerId: provider.id, modelId: model.id }
    }
  },
  actions: {
    async initModels() {
      try {
        const remoteModels = await api.model.getModels()
        const resolveRemoteProviders = (payload: any): any[] => {
          if (Array.isArray(payload)) {
            return payload
          }

          if (Array.isArray(payload?.items)) {
            return payload.items
          }

          if (Array.isArray(payload?.data?.items)) {
            const firstItem = payload.data.items[0]
            if (typeof firstItem?.config_value === 'string') {
              try {
                const parsed = JSON.parse(firstItem.config_value)
                return Array.isArray(parsed) ? parsed : []
              } catch (e) {
                console.error('Failed to parse config_value in initModels:', e)
                return []
              }
            }
            return payload.data.items
          }

          if (typeof payload?.config_value === 'string') {
            try {
              const parsed = JSON.parse(payload.config_value)
              return Array.isArray(parsed) ? parsed : []
            } catch (e) {
              console.error('Failed to parse config_value in initModels:', e)
              return []
            }
          }

          return []
        }

        const remoteProviders = resolveRemoteProviders(remoteModels)

        if (remoteProviders.length > 0) {
          remoteProviders.forEach((remoteProvider) => {
            const localProviderIndex = this.llmProviders.findIndex((p) => p.id === remoteProvider.id)

            if (localProviderIndex !== -1) {
              const localProvider = this.llmProviders[localProviderIndex]
              const mergedModelMap = new Map<string, MODEL_META>()
              const localModels = Array.isArray(localProvider.models) ? localProvider.models : []
              const remoteProviderModels = Array.isArray(remoteProvider.models) ? remoteProvider.models : []

              localModels.forEach((model) => {
                mergedModelMap.set(model.id, { ...model })
              })

              remoteProviderModels.forEach((remoteModel: any) => {
                if (!remoteModel?.id) return
                const localModel = mergedModelMap.get(remoteModel.id)
                mergedModelMap.set(remoteModel.id, {
                  ...(localModel || {}),
                  ...remoteModel,
                  providerId: remoteModel.providerId || remoteProvider.id || localProvider.id
                })
              })

              this.llmProviders[localProviderIndex] = {
                  ...localProvider,
                  ...remoteProvider,
                  apiKey: remoteProvider.apiKey ?? localProvider.apiKey,
                  apiUrl: remoteProvider.apiUrl ?? localProvider.apiUrl,
                  baseUrl: remoteProvider.baseUrl ?? localProvider.baseUrl,
                  enable: typeof remoteProvider.enable === 'boolean' ? remoteProvider.enable : localProvider.enable,
                  models: Array.from(mergedModelMap.values())
              }
            } else {
              this.llmProviders.push({
                ...remoteProvider,
                models: Array.isArray(remoteProvider.models) ? remoteProvider.models : []
              })
            }
          })
        }
      } catch (error) {
        console.error('Failed to init models from remote:', error)
      }
    },
    async saveModels() {
      try {
        const providersToSave = this.llmProviders
          .filter((provider) => provider.enable || Boolean(provider.apiKey))
          .map((provider) => ({
            ...provider,
            models: Array.isArray(provider.models)
              ? provider.models.filter(
                  (model) => !(model.enabled === false && model.isCustom !== true && !model.userConfig)
                )
              : provider.models
          }))

        await api.model.setModels(providersToSave)
      } catch (error) {
        console.error('Failed to save models to remote:', error)
      }
    },
    toggleProvider(providerId: string) {
      const provider = this.llmProviders.find((item) => item.id === providerId)
      if (!provider) return
      provider.enable = !provider.enable
      //this.saveModels()
    },
    updateProviderConfig(providerId: string, config: Partial<ProviderConfig>) {
      const provider = this.llmProviders.find((item) => item.id === providerId)
      if (!provider) return

      if (config.apiKey !== undefined) provider.apiKey = encrypt(config.apiKey)
      if (config.baseUrl !== undefined) provider.baseUrl = config.baseUrl
      if (config.models) {
        config.models.forEach((m) => {
          this.updateModelConfig(providerId,m, false)
        })
      }
      this.saveModels()
    },
    updateModelConfig(providerId: string, model: MODEL_META, save = true) {
      const provider = this.llmProviders.find((item) => item.id === providerId)
      if (!provider) return

      if (!provider.models) {
        provider.models = []
      }

      const index = provider.models.findIndex((m) => m.id === model.id)
      if (index !== -1) {
        provider.models[index] = { ...provider.models[index], ...model }
      } else {
        provider.models.push(model)
      }

      if (save) {
        this.saveModels()
      }
    }
  }
})
