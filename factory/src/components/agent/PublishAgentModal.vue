<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm">
    <div class="bg-white rounded-2xl w-full max-w-3xl shadow-2xl overflow-hidden">
      <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
        <div>
          <h3 class="text-lg font-bold text-slate-800">{{ modalTitle }}</h3>
          <p class="mt-1 text-sm text-slate-500">{{ modalDescription }}</p>
        </div>
        <button
          type="button"
          class="text-slate-400 hover:text-slate-600 transition-colors"
          :disabled="loading"
          @click="$emit('close')"
        >
          <X :size="18" />
        </button>
      </div>

      <div class="p-6 space-y-5 max-h-[75vh] overflow-y-auto">
        <div
            :class="isOverwrite ? 'bg-amber-50 border-amber-200 text-amber-700' : 'bg-blue-50 border-blue-200 text-blue-700'"
            class="rounded-xl border px-4 py-3 text-sm"
        >
          {{ noticeText }}
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-bold text-slate-700 mb-2">智能体名称</label>
            <input
                v-model="formName"
                class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-500"
                maxlength="100"
                placeholder="请输入智能体名称"
                type="text"
            />
          </div>

          <div>
            <label class="block text-sm font-bold text-slate-700 mb-2">智能体分类</label>
            <select
                v-model="formType"
                class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-500 appearance-none cursor-pointer"
            >
              <option v-for="item in categoryOptions" :key="item.id" :value="item.id">
                {{ item.label }}
              </option>
            </select>
          </div>
        </div>

        <div>
          <label class="block text-sm font-bold text-slate-700 mb-2">广场说明</label>
          <textarea
              v-model="formDescription"
              class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-500 resize-none"
              maxlength="500"
              placeholder="请输入智能体用途、适合人群或使用说明"
              rows="4"
          />
        </div>

        <div class="space-y-4">
          <div
              :class="hasGlobalRule ? 'border-blue-200 bg-blue-50/60 shadow-[0_18px_45px_-34px_rgba(37,99,235,0.65)]' : 'border-slate-200 bg-white'"
              class="rounded-[28px] border px-5 py-5 transition-all duration-300 ease-out"
          >
            <div class="flex items-start gap-4">
              <div class="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-slate-50 text-slate-500">
                <Globe :size="26"/>
              </div>
              <div class="min-w-0 flex-1">
                <div class="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
                  <div class="min-w-0">
                    <div class="flex flex-wrap items-center gap-3">
                      <div class="text-lg font-bold tracking-tight text-slate-900">所有人</div>
                      <span class="rounded-xl bg-amber-50 px-2.5 py-1 text-xs font-semibold text-amber-600">
                        推荐
                      </span>
                    </div>
                    <p class="mt-3 text-base leading-7 text-slate-500">
                      向全员开放智能体广场入口，适合统一开放使用的场景。
                    </p>
                  </div>

                  <div class="flex items-center gap-3">
                    <button
                        :aria-pressed="hasGlobalRule"
                        :class="hasGlobalRule ? 'bg-blue-600' : 'bg-slate-200'"
                        :disabled="loading"
                        class="relative inline-flex h-8 w-14 shrink-0 items-center rounded-full p-1 transition-all duration-300 disabled:cursor-not-allowed disabled:opacity-60"
                        type="button"
                        @click="toggleGlobalRule"
                    >
                      <span
                          :class="hasGlobalRule ? 'translate-x-6' : 'translate-x-0'"
                          class="inline-block h-6 w-6 rounded-full bg-white shadow-sm transition-transform duration-300"
                      />
                    </button>
                  </div>
                </div>

                <div :class="['auth-card-panel', {'auth-card-panel-open': hasGlobalRule}]">
                  <div class="auth-card-panel-inner">
                    <div class="rounded-2xl border border-blue-100 bg-white/80 p-4">
                      <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                        <div>
                          <div class="text-sm font-semibold text-slate-800">访问权限</div>
                          <div class="mt-1 text-sm text-slate-500">
                            选择全员可拥有的智能体权限范围。
                          </div>
                        </div>
                        <select
                            :disabled="loading"
                            :value="globalRight"
                            class="min-w-[8rem] rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm outline-none transition-colors focus:border-blue-500"
                            @change="updateGlobalRight(($event.target as HTMLSelectElement).value)"
                        >
                          <option value="1">使用</option>
                          <option value="2">可复制</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div
              :class="isRoleExpanded ? 'border-blue-200 bg-blue-50/60 shadow-[0_18px_45px_-34px_rgba(37,99,235,0.65)]' : 'border-slate-200 bg-white'"
              class="rounded-[28px] border px-5 py-5 transition-all duration-300 ease-out"
          >
            <div class="flex items-start gap-4">
              <div class="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-slate-50 text-slate-500">
                <Shield :size="26"/>
              </div>
              <div class="min-w-0 flex-1">
                <div class="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
                  <div class="min-w-0">
                    <div class="flex flex-wrap items-center gap-3">
                      <div class="text-lg font-bold tracking-tight text-slate-900">角色授权</div>
                      <span
                          v-if="roleRules.length > 0"
                          class="rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-700"
                      >
                        {{ roleRules.length }} 个角色
                      </span>
                    </div>
                    <p class="mt-3 text-base leading-7 text-slate-500">
                      给指定角色开放使用或可复制权限，适合按部门或职责进行管理。
                    </p>
                  </div>

                  <div class="flex items-center gap-3">
                    <button
                        :aria-pressed="isRoleExpanded"
                        :class="isRoleExpanded ? 'bg-blue-600' : 'bg-slate-200'"
                        :disabled="loading"
                        class="relative inline-flex h-8 w-14 shrink-0 items-center rounded-full p-1 transition-all duration-300 disabled:cursor-not-allowed disabled:opacity-60"
                        type="button"
                        @click="setRoleSectionEnabled(!isRoleExpanded)"
                    >
                      <span
                          :class="isRoleExpanded ? 'translate-x-6' : 'translate-x-0'"
                          class="inline-block h-6 w-6 rounded-full bg-white shadow-sm transition-transform duration-300"
                      />
                    </button>
                  </div>
                </div>

                <div :class="['auth-card-panel', {'auth-card-panel-open': isRoleExpanded}]">
                  <div class="auth-card-panel-inner">
                    <div class="space-y-3 rounded-2xl border border-blue-100 bg-white/80 p-4">
                      <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                        <div>
                          <div class="text-sm font-semibold text-slate-800">角色配置</div>
                          <div class="mt-1 text-sm text-slate-500">
                            选择角色后，可分别设置使用或可复制权限。
                          </div>
                        </div>
                        <button
                            :disabled="loading"
                            class="rounded-xl bg-blue-50 px-4 py-2 text-sm font-medium text-blue-700 transition-colors hover:bg-blue-100 disabled:cursor-not-allowed disabled:opacity-60"
                            type="button"
                            @click="roleSelectorVisible = true"
                        >
                          选择角色
                        </button>
                      </div>

                      <div
                          v-if="roleRules.length === 0"
                          class="rounded-2xl border border-dashed border-slate-200 py-5 text-center text-sm text-slate-400"
                      >
                        暂未指定角色
                      </div>

                      <div v-else class="space-y-2">
                        <div
                            v-for="rule in roleRules"
                            :key="`role-${rule.target_value}`"
                            class="flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white px-4 py-3 md:flex-row md:items-center"
                        >
                          <div class="min-w-0 flex-1">
                            <div class="truncate text-sm font-medium text-slate-700">
                              {{ rule.target_label || `角色#${rule.target_value}` }}
                            </div>
                            <div class="mt-1 text-xs text-slate-400">角色 ID: {{ rule.target_value }}</div>
                          </div>
                          <div class="flex items-center gap-2">
                            <select
                                :disabled="loading"
                                :value="rule.target_right"
                                class="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm outline-none transition-colors focus:border-blue-500"
                                @change="updateRuleRight('role', rule.target_value || '', ($event.target as HTMLSelectElement).value)"
                            >
                              <option value="1">使用</option>
                              <option value="2">可复制</option>
                            </select>
                            <button
                                :disabled="loading"
                                class="rounded-xl p-2 text-slate-400 transition-colors hover:bg-red-50 hover:text-red-500 disabled:cursor-not-allowed disabled:opacity-60"
                                type="button"
                                @click="removeRule('role', rule.target_value || '')"
                            >
                              <Trash2 :size="14"/>
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div
              :class="isUserExpanded ? 'border-blue-200 bg-blue-50/60 shadow-[0_18px_45px_-34px_rgba(37,99,235,0.65)]' : 'border-slate-200 bg-white'"
              class="rounded-[28px] border px-5 py-5 transition-all duration-300 ease-out"
          >
            <div class="flex items-start gap-4">
              <div class="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-slate-50 text-slate-500">
                <UserRound :size="26"/>
              </div>
              <div class="min-w-0 flex-1">
                <div class="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
                  <div class="min-w-0">
                    <div class="flex flex-wrap items-center gap-3">
                      <div class="text-lg font-bold tracking-tight text-slate-900">用户授权</div>
                      <span
                          v-if="userRules.length > 0"
                          class="rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-700"
                      >
                        {{ userRules.length }} 个用户
                      </span>
                    </div>
                    <p class="mt-3 text-base leading-7 text-slate-500">
                      给指定用户开放使用或复制权限，适合灰度试用或定向分享。
                    </p>
                  </div>

                  <div class="flex items-center gap-3">
                    <button
                        :aria-pressed="isUserExpanded"
                        :class="isUserExpanded ? 'bg-blue-600' : 'bg-slate-200'"
                        :disabled="loading"
                        class="relative inline-flex h-8 w-14 shrink-0 items-center rounded-full p-1 transition-all duration-300 disabled:cursor-not-allowed disabled:opacity-60"
                        type="button"
                        @click="setUserSectionEnabled(!isUserExpanded)"
                    >
                      <span
                          :class="isUserExpanded ? 'translate-x-6' : 'translate-x-0'"
                          class="inline-block h-6 w-6 rounded-full bg-white shadow-sm transition-transform duration-300"
                      />
                    </button>
                  </div>
                </div>

                <div :class="['auth-card-panel', {'auth-card-panel-open': isUserExpanded}]">
                  <div class="auth-card-panel-inner">
                    <div class="space-y-3 rounded-2xl border border-blue-100 bg-white/80 p-4">
                      <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                        <div>
                          <div class="text-sm font-semibold text-slate-800">用户配置</div>
                          <div class="mt-1 text-sm text-slate-500">
                            选择用户后，可分别设置使用或可复制权限。
                          </div>
                        </div>
                        <button
                            :disabled="loading"
                            class="rounded-xl bg-blue-50 px-4 py-2 text-sm font-medium text-blue-700 transition-colors hover:bg-blue-100 disabled:cursor-not-allowed disabled:opacity-60"
                            type="button"
                            @click="userSelectorVisible = true"
                        >
                          选择用户
                        </button>
                      </div>

                      <div
                          v-if="userRules.length === 0"
                          class="rounded-2xl border border-dashed border-slate-200 py-5 text-center text-sm text-slate-400"
                      >
                        暂未指定用户
                      </div>

                      <div v-else class="space-y-2">
                        <div
                            v-for="rule in userRules"
                            :key="`user-${rule.target_value}`"
                            class="flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white px-4 py-3 md:flex-row md:items-center"
                        >
                          <div class="min-w-0 flex-1">
                            <div class="truncate text-sm font-medium text-slate-700">
                              {{ rule.target_label || `用户#${rule.target_value}` }}
                            </div>
                            <div class="mt-1 text-xs text-slate-400">用户 ID: {{ rule.target_value }}</div>
                          </div>
                          <div class="flex items-center gap-2">
                            <select
                                :disabled="loading"
                                :value="rule.target_right"
                                class="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm outline-none transition-colors focus:border-blue-500"
                                @change="updateRuleRight('user', rule.target_value || '', ($event.target as HTMLSelectElement).value)"
                            >
                              <option value="1">使用</option>
                              <option value="2">可复制</option>
                            </select>
                            <button
                                :disabled="loading"
                                class="rounded-xl p-2 text-slate-400 transition-colors hover:bg-red-50 hover:text-red-500 disabled:cursor-not-allowed disabled:opacity-60"
                                type="button"
                                @click="removeRule('user', rule.target_value || '')"
                            >
                              <Trash2 :size="14"/>
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="px-6 py-4 bg-slate-50 flex justify-between gap-3">
        <button
            v-if="showOffline"
            :disabled="loading"
            class="px-5 py-2 font-medium rounded-xl transition-colors bg-red-50 text-red-600 hover:bg-red-100 disabled:opacity-60 disabled:cursor-not-allowed"
            type="button"
            @click="$emit('offline')"
        >
          下线智能体
        </button>
        <div class="ml-auto flex justify-end gap-3">
          <button
              :disabled="loading"
              class="px-5 py-2 text-slate-600 font-medium hover:bg-slate-200 rounded-xl transition-colors"
              type="button"
              @click="$emit('close')"
          >
            取消
          </button>
          <button
              :disabled="loading || !canSubmit"
              class="px-5 py-2 font-medium rounded-xl transition-all shadow-sm bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-60 disabled:cursor-not-allowed"
              type="button"
              @click="handleConfirm"
          >
            {{ loading ? submitLoadingText : submitText }}
          </button>
        </div>
      </div>
    </div>

    <RoleSelector
        v-model:visible="roleSelectorVisible"
        :initial-selected="selectedRoles"
        :multiple="true"
        title="选择授权角色"
        @confirm="handleRoleConfirm"
    />

    <UserSelector
        v-model:visible="userSelectorVisible"
        :initial-selected="selectedUsers"
        :multiple="true"
        title="选择授权用户"
        @confirm="handleUserConfirm"
    />
  </div>
