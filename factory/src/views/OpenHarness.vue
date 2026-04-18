<template>
  <div class="h-full overflow-y-auto bg-slate-50 p-6">
    <div class="max-w-7xl mx-auto space-y-6">
      <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div class="flex flex-wrap items-center gap-3 justify-between">
          <div>
            <h1 class="text-xl font-semibold text-slate-900">OpenHarness</h1>
            <p class="text-sm text-slate-500 mt-1">会话创建、会话状态、消息查询、普通发送、流式发送与取消</p>
          </div>
          <div class="flex flex-wrap items-center gap-2">
            <button
              class="px-4 py-2 rounded-lg bg-slate-900 text-white text-sm font-medium hover:bg-slate-800 disabled:opacity-60"
              :disabled="healthLoading"
              @click="checkHealth"
            >
              {{ healthLoading ? '检查中...' : '健康检查' }}
            </button>
            <span class="px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-700">
              {{ healthText }}
            </span>
            <span class="px-3 py-1 rounded-full text-xs font-semibold bg-blue-50 text-blue-700">
              {{ `当前前缀: ${apiPrefix}` }}
            </span>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-3">
          <h2 class="text-base font-semibold text-slate-900">创建会话</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <input v-model.trim="createForm.user_id" class="input-style" placeholder="user_id（可选）" />
            <input v-model.trim="createForm.model" class="input-style" placeholder="model（可选）" />
            <input v-model.trim="createForm.provider" class="input-style" placeholder="provider（可选）" />
            <input v-model.trim="createForm.base_url" class="input-style" placeholder="base_url（可选）" />
          </div>
          <textarea v-model="createForm.system_prompt" class="input-style min-h-[100px]" placeholder="system_prompt（可选）" />
          <button
            class="px-4 py-2 rounded-lg bg-blue-600 text-white text-sm font-medium hover:bg-blue-500 disabled:opacity-60"
            :disabled="createLoading"
            @click="handleCreateSession"
          >
            {{ createLoading ? '创建中...' : '创建会话' }}
          </button>
          <div v-if="sessionSnapshot" class="rounded-xl border border-slate-200 bg-slate-50 p-3 text-xs text-slate-700 space-y-1">
            <div>{{ `session_id: ${sessionSnapshot.session_id}` }}</div>
            <div>{{ `status: ${sessionSnapshot.status}` }}</div>
            <div>{{ `message_count: ${sessionSnapshot.message_count}` }}</div>
            <div>{{ `model: ${sessionSnapshot.model}` }}</div>
            <div>{{ `updated_at: ${formatTime(sessionSnapshot.updated_at)}` }}</div>
          </div>
        </div>

        <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-3">
          <h2 class="text-base font-semibold text-slate-900">会话操作</h2>
          <input v-model.trim="sessionId" class="input-style" placeholder="session_id" />
          <div class="flex flex-wrap gap-2">
            <button class="action-button bg-slate-900 text-white hover:bg-slate-800" :disabled="sessionLoading" @click="loadSession">查询会话</button>
            <button class="action-button bg-cyan-600 text-white hover:bg-cyan-500" :disabled="messagesLoading" @click="loadMessages">查询消息</button>
            <button class="action-button bg-orange-600 text-white hover:bg-orange-500" :disabled="cancelLoading" @click="handleCancel">取消会话</button>
          </div>
          <div v-if="cancelResult" class="rounded-xl border border-orange-200 bg-orange-50 p-3 text-xs text-orange-700">
            {{ `${cancelResult.detail}（cancelled=${cancelResult.cancelled}）` }}
          </div>
          <div class="rounded-xl border border-slate-200 bg-slate-50 p-3">
            <div class="text-xs font-semibold text-slate-600 mb-2">{{ `消息列表 (${messages.length})` }}</div>
            <div class="max-h-[220px] overflow-y-auto custom-scrollbar space-y-2 text-xs">
              <div v-if="messages.length === 0" class="text-slate-400">暂无消息</div>
              <pre v-for="(item, index) in messages" :key="index" class="whitespace-pre-wrap break-words bg-white border border-slate-200 rounded-lg p-2 text-slate-700">{{ formatJson(item) }}</pre>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-3">
          <h2 class="text-base font-semibold text-slate-900">普通发送</h2>
          <textarea v-model="submitContent" class="input-style min-h-[120px]" placeholder="输入要发送的消息" />
          <button class="px-4 py-2 rounded-lg bg-emerald-600 text-white text-sm font-medium hover:bg-emerald-500 disabled:opacity-60" :disabled="submitLoading" @click="handleSubmitMessage">
            {{ submitLoading ? '发送中...' : '发送消息' }}
          </button>
          <div class="rounded-xl border border-slate-200 bg-slate-50 p-3 space-y-2 text-xs">
            <div class="font-semibold text-slate-600">assistant_text</div>
            <pre class="whitespace-pre-wrap break-words text-slate-700">{{ submitAssistantText || '暂无' }}</pre>
            <div class="font-semibold text-slate-600">usage</div>
            <pre class="whitespace-pre-wrap break-words text-slate-700">{{ formatJson(submitUsage) }}</pre>
            <div class="font-semibold text-slate-600">events</div>
            <pre class="whitespace-pre-wrap break-words text-slate-700 max-h-[160px] overflow-y-auto custom-scrollbar">{{ formatJson(submitEvents) }}</pre>
          </div>
        </div>

        <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-3">
          <h2 class="text-base font-semibold text-slate-900">流式发送</h2>
          <textarea v-model="streamContent" class="input-style min-h-[120px]" placeholder="输入要流式发送的消息" />
          <div class="flex flex-wrap gap-2">
            <button class="action-button bg-violet-600 text-white hover:bg-violet-500" :disabled="streamLoading" @click="handleStreamMessage">开始流式发送</button>
            <button class="action-button bg-rose-600 text-white hover:bg-rose-500" :disabled="!streamLoading" @click="stopStream">停止并取消</button>
          </div>
          <div class="rounded-xl border border-slate-200 bg-slate-50 p-3 space-y-2 text-xs">
            <div class="font-semibold text-slate-600">流式状态</div>
            <div class="text-slate-700">{{ streamLoading ? '接收中...' : '空闲' }}</div>
            <div class="font-semibold text-slate-600">assistant_text</div>
            <pre class="whitespace-pre-wrap break-words text-slate-700 min-h-[64px]">{{ streamAssistantText || '暂无' }}</pre>
            <div class="font-semibold text-slate-600">events ({{ streamEvents.length }})</div>
            <pre class="whitespace-pre-wrap break-words text-slate-700 max-h-[180px] overflow-y-auto custom-scrollbar">{{ formatJson(streamEvents) }}</pre>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import message from '@/components/common/message'
