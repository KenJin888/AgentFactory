<template>
  <div class="space-y-1">
    <div v-for="node in nodes" :key="node.key">
      <div
        class="flex items-center gap-3 py-3 text-sm font-medium rounded-xl transition-all cursor-pointer"
        :class="$route.path === node.path ? 'bg-blue-600 text-white shadow-md shadow-blue-900/20' : 'hover:bg-slate-800/50 hover:text-white'"
        :style="{ paddingLeft: `${16 + level * 12}px`, paddingRight: '16px' }"
        role="button"
        tabindex="0"
        @click="handleRowClick(node)"
        @keydown.enter.prevent="handleRowClick(node)"
        @keydown.space.prevent="handleRowClick(node)"
      >
        <component
          :is="resolveIconComponent(node.icon)"
          :size="20"
          class="flex-shrink-0"
        />
        <span class="flex-1 truncate min-w-0">
          {{ node.title }}
        </span>

        <button
          v-if="node.children.length > 0"
          type="button"
          class="ml-auto transition-colors"
          @click.stop="$emit('toggle', node.key)"
        >
          <ChevronRight :size="16" :class="expanded[node.key] ? 'rotate-90 transition-transform' : 'transition-transform'" />
        </button>
        <span v-else class="w-4 ml-auto" />
      </div>

      <div v-show="node.children.length > 0 && expanded[node.key]">
        <ManagementMenuTree :nodes="node.children" :level="level + 1" :expanded="expanded" @toggle="$emit('toggle', $event)" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ChevronRight } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { getAgentCoverIconComponent } from '@/components/common/agentCover'

defineOptions({ name: 'ManagementMenuTree' })

export type ManagementMenuNode = {
  key: string
  title: string
  path: string
  icon?: string
  children: ManagementMenuNode[]
}

const resolveIconComponent = (icon?: string) => getAgentCoverIconComponent(icon)
const router = useRouter()

defineProps<{
  nodes: ManagementMenuNode[]
  level: number
  expanded: Record<string, boolean>
}>()

const emit = defineEmits<{
  toggle: [key: string]
}>()

const handleRowClick = (node: ManagementMenuNode) => {
  if (node.children.length > 0) {
    emit('toggle', node.key)
    return
  }
  router.push(node.path)
}
</script>
