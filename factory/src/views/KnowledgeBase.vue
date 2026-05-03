<template>
  <div class="flex h-full bg-slate-50 overflow-hidden">
    <!-- 左侧数据集列表 -->
    <div class="w-72 bg-white border-r border-slate-200 flex flex-col flex-shrink-0">
      <div class="p-4 border-b border-slate-100 flex items-center justify-between">
        <h2 class="font-bold text-slate-800 text-lg flex items-center gap-2">
          <Database class="text-indigo-600" :size="20" />
          知识库
        </h2>
        <button
          v-if="canCreate"
          @click="openDatasetModal()"
          class="p-2 text-slate-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
          title="新建数据集"
        >
          <Plus :size="20" />
        </button>
      </div>
      
      <!-- 数据集列表 -->
      <div class="flex-1 overflow-y-auto p-3 space-y-2">
        <div v-if="loadingDatasets" class="flex justify-center py-4">
          <Loader2 class="animate-spin text-slate-400" :size="20" />
        </div>
        <div v-else-if="datasets.length === 0" class="text-center py-8 text-slate-400 text-sm">
          暂无数据集
        </div>
        <div 
          v-else
          v-for="dataset in datasets" 
          :key="dataset.id"
          @click="selectDataset(dataset)"
          class="group flex items-center justify-between p-3 rounded-xl cursor-pointer transition-all duration-200 border"
          :class="activeDatasetId === dataset.id ? 'bg-indigo-50 border-indigo-200 shadow-sm' : 'bg-white border-transparent hover:bg-slate-50 hover:border-slate-200'"
        >
          <div class="flex items-center gap-3 overflow-hidden">
            <div 
              class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
              :class="activeDatasetId === dataset.id ? 'bg-indigo-100 text-indigo-600' : 'bg-slate-100 text-slate-500 group-hover:bg-white group-hover:shadow-sm'"
            >
              <Folder :size="16" />
            </div>
            <div class="flex-1 min-w-0">
              <div class="font-medium text-slate-700 truncate text-sm" :class="{'text-indigo-900': activeDatasetId === dataset.id}">
                {{ dataset.name }}
              </div>
              <div class="text-xs text-slate-400 truncate flex items-center gap-1">
                <FileText :size="10" />
                {{ dataset.document_count || 0 }} 文档
              </div>
            </div>
          </div>
          
          <!-- 操作菜单 -->
          <div v-if="dataset.can_manage && (canUpdate || canDelete)" class="relative" @click.stop>
            <button
              @click="toggleDatasetMenu(dataset.id)"
              class="p-1.5 rounded-lg text-slate-400 opacity-0 group-hover:opacity-100 transition-opacity hover:bg-slate-200 hover:text-slate-600"
              :class="{'opacity-100': showDatasetMenuId === dataset.id}"
            >
              <MoreVertical :size="14" />
            </button>

            <!-- 下拉菜单 -->
            <div
              v-if="showDatasetMenuId === dataset.id"
              class="absolute right-0 top-full mt-1 w-36 bg-white rounded-lg shadow-xl border border-slate-100 py-1 z-20"
              v-click-outside="closeDatasetMenu"
            >
              <button
                  v-if="canUpdate"
                  class="w-full text-left px-3 py-2 text-sm text-slate-600 hover:bg-slate-50 flex items-center gap-2"
                  @click="openDatasetAuthModal(dataset)"
              >
                <Shield :size="14"/>
                权限设置
              </button>
              <button
                v-if="canUpdate"
                @click="openDatasetModal(dataset)"
                class="w-full text-left px-3 py-2 text-sm text-slate-600 hover:bg-slate-50 flex items-center gap-2"
              >
                <Edit2 :size="14" /> 重命名
              </button>
              <button
                v-if="canDelete"
                @click="confirmDeleteDataset(dataset)"
                class="w-full text-left px-3 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center gap-2"
              >
                <Trash2 :size="14" /> 删除
              </button>
            </div>
          </div>
        </div>
      </div>
      

    </div>

    <!-- 右侧内容区域 -->
    <div class="flex-1 flex flex-col min-w-0 bg-slate-50">
      <div v-if="!activeDatasetId" class="flex-1 flex flex-col items-center justify-center text-slate-400">
        <div class="w-24 h-24 bg-slate-100 rounded-full flex items-center justify-center mb-4">
          <Database :size="40" class="text-slate-300" />
        </div>
        <p>请选择一个数据集查看文件</p>
      </div>
      
      <div v-else class="flex-1 flex flex-col h-full">
        <!-- 顶部栏 -->
        <div class="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between flex-shrink-0">
          <div>
             <h1 class="text-xl font-bold text-slate-800 flex items-center gap-2">
               {{ activeDataset?.name }}
               <span class="text-xs font-normal px-2 py-0.5 bg-indigo-50 text-indigo-600 rounded-full border border-indigo-100">
                 {{ activeDataset?.document_count || 0 }} 个文件
               </span>
               <span
                   :class="activeDatasetRightClass"
                   class="text-xs font-normal px-2 py-0.5 rounded-full border"
               >
                 {{ activeDatasetRightLabel }}
               </span>
             </h1>
             <p class="text-slate-500 text-sm mt-1 truncate max-w-lg">{{ activeDataset?.description || '暂无描述' }}</p>
            <p v-if="!activeDatasetCanWrite" class="text-amber-600 text-xs mt-1">
              当前为只读权限，可查看、下载、检索与浏览切片，但不能修改知识库内容。
            </p>
          </div>
          <div class="flex items-center gap-3">
            <div class="relative">
              <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" :size="16" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="搜索文件..."
                class="pl-9 pr-4 py-2 bg-slate-100 border-none rounded-lg text-sm focus:ring-2 focus:ring-indigo-500/20 focus:bg-white transition-all w-64 outline-none"
              >
            </div>
            <button
                v-if="activeDatasetCanManage"
              @click="fileInputRef?.click()"
              :disabled="uploading"
              class="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-70 disabled:cursor-not-allowed transition-colors shadow-sm shadow-indigo-200 font-medium text-sm"
            >
              <Loader2 v-if="uploading" class="animate-spin" :size="16" />
              <UploadCloud v-else :size="16" />
              上传文件
            </button>
            <button
              @click="openRetrieveModal"
              :disabled="chunkRetrieving"
              class="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-70 disabled:cursor-not-allowed transition-colors shadow-sm shadow-indigo-200 font-medium text-sm"
            >
              <Loader2 v-if="chunkRetrieving" class="animate-spin" :size="16" />
              <Search v-else :size="16" />
              检索测试
            </button>
            <input 
              type="file" 
              ref="fileInputRef" 
              class="hidden" 
              @change="handleUpload" 
              multiple
              accept=".pdf,.doc,.docx,.txt,.md,.ppt,.pptx"
            />
          </div>
        </div>

        <!-- 文件列表 -->
        <div class="flex-1 overflow-auto p-6">
          <div v-if="showDocsLoading" class="flex justify-center py-20">
            <Loader2 class="animate-spin text-indigo-500" :size="32" />
          </div>
          
          <div v-else-if="filteredDocs.length === 0" class="flex flex-col items-center justify-center py-20 text-slate-400 bg-white rounded-2xl border border-dashed border-slate-200 h-full max-h-[500px]">
            <FileText :size="48" class="mb-4 text-slate-200" />
            <p class="mb-4">暂无文件</p>
            <button
                v-if="activeDatasetCanManage"
              @click="fileInputRef?.click()"
              class="text-indigo-600 hover:text-indigo-700 font-medium text-sm flex items-center gap-1"
            >
              <Plus :size="16" /> 点击上传
            </button>
            <p v-else class="text-xs text-slate-400">当前权限为只读，无法上传文件</p>
          </div>

          <div v-else class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <table class="w-full text-left text-sm">
              <thead class="bg-slate-50 border-b border-slate-100 text-slate-500 font-medium">
                <tr>
                  <th class="px-6 py-3 w-1/3">文件名</th>
                  <th class="px-6 py-3">状态</th>
                  <th class="px-6 py-3">大小</th>
                  <th class="px-6 py-3">上传时间</th>
                  <th class="px-6 py-3 text-right">操作</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="doc in filteredDocs" :key="doc.id" class="hover:bg-slate-50/80 group">
                  <td class="px-6 py-4">
                    <div class="flex items-center gap-3">
                      <div class="w-8 h-8 rounded flex items-center justify-center flex-shrink-0" :class="getFileIconColor(doc.name)">
                        <component :is="getFileIcon(doc.name)" :size="16" />
                      </div>
                      <span class="font-medium text-slate-700 line-clamp-1" :title="doc.name">{{ doc.name }}</span>
                    </div>
                  </td>
                  <td class="px-6 py-4">
                    <div class="flex flex-col gap-1.5">
                      <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium w-fit" :class="getStatusBadgeClass(doc.run)">
                        <span class="w-1.5 h-1.5 rounded-full" :class="getStatusDotClass(doc.run)"></span>
                        {{ getStatusLabel(doc.run) }}
                      </span>
                      <div v-if="doc.run === 'RUNNING'" class="flex items-center gap-2">
                        <div class="h-1.5 w-24 bg-slate-200 rounded-full overflow-hidden">
                          <div class="h-full bg-amber-500 rounded-full transition-all" :style="{ width: `${getProgressPercent(doc.progress)}%` }"></div>
                        </div>
                        <span class="text-xs text-slate-500 tabular-nums">{{ getProgressPercent(doc.progress) }}%</span>
                        <button
                            v-if="activeDatasetCanManage"
                          @click="stopParsingDocuments(doc)"
                          :disabled="isStoppingDoc(doc.id)"
                          class="px-2 py-0.5 text-xs text-red-600 border border-red-200 rounded hover:bg-red-50 disabled:opacity-60 disabled:cursor-not-allowed transition-colors"
                          title="停止解析"
                        >
                          {{ isStoppingDoc(doc.id) ? '停止中...' : '停止解析' }}
                        </button>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 text-slate-500 font-mono text-xs">
                    {{ formatFileSize(doc.size) }}
                  </td>
                  <td class="px-6 py-4 text-slate-500">
                    {{ formatDate(doc.create_date || doc.update_date) }}
                  </td>
                  <td class="px-6 py-4 text-right">
                    <div class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button
                        @click="openChunkModal(doc)"
                        class="p-1.5 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                        title="查看切片"
                      >
                        <Search :size="16" />
                      </button>
                      <button
                          v-if="activeDatasetCanManage && doc.run !== 'RUNNING'"
                        @click="parseDocuments(doc)"
                        class="p-1.5 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                        title="开始解析"
                      >
                        <Play :size="16" />
                      </button>
                      <button
                        @click="handleDownload(doc)"
                        class="p-1.5 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                        title="下载"
                      >
                        <Download :size="16" />
                      </button>
                      <button
                          v-if="activeDatasetCanManage"
                        @click="openRenameDocModal(doc)"
                        class="p-1.5 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                        title="重命名"
                      >
                        <Edit2 :size="16" />
                      </button>
                      <button
                          v-if="activeDatasetCanManage"
                        @click="confirmDeleteDoc(doc)"
                        class="p-1.5 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                        title="删除"
                      >
                        <Trash2 :size="16" />
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- 数据集模态框 -->
    <div v-if="showDatasetModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in duration-200">
        <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
          <h3 class="font-bold text-slate-800">{{ editingDataset ? '编辑数据集' : '新建数据集' }}</h3>
          <button @click="closeDatasetModal" class="text-slate-400 hover:text-slate-600">
            <X :size="20" />
          </button>
        </div>
        <div class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">数据集名称</label>
            <input 
              v-model="datasetForm.name" 
              type="text" 
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all"
              placeholder="请输入名称"
            >
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">描述 (可选)</label>
            <textarea 
              v-model="datasetForm.description" 
              class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all h-24 resize-none"
              placeholder="请输入描述"
            ></textarea>
          </div>
        </div>
        <div class="px-6 py-4 bg-slate-50 flex justify-end gap-3">
          <button @click="closeDatasetModal" class="px-4 py-2 text-slate-600 hover:bg-slate-200 rounded-lg text-sm font-medium transition-colors">取消</button>
          <button 
            @click="saveDataset" 
            :disabled="!datasetForm.name.trim() || modalLoading"
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium flex items-center gap-2 transition-colors"
          >
            <Loader2 v-if="modalLoading" class="animate-spin" :size="16" />
            确定
          </button>
        </div>
      </div>
    </div>

    <!-- 文档重命名模态框 -->
    <div v-if="showRenameDocModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in duration-200">
        <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
          <h3 class="font-bold text-slate-800">重命名文档</h3>
          <button @click="closeRenameDocModal" class="text-slate-400 hover:text-slate-600">
            <X :size="20" />
          </button>
        </div>
        <div class="p-6">
          <label class="block text-sm font-medium text-slate-700 mb-1">文档名称</label>
          <input 
            v-model="renameDocForm.name" 
            type="text" 
            class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all"
            placeholder="请输入名称"
          >
        </div>
        <div class="px-6 py-4 bg-slate-50 flex justify-end gap-3">
          <button @click="closeRenameDocModal" class="px-4 py-2 text-slate-600 hover:bg-slate-200 rounded-lg text-sm font-medium transition-colors">取消</button>
          <button 
            @click="saveRenameDoc" 
            :disabled="!renameDocForm.name.trim() || modalLoading"
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium flex items-center gap-2 transition-colors"
          >
            <Loader2 v-if="modalLoading" class="animate-spin" :size="16" />
            确定
          </button>
        </div>
      </div>
    </div>

    <!-- Chunk 检索模态框 -->
    <div v-if="showRetrieveModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div class="bg-white rounded-2xl shadow-xl w-[min(96vw,1400px)] max-w-6xl h-[85vh] overflow-hidden animate-in fade-in zoom-in duration-200 flex flex-col">
        <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/50 flex-shrink-0">
          <h3 class="font-bold text-slate-800">检索测试</h3>
          <button @click="closeRetrieveModal" class="text-slate-400 hover:text-slate-600">
            <X :size="20" />
          </button>
        </div>
        <div class="p-6 border-b border-slate-100 bg-white space-y-3 flex-shrink-0">
          <div class="grid grid-cols-1 xl:grid-cols-[1.3fr_1fr_160px_auto] gap-3 items-center">
            <input
              v-model="retrieveForm.question"
              type="text"
              class="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all"
              placeholder="输入检索问题"
            >
            <select
              v-model="retrieveDocId"
              class="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all"
            >
              <option value="">全部文档（不限定）</option>
              <option v-for="doc in docs" :key="doc.id" :value="doc.id">
                {{ doc.name || doc.id }}
              </option>
            </select>
            <input
              v-model.number="retrieveForm.top_k"
              type="number"
              min="1"
              class="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all"
              placeholder="top_k"
            >
            <button
              @click="retrieveChunks"
              :disabled="chunkRetrieving || !retrieveForm.question.trim()"
              class="px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-800 disabled:opacity-60 disabled:cursor-not-allowed text-sm font-medium flex items-center gap-2 transition-colors justify-center min-w-[90px]"
            >
              <Loader2 v-if="chunkRetrieving" class="animate-spin" :size="16" />
              检索
            </button>
          </div>
        </div>

        <div class="flex-1 overflow-y-auto p-6 bg-slate-50/60">
          <div v-if="retrievalChunkList.length === 0" class="h-full min-h-[240px] flex items-center justify-center text-slate-400 text-sm">
            暂无检索结果
          </div>
          <div v-else class="space-y-4">
            <div
              v-for="(chunk, index) in retrievalChunkList"
              :key="chunk.id || `retrieve-${index}`"
              class="bg-white border border-slate-200 rounded-xl p-4 space-y-3 shadow-sm"
            >
              <div class="flex flex-wrap items-center justify-between gap-2">
                <div class="flex flex-wrap items-center gap-2 text-sm font-medium text-slate-800">
                  <span>#{{ index + 1 }}</span>
                  <span
                    v-if="hasRetrieveDocumentKeyword(chunk.document_keyword)"
                    class="text-xs font-normal text-slate-500"
                  >
                    document_keyword: {{ formatRetrieveValue(chunk.document_keyword) }}
                  </span>
                </div>
                <div class="px-3 py-1 rounded-lg bg-indigo-50 border border-indigo-100 text-indigo-700 text-base font-semibold leading-none">
                  相似度 {{ formatRetrieveSimilarity(chunk.similarity) }}
                </div>
              </div>

              <div class="flex flex-wrap gap-2">
                <span
                    v-if="hasRetrieveValue(chunk.chunk_id || chunk.id)"
                    class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-slate-100 border border-slate-200 text-slate-700 text-xs"
                >
                  <span class="text-slate-500">chunk_id</span>
                  <span class="font-medium">{{ formatRetrieveValue(chunk.chunk_id || chunk.id) }}</span>
                </span>
                <span
                    v-if="hasRetrieveValue(chunk.dataset_id)"
                    class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-emerald-50 border border-emerald-100 text-emerald-700 text-xs"
                >
                  <span class="text-emerald-600/80">dataset_id</span>
                  <span class="font-medium">{{ formatRetrieveValue(chunk.dataset_id) }}</span>
                </span>
                <span
                    v-if="hasRetrieveValue(chunk.document_id)"
                    class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-amber-50 border border-amber-100 text-amber-700 text-xs"
                >
                  <span class="text-amber-600/80">document_id</span>
                  <span class="font-medium">{{ formatRetrieveValue(chunk.document_id) }}</span>
                </span>
              </div>

              <div v-if="chunk.content !== undefined" class="space-y-1">
                <div class="text-xs text-slate-500 uppercase tracking-wide">content</div>
                <pre class="bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs text-slate-700 whitespace-pre-wrap break-words max-h-80 overflow-auto">{{ formatRetrieveValue(chunk.content) }}</pre>
              </div>

              <div v-if="chunk.content_ltks !== undefined" class="space-y-1">
                <div class="text-xs text-slate-500 uppercase tracking-wide">content_ltks</div>
                <pre class="bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs text-slate-700 whitespace-pre-wrap break-words max-h-80 overflow-auto">{{ formatRetrieveValue(chunk.content_ltks) }}</pre>
              </div>

              <div v-if="getRetrieveChunkEntries(chunk).length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div
                  v-for="[key, value] in getRetrieveChunkEntries(chunk)"
                  :key="`${chunk.id || index}-${key}`"
                  class="bg-slate-50 border border-slate-200 rounded-lg p-3"
                >
                  <div class="text-xs text-slate-500 uppercase tracking-wide">{{ key }}</div>
                  <div class="text-sm text-slate-700 whitespace-pre-wrap break-words mt-1">{{ formatRetrieveValue(value) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Chunk 管理模态框 -->
    <div v-if="showChunkModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-6xl h-[85vh] overflow-hidden animate-in fade-in zoom-in duration-200 flex flex-col">
        <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/50 flex-shrink-0">
          <div class="min-w-0">
            <h3 class="font-bold text-slate-800">切片管理</h3>
            <p class="text-xs text-slate-500 truncate mt-1">
              文档: {{ chunkManagingDoc?.name || '-' }}
            </p>
          </div>
          <button @click="closeChunkModal" class="text-slate-400 hover:text-slate-600">
            <X :size="20" />
          </button>
        </div>

        <div class="flex-1 overflow-y-auto p-6 space-y-6">
          <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
            <div v-if="!activeDatasetCanWrite"
                 class="mb-4 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-700">
              当前知识库为只读权限，切片仅可查看，不能新增、编辑或删除。
            </div>
            <div class="flex flex-wrap items-center gap-3">
              <input
                v-model="chunkListQuery.keywords"
                type="text"
                placeholder="按关键词过滤"
                class="px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all min-w-[220px]"
              >
              <input
                v-model="chunkListQuery.id"
                type="text"
                placeholder="按切片 id 查询"
                class="px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all min-w-[220px]"
              >
              <button
                @click="fetchChunks"
                :disabled="chunkModalLoading"
                class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-60 disabled:cursor-not-allowed text-sm font-medium flex items-center gap-2 transition-colors"
              >
                <Loader2 v-if="chunkModalLoading" class="animate-spin" :size="16" />
                刷新列表
              </button>
              <button
                  v-if="activeDatasetCanManage"
                @click="showChunkAddForm = !showChunkAddForm"
                :disabled="chunkSaving"
                class="ml-auto px-4 py-2 border border-indigo-200 text-indigo-600 rounded-lg hover:bg-indigo-50 disabled:opacity-60 disabled:cursor-not-allowed text-sm font-medium flex items-center gap-2 transition-colors"
              >
                <Plus :size="16" />
                {{ showChunkAddForm ? '收起新增' : '新增切片' }}
              </button>
            </div>

            <div v-if="showChunkAddForm" class="mt-4 bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-3">
              <div class="text-sm font-medium text-slate-700">新增 Chunk</div>
              <textarea
                v-model="chunkAddForm.content"
                class="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all min-h-[120px]"
                placeholder="输入切片内容"
              ></textarea>
              <input
                v-model="chunkAddForm.keywords"
                type="text"
                class="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all"
                placeholder="可选: 关键词，逗号分隔"
              >
              <div class="flex justify-end gap-2">
                <button
                  @click="showChunkAddForm = false"
                  class="px-4 py-2 text-slate-600 bg-white border border-slate-200 rounded-lg hover:bg-slate-100 text-sm font-medium transition-colors"
                >
                  取消
                </button>
                <button
                  @click="addChunk"
                  :disabled="chunkSaving || !chunkAddForm.content.trim()"
                  class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-60 disabled:cursor-not-allowed text-sm font-medium flex items-center gap-2 transition-colors"
                >
                  <Loader2 v-if="chunkSaving" class="animate-spin" :size="16" />
                  新增
                </button>
              </div>
            </div>
          </div>

          <div class="bg-white border border-slate-200 rounded-xl overflow-hidden">
            <div class="px-4 py-3 border-b border-slate-100 text-sm font-medium text-slate-700">切片列表</div>
            <div v-if="chunkModalLoading" class="flex justify-center py-8">
              <Loader2 class="animate-spin text-indigo-500" :size="24" />
            </div>
            <div v-else-if="chunkList.length === 0" class="text-center py-10 text-slate-400 text-sm">
              暂无切片数据
            </div>
            <div v-else class="divide-y divide-slate-100">
              <div v-for="chunk in chunkList" :key="chunk.id" class="p-4 space-y-3">
                <div class="flex items-start justify-between gap-3">
                  <div class="min-w-0">
                    <div class="text-xs text-slate-500 break-all">ID: {{ chunk.id }}</div>
                    <div class="text-xs text-slate-400 mt-1">
                      更新时间: {{ formatDate(chunk.update_date || chunk.create_date) }}
                    </div>
                  </div>
                  <div class="flex items-center gap-2">
                    <button
                        v-if="activeDatasetCanManage"
                      @click="startEditChunk(chunk)"
                      class="p-1.5 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                      title="编辑切片"
                    >
                      <Edit2 :size="16" />
                    </button>
                    <button
                        v-if="activeDatasetCanManage"
                      @click="confirmDeleteChunk(chunk)"
                      class="p-1.5 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                      title="删除切片"
                    >
                      <Trash2 :size="16" />
                    </button>
                  </div>
                </div>

                <div v-if="editingChunkId === chunk.id" class="space-y-3">
                  <textarea
                    v-model="editingChunkContent"
                    class="w-full px-3 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all min-h-[110px]"
                    placeholder="编辑切片内容"
                  ></textarea>
                  <div class="flex items-center justify-end gap-2">
                    <button @click="cancelEditChunk" class="px-3 py-1.5 text-slate-600 hover:bg-slate-200 rounded-lg text-sm transition-colors">
                      取消
                    </button>
                    <button
                      @click="saveChunkEdit"
                      :disabled="chunkSaving || !editingChunkContent.trim()"
                      class="px-3 py-1.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-60 disabled:cursor-not-allowed text-sm font-medium flex items-center gap-2 transition-colors"
                    >
                      <Loader2 v-if="chunkSaving" class="animate-spin" :size="14" />
                      保存
                    </button>
                  </div>
                </div>
                <div v-else class="space-y-1">
                  <div
                    @click="toggleChunkExpand(chunk.id)"
                    class="text-sm text-slate-700 whitespace-pre-wrap break-words leading-6 cursor-pointer"
                    :style="getChunkContentStyle(chunk.id)"
                    :title="isChunkExpanded(chunk.id) ? '点击收起' : '点击展开'"
                  >
                    {{ previewChunkContent(chunk) }}
                  </div>
                  <button
                    v-if="canExpandChunk(chunk)"
                    @click="toggleChunkExpand(chunk.id)"
                    class="text-xs text-indigo-600 hover:text-indigo-700 transition-colors"
                  >
                    {{ isChunkExpanded(chunk.id) ? '收起' : '展开' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <DatasetAuthModal
        :dataset-id="authEditingDataset?.id"
        :dataset-name="authEditingDataset?.name"
        :visible="showDatasetAuthModal"
        @close="closeDatasetAuthModal"
        @saved="handleDatasetAuthSaved"
    />

  </div>
</template>

<script setup lang="ts">
import type {CSSProperties} from 'vue'
import {computed, onMounted, onUnmounted, ref, watch} from 'vue'
import {
  Database,
  Download,
  Edit2,
  FileArchive,
  FileAudio,
  FileCode,
  FileImage,
  FileSpreadsheet,
  FileText,
  FileVideo,
  Folder,
  Loader2,
  MoreVertical,
  Play,
  Plus,
  Presentation,
  Search,
  Shield,
  Trash2,
  UploadCloud,
  X
} from 'lucide-vue-next'
import type {DATASET, DOCUMENT} from '@/types/knowledge'
import DatasetAuthModal from '@/components/common/DatasetAuthModal.vue'
import {api} from '../services/api'
import dialog from '@/components/common/dialog'
import message from '@/components/common/message'
import {useUserStore} from '@/stores/user'

// 状态
const datasets = ref<DATASET[]>([])
const docs = ref<DOCUMENT[]>([])
const loadingDatasets = ref(true)
const docsLoading = ref(false)
const docsLoadedForActiveDataset = ref(false)
const uploading = ref(false)
const searchQuery = ref('')
const activeDatasetId = ref('')
const showDatasetMenuId = ref('')

// 模态框状态
const showDatasetModal = ref(false)
const editingDataset = ref<DATASET | null>(null)
const datasetForm = ref({ name: '', description: '' })
const modalLoading = ref(false)
const showDatasetAuthModal = ref(false)
const authEditingDataset = ref<DATASET | null>(null)

const showRenameDocModal = ref(false)
const editingDoc = ref<DOCUMENT | null>(null)
const renameDocForm = ref({ name: '' })
const showRetrieveModal = ref(false)
const docsPollingTimer = ref<number | null>(null)
const stoppingDocIds = ref<Record<string, boolean>>({})

const PERMS = {
  create: 'module_ai:ai_ragflow:create',
  update: 'module_ai:ai_ragflow:update',
  delete: 'module_ai:ai_ragflow:delete',
} as const

const userStore = useUserStore()
const currentUser = computed(() => userStore.userInfo)
const isAdmin = computed(() => currentUser.value?.is_superuser || false)
const userPerms = computed(() => userStore.prems || [])
const hasWildcardPerm = computed(() => userPerms.value.includes('*:*:*'))
const hasPerm = (perm: string) => isAdmin.value || hasWildcardPerm.value || userPerms.value.includes(perm)
const canCreate = computed(() => hasPerm(PERMS.create))
const canUpdate = computed(() => hasPerm(PERMS.update))
const canDelete = computed(() => hasPerm(PERMS.delete))

type CHUNK_ITEM = {
  id: string;
  content?: string;
  create_date?: string;
  update_date?: string;
  [key: string]: any;
}

type RetrievalChunk = Record<string, any>

const showChunkModal = ref(false)
const chunkManagingDoc = ref<DOCUMENT | null>(null)
const chunkList = ref<CHUNK_ITEM[]>([])
const chunkModalLoading = ref(false)
const chunkSaving = ref(false)
const chunkRetrieving = ref(false)
const editingChunkId = ref('')
const editingChunkContent = ref('')
const expandedChunkIds = ref<Record<string, boolean>>({})
const showChunkAddForm = ref(false)
const chunkAddForm = ref({ content: '', keywords: '' })
const chunkListQuery = ref({
  keywords: '',
  id: '',
  page: 1,
  page_size: 50,
})
const retrieveForm = ref({
  question: '',
  top_k: 5,
})
const retrieveDocId = ref('')
const retrieveResult = ref<any>(null)

// DOM 引用
const fileInputRef = ref<HTMLInputElement | null>(null)

// 计算属性
const activeDataset = computed(() => datasets.value.find(d => d.id === activeDatasetId.value))
const activeDatasetCanWrite = computed(() => Boolean(activeDataset.value?.can_write))
const activeDatasetCanManage = computed(() => activeDatasetCanWrite.value && canUpdate.value)
const activeDatasetRightLabel = computed(() => activeDataset.value?.current_right === 2 ? '读写权限' : '只读权限')
const activeDatasetRightClass = computed(() => (
    activeDataset.value?.current_right === 2
        ? 'bg-emerald-50 text-emerald-600 border-emerald-100'
        : 'bg-amber-50 text-amber-700 border-amber-100'
))
const showDocsLoading = computed(() => docsLoading.value && !docsLoadedForActiveDataset.value)

const filteredDocs = computed(() => {
  const keyword = searchQuery.value.toLowerCase()
  return docs.value.filter(doc => (doc.name || '').toLowerCase().includes(keyword))
})

const extractRetrieveChunks = (value: any): RetrievalChunk[] => {
  if (!value) return []
  if (Array.isArray(value)) return value
  if (Array.isArray(value?.data)) return value.data
  if (Array.isArray(value?.chunks)) return value.chunks
  if (Array.isArray(value?.data?.chunks)) return value.data.chunks
  if (Array.isArray(value?.data?.data?.chunks)) return value.data.data.chunks
  return []
}

const sanitizeRetrieveChunk = (value: RetrievalChunk): RetrievalChunk => {
  if (!value || typeof value !== 'object') return { content: String(value ?? '') }
  const item = { ...value }
  if (item.id === undefined || item.id === null || item.id === '') {
    item.id = item.chunk_id ?? item.chunkId ?? ''
  }
  if (item.content === undefined) {
    item.content = item.text ?? item.chunk ?? item.body ?? ''
  }
  delete item.positions
  delete item.highlight
  return item
}

const retrievalChunkList = computed<RetrievalChunk[]>(() => extractRetrieveChunks(retrieveResult.value).map(sanitizeRetrieveChunk))

const formatRetrieveValue = (value: any) => {
  if (value === undefined || value === null) return '-'
  if (typeof value === 'string') return value || '-'
  if (typeof value === 'number' || typeof value === 'boolean') return String(value)
  try {
    return JSON.stringify(value, null, 2)
  } catch {
    return String(value)
  }
}

const formatRetrieveSimilarity = (value: any) => {
  if (typeof value === 'number' && Number.isFinite(value)) return value.toFixed(4)
  if (value === undefined || value === null || value === '') return '-'
  return String(value)
}

const hasRetrieveDocumentKeyword = (value: any) => {
  if (value === undefined || value === null) return false
  if (typeof value === 'string') return value.trim().length > 0
  if (Array.isArray(value)) return value.length > 0
  return true
}

const hasRetrieveValue = (value: any) => {
  if (value === undefined || value === null) return false
  if (typeof value === 'string') return value.trim().length > 0
  if (Array.isArray(value)) return value.length > 0
  return true
}

const getRetrieveChunkEntries = (chunk: RetrievalChunk): Array<[string, any]> => {
  const hiddenFields = new Set([
    'id',
    'chunk_id',
    'similarity',
    'content',
    'content_ltks',
    'dataset_id',
    'document_id',
    'image_id',
    'document_keyword',
    'positions',
    'highlight',
  ])
  return Object.entries(chunk).filter(([key]) => !hiddenFields.has(key))
}

// 自定义指令：点击外部关闭菜单
const vClickOutside = {
  mounted(el: any, binding: any) {
    el.clickOutsideEvent = (event: Event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event)
      }
    }
    document.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el: any) {
    document.removeEventListener('click', el.clickOutsideEvent)
  }
}

// 方法
const formatDate = (dateString?: string) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString() + ' ' + new Date(dateString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const formatFileSize = (bytes?: number) => {
  if (bytes === undefined) return '-'
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

const getStatusLabel = (run?: string) => {
  return run || '未知'
}

// UNSTART, RUNNING, CANCEL, DONE, FAIL
const getStatusBadgeClass = (run?: string) => {
  const normalized = (run || '').toLowerCase()
  if (normalized.includes('fail') || normalized.includes('cancel')) return 'bg-red-50 text-red-700'
  if (normalized === 'done') return 'bg-green-50 text-green-700'
  if (normalized.includes('running') && normalized.includes('ing')) return 'bg-amber-50 text-amber-700'
  return 'bg-slate-100 text-slate-600'
}

const getStatusDotClass = (run?: string) => {
  const normalized = (run || '').toLowerCase()
  if (normalized.includes('fail') || normalized.includes('cancel')) return 'bg-red-500'
  if (normalized === 'done') return 'bg-green-500'
  if (normalized.includes('running') && normalized.includes('ing')) return 'bg-amber-500'
  return 'bg-slate-400'
}

const getProgressPercent = (progress?: number) => {
  if (progress === undefined || progress === null || Number.isNaN(progress)) return 0
  const clamped = Math.min(1, Math.max(0, progress))
  return Math.round(clamped * 100)
}

const getFileIcon = (filename?: string) => {
  if (!filename) return FileText
  const ext = filename.split('.').pop()?.toLowerCase()
  
  switch (ext) {
    case 'jpg':
    case 'jpeg':
    case 'png':
    case 'gif':
    case 'svg':
    case 'webp':
      return FileImage
    case 'xls':
    case 'xlsx':
    case 'csv':
      return FileSpreadsheet
    case 'ppt':
    case 'pptx':
      return Presentation
    case 'mp4':
    case 'avi':
    case 'mov':
    case 'mkv':
      return FileVideo
    case 'mp3':
    case 'wav':
    case 'ogg':
      return FileAudio
    case 'zip':
    case 'rar':
    case '7z':
    case 'tar':
    case 'gz':
      return FileArchive
    case 'js':
    case 'ts':
    case 'py':
    case 'java':
    case 'c':
    case 'cpp':
    case 'html':
    case 'css':
    case 'json':
    case 'xml':
      return FileCode
    case 'pdf':
    case 'doc':
    case 'docx':
    case 'txt':
    case 'md':
    default:
      return FileText
  }
}

const getFileIconColor = (filename?: string) => {
  if (!filename) return 'bg-slate-50 text-slate-600'
  const ext = filename.split('.').pop()?.toLowerCase()
  
  switch (ext) {
    case 'jpg':
    case 'jpeg':
    case 'png':
    case 'gif':
    case 'svg':
    case 'webp':
      return 'bg-pink-50 text-pink-600'
    case 'xls':
    case 'xlsx':
    case 'csv':
      return 'bg-emerald-50 text-emerald-600'
    case 'ppt':
    case 'pptx':
      return 'bg-orange-50 text-orange-600'
    case 'mp4':
    case 'avi':
    case 'mov':
    case 'mkv':
      return 'bg-red-50 text-red-600'
    case 'mp3':
    case 'wav':
    case 'ogg':
      return 'bg-yellow-50 text-yellow-600'
    case 'zip':
    case 'rar':
    case '7z':
    case 'tar':
    case 'gz':
      return 'bg-slate-50 text-slate-600'
    case 'js':
    case 'ts':
    case 'py':
    case 'java':
    case 'c':
    case 'cpp':
    case 'html':
    case 'css':
    case 'json':
    case 'xml':
      return 'bg-blue-50 text-blue-600'
    case 'pdf':
      return 'bg-rose-50 text-rose-600'
    case 'doc':
    case 'docx':
      return 'bg-indigo-50 text-indigo-600'
    case 'txt':
    case 'md':
    default:
      return 'bg-slate-50 text-slate-600'
  }
}

const toChunkItem = (value: any): CHUNK_ITEM => {
  const rawContent = value?.content ?? value?.text ?? value?.chunk ?? value?.body ?? ''
  const content = typeof rawContent === 'string'
    ? rawContent
    : (() => {
      try {
        return JSON.stringify(rawContent, null, 2)
      } catch {
        return String(rawContent)
      }
    })()

  return {
    ...value,
    id: String(value?.id ?? value?.chunk_id ?? value?.chunkId ?? ''),
    content,
  }
}

const extractChunkList = (value: any): any[] => {
  if (Array.isArray(value)) return value
  if (!value || typeof value !== 'object') return []
  const candidates = [value.chunks, value.items, value.data, value.docs, value.records]
  const matched = candidates.find(item => Array.isArray(item))
  return Array.isArray(matched) ? matched : []
}

const previewChunkContent = (chunk: CHUNK_ITEM) => {
  const text = chunk.content || ''
  return text.trim() || '[空内容]'
}

const isChunkExpanded = (chunkId: string) => Boolean(expandedChunkIds.value[chunkId])

const toggleChunkExpand = (chunkId: string) => {
  expandedChunkIds.value = {
    ...expandedChunkIds.value,
    [chunkId]: !isChunkExpanded(chunkId),
  }
}

const collapsedChunkContentStyle: CSSProperties = {
  display: '-webkit-box',
  WebkitLineClamp: 3,
  WebkitBoxOrient: 'vertical',
  overflow: 'hidden',
}

const getChunkContentStyle = (chunkId: string): CSSProperties => {
  if (isChunkExpanded(chunkId)) return {}
  return collapsedChunkContentStyle
}

const canExpandChunk = (chunk: CHUNK_ITEM) => {
  const text = previewChunkContent(chunk)
  return text.length > 90 || text.includes('\n')
}

const closeChunkModal = () => {
  showChunkModal.value = false
  chunkManagingDoc.value = null
  chunkList.value = []
  chunkModalLoading.value = false
  chunkSaving.value = false
  chunkRetrieving.value = false
  showChunkAddForm.value = false
  chunkAddForm.value = { content: '', keywords: '' }
  chunkListQuery.value = { keywords: '', id: '', page: 1, page_size: 50 }
  retrieveForm.value = { question: '', top_k: 5 }
  retrieveResult.value = null
  editingChunkId.value = ''
  editingChunkContent.value = ''
  expandedChunkIds.value = {}
}

const openRetrieveModal = () => {
  if (!activeDatasetId.value) return
  showRetrieveModal.value = true
}

const closeRetrieveModal = () => {
  showRetrieveModal.value = false
}

const resetDocsState = () => {
  docsLoadedForActiveDataset.value = false
  docs.value = []
}

const syncActiveDatasetSelection = () => {
  if (datasets.value.length === 0) {
    activeDatasetId.value = ''
    resetDocsState()
    return false
  }

  const hasActive = datasets.value.some(dataset => dataset.id === activeDatasetId.value)
  if (!activeDatasetId.value || !hasActive) {
    const nextDatasetId = datasets.value[0].id
    const changed = activeDatasetId.value !== nextDatasetId
    activeDatasetId.value = nextDatasetId
    resetDocsState()
    return changed || docs.value.length === 0
  }

  return false
}

const openChunkModal = async (doc: DOCUMENT) => {
  if (!activeDatasetId.value) return
  chunkManagingDoc.value = doc
  chunkList.value = []
  showChunkAddForm.value = false
  chunkAddForm.value = { content: '', keywords: '' }
  retrieveForm.value = { question: '', top_k: 5 }
  retrieveResult.value = null
  editingChunkId.value = ''
  editingChunkContent.value = ''
  showChunkModal.value = true
  await fetchChunks()
}

const fetchChunks = async () => {
  if (!activeDatasetId.value || !chunkManagingDoc.value) return
  chunkModalLoading.value = true
  try {
    const query: Record<string, any> = {
      page: chunkListQuery.value.page,
      page_size: chunkListQuery.value.page_size,
    }
    if (chunkListQuery.value.keywords.trim()) query.keywords = chunkListQuery.value.keywords.trim()
    if (chunkListQuery.value.id.trim()) query.id = chunkListQuery.value.id.trim()

    const res = await api.knowledge.listChunks(activeDatasetId.value, chunkManagingDoc.value.id, query)
    chunkList.value = extractChunkList(res.data).map(toChunkItem)
    editingChunkId.value = ''
    editingChunkContent.value = ''
    expandedChunkIds.value = {}
  } catch (e) {
    console.error('加载切片失败:', e)
    alert('加载切片失败')
  } finally {
    chunkModalLoading.value = false
  }
}

const addChunk = async () => {
  if (!activeDatasetId.value || !chunkManagingDoc.value || !activeDatasetCanManage.value) return
  const content = chunkAddForm.value.content.trim()
  if (!content) return

  chunkSaving.value = true
  try {
    const payload: Record<string, any> = { content }
    const keywords = chunkAddForm.value.keywords
      .split(',')
      .map(item => item.trim())
      .filter(Boolean)
    if (keywords.length > 0) payload.important_keywords = keywords

    await api.knowledge.addChunk(activeDatasetId.value, chunkManagingDoc.value.id, payload)
    showChunkAddForm.value = false
    chunkAddForm.value = { content: '', keywords: '' }
    await fetchChunks()
  } catch (e) {
    console.error('新增切片失败:', e)
    alert('新增切片失败')
  } finally {
    chunkSaving.value = false
  }
}

const startEditChunk = (chunk: CHUNK_ITEM) => {
  if (!activeDatasetCanManage.value) return
  editingChunkId.value = chunk.id
  editingChunkContent.value = chunk.content || ''
}

const cancelEditChunk = () => {
  editingChunkId.value = ''
  editingChunkContent.value = ''
}

const saveChunkEdit = async () => {
  if (!activeDatasetId.value || !chunkManagingDoc.value || !editingChunkId.value || !activeDatasetCanManage.value) return
  const content = editingChunkContent.value.trim()
  if (!content) return

  chunkSaving.value = true
  try {
    await api.knowledge.updateChunk(
      activeDatasetId.value,
      chunkManagingDoc.value.id,
      editingChunkId.value,
      { content },
    )
    await fetchChunks()
  } catch (e) {
    console.error('更新切片失败:', e)
    alert('更新切片失败')
  } finally {
    chunkSaving.value = false
  }
}

const confirmDeleteChunk = async (chunk: CHUNK_ITEM) => {
  if (!activeDatasetId.value || !chunkManagingDoc.value || !activeDatasetCanManage.value) return
  try {
    await dialog.confirm(`确定要删除切片 "${chunk.id}" 吗？`)
    await api.knowledge.deleteChunks(activeDatasetId.value, chunkManagingDoc.value.id, {
      ids: [chunk.id],
      chunk_ids: [chunk.id],
    })
    await fetchChunks()
  } catch (e) {
    if (e instanceof Error && e.message === 'Cancel') return
    console.error('删除切片失败:', e)
    alert('删除切片失败')
  }
}

const retrieveChunks = async () => {
  if (!activeDatasetId.value) return
  const question = retrieveForm.value.question.trim()
  const targetDocId = retrieveDocId.value
  if (!question) return

  chunkRetrieving.value = true
  try {
    const res = await api.knowledge.retrieveChunks({
      question,
      dataset_ids: [activeDatasetId.value],
      document_ids: targetDocId ? [targetDocId] : [],
      top_k: Math.max(1, Number(retrieveForm.value.top_k) || 5),
    })
    retrieveResult.value = res.data
  } catch (e) {
    console.error('检索切片失败:', e)
    alert('检索切片失败')
  } finally {
    chunkRetrieving.value = false
  }
}

// 数据集操作
const fetchDatasets = async () => {
  loadingDatasets.value = true
  try {
    const res = await api.knowledge.listDatasets({ page: 1, page_size: 100 })
    datasets.value = res.data || []
    const shouldFetchDocs = syncActiveDatasetSelection()
    if (shouldFetchDocs && activeDatasetId.value) {
      await fetchDocs()
    }
  } catch (e) {
    console.error('加载数据集失败:', e)
  } finally {
    loadingDatasets.value = false
  }
}

const selectDataset = (dataset: DATASET) => {
  const isSwitchingDataset = activeDatasetId.value !== dataset.id
  activeDatasetId.value = dataset.id
  showDatasetMenuId.value = ''
  if (isSwitchingDataset) {
    resetDocsState()
  }
  fetchDocs()
}

const toggleDatasetMenu = (id: string) => {
  showDatasetMenuId.value = showDatasetMenuId.value === id ? '' : id
}

const closeDatasetMenu = () => {
  showDatasetMenuId.value = ''
}

const openDatasetModal = (dataset?: DATASET) => {
  if (dataset) {
    if (!dataset.can_manage || !canUpdate.value) {
      message.warning('暂无修改权限，请联系管理员开通')
      return
    }
  } else if (!canCreate.value) {
    message.warning('暂无创建权限，请联系管理员开通')
    return
  }
  closeDatasetMenu()
  editingDataset.value = dataset || null
  datasetForm.value = {
    name: dataset?.name || '',
    description: dataset?.description || ''
  }
  showDatasetModal.value = true
}

const closeDatasetModal = () => {
  showDatasetModal.value = false
  editingDataset.value = null
  datasetForm.value = { name: '', description: '' }
}

const openDatasetAuthModal = (dataset: DATASET) => {
  if (!dataset.can_manage || !canUpdate.value) {
    message.warning('暂无修改权限，请联系管理员开通')
    return
  }
  closeDatasetMenu()
  authEditingDataset.value = dataset
  showDatasetAuthModal.value = true
}

const closeDatasetAuthModal = () => {
  showDatasetAuthModal.value = false
  authEditingDataset.value = null
}

const handleDatasetAuthSaved = async () => {
  closeDatasetAuthModal()
  await fetchDatasets()
}

const saveDataset = async () => {
  if (editingDataset.value && !canUpdate.value) {
    message.warning('暂无修改权限，请联系管理员开通')
    return
  }
  if (!editingDataset.value && !canCreate.value) {
    message.warning('暂无创建权限，请联系管理员开通')
    return
  }
  modalLoading.value = true
  try {
    const name = datasetForm.value.name.trim()
    const description = datasetForm.value.description.trim()
    if (editingDataset.value) {
      // 更新
      await api.knowledge.updateDataset(editingDataset.value.id, {
        name,
        description,
      })
    } else {
      // 新建
      await api.knowledge.createDataset({
        name,
        description,
      })
    }
    await fetchDatasets()
    closeDatasetModal()
  } catch (e) {
    console.error('保存数据集失败:', e)
    alert('保存失败，请重试')
  } finally {
    modalLoading.value = false
  }
}

const confirmDeleteDataset = async (dataset: DATASET) => {
  if (!dataset.can_manage || !canDelete.value) {
    message.warning('暂无删除权限，请联系管理员开通')
    return
  }
  closeDatasetMenu()
  try {
    await dialog.confirm(`确定要删除数据集 "${dataset.name}" 吗？此操作不可恢复。`)

    // 假设 deleteDatasets 接受 ids 数组
    await api.knowledge.deleteDatasets({ ids: [dataset.id] })
    await fetchDatasets()
  } catch (e) {
    if (e instanceof Error && e.message === 'Cancel') return
    console.error('删除数据集失败:', e)
    alert('删除失败')
  }
}

// 文档操作
const fetchDocs = async () => {
  if (!activeDatasetId.value) return
  docsLoading.value = true
  try {
    const res = await api.knowledge.listDocuments(activeDatasetId.value, { page: 1, page_size: 100 })
    docs.value = res.data || []
    docsLoadedForActiveDataset.value = true
  } catch (e) {
    console.error('加载文档失败:', e)
  } finally {
    docsLoading.value = false
  }
  ensureDocsPolling()
}

const clearDocsPolling = () => {
  if (docsPollingTimer.value !== null) {
    window.clearInterval(docsPollingTimer.value)
    docsPollingTimer.value = null
  }
}

const ensureDocsPolling = () => {
  if (!activeDatasetId.value) {
    clearDocsPolling()
    return
  }
  const hasRunning = docs.value.some(doc => doc.run === 'RUNNING')
  if (!hasRunning) {
    clearDocsPolling()
    return
  }
  if (docsPollingTimer.value !== null) return
  docsPollingTimer.value = window.setInterval(async () => {
    if (!activeDatasetId.value) {
      clearDocsPolling()
      return
    }
    if (docsLoading.value) return
    await fetchDocs()
    const stillRunning = docs.value.some(doc => doc.run === 'RUNNING')
    if (!stillRunning) clearDocsPolling()
  }, 3000)
}

const handleUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement
  const files = input.files
  if (!files || files.length === 0 || !activeDatasetId.value || !activeDatasetCanManage.value) return
  
  uploading.value = true
  const formData = new FormData()
  for (let i = 0; i < files.length; i++) {
    formData.append('file', files[i])
  }
  
  try {
    await api.knowledge.uploadDocuments(activeDatasetId.value, formData)
    await fetchDocs()
    // 更新数据集信息（如文档数量）
    await fetchDatasets()
  } catch (e) {
    console.error('上传失败:', e)
    alert('上传失败')
  } finally {
    uploading.value = false
    if (fileInputRef.value) fileInputRef.value.value = ''
  }
}

const parseDocuments = async (doc: DOCUMENT) => {
  if (!activeDatasetId.value || !activeDatasetCanManage.value) return
  try {
    // 假设 parseDocuments 接受 document_ids 数组
    await api.knowledge.parseDocuments(activeDatasetId.value, { document_ids: [doc.id] })
    await fetchDocs()
  } catch (e) {
    console.error('解析失败:', e)
    alert('解析失败')
  }
}

const isStoppingDoc = (docId: string) => Boolean(stoppingDocIds.value[docId])

const stopParsingDocuments = async (doc: DOCUMENT) => {
  if (!activeDatasetId.value || !activeDatasetCanManage.value || isStoppingDoc(doc.id)) return
  stoppingDocIds.value = { ...stoppingDocIds.value, [doc.id]: true }
  try {
    const res = await api.knowledge.stopParsingDocuments(activeDatasetId.value, { document_ids: [doc.id] })
    if (res.code === 0) {
      await fetchDocs()
      return
    }
    alert('停止解析失败')
  } catch (e) {
    console.error('停止解析失败:', e)
    alert('停止解析失败')
  } finally {
    const next = { ...stoppingDocIds.value }
    delete next[doc.id]
    stoppingDocIds.value = next
  }
}

const handleDownload = async (doc: DOCUMENT) => {
  if (!activeDatasetId.value) return
  try {
    const res = await api.knowledge.downloadDocument(activeDatasetId.value, doc.id)
    const blob = res.data
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = doc.name || 'document'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (e) {
    console.error('下载失败:', e)
    alert('下载失败')
  }
}

const openRenameDocModal = (doc: DOCUMENT) => {
  if (!activeDatasetCanManage.value) return
  editingDoc.value = doc
  renameDocForm.value = { name: doc.name || '' }
  showRenameDocModal.value = true
}

const closeRenameDocModal = () => {
  showRenameDocModal.value = false
  editingDoc.value = null
  renameDocForm.value = { name: '' }
}

const saveRenameDoc = async () => {
  if (!editingDoc.value || !activeDatasetId.value || !activeDatasetCanManage.value) return
  modalLoading.value = true
  try {
    await api.knowledge.updateDocument(activeDatasetId.value, editingDoc.value.id, {
      document_id: editingDoc.value.id, // Some APIs need this in body
      name: renameDocForm.value.name.trim(),
    })
    await fetchDocs()
    closeRenameDocModal()
  } catch (e) {
    console.error('重命名失败:', e)
    alert('重命名失败')
  } finally {
    modalLoading.value = false
  }
}

const confirmDeleteDoc = async (doc: DOCUMENT) => {
  if (!activeDatasetId.value || !activeDatasetCanManage.value) return
  try {
    await dialog.confirm(`确定要删除文档 "${doc.name}" 吗？`)
    
    await api.knowledge.deleteDocuments(activeDatasetId.value, { ids: [doc.id] })
    await fetchDocs()
    await fetchDatasets() // Update counts
  } catch (e) {
    if (e instanceof Error && e.message === 'Cancel') return
    console.error('删除文档失败:', e)
    alert('删除失败')
  }
}

// 初始化
onMounted(async () => {
  await fetchDatasets()
})

onUnmounted(() => {
  clearDocsPolling()
  closeChunkModal()
})

watch(activeDatasetId, (nextId, prevId) => {
  if (nextId !== prevId) {
    clearDocsPolling()
    if (showChunkModal.value) closeChunkModal()
    if (showRetrieveModal.value) closeRetrieveModal()
    retrieveDocId.value = ''
    retrieveResult.value = null
    if (!nextId) {
      resetDocsState()
    }
  }
})
</script>

<style scoped>
/* 隐藏滚动条但保留功能 (Optional) */
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}
.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
</style>
