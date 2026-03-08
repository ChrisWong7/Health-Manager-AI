# Health Management System (AI个人健康信息管理助手)

基于 V1.0 架构设计文档构建的 MVP 项目。

## 目录结构
*   `docs/`: 架构设计文档
*   `backend/`: Python (FastAPI) 后端服务
*   `frontend/`: React 前端 (MVP版，无Node.js依赖)

## 快速开始

### 1. 启动服务 (推荐方式)
现在后端已集成前端服务，只需启动后端即可：

```bash
cd backend
pip install -r requirements.txt
python main.py
```
访问地址: `http://localhost:8000/static/index.html`

### 2. 部署到云端 (Render / Railway)
本项目已配置好一键部署文件：
- `render.yaml`: 用于 Render 平台。
- `Dockerfile`: 用于支持 Docker 的容器平台。

**部署步骤：**
1. 将代码推送到 GitHub。
2. 在 Render 仪表盘选择 "Blueprint"，关联此仓库。
3. **重要**：在环境变量中设置 `LLM_API_KEY`。

## 功能进度 (MVP)
- [x] 项目架构文档
- [x] 后端基础框架 (FastAPI + CORS + Static Files)
- [x] 前端基础页面 (React + Tailwind CSS)
- [x] 智能查询接口 (RAG流程 + Streaming)
- [x] 轻量级向量检索 (SimpleVectorStore)
- [x] 部署配置文件 (Docker & Render)
