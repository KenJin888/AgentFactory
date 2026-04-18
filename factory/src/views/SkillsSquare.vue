<template>
  <div class="h-full flex flex-col bg-gray-50 overflow-hidden relative">
    <!-- 顶部搜索和创建按钮区域 -->
    <div class="px-8 py-6 bg-slate-50 border-b border-gray-100 flex-shrink-0">
      <div class="max-w-6xl mx-auto flex flex-col md:flex-row gap-4 items-center justify-between">
        <div class="w-full md:w-auto flex-shrink-0">
          <h1 class="text-2xl font-bold text-slate-900">技能</h1>
          <p class="mt-1 text-sm text-slate-500">管理可用Skills技能。</p>
        </div>
        <div class="w-full md:w-auto flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-end">
          <div class="relative w-full md:w-96 group">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-blue-500" :size="20" />
            <input
              type="text"
              placeholder="查找技能..."
              v-model="searchQuery"
              class="w-full pl-10 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-4 focus:ring-blue-50 outline-none transition-all"
            />
          </div>
          <button
            @click="handleCreateClick"
            v-has-perm="PERMS.create"
            class="px-6 py-3 text-white rounded-xl font-bold shadow-lg transition-all flex items-center gap-2 active:scale-95 bg-slate-900 hover:bg-slate-800"
          >
            <Plus :size="18" />
            创建技能
          </button>
        </div>
      </div>
    </div>

    <!-- 技能卡片列表 -->
    <div v-if="loading" class="flex-1 flex items-center justify-center">
      <div class="text-center text-gray-500 flex flex-col items-center gap-2">
        <Loader2 class="animate-spin" />
        <span>正在加载技能列表...</span>
      </div>
    </div>
    <div v-else class="flex-1 overflow-y-auto p-8 custom-scrollbar">
      <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div
          v-for="skill in filteredSkills"
          :key="skill.name"
          @click="() => handleSkillClick(skill.name)"
          class="group bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:shadow-xl hover:border-blue-100 transition-all cursor-pointer relative overflow-hidden flex flex-col h-full"
        >
          <!-- 顶部标签 -->
          <div class="flex justify-between items-start mb-4">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-white shadow-lg bg-gradient-to-br from-blue-500 to-cyan-600">
              <Wrench :size="24" />
            </div>

            <!-- 右上角操作区 -->
            <div class="flex gap-1">
              <!-- 删除按钮 -->
              <button
                  @click.stop="() => handleDeleteSkill(skill.name)"
                  v-has-perm="PERMS.delete"
                  class="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors"
                  title="删除"
              >
                  <Trash2 :size="16" />
              </button>
            </div>
          </div>

          <!-- 内容区域 -->
          <div class="flex-1">
            <h3 class="text-lg font-bold text-slate-900 mb-2 group-hover:text-blue-600 transition-colors line-clamp-1">
                {{ skill.name }}
            </h3>
            <p class="text-slate-500 text-sm line-clamp-3 leading-relaxed">
                {{ skill.description }}
            </p>
          </div>

          <!-- 底部信息 -->

        </div>

        <!-- 空状态 -->
        <div v-if="filteredSkills.length === 0" class="col-span-full flex flex-col items-center justify-center py-20 text-slate-400">
          <Wrench :size="48" class="mb-4 opacity-50" />
          <p>暂无技能</p>
        </div>
      </div>
    </div>

    <!-- 创建技能模态框 -->
    <CreateSkillModal
      v-if="isModalOpen"
      @close="isModalOpen = false"
      @success="handleCreateSuccess"
    />
    <SkillDetailModal
      v-if="selectedSkill"
      :skill-name="selectedSkill"
      @close="selectedSkill = null"
      @deleted="fetchSkills"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Search, Plus, Loader2, Wrench, Trash2 } from 'lucide-vue-next'
import CreateSkillModal from '@/components/skill/CreateSkillModal.vue'
import SkillDetailModal from '@/components/skill/SkillDetailModal.vue'
import AISkillsAPI from '../services/fastApi/module_ai/ai_skills'
import { useUserStore } from '@/stores/user'
import { dialog } from '@/components/common/dialog'
import message from '@/components/common/message'

// 用户 store
const userStore = useUserStore()

// 响应式数据
const skills = ref<{ name: string; description: string }[]>([])
const loading = ref(true)
const searchQuery = ref('')
const isModalOpen = ref(false)
const selectedSkill = ref<string | null>(null)

const PERMS = {
  create: 'module_ai:ai_skills:create',
  delete: 'module_ai:ai_skills:delete'
} as const



// 过滤列表
const filteredSkills = computed(() => {
  return skills.value.filter(skill => {
    return skill.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  })
})

// 获取技能列表
const fetchSkills = async () => {
  loading.value = true
  try {
    const res = await AISkillsAPI.listSkills(true)
    // API 返回结构: { skills: { name: string; description: string }[] }
    skills.value = res.data?.data?.skills;
  } catch (error) {
    console.error('Error fetching skills:', error)
    message.error('获取技能列表失败')
  } finally {
    loading.value = false
  }
}

// 点击创建按钮
const handleCreateClick = () => {
  isModalOpen.value = true
}

// 点击技能卡片
const handleSkillClick = (skill: string) => {
  selectedSkill.value = skill
}

// 删除技能
const handleDeleteSkill = async (skill: string) => {
  try {
    await dialog.confirm(
      `确定要删除技能 "${skill}" 吗？`,
      '删除技能',
      { type: 'danger', confirmText: '删除', cancelText: '取消' }
    )

    await AISkillsAPI.deleteSkill(skill)

    // 刷新技能列表
    await fetchSkills()
    message.success('技能删除成功')
  } catch (error) {
    if (error instanceof Error && error.message === 'Cancel') {
      return
    }
    console.error('Error deleting skill:', error)
    message.error('删除失败，请重试')
  }
}


// 成功回调
const handleCreateSuccess = () => {
  fetchSkills()
  isModalOpen.value = false
}

onMounted(() => {
  fetchSkills()
})
</script>