</template>

<script setup lang="ts">
import {computed, onMounted, ref, watch} from 'vue'
import {Globe, Shield, Trash2, UserRound, X} from 'lucide-vue-next'
import DictAPI from '@/services/fastApi/module_system/dict'
import type {AiAgentAuthRule, AiAgentPublishPayload, AiAgentTable} from '@/services/fastApi/module_ai/ai_agent'
import RoleSelector, {type Role} from '@/components/common/RoleSelector.vue'
import UserSelector from '@/components/common/UserSelector.vue'
import type {User} from '@/types/user'

const props = withDefaults(defineProps<{
  agent: AiAgentTable | null
  loading?: boolean
  mode?: 'publish' | 'manage'
  showOffline?: boolean
}>(), {
  loading: false,
  mode: 'publish',
  showOffline: false
})

const emit = defineEmits<{
  close: []
  confirm: [payload: AiAgentPublishPayload]
  offline: []
}>()

const loading = ref(false)
const formName = ref('')
const formType = ref('internal')
const formDescription = ref('')
const authRules = ref<AiAgentAuthRule[]>([])
const categoryOptions = ref<{ id: string; label: string }[]>([])
const roleSelectorVisible = ref(false)
const userSelectorVisible = ref(false)
const roleSectionEnabled = ref(false)
const userSectionEnabled = ref(false)

