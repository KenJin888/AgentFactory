<template>
  <section class="flex-1 min-h-0 overflow-auto bg-slate-50">
    <router-view v-slot="{ Component, route }">
      <keep-alive :include="cachedViews">
        <component
          :is="Component"
          v-if="route.meta?.keepAlive"
          :key="route.fullPath"
          :refresh-user="refreshUser"
        />
      </keep-alive>
      <component
        :is="Component"
        v-if="!route.meta?.keepAlive"
        :key="route.fullPath"
        :refresh-user="refreshUser"
      />
    </router-view>
  </section>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useTagsViewStore } from '@/stores/tagsView'

defineProps<{
  refreshUser: () => void
}>()

const tagsViewStore = useTagsViewStore()
const { cachedViews } = storeToRefs(tagsViewStore)
</script>
