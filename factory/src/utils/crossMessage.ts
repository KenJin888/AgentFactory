export type CrossMessagePayload = {
  eventName: string
  eventId?: string | number
  payload?: unknown
}

export type CrossMessageHandler = (payload: unknown) => unknown | Promise<unknown>

export class CrossMessage {
  private static handlers = new Map<string, Set<CrossMessageHandler>>()
  private static pending = new Map<
    string,
    {
      eventName: string
      resolve: (value: unknown) => void
      reject: (reason?: unknown) => void
      timer?: number
    }
  >()
  private static initialized = false

  private static ensureListener() {
    if (this.initialized) return
    if (typeof window === 'undefined') return
    window.addEventListener('message', this.onMessage)
    this.initialized = true
  }

  private static normalizeMessage(data: unknown): CrossMessagePayload | null {
    if (!data) return null
    if (typeof data === 'object') {
      const dataAny = data as any
      if (typeof dataAny.eventName === 'string') {
        return {
          eventName: dataAny.eventName,
          eventId: dataAny.eventId,
          payload: dataAny.payload
        }
      }
      const eventName = dataAny.type || dataAny.event || dataAny.cmd
      if (typeof eventName === 'string') {
        return {
          eventName,
          eventId: dataAny.eventId,
          payload: dataAny.payload ?? dataAny
        }
      }
    }
    if (typeof data === 'string') {
      return { eventName: data }
    }
    return null
  }

  private static async onMessage(event: MessageEvent) {
    const message = CrossMessage.normalizeMessage(event.data)
    if (!message) return
    const { eventName, eventId, payload } = message
    if (eventId != null) {
      const pending = CrossMessage.pending.get(String(eventId))
      if (pending && pending.eventName === eventName) {
        if (pending.timer) window.clearTimeout(pending.timer)
        CrossMessage.pending.delete(String(eventId))
        pending.resolve(payload)
        return
      }
    }
    const handlers = CrossMessage.handlers.get(eventName)
    if (!handlers || handlers.size === 0) return
    const results = await Promise.all(
      Array.from(handlers.values()).map((handler) => handler(payload))
    )
    const response: CrossMessagePayload = {
      eventName,
      eventId,
      payload: results.length <= 1 ? results[0] : results
    }
    if (event.source && 'postMessage' in event.source) {
      ;(event.source as WindowProxy).postMessage(response, event.origin || '*')
    } else if (typeof window !== 'undefined') {
      window.parent?.postMessage(response, '*')
    }
  }

  static on(eventName: string, handler: CrossMessageHandler) {
    this.ensureListener()
    if (!this.handlers.has(eventName)) {
      this.handlers.set(eventName, new Set())
    }
    this.handlers.get(eventName)!.add(handler)
  }

  static off(eventName: string, handler: CrossMessageHandler) {
    const set = this.handlers.get(eventName)
    if (!set) return
    set.delete(handler)
    if (set.size === 0) {
      this.handlers.delete(eventName)
    }
  }

  static send(eventName: string, payload?: unknown, eventId?: string | number) {
    this.ensureListener()
    if (typeof window === 'undefined') return
    if(!payload) payload = {}
    const message: CrossMessagePayload = { eventName, eventId, payload: JSON.parse(JSON.stringify(payload)) }
    const target = window.parent && window.parent !== window ? window.parent : window
    target.postMessage(message, '*')
  }

  static request(eventName: string, payload?: unknown, timeoutMs = 3000) {
    this.ensureListener()
    const eventId = `${Date.now()}_${Math.random().toString(36).slice(2)}`
    return new Promise<unknown>((resolve, reject) => {
      if (typeof window === 'undefined') {
        resolve(null)
        return
      }
      const timer = window.setTimeout(() => {
        this.pending.delete(eventId)
        resolve(null)
      }, timeoutMs)
      this.pending.set(eventId, { eventName, resolve, reject, timer })
      this.send(eventName, payload, eventId)
    })
  }
}