const normalizeRules = (rules?: AiAgentAuthRule[] | null): AiAgentAuthRule[] => {
  const dedup = new Map<string, AiAgentAuthRule>()
  for (const item of rules || []) {
    const targetType = item.target_type
    const targetValue = item.target_type === 'global' ? null : String(item.target_value || '')
    if (!targetType || (targetType !== 'global' && !targetValue)) continue
    const key = `${targetType}:${targetValue ?? 'global'}`
    const existed = dedup.get(key)
    const nextRule: AiAgentAuthRule = {
      ...item,
      target_type: targetType,
      target_value: targetValue,
      target_right: item.target_right === 2 ? 2 : 1
    }
    if (!existed || nextRule.target_right > existed.target_right) {
      dedup.set(key, nextRule)
    }
  }
  return Array.from(dedup.values()).sort((left, right) => {
    const orderMap = {global: 0, role: 1, user: 2}
    const leftOrder = orderMap[left.target_type]
    const rightOrder = orderMap[right.target_type]
    if (leftOrder !== rightOrder) return leftOrder - rightOrder
    return String(left.target_label || left.target_value || '').localeCompare(String(right.target_label || right.target_value || ''))
  })
}

const applyAgentData = () => {
  const current = props.agent
  formName.value = current?.name || ''
  formType.value = current?.type || categoryOptions.value[0]?.id || 'internal'
  formDescription.value = current?.description || ''
  authRules.value = normalizeRules(current?.auth_rules)
  syncSectionStateFromRules(authRules.value)
}

