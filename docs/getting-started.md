# 🚀 项目快速开始指南

本文档提供了项目后端 (`\backend`) 和前端 (`\factory`) 的快速启动步骤，帮助开发者在本地快速搭建开发环境。

推荐参考：

- [FastapiAdmin](https://github.com/fastapiadmin/FastapiAdmin)

---

## 🛠️ 1. 环境准备要求

在开始之前，请确保您的开发环境已安装以下基础软件：

- **Node.js**: 18.x 或更高版本 (用于前端项目)
- **Python**: 3.10 或更高版本 (用于后端项目)
- **Redis**: 6.0+ (用于后端项目)
- **数据库**: MySQL 8.0+ / PostgreSQL 13+ / SQLite 3.x (后端数据库)
- **包管理工具**: 
  - 前端：推荐使用 `pnpm` 
  - 后端：推荐使用 `uv` 

---

## 🖥️ 2. 后端项目 (`\backend`)

后端项目是一个基于 **FastAPI + SQLAlchemy 2.0 + Pydantic 2.x** 构建的企业级服务。

### 2.1 创建虚拟环境并安装依赖

进入后端目录：
```bash
cd backend
```

> 需要修改 `backend/env` 目录下的 `.env.dev.example` 文件为 `.env.dev`，修改 `backend/env` 目录下的 `.env.prod.example` 文件为 `.env.prod`，然后根据实际情况修改数据库连接信息、Redis连接信息等。

**方式一：使用标准的 Python venv 和 pip (推荐新手)**
```bash
# 1. 创建虚拟环境
python -m venv .venv

# 2. 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
```

**方式二：使用高性能的 uv 工具 (推荐)**
```bash
# 1. 创建虚拟环境 (默认创建 .venv)
uv venv

# 2. 同步并安装依赖
uv sync
# 或者使用 uv add -r requirements.txt
```

### 2.2 数据库初始化与迁移

在启动服务前，需要初始化数据库表结构（默认使用 dev 环境配置）：

```bash
# 生成迁移文件（首次初始化或模型变更时执行）
python main.py revision

# 应用数据库迁移（同步表结构到数据库）
python main.py upgrade
```
*(注：如果使用 `uv`，在命令前加上 `uv run`，例如：`uv run main.py upgrade`)*

### 2.3 启动后端服务

启动开发环境服务：
```bash
# 默认以 dev 环境启动
python main.py run
# 或者显式指定环境
python main.py run --env=dev
```
*(注：如果使用 `uv`，命令为 `uv run main.py run`)*

启动成功后，通常可以通过 `http://127.0.0.1:8000/docs` 访问 Swagger API 接口文档。

---

## 🎨 3. 前端项目 (`\factory`)

前端项目是一个基于 **Vue 3 + Vite + TypeScript + Pinia** 构建的智能体管理系统。

### 3.1 安装依赖

> 需要修改 `factory` 目录下的 `.env.development.example` 文件为 `.env.development`，然后根据实际情况修改接口地址等。

进入前端目录并安装依赖：
```bash
cd factory

# 或者使用 pnpm (推荐)
pnpm install

```

### 3.2 启动开发服务

安装完成后，启动 Vite 本地开发服务器：
```bash
npm run dev
# 或 pnpm dev / yarn dev
```
启动成功后，控制台会输出本地访问地址，点击即可在浏览器中访问前端系统。