import { ohApi, type OhCancelSessionResponse, type OhSessionSnapshot, type OhSseEvent } from '@/services/fastApi/module_oh/oh_http'

const healthLoading = ref(false)
const createLoading = ref(false)
const sessionLoading = ref(false)
const messagesLoading = ref(false)
const submitLoading = ref(false)
const streamLoading = ref(false)
const cancelLoading = ref(false)

const healthText = ref('未检查')
const sessionId = ref('')
const sessionSnapshot = ref<OhSessionSnapshot | null>(null)
const messages = ref<Array<Record<string, unknown>>>([])
const cancelResult = ref<OhCancelSessionResponse | null>(null)

const submitContent = ref('')
const submitAssistantText = ref('')
const submitUsage = ref<Record<string, unknown>>({})
const submitEvents = ref<Array<Record<string, unknown>>>([])

const streamContent = ref('')
const streamAssistantText = ref('')
const streamEvents = ref<OhSseEvent[]>([])
const streamAbortController = ref<AbortController | null>(null)

const createForm = reactive({
  user_id: '',
  model: '',
  provider: '',
  base_url: '',
  system_prompt: ''
})

const apiPrefix = computed(() => ohApi.getResolvedPrefix())

const cleanPayloadValue = (value: string | number | undefined) => {
  if (typeof value === 'string') {
    const trimmed = value.trim()
    return trimmed.length ? trimmed : undefined
  }
  if (typeof value === 'number') {
    return Number.isFinite(value) ? value : undefined
  }
  return undefined
}

const requireSessionId = () => {
  const current = sessionId.value.trim()
  if (!current) {
    message.warning('请先输入 session_id')
    return ''
  }
  return current
}

const formatTime = (timestamp: number) => {
  if (!timestamp) {
    return '-'
  }
  return new Date(timestamp * 1000).toLocaleString()
}

const formatJson = (value: unknown) => {
  try {
    return JSON.stringify(value, null, 2)
  } catch {
    return String(value ?? '')
  }
}

const extractAssistantText = (event: OhSseEvent) => {
  const payload = event.payload || {}
  const textCandidate = payload.content
    ?? payload.text
    ?? payload.delta
    ?? payload.message
    ?? payload.chunk
  if (typeof textCandidate === 'string') {
    return textCandidate
  }
  if (textCandidate && typeof textCandidate === 'object') {
    const nested = (textCandidate as Record<string, unknown>).content
    if (typeof nested === 'string') {
      return nested
    }
  }
  return ''
}

const checkHealth = async () => {
  healthLoading.value = true
  try {
    const result = await ohApi.healthz()
    healthText.value = result.status || 'ok'
    message.success('健康检查成功')
  } catch (error: unknown) {
    healthText.value = '失败'
    const text = error instanceof Error ? error.message : '健康检查失败'
    message.error(text)
  } finally {
    healthLoading.value = false
  }
}

