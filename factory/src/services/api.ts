import ParamsAPI, {ConfigForm, ConfigPageQuery, ConfigTable} from './fastApi/module_system/params';
import AuthAPI from './fastApi/module_system/auth';
import DictAPI from './fastApi/module_system/dict';
import DeptAPI from './fastApi/module_system/dept';
import PositionAPI from './fastApi/module_system/position';
import MenuAPI from './fastApi/module_system/menu';
import FileAPI, {DownloadBody, UploadResult} from './fastApi/module_system/file';
import LogAPI, {LogPageQuery, LogTable} from './fastApi/module_system/log';
import NoticeAPI, {NoticeForm, NoticePageQuery, NoticeTable} from './fastApi/module_system/notice';
import ServerAPI, {ServerInfo} from './fastApi/module_monitor/server';
import {knowledgeApi} from './api/knowledge'
import {chatApi} from './api/chat'
import {UserAPI, UserInfo} from './fastApi/module_system/user';
import RoleAPI, {
  permissionDataType,
  RoleForm,
  RoleTable,
  TablePageQuery as RolePageQuery
} from './fastApi/module_system/role';
import AiAgentAPI, {
  AiAgentForm,
  AiAgentManagePayload,
  AiAgentPageQuery,
  AiAgentPublishPayload,
  AiAgentTable
} from './fastApi/module_ai/ai_agent';
import {Auth} from '@/utils/auth';

// API 方法集合 For Fast
let modelsConfigId: number | undefined;
let sysmodelConfigId: number | undefined;

