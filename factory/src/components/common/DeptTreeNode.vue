<template>
  <div>
    <!-- 当前节点 -->
    <div
      :class="[
        'flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer transition-all',
        isSelected ? 'bg-blue-50 text-blue-600' : 'hover:bg-slate-100 text-slate-700'
      ]"
      :style="{ paddingLeft: `${paddingLeft}px` }"
      @click="handleSelect"
    >
      <!-- 展开/收起图标 -->
      <ChevronRight
        v-if="hasChildren"
        :size="14"
        :class="['transition-transform', isExpanded ? 'rotate-90' : '']"
        @click.stop="handleToggle"
      />
      <span v-else class="w-3.5" />
      <!-- 部门名称 -->
      <span class="text-sm truncate">{{ dept.name }}</span>
    </div>
    <!-- 子节点 -->
    <template v-if="hasChildren && isExpanded">
      <DeptTreeNode
        v-for="child in dept.children"
        :key="child.id"
        :dept="child"
        :selected-dept-id="selectedDeptId"
        :expanded-depts="expandedDepts"
        :level="(level ?? 0) + 1"
        @select="$emit('select', $event)"
        @toggle-expand="$emit('toggle-expand', $event)"
      />
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { ChevronRight } from 'lucide-vue-next';

import type { Dept } from '@/types/user';

const props = defineProps<{
  dept: Dept;
  selectedDeptId?: number | null;
  expandedDepts?: number[];
  level?: number;
}>();

const emit = defineEmits<{
  (e: 'select', dept: Dept): void;
  (e: 'toggle-expand', deptId: number): void;
}>();

const isExpanded = computed(() => props.expandedDepts?.includes(props.dept.id) ?? false);
const isSelected = computed(() => props.selectedDeptId === props.dept.id);
const hasChildren = computed(() => props.dept.children && props.dept.children.length > 0);
const paddingLeft = computed(() => (props.level ?? 0) * 12 + 12);

const handleSelect = () => {
  emit('select', props.dept);
};

const handleToggle = () => {
  emit('toggle-expand', props.dept.id);
};
</script>
