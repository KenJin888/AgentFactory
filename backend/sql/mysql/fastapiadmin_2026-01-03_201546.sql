-- MySQL dump 10.13  Distrib 8.4.3, for macos14.5 (arm64)
--
-- Host: 127.0.0.1    Database: fastapiadmin
-- ------------------------------------------------------
-- Server version	8.4.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_ai_mcp`
--

DROP TABLE IF EXISTS `app_ai_mcp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_ai_mcp` (
  `name` varchar(50) NOT NULL COMMENT 'MCP 名称',
  `type` int NOT NULL COMMENT 'MCP 类型(0:stdio 1:sse)',
  `url` varchar(255) DEFAULT NULL COMMENT '远程 SSE 地址',
  `command` varchar(255) DEFAULT NULL COMMENT 'MCP 命令',
  `args` varchar(255) DEFAULT NULL COMMENT 'MCP 命令参数',
  `env` json DEFAULT NULL COMMENT 'MCP 环境变量',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_app_ai_mcp_uuid` (`uuid`),
  KEY `ix_app_ai_mcp_created_time` (`created_time`),
  KEY `ix_app_ai_mcp_id` (`id`),
  KEY `ix_app_ai_mcp_updated_time` (`updated_time`),
  KEY `ix_app_ai_mcp_created_id` (`created_id`),
  KEY `ix_app_ai_mcp_status` (`status`),
  KEY `ix_app_ai_mcp_updated_id` (`updated_id`),
  CONSTRAINT `app_ai_mcp_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `app_ai_mcp_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='MCP 服务器表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_ai_mcp`
--

/*!40000 ALTER TABLE `app_ai_mcp` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_ai_mcp` ENABLE KEYS */;

--
-- Table structure for table `app_job`
--

