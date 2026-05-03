/**
 * 统一文件上传处理 Composable
 * 参考 mcp_chat2 项目实现
 * @module composables/usePromptInputFiles
 */

import { ref, type Ref } from 'vue'
import { generateImageThumbnail } from '../utils/image'

/**
 * 文件上传配置
 */
export interface PromptInputFilesConfig {
  /** 最大文件数量 */
  maxCount?: number
  /** 单个文件最大大小（字节） */
  maxSize?: number
}


/** 默认配置 */
const DEFAULT_CONFIG: Required<PromptInputFilesConfig> = {
  maxCount: 10,
  maxSize: 20 * 1024 * 1024, // 20MB
}

/**
 * 文件上传处理
 * 简化版本：直接收集原始文件，由后端处理
 * @param config - 上传配置
 * @returns 文件处理方法和状态
 */
export function usePromptInputFiles(config: PromptInputFilesConfig = {}) {
  const mergedConfig = { ...DEFAULT_CONFIG, ...config }

  /** 已选择的原始文件列表 */
  const selectedFiles = ref<File[]>([])

  /** 是否正在处理 */
  const isProcessing = ref(false)

  /** 缩略图映射表（文件名 -> base64 缩略图） */
  const thumbnails = ref<Map<string, string>>(new Map())

  /**
   * 生成文件缩略图
   * @param file - 文件
   */
  const generateThumbnail = async (file: File): Promise<string | undefined> => {
    // 只对图片文件生成缩略图
    if (!file.type.startsWith('image/')) {
      return undefined
    }

    try {
      return await generateImageThumbnail(file)
    } catch (error) {
      console.error('生成缩略图失败:', error)
      return undefined
    }
  }

  /**
   * 获取文件缩略图
   * @param fileName - 文件名
   * @returns 缩略图 base64 或 undefined
   */
  const getThumbnail = (fileName: string): string | undefined => {
    return thumbnails.value.get(fileName)
  }

  /**
   * 处理文件选择事件
   * @param e - 文件选择事件
   */
  const handleFileSelect = async (e: Event) => {
    const files = (e.target as HTMLInputElement).files

    if (files && files.length > 0) {
      isProcessing.value = true
      try {
        const filesToAdd = Array.from(files).filter(file => file.size <= mergedConfig.maxSize)

        // 检查总数限制
        const remainingSlots = mergedConfig.maxCount - selectedFiles.value.length
        if (filesToAdd.length > remainingSlots) {
          console.warn(`最多只能上传 ${mergedConfig.maxCount} 个文件`)
          filesToAdd.splice(remainingSlots)
        }

        // 为图片文件生成缩略图
        for (const file of filesToAdd) {
          if (file.type.startsWith('image/')) {
            const thumbnail = await generateThumbnail(file)
            if (thumbnail) {
              thumbnails.value.set(file.name, thumbnail)
            }
          }
        }

        selectedFiles.value.push(...filesToAdd)
      } finally {
        isProcessing.value = false
      }
    }

    // 重置 input
    if (e.target) {
      (e.target as HTMLInputElement).value = ''
    }
  }

  /**
   * 处理粘贴事件
   * @param e - 剪贴板事件
   * @param fromCapture - 是否来自捕获阶段
   */
  const handlePaste = async (e: ClipboardEvent, fromCapture: boolean = false) => {
    if (!fromCapture && (e as any)?._deepchatHandled) return

    const files = e.clipboardData?.files
    if (files && files.length > 0) {
      isProcessing.value = true
      try {
        const filesToAdd = Array.from(files).filter(file => file.size <= mergedConfig.maxSize)

        const remainingSlots = mergedConfig.maxCount - selectedFiles.value.length
        if (filesToAdd.length > remainingSlots) {
          filesToAdd.splice(remainingSlots)
        }

        // 为图片文件生成缩略图
        for (const file of filesToAdd) {
          if (file.type.startsWith('image/')) {
            const thumbnail = await generateThumbnail(file)
            if (thumbnail) {
              thumbnails.value.set(file.name, thumbnail)
            }
          }
        }

        selectedFiles.value.push(...filesToAdd)
      } finally {
        isProcessing.value = false
      }
    }
  }

  /**
   * 处理拖放事件
   * @param files - 文件列表
   */
  const handleDrop = async (files: FileList) => {
    if (!files || files.length === 0) return

    isProcessing.value = true
    try {
      const filesToAdd = Array.from(files).filter(file => file.size <= mergedConfig.maxSize)

      const remainingSlots = mergedConfig.maxCount - selectedFiles.value.length
      if (filesToAdd.length > remainingSlots) {
        filesToAdd.splice(remainingSlots)
      }

      // 为图片文件生成缩略图
      for (const file of filesToAdd) {
        if (file.type.startsWith('image/')) {
          const thumbnail = await generateThumbnail(file)
          if (thumbnail) {
            thumbnails.value.set(file.name, thumbnail)
          }
        }
      }

      selectedFiles.value.push(...filesToAdd)
    } finally {
      isProcessing.value = false
    }
  }

  /**
   * 删除文件
   * @param idx - 文件索引
   */
  const deleteFile = (idx: number) => {
    if (idx >= 0 && idx < selectedFiles.value.length) {
      const file = selectedFiles.value[idx]
      // 清理缩略图
      thumbnails.value.delete(file.name)
      selectedFiles.value.splice(idx, 1)
    }
  }

  /**
   * 清空所有文件
   */
  const clearFiles = () => {
    thumbnails.value.clear()
    selectedFiles.value = []
  }

  /**
   * 根据名称删除文件
   * @param name - 文件名
   */
  const deleteFileByName = (name: string): void => {
    const idx = selectedFiles.value.findIndex(f => f.name === name)
    if (idx > -1) {
      deleteFile(idx)
    }
  }

  /**
   * 检查是否有文件
   */
  const hasFiles = (): boolean => {
    return selectedFiles.value.length > 0
  }

  /**
   * 计算总文件大小
   */
  const totalSize = (): number => {
    return selectedFiles.value.reduce((sum, file) => sum + file.size, 0)
  }

  // === Return Public API ===
  return {
    // State
    selectedFiles: selectedFiles as Ref<File[]>,
    isProcessing: isProcessing as Ref<boolean>,
    thumbnails,

    // Methods
    handleFileSelect,
    handlePaste,
    handleDrop,
    deleteFile,
    clearFiles,
    deleteFileByName,
    hasFiles,
    totalSize,
    generateThumbnail,
    getThumbnail
  }
}
