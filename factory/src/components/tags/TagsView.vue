<template>
  <div class="h-9 border-b border-slate-200 bg-slate-50 flex items-start pr-3">
    <div class="flex-1 min-w-0 h-[calc(100%+1px)] overflow-x-auto" style="scrollbar-width: none;">
      <div class="flex items-start h-full w-max">
        <button
          v-for="tag in visitedViews"
          :key="tag.fullPath"
          type="button"
          class="group relative h-[calc(100%-1px)] w-36 px-3 border-r border-slate-200 text-sm transition-colors flex items-center gap-2 flex-shrink-0"
          :class="isActive(tag) ? 'bg-slate-50 text-black' : 'bg-slate-100 text-slate-500 hover:bg-white hover:text-slate-800'"
          @click="openTag(tag)"
        >
          <div v-if="isActive(tag)" class="absolute top-0 left-0 right-0 h-[2px] bg-black"></div>
          <div v-if="isActive(tag)" class="absolute -bottom-[1px] left-0 right-0 h-[1px] bg-slate-50 z-10"></div>

          <component
            :is="resolveTagIconComponent(tag)"
            :size="14"
            class="flex-shrink-0"
          />

          <span class="flex-1 truncate text-left">{{ getTagTitle(tag) }}</span>

          <div
            v-if="!tag.affix"
            class="flex items-center justify-center rounded text-slate-400 hover:bg-slate-200 hover:text-slate-600 transition-all opacity-0 group-hover:opacity-100 p-0.5"
            :class="{ 'opacity-100': isActive(tag) }"
            @click.stop="closeTag(tag)"
          >
            <X :size="14" />
          </div>
        </button>
      </div>
    </div>
    <div class="flex items-center gap-1 shrink-0 ml-3 h-full">
      <button
        type="button"
        class="h-7 w-7  text-slate-600 hover:bg-slate-100 transition-colors flex items-center justify-center"
        title="关闭其他"
        aria-label="关闭其他"
        @click="closeOtherTags"
      >
        <CircleOff :size="14" />
      </button>
      <button
        type="button"
        class="h-7 w-7  text-slate-600 hover:bg-slate-100 transition-colors flex items-center justify-center"
        title="关闭全部"
        aria-label="关闭全部"
        @click="closeAllTags"
      >
        <TouchpadOff :size="14" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter, type RouteLocationNormalizedLoaded, type RouteRecordRaw } from 'vue-router'
import { usePermissionStore } from '@/stores/permission'
import { useTagsViewStore } from '@/stores/tagsView'
import { CircleOff, MessageSquareText, TouchpadOff, X } from 'lucide-vue-next'
import { getAgentCoverIconComponent } from '@/components/common/agentCover'
import AiAgentAPI from '@/services/fastApi/module_ai/ai_agent'

const route = useRoute()
const router = useRouter()
const permissionStore = usePermissionStore()
const tagsViewStore = useTagsViewStore()
const { visitedViews } = storeToRefs(tagsViewStore)
const agentNameMap = ref<Record<string, string>>({})
const loadingAgentIds = new Set<string>()

const resolveIconComponent = (icon?: string) => getAgentCoverIconComponent(icon)
const resolveAgentId = (value: unknown): string => {
  const normalized = tagsViewStore.normalizeAgentId(value)
  const parsed = Number(normalized)
  if (!Number.isInteger(parsed) || parsed <= 0) {
    return ''
  }
  return String(parsed)
}

const isAgentSessionTag = (tag: TagView) => Boolean(resolveAgentId(tag.agentId))

const resolveTagIconComponent = (tag: TagView) => {
  if (isAgentSessionTag(tag)) {
    return MessageSquareText
  }
  return resolveIconComponent(tag.icon)
}

const getTagTitle = (tag: TagView) => {
  const agentId = resolveAgentId(tag.agentId)
  if (!agentId) {
    return tag.title
  }
  return agentNameMap.value[agentId] || tag.title
}

const loadAgentName = async (agentId: string) => {
  if (!agentId || agentNameMap.value[agentId] || loadingAgentIds.has(agentId)) {
    return
  }
  loadingAgentIds.add(agentId)
  try {
    const result = await AiAgentAPI.detailAiAgent(Number(agentId))
    const agentName = String(result.data?.data?.name || '').trim()
    if (!agentName) {
      return
    }
    agentNameMap.value = {
      ...agentNameMap.value,
      [agentId]: agentName
    }
  } catch {
  } finally {
    loadingAgentIds.delete(agentId)
  }
}

const syncAgentNames = () => {
  const ids = Array.from(
    new Set(
      visitedViews.value
        .map((item) => resolveAgentId(item.agentId))
        .filter((item) => Boolean(item))
    )
  )
  ids.forEach((id) => {
    void loadAgentName(id)
  })
}

