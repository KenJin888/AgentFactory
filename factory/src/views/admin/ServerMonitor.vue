<template>
  <div class="min-h-screen bg-slate-50 p-8 overflow-y-auto">
    <div class="max-w-7xl mx-auto">
      <!-- 顶部导航栏 -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">服务器监控</h1>
          <p class="mt-1 text-sm text-slate-500">实时监控服务器运行状态和性能指标。</p>
        </div>
        <div class="flex gap-3">
          <button
            @click="fetchServerInfo"
            class="px-6 py-3 bg-slate-900 text-white rounded-xl font-bold hover:bg-slate-800 shadow-lg flex items-center gap-2 transition-transform active:scale-95"
          >
            <RefreshCwIcon :size="20" /> 刷新
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex flex-col items-center justify-center py-20">
        <Loader2Icon class="w-12 h-12 animate-spin text-blue-500 mb-4" />
        <span class="text-slate-500">加载中...</span>
      </div>

      <!-- Content -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- CPU Usage -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex items-center gap-2">
            <CpuIcon class="w-5 h-5 text-slate-600" />
            <span class="font-semibold text-slate-800">CPU使用情况</span>
            <div class="relative ml-2" @mouseenter="showCpuTooltip = true" @mouseleave="showCpuTooltip = false">
              <HelpCircleIcon class="w-4 h-4 text-slate-400 cursor-help" />
              <div v-if="showCpuTooltip" class="absolute left-6 top-0 w-48 p-2 bg-slate-800 text-white text-xs rounded-lg shadow-lg z-10">
                展示CPU核心数及使用率
              </div>
            </div>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-2 gap-4">
              <!-- CPU Cores -->
              <div class="bg-slate-50 rounded-xl p-4">
                <div class="text-sm text-slate-500 mb-4 text-center">核心数</div>
                <div class="flex justify-center mb-4">
                  <div class="relative w-32 h-32">
                    <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="45" fill="none" stroke="#e2e8f0" stroke-width="8" />
                      <circle cx="50" cy="50" r="45" fill="none" stroke="#3b82f6" stroke-width="8"
                        stroke-dasharray="283" stroke-dashoffset="0" stroke-linecap="round" />
                    </svg>
                    <div class="absolute inset-0 flex items-center justify-center">
                      <span class="text-3xl font-bold text-slate-800">{{ server.cpu?.cpu_num || 0 }}</span>
                    </div>
                  </div>
                </div>
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span class="text-slate-500">总核心数</span>
                    <span class="font-medium">{{ server.cpu?.cpu_num || 0 }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-slate-500">已用核心</span>
                    <span class="font-medium">{{ Math.floor(((server.cpu?.used || 0) * (server.cpu?.cpu_num || 0)) / 100) }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-slate-500">空闲核心</span>
                    <span class="font-medium">{{ Math.floor(((server.cpu?.free || 0) * (server.cpu?.cpu_num || 0)) / 100) }}</span>
                  </div>
                </div>
              </div>
              <!-- CPU Usage Rate -->
              <div class="bg-slate-50 rounded-xl p-4">
                <div class="text-sm text-slate-500 mb-4 text-center">使用率</div>
                <div class="flex justify-center mb-4">
                  <div class="relative w-32 h-32">
                    <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="45" fill="none" stroke="#e2e8f0" stroke-width="8" />
                      <circle cx="50" cy="50" r="45" fill="none"
                        :stroke="getCpuStatusColor()"
                        stroke-width="8"
                        :stroke-dasharray="283"
                        :stroke-dashoffset="283 - (283 * (server.cpu?.used || 0)) / 100"
                        stroke-linecap="round" />
                    </svg>
                    <div class="absolute inset-0 flex items-center justify-center">
                      <span class="text-3xl font-bold text-slate-800">{{ (server.cpu?.used || 0).toFixed(1) }}%</span>
                    </div>
                  </div>
                </div>
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span class="text-slate-500">用户使用率</span>
                    <span class="font-medium">{{ (server.cpu?.used || 0).toFixed(1) }}%</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-slate-500">系统使用率</span>
                    <span class="font-medium">{{ (server.cpu?.sys || 0).toFixed(1) }}%</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-slate-500">当前空闲率</span>
                    <span class="font-medium">{{ (server.cpu?.free || 0).toFixed(1) }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Memory Usage -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex items-center gap-2">
            <MemoryStickIcon class="w-5 h-5 text-slate-600" />
            <span class="font-semibold text-slate-800">内存使用情况</span>
            <div class="relative ml-2" @mouseenter="showMemTooltip = true" @mouseleave="showMemTooltip = false">
              <HelpCircleIcon class="w-4 h-4 text-slate-400 cursor-help" />
              <div v-if="showMemTooltip" class="absolute left-6 top-0 w-56 p-2 bg-slate-800 text-white text-xs rounded-lg shadow-lg z-10">
                展示系统内存和Python程序内存使用情况
              </div>
            </div>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-2 gap-4">
              <!-- System Memory -->
              <div class="bg-slate-50 rounded-xl p-4">
                <div class="text-sm text-slate-500 mb-4 text-center">系统内存</div>
                <div class="flex justify-center mb-4">
                  <div class="relative w-32 h-32">
                    <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="45" fill="none" stroke="#e2e8f0" stroke-width="8" />
                      <circle cx="50" cy="50" r="45" fill="none"
                        :stroke="getMemStatusColor()"
                        stroke-width="8"
                        :stroke-dasharray="283"
                        :stroke-dashoffset="283 - (283 * (server.mem?.usage || 0)) / 100"
                        stroke-linecap="round" />
                    </svg>
                    <div class="absolute inset-0 flex items-center justify-center">
                      <span class="text-2xl font-bold text-slate-800">{{ (server.mem?.usage || 0).toFixed(1) }}%</span>
                    </div>
                  </div>
                </div>
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span class="text-slate-500">总内存</span>
                    <span class="font-medium">{{ server.mem?.total || '-' }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-slate-500">已用内存</span>
                    <span class="font-medium">{{ server.mem?.used || '-' }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-slate-500">空闲内存</span>
                    <span class="font-medium">{{ server.mem?.free || '-' }}</span>
                  </div>
                </div>
              </div>
              <!-- Python Memory -->
              <div class="bg-slate-50 rounded-xl p-4">
                <div class="text-sm text-slate-500 mb-4 text-center">Python内存</div>
                <div class="flex justify-center mb-4">
                  <div class="relative w-32 h-32">
                    <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="45" fill="none" stroke="#e2e8f0" stroke-width="8" />
                      <circle cx="50" cy="50" r="45" fill="none"
                        :stroke="getPyMemStatusColor()"
                        stroke-width="8"
                        :stroke-dasharray="283"
                        :stroke-dashoffset="283 - (283 * (server.py?.memory_usage || 0)) / 100"
                        stroke-linecap="round" />
                    </svg>
                    <div class="absolute inset-0 flex items-center justify-center">
                      <span class="text-2xl font-bold text-slate-800">{{ (server.py?.memory_usage || 0).toFixed(1) }}%</span>
                    </div>
                  </div>
                </div>
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span class="text-slate-500">总内存</span>
                    <span class="font-medium">{{ server.py?.memory_total || '-' }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-slate-500">已用内存</span>
                    <span class="font-medium">{{ server.py?.memory_used || '-' }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-slate-500">空闲内存</span>
                    <span class="font-medium">{{ server.py?.memory_free || '-' }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Server Basic Info -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden lg:col-span-2">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex items-center gap-2">
            <MonitorIcon class="w-5 h-5 text-slate-600" />
            <span class="font-semibold text-slate-800">服务器基本信息</span>
            <div class="relative ml-2" @mouseenter="showSysTooltip = true" @mouseleave="showSysTooltip = false">
              <HelpCircleIcon class="w-4 h-4 text-slate-400 cursor-help" />
              <div v-if="showSysTooltip" class="absolute left-6 top-0 w-48 p-2 bg-slate-800 text-white text-xs rounded-lg shadow-lg z-10">
                展示服务器基本配置信息
              </div>
            </div>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="bg-slate-50 rounded-xl p-4">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">服务器名称</div>
                <div class="font-medium text-slate-900">{{ server.sys?.computer_name || '-' }}</div>
              </div>
              <div class="bg-slate-50 rounded-xl p-4">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">操作系统</div>
                <div class="font-medium text-slate-900">{{ server.sys?.os_name || '-' }}</div>
              </div>
              <div class="bg-slate-50 rounded-xl p-4">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">服务器IP</div>
                <div class="font-medium text-slate-900">{{ server.sys?.computer_ip || '-' }}</div>
              </div>
              <div class="bg-slate-50 rounded-xl p-4">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">系统架构</div>
                <div class="font-medium text-slate-900">{{ server.sys?.os_arch || '-' }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Python Environment -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden lg:col-span-2">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex items-center gap-2">
            <CodeIcon class="w-5 h-5 text-slate-600" />
            <span class="font-semibold text-slate-800">Python运行环境</span>
            <div class="relative ml-2" @mouseenter="showPyTooltip = true" @mouseleave="showPyTooltip = false">
              <HelpCircleIcon class="w-4 h-4 text-slate-400 cursor-help" />
              <div v-if="showPyTooltip" class="absolute left-6 top-0 w-56 p-2 bg-slate-800 text-white text-xs rounded-lg shadow-lg z-10">
                展示Python环境配置及运行状态
              </div>
            </div>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="bg-slate-50 rounded-xl p-4">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">Python名称</div>
                <div class="font-medium text-slate-900">{{ server.py?.name || '-' }}</div>
              </div>
              <div class="bg-slate-50 rounded-xl p-4">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">Python版本</div>
                <div class="font-medium text-slate-900">{{ server.py?.version || '-' }}</div>
              </div>
              <div class="bg-slate-50 rounded-xl p-4">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">启动时间</div>
                <div class="font-medium text-slate-900">{{ server.py?.start_time || '-' }}</div>
              </div>
              <div class="bg-slate-50 rounded-xl p-4">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">运行时长</div>
                <div class="font-medium text-slate-900">{{ server.py?.run_time || '-' }}</div>
              </div>
              <div class="bg-slate-50 rounded-xl p-4 md:col-span-2">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">安装路径</div>
                <div class="font-medium text-slate-900 break-all">{{ server.py?.home || '-' }}</div>
              </div>
              <div class="bg-slate-50 rounded-xl p-4 md:col-span-3">
                <div class="text-xs text-slate-500 mb-1 uppercase tracking-wide">项目路径</div>
                <div class="font-medium text-slate-900 break-all">{{ server.sys?.user_dir || '-' }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Disk Usage -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden lg:col-span-2">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex items-center gap-2">
            <HardDriveIcon class="w-5 h-5 text-slate-600" />
            <span class="font-semibold text-slate-800">磁盘使用情况</span>
            <div class="relative ml-2" @mouseenter="showDiskTooltip = true" @mouseleave="showDiskTooltip = false">
              <HelpCircleIcon class="w-4 h-4 text-slate-400 cursor-help" />
              <div v-if="showDiskTooltip" class="absolute left-6 top-0 w-48 p-2 bg-slate-800 text-white text-xs rounded-lg shadow-lg z-10">
                展示磁盘空间使用详情
              </div>
            </div>
          </div>
          <div class="p-6">
            <div v-if="server.disks?.length === 0" class="text-center py-8 text-slate-400">
              <InboxIcon class="w-12 h-12 mx-auto mb-2 text-slate-300" />
              <span>暂无数据</span>
            </div>
            <div v-else class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead class="bg-slate-50 text-slate-600 font-medium border-b border-slate-200">
                  <tr>
                    <th class="px-4 py-3 text-left">盘符路径</th>
                    <th class="px-4 py-3 text-center">文件系统</th>
                    <th class="px-4 py-3 text-left">盘符名称</th>
                    <th class="px-4 py-3 text-center">使用率</th>
                    <th class="px-4 py-3 text-center">总大小</th>
                    <th class="px-4 py-3 text-center">可用大小</th>
                    <th class="px-4 py-3 text-center">已用大小</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="disk in server.disks" :key="disk.dir_name" class="hover:bg-slate-50/80">
                    <td class="px-4 py-3">
                      <div class="max-w-[200px] truncate" :title="disk.dir_name">{{ disk.dir_name }}</div>
                    </td>
                    <td class="px-4 py-3 text-center">{{ disk.sys_type_name }}</td>
                    <td class="px-4 py-3">{{ disk.type_name }}</td>
                    <td class="px-4 py-3">
                      <div class="flex items-center gap-2">
                        <div class="flex-1 h-2 bg-slate-200 rounded-full overflow-hidden">
                          <div
                            class="h-full rounded-full transition-all"
                            :class="getDiskProgressColor(disk.usage)"
                            :style="{ width: `${disk.usage}%` }"
                          ></div>
                        </div>
                        <span class="text-xs w-10 text-right">{{ disk.usage }}%</span>
                      </div>
                    </td>
                    <td class="px-4 py-3 text-center">{{ disk.total }}</td>
                    <td class="px-4 py-3 text-center">{{ disk.free }}</td>
                    <td class="px-4 py-3 text-center">{{ disk.used }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { api } from '@/services/api';
import type { ServerInfo } from '@/services/fastApi/module_monitor/server';
import message from '@/components/common/message';
import {
  CpuIcon,
  MemoryStickIcon,
  MonitorIcon,
  CodeIcon,
  HardDriveIcon,
  HelpCircleIcon,
  RefreshCwIcon,
  Loader2Icon,
  InboxIcon
} from 'lucide-vue-next';

const loading = ref(false);
const showCpuTooltip = ref(false);
const showMemTooltip = ref(false);
const showSysTooltip = ref(false);
const showPyTooltip = ref(false);
const showDiskTooltip = ref(false);

const server = ref<ServerInfo>({
  cpu: {
    cpu_num: 0,
    used: 0,
    sys: 0,
    free: 0,
  },
  mem: {
    total: '',
    used: '',
    free: '',
    usage: 0,
  },
  sys: {
    computer_name: '',
    os_name: '',
    computer_ip: '',
    os_arch: '',
    user_dir: '',
  },
  py: {
    name: '',
    version: '',
    start_time: '',
    run_time: '',
    home: '',
    memory_total: '',
    memory_used: '',
    memory_free: '',
    memory_usage: 0,
  },
  disks: [],
});

const getCpuStatusColor = () => {
  const used = server.value.cpu?.used || 0;
  if (used > 80) return '#ef4444'; // red
  if (used > 60) return '#f59e0b'; // amber
  return '#22c55e'; // green
};

const getMemStatusColor = () => {
  const usage = server.value.mem?.usage || 0;
  if (usage > 80) return '#ef4444'; // red
  if (usage > 60) return '#f59e0b'; // amber
  return '#22c55e'; // green
};

const getPyMemStatusColor = () => {
  const usage = server.value.py?.memory_usage || 0;
  if (usage > 80) return '#ef4444'; // red
  if (usage > 60) return '#f59e0b'; // amber
  return '#22c55e'; // green
};

const getDiskProgressColor = (usage: number) => {
  if (usage > 80) return 'bg-red-500';
  if (usage > 60) return 'bg-amber-500';
  return 'bg-emerald-500';
};

const fetchServerInfo = async () => {
  loading.value = true;
  try {
    const res = await api.server.getServer();
    if (res?.data) {
      server.value = res.data;
    }
  } catch (error) {
    console.error('Failed to fetch server info:', error);
    message.error('获取服务器信息失败');
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchServerInfo();
});
</script>

<style scoped>
/* Custom scrollbar for table */
.overflow-x-auto::-webkit-scrollbar {
  height: 6px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
