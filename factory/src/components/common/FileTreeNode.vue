<template>
  <div>
    <!-- 当前节点 -->
    <div
      :class="[
        'flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer transition-all',
        isSelected ? 'bg-blue-50 text-blue-600 border border-blue-200' :
        node.type === 'directory' ? 'hover:bg-amber-50 text-slate-700' : 'hover:bg-slate-100 text-slate-700'
      ]"
      :style="{ paddingLeft: `${paddingLeft}px` }"
      @click="handleNodeClick"
    >
      <!-- 展开/收起图标（仅目录） -->
      <ChevronRight
        v-if="node.type === 'directory'"
        :size="14"
        :class="['transition-transform duration-200', isExpanded ? 'rotate-90' : '']"
        @click.stop="handleToggle"
      />
      <span v-else class="w-3.5" />

      <!-- 节点图标 -->
      <component
        :is="node.type === 'directory' ? FolderOpen : FileText"
        :size="14"
        :class="node.type === 'directory' ? 'text-amber-500' : 'text-blue-500'"
      />

      <!-- 节点名称 -->
      <span class="text-sm truncate">{{ node.name }}</span>

      <!-- 加载状态指示器 -->
      <Loader2
        v-if="node.type === 'directory' && isLoading"
        :size="12"
        class="animate-spin ml-auto text-slate-400"
      />
    </div>

    <!-- 子节点 -->
    <template v-if="node.type === 'directory' && isExpanded">
      <div v-if="node.children && node.children.length > 0">
        <FileTreeNode
          v-for="child in node.children"
          :key="child.id"
          :node="child"
          :selected-node-path="selectedNodePath"
          :expanded-nodes="expandedNodes"
          :level="(level ?? 0) + 1"
          @select="$emit('select', $event)"
          @toggle="$emit('toggle', $event)"
        />
      </div>
      <div v-else-if="node.loaded && (!node.children || node.children.length === 0)" class="px-3 py-1 text-xs text-slate-400 italic" :style="{ paddingLeft: `${paddingLeft + 20}px` }">
        空目录
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { ChevronRight, FolderOpen, FileText, Loader2 } from 'lucide-vue-next';
import type { KnowledgeBaseItem } from '@/services/fastApi/module_ai/ai_knowledge_base';

// 树节点类型
export interface FileTreeNode {
  id: string;           // 唯一标识，使用完整路径
  name: string;         // 显示名称
  type: 'file' | 'directory';
  path: string;         // 完整路径
  children?: FileTreeNode[]; // 子节点
  expanded?: boolean;   // 展开状态
  loaded?: boolean;     // 子节点是否已加载
  loading?: boolean;    // 是否正在加载子节点
  rawItem?: KnowledgeBaseItem; // 原始数据，用于文件预览
}

const props = defineProps<{
  node: FileTreeNode;
  selectedNodePath?: string | null;
  expandedNodes?: Record<string, boolean>;
  level?: number;
}>();

const emit = defineEmits<{
  (e: 'select', node: FileTreeNode): void;
  (e: 'toggle', node: FileTreeNode): void;
}>();

// 计算属性
const isExpanded = computed(() => {
  return props.expandedNodes?.[props.node.id] ?? props.node.expanded ?? false;
});

const isSelected = computed(() => {
  return props.selectedNodePath === props.node.id;
});

const isLoading = computed(() => {
  return props.node.loading ?? false;
});

const paddingLeft = computed(() => (props.level ?? 0) * 16 + 12);

// 处理节点点击
const handleNodeClick = () => {
  if (props.node.type === 'file') {
    // 文件：触发选择
    emit('select', props.node);
  } else {
    // 目录：如果没有加载过子节点，触发加载
    if (!props.node.loaded) {
      emit('toggle', props.node);
    } else {
      // 已加载，直接切换展开状态
      emit('toggle', props.node);
    }
  }
};

// 处理展开/收起切换
const handleToggle = (event: Event) => {
  event.stopPropagation();
  emit('toggle', props.node);
};
</script>