<template>
  <div class="min-h-screen bg-slate-50 p-8 overflow-y-auto">
    <div class="max-w-6xl mx-auto">
      <!-- 顶部导航栏 -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-2xl font-bold text-slate-900">个人中心</h1>
          <p class="mt-1 text-sm text-slate-500">管理账号资料与安全设置。</p>
        </div>
        <div class="flex items-center gap-6">
          <button @click="openHelp" class="flex items-center gap-2 text-slate-500 hover:text-slate-900 transition-colors">
            <HelpCircle class="w-5 h-5" />
            <span class="text-sm font-medium">帮助中心</span>
          </button>
          <button @click="handleLogout" class="flex items-center gap-2 text-rose-500 hover:text-rose-600 transition-colors">
            <LogOut class="w-5 h-5" />
            <span class="text-sm font-medium">退出登录</span>
          </button>
        </div>
      </div>

      <!-- 主卡片 -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
        <!-- 顶部横幅 -->
        <div class="h-32 bg-gradient-to-r from-blue-50 to-blue-100"></div>

        <!-- 内容区域 -->
        <div class="px-10 pb-10">
          <!-- 头像和基本信息 -->
          <div class="relative flex items-end justify-between -mt-12 mb-8">
            <div class="flex items-end gap-6">
              <!-- 头像 - 非编辑模式 -->
              <div v-if="!isEditing" class="relative">
                <div class="w-28 h-28 rounded-2xl bg-white p-1.5 shadow-lg border border-slate-100 overflow-hidden">
                  <img v-if="userInfo?.avatar" :src="userInfo.avatar" class="w-full h-full object-cover rounded-xl" alt="avatar" />
                  <div v-else class="w-full h-full bg-blue-50 flex items-center justify-center text-blue-300 rounded-xl">
                    <UserIcon class="w-12 h-12" />
                  </div>
                </div>
              </div>

              <!-- 头像 - 编辑模式 -->
              <div v-else class="relative group">
                <div
                  class="w-28 h-28 rounded-2xl bg-white p-1.5 shadow-lg border border-slate-100 overflow-hidden cursor-pointer"
                  @click="avatarInputRef?.click()"
                >
                  <img v-if="editForm.avatar" :src="editForm.avatar" class="w-full h-full object-cover rounded-xl" alt="avatar" />
                  <div v-else class="w-full h-full bg-blue-50 flex items-center justify-center text-blue-300 rounded-xl">
                    <UserIcon class="w-12 h-12" />
                  </div>
                  <!-- 上传中遮罩 -->
                  <div v-if="avatarUploading" class="absolute inset-0 bg-black/50 flex items-center justify-center rounded-xl">
                    <Loader2 class="w-6 h-6 animate-spin text-white" />
                  </div>
                  <!-- 悬停遮罩 -->
                  <div v-else class="absolute inset-0 bg-black/40 flex flex-col items-center justify-center text-white opacity-0 group-hover:opacity-100 transition-opacity rounded-xl">
                    <Camera class="w-6 h-6" />
                    <span class="text-xs font-medium mt-1">更换头像</span>
                  </div>
                </div>
                <input type="file" ref="avatarInputRef" class="hidden" accept="image/png, image/jpeg, image/jpg" @change="handleAvatarUpload" />
              </div>

              <!-- 用户信息 -->
              <div class="pb-2">
                <h2 class="text-2xl font-bold text-slate-900">{{ userInfo?.name || userInfo?.username || '-' }}</h2>
                <p class="text-slate-500 mt-1">
                  {{ userPositions }} {{ userDept }} @{{ userInfo?.username || '-' }}
                </p>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="flex items-center gap-3 pb-2">
              <template v-if="!isEditing">
                <button
                  @click="showPasswordModal = true"
                  class="flex items-center gap-2 px-5 py-2.5 bg-white border border-slate-200 text-slate-700 rounded-xl font-medium hover:bg-slate-50 hover:border-slate-300 transition-all"
                >
                  <Lock class="w-4 h-4" />
                  修改密码
                </button>
                <button
                  @click="startEdit"
                  class="flex items-center gap-2 px-5 py-2.5 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 transition-all shadow-sm"
                >
                  <Pencil class="w-4 h-4" />
                  编辑资料
                </button>
              </template>
              <template v-else>
                <button
                  @click="cancelEdit"
                  class="flex items-center gap-2 px-5 py-2.5 bg-white border border-slate-200 text-slate-700 rounded-xl font-medium hover:bg-slate-50 hover:border-slate-300 transition-all"
                >
                  <X class="w-4 h-4" />
                  取消
                </button>
                <button
                  @click="saveProfile"
                  :disabled="saving"
                  class="flex items-center gap-2 px-5 py-2.5 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Save class="w-4 h-4" />
                  {{ saving ? '保存中...' : '保存' }}
                </button>
              </template>
            </div>
          </div>

          <!-- 信息表单 -->
          <div class="space-y-6">
            <!-- 姓名 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">姓名</label>
              <div v-if="!isEditing" class="flex items-center gap-3 text-slate-900">
                <UserIcon class="w-5 h-5 text-slate-400" />
                <span class="text-lg">{{ userInfo?.name || userInfo?.username || '-' }}</span>
              </div>
              <input
                v-else
                v-model="editForm.name"
                type="text"
                class="w-full max-w-md px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                placeholder="请输入姓名"
              />
            </div>

            <!-- 手机号码 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">手机号码</label>
              <div v-if="!isEditing" class="flex items-center gap-3 text-slate-900">
                <Phone class="w-5 h-5 text-slate-400" />
                <span class="text-lg">{{ userInfo?.mobile || '-' }}</span>
              </div>
              <input
                v-else
                v-model="editForm.mobile"
                type="tel"
                class="w-full max-w-md px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                placeholder="请输入手机号码"
              />
            </div>

            <!-- 电子邮箱 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">电子邮箱</label>
              <div v-if="!isEditing" class="flex items-center gap-3 text-slate-900">
                <Mail class="w-5 h-5 text-slate-400" />
                <span class="text-lg">{{ userInfo?.email || '-' }}</span>
              </div>
              <input
                v-else
                v-model="editForm.email"
                type="email"
                class="w-full max-w-md px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                placeholder="请输入电子邮箱"
              />
            </div>

            <!-- 用户角色 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-3">用户角色</label>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="role in userRoles"
                  :key="role"
                  class="px-4 py-2 bg-blue-50 border border-blue-100 rounded-lg text-sm font-medium text-blue-700"
                >
                  {{ role }}
                </span>
              </div>
              <p class="text-xs text-slate-400 mt-3">* 用户角色由系统管理员分配，不可自行修改</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 修改密码弹窗 -->
    <Teleport to="body">
      <div v-if="showPasswordModal" class="fixed inset-0 z-50 flex items-center justify-center">
        <!-- 遮罩 -->
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showPasswordModal = false"></div>

        <!-- 弹窗内容 -->
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4 p-8">
          <h3 class="text-xl font-bold text-slate-900 mb-6">修改密码</h3>

          <div class="space-y-5">
            <!-- 当前密码 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">当前密码</label>
              <input
                v-model="passwordForm.old_password"
                type="password"
                class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                placeholder="请输入当前密码"
              />
            </div>

            <!-- 新密码 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">新密码</label>
              <input
                v-model="passwordForm.new_password"
                type="password"
                class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                placeholder="请输入新密码"
              />
            </div>

            <!-- 确认新密码 -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">确认新密码</label>
              <input
                v-model="passwordForm.confirm_password"
                type="password"
                class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 focus:outline-none focus:ring-4 focus:ring-blue-50 focus:border-blue-400 transition-all"
                placeholder="请再次输入新密码"
              />
            </div>
          </div>

          <!-- 按钮 -->
          <div class="flex items-center gap-3 mt-8">
            <button
              @click="showPasswordModal = false"
              class="flex-1 px-5 py-3 bg-white border border-slate-200 text-slate-700 rounded-xl font-medium hover:bg-slate-50 hover:border-slate-300 transition-all"
            >
              取消
            </button>
            <button
              @click="changePassword"
              :disabled="changingPassword"
              class="flex-1 px-5 py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ changingPassword ? '修改中...' : '确认修改' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>


  </div>
