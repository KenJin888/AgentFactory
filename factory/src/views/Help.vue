<template>
  <div class="h-screen overflow-hidden bg-slate-50 flex flex-col font-sans">
    <!-- Header -->
    <header class="px-8 py-6 bg-slate-50 border-b border-gray-100 flex-shrink-0">
      <div class="max-w-6xl mx-auto flex flex-col md:flex-row gap-4 items-center justify-between">
        <div class="w-full md:w-auto flex-shrink-0">
          <h1 class="text-2xl font-bold text-slate-900">帮助中心</h1>
          <p class="mt-1 text-sm text-slate-500">查看产品功能说明与使用指引。</p>
        </div>
        <div class="w-full md:w-auto flex flex-col md:flex-row items-stretch md:items-center gap-3 md:justify-end">
          <button 
            @click="showAbout = true"
            class="h-11 px-5 text-slate-600 hover:text-blue-600 bg-slate-50 hover:bg-blue-50 rounded-xl font-medium transition-all flex items-center gap-2 border border-slate-200 hover:border-blue-200"
          >
            <Info :size="18" />
            关于我们
          </button>
        </div>
      </div>
    </header>

    <div class="flex-1 overflow-hidden w-full p-6 md:p-8">
      <div class="max-w-6xl mx-auto h-full flex flex-col">
        <!-- Selection View (Grid) -->
        <div v-if="!activeId" class="flex-1 overflow-y-auto animate-in fade-in duration-300 pr-2">
          <div v-for="(groupConcepts, groupName) in groupedConcepts" :key="groupName" class="mb-6">
            <div 
              class="flex items-center gap-2 mb-4 cursor-pointer select-none text-slate-800 hover:text-blue-600 transition-colors w-fit group"
              @click="toggleGroup(String(groupName))"
            >
              <component :is="expandedGroups[String(groupName)] ? ChevronDown : ChevronRight" :size="20" class="text-slate-400 group-hover:text-blue-500 transition-colors" />
              <h2 class="text-lg font-bold">{{ groupName }}</h2>
            </div>
            <div v-show="expandedGroups[String(groupName)]">
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 pb-4">
                <button 
                  v-for="item in groupConcepts" 
                  :key="item.id" 
                  @click="activeId = item.id"
                  class="flex items-start text-left p-6 rounded-xl border border-slate-200 bg-white hover:border-blue-300 hover:shadow-md hover:-translate-y-0.5 transition-all duration-200 group gap-5"
                >
                  <div class="bg-slate-50 p-3.5 rounded-xl text-slate-500 group-hover:bg-blue-50 group-hover:text-blue-600 transition-colors shrink-0 mt-1">
                    <component :is="getAgentCoverIconComponent(item.icon)" :size="28" stroke-width="1.5" />
                  </div>
                  <div>
                    <h3 class="font-bold text-lg text-slate-800 mb-1.5 group-hover:text-blue-700 transition-colors">{{ item.title }}</h3>
                    <p class="text-slate-500 text-sm leading-relaxed">{{ item.subtitle }}</p>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Detail View -->
        <main v-else-if="activeItem" class="flex-1 overflow-hidden flex flex-col h-full animate-in fade-in slide-in-from-right-4 duration-300 pr-2">
          <!-- Minimal Header -->
          <div class="flex items-center backdrop-blur-md sticky top-0 z-10">
            <button
              @click="activeId = null"
              class="text-slate-500 hover:text-slate-900 transition-colors flex items-center gap-2 text-sm font-medium px-3 py-1 rounded-lg hover:bg-slate-50 -ml-3"
            >
              <ArrowLeft :size="16" />
              返回
            </button>
          </div>
          
          <article class="flex-1 overflow-y-auto pb-20">
            <header class="mb-8 mt-4">
              <div class="flex items-center gap-4 mb-6">
                <div class="text-blue-600 bg-blue-50/50 p-2.5 rounded-xl">
                  <component :is="getAgentCoverIconComponent(activeItem.icon)" :size="24" stroke-width="2" />
                </div>
                <h1 class="text-xl md:text-2xl font-extrabold text-slate-900 tracking-tight">{{ activeItem.title }}</h1>
              </div>
            </header>

            <div class="prose prose-slate prose-lg max-w-none">
              <p class="text-slate-700 leading-relaxed mb-10 text-lg">
                {{ activeItem.description }}
              </p>
              
              <div v-if="activeItem.content" class="mb-12 markdown-body !text-base !bg-transparent">
                <NodeRenderer :content="activeItem.content" />
              </div>

              <div class="mb-12">
                <h4 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2">
                  提示
                </h4>
                <ul class="space-y-4 list-none pl-0 m-0">
                  <li v-for="(detail, idx) in activeItem.details" :key="idx" class="flex items-start gap-4 text-slate-700 leading-relaxed">
                    <span class="flex-shrink-0 flex items-center justify-center w-1.5 h-1.5 rounded-full bg-blue-500 mt-2.5"></span>
                    <span>{{ detail }}</span>
                  </li>
                </ul>
              </div>

              <div v-if="activeItem.related && activeItem.related.length > 0" class="pt-10 mt-10 border-t border-slate-100">
                 <h3 class="text-sm font-bold text-slate-400 uppercase tracking-wider mb-6">相关概念</h3>
                 <div class="flex flex-wrap gap-3">
                   <button 
                     v-for="relId in activeItem.related" 
                     :key="relId"
                     @click="activeId = relId"
                     class="px-4 py-2.5 bg-slate-50 text-slate-600 hover:bg-slate-100 hover:text-slate-900 rounded-xl text-sm font-medium transition-colors flex items-center gap-2 border border-transparent hover:border-slate-200"
                   >
                     <component :is="getConceptIcon(relId)" :size="16" />
                     {{ getConceptTitle(relId) }}
                   </button>
                 </div>
              </div>
            </div>
          </article>
        </main>
      </div>
    </div>

    <!-- 关于我们弹窗 -->
    <div v-if="showAbout" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-in fade-in duration-200" @click="showAbout = false">
      <div class="bg-white rounded-2xl shadow-xl max-w-md w-full overflow-hidden" @click.stop>
        <div class="p-6 border-b border-slate-100 flex justify-between items-center">
          <h2 class="text-xl font-bold text-slate-900 flex items-center gap-2">
            <Info class="text-blue-600" :size="24" />
            关于我们
          </h2>
          <button @click="showAbout = false" class="text-slate-400 hover:text-slate-600 p-1.5 rounded-lg hover:bg-slate-100 transition-colors">
            <X :size="20" />
          </button>
        </div>
        <div class="p-6">
          <div class="flex flex-col items-center text-center mb-6">
            <div class="w-20 h-20 bg-blue-600 rounded-2xl flex items-center justify-center mb-4 shadow-lg shadow-blue-900/50 overflow-hidden">
              <img src="@/assets/logo.png" alt="StarCityAI" class="w-20 h-20 object-contain" />
            </div>
            <h3 class="text-lg font-bold text-slate-900">StarCityAI</h3>
            <p class="text-sm text-slate-500 mt-1">版本 v0.5.6</p>
          </div>
          <div class="space-y-4 text-sm text-slate-600 leading-relaxed">
            <p>
              这是一个基于现代 Web 技术构建的智能体管理与对话平台，旨在帮助企业和开发者快速构建、管理和使用基于大语言模型的 AI 应用。
            </p>
            <div class="bg-slate-50 p-4 rounded-xl border border-slate-100">
              <ul class="space-y-3">
                <li class="flex justify-between items-center">
                  <span class="text-slate-500">核心功能</span>
                  <span class="font-medium text-slate-700">智能体、知识库、技能</span>
                </li>
                <li class="flex justify-between items-center">
                  <span class="text-slate-500">前端框架</span>
                  <span class="font-medium text-slate-700">Vue 3 + Tailwind CSS</span>
                </li>
                <li class="flex justify-between items-center">
                  <span class="text-slate-500">版权所有</span>
                  <span class="font-medium text-slate-700">&copy; 2026 StarCityAI</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div class="p-5 bg-slate-50 border-t border-slate-100 flex justify-end">
          <button @click="showAbout = false" class="px-6 py-2.5 bg-white border border-slate-200 text-slate-700 rounded-xl hover:bg-slate-50 hover:text-slate-900 transition-colors font-medium text-sm shadow-sm hover:shadow">
            关闭
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { 
  Info,
  ArrowLeft,
  X,
  ChevronDown,
  ChevronRight
} from 'lucide-vue-next';
import NodeRenderer from 'markstream-vue';
import { concepts } from '@/config/help';
import { getAgentCoverIconComponent } from '@/components/common/agentCover';