const loadCategories = async () => {
  try {
    const response = await DictAPI.getInitDict('ai_agent_type')
    const dictData = response.data?.data
    if (Array.isArray(dictData)) {
      categoryOptions.value = dictData
        .filter((item: any) => item.status === '0')
        .sort((a: any, b: any) => (a.dict_sort || 0) - (b.dict_sort || 0))
          .map((item: any) => ({
            id: String(item.dict_value),
            label: String(item.dict_label)
          }))
    }
  } catch (error) {
    console.error('加载智能体分类失败:', error)
  } finally {
    if (categoryOptions.value.length === 0) {
      categoryOptions.value = [{id: 'internal', label: '分类'}]
    }
    if (!formType.value) {
      formType.value = categoryOptions.value[0].id
    }
  }
}

const updateRules = (updater: (rules: AiAgentAuthRule[]) => AiAgentAuthRule[]) => {
  authRules.value = normalizeRules(updater([...authRules.value]))
}

const hasGlobalRule = computed(() => authRules.value.some(rule => rule.target_type === 'global'))
const globalRight = computed(() => authRules.value.find(rule => rule.target_type === 'global')?.target_right ?? 1)
const roleRules = computed(() => authRules.value.filter(rule => rule.target_type === 'role'))
const userRules = computed(() => authRules.value.filter(rule => rule.target_type === 'user'))
const isRoleExpanded = computed(() => roleSectionEnabled.value || roleRules.value.length > 0)
const isUserExpanded = computed(() => userSectionEnabled.value || userRules.value.length > 0)
const selectedRoles = computed<Role[]>(() => roleRules.value.map(rule => ({
  id: Number(rule.target_value),
  name: rule.target_label || String(rule.target_value || ''),
})))
const selectedUsers = computed<User[]>(() => userRules.value.map(rule => ({
  id: Number(rule.target_value),
  name: rule.target_label || String(rule.target_value || ''),
} as User)))

