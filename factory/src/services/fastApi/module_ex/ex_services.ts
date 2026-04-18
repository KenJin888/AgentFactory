import request from "@/utils/request";

const API_PATH = "/ex/ex_services";

const ExServicesAPI = {
  getMenuTree(query?: ExMenuTreeQuery) {
    return request<ApiResponse<ExMenuTreeResult>>({
      url: `${API_PATH}/menu/tree`,
      method: "get",
      params: query,
    });
  },

  getPluginPermissions() {
    return request<ApiResponse<PluginPermissionSummary>>({
      url: `${API_PATH}/plugin/permissions`,
      method: "get",
    });
  },

  getAllPermissions() {
    return request<ApiResponse<AllPermissionSummary>>({
      url: `${API_PATH}/all/permissions`,
      method: "get",
    });
  },
};

export default ExServicesAPI;

export interface ExMenuTreeQuery {
  name?: string;
  route_path?: string;
  component_path?: string;
  type?: 1 | 2 | 3 | 4;
  permission?: string;
  description?: string;
  status?: string;
  created_time?: string[];
  updated_time?: string[];
  created_id?: number;
  updated_id?: number;
}

export interface ExMenuTreeResult {
  ex_menu_id: number;
  children: ExMenuItem[];
}

export interface ExMenuItem extends BaseType {
  name?: string;
  type?: number;
  order?: number;
  permission?: string;
  icon?: string;
  route_name?: string;
  route_path?: string;
  component_path?: string;
  redirect?: string;
  hidden?: boolean;
  keep_alive?: boolean;
  always_show?: boolean;
  title?: string;
  params?: Record<string, string>[] | null;
  affix?: boolean;
  parent_id?: number | null;
  status?: string;
  description?: string;
  parent_name?: string | null;
  children?: ExMenuItem[] | null;
}

export interface PluginModulePermission {
  module: string;
  permissions: string[];
}

export interface PluginPermissionSummary {
  modules: PluginModulePermission[];
  total_modules: number;
  total_permissions: number;
}

export interface AllPermissionSummary {
  plugin_modules: PluginModulePermission[];
  api_v1_modules: PluginModulePermission[];
  all_permissions: string[];
  total_plugin_modules: number;
  total_api_v1_modules: number;
  total_permissions: number;
}
