<template>
  <div class="min-h-screen flex">
    <div class="hidden lg:flex w-1/2 bg-blue-600 p-12 flex-col justify-between relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-blue-600 to-indigo-900 opacity-90" />
      <div class="relative z-10">
        <div class="flex items-center gap-3 text-white mb-12">
          <div class="w-10 h-10 bg-slate-900/30 backdrop-blur rounded-xl flex items-center justify-center">
            <img :src="webLogo" :alt="webTitle" class="w-8 h-8 object-contain" />
          </div>
          <span class="text-2xl tracking-tight">{{ webTitle }}</span>
        </div>
        <h1 class="text-5xl font-bold text-white mb-6 leading-tight">
          {{ webSlogan1 }} <br /> {{ webSlogan2 }}
        </h1>
        <p class="text-blue-100 text-lg max-w-md leading-relaxed">
          {{ webDescription }}
        </p>
      </div>
      <div class="relative z-10 text-blue-200 text-sm">
        {{ webCopyright }}
      </div>
    </div>

    <div class="flex-1 flex items-center justify-center p-8 bg-white">
      <div class="w-full max-w-md space-y-8">
        <!-- 登录面板 -->
        <template v-if="currentPanel === 'login'">
        <div class="text-center lg:text-left">
          <h2 class="text-3xl font-bold text-slate-900">欢迎回来</h2>
          <div class="mt-2 flex items-center justify-between">
            <p class="text-slate-500">请登录您的账号以继续</p>
            <a href="#" @click.prevent="switchPanel('resetPwd')" class="text-sm text-blue-600 hover:text-blue-700 font-medium">忘记密码?</a>
          </div>
        </div>

          <form @submit.prevent="handleLoginSubmit" class="space-y-6">
          <div class="space-y-2">
            <label class="text-sm font-medium text-slate-700">用户名</label>
            <input 
                type="text" 
                required
                v-model="loginForm.username"
                class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                placeholder="请输入用户名"
              />
          </div>

          <div class="space-y-2">
              <label class="text-sm font-medium text-slate-700">密码</label>
            <input 
              type="password" 
              required
                v-model="loginForm.password"
              class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                placeholder="请输入密码"
            />
          </div>

          <div v-if="error" class="p-4 bg-red-50 text-red-600 text-sm rounded-xl flex items-center gap-2 animate-in fade-in slide-in-from-top-2">
            <AlertCircle :size="16" /> {{ error }}
          </div>

          <button 
            type="submit" 
            :disabled="loading"
            class="w-full py-3.5 bg-blue-600 text-white rounded-xl font-bold hover:bg-blue-700 focus:ring-4 focus:ring-blue-100 transition-all active:scale-[0.98] flex items-center justify-center"
          >
            <Loader2 v-if="loading" class="animate-spin" />
            <span v-else>登 录 →</span>
          </button>
        </form>

        <p class="text-center text-sm text-slate-500">
            还没有账号? <a href="#" @click.prevent="switchPanel('register')" class="text-blue-600 font-bold hover:underline">马上注册</a>
          </p>
        </template>

        <!-- 注册面板 -->
        <template v-else-if="currentPanel === 'register'">
          <div class="text-center lg:text-left">
            <h2 class="text-3xl font-bold text-slate-900">注册账号</h2>
            <p class="text-slate-500 mt-2">创建您的新账号</p>
          </div>

          <form @submit.prevent="handleRegisterSubmit" class="space-y-6">
            <div class="space-y-2">
              <label class="text-sm font-medium text-slate-700">用户名</label>
              <input 
                type="text" 
                required
                v-model="registerForm.username"
                class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                placeholder="请输入用户名"
              />
            </div>

            <div class="space-y-2">
              <label class="text-sm font-medium text-slate-700">密码</label>
              <input 
                type="password" 
                required
                v-model="registerForm.password"
                class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                placeholder="请输入密码"
              />
            </div>

            <div class="space-y-2">
              <label class="text-sm font-medium text-slate-700">确认密码</label>
              <input 
                type="password" 
                required
                v-model="registerForm.confirmPassword"
                class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                placeholder="请再次输入密码"
              />
            </div>

            <div v-if="error" class="p-4 bg-red-50 text-red-600 text-sm rounded-xl flex items-center gap-2 animate-in fade-in slide-in-from-top-2">
              <AlertCircle :size="16" /> {{ error }}
            </div>

            <button 
              type="submit" 
              :disabled="loading"
              class="w-full py-3.5 bg-blue-600 text-white rounded-xl font-bold hover:bg-blue-700 focus:ring-4 focus:ring-blue-100 transition-all active:scale-[0.98] flex items-center justify-center"
            >
              <Loader2 v-if="loading" class="animate-spin" />
              <span v-else>注 册 →</span>
            </button>
          </form>

          <p class="text-center text-sm text-slate-500">
            已有账号? <a href="#" @click.prevent="switchPanel('login')" class="text-blue-600 font-bold hover:underline">立即登录</a>
          </p>
        </template>

        <!-- 重置密码面板 -->
        <template v-else-if="currentPanel === 'resetPwd'">
          <div class="text-center lg:text-left">
            <h2 class="text-3xl font-bold text-slate-900">重置密码</h2>
            <p class="text-slate-500 mt-2">请输入您的用户名重置密码</p>
          </div>

          <form @submit.prevent="handleResetPwdSubmit" class="space-y-6">
            <div class="space-y-2">
              <label class="text-sm font-medium text-slate-700">用户名</label>
              <input 
                type="text" 
                required
                v-model="resetForm.username"
                class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                placeholder="请输入用户名"
              />
            </div>

            <div class="space-y-2">
              <label class="text-sm font-medium text-slate-700">新密码</label>
              <input 
                type="password" 
                required
                v-model="resetForm.newPassword"
                class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                placeholder="请输入新密码"
              />
            </div>

            <div class="space-y-2">
              <label class="text-sm font-medium text-slate-700">确认新密码</label>
              <input 
                type="password" 
                required
                v-model="resetForm.confirmPassword"
                class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                placeholder="请再次输入新密码"
              />
            </div>

            <div v-if="error" class="p-4 bg-red-50 text-red-600 text-sm rounded-xl flex items-center gap-2 animate-in fade-in slide-in-from-top-2">
              <AlertCircle :size="16" /> {{ error }}
            </div>

            <button 
              type="submit" 
              :disabled="loading"
              class="w-full py-3.5 bg-blue-600 text-white rounded-xl font-bold hover:bg-blue-700 focus:ring-4 focus:ring-blue-100 transition-all active:scale-[0.98] flex items-center justify-center"
            >
              <Loader2 v-if="loading" class="animate-spin" />
              <span v-else>重置密码 →</span>
            </button>
          </form>

          <p class="text-center text-sm text-slate-500">
            想起密码了? <a href="#" @click.prevent="switchPanel('login')" class="text-blue-600 font-bold hover:underline">返回登录</a>
        </p>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Loader2, AlertCircle } from 'lucide-vue-next'
