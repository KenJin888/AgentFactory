<!-- IFrame 组件 - 用于内嵌外部页面 -->
<template>
  <div class="w-full h-full" v-loading="loading">
    <iframe
      :src="src"
      frameborder="0"
      width="100%"
      height="100%"
      scrolling="auto"
      class="w-full h-full"
      @load="handleLoad"
      @error="handleError"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Props {
  src: string
}

const props = defineProps<Props>()

const loading = ref(true)

const handleLoad = () => {
  loading.value = false
}

const handleError = () => {
  loading.value = false
  console.error('Failed to load iframe content:', props.src)
}

onMounted(() => {
  // 设置一个超时时间，防止 iframe 加载时间过长
  setTimeout(() => {
    loading.value = false
  }, 5000)
})
</script>
