// 创建人（owner）

export interface DATASET {
  id: string;
  name: string;
  avatar?: string;
  tenant_id?: string;
  description?: string;
  language?: string;
  document_count?: number;
  chunk_count?: number;
  parse_method?: string;
  create_date?: string;
  update_date?: string;
  created_by?: string;
  updated_by?: string;
  current_right?: number;
  can_view?: boolean;
  can_write?: boolean;
  can_manage?: boolean;
  is_admin?: boolean;
  [key: string]: any;
}

export interface DOCUMENT {
  id: string;
  name?: string;
  dataset_id?: string;
  run?:string; // UNSTART, RUNNING, CANCEL, DONE, FAIL
  progress?: number; // 解析进度
  status?: string;
  size?: number;
  chunk_count?: number;
  create_date?: string;
  update_date?: string;
  [key: string]: any;
}