const normalizePath = (basePath: string, segment: string) => {
  if (!segment) {
    return basePath || '/'
  }
  if (segment.startsWith('/')) {
    return segment.replace(/\/{2,}/g, '/')
  }
  const normalizedBase = basePath || '/'
  const normalizedSegment = segment.replace(/^\/+/, '')
  return `${normalizedBase.replace(/\/+$/, '')}/${normalizedSegment}`.replace(/\/{2,}/g, '/')
}

const isDisplayableRoute = (targetRoute: RouteLocationNormalizedLoaded) => {
  return Boolean(targetRoute.meta?.title) && !Boolean((targetRoute.meta as any)?.hidden) && !Boolean((targetRoute.meta as any)?.hideInTags)
}

const resolveConversationId = (targetRoute: RouteLocationNormalizedLoaded): string => {
  const raw = targetRoute.params?.conversationId
  if (Array.isArray(raw)) {
    return String(raw[0] || '').trim()
  }
  return String(raw || '').trim()
}

const createTagFromRoute = (targetRoute: RouteLocationNormalizedLoaded): TagView => {
  const conversationId = resolveConversationId(targetRoute)
  const agentId = tagsViewStore.getRegisteredAgentId(conversationId) || undefined
  return {
    name: String(targetRoute.name || ''),
    title: String(targetRoute.meta?.title || targetRoute.name || ''),
    path: targetRoute.path,
    fullPath: targetRoute.fullPath,
    icon: targetRoute.meta?.icon as string | undefined,
    affix: Boolean(targetRoute.meta?.affix),
    keepAlive: Boolean(targetRoute.meta?.keepAlive),
    query: targetRoute.query,
    conversationId: conversationId || undefined,
    agentId
  }
}

const addCurrentTag = () => {
  if (!isDisplayableRoute(route)) {
    return
  }
  const tag = createTagFromRoute(route)
  const exists = visitedViews.value.find((item) => item.fullPath === tag.fullPath)
  if (exists) {
    tagsViewStore.updateVisitedView(tag)
    return
  }
  tagsViewStore.addView(tag)
}

const collectAffixTags = (routes: RouteRecordRaw[], basePath = ''): TagView[] => {
  const tags: TagView[] = []
  routes.forEach((item) => {
    const fullPath = normalizePath(basePath, String(item.path || ''))
    if (item.meta?.affix && item.meta?.title && item.name) {
      tags.push({
        name: String(item.name),
        title: String(item.meta.title),
        path: fullPath,
        fullPath,
        icon: item.meta?.icon as string | undefined,
        affix: true,
        keepAlive: Boolean(item.meta.keepAlive)
      })
    }
    if (Array.isArray(item.children) && item.children.length > 0) {
      tags.push(...collectAffixTags(item.children, fullPath))
    }
  })
  return tags
}

const initAffixTags = () => {
  const affixTags = collectAffixTags(permissionStore.routes)
  affixTags.forEach((tag) => {
    tagsViewStore.addView(tag)
  })
}

const currentFullPath = computed(() => route.fullPath)
const isActive = (tag: TagView) => tagsViewStore.isActive(tag, currentFullPath.value)
const emitClosedTags = (tags: TagView[]) => {
  tags.forEach((tag) => {
    if (tag.conversationId) {
      tagsViewStore.unregisterConversationAgent(tag.conversationId)
    }
    window.dispatchEvent(new CustomEvent('tags-view:closed', { detail: { fullPath: tag.fullPath } }))
  })
}

const openTag = async (tag: TagView) => {
  if (tag.fullPath !== currentFullPath.value) {
    await router.push(tag.fullPath)
  }
}

const closeTag = async (tag: TagView) => {
  if (tag.affix) {
    return
  }
  const isCurrent = tag.fullPath === currentFullPath.value
  const removedTags = tagsViewStore.delView(tag)
  emitClosedTags(removedTags)
  if (isCurrent) {
    await tagsViewStore.toLastView(tag)
  }
}

const closeOtherTags = async () => {
  const currentTag = visitedViews.value.find((item) => item.fullPath === currentFullPath.value)
  if (!currentTag) {
    return
  }
  const removedTags = tagsViewStore.delOtherViews(currentTag)
  emitClosedTags(removedTags)
  if (route.fullPath !== currentTag.fullPath) {
    await router.push(currentTag.fullPath)
  }
}

const closeAllTags = async () => {
  const removedTags = tagsViewStore.delAllViews()
  emitClosedTags(removedTags)
  await tagsViewStore.toLastView()
}

watch(
  () => permissionStore.routes,
  () => {
    initAffixTags()
  },
  { deep: true, immediate: true }
)

watch(
  () => route.fullPath,
  () => {
    addCurrentTag()
  },
  { immediate: true }
)

watch(
  visitedViews,
  () => {
    syncAgentNames()
  },
  { deep: true, immediate: true }
)
</script>
