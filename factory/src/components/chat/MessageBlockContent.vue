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

<style>
/* 修复 markstream-vue 表格样式：添加外边框、内边框和斑马纹 */
.markstream-vue table {
  width: 100%;
  border-collapse: collapse;  /* 合并边框，实现整齐外边框 */
  margin: 1em 0;
  border: 1px solid #e2e8f0;  /* 外边框 */
}

.markstream-vue th,
.markstream-vue td {
  padding: 8px 12px;
  border-right: 1px solid #e2e8f0;  /* 内边框（右侧） */
  border-bottom: 1px solid #e2e8f0; /* 内边框（底部） */
  text-align: left;
}

/* 移除每行最后一个单元格的右边框，防止双重边框 */
.markstream-vue tr th:last-child,
.markstream-vue tr td:last-child {
  border-right: none;
}

/* 斑马纹：对 tbody 内的偶数行应用背景色 */
.markstream-vue tbody tr:nth-child(even) {
  background-color: #f8fafc;
}

/* 可选：鼠标悬停时加深背景，提升交互感 */
.markstream-vue tbody tr:hover {
  background-color: #f1f5f9;
}
</style>