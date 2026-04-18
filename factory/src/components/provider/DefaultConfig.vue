<template>
  <div class="h-full flex flex-col items-center justify-center text-center p-8">
    <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mb-4">
      <Server class="w-8 h-8 text-slate-400" />
    </div>
    <h3 class="text-lg font-medium text-slate-900 mb-2">选择服务商</h3>
    <p class="text-slate-500 max-w-sm">
      请从左侧列表选择一个模型服务商进行配置，启用后即可在对话中使用该服务商的模型。点击开关按钮可以启用或禁用模型服务商。
    </p>
  </div>
</template>

<script setup lang="ts">
import { Server } from 'lucide-vue-next'
</script>
