--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5 (ServBay)
-- Dumped by pg_dump version 17.5 (ServBay)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: app_ai_mcp; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.app_ai_mcp (
    name character varying(50) NOT NULL,
    type integer NOT NULL,
    url character varying(255),
    command character varying(255),
    args character varying(255),
    env json,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.app_ai_mcp OWNER TO tao;

--
-- Name: TABLE app_ai_mcp; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.app_ai_mcp IS 'MCP 服务器表';


--
-- Name: COLUMN app_ai_mcp.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.name IS 'MCP 名称';


--
-- Name: COLUMN app_ai_mcp.type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.type IS 'MCP 类型(0:stdio 1:sse)';


--
-- Name: COLUMN app_ai_mcp.url; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.url IS '远程 SSE 地址';


--
-- Name: COLUMN app_ai_mcp.command; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.command IS 'MCP 命令';


--
-- Name: COLUMN app_ai_mcp.args; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.args IS 'MCP 命令参数';


--
-- Name: COLUMN app_ai_mcp.env; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.env IS 'MCP 环境变量';


--
-- Name: COLUMN app_ai_mcp.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.id IS '主键ID';


--
-- Name: COLUMN app_ai_mcp.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN app_ai_mcp.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN app_ai_mcp.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.description IS '备注/描述';


--
-- Name: COLUMN app_ai_mcp.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.created_time IS '创建时间';


--
-- Name: COLUMN app_ai_mcp.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.updated_time IS '更新时间';


--
-- Name: COLUMN app_ai_mcp.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.created_id IS '创建人ID';


--
-- Name: COLUMN app_ai_mcp.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_ai_mcp.updated_id IS '更新人ID';


--
-- Name: app_ai_mcp_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.app_ai_mcp_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.app_ai_mcp_id_seq OWNER TO tao;

--
-- Name: app_ai_mcp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.app_ai_mcp_id_seq OWNED BY public.app_ai_mcp.id;


--
-- Name: app_job; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.app_job (
    name character varying(64),
    jobstore character varying(64),
    executor character varying(64),
    trigger character varying(64) NOT NULL,
    trigger_args text,
    func text NOT NULL,
    args text,
    kwargs text,
    "coalesce" boolean,
    max_instances integer,
    start_date character varying(64),
    end_date character varying(64),
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.app_job OWNER TO tao;

--
-- Name: TABLE app_job; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.app_job IS '定时任务调度表';


--
-- Name: COLUMN app_job.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.name IS '任务名称';


--
-- Name: COLUMN app_job.jobstore; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.jobstore IS '存储器';


--
-- Name: COLUMN app_job.executor; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.executor IS '执行器:将运行此作业的执行程序的名称';


--
-- Name: COLUMN app_job.trigger; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.trigger IS '触发器:控制此作业计划的 trigger 对象';


--
-- Name: COLUMN app_job.trigger_args; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.trigger_args IS '触发器参数';


--
-- Name: COLUMN app_job.func; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.func IS '任务函数';


--
-- Name: COLUMN app_job.args; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.args IS '位置参数';


--
-- Name: COLUMN app_job.kwargs; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.kwargs IS '关键字参数';


--
-- Name: COLUMN app_job."coalesce"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job."coalesce" IS '是否合并运行:是否在多个运行时间到期时仅运行作业一次';


--
-- Name: COLUMN app_job.max_instances; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.max_instances IS '最大实例数:允许的最大并发执行实例数';


--
-- Name: COLUMN app_job.start_date; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.start_date IS '开始时间';


--
-- Name: COLUMN app_job.end_date; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.end_date IS '结束时间';


--
-- Name: COLUMN app_job.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.id IS '主键ID';


--
-- Name: COLUMN app_job.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN app_job.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN app_job.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.description IS '备注/描述';


--
-- Name: COLUMN app_job.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.created_time IS '创建时间';


--
-- Name: COLUMN app_job.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.updated_time IS '更新时间';


--
-- Name: COLUMN app_job.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.created_id IS '创建人ID';


--
-- Name: COLUMN app_job.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job.updated_id IS '更新人ID';


--
-- Name: app_job_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.app_job_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.app_job_id_seq OWNER TO tao;

--
-- Name: app_job_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.app_job_id_seq OWNED BY public.app_job.id;


--
-- Name: app_job_log; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.app_job_log (
    job_name character varying(64) NOT NULL,
    job_group character varying(64) NOT NULL,
    job_executor character varying(64) NOT NULL,
    invoke_target character varying(500) NOT NULL,
    job_args character varying(255),
    job_kwargs character varying(255),
    job_trigger character varying(255),
    job_message character varying(500),
    exception_info character varying(2000),
    job_id integer,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL
);


ALTER TABLE public.app_job_log OWNER TO tao;

--
-- Name: TABLE app_job_log; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.app_job_log IS '定时任务调度日志表';


--
-- Name: COLUMN app_job_log.job_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.job_name IS '任务名称';


--
-- Name: COLUMN app_job_log.job_group; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.job_group IS '任务组名';


--
-- Name: COLUMN app_job_log.job_executor; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.job_executor IS '任务执行器';


--
-- Name: COLUMN app_job_log.invoke_target; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.invoke_target IS '调用目标字符串';


--
-- Name: COLUMN app_job_log.job_args; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.job_args IS '位置参数';


--
-- Name: COLUMN app_job_log.job_kwargs; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.job_kwargs IS '关键字参数';


--
-- Name: COLUMN app_job_log.job_trigger; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.job_trigger IS '任务触发器';


--
-- Name: COLUMN app_job_log.job_message; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.job_message IS '日志信息';


--
-- Name: COLUMN app_job_log.exception_info; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.exception_info IS '异常信息';


--
-- Name: COLUMN app_job_log.job_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.job_id IS '任务ID';


--
-- Name: COLUMN app_job_log.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.id IS '主键ID';


--
-- Name: COLUMN app_job_log.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN app_job_log.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN app_job_log.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.description IS '备注/描述';


--
-- Name: COLUMN app_job_log.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.created_time IS '创建时间';


--
-- Name: COLUMN app_job_log.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_job_log.updated_time IS '更新时间';


--
-- Name: app_job_log_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.app_job_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.app_job_log_id_seq OWNER TO tao;

--
-- Name: app_job_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.app_job_log_id_seq OWNED BY public.app_job_log.id;


--
-- Name: app_myapp; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.app_myapp (
    name character varying(64) NOT NULL,
    access_url character varying(500) NOT NULL,
    icon_url character varying(300),
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.app_myapp OWNER TO tao;

--
-- Name: TABLE app_myapp; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.app_myapp IS '应用系统表';


--
-- Name: COLUMN app_myapp.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.name IS '应用名称';


--
-- Name: COLUMN app_myapp.access_url; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.access_url IS '访问地址';


--
-- Name: COLUMN app_myapp.icon_url; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.icon_url IS '应用图标URL';


--
-- Name: COLUMN app_myapp.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.id IS '主键ID';


--
-- Name: COLUMN app_myapp.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN app_myapp.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN app_myapp.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.description IS '备注/描述';


--
-- Name: COLUMN app_myapp.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.created_time IS '创建时间';


--
-- Name: COLUMN app_myapp.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.updated_time IS '更新时间';


--
-- Name: COLUMN app_myapp.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.created_id IS '创建人ID';


--
-- Name: COLUMN app_myapp.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.app_myapp.updated_id IS '更新人ID';


--
-- Name: app_myapp_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.app_myapp_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.app_myapp_id_seq OWNER TO tao;

--
-- Name: app_myapp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.app_myapp_id_seq OWNED BY public.app_myapp.id;


--
-- Name: apscheduler_jobs; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.apscheduler_jobs (
    id character varying(191) NOT NULL,
    next_run_time double precision,
    job_state bytea NOT NULL
);


ALTER TABLE public.apscheduler_jobs OWNER TO tao;

--
-- Name: gen_demo; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.gen_demo (
    name character varying(64) NOT NULL,
    a integer,
    b bigint,
    c double precision,
    d boolean NOT NULL,
    e date,
    f time without time zone,
    g timestamp without time zone,
    h text,
    i json,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.gen_demo OWNER TO tao;

--
-- Name: TABLE gen_demo; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.gen_demo IS '示例表';


--
-- Name: COLUMN gen_demo.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.name IS '名称';


--
-- Name: COLUMN gen_demo.a; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.a IS '整数';


--
-- Name: COLUMN gen_demo.b; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.b IS '大整数';


--
-- Name: COLUMN gen_demo.c; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.c IS '浮点数';


--
-- Name: COLUMN gen_demo.d; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.d IS '布尔型';


--
-- Name: COLUMN gen_demo.e; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.e IS '日期';


--
-- Name: COLUMN gen_demo.f; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.f IS '时间';


--
-- Name: COLUMN gen_demo.g; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.g IS '日期时间';


--
-- Name: COLUMN gen_demo.h; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.h IS '长文本';


--
-- Name: COLUMN gen_demo.i; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.i IS '元数据(JSON格式)';


--
-- Name: COLUMN gen_demo.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.id IS '主键ID';


--
-- Name: COLUMN gen_demo.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN gen_demo.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN gen_demo.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.description IS '备注/描述';


--
-- Name: COLUMN gen_demo.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.created_time IS '创建时间';


--
-- Name: COLUMN gen_demo.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.updated_time IS '更新时间';


--
-- Name: COLUMN gen_demo.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.created_id IS '创建人ID';


--
-- Name: COLUMN gen_demo.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_demo.updated_id IS '更新人ID';


--
-- Name: gen_demo_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.gen_demo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gen_demo_id_seq OWNER TO tao;

--
-- Name: gen_demo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.gen_demo_id_seq OWNED BY public.gen_demo.id;


--
-- Name: gen_table; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.gen_table (
    table_name character varying(200) NOT NULL,
    table_comment character varying(500),
    class_name character varying(100) NOT NULL,
    package_name character varying(100),
    module_name character varying(30),
    business_name character varying(30),
    function_name character varying(100),
    sub_table_name character varying(64) DEFAULT NULL::character varying,
    sub_table_fk_name character varying(64) DEFAULT NULL::character varying,
    parent_menu_id integer,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.gen_table OWNER TO tao;

--
-- Name: TABLE gen_table; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.gen_table IS '代码生成表';


--
-- Name: COLUMN gen_table.table_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.table_name IS '表名称';


--
-- Name: COLUMN gen_table.table_comment; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.table_comment IS '表描述';


--
-- Name: COLUMN gen_table.class_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.class_name IS '实体类名称';


--
-- Name: COLUMN gen_table.package_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.package_name IS '生成包路径';


--
-- Name: COLUMN gen_table.module_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.module_name IS '生成模块名';


--
-- Name: COLUMN gen_table.business_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.business_name IS '生成业务名';


--
-- Name: COLUMN gen_table.function_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.function_name IS '生成功能名';


--
-- Name: COLUMN gen_table.sub_table_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.sub_table_name IS '关联子表的表名';


--
-- Name: COLUMN gen_table.sub_table_fk_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.sub_table_fk_name IS '子表关联的外键名';


--
-- Name: COLUMN gen_table.parent_menu_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.parent_menu_id IS '父菜单ID';


--
-- Name: COLUMN gen_table.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.id IS '主键ID';


--
-- Name: COLUMN gen_table.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN gen_table.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN gen_table.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.description IS '备注/描述';


--
-- Name: COLUMN gen_table.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.created_time IS '创建时间';


--
-- Name: COLUMN gen_table.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.updated_time IS '更新时间';


--
-- Name: COLUMN gen_table.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.created_id IS '创建人ID';


--
-- Name: COLUMN gen_table.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table.updated_id IS '更新人ID';


--
-- Name: gen_table_column; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.gen_table_column (
    column_name character varying(200) NOT NULL,
    column_comment character varying(500),
    column_type character varying(100) NOT NULL,
    column_length character varying(50),
    column_default character varying(200),
    is_pk boolean DEFAULT false NOT NULL,
    is_increment boolean DEFAULT false NOT NULL,
    is_nullable boolean DEFAULT true NOT NULL,
    is_unique boolean DEFAULT false NOT NULL,
    python_type character varying(100),
    python_field character varying(200),
    is_insert boolean DEFAULT true NOT NULL,
    is_edit boolean DEFAULT true NOT NULL,
    is_list boolean DEFAULT true NOT NULL,
    is_query boolean DEFAULT false NOT NULL,
    query_type character varying(50),
    html_type character varying(100),
    dict_type character varying(200),
    sort integer NOT NULL,
    table_id integer NOT NULL,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.gen_table_column OWNER TO tao;

--
-- Name: TABLE gen_table_column; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.gen_table_column IS '代码生成表字段';


--
-- Name: COLUMN gen_table_column.column_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.column_name IS '列名称';


--
-- Name: COLUMN gen_table_column.column_comment; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.column_comment IS '列描述';


--
-- Name: COLUMN gen_table_column.column_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.column_type IS '列类型';


--
-- Name: COLUMN gen_table_column.column_length; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.column_length IS '列长度';


--
-- Name: COLUMN gen_table_column.column_default; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.column_default IS '列默认值';


--
-- Name: COLUMN gen_table_column.is_pk; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_pk IS '是否主键';


--
-- Name: COLUMN gen_table_column.is_increment; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_increment IS '是否自增';


--
-- Name: COLUMN gen_table_column.is_nullable; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_nullable IS '是否允许为空';


--
-- Name: COLUMN gen_table_column.is_unique; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_unique IS '是否唯一';


--
-- Name: COLUMN gen_table_column.python_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.python_type IS 'Python类型';


--
-- Name: COLUMN gen_table_column.python_field; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.python_field IS 'Python字段名';


--
-- Name: COLUMN gen_table_column.is_insert; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_insert IS '是否为新增字段';


--
-- Name: COLUMN gen_table_column.is_edit; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_edit IS '是否编辑字段';


--
-- Name: COLUMN gen_table_column.is_list; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_list IS '是否列表字段';


--
-- Name: COLUMN gen_table_column.is_query; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.is_query IS '是否查询字段';


--
-- Name: COLUMN gen_table_column.query_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.query_type IS '查询方式';


--
-- Name: COLUMN gen_table_column.html_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.html_type IS '显示类型';


--
-- Name: COLUMN gen_table_column.dict_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.dict_type IS '字典类型';


--
-- Name: COLUMN gen_table_column.sort; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.sort IS '排序';


--
-- Name: COLUMN gen_table_column.table_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.table_id IS '归属表编号';


--
-- Name: COLUMN gen_table_column.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.id IS '主键ID';


--
-- Name: COLUMN gen_table_column.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN gen_table_column.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN gen_table_column.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.description IS '备注/描述';


--
-- Name: COLUMN gen_table_column.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.created_time IS '创建时间';


--
-- Name: COLUMN gen_table_column.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.updated_time IS '更新时间';


--
-- Name: COLUMN gen_table_column.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.created_id IS '创建人ID';


--
-- Name: COLUMN gen_table_column.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.gen_table_column.updated_id IS '更新人ID';


--
-- Name: gen_table_column_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.gen_table_column_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gen_table_column_id_seq OWNER TO tao;

--
-- Name: gen_table_column_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.gen_table_column_id_seq OWNED BY public.gen_table_column.id;


--
-- Name: gen_table_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.gen_table_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gen_table_id_seq OWNER TO tao;

--
-- Name: gen_table_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.gen_table_id_seq OWNED BY public.gen_table.id;


--
-- Name: sys_dept; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_dept (
    name character varying(64) NOT NULL,
    "order" integer NOT NULL,
    code character varying(16),
    leader character varying(32),
    phone character varying(11),
    email character varying(64),
    parent_id integer,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.sys_dept OWNER TO tao;

--
-- Name: TABLE sys_dept; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_dept IS '部门表';


--
-- Name: COLUMN sys_dept.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.name IS '部门名称';


--
-- Name: COLUMN sys_dept."order"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept."order" IS '显示排序';


--
-- Name: COLUMN sys_dept.code; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.code IS '部门编码';


--
-- Name: COLUMN sys_dept.leader; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.leader IS '部门负责人';


--
-- Name: COLUMN sys_dept.phone; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.phone IS '手机';


--
-- Name: COLUMN sys_dept.email; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.email IS '邮箱';


--
-- Name: COLUMN sys_dept.parent_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.parent_id IS '父级部门ID';


--
-- Name: COLUMN sys_dept.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.id IS '主键ID';


--
-- Name: COLUMN sys_dept.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_dept.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_dept.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.description IS '备注/描述';


--
-- Name: COLUMN sys_dept.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.created_time IS '创建时间';


--
-- Name: COLUMN sys_dept.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.updated_time IS '更新时间';


--
-- Name: COLUMN sys_dept.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.created_id IS '创建人ID';


--
-- Name: COLUMN sys_dept.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dept.updated_id IS '更新人ID';


--
-- Name: sys_dept_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_dept_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_dept_id_seq OWNER TO tao;

--
-- Name: sys_dept_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_dept_id_seq OWNED BY public.sys_dept.id;


--
-- Name: sys_dict_data; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_dict_data (
    dict_sort integer NOT NULL,
    dict_label character varying(255) NOT NULL,
    dict_value character varying(255) NOT NULL,
    css_class character varying(255),
    list_class character varying(255),
    is_default boolean NOT NULL,
    dict_type character varying(255) NOT NULL,
    dict_type_id integer NOT NULL,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL
);


ALTER TABLE public.sys_dict_data OWNER TO tao;

--
-- Name: TABLE sys_dict_data; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_dict_data IS '字典数据表';


--
-- Name: COLUMN sys_dict_data.dict_sort; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.dict_sort IS '字典排序';


--
-- Name: COLUMN sys_dict_data.dict_label; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.dict_label IS '字典标签';


--
-- Name: COLUMN sys_dict_data.dict_value; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.dict_value IS '字典键值';


--
-- Name: COLUMN sys_dict_data.css_class; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.css_class IS '样式属性（其他样式扩展）';


--
-- Name: COLUMN sys_dict_data.list_class; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.list_class IS '表格回显样式';


--
-- Name: COLUMN sys_dict_data.is_default; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.is_default IS '是否默认（True是 False否）';


--
-- Name: COLUMN sys_dict_data.dict_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.dict_type IS '字典类型';


--
-- Name: COLUMN sys_dict_data.dict_type_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.dict_type_id IS '字典类型ID';


--
-- Name: COLUMN sys_dict_data.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.id IS '主键ID';


--
-- Name: COLUMN sys_dict_data.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_dict_data.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_dict_data.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.description IS '备注/描述';


--
-- Name: COLUMN sys_dict_data.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.created_time IS '创建时间';


--
-- Name: COLUMN sys_dict_data.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_data.updated_time IS '更新时间';


--
-- Name: sys_dict_data_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_dict_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_dict_data_id_seq OWNER TO tao;

--
-- Name: sys_dict_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_dict_data_id_seq OWNED BY public.sys_dict_data.id;


--
-- Name: sys_dict_type; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_dict_type (
    dict_name character varying(64) NOT NULL,
    dict_type character varying(255) NOT NULL,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL
);


ALTER TABLE public.sys_dict_type OWNER TO tao;

--
-- Name: TABLE sys_dict_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_dict_type IS '字典类型表';


--
-- Name: COLUMN sys_dict_type.dict_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_type.dict_name IS '字典名称';


--
-- Name: COLUMN sys_dict_type.dict_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_type.dict_type IS '字典类型';


--
-- Name: COLUMN sys_dict_type.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_type.id IS '主键ID';


--
-- Name: COLUMN sys_dict_type.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_type.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_dict_type.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_type.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_dict_type.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_type.description IS '备注/描述';


--
-- Name: COLUMN sys_dict_type.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_type.created_time IS '创建时间';


--
-- Name: COLUMN sys_dict_type.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_dict_type.updated_time IS '更新时间';


--
-- Name: sys_dict_type_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_dict_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_dict_type_id_seq OWNER TO tao;

--
-- Name: sys_dict_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_dict_type_id_seq OWNED BY public.sys_dict_type.id;


--
-- Name: sys_log; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_log (
    type integer NOT NULL,
    request_path character varying(255) NOT NULL,
    request_method character varying(10) NOT NULL,
    request_payload text,
    request_ip character varying(50),
    login_location character varying(255),
    request_os character varying(64),
    request_browser character varying(64),
    response_code integer NOT NULL,
    response_json text,
    process_time character varying(20),
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.sys_log OWNER TO tao;

--
-- Name: TABLE sys_log; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_log IS '系统日志表';


--
-- Name: COLUMN sys_log.type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.type IS '日志类型(1登录日志 2操作日志)';


--
-- Name: COLUMN sys_log.request_path; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.request_path IS '请求路径';


--
-- Name: COLUMN sys_log.request_method; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.request_method IS '请求方式';


--
-- Name: COLUMN sys_log.request_payload; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.request_payload IS '请求体';


--
-- Name: COLUMN sys_log.request_ip; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.request_ip IS '请求IP地址';


--
-- Name: COLUMN sys_log.login_location; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.login_location IS '登录位置';


--
-- Name: COLUMN sys_log.request_os; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.request_os IS '操作系统';


--
-- Name: COLUMN sys_log.request_browser; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.request_browser IS '浏览器';


--
-- Name: COLUMN sys_log.response_code; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.response_code IS '响应状态码';


--
-- Name: COLUMN sys_log.response_json; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.response_json IS '响应体';


--
-- Name: COLUMN sys_log.process_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.process_time IS '处理时间';


--
-- Name: COLUMN sys_log.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.id IS '主键ID';


--
-- Name: COLUMN sys_log.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_log.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_log.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.description IS '备注/描述';


--
-- Name: COLUMN sys_log.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.created_time IS '创建时间';


--
-- Name: COLUMN sys_log.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.updated_time IS '更新时间';


--
-- Name: COLUMN sys_log.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.created_id IS '创建人ID';


--
-- Name: COLUMN sys_log.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_log.updated_id IS '更新人ID';


--
-- Name: sys_log_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_log_id_seq OWNER TO tao;

--
-- Name: sys_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_log_id_seq OWNED BY public.sys_log.id;


--
-- Name: sys_menu; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_menu (
    name character varying(50) NOT NULL,
    type integer NOT NULL,
    "order" integer NOT NULL,
    permission character varying(100),
    icon character varying(50),
    route_name character varying(100),
    route_path character varying(200),
    component_path character varying(200),
    redirect character varying(200),
    hidden boolean NOT NULL,
    keep_alive boolean NOT NULL,
    always_show boolean NOT NULL,
    title character varying(50),
    params json,
    affix boolean NOT NULL,
    parent_id integer,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL
);


ALTER TABLE public.sys_menu OWNER TO tao;

--
-- Name: TABLE sys_menu; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_menu IS '菜单表';


--
-- Name: COLUMN sys_menu.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.name IS '菜单名称';


--
-- Name: COLUMN sys_menu.type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.type IS '菜单类型(1:目录 2:菜单 3:按钮/权限 4:链接)';


--
-- Name: COLUMN sys_menu."order"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu."order" IS '显示排序';


--
-- Name: COLUMN sys_menu.permission; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.permission IS '权限标识(如:module_system:user:query)';


--
-- Name: COLUMN sys_menu.icon; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.icon IS '菜单图标';


--
-- Name: COLUMN sys_menu.route_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.route_name IS '路由名称';


--
-- Name: COLUMN sys_menu.route_path; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.route_path IS '路由路径';


--
-- Name: COLUMN sys_menu.component_path; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.component_path IS '组件路径';


--
-- Name: COLUMN sys_menu.redirect; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.redirect IS '重定向地址';


--
-- Name: COLUMN sys_menu.hidden; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.hidden IS '是否隐藏(True:隐藏 False:显示)';


--
-- Name: COLUMN sys_menu.keep_alive; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.keep_alive IS '是否缓存(True:是 False:否)';


--
-- Name: COLUMN sys_menu.always_show; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.always_show IS '是否始终显示(True:是 False:否)';


--
-- Name: COLUMN sys_menu.title; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.title IS '菜单标题';


--
-- Name: COLUMN sys_menu.params; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.params IS '路由参数(JSON对象)';


--
-- Name: COLUMN sys_menu.affix; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.affix IS '是否固定标签页(True:是 False:否)';


--
-- Name: COLUMN sys_menu.parent_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.parent_id IS '父菜单ID';


--
-- Name: COLUMN sys_menu.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.id IS '主键ID';


--
-- Name: COLUMN sys_menu.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_menu.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_menu.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.description IS '备注/描述';


--
-- Name: COLUMN sys_menu.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.created_time IS '创建时间';


--
-- Name: COLUMN sys_menu.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_menu.updated_time IS '更新时间';


--
-- Name: sys_menu_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_menu_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_menu_id_seq OWNER TO tao;

--
-- Name: sys_menu_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_menu_id_seq OWNED BY public.sys_menu.id;


--
-- Name: sys_notice; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_notice (
    notice_title character varying(64) NOT NULL,
    notice_type character varying(1) NOT NULL,
    notice_content text,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.sys_notice OWNER TO tao;

--
-- Name: TABLE sys_notice; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_notice IS '通知公告表';


--
-- Name: COLUMN sys_notice.notice_title; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.notice_title IS '公告标题';


--
-- Name: COLUMN sys_notice.notice_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.notice_type IS '公告类型(1通知 2公告)';


--
-- Name: COLUMN sys_notice.notice_content; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.notice_content IS '公告内容';


--
-- Name: COLUMN sys_notice.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.id IS '主键ID';


--
-- Name: COLUMN sys_notice.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_notice.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_notice.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.description IS '备注/描述';


--
-- Name: COLUMN sys_notice.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.created_time IS '创建时间';


--
-- Name: COLUMN sys_notice.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.updated_time IS '更新时间';


--
-- Name: COLUMN sys_notice.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.created_id IS '创建人ID';


--
-- Name: COLUMN sys_notice.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_notice.updated_id IS '更新人ID';


--
-- Name: sys_notice_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_notice_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_notice_id_seq OWNER TO tao;

--
-- Name: sys_notice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_notice_id_seq OWNED BY public.sys_notice.id;


--
-- Name: sys_param; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_param (
    config_name character varying(64) NOT NULL,
    config_key character varying(500) NOT NULL,
    config_value character varying(500),
    config_type boolean,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL
);


ALTER TABLE public.sys_param OWNER TO tao;

--
-- Name: TABLE sys_param; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_param IS '系统参数表';


--
-- Name: COLUMN sys_param.config_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.config_name IS '参数名称';


--
-- Name: COLUMN sys_param.config_key; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.config_key IS '参数键名';


--
-- Name: COLUMN sys_param.config_value; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.config_value IS '参数键值';


--
-- Name: COLUMN sys_param.config_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.config_type IS '系统内置(True:是 False:否)';


--
-- Name: COLUMN sys_param.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.id IS '主键ID';


--
-- Name: COLUMN sys_param.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_param.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_param.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.description IS '备注/描述';


--
-- Name: COLUMN sys_param.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.created_time IS '创建时间';


--
-- Name: COLUMN sys_param.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_param.updated_time IS '更新时间';


--
-- Name: sys_param_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_param_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_param_id_seq OWNER TO tao;

--
-- Name: sys_param_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_param_id_seq OWNED BY public.sys_param.id;


--
-- Name: sys_position; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_position (
    name character varying(64) NOT NULL,
    "order" integer NOT NULL,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.sys_position OWNER TO tao;

--
-- Name: TABLE sys_position; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_position IS '岗位表';


--
-- Name: COLUMN sys_position.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position.name IS '岗位名称';


--
-- Name: COLUMN sys_position."order"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position."order" IS '显示排序';


--
-- Name: COLUMN sys_position.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position.id IS '主键ID';


--
-- Name: COLUMN sys_position.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_position.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_position.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position.description IS '备注/描述';


--
-- Name: COLUMN sys_position.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position.created_time IS '创建时间';


--
-- Name: COLUMN sys_position.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position.updated_time IS '更新时间';


--
-- Name: COLUMN sys_position.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position.created_id IS '创建人ID';


--
-- Name: COLUMN sys_position.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_position.updated_id IS '更新人ID';


--
-- Name: sys_position_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_position_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_position_id_seq OWNER TO tao;

--
-- Name: sys_position_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_position_id_seq OWNED BY public.sys_position.id;


--
-- Name: sys_role; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_role (
    name character varying(64) NOT NULL,
    code character varying(16),
    "order" integer NOT NULL,
    data_scope integer NOT NULL,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL
);


ALTER TABLE public.sys_role OWNER TO tao;

--
-- Name: TABLE sys_role; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_role IS '角色表';


--
-- Name: COLUMN sys_role.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role.name IS '角色名称';


--
-- Name: COLUMN sys_role.code; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role.code IS '角色编码';


--
-- Name: COLUMN sys_role."order"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role."order" IS '显示排序';


--
-- Name: COLUMN sys_role.data_scope; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role.data_scope IS '数据权限范围(1:仅本人 2:本部门 3:本部门及以下 4:全部 5:自定义)';


--
-- Name: COLUMN sys_role.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role.id IS '主键ID';


--
-- Name: COLUMN sys_role.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_role.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_role.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role.description IS '备注/描述';


--
-- Name: COLUMN sys_role.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role.created_time IS '创建时间';


--
-- Name: COLUMN sys_role.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role.updated_time IS '更新时间';


--
-- Name: sys_role_depts; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_role_depts (
    role_id integer NOT NULL,
    dept_id integer NOT NULL
);


ALTER TABLE public.sys_role_depts OWNER TO tao;

--
-- Name: TABLE sys_role_depts; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_role_depts IS '角色部门关联表';


--
-- Name: COLUMN sys_role_depts.role_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role_depts.role_id IS '角色ID';


--
-- Name: COLUMN sys_role_depts.dept_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role_depts.dept_id IS '部门ID';


--
-- Name: sys_role_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_role_id_seq OWNER TO tao;

--
-- Name: sys_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_role_id_seq OWNED BY public.sys_role.id;


--
-- Name: sys_role_menus; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_role_menus (
    role_id integer NOT NULL,
    menu_id integer NOT NULL
);


ALTER TABLE public.sys_role_menus OWNER TO tao;

--
-- Name: TABLE sys_role_menus; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_role_menus IS '角色菜单关联表';


--
-- Name: COLUMN sys_role_menus.role_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role_menus.role_id IS '角色ID';


--
-- Name: COLUMN sys_role_menus.menu_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_role_menus.menu_id IS '菜单ID';


--
-- Name: sys_user; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_user (
    username character varying(64) NOT NULL,
    password character varying(255) NOT NULL,
    name character varying(32) NOT NULL,
    mobile character varying(11),
    email character varying(64),
    gender character varying(1),
    avatar character varying(255),
    is_superuser boolean NOT NULL,
    last_login timestamp with time zone,
    gitee_login character varying(32),
    github_login character varying(32),
    wx_login character varying(32),
    qq_login character varying(32),
    dept_id integer,
    id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    status character varying(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer
);


ALTER TABLE public.sys_user OWNER TO tao;

--
-- Name: TABLE sys_user; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_user IS '用户表';


--
-- Name: COLUMN sys_user.username; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.username IS '用户名/登录账号';


--
-- Name: COLUMN sys_user.password; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.password IS '密码哈希';


--
-- Name: COLUMN sys_user.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.name IS '昵称';


--
-- Name: COLUMN sys_user.mobile; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.mobile IS '手机号';


--
-- Name: COLUMN sys_user.email; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.email IS '邮箱';


--
-- Name: COLUMN sys_user.gender; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.gender IS '性别(0:男 1:女 2:未知)';


--
-- Name: COLUMN sys_user.avatar; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.avatar IS '头像URL地址';


--
-- Name: COLUMN sys_user.is_superuser; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.is_superuser IS '是否超管';


--
-- Name: COLUMN sys_user.last_login; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.last_login IS '最后登录时间';


--
-- Name: COLUMN sys_user.gitee_login; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.gitee_login IS 'Gitee登录';


--
-- Name: COLUMN sys_user.github_login; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.github_login IS 'Github登录';


--
-- Name: COLUMN sys_user.wx_login; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.wx_login IS '微信登录';


--
-- Name: COLUMN sys_user.qq_login; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.qq_login IS 'QQ登录';


--
-- Name: COLUMN sys_user.dept_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.dept_id IS '部门ID';


--
-- Name: COLUMN sys_user.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.id IS '主键ID';


--
-- Name: COLUMN sys_user.uuid; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.uuid IS 'UUID全局唯一标识';


--
-- Name: COLUMN sys_user.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.status IS '是否启用(0:启用 1:禁用)';


--
-- Name: COLUMN sys_user.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.description IS '备注/描述';


--
-- Name: COLUMN sys_user.created_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.created_time IS '创建时间';


--
-- Name: COLUMN sys_user.updated_time; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.updated_time IS '更新时间';


--
-- Name: COLUMN sys_user.created_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.created_id IS '创建人ID';


--
-- Name: COLUMN sys_user.updated_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user.updated_id IS '更新人ID';


--
-- Name: sys_user_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.sys_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sys_user_id_seq OWNER TO tao;

--
-- Name: sys_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.sys_user_id_seq OWNED BY public.sys_user.id;


--
-- Name: sys_user_positions; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_user_positions (
    user_id integer NOT NULL,
    position_id integer NOT NULL
);


ALTER TABLE public.sys_user_positions OWNER TO tao;

--
-- Name: TABLE sys_user_positions; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_user_positions IS '用户岗位关联表';


--
-- Name: COLUMN sys_user_positions.user_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user_positions.user_id IS '用户ID';


--
-- Name: COLUMN sys_user_positions.position_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user_positions.position_id IS '岗位ID';


--
-- Name: sys_user_roles; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.sys_user_roles (
    user_id integer NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE public.sys_user_roles OWNER TO tao;

--
-- Name: TABLE sys_user_roles; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.sys_user_roles IS '用户角色关联表';


--
-- Name: COLUMN sys_user_roles.user_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user_roles.user_id IS '用户ID';


--
-- Name: COLUMN sys_user_roles.role_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.sys_user_roles.role_id IS '角色ID';


--
-- Name: app_ai_mcp id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_ai_mcp ALTER COLUMN id SET DEFAULT nextval('public.app_ai_mcp_id_seq'::regclass);


--
-- Name: app_job id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_job ALTER COLUMN id SET DEFAULT nextval('public.app_job_id_seq'::regclass);


--
-- Name: app_job_log id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_job_log ALTER COLUMN id SET DEFAULT nextval('public.app_job_log_id_seq'::regclass);


--
-- Name: app_myapp id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_myapp ALTER COLUMN id SET DEFAULT nextval('public.app_myapp_id_seq'::regclass);


--
-- Name: gen_demo id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_demo ALTER COLUMN id SET DEFAULT nextval('public.gen_demo_id_seq'::regclass);


--
-- Name: gen_table id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table ALTER COLUMN id SET DEFAULT nextval('public.gen_table_id_seq'::regclass);


--
-- Name: gen_table_column id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table_column ALTER COLUMN id SET DEFAULT nextval('public.gen_table_column_id_seq'::regclass);


--
-- Name: sys_dept id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dept ALTER COLUMN id SET DEFAULT nextval('public.sys_dept_id_seq'::regclass);


--
-- Name: sys_dict_data id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dict_data ALTER COLUMN id SET DEFAULT nextval('public.sys_dict_data_id_seq'::regclass);


--
-- Name: sys_dict_type id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dict_type ALTER COLUMN id SET DEFAULT nextval('public.sys_dict_type_id_seq'::regclass);


--
-- Name: sys_log id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_log ALTER COLUMN id SET DEFAULT nextval('public.sys_log_id_seq'::regclass);


--
-- Name: sys_menu id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_menu ALTER COLUMN id SET DEFAULT nextval('public.sys_menu_id_seq'::regclass);


--
-- Name: sys_notice id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_notice ALTER COLUMN id SET DEFAULT nextval('public.sys_notice_id_seq'::regclass);


--
-- Name: sys_param id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_param ALTER COLUMN id SET DEFAULT nextval('public.sys_param_id_seq'::regclass);


--
-- Name: sys_position id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_position ALTER COLUMN id SET DEFAULT nextval('public.sys_position_id_seq'::regclass);


--
-- Name: sys_role id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_role ALTER COLUMN id SET DEFAULT nextval('public.sys_role_id_seq'::regclass);


--
-- Name: sys_user id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user ALTER COLUMN id SET DEFAULT nextval('public.sys_user_id_seq'::regclass);


--
-- Data for Name: app_ai_mcp; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.app_ai_mcp (name, type, url, command, args, env, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: app_job; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.app_job (name, jobstore, executor, trigger, trigger_args, func, args, kwargs, "coalesce", max_instances, start_date, end_date, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: app_job_log; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.app_job_log (job_name, job_group, job_executor, invoke_target, job_args, job_kwargs, job_trigger, job_message, exception_info, job_id, id, uuid, status, description, created_time, updated_time) FROM stdin;
\.


--
-- Data for Name: app_myapp; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.app_myapp (name, access_url, icon_url, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: apscheduler_jobs; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.apscheduler_jobs (id, next_run_time, job_state) FROM stdin;
\.


--
-- Data for Name: gen_demo; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.gen_demo (name, a, b, c, d, e, f, g, h, i, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: gen_table; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.gen_table (table_name, table_comment, class_name, package_name, module_name, business_name, function_name, sub_table_name, sub_table_fk_name, parent_menu_id, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: gen_table_column; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.gen_table_column (column_name, column_comment, column_type, column_length, column_default, is_pk, is_increment, is_nullable, is_unique, python_type, python_field, is_insert, is_edit, is_list, is_query, query_type, html_type, dict_type, sort, table_id, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: sys_dept; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_dept (name, "order", code, leader, phone, email, parent_id, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
集团总公司	1	GROUP	部门负责人	1582112620	deptadmin@example.com	\N	1	8d654e65-99ff-4387-a37c-84d62a88a028	0	集团总公司	2026-01-03 21:32:18.926144	2026-01-03 21:32:18.926145	\N	\N
\.


--
-- Data for Name: sys_dict_data; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_dict_data (dict_sort, dict_label, dict_value, css_class, list_class, is_default, dict_type, dict_type_id, id, uuid, status, description, created_time, updated_time) FROM stdin;
1	男	0	blue	\N	t	sys_user_sex	1	1	bd6a2210-c201-41e8-a88e-9d70f21af893	0	性别男	2026-01-03 21:32:18.934083	2026-01-03 21:32:18.934084
2	女	1	pink	\N	f	sys_user_sex	1	2	41a3ebab-d0d4-47b5-9b46-4d090c3328fb	0	性别女	2026-01-03 21:32:18.934087	2026-01-03 21:32:18.934088
3	未知	2	red	\N	f	sys_user_sex	1	3	9b16809d-943e-4bca-ae8e-e9d97a05f3fa	0	性别未知	2026-01-03 21:32:18.934091	2026-01-03 21:32:18.934091
1	是	1		primary	t	sys_yes_no	2	4	cca9a62e-ddeb-4aca-bb45-7de890e39c09	0	是	2026-01-03 21:32:18.934094	2026-01-03 21:32:18.934094
2	否	0		danger	f	sys_yes_no	2	5	c316ecf0-d687-4189-8e06-97c9193d7f7b	0	否	2026-01-03 21:32:18.934097	2026-01-03 21:32:18.934097
1	启用	1		primary	f	sys_common_status	3	6	93b2ed52-6cc0-40a1-af69-c63fb6a45ffc	0	启用状态	2026-01-03 21:32:18.9341	2026-01-03 21:32:18.934101
2	停用	0		danger	f	sys_common_status	3	7	52af9571-5ef4-4139-9884-1e992b84f495	0	停用状态	2026-01-03 21:32:18.934105	2026-01-03 21:32:18.934105
1	通知	1	blue	warning	t	sys_notice_type	4	8	561c4aa2-5c1d-453c-8a40-2174bdde1d7c	0	通知	2026-01-03 21:32:18.934109	2026-01-03 21:32:18.934109
2	公告	2	orange	success	f	sys_notice_type	4	9	1c9747bc-cf5d-4dfd-ba33-b4807c6e58da	0	公告	2026-01-03 21:32:18.934113	2026-01-03 21:32:18.934113
99	其他	0		info	f	sys_oper_type	5	10	409b6db6-191c-418c-9959-7bde1364d07c	0	其他操作	2026-01-03 21:32:18.934117	2026-01-03 21:32:18.934117
1	新增	1		info	f	sys_oper_type	5	11	d9a58448-fe91-4bf4-9e19-b64f66951a2c	0	新增操作	2026-01-03 21:32:18.934121	2026-01-03 21:32:18.934121
2	修改	2		info	f	sys_oper_type	5	12	f587833d-ae30-4280-beea-a531a42fd60f	0	修改操作	2026-01-03 21:32:18.934124	2026-01-03 21:32:18.934124
3	删除	3		danger	f	sys_oper_type	5	13	128f44ac-dbac-4370-96d3-ecca27bde3f5	0	删除操作	2026-01-03 21:32:18.934127	2026-01-03 21:32:18.934127
4	分配权限	4		primary	f	sys_oper_type	5	14	0acbce3f-60ac-4002-8e51-df3e384e8437	0	授权操作	2026-01-03 21:32:18.93413	2026-01-03 21:32:18.934131
5	导出	5		warning	f	sys_oper_type	5	15	783e208b-e6b6-45db-8a42-da13383340dd	0	导出操作	2026-01-03 21:32:18.934133	2026-01-03 21:32:18.934134
6	导入	6		warning	f	sys_oper_type	5	16	30bf7414-46da-454f-96d2-aead5a349e39	0	导入操作	2026-01-03 21:32:18.934137	2026-01-03 21:32:18.934137
7	强退	7		danger	f	sys_oper_type	5	17	4f69e213-23eb-4003-a68f-ae1d19b1c0be	0	强退操作	2026-01-03 21:32:18.93414	2026-01-03 21:32:18.93414
8	生成代码	8		warning	f	sys_oper_type	5	18	45aa655b-a610-43da-a26f-89591d289286	0	生成操作	2026-01-03 21:32:18.934143	2026-01-03 21:32:18.934143
9	清空数据	9		danger	f	sys_oper_type	5	19	d9e62139-5093-4434-a7ae-2f228bb06ee2	0	清空操作	2026-01-03 21:32:18.934146	2026-01-03 21:32:18.934146
1	默认(Memory)	default		\N	t	sys_job_store	6	20	b05a55b9-819e-420c-b195-919642f8cecd	0	默认分组	2026-01-03 21:32:18.934149	2026-01-03 21:32:18.934149
2	数据库(Sqlalchemy)	sqlalchemy		\N	f	sys_job_store	6	21	839b814f-e46f-446d-bbc4-3e383398a4f6	0	数据库分组	2026-01-03 21:32:18.934152	2026-01-03 21:32:18.934152
3	数据库(Redis)	redis		\N	f	sys_job_store	6	22	3e96b9aa-1d44-4d8d-a0d8-8a8e122992c3	0	reids分组	2026-01-03 21:32:18.934155	2026-01-03 21:32:18.934155
1	线程池	default		\N	f	sys_job_executor	7	23	6ba38fd3-a029-4062-9020-7a641b58b931	0	线程池	2026-01-03 21:32:18.934158	2026-01-03 21:32:18.934158
2	进程池	processpool		\N	f	sys_job_executor	7	24	3268717a-2355-4a6d-8d41-37520c6fd3bc	0	进程池	2026-01-03 21:32:18.934161	2026-01-03 21:32:18.934161
1	演示函数	scheduler_test.job		\N	t	sys_job_function	8	25	e23a88c8-9893-4b5e-b7c6-5ca0f4503166	0	演示函数	2026-01-03 21:32:18.934164	2026-01-03 21:32:18.934165
1	指定日期(date)	date		\N	t	sys_job_trigger	9	26	9eae1ac4-ecba-45f6-a647-be55d28ee6fe	0	指定日期任务触发器	2026-01-03 21:32:18.934168	2026-01-03 21:32:18.934169
2	间隔触发器(interval)	interval		\N	f	sys_job_trigger	9	27	5cdefb4c-37f1-449a-8943-817e43584928	0	间隔触发器任务触发器	2026-01-03 21:32:18.934171	2026-01-03 21:32:18.934172
3	cron表达式	cron		\N	f	sys_job_trigger	9	28	9ef32420-9fad-4afd-8551-c65f96452906	0	间隔触发器任务触发器	2026-01-03 21:32:18.934175	2026-01-03 21:32:18.934175
1	默认(default)	default		\N	t	sys_list_class	10	29	9b5beaef-1c70-4efe-a5cc-0ad4bb690ab7	0	默认表格回显样式	2026-01-03 21:32:18.934178	2026-01-03 21:32:18.934178
2	主要(primary)	primary		\N	f	sys_list_class	10	30	bf59ec99-cb51-4223-b6d0-3f05158110d8	0	主要表格回显样式	2026-01-03 21:32:18.934181	2026-01-03 21:32:18.934181
3	成功(success)	success		\N	f	sys_list_class	10	31	63104263-1c40-4a42-be52-038296e66a7a	0	成功表格回显样式	2026-01-03 21:32:18.934184	2026-01-03 21:32:18.934184
4	信息(info)	info		\N	f	sys_list_class	10	32	cdfb253e-293d-45c7-845d-6ec9b33a165d	0	信息表格回显样式	2026-01-03 21:32:18.934187	2026-01-03 21:32:18.934187
5	警告(warning)	warning		\N	f	sys_list_class	10	33	fc9a9e08-bba1-41ce-9284-0237bcd07835	0	警告表格回显样式	2026-01-03 21:32:18.93419	2026-01-03 21:32:18.93419
6	危险(danger)	danger		\N	f	sys_list_class	10	34	d9410025-6b47-4cc8-b162-738d7ccedd93	0	危险表格回显样式	2026-01-03 21:32:18.934193	2026-01-03 21:32:18.934193
\.


--
-- Data for Name: sys_dict_type; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_dict_type (dict_name, dict_type, id, uuid, status, description, created_time, updated_time) FROM stdin;
用户性别	sys_user_sex	1	cee3722a-32e8-4ae0-a5a4-bcd6721656a6	0	用户性别列表	2026-01-03 21:32:18.930619	2026-01-03 21:32:18.93062
系统是否	sys_yes_no	2	f6f1923a-8662-434d-9494-6a9bdeae03da	0	系统是否列表	2026-01-03 21:32:18.930624	2026-01-03 21:32:18.930625
系统状态	sys_common_status	3	21ad6e7f-69b9-451e-b03e-8e24c04bdd0b	0	系统状态	2026-01-03 21:32:18.930628	2026-01-03 21:32:18.930628
通知类型	sys_notice_type	4	33c7a8d3-c61a-4607-971d-ae2b2e984068	0	通知类型列表	2026-01-03 21:32:18.930631	2026-01-03 21:32:18.930631
操作类型	sys_oper_type	5	a690ee39-010c-421e-b884-6e7b5b309263	0	操作类型列表	2026-01-03 21:32:18.930634	2026-01-03 21:32:18.930634
任务存储器	sys_job_store	6	1308fc02-bedd-4c86-876b-bcaa27c25256	0	任务分组列表	2026-01-03 21:32:18.930637	2026-01-03 21:32:18.930637
任务执行器	sys_job_executor	7	963bd467-271b-4def-984c-a6c5c3b1e6c2	0	任务执行器列表	2026-01-03 21:32:18.93064	2026-01-03 21:32:18.930641
任务函数	sys_job_function	8	77c1b8d9-4938-4959-b927-14f8df85a536	0	任务函数列表	2026-01-03 21:32:18.930644	2026-01-03 21:32:18.930644
任务触发器	sys_job_trigger	9	63d803cc-bab8-466e-bd18-4297f15ebe68	0	任务触发器列表	2026-01-03 21:32:18.930647	2026-01-03 21:32:18.930647
表格回显样式	sys_list_class	10	4604846e-a556-4d3a-9c2f-c72cfb29fdf0	0	表格回显样式列表	2026-01-03 21:32:18.93065	2026-01-03 21:32:18.93065
\.


--
-- Data for Name: sys_log; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_log (type, request_path, request_method, request_payload, request_ip, login_location, request_os, request_browser, response_code, response_json, process_time, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: sys_menu; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_menu (name, type, "order", permission, icon, route_name, route_path, component_path, redirect, hidden, keep_alive, always_show, title, params, affix, parent_id, id, uuid, status, description, created_time, updated_time) FROM stdin;
仪表盘	1	1		client	Dashboard	/dashboard	\N	/dashboard/workplace	f	t	t	仪表盘	null	f	\N	1	cb8697f1-d99f-486f-a35d-ca588d00ecee	0	初始化数据	2026-01-03 21:32:18.905383	2026-01-03 21:32:18.905387
系统管理	1	2	\N	system	System	/system	\N	/system/menu	f	t	f	系统管理	null	f	\N	2	8686a005-e6f2-4f27-a592-dd1e33c1c5e7	0	初始化数据	2026-01-03 21:32:18.905392	2026-01-03 21:32:18.905392
应用管理	1	3	\N	el-icon-ShoppingBag	Application	/application	\N	/application/myapp	f	t	f	应用管理	null	f	\N	3	aed230c6-6a2f-47a2-ae17-19a36111987f	0	初始化数据	2026-01-03 21:32:18.905395	2026-01-03 21:32:18.905395
监控管理	1	4	\N	monitor	Monitor	/monitor	\N	/monitor/online	f	t	f	监控管理	null	f	\N	4	f94f6492-288a-4df3-b6a2-37eaec7f7b6f	0	初始化数据	2026-01-03 21:32:18.905398	2026-01-03 21:32:18.905399
代码管理	1	5	\N	code	Generator	/generator	\N	/generator/gencode	f	t	f	代码管理	null	f	\N	5	9a68972f-7c40-4104-97b1-372213d500c1	0	代码管理	2026-01-03 21:32:18.905401	2026-01-03 21:32:18.905402
接口管理	1	6	\N	document	Common	/common	\N	/common/docs	f	t	f	接口管理	null	f	\N	6	75341f65-6da9-4bd6-a9c1-eab807edd5fb	0	初始化数据	2026-01-03 21:32:18.905405	2026-01-03 21:32:18.905405
案例管理	1	7	\N	menu	Example	/example	\N	/example/demo	f	t	f	案例管理	null	f	\N	7	5145f454-4bd1-48c9-a780-c809cfcf669e	0	案例管理	2026-01-03 21:32:18.905408	2026-01-03 21:32:18.905408
工作台	2	1	dashboard:workplace:query	el-icon-PieChart	Workplace	/dashboard/workplace	dashboard/workplace	\N	f	t	f	工作台	null	f	1	8	15605dd7-2ab4-4ad4-b2e6-3a32976d4c1a	0	初始化数据	2026-01-03 21:32:18.907989	2026-01-03 21:32:18.907991
菜单管理	2	1	module_system:menu:query	menu	Menu	/system/menu	module_system/menu/index	\N	f	t	f	菜单管理	null	f	2	9	7ba1cbc7-4822-472a-a239-647ef5807fb8	0	初始化数据	2026-01-03 21:32:18.907995	2026-01-03 21:32:18.907996
部门管理	2	2	module_system:dept:query	tree	Dept	/system/dept	module_system/dept/index	\N	f	t	f	部门管理	null	f	2	10	4d852241-ce79-45b2-aac2-cb683b4fe502	0	初始化数据	2026-01-03 21:32:18.907999	2026-01-03 21:32:18.907999
岗位管理	2	3	module_system:position:query	el-icon-Coordinate	Position	/system/position	module_system/position/index	\N	f	t	f	岗位管理	null	f	2	11	0515619f-cc9c-4a94-a11b-4c56c14a7ad7	0	初始化数据	2026-01-03 21:32:18.908002	2026-01-03 21:32:18.908003
角色管理	2	4	module_system:role:query	role	Role	/system/role	module_system/role/index	\N	f	t	f	角色管理	null	f	2	12	680024f6-08da-4141-a993-452a0bbbc008	0	初始化数据	2026-01-03 21:32:18.908005	2026-01-03 21:32:18.908006
用户管理	2	5	module_system:user:query	el-icon-User	User	/system/user	module_system/user/index	\N	f	t	f	用户管理	null	f	2	13	9900d01f-556f-4580-a09a-aecd51a99c86	0	初始化数据	2026-01-03 21:32:18.908009	2026-01-03 21:32:18.908009
日志管理	2	6	module_system:log:query	el-icon-Aim	Log	/system/log	module_system/log/index	\N	f	t	f	日志管理	null	f	2	14	4cf02289-e5d6-4fd4-8a35-2415dec384fa	0	初始化数据	2026-01-03 21:32:18.908012	2026-01-03 21:32:18.908012
公告管理	2	7	module_system:notice:query	bell	Notice	/system/notice	module_system/notice/index	\N	f	t	f	公告管理	null	f	2	15	c4cac9c7-d750-4b27-9731-039149f2897d	0	初始化数据	2026-01-03 21:32:18.908015	2026-01-03 21:32:18.908015
参数管理	2	8	module_system:param:query	setting	Params	/system/param	module_system/param/index	\N	f	t	f	参数管理	null	f	2	16	2385358e-b01c-4a48-93e0-d3b85f18438b	0	初始化数据	2026-01-03 21:32:18.908018	2026-01-03 21:32:18.908018
字典管理	2	9	module_system:dict_type:query	dict	Dict	/system/dict	module_system/dict/index	\N	f	t	f	字典管理	null	f	2	17	b9da7600-bbc3-48b9-86bd-c87d99e782e8	0	初始化数据	2026-01-03 21:32:18.908021	2026-01-03 21:32:18.908021
我的应用	2	1	module_application:myapp:query	el-icon-ShoppingCartFull	MYAPP	/application/myapp	module_application/myapp/index	\N	f	t	f	我的应用	null	f	3	18	4b89ed0b-c1c2-4a08-95a9-c0aff320fbbf	0	初始化数据	2026-01-03 21:32:18.908024	2026-01-03 21:32:18.908024
任务管理	2	2	module_application:job:query	el-icon-DataLine	Job	/application/job	module_application/job/index	\N	f	t	f	任务管理	null	f	3	19	586828bb-10f6-4eff-82b9-1ac747bafef2	0	初始化数据	2026-01-03 21:32:18.908027	2026-01-03 21:32:18.908027
AI智能助手	2	3	module_application:ai:chat	el-icon-ToiletPaper	AI	/application/ai	module_application/ai/index	\N	f	t	f	AI智能助手	null	f	3	20	be03f057-ed7d-4c9e-9cb3-a17eabc58920	0	AI智能助手	2026-01-03 21:32:18.90803	2026-01-03 21:32:18.90803
流程管理	2	4	module_application:workflow:query	el-icon-ShoppingBag	Workflow	/application/workflow	module_application/workflow/index	\N	f	t	f	我的流程	null	f	3	21	b3e1ec0a-4411-4909-9b91-b11fa7cb56ae	0	我的流程	2026-01-03 21:32:18.908033	2026-01-03 21:32:18.908034
在线用户	2	1	module_monitor:online:query	el-icon-Headset	MonitorOnline	/monitor/online	module_monitor/online/index	\N	f	t	f	在线用户	null	f	4	22	bd3696da-f6cd-4d37-b2d3-458c0653c86b	0	初始化数据	2026-01-03 21:32:18.908036	2026-01-03 21:32:18.908037
服务器监控	2	2	module_monitor:server:query	el-icon-Odometer	MonitorServer	/monitor/server	module_monitor/server/index	\N	f	t	f	服务器监控	null	f	4	23	da8f2dd6-a3c8-4d0e-b4b8-995baafa47a4	0	初始化数据	2026-01-03 21:32:18.908039	2026-01-03 21:32:18.90804
缓存监控	2	3	module_monitor:cache:query	el-icon-Stopwatch	MonitorCache	/monitor/cache	module_monitor/cache/index	\N	f	t	f	缓存监控	null	f	4	24	4a738c1e-2d6a-4c43-abf7-0ead777544df	0	初始化数据	2026-01-03 21:32:18.908042	2026-01-03 21:32:18.908043
文件管理	2	4	module_monitor:resource:query	el-icon-Files	Resource	/monitor/resource	module_monitor/resource/index	\N	f	t	f	文件管理	null	f	4	25	b57d3b59-82a1-4430-8b8a-7545c296f86a	0	初始化数据	2026-01-03 21:32:18.908045	2026-01-03 21:32:18.908046
代码生成	2	1	module_generator:gencode:query	code	GenCode	/generator/gencode	module_generator/gencode/index	\N	f	t	f	代码生成	null	f	5	26	d7bba83a-d934-4692-976c-56a43e69665a	0	代码生成	2026-01-03 21:32:18.908048	2026-01-03 21:32:18.908049
Swagger文档	4	1	module_common:docs:query	api	Docs	/common/docs	module_common/docs/index	\N	f	t	f	Swagger文档	null	f	6	27	f8d27069-6348-474d-9338-f063cdeab56e	0	初始化数据	2026-01-03 21:32:18.908052	2026-01-03 21:32:18.908052
Redoc文档	4	2	module_common:redoc:query	el-icon-Document	Redoc	/common/redoc	module_common/redoc/index	\N	f	t	f	Redoc文档	null	f	6	28	572fd0dc-26c6-480a-a142-223da6de2697	0	初始化数据	2026-01-03 21:32:18.908054	2026-01-03 21:32:18.908055
示例管理	2	1	module_example:demo:query	menu	Demo	/example/demo	module_example/demo/index	\N	f	t	f	示例管理	null	f	7	29	8bdeda95-8219-48ef-abe4-cba88a251e88	0	示例管理	2026-01-03 21:32:18.908057	2026-01-03 21:32:18.908058
创建菜单	3	1	module_system:menu:create	\N	\N	\N	\N	\N	f	t	f	创建菜单	null	f	9	30	d7e7d1da-e452-422f-a05b-3220b5534abc	0	初始化数据	2026-01-03 21:32:18.911445	2026-01-03 21:32:18.911447
修改菜单	3	2	module_system:menu:update	\N	\N	\N	\N	\N	f	t	f	修改菜单	null	f	9	31	82b62e27-b2d0-44b1-9319-9f8b2160be2a	0	初始化数据	2026-01-03 21:32:18.91145	2026-01-03 21:32:18.91145
删除菜单	3	3	module_system:menu:delete	\N	\N	\N	\N	\N	f	t	f	删除菜单	null	f	9	32	d796f75f-ea78-41fa-a6f6-d8b3cc9698db	0	初始化数据	2026-01-03 21:32:18.911453	2026-01-03 21:32:18.911453
批量修改菜单状态	3	4	module_system:menu:patch	\N	\N	\N	\N	\N	f	t	f	批量修改菜单状态	null	f	9	33	5e130db5-b6f1-40ae-bba6-f8f08bc433be	0	初始化数据	2026-01-03 21:32:18.911456	2026-01-03 21:32:18.911456
详情改菜	3	5	module_system:menu:detail	\N	\N	\N	\N	\N	f	t	f	详情改菜	null	f	9	34	5f31aeb8-beda-46fc-8715-5bc807787c38	0	初始化数据	2026-01-03 21:32:18.911459	2026-01-03 21:32:18.911459
查询菜单	3	6	module_system:menu:query	\N	\N	\N	\N	\N	f	t	f	查询菜单	null	f	9	35	a0f600b3-b948-4197-a162-b0f0019e0029	0	初始化数据	2026-01-03 21:32:18.911462	2026-01-03 21:32:18.911462
创建部门	3	1	module_system:dept:create	\N	\N	\N	\N	\N	f	t	f	创建部门	null	f	10	36	d699fba9-3c38-4f6d-aaad-e0fe1c6e4ef9	0	初始化数据	2026-01-03 21:32:18.911465	2026-01-03 21:32:18.911465
修改部门	3	2	module_system:dept:update	\N	\N	\N	\N	\N	f	t	f	修改部门	null	f	10	37	7fbc26de-231f-47e5-a776-549bc1d6e8da	0	初始化数据	2026-01-03 21:32:18.911468	2026-01-03 21:32:18.911468
删除部门	3	3	module_system:dept:delete	\N	\N	\N	\N	\N	f	t	f	删除部门	null	f	10	38	e2adf21d-20b9-4a66-b3e9-22dd97067f47	0	初始化数据	2026-01-03 21:32:18.911471	2026-01-03 21:32:18.911471
批量修改部门状态	3	4	module_system:dept:patch	\N	\N	\N	\N	\N	f	t	f	批量修改部门状态	null	f	10	39	174fc5cc-f3d0-48e5-a2f2-4d5d3768601f	0	初始化数据	2026-01-03 21:32:18.911474	2026-01-03 21:32:18.911474
详情部门	3	5	module_system:dept:detail	\N	\N	\N	\N	\N	f	t	f	详情部门	null	f	10	40	0cd163e8-e13d-4e54-af81-4d3b51fb8421	0	初始化数据	2026-01-03 21:32:18.911477	2026-01-03 21:32:18.911477
查询部门	3	6	module_system:dept:query	\N	\N	\N	\N	\N	f	t	f	查询部门	null	f	10	41	39776689-4fb6-47a6-acbc-cd0f63a88113	0	初始化数据	2026-01-03 21:32:18.91148	2026-01-03 21:32:18.91148
创建岗位	3	1	module_system:position:create	\N	\N	\N	\N	\N	f	t	f	创建岗位	null	f	11	42	6087b1ed-b52a-4a71-bbfe-74cd6d16752d	0	初始化数据	2026-01-03 21:32:18.911483	2026-01-03 21:32:18.911483
修改岗位	3	2	module_system:position:update	\N	\N	\N	\N	\N	f	t	f	修改岗位	null	f	11	43	c81de02c-8781-47b3-804d-e8b572f2b1d1	0	初始化数据	2026-01-03 21:32:18.911485	2026-01-03 21:32:18.911486
删除岗位	3	3	module_system:position:delete	\N	\N	\N	\N	\N	f	t	f	修改岗位	null	f	11	44	9ada8ac9-50c3-4251-88a6-1cea182b6e23	0	初始化数据	2026-01-03 21:32:18.911488	2026-01-03 21:32:18.911489
批量修改岗位状态	3	4	module_system:position:patch	\N	\N	\N	\N	\N	f	t	f	批量修改岗位状态	null	f	11	45	bfcd71e3-b90e-4dfd-bb99-1e58ec411745	0	初始化数据	2026-01-03 21:32:18.911491	2026-01-03 21:32:18.911491
岗位导出	3	5	module_system:position:export	\N	\N	\N	\N	\N	f	t	f	岗位导出	null	f	11	46	e4f86a4d-b64c-484c-833f-5fcf7f55273c	0	初始化数据	2026-01-03 21:32:18.911494	2026-01-03 21:32:18.911494
详情岗位	3	6	module_system:position:detail	\N	\N	\N	\N	\N	f	t	f	详情岗位	null	f	11	47	5cbfc463-d1b2-4268-af93-2bd80012a80c	0	初始化数据	2026-01-03 21:32:18.911497	2026-01-03 21:32:18.911497
查询岗位	3	7	module_system:position:query	\N	\N	\N	\N	\N	f	t	f	查询岗位	null	f	11	48	20aaaf6d-f02e-422e-8800-48e1c0ae9dd7	0	初始化数据	2026-01-03 21:32:18.911499	2026-01-03 21:32:18.9115
创建角色	3	1	module_system:role:create	\N	\N	\N	\N	\N	f	t	f	创建角色	null	f	12	49	f7f2a522-4d2f-4ae2-b081-fc455b5fd869	0	初始化数据	2026-01-03 21:32:18.911502	2026-01-03 21:32:18.911503
修改角色	3	2	module_system:role:update	\N	\N	\N	\N	\N	f	t	f	修改角色	null	f	12	50	0c7738be-cf93-42cd-a77b-473262ba35b8	0	初始化数据	2026-01-03 21:32:18.911505	2026-01-03 21:32:18.911506
删除角色	3	3	module_system:role:delete	\N	\N	\N	\N	\N	f	t	f	删除角色	null	f	12	51	d74eb083-c965-4002-9cab-d28c944941e8	0	初始化数据	2026-01-03 21:32:18.911508	2026-01-03 21:32:18.911509
批量修改角色状态	3	4	module_system:role:patch	\N	\N	\N	\N	\N	f	t	f	批量修改角色状态	null	f	12	52	8f3181f4-3797-4c8d-9727-73b65e83dc13	0	初始化数据	2026-01-03 21:32:18.911511	2026-01-03 21:32:18.911512
角色导出	3	5	module_system:role:export	\N	\N	\N	\N	\N	f	t	f	角色导出	null	f	12	53	0409184f-4e47-4e5b-ab46-06977ac912ee	0	初始化数据	2026-01-03 21:32:18.911514	2026-01-03 21:32:18.911515
详情角色	3	6	module_system:role:detail	\N	\N	\N	\N	\N	f	t	f	详情角色	null	f	12	54	1a1a37ae-f6f6-471d-a296-382edebfedb8	0	初始化数据	2026-01-03 21:32:18.911517	2026-01-03 21:32:18.911518
查询角色	3	7	module_system:role:query	\N	\N	\N	\N	\N	f	t	f	查询角色	null	f	12	55	81bd5583-a5e7-403e-9388-fd7b5be62d50	0	初始化数据	2026-01-03 21:32:18.91152	2026-01-03 21:32:18.91152
创建用户	3	1	module_system:user:create	\N	\N	\N	\N	\N	f	t	f	创建用户	null	f	13	56	1b409e37-c8e1-4b32-9842-96d4d5870769	0	初始化数据	2026-01-03 21:32:18.911523	2026-01-03 21:32:18.911523
修改用户	3	2	module_system:user:update	\N	\N	\N	\N	\N	f	t	f	修改用户	null	f	13	57	89d8146a-0a01-42f0-8249-538c65fcb20a	0	初始化数据	2026-01-03 21:32:18.911526	2026-01-03 21:32:18.911526
删除用户	3	3	module_system:user:delete	\N	\N	\N	\N	\N	f	t	f	删除用户	null	f	13	58	58fee4f1-cf15-4b41-ac10-d07246b4ee59	0	初始化数据	2026-01-03 21:32:18.911529	2026-01-03 21:32:18.911529
批量修改用户状态	3	4	module_system:user:patch	\N	\N	\N	\N	\N	f	t	f	批量修改用户状态	null	f	13	59	c7df3326-7d54-4a34-85f6-0ba84c2f00bf	0	初始化数据	2026-01-03 21:32:18.911532	2026-01-03 21:32:18.911532
导出用户	3	5	module_system:user:export	\N	\N	\N	\N	\N	f	t	f	导出用户	null	f	13	60	e7a89f3c-7add-4580-a6f6-fd4c27893973	0	初始化数据	2026-01-03 21:32:18.911534	2026-01-03 21:32:18.911535
导入用户	3	6	module_system:user:import	\N	\N	\N	\N	\N	f	t	f	导入用户	null	f	13	61	79e9601e-1ded-4883-8ef4-f0602d5c1767	0	初始化数据	2026-01-03 21:32:18.911537	2026-01-03 21:32:18.911538
下载用户导入模板	3	7	module_system:user:download	\N	\N	\N	\N	\N	f	t	f	下载用户导入模板	null	f	13	62	9af6e9b9-71ce-4dfc-8df3-a97a6556d115	0	初始化数据	2026-01-03 21:32:18.91154	2026-01-03 21:32:18.91154
详情用户	3	8	module_system:user:detail	\N	\N	\N	\N	\N	f	t	f	详情用户	null	f	13	63	5ae4fded-90d9-4d28-b93b-1d78a71a3ad6	0	初始化数据	2026-01-03 21:32:18.911543	2026-01-03 21:32:18.911543
查询用户	3	9	module_system:user:query	\N	\N	\N	\N	\N	f	t	f	查询用户	null	f	13	64	a26b1bd7-d863-4c6c-80f5-da4e6fa9d34b	0	初始化数据	2026-01-03 21:32:18.911546	2026-01-03 21:32:18.911546
日志删除	3	1	module_system:log:delete	\N	\N	\N	\N	\N	f	t	f	日志删除	null	f	14	65	7ed74443-10e7-40e9-b7d2-99b814597417	0	初始化数据	2026-01-03 21:32:18.911548	2026-01-03 21:32:18.911549
日志导出	3	2	module_system:log:export	\N	\N	\N	\N	\N	f	t	f	日志导出	null	f	14	66	cab97ed3-a0fe-4a37-8a86-9d394e7de088	0	初始化数据	2026-01-03 21:32:18.911551	2026-01-03 21:32:18.911551
日志详情	3	3	module_system:log:detail	\N	\N	\N	\N	\N	f	t	f	日志详情	null	f	14	67	d4964258-ec78-4e05-98f1-0174bb914cc4	0	初始化数据	2026-01-03 21:32:18.911554	2026-01-03 21:32:18.911554
查询日志	3	4	module_system:log:query	\N	\N	\N	\N	\N	f	t	f	查询日志	null	f	14	68	b4e13038-5e5e-4a1b-8b32-b0132b5271c5	0	初始化数据	2026-01-03 21:32:18.911557	2026-01-03 21:32:18.911557
公告创建	3	1	module_system:notice:create	\N	\N	\N	\N	\N	f	t	f	公告创建	null	f	15	69	dd2c2504-743e-48e3-a758-f9aa2bcdcd83	0	初始化数据	2026-01-03 21:32:18.911559	2026-01-03 21:32:18.91156
公告修改	3	2	module_system:notice:update	\N	\N	\N	\N	\N	f	t	f	修改用户	null	f	15	70	3daceab3-ec00-4fc8-bd3a-dac224b727e0	0	初始化数据	2026-01-03 21:32:18.911562	2026-01-03 21:32:18.911564
公告删除	3	3	module_system:notice:delete	\N	\N	\N	\N	\N	f	t	f	公告删除	null	f	15	71	4966506d-bc03-4df9-b0e5-9a1a78946357	0	初始化数据	2026-01-03 21:32:18.911567	2026-01-03 21:32:18.911567
公告导出	3	4	module_system:notice:export	\N	\N	\N	\N	\N	f	t	f	公告导出	null	f	15	72	fc4a35a3-8795-4d58-859d-31be25af894f	0	初始化数据	2026-01-03 21:32:18.911571	2026-01-03 21:32:18.911571
公告批量修改状态	3	5	module_system:notice:patch	\N	\N	\N	\N	\N	f	t	f	公告批量修改状态	null	f	15	73	f41bfd30-e52c-4ac8-a008-27f5d4fde5de	0	初始化数据	2026-01-03 21:32:18.911575	2026-01-03 21:32:18.911575
公告详情	3	6	module_system:notice:detail	\N	\N	\N	\N	\N	f	t	f	公告详情	null	f	15	74	8a129bcf-53fb-4c73-872b-8e281d09bb1d	0	初始化数据	2026-01-03 21:32:18.911579	2026-01-03 21:32:18.911579
查询公告	3	5	module_system:notice:query	\N	\N	\N	\N	\N	f	t	f	查询公告	null	f	15	75	3f24b0f2-5d84-4e98-9097-d90f6276678c	0	初始化数据	2026-01-03 21:32:18.911582	2026-01-03 21:32:18.911583
创建参数	3	1	module_system:param:create	\N	\N	\N	\N	\N	f	t	f	创建参数	null	f	16	76	8513bd00-0f00-4cd6-a76a-1e83e194a4e4	0	初始化数据	2026-01-03 21:32:18.911586	2026-01-03 21:32:18.911587
修改参数	3	2	module_system:param:update	\N	\N	\N	\N	\N	f	t	f	修改参数	null	f	16	77	36a7d50e-34a1-462b-b388-b9d6d8539ad2	0	初始化数据	2026-01-03 21:32:18.91159	2026-01-03 21:32:18.911591
删除参数	3	3	module_system:param:delete	\N	\N	\N	\N	\N	f	t	f	删除参数	null	f	16	78	505028b6-0362-4792-9b86-4edd40f81ffd	0	初始化数据	2026-01-03 21:32:18.911594	2026-01-03 21:32:18.911594
导出参数	3	4	module_system:param:export	\N	\N	\N	\N	\N	f	t	f	导出参数	null	f	16	79	2c5d2b14-366f-4632-930b-0396b6ac4bd3	0	初始化数据	2026-01-03 21:32:18.911598	2026-01-03 21:32:18.911598
参数上传	3	5	module_system:param:upload	\N	\N	\N	\N	\N	f	t	f	参数上传	null	f	16	80	60aee432-dd9b-448c-b527-18b49c7d137a	0	初始化数据	2026-01-03 21:32:18.911602	2026-01-03 21:32:18.911602
参数详情	3	6	module_system:param:detail	\N	\N	\N	\N	\N	f	t	f	参数详情	null	f	16	81	c87eb5ed-62a1-4cd4-8851-0e00cb69b2cc	0	初始化数据	2026-01-03 21:32:18.911605	2026-01-03 21:32:18.911605
查询参数	3	7	module_system:param:query	\N	\N	\N	\N	\N	f	t	f	查询参数	null	f	16	82	d44dccb9-3b72-4e56-bff4-842ccab4cf6a	0	初始化数据	2026-01-03 21:32:18.911608	2026-01-03 21:32:18.911608
创建字典类型	3	1	module_system:dict_type:create	\N	\N	\N	\N	\N	f	t	f	创建字典类型	null	f	17	83	9550ae0d-72c5-4594-b478-a5fae5b27fc9	0	初始化数据	2026-01-03 21:32:18.911611	2026-01-03 21:32:18.911611
修改字典类型	3	2	module_system:dict_type:update	\N	\N	\N	\N	\N	f	t	f	修改字典类型	null	f	17	84	6c9762a7-0846-40df-82ba-4472ca2b5881	0	初始化数据	2026-01-03 21:32:18.911614	2026-01-03 21:32:18.911614
删除字典类型	3	3	module_system:dict_type:delete	\N	\N	\N	\N	\N	f	t	f	删除字典类型	null	f	17	85	7f8d933f-dee6-4dde-b72f-707a7f1b7e49	0	初始化数据	2026-01-03 21:32:18.911617	2026-01-03 21:32:18.911617
导出字典类型	3	4	module_system:dict_type:export	\N	\N	\N	\N	\N	f	t	f	导出字典类型	null	f	17	86	5d14d903-230c-413a-8bba-b70e6b91d33c	0	初始化数据	2026-01-03 21:32:18.911619	2026-01-03 21:32:18.91162
批量修改字典状态	3	5	module_system:dict_type:patch	\N	\N	\N	\N	\N	f	t	f	导出字典类型	null	f	17	87	d1712e01-35ac-443b-aece-06c62c0ab088	0	初始化数据	2026-01-03 21:32:18.911622	2026-01-03 21:32:18.911623
字典数据查询	3	6	module_system:dict_data:query	\N	\N	\N	\N	\N	f	t	f	字典数据查询	null	f	17	88	1565475c-f3a9-4bbb-b93b-5e220467cc81	0	初始化数据	2026-01-03 21:32:18.911625	2026-01-03 21:32:18.911625
创建字典数据	3	7	module_system:dict_data:create	\N	\N	\N	\N	\N	f	t	f	创建字典数据	null	f	17	89	578edd73-25f7-43bb-9f8b-1502e6a028d3	0	初始化数据	2026-01-03 21:32:18.911628	2026-01-03 21:32:18.911628
修改字典数据	3	8	module_system:dict_data:update	\N	\N	\N	\N	\N	f	t	f	修改字典数据	null	f	17	90	71a3bab7-d934-484c-aa9a-e7a7266cddc5	0	初始化数据	2026-01-03 21:32:18.911631	2026-01-03 21:32:18.911631
删除字典数据	3	9	module_system:dict_data:delete	\N	\N	\N	\N	\N	f	t	f	删除字典数据	null	f	17	91	e336aadd-a4fa-41f7-8649-7269ec57f691	0	初始化数据	2026-01-03 21:32:18.911634	2026-01-03 21:32:18.911634
导出字典数据	3	10	module_system:dict_data:export	\N	\N	\N	\N	\N	f	t	f	导出字典数据	null	f	17	92	3595a298-ff90-400a-bbb7-b22b5991b53d	0	初始化数据	2026-01-03 21:32:18.911636	2026-01-03 21:32:18.911637
批量修改字典数据状态	3	11	module_system:dict_data:patch	\N	\N	\N	\N	\N	f	t	f	批量修改字典数据状态	null	f	17	93	f19ece16-4c9e-4e36-9d40-e95119439dba	0	初始化数据	2026-01-03 21:32:18.911639	2026-01-03 21:32:18.911639
详情字典类型	3	12	module_system:dict_type:detail	\N	\N	\N	\N	\N	f	t	f	详情字典类型	null	f	17	94	8c8a3c93-4b81-4f2a-9f19-69d55289bed0	0	初始化数据	2026-01-03 21:32:18.911642	2026-01-03 21:32:18.911642
查询字典类型	3	13	module_system:dict_type:query	\N	\N	\N	\N	\N	f	t	f	查询字典类型	null	f	17	95	3c086e98-80be-43a9-bf92-9e549ce52001	0	初始化数据	2026-01-03 21:32:18.911645	2026-01-03 21:32:18.911645
详情字典数据	3	14	module_system:dict_data:detail	\N	\N	\N	\N	\N	f	t	f	详情字典数据	null	f	17	96	7747b9b0-4876-4379-838c-71746abf40d3	0	初始化数据	2026-01-03 21:32:18.911647	2026-01-03 21:32:18.911648
创建应用	3	1	module_application:myapp:create	\N	\N	\N	\N	\N	f	t	f	创建应用	null	f	18	97	6597310c-0997-4adf-ab77-a3abf3c06fdb	0	初始化数据	2026-01-03 21:32:18.91165	2026-01-03 21:32:18.91165
修改应用	3	2	module_application:myapp:update	\N	\N	\N	\N	\N	f	t	f	修改应用	null	f	18	98	bf921c89-86aa-429c-b00d-92b9b4267451	0	初始化数据	2026-01-03 21:32:18.911653	2026-01-03 21:32:18.911653
删除应用	3	3	module_application:myapp:delete	\N	\N	\N	\N	\N	f	t	f	删除应用	null	f	18	99	dcd2b033-e1ff-4361-abb9-499358d7533b	0	初始化数据	2026-01-03 21:32:18.911656	2026-01-03 21:32:18.911656
批量修改应用状态	3	4	module_application:myapp:patch	\N	\N	\N	\N	\N	f	t	f	批量修改应用状态	null	f	18	100	abde1610-99f2-4366-9cbf-dbc0991a9aa3	0	初始化数据	2026-01-03 21:32:18.911658	2026-01-03 21:32:18.911659
详情应用	3	5	module_application:myapp:detail	\N	\N	\N	\N	\N	f	t	f	详情应用	null	f	18	101	e4ec94d0-7514-4423-80aa-c3e6f6a9e840	0	初始化数据	2026-01-03 21:32:18.911661	2026-01-03 21:32:18.911662
查询应用	3	6	module_application:myapp:query	\N	\N	\N	\N	\N	f	t	f	查询应用	null	f	18	102	3f4ad15e-a846-43ba-81b7-c07998fae40e	0	初始化数据	2026-01-03 21:32:18.911664	2026-01-03 21:32:18.911665
创建任务	3	1	module_application:job:create	\N	\N	\N	\N	\N	f	t	f	创建任务	null	f	19	103	f3bd89ed-6be3-4b1b-9c8d-5f1473074c6a	0	初始化数据	2026-01-03 21:32:18.911667	2026-01-03 21:32:18.911667
修改和操作任务	3	2	module_application:job:update	\N	\N	\N	\N	\N	f	t	f	修改和操作任务	null	f	19	104	af780bd5-d542-422f-8714-17a67628b705	0	初始化数据	2026-01-03 21:32:18.91167	2026-01-03 21:32:18.91167
删除和清除任务	3	3	module_application:job:delete	\N	\N	\N	\N	\N	f	t	f	删除和清除任务	null	f	19	105	1b6d0689-87fe-4092-9407-7da413b99786	0	初始化数据	2026-01-03 21:32:18.911672	2026-01-03 21:32:18.911673
导出定时任务	3	4	module_application:job:export	\N	\N	\N	\N	\N	f	t	f	导出定时任务	null	f	19	106	5e1b35b0-c349-41a6-8873-e80787e5a00b	0	初始化数据	2026-01-03 21:32:18.911675	2026-01-03 21:32:18.911676
详情定时任务	3	5	module_application:job:detail	\N	\N	\N	\N	\N	f	t	f	详情任务	null	f	19	107	7e9c0d83-f381-42c9-a0a0-448680e8c36c	0	初始化数据	2026-01-03 21:32:18.91168	2026-01-03 21:32:18.911681
查询定时任务	3	6	module_application:job:query	\N	\N	\N	\N	\N	f	t	f	查询定时任务	null	f	19	108	9020114f-35f2-4383-9659-b72f2ff9d72a	0	初始化数据	2026-01-03 21:32:18.911684	2026-01-03 21:32:18.911684
智能对话	3	1	module_application:ai:chat	\N	\N	\N	\N	\N	f	t	f	智能对话	null	f	20	109	353ee35e-c3c1-4ee1-8a64-324bdc7f1d96	0	智能对话	2026-01-03 21:32:18.911686	2026-01-03 21:32:18.911687
在线用户强制下线	3	1	module_monitor:online:delete	\N	\N	\N	\N	\N	f	t	f	在线用户强制下线	null	f	22	110	0edf0de3-ae8d-4a47-9e43-74ac1ff9a8a9	0	初始化数据	2026-01-03 21:32:18.911689	2026-01-03 21:32:18.91169
清除缓存	3	1	module_monitor:cache:delete	\N	\N	\N	\N	\N	f	t	f	清除缓存	null	f	24	111	8ba7c514-fcfe-4bf7-a3fb-3683e2a2927c	0	初始化数据	2026-01-03 21:32:18.911692	2026-01-03 21:32:18.911693
文件上传	3	1	module_monitor:resource:upload	\N	\N	\N	\N	\N	f	t	f	文件上传	null	f	25	112	2e1be8fb-fa3e-422b-baeb-491ca1b39a25	0	初始化数据	2026-01-03 21:32:18.911695	2026-01-03 21:32:18.911695
文件下载	3	2	module_monitor:resource:download	\N	\N	\N	\N	\N	f	t	f	文件下载	null	f	25	113	5876d559-7e73-4f02-bb76-447a5d20a452	0	初始化数据	2026-01-03 21:32:18.911698	2026-01-03 21:32:18.911698
文件删除	3	3	module_monitor:resource:delete	\N	\N	\N	\N	\N	f	t	f	文件删除	null	f	25	114	a37dfbdc-dd4a-43f0-82f5-ff2ad50481ec	0	初始化数据	2026-01-03 21:32:18.911701	2026-01-03 21:32:18.911701
文件移动	3	4	module_monitor:resource:move	\N	\N	\N	\N	\N	f	t	f	文件移动	null	f	25	115	99cf44db-1661-4fd6-8d7d-1d9fd0e963d2	0	初始化数据	2026-01-03 21:32:18.911704	2026-01-03 21:32:18.911704
文件复制	3	5	module_monitor:resource:copy	\N	\N	\N	\N	\N	f	t	f	文件复制	null	f	25	116	43eeccb8-f09e-4a35-9df7-04009fd7ffd4	0	初始化数据	2026-01-03 21:32:18.911706	2026-01-03 21:32:18.911707
文件重命名	3	6	module_monitor:resource:rename	\N	\N	\N	\N	\N	f	t	f	文件重命名	null	f	25	117	c8fd4446-9147-4dd0-9dbb-b7ad7531edb2	0	初始化数据	2026-01-03 21:32:18.911709	2026-01-03 21:32:18.911709
创建目录	3	7	module_monitor:resource:create_dir	\N	\N	\N	\N	\N	f	t	f	创建目录	null	f	25	118	d2c29d13-d63c-41e0-9798-db94fdd06e38	0	初始化数据	2026-01-03 21:32:18.911712	2026-01-03 21:32:18.911712
导出文件列表	3	9	module_monitor:resource:export	\N	\N	\N	\N	\N	f	t	f	导出文件列表	null	f	25	119	5bb86efe-3d16-41d9-a3e6-e1e22cc8683c	0	初始化数据	2026-01-03 21:32:18.911715	2026-01-03 21:32:18.911715
查询代码生成业务表列表	3	1	module_generator:gencode:query	\N	\N	\N	\N	\N	f	t	f	查询代码生成业务表列表	null	f	26	120	2a292a26-2ca3-42ab-ab6c-f8225d916df8	0	查询代码生成业务表列表	2026-01-03 21:32:18.911717	2026-01-03 21:32:18.911718
创建表结构	3	2	module_generator:gencode:create	\N	\N	\N	\N	\N	f	t	f	创建表结构	null	f	26	121	ec7640e8-1790-4563-a54f-d6b487bc3501	0	创建表结构	2026-01-03 21:32:18.91172	2026-01-03 21:32:18.911721
编辑业务表信息	3	3	module_generator:gencode:update	\N	\N	\N	\N	\N	f	t	f	编辑业务表信息	null	f	26	122	c38e5ba5-ffc4-47e3-910e-c24978781830	0	编辑业务表信息	2026-01-03 21:32:18.911723	2026-01-03 21:32:18.911724
删除业务表信息	3	4	module_generator:gencode:delete	\N	\N	\N	\N	\N	f	t	f	删除业务表信息	null	f	26	123	9f534ac6-8ccd-4ea6-a30b-e9aa41177146	0	删除业务表信息	2026-01-03 21:32:18.911726	2026-01-03 21:32:18.911726
导入表结构	3	5	module_generator:gencode:import	\N	\N	\N	\N	\N	f	t	f	导入表结构	null	f	26	124	8fbc97e8-583a-4f51-a87b-819c1158568e	0	导入表结构	2026-01-03 21:32:18.911729	2026-01-03 21:32:18.911729
批量生成代码	3	6	module_generator:gencode:operate	\N	\N	\N	\N	\N	f	t	f	批量生成代码	null	f	26	125	8c98d051-8277-4382-887e-8f11a27fa839	0	批量生成代码	2026-01-03 21:32:18.911732	2026-01-03 21:32:18.911732
生成代码到指定路径	3	7	module_generator:gencode:code	\N	\N	\N	\N	\N	f	t	f	生成代码到指定路径	null	f	26	126	b516e17a-68c7-447b-b67e-e706bec688c6	0	生成代码到指定路径	2026-01-03 21:32:18.911735	2026-01-03 21:32:18.911735
查询数据库表列表	3	8	module_generator:dblist:query	\N	\N	\N	\N	\N	f	t	f	查询数据库表列表	null	f	26	127	c489c527-1397-4763-afb5-39c6bce33c34	0	查询数据库表列表	2026-01-03 21:32:18.911737	2026-01-03 21:32:18.911738
同步数据库	3	9	module_generator:db:sync	\N	\N	\N	\N	\N	f	t	f	同步数据库	null	f	26	128	e98d0079-e340-45bc-b09f-9476f71b2aa3	0	同步数据库	2026-01-03 21:32:18.91174	2026-01-03 21:32:18.911741
创建示例	3	1	module_example:demo:create	\N	\N	\N	\N	\N	f	t	f	创建示例	null	f	29	129	065ff5d5-e279-4df3-91d1-4c81eb589794	0	初始化数据	2026-01-03 21:32:18.911743	2026-01-03 21:32:18.911743
更新示例	3	2	module_example:demo:update	\N	\N	\N	\N	\N	f	t	f	更新示例	null	f	29	130	a7778542-d3cd-4964-839a-6aa631b8955c	0	初始化数据	2026-01-03 21:32:18.911746	2026-01-03 21:32:18.911746
删除示例	3	3	module_example:demo:delete	\N	\N	\N	\N	\N	f	t	f	删除示例	null	f	29	131	e72c989e-69b1-4bad-8c9f-192312c671ba	0	初始化数据	2026-01-03 21:32:18.911749	2026-01-03 21:32:18.911749
批量修改示例状态	3	4	module_example:demo:patch	\N	\N	\N	\N	\N	f	t	f	批量修改示例状态	null	f	29	132	7ef6f0b7-cc65-4283-b1aa-02c29a4a68fc	0	初始化数据	2026-01-03 21:32:18.911751	2026-01-03 21:32:18.911752
导出示例	3	5	module_example:demo:export	\N	\N	\N	\N	\N	f	t	f	导出示例	null	f	29	133	e3e0a107-d9c7-4e2a-85d8-442201477bda	0	初始化数据	2026-01-03 21:32:18.911754	2026-01-03 21:32:18.911754
导入示例	3	6	module_example:demo:import	\N	\N	\N	\N	\N	f	t	f	导入示例	null	f	29	134	82a3f388-66ac-4804-87d5-6c1553a9fb73	0	初始化数据	2026-01-03 21:32:18.911757	2026-01-03 21:32:18.911757
下载导入示例模版	3	7	module_example:demo:download	\N	\N	\N	\N	\N	f	t	f	下载导入示例模版	null	f	29	135	37044da4-53aa-45ca-b0b4-c482a6267738	0	初始化数据	2026-01-03 21:32:18.91176	2026-01-03 21:32:18.91176
详情示例	3	8	module_example:demo:detail	\N	\N	\N	\N	\N	f	t	f	详情示例	null	f	29	136	bcb8c7c2-8336-445b-bd5a-e520df635780	0	初始化数据	2026-01-03 21:32:18.911763	2026-01-03 21:32:18.911763
查询示例	3	9	module_example:demo:query	\N	\N	\N	\N	\N	f	t	f	查询示例	null	f	29	137	b9c1eeb0-426a-42ba-9cec-a6dca30bdb9d	0	初始化数据	2026-01-03 21:32:18.911766	2026-01-03 21:32:18.911766
\.


--
-- Data for Name: sys_notice; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_notice (notice_title, notice_type, notice_content, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: sys_param; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_param (config_name, config_key, config_value, config_type, id, uuid, status, description, created_time, updated_time) FROM stdin;
网站名称	sys_web_title	FastApiAdmin	t	1	c27c73a7-59b3-4942-a6a5-c1014a48ba31	0	初始化数据	2026-01-03 21:32:18.923106	2026-01-03 21:32:18.923107
网站描述	sys_web_description	FastApiAdmin 是完全开源的权限管理系统	t	2	83e5866f-6926-4b27-a323-c8b5457535e6	0	初始化数据	2026-01-03 21:32:18.923111	2026-01-03 21:32:18.923112
网页图标	sys_web_favicon	https://service.fastapiadmin.com/api/v1/static/image/favicon.png	t	3	32ce1f34-f4c2-4b41-9845-f937cc385017	0	初始化数据	2026-01-03 21:32:18.923115	2026-01-03 21:32:18.923115
网站Logo	sys_web_logo	https://service.fastapiadmin.com/api/v1/static/image/logo.png	t	4	d8b9b7e3-c501-4f3c-a71b-94e44d319069	0	初始化数据	2026-01-03 21:32:18.923118	2026-01-03 21:32:18.923118
登录背景	sys_login_background	https://service.fastapiadmin.com/api/v1/static/image/background.svg	t	5	92713ea5-6fa8-4adc-ac7b-5e2a6ab80704	0	初始化数据	2026-01-03 21:32:18.923121	2026-01-03 21:32:18.923122
版权信息	sys_web_copyright	Copyright © 2025-2026 service.fastapiadmin.com 版权所有	t	6	cbd70fb4-28c8-4e13-b9e4-44d461b5c1f1	0	初始化数据	2026-01-03 21:32:18.923125	2026-01-03 21:32:18.923125
备案信息	sys_keep_record	陕ICP备2025069493号-1	t	7	059c93c3-82c2-4dfd-94f3-e539060d9fbc	0	初始化数据	2026-01-03 21:32:18.923128	2026-01-03 21:32:18.923128
帮助文档	sys_help_doc	https://service.fastapiadmin.com	t	8	96ea2556-f9f0-403c-8da6-04c01970fe66	0	初始化数据	2026-01-03 21:32:18.923131	2026-01-03 21:32:18.923132
隐私政策	sys_web_privacy	https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE	t	9	8fc4c4ee-8309-461c-8b62-c9bdeb4586d3	0	初始化数据	2026-01-03 21:32:18.923134	2026-01-03 21:32:18.923135
用户协议	sys_web_clause	https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE	t	10	b47bde1c-a594-4362-8a0a-85b1574f4069	0	初始化数据	2026-01-03 21:32:18.923138	2026-01-03 21:32:18.923138
源码代码	sys_git_code	https://github.com/fastapiadmin/FastapiAdmin.git	t	11	8cd060d1-01f6-48da-9150-b4050341e030	0	初始化数据	2026-01-03 21:32:18.923141	2026-01-03 21:32:18.923141
项目版本	sys_web_version	2.0.0	t	12	f4797975-4fb8-4d5e-8ea9-70330ea2b374	0	初始化数据	2026-01-03 21:32:18.923144	2026-01-03 21:32:18.923144
演示模式启用	demo_enable	false	t	13	f9d47fb7-72a7-4acc-a61e-13f0436b7664	0	初始化数据	2026-01-03 21:32:18.923147	2026-01-03 21:32:18.923148
演示访问IP白名单	ip_white_list	["127.0.0.1"]	t	14	9c60b05f-b473-4706-8d5d-60f1f1fc605b	0	初始化数据	2026-01-03 21:32:18.92315	2026-01-03 21:32:18.923151
接口白名单	white_api_list_path	["/api/v1/system/auth/login", "/api/v1/system/auth/token/refresh", "/api/v1/system/auth/captcha/get", "/api/v1/system/auth/logout", "/api/v1/system/config/info", "/api/v1/system/user/current/info", "/api/v1/system/notice/available"]	t	15	f0bd25e4-3c2c-478b-b625-4e63a9f7cc85	0	初始化数据	2026-01-03 21:32:18.923154	2026-01-03 21:32:18.923154
访问IP黑名单	ip_black_list	[]	t	16	e69668dd-1cf5-406d-9089-788155dd6f39	0	初始化数据	2026-01-03 21:32:18.923157	2026-01-03 21:32:18.923157
\.


--
-- Data for Name: sys_position; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_position (name, "order", id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
\.


--
-- Data for Name: sys_role; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_role (name, code, "order", data_scope, id, uuid, status, description, created_time, updated_time) FROM stdin;
管理员角色	ADMIN	1	4	1	21b7bab1-5126-4d1c-bcbc-63d3b7518f55	0	初始化角色	2026-01-03 21:32:18.92835	2026-01-03 21:32:18.928351
\.


--
-- Data for Name: sys_role_depts; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_role_depts (role_id, dept_id) FROM stdin;
\.


--
-- Data for Name: sys_role_menus; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_role_menus (role_id, menu_id) FROM stdin;
\.


--
-- Data for Name: sys_user; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_user (username, password, name, mobile, email, gender, avatar, is_superuser, last_login, gitee_login, github_login, wx_login, qq_login, dept_id, id, uuid, status, description, created_time, updated_time, created_id, updated_id) FROM stdin;
admin	$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa	超级管理员	\N	\N	0	https://service.fastapiadmin.com/api/v1/static/image/avatar.png	t	\N	\N	\N	\N	\N	1	1	74ae22e9-6ba7-463a-bb88-03cf32e15796	0	超级管理员	2026-01-03 21:32:18.938652	2026-01-03 21:32:18.938653	\N	\N
\.


--
-- Data for Name: sys_user_positions; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_user_positions (user_id, position_id) FROM stdin;
\.


--
-- Data for Name: sys_user_roles; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.sys_user_roles (user_id, role_id) FROM stdin;
1	1
\.


--
-- Name: app_ai_mcp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.app_ai_mcp_id_seq', 1, false);


--
-- Name: app_job_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.app_job_id_seq', 1, false);


--
-- Name: app_job_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.app_job_log_id_seq', 1, false);


--
-- Name: app_myapp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.app_myapp_id_seq', 1, false);


--
-- Name: gen_demo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.gen_demo_id_seq', 1, false);


--
-- Name: gen_table_column_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.gen_table_column_id_seq', 1, false);


--
-- Name: gen_table_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.gen_table_id_seq', 1, false);


--
-- Name: sys_dept_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_dept_id_seq', 1, true);


--
-- Name: sys_dict_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_dict_data_id_seq', 34, true);


--
-- Name: sys_dict_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_dict_type_id_seq', 10, true);


--
-- Name: sys_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_log_id_seq', 1, false);


--
-- Name: sys_menu_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_menu_id_seq', 137, true);


--
-- Name: sys_notice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_notice_id_seq', 1, false);


--
-- Name: sys_param_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_param_id_seq', 16, true);


--
-- Name: sys_position_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_position_id_seq', 1, false);


--
-- Name: sys_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_role_id_seq', 1, true);


--
-- Name: sys_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.sys_user_id_seq', 1, true);


--
-- Name: app_ai_mcp app_ai_mcp_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_ai_mcp
    ADD CONSTRAINT app_ai_mcp_pkey PRIMARY KEY (id);


--
-- Name: app_job_log app_job_log_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_job_log
    ADD CONSTRAINT app_job_log_pkey PRIMARY KEY (id);


--
-- Name: app_job app_job_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_job
    ADD CONSTRAINT app_job_pkey PRIMARY KEY (id);


--
-- Name: app_myapp app_myapp_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_myapp
    ADD CONSTRAINT app_myapp_pkey PRIMARY KEY (id);


--
-- Name: apscheduler_jobs apscheduler_jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.apscheduler_jobs
    ADD CONSTRAINT apscheduler_jobs_pkey PRIMARY KEY (id);


--
-- Name: gen_demo gen_demo_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_demo
    ADD CONSTRAINT gen_demo_pkey PRIMARY KEY (id);


--
-- Name: gen_table_column gen_table_column_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_pkey PRIMARY KEY (id);


--
-- Name: gen_table gen_table_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table
    ADD CONSTRAINT gen_table_pkey PRIMARY KEY (id);


--
-- Name: sys_dept sys_dept_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dept
    ADD CONSTRAINT sys_dept_pkey PRIMARY KEY (id);


--
-- Name: sys_dict_data sys_dict_data_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dict_data
    ADD CONSTRAINT sys_dict_data_pkey PRIMARY KEY (id);


--
-- Name: sys_dict_type sys_dict_type_dict_type_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dict_type
    ADD CONSTRAINT sys_dict_type_dict_type_key UNIQUE (dict_type);


--
-- Name: sys_dict_type sys_dict_type_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dict_type
    ADD CONSTRAINT sys_dict_type_pkey PRIMARY KEY (id);


--
-- Name: sys_log sys_log_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_log
    ADD CONSTRAINT sys_log_pkey PRIMARY KEY (id);


--
-- Name: sys_menu sys_menu_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_menu
    ADD CONSTRAINT sys_menu_pkey PRIMARY KEY (id);


--
-- Name: sys_notice sys_notice_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_notice
    ADD CONSTRAINT sys_notice_pkey PRIMARY KEY (id);


--
-- Name: sys_param sys_param_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_param
    ADD CONSTRAINT sys_param_pkey PRIMARY KEY (id);


--
-- Name: sys_position sys_position_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_position
    ADD CONSTRAINT sys_position_pkey PRIMARY KEY (id);


--
-- Name: sys_role_depts sys_role_depts_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_role_depts
    ADD CONSTRAINT sys_role_depts_pkey PRIMARY KEY (role_id, dept_id);


--
-- Name: sys_role_menus sys_role_menus_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_role_menus
    ADD CONSTRAINT sys_role_menus_pkey PRIMARY KEY (role_id, menu_id);


--
-- Name: sys_role sys_role_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_role
    ADD CONSTRAINT sys_role_pkey PRIMARY KEY (id);


--
-- Name: sys_user sys_user_email_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_email_key UNIQUE (email);


--
-- Name: sys_user sys_user_mobile_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_mobile_key UNIQUE (mobile);


--
-- Name: sys_user sys_user_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_pkey PRIMARY KEY (id);


--
-- Name: sys_user_positions sys_user_positions_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user_positions
    ADD CONSTRAINT sys_user_positions_pkey PRIMARY KEY (user_id, position_id);


--
-- Name: sys_user_roles sys_user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user_roles
    ADD CONSTRAINT sys_user_roles_pkey PRIMARY KEY (user_id, role_id);


--
-- Name: sys_user sys_user_username_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_username_key UNIQUE (username);


--
-- Name: ix_app_ai_mcp_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_ai_mcp_created_id ON public.app_ai_mcp USING btree (created_id);


--
-- Name: ix_app_ai_mcp_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_ai_mcp_created_time ON public.app_ai_mcp USING btree (created_time);


--
-- Name: ix_app_ai_mcp_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_ai_mcp_id ON public.app_ai_mcp USING btree (id);


--
-- Name: ix_app_ai_mcp_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_ai_mcp_status ON public.app_ai_mcp USING btree (status);


--
-- Name: ix_app_ai_mcp_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_ai_mcp_updated_id ON public.app_ai_mcp USING btree (updated_id);


--
-- Name: ix_app_ai_mcp_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_ai_mcp_updated_time ON public.app_ai_mcp USING btree (updated_time);


--
-- Name: ix_app_ai_mcp_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_app_ai_mcp_uuid ON public.app_ai_mcp USING btree (uuid);


--
-- Name: ix_app_job_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_job_created_id ON public.app_job USING btree (created_id);


--
-- Name: ix_app_job_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_job_created_time ON public.app_job USING btree (created_time);


--
-- Name: ix_app_job_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_job_id ON public.app_job USING btree (id);


--
-- Name: ix_app_job_log_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_job_log_created_time ON public.app_job_log USING btree (created_time);


--
-- Name: ix_app_job_log_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_job_log_id ON public.app_job_log USING btree (id);


--
-- Name: ix_app_job_log_job_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_job_log_job_id ON public.app_job_log USING btree (job_id);


--
-- Name: ix_app_job_log_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_job_log_status ON public.app_job_log USING btree (status);


--
-- Name: ix_app_job_log_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_job_log_updated_time ON public.app_job_log USING btree (updated_time);


--
-- Name: ix_app_job_log_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_app_job_log_uuid ON public.app_job_log USING btree (uuid);


--
-- Name: ix_app_job_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_job_status ON public.app_job USING btree (status);


--
-- Name: ix_app_job_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_job_updated_id ON public.app_job USING btree (updated_id);


--
-- Name: ix_app_job_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_job_updated_time ON public.app_job USING btree (updated_time);


--
-- Name: ix_app_job_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_app_job_uuid ON public.app_job USING btree (uuid);


--
-- Name: ix_app_myapp_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_myapp_created_id ON public.app_myapp USING btree (created_id);


--
-- Name: ix_app_myapp_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_myapp_created_time ON public.app_myapp USING btree (created_time);


--
-- Name: ix_app_myapp_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_myapp_id ON public.app_myapp USING btree (id);


--
-- Name: ix_app_myapp_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_myapp_status ON public.app_myapp USING btree (status);


--
-- Name: ix_app_myapp_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_myapp_updated_id ON public.app_myapp USING btree (updated_id);


--
-- Name: ix_app_myapp_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_app_myapp_updated_time ON public.app_myapp USING btree (updated_time);


--
-- Name: ix_app_myapp_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_app_myapp_uuid ON public.app_myapp USING btree (uuid);


--
-- Name: ix_apscheduler_jobs_next_run_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_apscheduler_jobs_next_run_time ON public.apscheduler_jobs USING btree (next_run_time);


--
-- Name: ix_gen_demo_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_demo_created_id ON public.gen_demo USING btree (created_id);


--
-- Name: ix_gen_demo_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_demo_created_time ON public.gen_demo USING btree (created_time);


--
-- Name: ix_gen_demo_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_demo_id ON public.gen_demo USING btree (id);


--
-- Name: ix_gen_demo_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_demo_status ON public.gen_demo USING btree (status);


--
-- Name: ix_gen_demo_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_demo_updated_id ON public.gen_demo USING btree (updated_id);


--
-- Name: ix_gen_demo_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_demo_updated_time ON public.gen_demo USING btree (updated_time);


--
-- Name: ix_gen_demo_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_gen_demo_uuid ON public.gen_demo USING btree (uuid);


--
-- Name: ix_gen_table_column_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_column_created_id ON public.gen_table_column USING btree (created_id);


--
-- Name: ix_gen_table_column_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_column_created_time ON public.gen_table_column USING btree (created_time);


--
-- Name: ix_gen_table_column_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_column_id ON public.gen_table_column USING btree (id);


--
-- Name: ix_gen_table_column_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_column_status ON public.gen_table_column USING btree (status);


--
-- Name: ix_gen_table_column_table_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_column_table_id ON public.gen_table_column USING btree (table_id);


--
-- Name: ix_gen_table_column_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_column_updated_id ON public.gen_table_column USING btree (updated_id);


--
-- Name: ix_gen_table_column_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_column_updated_time ON public.gen_table_column USING btree (updated_time);


--
-- Name: ix_gen_table_column_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_gen_table_column_uuid ON public.gen_table_column USING btree (uuid);


--
-- Name: ix_gen_table_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_created_id ON public.gen_table USING btree (created_id);


--
-- Name: ix_gen_table_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_created_time ON public.gen_table USING btree (created_time);


--
-- Name: ix_gen_table_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_id ON public.gen_table USING btree (id);


--
-- Name: ix_gen_table_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_status ON public.gen_table USING btree (status);


--
-- Name: ix_gen_table_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_updated_id ON public.gen_table USING btree (updated_id);


--
-- Name: ix_gen_table_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_gen_table_updated_time ON public.gen_table USING btree (updated_time);


--
-- Name: ix_gen_table_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_gen_table_uuid ON public.gen_table USING btree (uuid);


--
-- Name: ix_sys_dept_code; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dept_code ON public.sys_dept USING btree (code);


--
-- Name: ix_sys_dept_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dept_created_id ON public.sys_dept USING btree (created_id);


--
-- Name: ix_sys_dept_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dept_created_time ON public.sys_dept USING btree (created_time);


--
-- Name: ix_sys_dept_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dept_id ON public.sys_dept USING btree (id);


--
-- Name: ix_sys_dept_parent_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dept_parent_id ON public.sys_dept USING btree (parent_id);


--
-- Name: ix_sys_dept_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dept_status ON public.sys_dept USING btree (status);


--
-- Name: ix_sys_dept_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dept_updated_id ON public.sys_dept USING btree (updated_id);


--
-- Name: ix_sys_dept_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dept_updated_time ON public.sys_dept USING btree (updated_time);


--
-- Name: ix_sys_dept_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_dept_uuid ON public.sys_dept USING btree (uuid);


--
-- Name: ix_sys_dict_data_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dict_data_created_time ON public.sys_dict_data USING btree (created_time);


--
-- Name: ix_sys_dict_data_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dict_data_id ON public.sys_dict_data USING btree (id);


--
-- Name: ix_sys_dict_data_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dict_data_status ON public.sys_dict_data USING btree (status);


--
-- Name: ix_sys_dict_data_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dict_data_updated_time ON public.sys_dict_data USING btree (updated_time);


--
-- Name: ix_sys_dict_data_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_dict_data_uuid ON public.sys_dict_data USING btree (uuid);


--
-- Name: ix_sys_dict_type_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dict_type_created_time ON public.sys_dict_type USING btree (created_time);


--
-- Name: ix_sys_dict_type_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dict_type_id ON public.sys_dict_type USING btree (id);


--
-- Name: ix_sys_dict_type_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dict_type_status ON public.sys_dict_type USING btree (status);


--
-- Name: ix_sys_dict_type_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_dict_type_updated_time ON public.sys_dict_type USING btree (updated_time);


--
-- Name: ix_sys_dict_type_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_dict_type_uuid ON public.sys_dict_type USING btree (uuid);


--
-- Name: ix_sys_log_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_log_created_id ON public.sys_log USING btree (created_id);


--
-- Name: ix_sys_log_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_log_created_time ON public.sys_log USING btree (created_time);


--
-- Name: ix_sys_log_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_log_id ON public.sys_log USING btree (id);


--
-- Name: ix_sys_log_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_log_status ON public.sys_log USING btree (status);


--
-- Name: ix_sys_log_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_log_updated_id ON public.sys_log USING btree (updated_id);


--
-- Name: ix_sys_log_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_log_updated_time ON public.sys_log USING btree (updated_time);


--
-- Name: ix_sys_log_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_log_uuid ON public.sys_log USING btree (uuid);


--
-- Name: ix_sys_menu_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_menu_created_time ON public.sys_menu USING btree (created_time);


--
-- Name: ix_sys_menu_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_menu_id ON public.sys_menu USING btree (id);


--
-- Name: ix_sys_menu_parent_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_menu_parent_id ON public.sys_menu USING btree (parent_id);


--
-- Name: ix_sys_menu_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_menu_status ON public.sys_menu USING btree (status);


--
-- Name: ix_sys_menu_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_menu_updated_time ON public.sys_menu USING btree (updated_time);


--
-- Name: ix_sys_menu_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_menu_uuid ON public.sys_menu USING btree (uuid);


--
-- Name: ix_sys_notice_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_notice_created_id ON public.sys_notice USING btree (created_id);


--
-- Name: ix_sys_notice_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_notice_created_time ON public.sys_notice USING btree (created_time);


--
-- Name: ix_sys_notice_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_notice_id ON public.sys_notice USING btree (id);


--
-- Name: ix_sys_notice_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_notice_status ON public.sys_notice USING btree (status);


--
-- Name: ix_sys_notice_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_notice_updated_id ON public.sys_notice USING btree (updated_id);


--
-- Name: ix_sys_notice_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_notice_updated_time ON public.sys_notice USING btree (updated_time);


--
-- Name: ix_sys_notice_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_notice_uuid ON public.sys_notice USING btree (uuid);


--
-- Name: ix_sys_param_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_param_created_time ON public.sys_param USING btree (created_time);


--
-- Name: ix_sys_param_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_param_id ON public.sys_param USING btree (id);


--
-- Name: ix_sys_param_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_param_status ON public.sys_param USING btree (status);


--
-- Name: ix_sys_param_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_param_updated_time ON public.sys_param USING btree (updated_time);


--
-- Name: ix_sys_param_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_param_uuid ON public.sys_param USING btree (uuid);


--
-- Name: ix_sys_position_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_position_created_id ON public.sys_position USING btree (created_id);


--
-- Name: ix_sys_position_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_position_created_time ON public.sys_position USING btree (created_time);


--
-- Name: ix_sys_position_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_position_id ON public.sys_position USING btree (id);


--
-- Name: ix_sys_position_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_position_status ON public.sys_position USING btree (status);


--
-- Name: ix_sys_position_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_position_updated_id ON public.sys_position USING btree (updated_id);


--
-- Name: ix_sys_position_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_position_updated_time ON public.sys_position USING btree (updated_time);


--
-- Name: ix_sys_position_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_position_uuid ON public.sys_position USING btree (uuid);


--
-- Name: ix_sys_role_code; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_role_code ON public.sys_role USING btree (code);


--
-- Name: ix_sys_role_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_role_created_time ON public.sys_role USING btree (created_time);


--
-- Name: ix_sys_role_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_role_id ON public.sys_role USING btree (id);


--
-- Name: ix_sys_role_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_role_status ON public.sys_role USING btree (status);


--
-- Name: ix_sys_role_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_role_updated_time ON public.sys_role USING btree (updated_time);


--
-- Name: ix_sys_role_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_role_uuid ON public.sys_role USING btree (uuid);


--
-- Name: ix_sys_user_created_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_user_created_id ON public.sys_user USING btree (created_id);


--
-- Name: ix_sys_user_created_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_user_created_time ON public.sys_user USING btree (created_time);


--
-- Name: ix_sys_user_dept_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_user_dept_id ON public.sys_user USING btree (dept_id);


--
-- Name: ix_sys_user_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_user_id ON public.sys_user USING btree (id);


--
-- Name: ix_sys_user_status; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_user_status ON public.sys_user USING btree (status);


--
-- Name: ix_sys_user_updated_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_user_updated_id ON public.sys_user USING btree (updated_id);


--
-- Name: ix_sys_user_updated_time; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_sys_user_updated_time ON public.sys_user USING btree (updated_time);


--
-- Name: ix_sys_user_uuid; Type: INDEX; Schema: public; Owner: tao
--

CREATE UNIQUE INDEX ix_sys_user_uuid ON public.sys_user USING btree (uuid);


--
-- Name: app_ai_mcp app_ai_mcp_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_ai_mcp
    ADD CONSTRAINT app_ai_mcp_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: app_ai_mcp app_ai_mcp_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_ai_mcp
    ADD CONSTRAINT app_ai_mcp_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: app_job app_job_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_job
    ADD CONSTRAINT app_job_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: app_job_log app_job_log_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_job_log
    ADD CONSTRAINT app_job_log_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.app_job(id) ON DELETE CASCADE;


--
-- Name: app_job app_job_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_job
    ADD CONSTRAINT app_job_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: app_myapp app_myapp_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_myapp
    ADD CONSTRAINT app_myapp_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: app_myapp app_myapp_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.app_myapp
    ADD CONSTRAINT app_myapp_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_demo gen_demo_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_demo
    ADD CONSTRAINT gen_demo_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_demo gen_demo_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_demo
    ADD CONSTRAINT gen_demo_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_table_column gen_table_column_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_table_column gen_table_column_table_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_table_id_fkey FOREIGN KEY (table_id) REFERENCES public.gen_table(id) ON DELETE CASCADE;


--
-- Name: gen_table_column gen_table_column_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table_column
    ADD CONSTRAINT gen_table_column_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_table gen_table_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table
    ADD CONSTRAINT gen_table_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: gen_table gen_table_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.gen_table
    ADD CONSTRAINT gen_table_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_dept sys_dept_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dept
    ADD CONSTRAINT sys_dept_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_dept sys_dept_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dept
    ADD CONSTRAINT sys_dept_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.sys_dept(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_dept sys_dept_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dept
    ADD CONSTRAINT sys_dept_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_dict_data sys_dict_data_dict_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_dict_data
    ADD CONSTRAINT sys_dict_data_dict_type_id_fkey FOREIGN KEY (dict_type_id) REFERENCES public.sys_dict_type(id) ON DELETE CASCADE;


--
-- Name: sys_log sys_log_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_log
    ADD CONSTRAINT sys_log_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_log sys_log_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_log
    ADD CONSTRAINT sys_log_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_menu sys_menu_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_menu
    ADD CONSTRAINT sys_menu_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.sys_menu(id) ON DELETE SET NULL;


--
-- Name: sys_notice sys_notice_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_notice
    ADD CONSTRAINT sys_notice_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_notice sys_notice_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_notice
    ADD CONSTRAINT sys_notice_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_position sys_position_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_position
    ADD CONSTRAINT sys_position_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_position sys_position_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_position
    ADD CONSTRAINT sys_position_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_role_depts sys_role_depts_dept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_role_depts
    ADD CONSTRAINT sys_role_depts_dept_id_fkey FOREIGN KEY (dept_id) REFERENCES public.sys_dept(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_role_depts sys_role_depts_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_role_depts
    ADD CONSTRAINT sys_role_depts_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.sys_role(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_role_menus sys_role_menus_menu_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_role_menus
    ADD CONSTRAINT sys_role_menus_menu_id_fkey FOREIGN KEY (menu_id) REFERENCES public.sys_menu(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_role_menus sys_role_menus_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_role_menus
    ADD CONSTRAINT sys_role_menus_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.sys_role(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_user sys_user_created_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_created_id_fkey FOREIGN KEY (created_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_user sys_user_dept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_dept_id_fkey FOREIGN KEY (dept_id) REFERENCES public.sys_dept(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: sys_user_positions sys_user_positions_position_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user_positions
    ADD CONSTRAINT sys_user_positions_position_id_fkey FOREIGN KEY (position_id) REFERENCES public.sys_position(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_user_positions sys_user_positions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user_positions
    ADD CONSTRAINT sys_user_positions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_user_roles sys_user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user_roles
    ADD CONSTRAINT sys_user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.sys_role(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_user_roles sys_user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user_roles
    ADD CONSTRAINT sys_user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sys_user sys_user_updated_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.sys_user
    ADD CONSTRAINT sys_user_updated_id_fkey FOREIGN KEY (updated_id) REFERENCES public.sys_user(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