const isOverwrite = computed(() => {
  const current = props.agent
  return Boolean(current?.public_agent_id && current.public_agent_id > 0 && current.publish_status !== 'clone')
})

const modalTitle = computed(() => props.mode === 'manage' ? '管理广场智能体' : '发布智能体')
const modalDescription = computed(() => props.mode === 'manage' ? '更新广场信息与授权范围。' : '设置发布名称、说明和授权范围。')
const noticeText = computed(() => {
  if (props.mode === 'manage') {
    return '管理操作将直接更新当前广场智能体的展示信息和授权规则。'
  }
  return isOverwrite.value
      ? '当前智能体已有关联广场版本，本次发布会覆盖旧版本并刷新授权规则。'
      : '发布后会创建广场版本，并按下面的规则控制谁可以使用或可复制。'
})
const submitText = computed(() => props.mode === 'manage' ? '确认保存' : '确认发布')
const submitLoadingText = computed(() => props.mode === 'manage' ? '保存中...' : '发布中...')
const canSubmit = computed(() => Boolean(formName.value.trim() && formType.value))

const syncSectionStateFromRules = (rules: AiAgentAuthRule[]) => {
  roleSectionEnabled.value = rules.some(rule => rule.target_type === 'role')
  userSectionEnabled.value = rules.some(rule => rule.target_type === 'user')
}

const setGlobalRuleEnabled = (enabled: boolean) => {
  updateRules((rules) => {
    const hasRule = rules.some(rule => rule.target_type === 'global')
    if (!enabled) {
      return rules.filter(rule => rule.target_type !== 'global')
    }
    if (hasRule) return rules
    return [
      ...rules,
      {
        target_type: 'global',
        target_value: null,
        target_label: '所有人',
        target_right: 1
      }
    ]
  })
}

const toggleGlobalRule = () => setGlobalRuleEnabled(!hasGlobalRule.value)