const activeId = ref<string | null>(null);
const showAbout = ref(false);

const groupedConcepts = computed(() => {
  const groups: Record<string, typeof concepts> = {};
  concepts.forEach(concept => {
    const groupName = concept.group || '其他';
    if (!groups[groupName]) {
      groups[groupName] = [];
    }
    groups[groupName].push(concept);
  });
  return groups;
});

const expandedGroups = ref<Record<string, boolean>>(
  Object.keys(groupedConcepts.value).reduce((acc, key) => {
    acc[key] = true;
    return acc;
  }, {} as Record<string, boolean>)
);

const toggleGroup = (groupName: string) => {
  expandedGroups.value[groupName] = !expandedGroups.value[groupName];
};

const activeItem = computed(() => concepts.find(c => c.id === activeId.value));

const getConceptTitle = (id: string) => {
  return concepts.find(c => c.id === id)?.title || id;
};

const getConceptIcon = (id: string) => {
  const iconStr = concepts.find(c => c.id === id)?.icon;
  return getAgentCoverIconComponent(iconStr);
};
</script>

<style scoped>
/* 自定义滚动条样式 */
.overflow-y-auto::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: #94a3b8;
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background-color: #64748b;
}

/* 兼容 Firefox */
.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: #94a3b8 transparent;
}
</style>
