import type {AssistantMessageBlock, MESSAGE, UserMessageContent} from '@/types/chat'

const tryParseJson = (value: unknown): unknown => {
    if (typeof value !== 'string') {
        return value
    }

    const text = value.trim()
    if (!text) {
        return value
    }

    try {
        return JSON.parse(text)
    } catch {
        return value
    }
}

const isAssistantBlock = (value: unknown): value is AssistantMessageBlock => {
    if (!value || typeof value !== 'object' || Array.isArray(value)) {
        return false
    }

    return typeof (value as AssistantMessageBlock).type === 'string'
}

const normalizeAssistantBlocks = (
    value: unknown,
    fallbackTimestamp = Date.now()
): AssistantMessageBlock[] => {
    if (!Array.isArray(value)) {
        return []
    }

    const blocks = value.filter(isAssistantBlock).map((block) => ({
        ...block,
        timestamp: block.timestamp || fallbackTimestamp
    }))

    if (blocks.length > 0) {
        return blocks
    }

    const text = value
        .map((item) => {
            if (typeof item === 'string') return item
            if (item && typeof item === 'object' && 'content' in item) {
                return typeof (item as { content?: unknown }).content === 'string'
                    ? (item as { content?: string }).content || ''
                    : ''
            }
            return ''
        })
        .filter(Boolean)
        .join('\n')
        .trim()

    if (!text) {
        return []
    }

    return [
        {
            type: 'content',
            content: text,
            status: 'success',
            timestamp: fallbackTimestamp
        }
    ]
}

export const parseAssistantStoredContent = (
    rawContent: unknown,
    fallbackTimestamp = Date.now()
): {
    content: AssistantMessageBlock[]
    metadata?: MESSAGE['metadata']
} => {
    const parsed = tryParseJson(rawContent)

    if (Array.isArray(parsed)) {
        return {
            content: normalizeAssistantBlocks(parsed, fallbackTimestamp)
        }
    }

    if (parsed && typeof parsed === 'object') {
        const payload = parsed as {
            content?: unknown
            metadata?: MESSAGE['metadata']
        }

        const nestedContent = tryParseJson(payload.content)
        const content = normalizeAssistantBlocks(nestedContent, fallbackTimestamp)

        if (content.length > 0) {
            return {
                content,
                metadata: payload.metadata
            }
        }

        if (typeof payload.content === 'string' && payload.content.trim()) {
            return {
                content: [
                    {
                        type: 'content',
                        content: payload.content,
                        status: 'success',
                        timestamp: fallbackTimestamp
                    }
                ],
                metadata: payload.metadata
            }
        }
    }

    if (typeof rawContent === 'string' && rawContent.trim()) {
        return {
            content: [
                {
                    type: 'content',
                    content: rawContent,
                    status: 'success',
                    timestamp: fallbackTimestamp
                }
            ]
        }
    }

    return {content: []}
}

export const serializeAssistantStoredContent = (
    message: Pick<MESSAGE, 'content' | 'metadata'>
): string => {
    return JSON.stringify({
        content: message.content,
        metadata: message.metadata
    })
}

export const serializeUserStoredContent = (content: string | UserMessageContent): string => {
    if (typeof content === 'string') {
        return content
    }

    return JSON.stringify(content)
}

const normalizeUserFiles = (value: unknown): UserMessageContent['files'] => {
    if (!Array.isArray(value)) {
        return []
    }

    return value
        .map((item) => {
            if (!item || typeof item !== 'object' || Array.isArray(item)) {
                return null
            }

            const file = item as Record<string, unknown>
            const normalizedFile: Record<string, unknown> = {}

            if (typeof file.name === 'string' && file.name.trim()) {
                normalizedFile.name = file.name
            }
            if (typeof file.content === 'string' && file.content.trim()) {
                normalizedFile.content = file.content
            }

            for (const key of ['mimeType', 'metadata', 'token', 'path', 'thumbnail']) {
                if (file[key] !== undefined) {
                    normalizedFile[key] = file[key]
                }
            }

            return Object.keys(normalizedFile).length > 0
                ? (normalizedFile as NonNullable<UserMessageContent['files']>[number])
                : null
        })
        .filter((item): item is NonNullable<UserMessageContent['files']>[number] => Boolean(item))
}

export const parseUserStoredContent = (rawContent: unknown): UserMessageContent => {
    const parsed = tryParseJson(rawContent)

    if (parsed && typeof parsed === 'object' && !Array.isArray(parsed)) {
        const payload = parsed as Record<string, unknown>
        return {
            think: typeof payload.think === 'boolean' ? payload.think : undefined,
            search: typeof payload.search === 'boolean' ? payload.search : undefined,
            text: typeof payload.text === 'string'
                ? payload.text
                : (typeof rawContent === 'string' ? rawContent : ''),
            continue: typeof payload.continue === 'boolean' ? payload.continue : undefined,
            files: normalizeUserFiles(payload.files),
            resources: Array.isArray(payload.resources) ? payload.resources : undefined,
            prompts: Array.isArray(payload.prompts) ? payload.prompts : undefined,
            links: Array.isArray(payload.links)
                ? payload.links.filter((item): item is string => typeof item === 'string')
                : undefined,
            content: payload.content
        }
    }

    return {
        text: '',
        files: []
    }
}