const handleCreateSession = async () => {
  createLoading.value = true
  cancelResult.value = null
  try {
    const snapshot = await ohApi.createSession({
      user_id: cleanPayloadValue(createForm.user_id) as string | undefined,
      model: cleanPayloadValue(createForm.model) as string | undefined,
      base_url: cleanPayloadValue(createForm.base_url) as string | undefined,
      system_prompt: cleanPayloadValue(createForm.system_prompt) as string | undefined,
      provider: cleanPayloadValue(createForm.provider) as string | undefined
    })
    sessionSnapshot.value = snapshot
    sessionId.value = snapshot.session_id
    message.success('会话创建成功')
  } catch (error: unknown) {
    const text = error instanceof Error ? error.message : '创建会话失败'
    message.error(text)
  } finally {
    createLoading.value = false
  }
}

const loadSession = async () => {
  const current = requireSessionId()
  if (!current) {
    return
  }
  sessionLoading.value = true
  cancelResult.value = null
  try {
    sessionSnapshot.value = await ohApi.getSession(current)
    message.success('会话查询成功')
  } catch (error: unknown) {
    const text = error instanceof Error ? error.message : '会话查询失败'
    message.error(text)
  } finally {
    sessionLoading.value = false
  }
}

const loadMessages = async () => {
  const current = requireSessionId()
  if (!current) {
    return
  }
  messagesLoading.value = true
  cancelResult.value = null
  try {
    const result = await ohApi.getMessages(current)
    messages.value = result.messages || []
    message.success('消息查询成功')
  } catch (error: unknown) {
    const text = error instanceof Error ? error.message : '消息查询失败'
    message.error(text)
  } finally {
    messagesLoading.value = false
  }
}

const handleSubmitMessage = async () => {
  const current = requireSessionId()
  if (!current) {
    return
  }
  if (!submitContent.value.trim()) {
    message.warning('请输入消息内容')
    return
  }
  submitLoading.value = true
  cancelResult.value = null
  try {
    const result = await ohApi.submitMessage(current, submitContent.value)
    submitAssistantText.value = result.assistant_text
    submitUsage.value = result.usage || {}
    submitEvents.value = (result.events || []).map((event) => ({
      type: event.type,
      payload: event.payload
    }))
    if (sessionSnapshot.value) {
      sessionSnapshot.value.message_count = result.message_count
    }
    await loadMessages()
    message.success('消息发送成功')
  } catch (error: unknown) {
    const text = error instanceof Error ? error.message : '消息发送失败'
    message.error(text)
  } finally {
    submitLoading.value = false
  }
}

const handleCancel = async () => {
  const current = requireSessionId()
  if (!current) {
    return
  }
  cancelLoading.value = true
  try {
    cancelResult.value = await ohApi.cancelSession(current)
    message.success(cancelResult.value.detail)
    await loadSession()
  } catch (error: unknown) {
    const text = error instanceof Error ? error.message : '取消失败'
    message.error(text)
  } finally {
    cancelLoading.value = false
  }
}

const stopStream = async () => {
  if (streamAbortController.value) {
    streamAbortController.value.abort()
  }
  const current = sessionId.value.trim()
  if (current) {
    try {
      cancelResult.value = await ohApi.cancelSession(current)
      message.info(cancelResult.value.detail)
    } catch (error: unknown) {
      const text = error instanceof Error ? error.message : '停止流式发送失败'
      message.error(text)
    }
  }
}

const handleStreamMessage = async () => {
  const current = requireSessionId()
  if (!current) {
    return
  }
  if (!streamContent.value.trim()) {
    message.warning('请输入流式消息内容')
    return
  }
  streamEvents.value = []
  streamAssistantText.value = ''
  cancelResult.value = null
  streamAbortController.value = new AbortController()
  streamLoading.value = true
  try {
    await ohApi.streamMessage(
      current,
      streamContent.value,
      (event) => {
        streamEvents.value.push(event)
        const text = extractAssistantText(event)
        if (text) {
          streamAssistantText.value += text
        }
      },
      streamAbortController.value.signal
    )
    await loadSession()
    await loadMessages()
    message.success('流式发送完成')
  } catch (error: unknown) {
    if (error instanceof DOMException && error.name === 'AbortError') {
      message.info('流式发送已停止')
    } else {
      const text = error instanceof Error ? error.message : '流式发送失败'
      message.error(text)
    }
  } finally {
    streamLoading.value = false
    streamAbortController.value = null
  }
}
</script>

<style scoped>
.input-style {
  width: 100%;
  border: 1px solid rgb(226 232 240);
  border-radius: 0.75rem;
  padding: 0.625rem 0.75rem;
  font-size: 0.875rem;
  background: white;
  color: rgb(15 23 42);
  outline: none;
  transition: all 0.2s ease;
}

.input-style:focus {
  border-color: rgb(59 130 246);
  box-shadow: 0 0 0 3px rgb(59 130 246 / 0.15);
}

.action-button {
  padding: 0.5rem 0.875rem;
  border-radius: 0.625rem;
  font-size: 0.75rem;
  font-weight: 600;
  transition: all 0.2s ease;
}
</style>

