import { ref, reactive, computed, type Ref, type ComputedRef } from 'vue'

export interface PaginationParams {
  page_no: number
  page_size: number
}

export interface QueryParams {
  [key: string]: any
}

export interface FetchListResult<T> {
  items: T[]
  total: number
}

export interface UseCrudPageOptions<T, Q extends QueryParams> {
  // 初始分页
  initialPage?: number
  initialPageSize?: number
  // 初始查询参数
  initialQuery?: Q
  // 获取列表的API函数
  fetchList: (params: PaginationParams & Q) => Promise<FetchListResult<T>>
}

export interface UseCrudPageReturn<T, Q extends QueryParams> {
  // 状态
  loading: Ref<boolean>
  currentPage: Ref<number>
  pageSize: Ref<number>
  total: Ref<number>
  queryParams: Q
  dataList: Ref<T[]>
  selectedIds: Ref<(string | number)[]>
  isAllSelected: ComputedRef<boolean>

  // 方法
  fetchData: () => Promise<void>
  handleSearch: () => Promise<void>
  handleReset: () => Promise<void>
  handlePageChange: (page: number) => Promise<void>
  handleSizeChange: (size: number) => Promise<void>
  handleRefresh: () => Promise<void>
  toggleSelectAll: () => void
  toggleSelect: (id: string | number) => void
  clearSelection: () => void
}

/**
 * CRUD 页面状态管理组合式函数
 * @param options - 配置选项
 * @example
 * const {
 *   loading,
 *   currentPage,
 *   pageSize,
 *   total,
 *   queryParams,
 *   dataList,
 *   selectedIds,
 *   isAllSelected,
 *   fetchData,
 *   handleSearch,
 *   handleReset,
 *   handlePageChange,
 *   handleSizeChange,
 *   handleRefresh,
 *   toggleSelectAll,
 *   toggleSelect,
 * } = useCrudPage({
 *   initialQuery: {
 *     name: '',
 *     status: '',
 *   },
 *   fetchList: async (params) => {
 *     const res = await api.role.listRole(params)
 *     return {
 *       items: res?.data?.items || [],
 *       total: res?.data?.total || 0,
 *     }
 *   },
 * })
 */
export function useCrudPage<T, Q extends QueryParams>(
  options: UseCrudPageOptions<T, Q>
): UseCrudPageReturn<T, Q> {
  const {
    initialPage = 1,
    initialPageSize = 10,
    initialQuery = {} as Q,
    fetchList,
  } = options

  // 加载状态
  const loading = ref(false)

  // 分页状态
  const currentPage = ref(initialPage)
  const pageSize = ref(initialPageSize)
  const total = ref(0)

  // 查询参数 - 使用 as 断言解决类型问题
  const queryParams = reactive<Q>({ ...initialQuery }) as Q

  // 数据列表
  const dataList = ref<T[]>([]) as Ref<T[]>

  // 选中的ID列表（用于批量操作）
  const selectedIds = ref<(string | number)[]>([])

  // 是否全选
  const isAllSelected = computed(() => {
    return dataList.value.length > 0 && selectedIds.value.length === dataList.value.length
  })

  // 获取列表数据
  const fetchData = async () => {
    loading.value = true
    try {
      const params = {
        page_no: currentPage.value,
        page_size: pageSize.value,
        ...queryParams,
      }
      const res = await fetchList(params as PaginationParams & Q)
      dataList.value = res.items || []
      total.value = res.total || 0
      // 清空选中
      selectedIds.value = []
    } catch (error) {
      console.error('Fetch data failed:', error)
      dataList.value = []
      total.value = 0
    } finally {
      loading.value = false
    }
  }

  // 搜索（重置到第一页）
  const handleSearch = async () => {
    currentPage.value = 1
    await fetchData()
  }

  // 重置查询
  const handleReset = async () => {
    Object.keys(queryParams).forEach((key) => {
      ;(queryParams as any)[key] = initialQuery[key]
    })
    currentPage.value = 1
    await fetchData()
  }

  // 分页变化
  const handlePageChange = async (page: number) => {
    currentPage.value = page
    await fetchData()
  }

  // 每页条数变化
  const handleSizeChange = async (size: number) => {
    pageSize.value = size
    currentPage.value = 1
    await fetchData()
  }

  // 刷新当前页
  const handleRefresh = async () => {
    await fetchData()
  }

  // 切换全选
  const toggleSelectAll = () => {
    if (isAllSelected.value) {
      selectedIds.value = []
    } else {
      selectedIds.value = dataList.value
        .map((item) => (item as any).id)
        .filter((id) => id != null)
    }
  }

  // 切换单选
  const toggleSelect = (id: string | number) => {
    const index = selectedIds.value.indexOf(id)
    if (index > -1) {
      selectedIds.value.splice(index, 1)
    } else {
      selectedIds.value.push(id)
    }
  }

  // 清空选中
  const clearSelection = () => {
    selectedIds.value = []
  }

  return {
    // 状态
    loading,
    currentPage,
    pageSize,
    total,
    queryParams,
    dataList,
    selectedIds,
    isAllSelected,

    // 方法
    fetchData,
    handleSearch,
    handleReset,
    handlePageChange,
    handleSizeChange,
    handleRefresh,
    toggleSelectAll,
    toggleSelect,
    clearSelection,
  }
}

export default useCrudPage