</template>

<script setup lang="ts">
import {computed, onMounted, reactive, ref} from 'vue';
import {useRouter} from 'vue-router';
import {
  Camera,
  HelpCircle,
  Loader2,
  Lock,
  LogOut,
  Mail,
  Pencil,
  Phone,
  Save,
  User as UserIcon,
  X
} from 'lucide-vue-next';
import {useUserStore} from '@/stores/user';
import message from '@/components/common/message';
import {dialog} from '@/components/common/dialog';
import {redirectToAppBase} from '@/utils/navigation';

const router = useRouter();
const userStore = useUserStore();

// 用户信息
const userInfo = computed(() => userStore.userInfo);

// 用户岗位（从 positions 数组中获取）
const userPositions = computed(() => {
  if (!userInfo.value?.positions || userInfo.value.positions.length === 0) {
    return '';
  }
  return userInfo.value.positions.map((p: any) => p.name).join('、');
});

// 用户部门（从 dept 对象中获取）
const userDept = computed(() => {
  return userInfo.value?.dept?.name || '-';
});

// 用户角色（从用户信息中获取）
const userRoles = computed(() => {
  if (userInfo.value?.is_superuser) {
    return ['超级管理员'];
  }
  return userInfo.value?.roles?.map((r: any) => r.name) || ['普通用户'];
});