const setRoleSectionEnabled = (enabled: boolean) => {
  roleSectionEnabled.value = enabled
  if (!enabled) {
    updateRules((rules) => rules.filter(rule => rule.target_type !== 'role'))
  }
}

const setUserSectionEnabled = (enabled: boolean) => {
  userSectionEnabled.value = enabled
  if (!enabled) {
    updateRules((rules) => rules.filter(rule => rule.target_type !== 'user'))
  }
}

const updateGlobalRight = (value: string) => {
  const nextRight = value === '2' ? 2 : 1
  updateRules((rules) => rules.map(rule => (
      rule.target_type === 'global'
          ? {...rule, target_right: nextRight}
          : rule
  )))
}

const updateRuleRight = (targetType: 'role' | 'user', targetValue: string, value: string) => {
  const nextRight = value === '2' ? 2 : 1
  updateRules((rules) => rules.map(rule => (
      rule.target_type === targetType && String(rule.target_value || '') === targetValue
          ? {...rule, target_right: nextRight}
          : rule
  )))
}

const removeRule = (targetType: 'role' | 'user', targetValue: string) => {
  updateRules((rules) => rules.filter(rule => !(rule.target_type === targetType && String(rule.target_value || '') === targetValue)))
}

const handleRoleConfirm = (roles: Role[]) => {
  roleSectionEnabled.value = true
  const selectedMap = new Map(roles.map(role => [String(role.id), role]))
  updateRules((rules) => {
    const preserved = rules.filter(rule => rule.target_type !== 'role')
    const nextRoleRules = Array.from(selectedMap.values()).map((role) => {
      const existed = rules.find(rule => rule.target_type === 'role' && String(rule.target_value || '') === String(role.id))
      return {
        target_type: 'role' as const,
        target_value: String(role.id),
        target_label: role.name,
        target_right: (existed?.target_right === 1 ? 1 : 2) as 1 | 2
      }
    })
    return [...preserved, ...nextRoleRules]
  })
}

const handleUserConfirm = (users: User[]) => {
  userSectionEnabled.value = true
  const selectedMap = new Map(users.map(user => [String(user.id), user]))
  updateRules((rules) => {
    const preserved = rules.filter(rule => rule.target_type !== 'user')
    const nextUserRules = Array.from(selectedMap.values()).map((user) => {
      const existed = rules.find(rule => rule.target_type === 'user' && String(rule.target_value || '') === String(user.id))
      return {
        target_type: 'user' as const,
        target_value: String(user.id),
        target_label: user.name,
        target_right: (existed?.target_right === 1 ? 1 : 2) as 1 | 2
      }
    })
    return [...preserved, ...nextUserRules]
  })
}

const handleConfirm = () => {
  emit('confirm', {
    name: formName.value.trim(),
    description: formDescription.value.trim(),
    type: formType.value,
    auth_rules: normalizeRules(authRules.value).map(rule => ({
      target_type: rule.target_type,
      target_value: rule.target_type === 'global' ? null : String(rule.target_value || ''),
      target_right: rule.target_right === 2 ? 2 : 1
    }))
  })
}

watch(
  () => props.agent,
  () => {
    applyAgentData()
    syncSectionStateFromRules(authRules.value)
  },
  { immediate: true }
)

watch(
  () => props.loading,
  (value) => {
    loading.value = Boolean(value)
  },
  { immediate: true }
)

onMounted(async () => {
  await loadCategories()
  applyAgentData()
})
</script>

<style scoped>
.auth-card-panel {
  display: grid;
  grid-template-rows: 0fr;
  margin-top: 0;
  opacity: 0;
  transform: translateY(-8px);
  transition: grid-template-rows 0.32s cubic-bezier(0.22, 1, 0.36, 1),
  margin-top 0.32s cubic-bezier(0.22, 1, 0.36, 1),
  opacity 0.24s ease,
  transform 0.32s cubic-bezier(0.22, 1, 0.36, 1);
}

.auth-card-panel-open {
  grid-template-rows: 1fr;
  margin-top: 1.25rem;
  opacity: 1;
  transform: translateY(0);
}

.auth-card-panel-inner {
  min-height: 0;
  overflow: hidden;
}
</style>
