import type { Directive, DirectiveBinding } from 'vue'
import { useUserStore } from '@/stores/user'
import { ROLE_ROOT } from '@/utils/auth'

type MaybeArray<T> = T | T[]

const normalizeToStringArray = (value: unknown): string[] => {
  if (Array.isArray(value)) {
    return value.map((item) => String(item)).filter(Boolean)
  }
  if (typeof value === 'string') {
    const trimmed = value.trim()
    return trimmed ? [trimmed] : []
  }
  return []
}

const removeElement = (el: HTMLElement) => {
  const parent = el.parentNode
  if (!parent) {
    return
  }
  parent.removeChild(el)
}

const hasWildcardPermission = (perms: string[]) => perms.includes('*:*:*')

const isRootRole = (codes: string[]) => codes.includes(ROLE_ROOT)

const applyPerm = (el: HTMLElement, binding: DirectiveBinding<MaybeArray<string>>) => {
  const requiredValue = binding.value
  if (!requiredValue || (typeof requiredValue !== 'string' && !Array.isArray(requiredValue))) {
    throw new Error('需要提供权限标识！例如：v-has-perm="\'sys:user:add\'" 或 v-has-perm="[\'sys:user:add\', \'sys:user:edit\']"')
  }
  const required = normalizeToStringArray(binding.value)
  if (required.length === 0) {
    return
  }
  const userStore = useUserStore()
  const isSuperuser = Boolean(userStore.userInfo?.is_superuser)
  if (isSuperuser) {
    return
  }
  const userPerms = userStore.prems || []
  const roleCodes =
    userStore.userInfo?.roles?.map((role) => String(role.code || '').trim()).filter(Boolean) || []

  if (isRootRole(roleCodes) || hasWildcardPermission(userPerms) || required.includes('*:*:*')) {
    return
  }
  const ok = required.some((perm) => userPerms.includes(perm))
  if (!ok) {
    removeElement(el)
  }
}

const applyRole = (el: HTMLElement, binding: DirectiveBinding<MaybeArray<string>>) => {
  const requiredValue = binding.value
  if (!requiredValue || (typeof requiredValue !== 'string' && !Array.isArray(requiredValue))) {
    throw new Error('需要提供角色标识！例如：v-has-role="\'ADMIN\'" 或 v-has-role="[\'ADMIN\', \'TEST\']"')
  }
  const required = normalizeToStringArray(binding.value)
  if (required.length === 0) {
    return
  }
  const userStore = useUserStore()
  const isSuperuser = Boolean(userStore.userInfo?.is_superuser)
  if (isSuperuser) {
    return
  }
  const roleCodes =
    userStore.userInfo?.roles?.map((role) => String(role.code || '').trim()).filter(Boolean) || []
  if (isRootRole(roleCodes)) {
    return
  }
  const ok = required.some((code) => roleCodes.includes(code))
  if (!ok) {
    removeElement(el)
  }
}

export const hasPerm: Directive<HTMLElement, MaybeArray<string>> = {
  mounted: applyPerm,
  updated: applyPerm
}

export const hasRole: Directive<HTMLElement, MaybeArray<string>> = {
  mounted: applyRole,
  updated: applyRole
}
