<template>
  <div class="app-container">
    <router-view />
  </div>
</template>

<script setup lang="ts">
// App.vue 是应用的根组件，主要用于挂载路由视图
// 所有的路由组件将通过 router-view 渲染
</script>

<style scoped>
.app-container {
  width: 100%;
  height: 100vh;
  overflow: hidden;
}
</style>