import defaultLogo from '@/assets/logo.png'

import { useUserStore } from '@/stores/user';
import { useConfigStore } from '@/stores/config'
// 定义组件属性
const props = defineProps<{
  // 可选的登录成功回调
  onLogin?: () => void
}>()

const userStore = useUserStore()
const configStore = useConfigStore()
const webTitle = computed(() => configStore.getConfigValue('sys_web_title', 'AgnetFactory'))
const webLogo = computed(() => configStore.getConfigValue('sys_web_logo', defaultLogo))
const webSlogan1 = computed(() => configStore.getConfigValue('sys_web_slogan1', '释放'))
const webSlogan2 = computed(() => configStore.getConfigValue('sys_web_slogan2', 'AI 生产力'))
const webDescription = computed(() => configStore.getConfigValue('sys_web_description', '专为智能体设计的企业管理平台'))
const webCopyright = computed(() => configStore.getConfigValue('sys_web_copyright', '© 2026 AgnetFactory'))

onMounted(async () => {
  await configStore.getConfig()
})
// 当前面板: login | register | resetPwd
type PanelType = 'login' | 'register' | 'resetPwd'
const currentPanel = ref<PanelType>('login')

// 切换面板
const switchPanel = (panel: PanelType) => {
  currentPanel.value = panel
  error.value = ''
  loading.value = false
}

// 登录表单
const loginForm = reactive({ username: '', password: '' })

// 注册表单
const registerForm = reactive({ username: '', password: '', confirmPassword: '' })

// 重置密码表单
const resetForm = reactive({ username: '', newPassword: '', confirmPassword: '' })

const loading = ref(false)
const error = ref('')

// Vue Router 实例
const router = useRouter()
const route = useRoute()

const resolveRedirectPath = () => {
  const redirect = route.query.redirect
  if (typeof redirect === 'string' && redirect.startsWith('/')) {
    return redirect
  }
  return '/'
}

// 登录提交
const handleLoginSubmit = async () => {
  loading.value = true
  error.value = ''

  try {
    await userStore.login(loginForm)
    router.push(resolveRedirectPath())
  } catch (err: any) {
    console.error(err)
    error.value = err.message || '无法连接到服务器'
  } finally {
    loading.value = false
  }
}

// 注册提交
const handleRegisterSubmit = async () => {
  loading.value = true
  error.value = ''

  // 验证密码是否一致
  if (registerForm.password !== registerForm.confirmPassword) {
    error.value = '两次输入的密码不一致'
    loading.value = false
    return
  }

  try {
    await userStore.register({
      username: registerForm.username,
      password: registerForm.password,
      confirmPassword: registerForm.confirmPassword
    });
    await userStore.login({
      username: registerForm.username,
      password: registerForm.password
    })
    await userStore.loadUser(true)
    router.push(resolveRedirectPath())
  } catch (err: any) {
    console.error(err)
    error.value = err.message || '注册失败'
  } finally {
    loading.value = false
  }
}

// 重置密码提交
const handleResetPwdSubmit = async () => {
  loading.value = true
  error.value = ''
  // 验证密码是否一致
  if (resetForm.newPassword !== resetForm.confirmPassword) {
    error.value = '两次输入的密码不一致'
    loading.value = false
    return
  }
  try {
    // 发送重置密码请求
    await userStore.resetPassword({
      username: resetForm.username,
      new_password: resetForm.newPassword,
      confirmPassword: resetForm.confirmPassword
    })

    // 重置成功后切换到登录页
    error.value = ''
    alert('密码重置成功，请使用新密码登录')
    switchPanel('login')
  } catch (err: any) {
    console.error(err)
    error.value = err.message || '重置密码失败'
  } finally {
    loading.value = false
  }
}
</script>
