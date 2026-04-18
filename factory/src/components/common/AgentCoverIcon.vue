<template>
  <div :class="containerClass" :style="{ backgroundColor: normalizedCover.color }">
    <component :is="iconComponent" :size="size" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { getAgentCoverIconComponent, normalizeAgentCover, type AgentCoverConfig } from './agentCover'

const props = withDefaults(
  defineProps<{
    cover?: string | AgentCoverConfig | null
    size?: number
    containerClass?: string
  }>(),
  {
    cover: '',
    size: 20,
    containerClass: 'w-10 h-10 rounded-xl flex items-center justify-center text-white'
  }
)

const normalizedCover = computed(() => normalizeAgentCover(props.cover))
const iconComponent = computed(() => getAgentCoverIconComponent(normalizedCover.value.icon))
</script>
