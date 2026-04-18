import type {RAGFlowResponse} from '../fastApi/module_ai/ai_ragflow'
import AiRagflowAPI, {
  ChatCompletionRequest,
  ChunkListQuery,
  DatasetAuthRule,
  DatasetAuthRulesPayload,
  DatasetPageQuery,
  DocumentPageQuery,
} from '../fastApi/module_ai/ai_ragflow'
import type {DATASET, DOCUMENT} from '@/types/knowledge'

export const knowledgeApi = {
  listDatasets: async (query: DatasetPageQuery): Promise<RAGFlowResponse<DATASET[]>> => {
    const res = await AiRagflowAPI.listDatasets(query)
    const response = res.data
    const items = Array.isArray(response?.data) ? response.data.map(toDataset) : []
    return { ...response, data: items }
  },
  createDataset: async (body: Record<string, any>): Promise<RAGFlowResponse<DATASET | any>> => {
    const res = await AiRagflowAPI.createDataset(body)
    const response = res.data
    return { ...response, data: mapDatasetData(response?.data) }
  },
  deleteDatasets: async (body: Record<string, any>): Promise<RAGFlowResponse<any>> => {
    const res = await AiRagflowAPI.deleteDatasets(body)
    return res.data
  },
  updateDataset: async (datasetId: string, body: Record<string, any>): Promise<RAGFlowResponse<DATASET | any>> => {
    const res = await AiRagflowAPI.updateDataset(datasetId, body)
    const response = res.data
    return { ...response, data: mapDatasetData(response?.data) }
  },
  uploadDocuments: async (datasetId: string, formData: FormData): Promise<RAGFlowResponse<DOCUMENT[] | DOCUMENT | any>> => {
    const res = await AiRagflowAPI.uploadDocuments(datasetId, formData)
    const response = res.data
    return { ...response, data: mapDocumentData(response?.data) }
  },
  updateDocument: async (datasetId: string, documentId: string, body: Record<string, any>): Promise<RAGFlowResponse<DOCUMENT | any>> => {
    const res = await AiRagflowAPI.updateDocument(datasetId, documentId, body)
    const response = res.data
    return { ...response, data: mapDocumentData(response?.data) }
  },
  downloadDocument: (datasetId: string, documentId: string) => AiRagflowAPI.downloadDocument(datasetId, documentId),
  listDocuments: async (datasetId: string, query: DocumentPageQuery): Promise<RAGFlowResponse<DOCUMENT[]>> => {
    const res = await AiRagflowAPI.listDocuments(datasetId, query)
    const response = res.data
    const items = Array.isArray(response?.data) ? response.data.map(toDocument) : []
    return { ...response, data: items }
  },
  listDatasetAuthRules: async (datasetId: string): Promise<RAGFlowResponse<DatasetAuthRule[]>> => {
    const res = await AiRagflowAPI.listDatasetAuthRules(datasetId)
    return res.data
  },
  updateDatasetAuthRules: async (datasetId: string, body: DatasetAuthRulesPayload): Promise<RAGFlowResponse<DatasetAuthRule[]>> => {
    const res = await AiRagflowAPI.updateDatasetAuthRules(datasetId, body)
    return res.data
  },
  deleteDocuments: async (datasetId: string, body: Record<string, any>): Promise<RAGFlowResponse<any>> => {
    const res = await AiRagflowAPI.deleteDocuments(datasetId, body)
    return res.data
  },
  parseDocuments: async (datasetId: string, body: Record<string, any>): Promise<RAGFlowResponse<any>> => {
    const res = await AiRagflowAPI.parseDocuments(datasetId, body)
    return res.data
  },
  stopParsingDocuments: async (datasetId: string, body: Record<string, any>): Promise<RAGFlowResponse<any>> => {
    const res = await AiRagflowAPI.stopParsingDocuments(datasetId, body)
    return res.data
  },
  addChunk: async (datasetId: string, documentId: string, body: Record<string, any>): Promise<RAGFlowResponse<any>> => {
    const res = await AiRagflowAPI.addChunk(datasetId, documentId, body)
    return res.data
  },
  listChunks: async (datasetId: string, documentId: string, query: ChunkListQuery = {}): Promise<RAGFlowResponse<any>> => {
    const res = await AiRagflowAPI.listChunks(datasetId, documentId, query)
    return res.data
  },
  deleteChunks: async (datasetId: string, documentId: string, body: Record<string, any>): Promise<RAGFlowResponse<any>> => {
    const res = await AiRagflowAPI.deleteChunks(datasetId, documentId, body)
    return res.data
  },
  updateChunk: async (datasetId: string, documentId: string, chunkId: string, body: Record<string, any>): Promise<RAGFlowResponse<any>> => {
    const res = await AiRagflowAPI.updateChunk(datasetId, documentId, chunkId, body)
    return res.data
  },
  retrieveChunks: async (body: Record<string, any>): Promise<RAGFlowResponse<any>> => {
    const res = await AiRagflowAPI.retrieveChunks(body)
    return res.data
  },
  chatCompletions: async (body: ChatCompletionRequest) => {
    const res = await AiRagflowAPI.chatCompletions(body)
    return res.data
  }
}

const toDataset = (data: any): DATASET => ({
  ...data,
  id: String(data?.dataset_id ?? data?.id ?? ''),
  name: data?.name ?? '',
})

const DOCUMENT_RUN_STATUS_MAP: Record<string, string> = {
  '0': 'UNSTART',
  '1': 'RUNNING',
  '2': 'CANCEL',
  '3': 'DONE',
  '4': 'FAIL',
  UNSTART: 'UNSTART',
  RUNNING: 'RUNNING',
  CANCEL: 'CANCEL',
  DONE: 'DONE',
  FAIL: 'FAIL',
}

const normalizeDocumentRun = (run: unknown, fallbackStatus?: unknown) => {
  const raw = run ?? fallbackStatus
  if (raw === undefined || raw === null) return undefined
  const normalized = String(raw).trim().toUpperCase()
  if (!normalized) return undefined
  return DOCUMENT_RUN_STATUS_MAP[normalized] ?? normalized
}

const normalizeDocumentProgress = (progress: unknown) => {
  if (progress === undefined || progress === null || progress === '') return undefined
  const numericProgress = Number(progress)
  return Number.isNaN(numericProgress) ? undefined : numericProgress
}

const toDocument = (data: any): DOCUMENT => ({
  ...data,
  id: String(data?.id ?? ''),
  run: normalizeDocumentRun(data?.run, data?.status),
  progress: normalizeDocumentProgress(data?.progress),
})

const mapDatasetData = (data: any) => {
  if (Array.isArray(data)) {
    return data.map(toDataset)
  }
  if (data && typeof data === 'object') {
    return toDataset(data)
  }
  return data
}

const mapDocumentData = (data: any) => {
  if (Array.isArray(data)) {
    return data.map(toDocument)
  }
  if (data && typeof data === 'object') {
    return toDocument(data)
  }
  return data
}

