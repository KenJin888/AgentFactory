import request from "@/utils/request";

const API_PATH = "/ai/ai_skills";

const AISkillsAPI = {
  // 列出技能列表
  listSkills(forceRefresh: boolean = false) {
    return request<ApiResponse<SkillsListResponse>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: { force_refresh: forceRefresh },
    });
  },

  // 获取技能详情
  getSkillDetail(name: string) {
    return request<ApiResponse<SkillDetailResponse>>({
      url: `${API_PATH}/detail/${name}`,
      method: "get",
    });
  },

  // 创建技能 - 通过文件上传
  createSkillWithFile(name: string, file: File) {
    const formData = new FormData();
    formData.append("file", file);

    return request<ApiResponse>({
      url: `${API_PATH}/create/${name}`,
      method: "post",
      data: formData,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  // 创建技能 - 通过URL
  createSkillWithUrl(name: string, url: string) {
    return request<ApiResponse>({
      url: `${API_PATH}/create/${name}`,
      method: "post",
      data: { url },
    });
  },

  // 更新技能内容
  updateSkill(name: string, content: string) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${name}`,
      method: "put",
      data: { content },
    });
  },

  // 删除技能
  deleteSkill(name: string) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete/${name}`,
      method: "delete",
    });
  },

  // 列出技能目录下的文件
  listSkillFiles(path?: string) {
    return request<ApiResponse<SkillFilesResponse>>({
      url: `/ai/ai_skills/file/list`,
      method: "get",
      params: path ? { path } : {},
    });
  },

  // 读取技能文件内容
  readSkillFile(path: string) {
    return request<ApiResponse<SkillFileContentResponse>>({
      url: `/ai/ai_skills/file/read`,
      method: "post",
      data: { path },
    });
  },
};

export default AISkillsAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 技能列表响应
export interface SkillsListResponse {
  skills: { name: string; description: string }[];
}

// 技能详情响应
export interface SkillDetailResponse {
  content: string;
}

// 创建技能请求（URL方式）
export interface CreateSkillWithUrlRequest {
  url: string;
}

// 更新技能请求
export interface UpdateSkillRequest {
  content: string;
}

// 技能文件列表响应
export interface SkillFilesResponse {
  current_path: string;
  items: Array<{
    name: string;
    type: 'file' | 'directory';
    is_dir?: boolean;
    size?: number;
  }>;
}

// 技能文件内容响应
export interface SkillFileContentResponse {
  content: string;
  file_path: string;
  url?: string;
}