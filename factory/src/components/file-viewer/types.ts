// 统一文件系统项类型
export interface FileSystemItem {
  id: string
  name: string           // 统一字段名
  path: string
  type: 'file' | 'directory'
  size?: number
  modified: Date
  mimeType?: string
  icon?: string
  // 操作权限
  canDelete?: boolean
  canRename?: boolean
  canDownload?: boolean
}

// 文件内容预览
export interface FileContent {
  content: string
  path: string
  size: number
  modified: Date
  mimeType?: string
}

// 视图模式
export type ViewMode = 'grid' | 'list'

// 文件操作类型
export type FileAction = 'open' | 'download' | 'rename' | 'delete' | 'preview'

// 将 KnowledgeBaseItem 转换为统一的 FileSystemItem
export function normalizeFileItem(item: any): FileSystemItem {
  console.log('标准化前的item:', item)

  // 统一名称字段
  const name = item.name || item.filename || item.file_name || item.title ||
               item.path?.split('/')?.pop() || '未命名'

  // 统一路径
  const path = item.path || ''

  // 确定类型
  let type: 'file' | 'directory' = 'file'
  if (item.type === 'directory') type = 'directory'
  else if (item.type === 'file') type = 'file'
  else if (item.is_dir === true) type = 'directory'
  else if (item.is_file === true) type = 'file'

  // 解析日期
  const modifiedStr = item.modified_time || item.modified || new Date().toISOString()
  const modified = new Date(modifiedStr)

  // 生成唯一ID
  const id = `file-${path}-${type}-${modified.getTime()}`

  const result = {
    id,
    name,
    path,
    type,
    size: item.size || 0,
    modified,
    canDelete: true,
    canRename: true,
    canDownload: type === 'file'
  }

  console.log('标准化后的result:', result)
  return result
}

// 将 KnowledgeBaseFileContent 转换为 FileContent
export function normalizeFileContent(content: any): FileContent {
  return {
    content: content.content || '',
    path: content.path || '',
    size: content.size || 0,
    modified: new Date(content.modified_time || new Date().toISOString()),
    mimeType: content.mimeType
  }
}