DROP TABLE IF EXISTS `app_job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_job` (
  `name` varchar(64) DEFAULT NULL COMMENT '任务名称',
  `jobstore` varchar(64) DEFAULT NULL COMMENT '存储器',
  `executor` varchar(64) DEFAULT NULL COMMENT '执行器:将运行此作业的执行程序的名称',
  `trigger` varchar(64) NOT NULL COMMENT '触发器:控制此作业计划的 trigger 对象',
  `trigger_args` text COMMENT '触发器参数',
  `func` text NOT NULL COMMENT '任务函数',
  `args` text COMMENT '位置参数',
  `kwargs` text COMMENT '关键字参数',
  `coalesce` tinyint(1) DEFAULT NULL COMMENT '是否合并运行:是否在多个运行时间到期时仅运行作业一次',
  `max_instances` int DEFAULT NULL COMMENT '最大实例数:允许的最大并发执行实例数',
  `start_date` varchar(64) DEFAULT NULL COMMENT '开始时间',
  `end_date` varchar(64) DEFAULT NULL COMMENT '结束时间',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_app_job_uuid` (`uuid`),
  KEY `ix_app_job_status` (`status`),
  KEY `ix_app_job_created_id` (`created_id`),
  KEY `ix_app_job_updated_time` (`updated_time`),
  KEY `ix_app_job_id` (`id`),
  KEY `ix_app_job_created_time` (`created_time`),
  KEY `ix_app_job_updated_id` (`updated_id`),
  CONSTRAINT `app_job_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `app_job_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='定时任务调度表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_job`
--

/*!40000 ALTER TABLE `app_job` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_job` ENABLE KEYS */;

--
-- Table structure for table `app_job_log`
--

DROP TABLE IF EXISTS `app_job_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_job_log` (
  `job_name` varchar(64) NOT NULL COMMENT '任务名称',
  `job_group` varchar(64) NOT NULL COMMENT '任务组名',
  `job_executor` varchar(64) NOT NULL COMMENT '任务执行器',
  `invoke_target` varchar(500) NOT NULL COMMENT '调用目标字符串',
  `job_args` varchar(255) DEFAULT NULL COMMENT '位置参数',
  `job_kwargs` varchar(255) DEFAULT NULL COMMENT '关键字参数',
  `job_trigger` varchar(255) DEFAULT NULL COMMENT '任务触发器',
  `job_message` varchar(500) DEFAULT NULL COMMENT '日志信息',
  `exception_info` varchar(2000) DEFAULT NULL COMMENT '异常信息',
  `job_id` int DEFAULT NULL COMMENT '任务ID',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_app_job_log_uuid` (`uuid`),
  KEY `ix_app_job_log_created_time` (`created_time`),
  KEY `ix_app_job_log_updated_time` (`updated_time`),
  KEY `ix_app_job_log_id` (`id`),
  KEY `ix_app_job_log_status` (`status`),
  KEY `ix_app_job_log_job_id` (`job_id`),
  CONSTRAINT `app_job_log_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `app_job` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='定时任务调度日志表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_job_log`
--

/*!40000 ALTER TABLE `app_job_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_job_log` ENABLE KEYS */;

--
-- Table structure for table `app_myapp`
--

DROP TABLE IF EXISTS `app_myapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_myapp` (
  `name` varchar(64) NOT NULL COMMENT '应用名称',
  `access_url` varchar(500) NOT NULL COMMENT '访问地址',
  `icon_url` varchar(300) DEFAULT NULL COMMENT '应用图标URL',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_app_myapp_uuid` (`uuid`),
  KEY `ix_app_myapp_updated_time` (`updated_time`),
  KEY `ix_app_myapp_created_id` (`created_id`),
  KEY `ix_app_myapp_status` (`status`),
  KEY `ix_app_myapp_updated_id` (`updated_id`),
  KEY `ix_app_myapp_created_time` (`created_time`),
  KEY `ix_app_myapp_id` (`id`),
  CONSTRAINT `app_myapp_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `app_myapp_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='应用系统表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_myapp`
--

/*!40000 ALTER TABLE `app_myapp` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_myapp` ENABLE KEYS */;

--
-- Table structure for table `apscheduler_jobs`
--

DROP TABLE IF EXISTS `apscheduler_jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apscheduler_jobs` (
  `id` varchar(191) NOT NULL,
  `next_run_time` double DEFAULT NULL,
  `job_state` blob NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_apscheduler_jobs_next_run_time` (`next_run_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apscheduler_jobs`
--

/*!40000 ALTER TABLE `apscheduler_jobs` DISABLE KEYS */;
/*!40000 ALTER TABLE `apscheduler_jobs` ENABLE KEYS */;

--
-- Table structure for table `gen_demo`
--

DROP TABLE IF EXISTS `gen_demo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gen_demo` (
  `name` varchar(64) NOT NULL COMMENT '名称',
  `a` int DEFAULT NULL COMMENT '整数',
  `b` bigint DEFAULT NULL COMMENT '大整数',
  `c` float DEFAULT NULL COMMENT '浮点数',
  `d` tinyint(1) NOT NULL COMMENT '布尔型',
  `e` date DEFAULT NULL COMMENT '日期',
  `f` time DEFAULT NULL COMMENT '时间',
  `g` datetime DEFAULT NULL COMMENT '日期时间',
  `h` text COMMENT '长文本',
  `i` json DEFAULT NULL COMMENT '元数据(JSON格式)',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_gen_demo_uuid` (`uuid`),
  KEY `ix_gen_demo_updated_time` (`updated_time`),
  KEY `ix_gen_demo_created_id` (`created_id`),
  KEY `ix_gen_demo_id` (`id`),
  KEY `ix_gen_demo_status` (`status`),
  KEY `ix_gen_demo_updated_id` (`updated_id`),
  KEY `ix_gen_demo_created_time` (`created_time`),
  CONSTRAINT `gen_demo_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `gen_demo_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='示例表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gen_demo`
--

/*!40000 ALTER TABLE `gen_demo` DISABLE KEYS */;
/*!40000 ALTER TABLE `gen_demo` ENABLE KEYS */;

--
-- Table structure for table `gen_table`
--

DROP TABLE IF EXISTS `gen_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gen_table` (
  `table_name` varchar(200) NOT NULL COMMENT '表名称',
  `table_comment` varchar(500) DEFAULT NULL COMMENT '表描述',
  `class_name` varchar(100) NOT NULL COMMENT '实体类名称',
  `package_name` varchar(100) DEFAULT NULL COMMENT '生成包路径',
  `module_name` varchar(30) DEFAULT NULL COMMENT '生成模块名',
  `business_name` varchar(30) DEFAULT NULL COMMENT '生成业务名',
  `function_name` varchar(100) DEFAULT NULL COMMENT '生成功能名',
  `sub_table_name` varchar(64) DEFAULT NULL COMMENT '关联子表的表名',
  `sub_table_fk_name` varchar(64) DEFAULT NULL COMMENT '子表关联的外键名',
  `parent_menu_id` int DEFAULT NULL COMMENT '父菜单ID',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_gen_table_uuid` (`uuid`),
  KEY `ix_gen_table_created_id` (`created_id`),
  KEY `ix_gen_table_created_time` (`created_time`),
  KEY `ix_gen_table_updated_id` (`updated_id`),
  KEY `ix_gen_table_id` (`id`),
  KEY `ix_gen_table_status` (`status`),
  KEY `ix_gen_table_updated_time` (`updated_time`),
  CONSTRAINT `gen_table_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `gen_table_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='代码生成表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gen_table`
--

/*!40000 ALTER TABLE `gen_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `gen_table` ENABLE KEYS */;

--
-- Table structure for table `gen_table_column`
--

DROP TABLE IF EXISTS `gen_table_column`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gen_table_column` (
  `column_name` varchar(200) NOT NULL COMMENT '列名称',
  `column_comment` varchar(500) DEFAULT NULL COMMENT '列描述',
  `column_type` varchar(100) NOT NULL COMMENT '列类型',
  `column_length` varchar(50) DEFAULT NULL COMMENT '列长度',
  `column_default` varchar(200) DEFAULT NULL COMMENT '列默认值',
  `is_pk` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否主键',
  `is_increment` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否自增',
  `is_nullable` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否允许为空',
  `is_unique` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否唯一',
  `python_type` varchar(100) DEFAULT NULL COMMENT 'Python类型',
  `python_field` varchar(200) DEFAULT NULL COMMENT 'Python字段名',
  `is_insert` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否为新增字段',
  `is_edit` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否编辑字段',
  `is_list` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否列表字段',
  `is_query` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否查询字段',
  `query_type` varchar(50) DEFAULT NULL COMMENT '查询方式',
  `html_type` varchar(100) DEFAULT NULL COMMENT '显示类型',
  `dict_type` varchar(200) DEFAULT NULL COMMENT '字典类型',
  `sort` int NOT NULL COMMENT '排序',
  `table_id` int NOT NULL COMMENT '归属表编号',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_gen_table_column_uuid` (`uuid`),
  KEY `ix_gen_table_column_status` (`status`),
  KEY `ix_gen_table_column_id` (`id`),
  KEY `ix_gen_table_column_created_time` (`created_time`),
  KEY `ix_gen_table_column_created_id` (`created_id`),
  KEY `ix_gen_table_column_table_id` (`table_id`),
  KEY `ix_gen_table_column_updated_id` (`updated_id`),
  KEY `ix_gen_table_column_updated_time` (`updated_time`),
  CONSTRAINT `gen_table_column_ibfk_1` FOREIGN KEY (`table_id`) REFERENCES `gen_table` (`id`) ON DELETE CASCADE,
  CONSTRAINT `gen_table_column_ibfk_2` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `gen_table_column_ibfk_3` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='代码生成表字段';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gen_table_column`
--

/*!40000 ALTER TABLE `gen_table_column` DISABLE KEYS */;
/*!40000 ALTER TABLE `gen_table_column` ENABLE KEYS */;

--
-- Table structure for table `sys_dept`
--

DROP TABLE IF EXISTS `sys_dept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_dept` (
  `name` varchar(64) NOT NULL COMMENT '部门名称',
  `order` int NOT NULL COMMENT '显示排序',
  `code` varchar(16) DEFAULT NULL COMMENT '部门编码',
  `leader` varchar(32) DEFAULT NULL COMMENT '部门负责人',
  `phone` varchar(11) DEFAULT NULL COMMENT '手机',
  `email` varchar(64) DEFAULT NULL COMMENT '邮箱',
  `parent_id` int DEFAULT NULL COMMENT '父级部门ID',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_dept_uuid` (`uuid`),
  KEY `ix_sys_dept_created_id` (`created_id`),
  KEY `ix_sys_dept_status` (`status`),
  KEY `ix_sys_dept_updated_id` (`updated_id`),
  KEY `ix_sys_dept_created_time` (`created_time`),
  KEY `ix_sys_dept_id` (`id`),
  KEY `ix_sys_dept_code` (`code`),
  KEY `ix_sys_dept_updated_time` (`updated_time`),
  KEY `ix_sys_dept_parent_id` (`parent_id`),
  CONSTRAINT `sys_dept_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_dept_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_dept_ibfk_3` FOREIGN KEY (`parent_id`) REFERENCES `sys_dept` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='部门表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dept`
--

/*!40000 ALTER TABLE `sys_dept` DISABLE KEYS */;
INSERT INTO `sys_dept` VALUES ('集团总公司',1,'GROUP','部门负责人','1582112620','deptadmin@example.com',NULL,1,'5100f8a1-c846-4e9f-bc48-03ddf7b8cfa8','0','集团总公司','2026-01-03 20:15:40','2026-01-03 20:15:40',NULL,NULL);
/*!40000 ALTER TABLE `sys_dept` ENABLE KEYS */;

--
-- Table structure for table `sys_dict_data`
--

DROP TABLE IF EXISTS `sys_dict_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_dict_data` (
  `dict_sort` int NOT NULL COMMENT '字典排序',
  `dict_label` varchar(255) NOT NULL COMMENT '字典标签',
  `dict_value` varchar(255) NOT NULL COMMENT '字典键值',
  `css_class` varchar(255) DEFAULT NULL COMMENT '样式属性（其他样式扩展）',
  `list_class` varchar(255) DEFAULT NULL COMMENT '表格回显样式',
  `is_default` tinyint(1) NOT NULL COMMENT '是否默认（True是 False否）',
  `dict_type` varchar(255) NOT NULL COMMENT '字典类型',
  `dict_type_id` int NOT NULL COMMENT '字典类型ID',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_dict_data_uuid` (`uuid`),
  KEY `dict_type_id` (`dict_type_id`),
  KEY `ix_sys_dict_data_created_time` (`created_time`),
  KEY `ix_sys_dict_data_status` (`status`),
  KEY `ix_sys_dict_data_updated_time` (`updated_time`),
  KEY `ix_sys_dict_data_id` (`id`),
  CONSTRAINT `sys_dict_data_ibfk_1` FOREIGN KEY (`dict_type_id`) REFERENCES `sys_dict_type` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='字典数据表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dict_data`
--

/*!40000 ALTER TABLE `sys_dict_data` DISABLE KEYS */;
INSERT INTO `sys_dict_data` VALUES (1,'男','0','blue',NULL,1,'sys_user_sex',1,1,'b71c0f3e-983b-4e21-a9df-b1544bda8c1e','0','性别男','2026-01-03 20:15:40','2026-01-03 20:15:40'),(2,'女','1','pink',NULL,0,'sys_user_sex',1,2,'5253857a-dbb7-47a5-abbf-a7b60591473d','0','性别女','2026-01-03 20:15:40','2026-01-03 20:15:40'),(3,'未知','2','red',NULL,0,'sys_user_sex',1,3,'982fcce9-05f2-403b-8108-5ce406834f1d','0','性别未知','2026-01-03 20:15:40','2026-01-03 20:15:40'),(1,'是','1','','primary',1,'sys_yes_no',2,4,'dc8ac98b-0800-4047-ab14-3c6dc1e6ac2d','0','是','2026-01-03 20:15:40','2026-01-03 20:15:40'),(2,'否','0','','danger',0,'sys_yes_no',2,5,'78b59b15-f2e7-42d7-ad8a-040c41c12657','0','否','2026-01-03 20:15:40','2026-01-03 20:15:40'),(1,'启用','1','','primary',0,'sys_common_status',3,6,'fe1a3c63-dd4b-4e5a-9552-5087e8fecbca','0','启用状态','2026-01-03 20:15:40','2026-01-03 20:15:40'),(2,'停用','0','','danger',0,'sys_common_status',3,7,'1281843e-7511-42b6-9c15-1051a413c852','0','停用状态','2026-01-03 20:15:40','2026-01-03 20:15:40'),(1,'通知','1','blue','warning',1,'sys_notice_type',4,8,'0165557b-0ec4-4119-bba0-60b859ffbecd','0','通知','2026-01-03 20:15:40','2026-01-03 20:15:40'),(2,'公告','2','orange','success',0,'sys_notice_type',4,9,'0ca9b44f-81a3-4206-9259-0bc21a20a061','0','公告','2026-01-03 20:15:40','2026-01-03 20:15:40'),(99,'其他','0','','info',0,'sys_oper_type',5,10,'38d79ba8-4bf7-4ba0-83a9-c9213cb99e36','0','其他操作','2026-01-03 20:15:40','2026-01-03 20:15:40'),(1,'新增','1','','info',0,'sys_oper_type',5,11,'abe2f3c3-1c78-4343-9573-2a6d3352a66a','0','新增操作','2026-01-03 20:15:40','2026-01-03 20:15:40'),(2,'修改','2','','info',0,'sys_oper_type',5,12,'961ba743-3aa9-4d99-a32b-8aa91034adad','0','修改操作','2026-01-03 20:15:40','2026-01-03 20:15:40'),(3,'删除','3','','danger',0,'sys_oper_type',5,13,'9effb5cb-3ce7-479a-ab62-5c48febcb16c','0','删除操作','2026-01-03 20:15:40','2026-01-03 20:15:40'),(4,'分配权限','4','','primary',0,'sys_oper_type',5,14,'29cc5cb9-0cc0-4159-9af5-54835abec41b','0','授权操作','2026-01-03 20:15:40','2026-01-03 20:15:40'),(5,'导出','5','','warning',0,'sys_oper_type',5,15,'214093c5-4b65-4f0b-b5fd-1bddf1a6b3d4','0','导出操作','2026-01-03 20:15:40','2026-01-03 20:15:40'),(6,'导入','6','','warning',0,'sys_oper_type',5,16,'67c70659-e716-4c1f-ac3a-f3f4938b1203','0','导入操作','2026-01-03 20:15:40','2026-01-03 20:15:40'),(7,'强退','7','','danger',0,'sys_oper_type',5,17,'39ecb30b-edc3-422d-b089-6d93235f5d26','0','强退操作','2026-01-03 20:15:40','2026-01-03 20:15:40'),(8,'生成代码','8','','warning',0,'sys_oper_type',5,18,'debd57ce-1342-4e5d-a85f-f4535352905a','0','生成操作','2026-01-03 20:15:40','2026-01-03 20:15:40'),(9,'清空数据','9','','danger',0,'sys_oper_type',5,19,'ab56b2c7-973b-4dd9-860b-0164bc5ba019','0','清空操作','2026-01-03 20:15:40','2026-01-03 20:15:40'),(1,'默认(Memory)','default','',NULL,1,'sys_job_store',6,20,'5618beeb-3a05-4ef9-a740-efd90b59552d','0','默认分组','2026-01-03 20:15:40','2026-01-03 20:15:40'),(2,'数据库(Sqlalchemy)','sqlalchemy','',NULL,0,'sys_job_store',6,21,'d7bc5d31-50e9-4db7-9a92-a6547ec4a97c','0','数据库分组','2026-01-03 20:15:40','2026-01-03 20:15:40'),(3,'数据库(Redis)','redis','',NULL,0,'sys_job_store',6,22,'6a952248-23ed-420d-9bc8-db0698e638e4','0','reids分组','2026-01-03 20:15:40','2026-01-03 20:15:40'),(1,'线程池','default','',NULL,0,'sys_job_executor',7,23,'c8a000a4-883a-4ca9-b66b-a1df8d7f3f1d','0','线程池','2026-01-03 20:15:40','2026-01-03 20:15:40'),(2,'进程池','processpool','',NULL,0,'sys_job_executor',7,24,'b7da32b7-3bd6-4d4f-b879-d6ee4f02aeab','0','进程池','2026-01-03 20:15:40','2026-01-03 20:15:40'),(1,'演示函数','scheduler_test.job','',NULL,1,'sys_job_function',8,25,'a4fe97af-29ff-4a79-9eb3-9fe970ec81de','0','演示函数','2026-01-03 20:15:40','2026-01-03 20:15:40'),(1,'指定日期(date)','date','',NULL,1,'sys_job_trigger',9,26,'e4327cb8-7530-427f-825a-e10587ab4c1e','0','指定日期任务触发器','2026-01-03 20:15:40','2026-01-03 20:15:40'),(2,'间隔触发器(interval)','interval','',NULL,0,'sys_job_trigger',9,27,'b7c28ff0-1d77-43c1-8338-b80e7cbebaba','0','间隔触发器任务触发器','2026-01-03 20:15:40','2026-01-03 20:15:40'),(3,'cron表达式','cron','',NULL,0,'sys_job_trigger',9,28,'dee0c67b-67b9-4e40-8667-aa904a6a9b23','0','间隔触发器任务触发器','2026-01-03 20:15:40','2026-01-03 20:15:40'),(1,'默认(default)','default','',NULL,1,'sys_list_class',10,29,'b74feec7-4854-4df2-96a3-b239019d1d95','0','默认表格回显样式','2026-01-03 20:15:40','2026-01-03 20:15:40'),(2,'主要(primary)','primary','',NULL,0,'sys_list_class',10,30,'c2add402-5bb8-4578-b3bd-1ed5812c53e1','0','主要表格回显样式','2026-01-03 20:15:40','2026-01-03 20:15:40'),(3,'成功(success)','success','',NULL,0,'sys_list_class',10,31,'a2ff7ac9-d2ff-4e91-ad61-f131b02ee7fa','0','成功表格回显样式','2026-01-03 20:15:40','2026-01-03 20:15:40'),(4,'信息(info)','info','',NULL,0,'sys_list_class',10,32,'b7ee3f0f-c602-4c9f-b825-3e66a043235c','0','信息表格回显样式','2026-01-03 20:15:40','2026-01-03 20:15:40'),(5,'警告(warning)','warning','',NULL,0,'sys_list_class',10,33,'b97564d3-dff5-4604-95ad-a2ab0a965abd','0','警告表格回显样式','2026-01-03 20:15:40','2026-01-03 20:15:40'),(6,'危险(danger)','danger','',NULL,0,'sys_list_class',10,34,'66e34673-4da4-4e23-8aeb-b5c0072283a4','0','危险表格回显样式','2026-01-03 20:15:40','2026-01-03 20:15:40');
/*!40000 ALTER TABLE `sys_dict_data` ENABLE KEYS */;

--
-- Table structure for table `sys_dict_type`
--

DROP TABLE IF EXISTS `sys_dict_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_dict_type` (
  `dict_name` varchar(64) NOT NULL COMMENT '字典名称',
  `dict_type` varchar(255) NOT NULL COMMENT '字典类型',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `dict_type` (`dict_type`),
  UNIQUE KEY `ix_sys_dict_type_uuid` (`uuid`),
  KEY `ix_sys_dict_type_id` (`id`),
  KEY `ix_sys_dict_type_updated_time` (`updated_time`),
  KEY `ix_sys_dict_type_status` (`status`),
  KEY `ix_sys_dict_type_created_time` (`created_time`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='字典类型表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dict_type`
--

/*!40000 ALTER TABLE `sys_dict_type` DISABLE KEYS */;
INSERT INTO `sys_dict_type` VALUES ('用户性别','sys_user_sex',1,'27b1bb0b-8a00-4ea8-929d-c3f0547449ec','0','用户性别列表','2026-01-03 20:15:40','2026-01-03 20:15:40'),('系统是否','sys_yes_no',2,'c4ff4678-78cd-47e5-b77b-de1b137d2eee','0','系统是否列表','2026-01-03 20:15:40','2026-01-03 20:15:40'),('系统状态','sys_common_status',3,'19fd6bf7-aa2f-4edb-946b-27dc7d44ad3e','0','系统状态','2026-01-03 20:15:40','2026-01-03 20:15:40'),('通知类型','sys_notice_type',4,'197af39f-67df-4d2c-8ebf-ce3f02974c42','0','通知类型列表','2026-01-03 20:15:40','2026-01-03 20:15:40'),('操作类型','sys_oper_type',5,'e80add1a-7f9f-427d-9739-bf3376cf3c22','0','操作类型列表','2026-01-03 20:15:40','2026-01-03 20:15:40'),('任务存储器','sys_job_store',6,'269c2b74-16d1-4fc1-a08f-d091d69c72ba','0','任务分组列表','2026-01-03 20:15:40','2026-01-03 20:15:40'),('任务执行器','sys_job_executor',7,'d44dedf6-e444-4e33-b767-a392276fe508','0','任务执行器列表','2026-01-03 20:15:40','2026-01-03 20:15:40'),('任务函数','sys_job_function',8,'b00b874d-19aa-4084-a0b7-b974f28889b3','0','任务函数列表','2026-01-03 20:15:40','2026-01-03 20:15:40'),('任务触发器','sys_job_trigger',9,'f69c3d51-02db-4dca-bd8c-08a2d4aa025e','0','任务触发器列表','2026-01-03 20:15:40','2026-01-03 20:15:40'),('表格回显样式','sys_list_class',10,'022c2430-953c-4e3f-ae2d-c7b0c5bd65dc','0','表格回显样式列表','2026-01-03 20:15:40','2026-01-03 20:15:40');
/*!40000 ALTER TABLE `sys_dict_type` ENABLE KEYS */;

--
-- Table structure for table `sys_log`
--

DROP TABLE IF EXISTS `sys_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_log` (
  `type` int NOT NULL COMMENT '日志类型(1登录日志 2操作日志)',
  `request_path` varchar(255) NOT NULL COMMENT '请求路径',
  `request_method` varchar(10) NOT NULL COMMENT '请求方式',
  `request_payload` text COMMENT '请求体',
  `request_ip` varchar(50) DEFAULT NULL COMMENT '请求IP地址',
  `login_location` varchar(255) DEFAULT NULL COMMENT '登录位置',
  `request_os` varchar(64) DEFAULT NULL COMMENT '操作系统',
  `request_browser` varchar(64) DEFAULT NULL COMMENT '浏览器',
  `response_code` int NOT NULL COMMENT '响应状态码',
  `response_json` text COMMENT '响应体',
  `process_time` varchar(20) DEFAULT NULL COMMENT '处理时间',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_log_uuid` (`uuid`),
  KEY `ix_sys_log_created_id` (`created_id`),
  KEY `ix_sys_log_updated_time` (`updated_time`),
  KEY `ix_sys_log_updated_id` (`updated_id`),
  KEY `ix_sys_log_id` (`id`),
  KEY `ix_sys_log_created_time` (`created_time`),
  KEY `ix_sys_log_status` (`status`),
  CONSTRAINT `sys_log_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_log_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='系统日志表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_log`
--

/*!40000 ALTER TABLE `sys_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_log` ENABLE KEYS */;

--
-- Table structure for table `sys_menu`
--

DROP TABLE IF EXISTS `sys_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_menu` (
  `name` varchar(50) NOT NULL COMMENT '菜单名称',
  `type` int NOT NULL COMMENT '菜单类型(1:目录 2:菜单 3:按钮/权限 4:链接)',
  `order` int NOT NULL COMMENT '显示排序',
  `permission` varchar(100) DEFAULT NULL COMMENT '权限标识(如:module_system:user:query)',
  `icon` varchar(50) DEFAULT NULL COMMENT '菜单图标',
  `route_name` varchar(100) DEFAULT NULL COMMENT '路由名称',
  `route_path` varchar(200) DEFAULT NULL COMMENT '路由路径',
  `component_path` varchar(200) DEFAULT NULL COMMENT '组件路径',
  `redirect` varchar(200) DEFAULT NULL COMMENT '重定向地址',
  `hidden` tinyint(1) NOT NULL COMMENT '是否隐藏(True:隐藏 False:显示)',
  `keep_alive` tinyint(1) NOT NULL COMMENT '是否缓存(True:是 False:否)',
  `always_show` tinyint(1) NOT NULL COMMENT '是否始终显示(True:是 False:否)',
  `title` varchar(50) DEFAULT NULL COMMENT '菜单标题',
  `params` json DEFAULT NULL COMMENT '路由参数(JSON对象)',
  `affix` tinyint(1) NOT NULL COMMENT '是否固定标签页(True:是 False:否)',
  `parent_id` int DEFAULT NULL COMMENT '父菜单ID',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_menu_uuid` (`uuid`),
  KEY `ix_sys_menu_updated_time` (`updated_time`),
  KEY `ix_sys_menu_status` (`status`),
  KEY `ix_sys_menu_created_time` (`created_time`),
  KEY `ix_sys_menu_id` (`id`),
  KEY `ix_sys_menu_parent_id` (`parent_id`),
  CONSTRAINT `sys_menu_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `sys_menu` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=138 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='菜单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_menu`
--

/*!40000 ALTER TABLE `sys_menu` DISABLE KEYS */;
INSERT INTO `sys_menu` VALUES ('仪表盘',1,1,'','client','Dashboard','/dashboard',NULL,'/dashboard/workplace',0,1,1,'仪表盘','null',0,NULL,1,'6ab03272-a823-4d2b-8bcc-00ef363f96fd','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('系统管理',1,2,NULL,'system','System','/system',NULL,'/system/menu',0,1,0,'系统管理','null',0,NULL,2,'87609dc2-9d90-48df-ab17-568f67665e4a','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('应用管理',1,3,NULL,'el-icon-ShoppingBag','Application','/application',NULL,'/application/myapp',0,1,0,'应用管理','null',0,NULL,3,'f4200bfa-839e-483b-85e1-01b8f4620aaa','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('监控管理',1,4,NULL,'monitor','Monitor','/monitor',NULL,'/monitor/online',0,1,0,'监控管理','null',0,NULL,4,'fbe6a232-649b-48c9-853f-e34aeb21dc04','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('代码管理',1,5,NULL,'code','Generator','/generator',NULL,'/generator/gencode',0,1,0,'代码管理','null',0,NULL,5,'8c1085c1-8b43-4442-a319-bd1b50272a42','0','代码管理','2026-01-03 20:15:40','2026-01-03 20:15:40'),('接口管理',1,6,NULL,'document','Common','/common',NULL,'/common/docs',0,1,0,'接口管理','null',0,NULL,6,'6994bc7e-eacc-4ccd-908b-83c67616aac3','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('案例管理',1,7,NULL,'menu','Example','/example',NULL,'/example/demo',0,1,0,'案例管理','null',0,NULL,7,'5da39814-6873-48ec-8b36-da6042d06e3f','0','案例管理','2026-01-03 20:15:40','2026-01-03 20:15:40'),('工作台',2,1,'dashboard:workplace:query','el-icon-PieChart','Workplace','/dashboard/workplace','dashboard/workplace',NULL,0,1,0,'工作台','null',0,1,8,'ca9b78d3-05f8-4fe7-ada8-6b00b7c935c4','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('菜单管理',2,1,'module_system:menu:query','menu','Menu','/system/menu','module_system/menu/index',NULL,0,1,0,'菜单管理','null',0,2,9,'18f7afa0-cbb1-4952-8dab-025d9aac0a97','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('部门管理',2,2,'module_system:dept:query','tree','Dept','/system/dept','module_system/dept/index',NULL,0,1,0,'部门管理','null',0,2,10,'31c8381e-6195-4844-8c15-4f2898d0b981','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('岗位管理',2,3,'module_system:position:query','el-icon-Coordinate','Position','/system/position','module_system/position/index',NULL,0,1,0,'岗位管理','null',0,2,11,'387ae485-b8cd-4a73-83b8-1aa431a706eb','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('角色管理',2,4,'module_system:role:query','role','Role','/system/role','module_system/role/index',NULL,0,1,0,'角色管理','null',0,2,12,'02f3f896-5dee-4039-86e4-d40872b0774b','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('用户管理',2,5,'module_system:user:query','el-icon-User','User','/system/user','module_system/user/index',NULL,0,1,0,'用户管理','null',0,2,13,'5d7fffee-5972-478b-8d64-5c4fa5ec5cd9','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('日志管理',2,6,'module_system:log:query','el-icon-Aim','Log','/system/log','module_system/log/index',NULL,0,1,0,'日志管理','null',0,2,14,'b9545a78-7165-464b-bcd0-23c1f8464e5d','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('公告管理',2,7,'module_system:notice:query','bell','Notice','/system/notice','module_system/notice/index',NULL,0,1,0,'公告管理','null',0,2,15,'9e1a1629-5b45-4f50-8ccc-afe8db61d015','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('参数管理',2,8,'module_system:param:query','setting','Params','/system/param','module_system/param/index',NULL,0,1,0,'参数管理','null',0,2,16,'f37e7718-6b98-43d7-af8f-c863c4749a20','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('字典管理',2,9,'module_system:dict_type:query','dict','Dict','/system/dict','module_system/dict/index',NULL,0,1,0,'字典管理','null',0,2,17,'4379b2b9-c070-45cf-b4b2-0864324e6161','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('我的应用',2,1,'module_application:myapp:query','el-icon-ShoppingCartFull','MYAPP','/application/myapp','module_application/myapp/index',NULL,0,1,0,'我的应用','null',0,3,18,'1e4a5308-6e0d-4cb6-b099-100572b203a7','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('任务管理',2,2,'module_application:job:query','el-icon-DataLine','Job','/application/job','module_application/job/index',NULL,0,1,0,'任务管理','null',0,3,19,'fb8f7fc5-6fbf-4c03-91ff-20017d0757a4','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('AI智能助手',2,3,'module_application:ai:chat','el-icon-ToiletPaper','AI','/application/ai','module_application/ai/index',NULL,0,1,0,'AI智能助手','null',0,3,20,'800d1611-bc2b-46df-9878-7a8454c67d51','0','AI智能助手','2026-01-03 20:15:40','2026-01-03 20:15:40'),('流程管理',2,4,'module_application:workflow:query','el-icon-ShoppingBag','Workflow','/application/workflow','module_application/workflow/index',NULL,0,1,0,'我的流程','null',0,3,21,'85887c52-f2b1-40eb-96c8-4b50fdc4ac38','0','我的流程','2026-01-03 20:15:40','2026-01-03 20:15:40'),('在线用户',2,1,'module_monitor:online:query','el-icon-Headset','MonitorOnline','/monitor/online','module_monitor/online/index',NULL,0,1,0,'在线用户','null',0,4,22,'f0d77cc8-4b29-4b8a-83a0-c07f50104596','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('服务器监控',2,2,'module_monitor:server:query','el-icon-Odometer','MonitorServer','/monitor/server','module_monitor/server/index',NULL,0,1,0,'服务器监控','null',0,4,23,'d819eb52-36c8-4b87-bcc0-23a70cd00f78','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('缓存监控',2,3,'module_monitor:cache:query','el-icon-Stopwatch','MonitorCache','/monitor/cache','module_monitor/cache/index',NULL,0,1,0,'缓存监控','null',0,4,24,'dad0cf0b-33ef-42bc-8f79-cdc467b6845d','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('文件管理',2,4,'module_monitor:resource:query','el-icon-Files','Resource','/monitor/resource','module_monitor/resource/index',NULL,0,1,0,'文件管理','null',0,4,25,'89979d3f-5d2f-4b0a-81b0-bb2b1c74b50c','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('代码生成',2,1,'module_generator:gencode:query','code','GenCode','/generator/gencode','module_generator/gencode/index',NULL,0,1,0,'代码生成','null',0,5,26,'15b626e5-151d-443d-bdc5-dc6b4dff4da6','0','代码生成','2026-01-03 20:15:40','2026-01-03 20:15:40'),('Swagger文档',4,1,'module_common:docs:query','api','Docs','/common/docs','module_common/docs/index',NULL,0,1,0,'Swagger文档','null',0,6,27,'6a12698f-7fba-4b4e-850f-4b19db12ad74','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('Redoc文档',4,2,'module_common:redoc:query','el-icon-Document','Redoc','/common/redoc','module_common/redoc/index',NULL,0,1,0,'Redoc文档','null',0,6,28,'79750178-0a65-48fd-b775-8da287ccfee5','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('示例管理',2,1,'module_example:demo:query','menu','Demo','/example/demo','module_example/demo/index',NULL,0,1,0,'示例管理','null',0,7,29,'6628cf01-5efc-42bd-b5fd-6a7505bfc76a','0','示例管理','2026-01-03 20:15:40','2026-01-03 20:15:40'),('创建菜单',3,1,'module_system:menu:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建菜单','null',0,9,30,'47862c59-6fef-4e9e-84b7-c6e90243e486','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('修改菜单',3,2,'module_system:menu:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改菜单','null',0,9,31,'53a8a559-72bd-451d-98c1-8fa3dbec99fe','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('删除菜单',3,3,'module_system:menu:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除菜单','null',0,9,32,'aa59878c-68ac-44f8-9854-b1a3c8ba8295','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('批量修改菜单状态',3,4,'module_system:menu:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改菜单状态','null',0,9,33,'314f09ee-c734-416e-98c0-e11672388419','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('详情改菜',3,5,'module_system:menu:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情改菜','null',0,9,34,'94624520-2148-437b-8353-a791650beee7','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('查询菜单',3,6,'module_system:menu:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询菜单','null',0,9,35,'ae0f36d1-09b0-4142-a65f-14aeef82cbba','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('创建部门',3,1,'module_system:dept:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建部门','null',0,10,36,'e6082d5e-eea1-450b-a181-321896040785','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('修改部门',3,2,'module_system:dept:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改部门','null',0,10,37,'ae60f687-ba81-4859-944a-be0388e47dc0','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('删除部门',3,3,'module_system:dept:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除部门','null',0,10,38,'6e396a56-735d-43c6-b259-8505dc102210','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('批量修改部门状态',3,4,'module_system:dept:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改部门状态','null',0,10,39,'48dce68d-0d1e-4eb4-96e2-6691df9dfd87','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('详情部门',3,5,'module_system:dept:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情部门','null',0,10,40,'0cf88465-a6cc-4015-8a3d-a7cfd2337d74','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('查询部门',3,6,'module_system:dept:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询部门','null',0,10,41,'3d7ab65a-150b-49b9-9eaa-9b093ee1fe9b','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('创建岗位',3,1,'module_system:position:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建岗位','null',0,11,42,'9dafe232-089d-4b32-a419-dfb5faef3f0e','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('修改岗位',3,2,'module_system:position:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改岗位','null',0,11,43,'7aa63e69-6b07-4880-80aa-bfba5999e06a','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('删除岗位',3,3,'module_system:position:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改岗位','null',0,11,44,'e413a979-81f6-4619-960c-5abfb70d0e2c','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('批量修改岗位状态',3,4,'module_system:position:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改岗位状态','null',0,11,45,'97212313-5f3c-48b1-8c52-d78452880521','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('岗位导出',3,5,'module_system:position:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'岗位导出','null',0,11,46,'b5b51722-448b-4a88-8165-2caaa5ac527b','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('详情岗位',3,6,'module_system:position:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情岗位','null',0,11,47,'1134acaf-0b12-4f96-ad0a-ef8f238d722a','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('查询岗位',3,7,'module_system:position:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询岗位','null',0,11,48,'7cf2acae-a154-4aa9-80bf-6ee681006423','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('创建角色',3,1,'module_system:role:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建角色','null',0,12,49,'2f8063bb-dd5d-4439-9bd9-016cbcbdfd17','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('修改角色',3,2,'module_system:role:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改角色','null',0,12,50,'0c1afd4d-7ad6-4df8-bcc1-db4ab5b03ff9','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('删除角色',3,3,'module_system:role:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除角色','null',0,12,51,'4bea1760-b42c-451d-8c23-4d2b99a11f63','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('批量修改角色状态',3,4,'module_system:role:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改角色状态','null',0,12,52,'add80b1b-6a00-40ea-9088-ac8f77ac7cae','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('角色导出',3,5,'module_system:role:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'角色导出','null',0,12,53,'0ad7f1a3-9068-45dc-9d1a-95fcc43751b6','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('详情角色',3,6,'module_system:role:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情角色','null',0,12,54,'d0f92ba2-8482-4f48-b008-b29f6b4efc4e','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('查询角色',3,7,'module_system:role:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询角色','null',0,12,55,'37e16cb6-12a9-4f81-ae23-e035eb905cd4','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('创建用户',3,1,'module_system:user:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建用户','null',0,13,56,'316a2b7f-5570-4d27-b15a-0e898faa4c65','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('修改用户',3,2,'module_system:user:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改用户','null',0,13,57,'38ed04bf-e0d3-49a3-b989-3b901d0306ca','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('删除用户',3,3,'module_system:user:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除用户','null',0,13,58,'7a81183f-efa6-40cf-80ea-e35c5897b544','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('批量修改用户状态',3,4,'module_system:user:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改用户状态','null',0,13,59,'0374c345-551f-4d54-a8d1-dc933a0df6ab','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('导出用户',3,5,'module_system:user:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出用户','null',0,13,60,'370e1517-567e-4720-ab20-2ea9698ba967','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('导入用户',3,6,'module_system:user:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入用户','null',0,13,61,'2eb7f372-91a7-498b-9d63-83f50cdcae5b','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('下载用户导入模板',3,7,'module_system:user:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'下载用户导入模板','null',0,13,62,'28b4fb56-4c00-427c-be4f-bfe91baac3d4','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('详情用户',3,8,'module_system:user:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情用户','null',0,13,63,'d4c70e6f-9843-4cbb-bc1e-27125e45ba47','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('查询用户',3,9,'module_system:user:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询用户','null',0,13,64,'7fa25727-ac0f-456a-9e35-571fa816adce','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('日志删除',3,1,'module_system:log:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'日志删除','null',0,14,65,'f16ddf24-2f57-4927-a10e-bab6211e3383','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('日志导出',3,2,'module_system:log:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'日志导出','null',0,14,66,'696fade5-15a7-4d76-80c3-b5a4e48cb9b0','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('日志详情',3,3,'module_system:log:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'日志详情','null',0,14,67,'4e23594b-589f-44d1-8db7-fb301c28e0f7','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('查询日志',3,4,'module_system:log:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询日志','null',0,14,68,'769ec72d-8668-419d-9707-5566c1103454','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('公告创建',3,1,'module_system:notice:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告创建','null',0,15,69,'783afff0-8fd8-476d-85e4-0baff953d153','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('公告修改',3,2,'module_system:notice:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改用户','null',0,15,70,'509fbedd-db66-4bea-bb15-142b13a1a0cc','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('公告删除',3,3,'module_system:notice:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告删除','null',0,15,71,'3fd48660-a6be-41df-8d4a-d6df2deedb97','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('公告导出',3,4,'module_system:notice:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告导出','null',0,15,72,'cb7d6846-7f38-426d-b902-f860a97cf244','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('公告批量修改状态',3,5,'module_system:notice:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告批量修改状态','null',0,15,73,'9509cccc-9833-47c5-b53c-0727233a52fa','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('公告详情',3,6,'module_system:notice:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'公告详情','null',0,15,74,'14047ac2-d576-484a-9cae-674ac4fca0fa','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('查询公告',3,5,'module_system:notice:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询公告','null',0,15,75,'18101b02-45c3-4b20-bab6-9ce85efc52dc','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('创建参数',3,1,'module_system:param:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建参数','null',0,16,76,'c01a78e9-2ee6-4359-9d2d-e912655ee5c2','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('修改参数',3,2,'module_system:param:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改参数','null',0,16,77,'a73c8245-0c7c-4ea2-ab7c-c7c31fff52da','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('删除参数',3,3,'module_system:param:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除参数','null',0,16,78,'7b066411-073f-4e4f-a754-3ad8e0da6489','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('导出参数',3,4,'module_system:param:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出参数','null',0,16,79,'72c49289-b82b-4f91-97f5-7451022dc5ad','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('参数上传',3,5,'module_system:param:upload',NULL,NULL,NULL,NULL,NULL,0,1,0,'参数上传','null',0,16,80,'75bcfd6d-b99c-47fd-a85e-4fbec852e2b2','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('参数详情',3,6,'module_system:param:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'参数详情','null',0,16,81,'48f507e3-3439-425c-9a21-1b9b057e19d8','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('查询参数',3,7,'module_system:param:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询参数','null',0,16,82,'75528178-c64a-48fa-80e5-0c329371a978','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('创建字典类型',3,1,'module_system:dict_type:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建字典类型','null',0,17,83,'30a58b57-8fa0-4913-845b-bd8fc05ae132','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('修改字典类型',3,2,'module_system:dict_type:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改字典类型','null',0,17,84,'f01e1fb3-ab3c-47fe-aca3-da3b4189d02b','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('删除字典类型',3,3,'module_system:dict_type:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除字典类型','null',0,17,85,'c72c207c-19ca-477e-9ac6-28b7252d14bc','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('导出字典类型',3,4,'module_system:dict_type:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典类型','null',0,17,86,'5ddcd280-6b45-496b-b358-538b58126b74','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('批量修改字典状态',3,5,'module_system:dict_type:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典类型','null',0,17,87,'42d69567-3a63-4ed7-99a1-592c2c328045','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('字典数据查询',3,6,'module_system:dict_data:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'字典数据查询','null',0,17,88,'a017e99e-ead8-41c0-8eaa-232c100d36d1','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('创建字典数据',3,7,'module_system:dict_data:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建字典数据','null',0,17,89,'8969e135-4787-41a3-8cae-4fd49cfc49b9','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('修改字典数据',3,8,'module_system:dict_data:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改字典数据','null',0,17,90,'b9b7242e-bc87-45fb-8f43-60c93d632a47','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('删除字典数据',3,9,'module_system:dict_data:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除字典数据','null',0,17,91,'18052459-cd11-4a6c-8af1-76e4efae8225','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('导出字典数据',3,10,'module_system:dict_data:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典数据','null',0,17,92,'581d5104-a50f-498e-a7e6-f6801c97c965','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('批量修改字典数据状态',3,11,'module_system:dict_data:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改字典数据状态','null',0,17,93,'30f42b10-10b3-4c4a-aeb6-fd84eacba90b','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('详情字典类型',3,12,'module_system:dict_type:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情字典类型','null',0,17,94,'13326374-adca-4fcf-b725-08013e8644f9','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('查询字典类型',3,13,'module_system:dict_type:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询字典类型','null',0,17,95,'752593ea-d769-4c71-88fe-bef629acba9c','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('详情字典数据',3,14,'module_system:dict_data:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情字典数据','null',0,17,96,'b6e8f504-11c1-4ba7-8c64-f4446f958e26','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('创建应用',3,1,'module_application:myapp:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建应用','null',0,18,97,'91cb1744-65ca-415c-b85a-b176f77473be','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('修改应用',3,2,'module_application:myapp:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改应用','null',0,18,98,'e7b80cc7-9f9d-4580-be2b-cda26642c300','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('删除应用',3,3,'module_application:myapp:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除应用','null',0,18,99,'2b955ecc-80af-4a4a-9554-b33d01da8788','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('批量修改应用状态',3,4,'module_application:myapp:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改应用状态','null',0,18,100,'897e06b4-cf07-4432-9770-da926272a518','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('详情应用',3,5,'module_application:myapp:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情应用','null',0,18,101,'37983db4-d172-4621-ab01-5ab18e3a5794','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('查询应用',3,6,'module_application:myapp:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询应用','null',0,18,102,'3fced896-d9fc-4cd4-9875-1861c784a239','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('创建任务',3,1,'module_application:job:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建任务','null',0,19,103,'589bf53a-4b80-4446-9f92-f27d72cddef9','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('修改和操作任务',3,2,'module_application:job:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'修改和操作任务','null',0,19,104,'71f748e4-8f6e-4e5b-94cb-41984e09d1f5','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('删除和清除任务',3,3,'module_application:job:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除和清除任务','null',0,19,105,'7c323e09-76f6-4bd8-a6c0-644d35b94693','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('导出定时任务',3,4,'module_application:job:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出定时任务','null',0,19,106,'dad17cfc-19ca-472e-9b58-25d0e06f4057','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('详情定时任务',3,5,'module_application:job:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情任务','null',0,19,107,'680439b9-2190-4dda-8b87-4fe0bece8919','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('查询定时任务',3,6,'module_application:job:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询定时任务','null',0,19,108,'bd3736e5-8c25-4858-891b-0fa9e8ee6bcb','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('智能对话',3,1,'module_application:ai:chat',NULL,NULL,NULL,NULL,NULL,0,1,0,'智能对话','null',0,20,109,'40841301-1361-4c5f-af5b-9fafc92d498a','0','智能对话','2026-01-03 20:15:40','2026-01-03 20:15:40'),('在线用户强制下线',3,1,'module_monitor:online:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'在线用户强制下线','null',0,22,110,'b86c973c-6554-44fe-a8f9-3547b4e4c51d','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('清除缓存',3,1,'module_monitor:cache:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'清除缓存','null',0,24,111,'a035a875-d730-422e-80de-37aec6c1a49c','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('文件上传',3,1,'module_monitor:resource:upload',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件上传','null',0,25,112,'db1d5cb3-b839-4d4b-b8ea-7cd76514ef8c','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('文件下载',3,2,'module_monitor:resource:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件下载','null',0,25,113,'076370a2-2ff2-4a46-b01f-8f1aac0d4b71','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('文件删除',3,3,'module_monitor:resource:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件删除','null',0,25,114,'1de098f5-a21c-43fa-b825-8f8abf48ae92','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('文件移动',3,4,'module_monitor:resource:move',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件移动','null',0,25,115,'1f7ee57a-b1ea-4513-8cec-0deef018a787','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('文件复制',3,5,'module_monitor:resource:copy',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件复制','null',0,25,116,'53547c60-b049-413b-909b-02f340b78066','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('文件重命名',3,6,'module_monitor:resource:rename',NULL,NULL,NULL,NULL,NULL,0,1,0,'文件重命名','null',0,25,117,'9ae32f22-be06-4753-a878-19321751fe27','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('创建目录',3,7,'module_monitor:resource:create_dir',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建目录','null',0,25,118,'92d91df4-1d57-4e84-9e51-a4eafad23bbd','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('导出文件列表',3,9,'module_monitor:resource:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出文件列表','null',0,25,119,'f6a748db-ba49-41da-afe9-18720604e037','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('查询代码生成业务表列表',3,1,'module_generator:gencode:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询代码生成业务表列表','null',0,26,120,'7c169e8a-dd9c-4955-9722-c3ca05d5c908','0','查询代码生成业务表列表','2026-01-03 20:15:40','2026-01-03 20:15:40'),('创建表结构',3,2,'module_generator:gencode:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建表结构','null',0,26,121,'ddf13f80-8178-4133-926e-51d148f9300d','0','创建表结构','2026-01-03 20:15:40','2026-01-03 20:15:40'),('编辑业务表信息',3,3,'module_generator:gencode:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'编辑业务表信息','null',0,26,122,'2bc87149-640c-40a4-85bc-2c9486b5f5bd','0','编辑业务表信息','2026-01-03 20:15:40','2026-01-03 20:15:40'),('删除业务表信息',3,4,'module_generator:gencode:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除业务表信息','null',0,26,123,'9590e6a5-83fb-47fe-ad10-5d71f67ee56d','0','删除业务表信息','2026-01-03 20:15:40','2026-01-03 20:15:40'),('导入表结构',3,5,'module_generator:gencode:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入表结构','null',0,26,124,'10d28c8d-f0c9-4e4f-85f2-ea9a0aa36127','0','导入表结构','2026-01-03 20:15:40','2026-01-03 20:15:40'),('批量生成代码',3,6,'module_generator:gencode:operate',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量生成代码','null',0,26,125,'1e42140f-53ce-4d27-aefe-352c5cbb3140','0','批量生成代码','2026-01-03 20:15:40','2026-01-03 20:15:40'),('生成代码到指定路径',3,7,'module_generator:gencode:code',NULL,NULL,NULL,NULL,NULL,0,1,0,'生成代码到指定路径','null',0,26,126,'b57a92e7-1715-4541-85b0-8514c04103b1','0','生成代码到指定路径','2026-01-03 20:15:40','2026-01-03 20:15:40'),('查询数据库表列表',3,8,'module_generator:dblist:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询数据库表列表','null',0,26,127,'5686315b-843f-4bdd-b85f-ee48b68d5c06','0','查询数据库表列表','2026-01-03 20:15:40','2026-01-03 20:15:40'),('同步数据库',3,9,'module_generator:db:sync',NULL,NULL,NULL,NULL,NULL,0,1,0,'同步数据库','null',0,26,128,'09c5ab99-cce1-4086-ab11-5c8677ac05d5','0','同步数据库','2026-01-03 20:15:40','2026-01-03 20:15:40'),('创建示例',3,1,'module_example:demo:create',NULL,NULL,NULL,NULL,NULL,0,1,0,'创建示例','null',0,29,129,'240b81f0-cea2-4991-a20c-9b8660bcc062','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('更新示例',3,2,'module_example:demo:update',NULL,NULL,NULL,NULL,NULL,0,1,0,'更新示例','null',0,29,130,'ed418b6a-d70f-429f-8aa1-482f82996557','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('删除示例',3,3,'module_example:demo:delete',NULL,NULL,NULL,NULL,NULL,0,1,0,'删除示例','null',0,29,131,'02ff30ca-80d2-48e7-b150-bc44e449e761','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('批量修改示例状态',3,4,'module_example:demo:patch',NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改示例状态','null',0,29,132,'444ed212-729e-4651-9751-30fa4b9fdb94','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('导出示例',3,5,'module_example:demo:export',NULL,NULL,NULL,NULL,NULL,0,1,0,'导出示例','null',0,29,133,'a61b99e3-d0f9-435a-a1a4-9a0a86991f72','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('导入示例',3,6,'module_example:demo:import',NULL,NULL,NULL,NULL,NULL,0,1,0,'导入示例','null',0,29,134,'b4693ca0-d8a6-46b1-a6d3-b0c2e3aa82cd','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('下载导入示例模版',3,7,'module_example:demo:download',NULL,NULL,NULL,NULL,NULL,0,1,0,'下载导入示例模版','null',0,29,135,'4f57c2dc-d4a6-48c9-984a-45805713c138','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('详情示例',3,8,'module_example:demo:detail',NULL,NULL,NULL,NULL,NULL,0,1,0,'详情示例','null',0,29,136,'46bdd3ae-ddac-4685-9264-5c039dd5958f','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('查询示例',3,9,'module_example:demo:query',NULL,NULL,NULL,NULL,NULL,0,1,0,'查询示例','null',0,29,137,'52ef488f-6a6a-4d84-abd7-ff13da9f5e84','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40');
/*!40000 ALTER TABLE `sys_menu` ENABLE KEYS */;

--
-- Table structure for table `sys_notice`
--

DROP TABLE IF EXISTS `sys_notice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_notice` (
  `notice_title` varchar(64) NOT NULL COMMENT '公告标题',
  `notice_type` varchar(1) NOT NULL COMMENT '公告类型(1通知 2公告)',
  `notice_content` text COMMENT '公告内容',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_notice_uuid` (`uuid`),
  KEY `ix_sys_notice_created_time` (`created_time`),
  KEY `ix_sys_notice_updated_time` (`updated_time`),
  KEY `ix_sys_notice_created_id` (`created_id`),
  KEY `ix_sys_notice_id` (`id`),
  KEY `ix_sys_notice_status` (`status`),
  KEY `ix_sys_notice_updated_id` (`updated_id`),
  CONSTRAINT `sys_notice_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_notice_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='通知公告表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_notice`
--

/*!40000 ALTER TABLE `sys_notice` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_notice` ENABLE KEYS */;

--
-- Table structure for table `sys_param`
--

DROP TABLE IF EXISTS `sys_param`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_param` (
  `config_name` varchar(64) NOT NULL COMMENT '参数名称',
  `config_key` varchar(500) NOT NULL COMMENT '参数键名',
  `config_value` varchar(500) DEFAULT NULL COMMENT '参数键值',
  `config_type` tinyint(1) DEFAULT NULL COMMENT '系统内置(True:是 False:否)',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_param_uuid` (`uuid`),
  KEY `ix_sys_param_id` (`id`),
  KEY `ix_sys_param_created_time` (`created_time`),
  KEY `ix_sys_param_updated_time` (`updated_time`),
  KEY `ix_sys_param_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='系统参数表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_param`
--

/*!40000 ALTER TABLE `sys_param` DISABLE KEYS */;
INSERT INTO `sys_param` VALUES ('网站名称','sys_web_title','FastApiAdmin',1,1,'f8821461-4cf7-4a82-adf7-b770d08845ac','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('网站描述','sys_web_description','FastApiAdmin 是完全开源的权限管理系统',1,2,'ff33eab0-fdfa-48e5-9c74-fc58d222d8f5','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('网页图标','sys_web_favicon','https://service.fastapiadmin.com/api/v1/static/image/favicon.png',1,3,'9457e932-11f7-4934-a0dd-afde24442bc4','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('网站Logo','sys_web_logo','https://service.fastapiadmin.com/api/v1/static/image/logo.png',1,4,'a44f8d04-cf77-4116-8d85-421467f4c4c9','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('登录背景','sys_login_background','https://service.fastapiadmin.com/api/v1/static/image/background.svg',1,5,'4516b274-d45a-4d84-a9c7-07aaff32af1c','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('版权信息','sys_web_copyright','Copyright © 2025-2026 service.fastapiadmin.com 版权所有',1,6,'e6d2ecaf-0aef-46bd-a780-454212c4310e','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('备案信息','sys_keep_record','陕ICP备2025069493号-1',1,7,'5a7f0bdc-6c7d-4e22-8885-b69ad1c18a8a','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('帮助文档','sys_help_doc','https://service.fastapiadmin.com',1,8,'7a4ab36e-2b0b-426f-a973-7a0f54e987f9','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('隐私政策','sys_web_privacy','https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE',1,9,'c4d0d089-7e7a-40d5-828d-e7d0798fbff6','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('用户协议','sys_web_clause','https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE',1,10,'0f9891e2-c044-4195-8414-dd2520595a92','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('源码代码','sys_git_code','https://github.com/fastapiadmin/FastapiAdmin.git',1,11,'16a0c6cf-3e54-414c-ba7d-761d074ffb99','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('项目版本','sys_web_version','2.0.0',1,12,'ed3e3c09-927a-4298-9594-7369ab348bfa','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('演示模式启用','demo_enable','false',1,13,'e0305279-8e92-48c8-849d-28df2956ae56','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('演示访问IP白名单','ip_white_list','[\"127.0.0.1\"]',1,14,'5ee61c8b-6e96-4414-9792-98ad92898798','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('接口白名单','white_api_list_path','[\"/api/v1/system/auth/login\", \"/api/v1/system/auth/token/refresh\", \"/api/v1/system/auth/captcha/get\", \"/api/v1/system/auth/logout\", \"/api/v1/system/config/info\", \"/api/v1/system/user/current/info\", \"/api/v1/system/notice/available\"]',1,15,'f51f0052-3629-432d-87a8-bb821f443894','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40'),('访问IP黑名单','ip_black_list','[]',1,16,'c7cfa114-6a19-4be0-8c44-f75522069349','0','初始化数据','2026-01-03 20:15:40','2026-01-03 20:15:40');
/*!40000 ALTER TABLE `sys_param` ENABLE KEYS */;

--
-- Table structure for table `sys_position`
--

DROP TABLE IF EXISTS `sys_position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_position` (
  `name` varchar(64) NOT NULL COMMENT '岗位名称',
  `order` int NOT NULL COMMENT '显示排序',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_position_uuid` (`uuid`),
  KEY `ix_sys_position_updated_time` (`updated_time`),
  KEY `ix_sys_position_created_id` (`created_id`),
  KEY `ix_sys_position_id` (`id`),
  KEY `ix_sys_position_status` (`status`),
  KEY `ix_sys_position_updated_id` (`updated_id`),
  KEY `ix_sys_position_created_time` (`created_time`),
  CONSTRAINT `sys_position_ibfk_1` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_position_ibfk_2` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='岗位表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_position`
--

/*!40000 ALTER TABLE `sys_position` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_position` ENABLE KEYS */;

--
-- Table structure for table `sys_role`
--

DROP TABLE IF EXISTS `sys_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_role` (
  `name` varchar(64) NOT NULL COMMENT '角色名称',
  `code` varchar(16) DEFAULT NULL COMMENT '角色编码',
  `order` int NOT NULL COMMENT '显示排序',
  `data_scope` int NOT NULL COMMENT '数据权限范围(1:仅本人 2:本部门 3:本部门及以下 4:全部 5:自定义)',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_role_uuid` (`uuid`),
  KEY `ix_sys_role_id` (`id`),
  KEY `ix_sys_role_status` (`status`),
  KEY `ix_sys_role_updated_time` (`updated_time`),
  KEY `ix_sys_role_code` (`code`),
  KEY `ix_sys_role_created_time` (`created_time`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='角色表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_role`
--

/*!40000 ALTER TABLE `sys_role` DISABLE KEYS */;
INSERT INTO `sys_role` VALUES ('管理员角色','ADMIN',1,4,1,'b5153b2b-7eb4-4332-bcc6-8a93a1de0a53','0','初始化角色','2026-01-03 20:15:40','2026-01-03 20:15:40');
/*!40000 ALTER TABLE `sys_role` ENABLE KEYS */;

--
-- Table structure for table `sys_role_depts`
--

DROP TABLE IF EXISTS `sys_role_depts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_role_depts` (
  `role_id` int NOT NULL COMMENT '角色ID',
  `dept_id` int NOT NULL COMMENT '部门ID',
  PRIMARY KEY (`role_id`,`dept_id`),
  KEY `dept_id` (`dept_id`),
  CONSTRAINT `sys_role_depts_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sys_role_depts_ibfk_2` FOREIGN KEY (`dept_id`) REFERENCES `sys_dept` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='角色部门关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_role_depts`
--

/*!40000 ALTER TABLE `sys_role_depts` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_role_depts` ENABLE KEYS */;

--
-- Table structure for table `sys_role_menus`
--

DROP TABLE IF EXISTS `sys_role_menus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_role_menus` (
  `role_id` int NOT NULL COMMENT '角色ID',
  `menu_id` int NOT NULL COMMENT '菜单ID',
  PRIMARY KEY (`role_id`,`menu_id`),
  KEY `menu_id` (`menu_id`),
  CONSTRAINT `sys_role_menus_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sys_role_menus_ibfk_2` FOREIGN KEY (`menu_id`) REFERENCES `sys_menu` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='角色菜单关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_role_menus`
--

/*!40000 ALTER TABLE `sys_role_menus` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_role_menus` ENABLE KEYS */;

--
-- Table structure for table `sys_user`
--

DROP TABLE IF EXISTS `sys_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_user` (
  `username` varchar(64) NOT NULL COMMENT '用户名/登录账号',
  `password` varchar(255) NOT NULL COMMENT '密码哈希',
  `name` varchar(32) NOT NULL COMMENT '昵称',
  `mobile` varchar(11) DEFAULT NULL COMMENT '手机号',
  `email` varchar(64) DEFAULT NULL COMMENT '邮箱',
  `gender` varchar(1) DEFAULT NULL COMMENT '性别(0:男 1:女 2:未知)',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像URL地址',
  `is_superuser` tinyint(1) NOT NULL COMMENT '是否超管',
  `last_login` datetime DEFAULT NULL COMMENT '最后登录时间',
  `gitee_login` varchar(32) DEFAULT NULL COMMENT 'Gitee登录',
  `github_login` varchar(32) DEFAULT NULL COMMENT 'Github登录',
  `wx_login` varchar(32) DEFAULT NULL COMMENT '微信登录',
  `qq_login` varchar(32) DEFAULT NULL COMMENT 'QQ登录',
  `dept_id` int DEFAULT NULL COMMENT '部门ID',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `uuid` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
  `status` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
  `description` text COMMENT '备注/描述',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_time` datetime NOT NULL COMMENT '更新时间',
  `created_id` int DEFAULT NULL COMMENT '创建人ID',
  `updated_id` int DEFAULT NULL COMMENT '更新人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `ix_sys_user_uuid` (`uuid`),
  UNIQUE KEY `mobile` (`mobile`),
  UNIQUE KEY `email` (`email`),
  KEY `ix_sys_user_dept_id` (`dept_id`),
  KEY `ix_sys_user_id` (`id`),
  KEY `ix_sys_user_status` (`status`),
  KEY `ix_sys_user_created_id` (`created_id`),
  KEY `ix_sys_user_created_time` (`created_time`),
  KEY `ix_sys_user_updated_id` (`updated_id`),
  KEY `ix_sys_user_updated_time` (`updated_time`),
  CONSTRAINT `sys_user_ibfk_1` FOREIGN KEY (`updated_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_user_ibfk_2` FOREIGN KEY (`dept_id`) REFERENCES `sys_dept` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `sys_user_ibfk_3` FOREIGN KEY (`created_id`) REFERENCES `sys_user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user`
--

/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
INSERT INTO `sys_user` VALUES ('admin','$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa','超级管理员',NULL,NULL,'0','https://service.fastapiadmin.com/api/v1/static/image/avatar.png',1,NULL,NULL,NULL,NULL,NULL,1,1,'e5d8aae9-8f73-4d99-8e4e-19ef8c1df901','0','超级管理员','2026-01-03 20:15:40','2026-01-03 20:15:40',NULL,NULL);
/*!40000 ALTER TABLE `sys_user` ENABLE KEYS */;

--
-- Table structure for table `sys_user_positions`
--

DROP TABLE IF EXISTS `sys_user_positions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_user_positions` (
  `user_id` int NOT NULL COMMENT '用户ID',
  `position_id` int NOT NULL COMMENT '岗位ID',
  PRIMARY KEY (`user_id`,`position_id`),
  KEY `position_id` (`position_id`),
  CONSTRAINT `sys_user_positions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sys_user_positions_ibfk_2` FOREIGN KEY (`position_id`) REFERENCES `sys_position` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户岗位关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user_positions`
--

/*!40000 ALTER TABLE `sys_user_positions` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_user_positions` ENABLE KEYS */;

--
-- Table structure for table `sys_user_roles`
--

DROP TABLE IF EXISTS `sys_user_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_user_roles` (
  `user_id` int NOT NULL COMMENT '用户ID',
  `role_id` int NOT NULL COMMENT '角色ID',
  PRIMARY KEY (`user_id`,`role_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `sys_user_roles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sys_user_roles_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户角色关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user_roles`
--

/*!40000 ALTER TABLE `sys_user_roles` DISABLE KEYS */;
INSERT INTO `sys_user_roles` VALUES (1,1);
/*!40000 ALTER TABLE `sys_user_roles` ENABLE KEYS */;

--
-- Dumping routines for database 'fastapiadmin'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-03 20:15:51