// 编辑状态
const isEditing = ref(false);
const saving = ref(false);

// 编辑表单
const editForm = reactive({
  name: '',
  mobile: '',
  email: '',
  avatar: ''
});

// 密码弹窗
const showPasswordModal = ref(false);
const changingPassword = ref(false);
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
});

// 头像相关
const avatarInputRef = ref<HTMLInputElement | null>(null);
const avatarUploading = ref(false);

// 开始编辑
const startEdit = () => {
  editForm.name = userInfo.value?.name || userInfo.value?.username || '';
  editForm.mobile = userInfo.value?.mobile || '';
  editForm.email = userInfo.value?.email || '';
  editForm.avatar = userInfo.value?.avatar || '';
  isEditing.value = true;
};

// 取消编辑
const cancelEdit = () => {
  isEditing.value = false;
};

// 保存资料
const saveProfile = async () => {
  saving.value = true;
  try {
    const result = await userStore.updateProfile({
      name: editForm.name,
      mobile: editForm.mobile,
      email: editForm.email,
      avatar: editForm.avatar
    });

    if (result.success) {
      message.success('保存成功');
      isEditing.value = false;
    } else {
      message.error(result.msg || '保存失败');
    }
  } catch (error: any) {
    message.error(error?.message || '保存失败，请稍后重试');
  } finally {
    saving.value = false;
  }
};

// 修改密码
const changePassword = async () => {
  // 验证
  if (!passwordForm.old_password) {
    message.warning('请输入当前密码');
    return;
  }
  if (!passwordForm.new_password) {
    message.warning('请输入新密码');
    return;
  }
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    message.warning('两次输入的新密码不一致');
    return;
  }

  changingPassword.value = true;
  try {
    const result = await userStore.changePassword({
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password,
      confirm_password: passwordForm.confirm_password
    });

    if (result.success) {
      message.success('密码修改成功');
      showPasswordModal.value = false;
      // 清空表单
      passwordForm.old_password = '';
      passwordForm.new_password = '';
      passwordForm.confirm_password = '';
    } else {
      message.error(result.msg || '密码修改失败');
    }
  } catch (error: any) {
    message.error(error?.message || '密码修改失败，请稍后重试');
  } finally {
    changingPassword.value = false;
  }
};

// 处理头像上传 - 只更新本地表单数据
const handleAvatarUpload = async (e: Event) => {
  const target = e.target as HTMLInputElement;
  const file = target.files?.[0];
  if (!file) return;

  // 验证文件类型
  if (!['image/jpeg', 'image/png', 'image/jpg'].includes(file.type)) {
    message.error('仅支持 JPG 或 PNG 格式');
    return;
  }

  // 验证文件大小 (1MB)
  if (file.size > 1024 * 1024) {
    message.error('图片大小不能超过 1MB');
    return;
  }

  avatarUploading.value = true;
  const uploadData = new FormData();
  uploadData.append('file', file);

  try {
    const res = await userStore.uploadAvatar(uploadData);
    // res 是 ApiResponse<UploadFilePath> 结构，实际数据在 res.data 中
    if (res && res.data && res.data.file_url) {
      // 只更新本地表单数据，不立即保存
      editForm.avatar = res.data.file_url;
      message.success('头像上传成功');
    } else {
      message.error('上传失败，请重试');
    }
  } catch (error: any) {
    console.error('Avatar upload failed:', error);
    message.error(error?.message || '头像上传失败');
  } finally {
    avatarUploading.value = false;
    // 清空 input 值，允许重复选择同一文件
    if (avatarInputRef.value) {
      avatarInputRef.value.value = '';
    }
  }
};

// 打开帮助
const openHelp = () => {
  router.push({ name: 'Help' });
};

// 退出登录
const handleLogout = async () => {
  try {
    await dialog.confirm("确定退出登录？");
    await userStore.loginOut();
    redirectToAppBase();
  } catch {
    // cancelled
  }
};

// 初始化
onMounted(() => {
  userStore.loadUser();
});
</script>
