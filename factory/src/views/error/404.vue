<template>
  <div class="min-h-screen bg-slate-50 flex items-center justify-center p-6">
    <div class="w-full max-w-2xl bg-white border border-slate-200 rounded-2xl shadow-sm p-8 md:p-10">
      <p class="text-sm font-semibold text-blue-600 tracking-wide">404 NOT FOUND</p>
      <h1 class="mt-3 text-3xl md:text-4xl font-bold text-slate-900">页面走丢了</h1>
      <p class="mt-4 text-slate-600 leading-relaxed">
        您访问的路径不存在或已被移动，请检查地址是否正确，或返回首页继续操作。
      </p>

      <div class="mt-6 rounded-xl bg-slate-50 border border-slate-200 p-4">
        <p class="text-xs text-slate-500">请求路径</p>
        <p class="mt-1 text-sm text-slate-800 break-all">{{ displayPath }}</p>
      </div>

      <div class="mt-8 flex flex-wrap gap-3">
        <button
          type="button"
          class="px-5 py-2.5 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 transition-colors"
          @click="goHome"
        >
          返回首页
        </button>
        <button
          type="button"
          class="px-5 py-2.5 bg-white text-slate-700 border border-slate-300 rounded-xl font-medium hover:bg-slate-100 transition-colors"
          @click="goBack"
        >
          返回上一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const displayPath = computed(() => {
  const rawPath = route.query.path
  if (typeof rawPath !== 'string' || !rawPath.trim()) {
    return '未知路径'
  }
  return rawPath
})

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  router.back()
}
</script>