export const api = {
  // 认证相关
  auth: {
    login: async (data: any) => {
      const response = await AuthAPI.login(data)
      return response.data.data;
    },
    register: (data: { username: string; password: string; confirmPassword: string }) => UserAPI.registerUser(data),
    resetPassword: (data: { username: string; new_password: string; confirmPassword: string }) => UserAPI.forgetPassword(data),
  },
  
  // 用户相关
  user: {
    getProfile: (): Promise<UserInfo | null> => Auth.getCurrentUserInfo(),
    updateProfile: async (data: any): Promise<ApiResponse<UserInfo>> => {
      const body = {
        email: data?.email,
        mobile: data?.mobile ?? data?.phone,
        avatar: data?.avatar ?? data?.avatar_url,
        name: data?.name,
        username: data?.username,
        gender: data?.gender,
      };
      const res = await UserAPI.updateCurrentUserInfo(body);
      return res.data;
    },
    uploadCurrentUserAvatar: async (body: any): Promise<ApiResponse<UploadFilePath>> => {
      const res = await UserAPI.uploadCurrentUserAvatar(body);
      return res.data;
    },
    changeCurrentUserPassword: async (body: any): Promise<ApiResponse<any>> => {
      const res = await UserAPI.changeCurrentUserPassword(body);
      return res.data;
    },
    resetUserPassword: async (body: any): Promise<ApiResponse<any>> => {
      const res = await UserAPI.resetUserPassword(body);
      return res.data;
    },
    registerUser: async (body: any): Promise<ApiResponse<any>> => {
      const res = await UserAPI.registerUser(body);
      return res.data;
    },
    forgetPassword: async (body: any): Promise<ApiResponse<any>> => {
      const res = await UserAPI.forgetPassword(body);
      return res.data;
    },
    listUser: async (query: any): Promise<ApiResponse<PageResult<UserInfo[]>>> => {
      const res = await UserAPI.listUser(query);
      return res.data;
    },
    detailUser: async (id: number): Promise<ApiResponse<UserInfo>> => {
      const res = await UserAPI.detailUser(id);
      return res.data;
    },
    createUser: async (body: any): Promise<ApiResponse<any>> => {
      const res = await UserAPI.createUser(body);
      return res.data;
    },
    updateUser: async (id: number, body: any): Promise<ApiResponse<any>> => {
      const res = await UserAPI.updateUser(id, body);
      return res.data;
    },
    deleteUser: async (body: number[]): Promise<ApiResponse<any>> => {
      const res = await UserAPI.deleteUser(body);
      return res.data;
    },
    batchUser: async (body: any): Promise<ApiResponse<any>> => {
      const res = await UserAPI.batchUser(body);
      return res.data;
    },
    exportUser: async (body: any): Promise<any> => {
      const res = await UserAPI.exportUser(body);
      return res.data;
    },
    downloadTemplateUser: async (): Promise<any> => {
      const res = await UserAPI.downloadTemplateUser();
      return res.data;
    },
    importUser: async (body: FormData): Promise<any> => {
      const res = await UserAPI.importUser(body);
      return res.data;
    }
  },

  // 角色相关
  role: {
    listRole: async (query: RolePageQuery): Promise<ApiResponse<PageResult<RoleTable[]>>> => {
      const res = await RoleAPI.listRole(query);
      return res.data;
    },
    detailRole: async (id: number): Promise<ApiResponse<RoleTable>> => {
      const res = await RoleAPI.detailRole(id);
      return res.data;
    },
    createRole: async (body: RoleForm): Promise<ApiResponse<any>> => {
      const res = await RoleAPI.createRole(body);
      return res.data;
    },
    updateRole: async (id: number, body: RoleForm): Promise<ApiResponse<any>> => {
      const res = await RoleAPI.updateRole(id, body);
      return res.data;
    },
    deleteRole: async (ids: number[]): Promise<ApiResponse<any>> => {
      const res = await RoleAPI.deleteRole(ids);
      return res.data;
    },
    setPermission: async (body: permissionDataType): Promise<ApiResponse<any>> => {
      const res = await RoleAPI.setPermission(body);
      return res.data;
    },
    batchRole: async (body: any): Promise<ApiResponse<any>> => {
      const res = await RoleAPI.batchRole(body);
      return res.data;
    },
    assignRolePerm: async (id: number, body: { menu_ids: number[] }): Promise<ApiResponse<any>> => {
      const res = await RoleAPI.assignRolePerm(id, body);
      return res.data;
    },
    exportRole: async (body: any): Promise<any> => {
      const res = await RoleAPI.exportRole(body);
      return res.data;
    }
  },

  // 部门相关
  dept: {
    listDept: async (query?: any): Promise<ApiResponse<any>> => {
      const res = await DeptAPI.listDept(query);
      return res.data;
    },
    detailDept: async (id: number): Promise<ApiResponse<any>> => {
      const res = await DeptAPI.detailDept(id);
      return res.data;
    },
    createDept: async (body: any): Promise<ApiResponse<any>> => {
      const res = await DeptAPI.createDept(body);
      return res.data;
    },
    updateDept: async (id: number, body: any): Promise<ApiResponse<any>> => {
      const res = await DeptAPI.updateDept(id, body);
      return res.data;
    },
    deleteDept: async (ids: number[]): Promise<ApiResponse<any>> => {
      const res = await DeptAPI.deleteDept(ids);
      return res.data;
    },
    batchDept: async (body: any): Promise<ApiResponse<any>> => {
      const res = await DeptAPI.batchDept(body);
      return res.data;
    }
  },

  // 岗位相关
  position: {
    listPosition: async (query?: any): Promise<ApiResponse<any>> => {
      const res = await PositionAPI.listPosition(query);
      return res.data;
    },
    detailPosition: async (id: number): Promise<ApiResponse<any>> => {
      const res = await PositionAPI.detailPosition(id);
      return res.data;
    },
    createPosition: async (body: any): Promise<ApiResponse<any>> => {
      const res = await PositionAPI.createPosition(body);
      return res.data;
    },
    updatePosition: async (id: number, body: any): Promise<ApiResponse<any>> => {
      const res = await PositionAPI.updatePosition(id, body);
      return res.data;
    },
    deletePosition: async (ids: number[]): Promise<ApiResponse<any>> => {
      const res = await PositionAPI.deletePosition(ids);
      return res.data;
    },
    batchPosition: async (body: any): Promise<ApiResponse<any>> => {
      const res = await PositionAPI.batchPosition(body);
      return res.data;
    },
    exportPosition: async (body: any): Promise<any> => {
      const res = await PositionAPI.exportPosition(body);
      return res.data;
    }
  },

  // 菜单相关
  menu: {
    listMenu: async (query?: any): Promise<ApiResponse<any>> => {
      const res = await MenuAPI.listMenu(query);
      return res.data;
    }
  },

  // 日志相关
  log: {
    listLog: async (query: LogPageQuery): Promise<ApiResponse<PageResult<LogTable[]>>> => {
      const res = await LogAPI.listLog(query);
      return res.data;
    },
    detailLog: async (id: number): Promise<ApiResponse<LogTable>> => {
      const res = await LogAPI.detailLog(id);
      return res.data;
    },
    deleteLog: async (ids: number[]): Promise<ApiResponse<any>> => {
      const res = await LogAPI.deleteLog(ids);
      return res.data;
    },
    exportLog: async (body: LogPageQuery): Promise<any> => {
      const res = await LogAPI.exportLog(body);
      return res.data;
    }
  },

  // 公告相关
  notice: {
    listNotice: async (query: NoticePageQuery): Promise<ApiResponse<PageResult<NoticeTable[]>>> => {
      const res = await NoticeAPI.listNotice(query);
      return res.data;
    },
    detailNotice: async (id: number): Promise<ApiResponse<NoticeTable>> => {
      const res = await NoticeAPI.detailNotice(id);
      return res.data;
    },
    createNotice: async (body: NoticeForm): Promise<ApiResponse<any>> => {
      const res = await NoticeAPI.createNotice(body);
      return res.data;
    },
    updateNotice: async (id: number, body: NoticeForm): Promise<ApiResponse<any>> => {
      const res = await NoticeAPI.updateNotice(id, body);
      return res.data;
    },
    deleteNotice: async (ids: number[]): Promise<ApiResponse<any>> => {
      const res = await NoticeAPI.deleteNotice(ids);
      return res.data;
    },
    exportNotice: async (body: NoticePageQuery): Promise<any> => {
      const res = await NoticeAPI.exportNotice(body);
      return res.data;
    }
  },

  // 参数相关
  params: {
    getInitConfig: async (): Promise<ApiResponse<ConfigTable[]>> => {
      const res = await ParamsAPI.getInitConfig();
      return res.data;
    },
    listParams: async (query: ConfigPageQuery): Promise<ApiResponse<PageResult<ConfigTable[]>>> => {
      const res = await ParamsAPI.listParams(query);
      return res.data;
    },
    detailParams: async (id: number): Promise<ApiResponse<ConfigTable>> => {
      const res = await ParamsAPI.detailParams(id);
      return res.data;
    },
    createParams: async (body: ConfigForm): Promise<ApiResponse<any>> => {
      const res = await ParamsAPI.createParams(body);
      return res.data;
    },
    updateParams: async (id: number, body: ConfigForm): Promise<ApiResponse<any>> => {
      const res = await ParamsAPI.updateParams(id, body);
      return res.data;
    },
    deleteParams: async (ids: number[]): Promise<ApiResponse<any>> => {
      const res = await ParamsAPI.deleteParams(ids);
      return res.data;
    },
    exportParams: async (body: ConfigPageQuery): Promise<any> => {
      const res = await ParamsAPI.exportParams(body);
      return res.data;
    }
  },

  // 文件相关
  file: {
    upload: async (body: FormData): Promise<ApiResponse<UploadResult>> => {
      const res = await FileAPI.upload(body);
      return res.data;
    },
    download: async (body: DownloadBody): Promise<ApiResponse<string>> => {
      const res = await FileAPI.download(body);
      return res.data;
    }
  },

  // 服务器监控相关
  server: {
    getServer: async (): Promise<ApiResponse<ServerInfo>> => {
      const res = await ServerAPI.getServer();
      return res.data;
    }
  },

  // 聊天相关
  chat: chatApi,
  
  // 知识库相关
  knowledge: knowledgeApi,
  
  // 代理相关
  agent: {
    getAgents: async (query: AiAgentPageQuery = {}): Promise<AiAgentTable[]> => {
      const res = await AiAgentAPI.listAiAgent({
        page_no: 1,
        page_size: 100,
        ...query,
      });
      return res.data?.data?.items || [];
    },
    getMyAgents: async (query: AiAgentPageQuery = {}): Promise<AiAgentTable[]> => {
      const res = await AiAgentAPI.listMyAiAgent({
        page_no: 1,
        page_size: 100,
        ...query,
      });
      return res.data?.data?.items || [];
    },
    getSquareAgents: async (query: AiAgentPageQuery = {}): Promise<AiAgentTable[]> => {
      const res = await AiAgentAPI.listSquareAiAgent({
        page_no: 1,
        page_size: 100,
        ...query,
      });
      return res.data?.data?.items || [];
    },
      detailAgent: async (agentId: number): Promise<AiAgentTable | null> => {
          const res = await AiAgentAPI.detailAiAgent(agentId);
          return res.data?.data || null;
      },
    getFavoriteAgents: async (): Promise<AiAgentTable[]> => {
      const res = await AiAgentAPI.listFavoriteAiAgent();
      return res.data?.data || [];
    },
    createAgent: async (body: AiAgentForm) => {
      const res = await AiAgentAPI.createAiAgent(body);
      return res.data;
    },
    updateAgent: async (agentId: number, body: AiAgentForm) => {
      const res = await AiAgentAPI.updateAiAgent(agentId, body);
      return res.data;
    },
      publishAgent: async (agentId: number, body: AiAgentPublishPayload) => {
          const res = await AiAgentAPI.publishAiAgent(agentId, body);
          return res.data;
      },
      manageAgent: async (agentId: number, body: AiAgentManagePayload) => {
          const res = await AiAgentAPI.manageAiAgent(agentId, body);
      return res.data;
    },
    offlineAgent: async (agentId: number) => {
      const res = await AiAgentAPI.offlineAiAgent(agentId);
      return res.data;
    },
      cloneAgent: async (agentId: number) => {
          const res = await AiAgentAPI.cloneAiAgent(agentId);
          return res.data;
      },
    forkAgent: async (agentId: number) => {
        const res = await AiAgentAPI.cloneAiAgent(agentId);
      return res.data;
    },
    deletePrivateAgent: async (agentId: number | string) => {
      const res = await AiAgentAPI.deletePrivateAiAgent(Number(agentId));
      return res.data;
    },
    deleteAgent: async (agentId: number | string) => {
      const res = await AiAgentAPI.deleteAiAgent([Number(agentId)]);
      return res.data;
    },
    getAgentTypes: async () => {
      const res = await DictAPI.getInitDict("ai_agent_type");
      return res.data?.data;
    },
    exportAgents: async (query: AiAgentPageQuery = {}) => {
      const res = await AiAgentAPI.exportAiAgent(query);
      return res.data;
    },
    downloadAgentTemplate: async () => {
      const res = await AiAgentAPI.downloadTemplateAiAgent();
      return res.data;
    },
    importAgents: async (body: FormData) => {
      const res = await AiAgentAPI.importAiAgent(body);
      return res.data;
    },
  },
  
  // 模型相关
  model: {
    getModels: async () => {
      if (modelsConfigId) {
        try {
          const res = await ParamsAPI.detailParams(modelsConfigId);
          if (res.data?.data) {
            return JSON.parse(res.data.data.config_value || '[]');
          }
        } catch (e) {
          modelsConfigId = undefined;
        }
      }

      const res = await ParamsAPI.listParams({
        page_no: 1,
        page_size: 10,
        config_key: 'aisaas_models'
      });
      const list = res.data?.data?.items;
      if (list && list.length > 0) {
        modelsConfigId = Number(list[0].id);
        try {
          return JSON.parse(list[0].config_value || '[]');
        } catch (e) {
          console.error('Failed to parse model config', e);
          return [];
        }
      }
      return [];
    },
    setModels: async (data: any) => {
      const configValue = JSON.stringify(data);
      const configName = 'aisaas_models';
      const configKey = 'aisaas_models';

      if (modelsConfigId) {
        try {
          return await ParamsAPI.updateParams(modelsConfigId, {
            config_name: configName,
            config_key: configKey,
            config_value: configValue,
            config_type: true
          });
        } catch (e) {
          modelsConfigId = undefined;
        }
      }

      const res = await ParamsAPI.listParams({
        page_no: 1,
        page_size: 10,
        config_key: 'aisaas_models'
      });
      
      const list = res.data?.data?.items;
      if (list && list.length > 0) {
        const config = list[0];
        if (config.id) {
          modelsConfigId = Number(config.id);
          return ParamsAPI.updateParams(Number(config.id), {
            ...config,
            config_value: configValue
          });
        }
      }
      return ParamsAPI.createParams({
        config_name: configName,
        config_key: configKey,
        config_value: configValue,
        config_type: true
      });
    },
  },
  // 系统模型配置
  sysmodel: {
    getSysModels: async () => {
      if (sysmodelConfigId) {
        try {
          const res = await ParamsAPI.detailParams(sysmodelConfigId);
          if (res.data?.data) {
            return JSON.parse(res.data.data.config_value || '{}');
          }
        } catch (e) {
          sysmodelConfigId = undefined;
        }
      }

      const res = await ParamsAPI.listParams({
        page_no: 1,
        page_size: 10,
        config_key: 'aisaas_sysmodel'
      });
      const list = res.data?.data?.items;
      if (list && list.length > 0) {
        sysmodelConfigId = Number(list[0].id);
        try {
          return JSON.parse(list[0].config_value || '{}');
        } catch (e) {
          console.error('Failed to parse sysmodel config', e);
          return {};
        }
      }
      return {};
    },
    setSysModels: async (data: any) => {
      const configValue = JSON.stringify(data);
      const configName = 'aisaas_sysmodel';
      const configKey = 'aisaas_sysmodel';

      if (sysmodelConfigId) {
        try {
          return await ParamsAPI.updateParams(sysmodelConfigId, {
            config_name: configName,
            config_key: configKey,
            config_value: configValue,
            config_type: true
          });
        } catch (e) {
          sysmodelConfigId = undefined;
        }
      }

      const res = await ParamsAPI.listParams({
        page_no: 1,
        page_size: 10,
        config_key: 'aisaas_sysmodel'
      });
      
      const list = res.data?.data?.items;
      if (list && list.length > 0) {
        const config = list[0];
        if (config.id) {
          sysmodelConfigId = Number(config.id);
          return ParamsAPI.updateParams(Number(config.id), {
            ...config,
            config_value: configValue
          });
        }
      }
      return ParamsAPI.createParams({
        config_name: configName,
        config_key: configKey,
        config_value: configValue,
        config_type: true
      });
    },
  }
};
