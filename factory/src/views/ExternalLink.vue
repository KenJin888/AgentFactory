<!-- 外链页面 - 用于内嵌显示外部链接 -->
<template>
  <div class="w-full h-full bg-white">
    <IFrame :src="src" />
  </div>
</template>

<script setup lang="ts">
import IFrame from '@/components/common/IFrame.vue'

defineOptions({
  name: 'ExternalLink'
})

interface Props {
  src: string
}

const props = defineProps<Props>()
</script>
