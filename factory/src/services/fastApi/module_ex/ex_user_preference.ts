import request from "@/utils/request";

const API_PATH = "/ex/ex_user_preference";

const ExUserPreferenceAPI = {
  listExUserPreference(query: ExUserPreferencePageQuery) {
    return request<ApiResponse<PageResult<ExUserPreferenceTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  detailExUserPreference(id: number) {
    return request<ApiResponse<ExUserPreferenceTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  createExUserPreference(body: ExUserPreferenceForm) {
    return request<ApiResponse<ExUserPreferenceTable>>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateExUserPreference(id: number, body: ExUserPreferenceUpdateForm) {
    return request<ApiResponse<ExUserPreferenceTable>>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteExUserPreference(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  getMyPreference(prefKey: string) {
    return request<ApiResponse<ExUserPreferenceTable | null>>({
      url: `${API_PATH}/my/key/${encodeURIComponent(prefKey)}`,
      method: "get",
    });
  },

  setMyPreference(prefKey: string, body: ExUserPreferenceSetMyForm) {
    return request<ApiResponse<ExUserPreferenceTable>>({
      url: `${API_PATH}/my/key/${encodeURIComponent(prefKey)}`,
      method: "put",
      data: body,
    });
  },
};

export default ExUserPreferenceAPI;

export interface ExUserPreferencePageQuery extends PageQuery {
  user_id?: number;
  pref_key?: string;
  status?: string;
  created_time?: string[];
  updated_time?: string[];
}

export interface ExUserPreferenceTable extends BaseType {
  user_id?: number;
  pref_key?: string;
  pref_value?: string | null;
  created_by?: CommonType;
  updated_by?: CommonType;
}

export interface ExUserPreferenceForm extends BaseFormType {
  user_id: number;
  pref_key: string;
  pref_value?: string | null;
}

export interface ExUserPreferenceUpdateForm extends BaseFormType {
  user_id?: number;
  pref_key?: string;
  pref_value?: string | null;
}

export interface ExUserPreferenceSetMyForm {
  pref_value?: string | null;
}
