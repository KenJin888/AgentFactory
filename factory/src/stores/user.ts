import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { api } from '@/services/api'
import { Auth } from '@/utils/auth';
import { UserInfo, InfoFormState, PasswordFormState, ResetPasswordForm } from '@/services/fastApi/module_system/user';
import type { MenuTable } from '@/services/fastApi/module_system/menu';

export const useUserStore = defineStore('user', () => {
  const userInfo = ref<UserInfo | null>(null);
  const isLoading = ref(false);
  const token = ref<string>(Auth.getAccessToken());
  const isLoggedIn = computed(() => !!token.value);
  const rememberMe = ref<boolean>(Auth.getRememberMe());
  const routeList = ref<MenuTable[]>([]);
  const prems = ref<string[]>([]);
  const hasGetRoute = ref(false);
  // 登录
  const login = async (data: any) => {
    isLoading.value = true;
    try {
      const rtn = await api.auth.login(data);
      setTokens(rtn.access_token, rtn.refresh_token, true);
      await loadUser();
      return rtn;
    } finally {
      isLoading.value = false;
    }
  };

  // 注册
  const register = async (data: any) => {
    isLoading.value = true;
    try {
      const result = await api.auth.register(data);
      return result;
    } finally {
      isLoading.value = false;
    }
  };

  // 重置密码
  const resetPassword = async (data: any) => {
    isLoading.value = true;
    try {
      const result = await api.auth.resetPassword(data);
      return result;
    } finally {
      isLoading.value = false;
    }
  };

  // 设置 tokens
  const setTokens = async (accessToken: string, refreshToken: string, isRemember: boolean) => {
    Auth.setTokens(accessToken, refreshToken, isRemember);
    token.value = accessToken;
    rememberMe.value = isRemember;
  };

  // 退出登录
  const loginOut = async () => {
    isLoading.value = true;
    try {
      Auth.clearAuth();
      userInfo.value = null;
      token.value = '';
      routeList.value = [];
      prems.value = [];
      hasGetRoute.value = false;
      try {
        const { usePermissionStore } = await import('@/stores/permission');
        usePermissionStore().resetRouter();
      } catch (_error) {}
    } finally {
      isLoading.value = false;
    }
  };

  const setPermissions = (menus: MenuTable[]) => {
    prems.value = [];
    const roleMenus =
      userInfo.value?.roles
        ?.filter((role) => role.menus && role.menus.length > 0)
        .flatMap((role) => role.menus as MenuTable[]) || [];
    const permissionSet = new Set<string>();
    const collect = (items: MenuTable[]) => {
      items.forEach((item) => {
        if (item.permission) {
          permissionSet.add(item.permission);
        }
        if (item.children && item.children.length > 0) {
          collect(item.children);
        }
      });
    };
    collect([...(menus || []), ...roleMenus]);
    prems.value = Array.from(permissionSet);
  };

  const setRoute = (menus: MenuTable[]) => {
    routeList.value = menus;
    hasGetRoute.value = true;
    setPermissions(menus);
  };

  // 加载用户信息
  let loadUserPromise: Promise<UserInfo | null> | null = null;
  const loadUser = async (refresh: boolean = false) => {
    if (userInfo.value == null || refresh) {
      if (loadUserPromise == null) {
        loadUserPromise = new Promise<UserInfo | null>(async (resolve) => {
          try {
            const info = await Auth.getCurrentUserInfo();
            if (!info) {
              userInfo.value = null;
              routeList.value = [];
              prems.value = [];
              hasGetRoute.value = false;
              resolve(null);
              return;
            }
            const menus = info.menus || [];
            const nextUserInfo = { ...info };
            delete (nextUserInfo as any).menus;
            userInfo.value = nextUserInfo;
            setRoute(menus);
            resolve(nextUserInfo);
          } catch (error) {
            console.error('Failed to load user info:', error);
            routeList.value = [];
            prems.value = [];
            hasGetRoute.value = false;
            resolve(null);
          } finally {
            loadUserPromise = null;
            isLoading.value = false;
          }
        });
      }
      userInfo.value = await loadUserPromise;
    }
    return userInfo.value;
  };

  // 更新用户信息
  const updateProfile = async (data: InfoFormState) => {
    isLoading.value = true;
    try {
      const result = await api.user.updateProfile(data);
      if (result.success) {
        await loadUser(true);
      }
      return result;
    } finally {
      isLoading.value = false;
    }
  };

  // 上传用户头像
  const uploadAvatar = async (formData: FormData) => {
    isLoading.value = true;
    try {
      const result = await api.user.uploadCurrentUserAvatar(formData);
      if (result.success) {
        await loadUser(true);
      }
      return result;
    } finally {
      isLoading.value = false;
    }
  };

  // 修改密码
  const changePassword = async (data: PasswordFormState) => {
    isLoading.value = true;
    try {
      const result = await api.user.changeCurrentUserPassword(data);
      return result;
    } finally {
      isLoading.value = false;
    }
  };

  // 重置用户密码
  const resetUserPassword = async (data: ResetPasswordForm) => {
    isLoading.value = true;
    try {
      const result = await api.user.resetUserPassword(data);
      return result;
    } finally {
      isLoading.value = false;
    }
  };

  // 获取用户列表
  const getUserList = async (query: any) => {
    isLoading.value = true;
    try {
      const result = await api.user.listUser(query);
      return result;
    } finally {
      isLoading.value = false;
    }
  };

  // 获取用户详情
  const getUserDetail = async (id: number) => {
    isLoading.value = true;
    try {
      const result = await api.user.detailUser(id);
      return result;
    } finally {
      isLoading.value = false;
    }
  };

  // 创建用户
  const createUser = async (data: any) => {
    isLoading.value = true;
    try {
      const result = await api.user.createUser(data);
      return result;
    } finally {
      isLoading.value = false;
    }
  };

  // 更新用户
  const updateUser = async (id: number, data: any) => {
    isLoading.value = true;
    try {
      const result = await api.user.updateUser(id, data);
      return result;
    } finally {
      isLoading.value = false;
    }
  };

  // 删除用户
  const deleteUser = async (ids: number[]) => {
    isLoading.value = true;
    try {
      const result = await api.user.deleteUser(ids);
      return result;
    } finally {
      isLoading.value = false;
    }
  };

  // 批量操作用户
  const batchUser = async (data: any) => {
    isLoading.value = true;
    try {
      const result = await api.user.batchUser(data);
      return result;
    } finally {
      isLoading.value = false;
    }
  };

  // 导出用户
  const exportUser = async (data: any) => {
    isLoading.value = true;
    try {
      const result = await api.user.exportUser(data);
      return result;
    } finally {
      isLoading.value = false;
    }
  };

  // 导入用户
  const importUser = async (formData: FormData) => {
    isLoading.value = true;
    try {
      const result = await api.user.importUser(formData);
      return result;
    } finally {
      isLoading.value = false;
    }
  };

  // 下载用户模板
  const downloadTemplateUser = async () => {
    isLoading.value = true;
    try {
      const result = await api.user.downloadTemplateUser();
      return result;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    // 状态
    userInfo,
    isLoading,
    token,
    isLoggedIn,
    rememberMe,
    routeList,
    prems,
    hasGetRoute,

    // 认证相关
    login,
    register,
    resetPassword,
    setTokens,
    loginOut,
    loadUser,
    setRoute,
    setPermissions,

    // 个人资料相关
    updateProfile,
    uploadAvatar,
    changePassword,

    // 管理员相关
    resetUserPassword,
    getUserList,
    getUserDetail,
    createUser,
    updateUser,
    deleteUser,
    batchUser,
    exportUser,
    importUser,
    downloadTemplateUser,
  };
});
