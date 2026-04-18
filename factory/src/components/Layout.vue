<template>
  <div class="flex h-screen bg-slate-50 font-sans">
    <Sidebar/>
    <div class="flex-1 flex flex-col h-full overflow-hidden">
      <TagsView />
      <AppMain  :refresh-user="refreshUser" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import Sidebar from './Sidebar.vue'
import TagsView from './tags/TagsView.vue'
import AppMain from './layout/AppMain.vue'
import { useModelProviderStore } from '@/stores/modelProviders'
import { useUserStore } from '@/stores/user'
const userStore = useUserStore()

// 响应式数据
// const sessions = ref<ChatSession[]>([])
// const user = ref<User | null>(null)
const modelProviderStore = useModelProviderStore()


// 刷新用户信息的方法（供子组件调用）
const refreshUser = () => {
  userStore.loadUser(true)
}

// 暴露方法给父组件
defineExpose({
  refreshUser
})

// 组件挂载时加载数据
onMounted(async () => {
  // 先加载用户信息，确保 user_id 可用
  await userStore.loadUser()
  modelProviderStore.initModels()
})
</script>
