import { computed, type ComputedRef, type Ref, unref } from 'vue'
import { useUserStore } from '@/stores/user'
import { ROLE_ROOT } from '@/utils/auth'

export interface CrudPerms {
  list?: string
  create?: string
  update?: string
  delete?: string
  export?: string
  import?: string
  batch?: string
  detail?: string
  permission?: string
  [key: string]: string | undefined
}

export interface UseCrudAuthReturn {
  can: (key: keyof CrudPerms) => boolean
  canList: ComputedRef<boolean>
  canCreate: ComputedRef<boolean>
  canUpdate: ComputedRef<boolean>
  canDelete: ComputedRef<boolean>
  canExport: ComputedRef<boolean>
  canImport: ComputedRef<boolean>
  canBatch: ComputedRef<boolean>
  canDetail: ComputedRef<boolean>
  canPermission: ComputedRef<boolean>
  isSuper: ComputedRef<boolean>
  isRoot: ComputedRef<boolean>
  hasWildcard: ComputedRef<boolean>
  userPerms: ComputedRef<string[]>
}

/**
 * CRUD 页面权限管理组合式函数
 * @param perms - 权限配置对象或 Ref
 * @example
 * const PERMS = {
 *   list: 'module_system:role:query',
 *   create: 'module_system:role:create',
 *   update: 'module_system:role:update',
 *   delete: 'module_system:role:delete',
 *   export: 'module_system:role:export',
 *   batch: 'module_system:role:batch'
 * }
 * const { can, canCreate, canDelete, isSuper } = useCrudAuth(PERMS)
 *
 * // 模板中使用
 * <button v-has-perm="PERMS.create" :disabled="!canCreate">新增</button>
 * <button @click="handleDelete" :disabled="!can('delete')">删除</button>
 */
export function useCrudAuth<P extends CrudPerms | Ref<CrudPerms>>(perms: P = {} as P): UseCrudAuthReturn {
  const userStore = useUserStore()

  const userPerms = computed(() => userStore.prems || [])
  const userRoles = computed(() =>
    userStore.userInfo?.roles?.map((role) => String(role.code || '').trim()).filter(Boolean) || []
  )
  const isSuper = computed(() => !!userStore.userInfo?.is_superuser)
  const isRoot = computed(() => userRoles.value.includes(ROLE_ROOT))
  const hasWildcard = computed(() => userPerms.value.includes('*:*:*'))

  /**
   * 检查是否拥有指定权限
   * 超管、ROOT角色、通配符权限拥有所有权限
   */
  const checkPerm = (perm?: string): boolean => {
    if (!perm) return true
    if (isSuper.value || isRoot.value || hasWildcard.value) return true
    return userPerms.value.includes(perm)
  }

  /**
   * 通用权限检查函数
   */
  const can = (key: keyof CrudPerms): boolean => {
    const permsValue = unref(perms)
    return checkPerm(permsValue[key])
  }

  // 预计算的常用权限
  const canList = computed(() => can('list'))
  const canCreate = computed(() => can('create'))
  const canUpdate = computed(() => can('update'))
  const canDelete = computed(() => can('delete'))
  const canExport = computed(() => can('export'))
  const canImport = computed(() => can('import'))
  const canBatch = computed(() => can('batch'))
  const canDetail = computed(() => can('detail'))
  const canPermission = computed(() => can('permission'))

  return {
    can,
    canList,
    canCreate,
    canUpdate,
    canDelete,
    canExport,
    canImport,
    canBatch,
    canDetail,
    canPermission,
    isSuper,
    isRoot,
    hasWildcard,
    userPerms
  }
}

export default useCrudAuth
