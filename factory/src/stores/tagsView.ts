import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'

export const MAX_SESSION_TABS = 3
const CHAT_PAGE_NAME = 'ChatPage'

type SessionTabGuardResult =
  | { allowed: true }
  | { allowed: false; reason: 'duplicate'; existingView: TagView }
  | { allowed: false; reason: 'max_limit' }

export const useTagsViewStore = defineStore('tagsView', () => {
  const visitedViews = ref<TagView[]>([])
  const cachedViews = ref<string[]>([])
  const conversationAgentMap = ref<Record<string, string>>({})
  const router = useRouter()

  const visitedViewMap = computed(() => {
    const map = new Map<string, TagView>()
    visitedViews.value.forEach((item) => {
      map.set(item.fullPath, item)
    })
    return map
  })

  const addVisitedView = (view: TagView) => {
    if (!view?.title || !view?.name) {
      return
    }
    if (visitedViewMap.value.has(view.fullPath)) {
      return
    }
    if (view.affix) {
      visitedViews.value.unshift(view)
      return
    }
    visitedViews.value.push(view)
  }

  const addCachedView = (view: TagView) => {
    if (!view?.keepAlive || !view?.name) {
      return
    }
    if (cachedViews.value.includes(view.name)) {
      return
    }
    cachedViews.value.push(view.name)
  }

  const addView = (view: TagView) => {
    addVisitedView(view)
    addCachedView(view)
  }

  const updateVisitedView = (view: Partial<TagView> & Pick<TagView, 'fullPath'>) => {
    const index = visitedViews.value.findIndex((item) => item.fullPath === view.fullPath)
    if (index < 0) {
      return
    }
    visitedViews.value[index] = {
      ...visitedViews.value[index],
      ...view
    }
  }

  const normalizeAgentId = (value: unknown): string => {
    const raw = String(value ?? '').trim()
    if (!raw) {
      return ''
    }
    const parsed = Number(raw)
    if (!Number.isInteger(parsed) || parsed < 0) {
      return ''
    }
    return String(parsed)
  }

  const normalizeConversationId = (value: unknown): string => {
    const raw = String(value ?? '').trim()
    return raw
  }

  const registerConversationAgent = (conversationId: unknown, agentId: unknown) => {
    const normalizedConversationId = normalizeConversationId(conversationId)
    const normalizedAgentId = normalizeAgentId(agentId)
    if (!normalizedConversationId || !normalizedAgentId) {
      return
    }
    conversationAgentMap.value[normalizedConversationId] = normalizedAgentId
  }

  const unregisterConversationAgent = (conversationId: unknown) => {
    const normalizedConversationId = normalizeConversationId(conversationId)
    if (!normalizedConversationId) {
      return
    }
    delete conversationAgentMap.value[normalizedConversationId]
  }

  const getRegisteredAgentId = (conversationId: unknown): string => {
    const normalizedConversationId = normalizeConversationId(conversationId)
    if (!normalizedConversationId) {
      return ''
    }
    return conversationAgentMap.value[normalizedConversationId] || ''
  }

  const delCachedView = (view: TagView) => {
    if (!view?.name) {
      return
    }
    // Only remove from cachedViews if there are no other views with the same name
    const hasOtherViewsWithSameName = visitedViews.value.some(
      (item) => item.name === view.name && item.fullPath !== view.fullPath
    )
    if (hasOtherViewsWithSameName) {
      return
    }
    const index = cachedViews.value.indexOf(view.name)
    if (index >= 0) {
      cachedViews.value.splice(index, 1)
    }
  }

  const delVisitedView = (view: TagView) => {
    const index = visitedViews.value.findIndex((item) => item.fullPath === view.fullPath)
    if (index >= 0) {
      visitedViews.value.splice(index, 1)
    }
  }

  const delView = (view: TagView) => {
    const exists = visitedViews.value.some((item) => item.fullPath === view.fullPath)
    if (!exists) {
      return [] as TagView[]
    }
    delVisitedView(view)
    delCachedView(view)
    return [view]
  }

  const delOtherViews = (view: TagView) => {
    const removedViews = visitedViews.value.filter((item) => !item.affix && item.fullPath !== view.fullPath)
    visitedViews.value = visitedViews.value.filter((item) => item.affix || item.fullPath === view.fullPath)
    cachedViews.value = view.keepAlive && view.name ? [view.name] : []
    return removedViews
  }

  const delAllViews = () => {
    const removedViews = visitedViews.value.filter((item) => !item.affix)
    const affixTags = visitedViews.value.filter((item) => item.affix)
    visitedViews.value = affixTags
    cachedViews.value = []
    return removedViews
  }

  const isActive = (view: TagView, currentFullPath: string) => {
    return view.fullPath === currentFullPath
  }

  const getSessionTabs = () => {
    return visitedViews.value.filter((item) => item.name === CHAT_PAGE_NAME)
  }

  const countSessionTabs = () => {
    return getSessionTabs().length
  }

  const findSessionTabByAgentId = (agentId: unknown, excludeFullPath = ''): TagView | undefined => {
    const normalizedAgentId = normalizeAgentId(agentId)
    if (!normalizedAgentId) {
      return undefined
    }
    return getSessionTabs().find((item) => {
      if (excludeFullPath && item.fullPath === excludeFullPath) {
        return false
      }
      return normalizeAgentId(item.agentId) === normalizedAgentId
    })
  }

  const canOpenSessionTab = (agentId: unknown, excludeFullPath = ''): SessionTabGuardResult => {
    const duplicated = findSessionTabByAgentId(agentId, excludeFullPath)
    if (duplicated) {
      return { allowed: false, reason: 'duplicate', existingView: duplicated }
    }
    if (countSessionTabs() >= MAX_SESSION_TABS) {
      return { allowed: false, reason: 'max_limit' }
    }
    return { allowed: true }
  }

  const toLastView = async (view?: TagView) => {
    const latestView = visitedViews.value.at(-1)
    if (latestView?.fullPath) {
      await router.push(latestView.fullPath)
      return
    }
    if (view?.affix && view?.fullPath) {
      await router.replace(view.fullPath)
      return
    }
    await router.push('/')
  }

  return {
    visitedViews,
    cachedViews,
    addVisitedView,
    addCachedView,
    addView,
    updateVisitedView,
    normalizeAgentId,
    registerConversationAgent,
    unregisterConversationAgent,
    getRegisteredAgentId,
    delVisitedView,
    delCachedView,
    delView,
    delOtherViews,
    delAllViews,
    findSessionTabByAgentId,
    countSessionTabs,
    canOpenSessionTab,
    isActive,
    toLastView
  }
})
