// src/types.ts

export enum SubscriptionStatus {
  FREE = 'Free',
  PRO = 'Pro',
}

// 🔥 新增：补全 AgentCategory 定义
export interface AgentCategory {
  id: string;
  name: string;
  icon: string;
  sort_order: number;
}

export interface User {
  id: number;
  username: string;
  is_admin: boolean;
  is_pro: boolean; 
  email?: string;
  phone?: string;
  avatar_url?: string;
  membership_expires_at?: string;
  subscription_status?: string;
}

// Agent 类型设计待定， 参考： ai_agent
export interface Agent {
  id: number;
  name: string;
  description: string;
  system_prompt: string;
  model: string;
  category: string;
  creator_id?: number | null; 
  review_prompt?: string;
  trigger_text?: string;
  enable_upload?: boolean;
  enable_voice?: boolean;
  enable_thinking?: boolean;
  enable_search?: boolean;
  // 为了显示方便，有时后端会返回 icon_url，如果没有就用 name[0]
  icon_url?: string; 
}

export interface ChatSession {
  id: number;
  title: string;
  agent_id: number;
  user_id: number;
  agent: Agent;
  updated_at: string;
}
/**
 * 消息类型
 * export interface ChatMessage {
  id: number;
  session_id: number;
  role: 'user' | 'ai' | 'system' | 'assistant';
  content: string;
  created_at: string;
}


export type MessageContent = {
  type: 'text' | 'image' | 'voice' | 'thinking' | 'search' | 'code' | 'error'
  text?: string
  image?: string
  voice?: string
  thinking?: string
  search?: string
  code?: string
  error?: string
} 

export type AssistantMessageBlock = {
  type:
    | 'content'
    | 'search'
    | 'reasoning_content'
    | 'plan'
    | 'error'
    | 'tool_call'
    | 'action'
    | 'image'
    | 'artifact-thinking'
    | 'mcp_ui_resource'
  id?: string
  content?: string
  status:
    | 'success'
    | 'loading'
    | 'cancel'
    | 'error'
    | 'reading'
    | 'optimizing'
    | 'pending'
    | 'granted'
    | 'denied'
  timestamp: number
} 



export type ChatMessage = {
  id: string
  content: UserMessageContent | AssistantMessageBlock[]
  role: 'user' | 'assistant' | 'system' | 'agent'
  timestamp?: number
  status: 'sent' | 'pending' | 'error'
  error: string
  parentId?: string
  conversationId: string // session_id
} */

export interface PaymentRecord {
  id: number;
  out_trade_no: string;
  amount: number;
  status: string;
  created_at: string;
}

export interface KnowledgeDoc {
  id: number;
  title: string;
  description: string;
  file_type: string;
  file_path?: string;
  content?: string;
  created_at: string;
}