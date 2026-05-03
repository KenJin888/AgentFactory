/**
 * 图片处理工具函数
 * 参考 mcp_chat2 项目实现
 */

const MAX_THUMBNAIL_SIZE = 1200

interface ImageDimensions {
  width: number
  height: number
}

/**
 * 计算等比例缩放后的尺寸
 */
const calculateAspectRatioFit = (
  srcWidth: number,
  srcHeight: number,
  maxWidth: number,
  maxHeight: number
): ImageDimensions => {
  const ratio = Math.min(maxWidth / srcWidth, maxHeight / srcHeight)
  return {
    width: Math.round(srcWidth * ratio),
    height: Math.round(srcHeight * ratio)
  }
}

/**
 * 生成图片缩略图（压缩后的 base64）
 * @param file - 图片文件
 * @returns 压缩后的 base64 缩略图
 */
export const generateImageThumbnail = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const img = new Image()
    const objectUrl = URL.createObjectURL(file)

    img.onload = () => {
      // 计算压缩后的尺寸
      const { width, height } = calculateAspectRatioFit(
        img.width,
        img.height,
        MAX_THUMBNAIL_SIZE,
        MAX_THUMBNAIL_SIZE
      )

      // 创建 canvas 进行压缩
      const canvas = document.createElement('canvas')
      canvas.width = width
      canvas.height = height
      const ctx = canvas.getContext('2d')

      if (!ctx) {
        URL.revokeObjectURL(objectUrl)
        img.remove()
        reject(new Error('Failed to get canvas context'))
        return
      }

      // 绘制并压缩图片
      ctx.drawImage(img, 0, 0, width, height)
      const compressedBase64 = canvas.toDataURL(file.type, 0.9)

      // 清理
      URL.revokeObjectURL(objectUrl)
      img.remove()
      canvas.remove()

      resolve(compressedBase64)
    }

    img.onerror = () => {
      URL.revokeObjectURL(objectUrl)
      img.remove()
      reject(new Error('Failed to load image'))
    }

    img.src = objectUrl
  })
}

/**
 * 将文件转换为 base64
 * @param file - 文件
 * @returns base64 字符串
 */
export const fileToBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => {
      resolve(reader.result as string)
    }
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

/**
 * 计算图片 token 数（估算）
 * @param width - 图片宽度
 * @param height - 图片高度
 * @returns token 数
 */
export const calculateImageTokens = (width: number, height: number): number => {
  return Math.round((width * height) / 750)
}
