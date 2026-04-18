<template>
  <NodeRenderer :content="content" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import NodeRenderer from 'markstream-vue'
import type { AssistantMessageBlock } from '../../types/chat'

const props = defineProps<{
  block: AssistantMessageBlock
}>()

const content = computed(() => props.block.content || '')
</script>
