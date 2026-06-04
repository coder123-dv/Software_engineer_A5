# 🏛️ 景区导览服务AI数字人

> 第十五届中国软件杯大赛 A5赛题 — 基于AI大模型的智慧景区3D数字人导览系统

## 📖 项目简介

本系统是一个面向智慧景区的AI数字人导览服务平台，结合3D虚拟形象、大模型对话、语音交互和知识库检索增强（RAG），为游客提供7×24小时智能导游服务，同时为景区管理者提供运营数据分析工具。

### 核心特色

- 🤖 **3D数字人** — 基于Three.js + VRM模型，具备口型同步和表情驱动能力
- 💬 **智能问答** — RAG知识库检索增强，事实性问答准确率≥90%
- 🎙️ **多模态交互** — 支持语音/文本双通道输入，数字人语音播报回复
- 📊 **管理后台** — 知识库管理、数字人配置、游客情感分析、数据大屏
- 🐳 **一键部署** — Docker Compose 容器化部署

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                     前端 (Vue 3 + Vite)                      │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌─────────┐  │
│  │ Three.js  │  │ 对话面板  │  │ 管理后台  │  │ 数据大屏│  │
│  │ VRM数字人 │  │ 语音录制  │  │ 知识库    │  │ ECharts │  │
│  └───────────┘  └───────────┘  └───────────┘  └─────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/SSE
┌──────────────────────────┴──────────────────────────────────┐
│                   后端 (FastAPI)                              │
│  ┌─────────┐  ┌─────────┐  ┌──────────┐  ┌─────────────┐  │
│  │ 对话API │  │ RAG引擎 │  │ Viseme   │  │ 情感分析    │  │
│  │ SSE流式 │  │ 混合检索│  │ 口型生成 │  │ 词典+规则   │  │
│  └─────────┘  └─────────┘  └──────────┘  └─────────────┘  │
│  ┌─────────┐  ┌─────────┐  ┌──────────┐                    │
│  │ LLM服务 │  │ TTS/ASR │  │ 知识管理 │                    │
│  │ OpenAI  │  │ API调用 │  │ CRUD     │                    │
│  └─────────┘  └─────────┘  └──────────┘                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                   数据层 (SQLite)                             │
│  知识文档 │ 向量索引 │ 对话记录 │ 游客画像 │ 统计数据      │
└─────────────────────────────────────────────────────────────┘
```

## 📁 项目结构

```
software_A5/
├── backend/                 # FastAPI 后端服务
│   ├── app/
│   │   ├── api/            # API路由 (chat/voice/knowledge/auth/analytics)
│   │   ├── models/         # SQLAlchemy ORM模型
│   │   ├── services/       # 业务逻辑 (LLM/RAG/TTS/ASR/情感分析)
│   │   ├── rag/            # RAG引擎 (索引/检索/向量存储)
│   │   ├── schemas/        # Pydantic数据模型
│   │   └── utils/          # 工具函数 (文档解析)
│   ├── storage/            # SQLite数据库 + 上传文件
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/                # Vue 3 前端
│   ├── src/
│   │   ├── views/          # 页面 (游客端 + 管理后台)
│   │   ├── components/     # 组件 (3D数字人/对话/后台)
│   │   ├── api/            # API调用层
│   │   └── router/         # Vue Router路由
│   ├── Dockerfile
│   └── nginx.conf
├── data/                    # 测试数据 (灵山胜境资料包)
├── docker-compose.yml       # Docker编排
├── .env.example             # 环境变量模板
└── README.md
```

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (部署用)

### 方式一: Docker 一键部署 (推荐)

```bash
# 1. 克隆项目
git clone <repo-url>
cd software_A5

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 AI 模型 API Key

# 3. 启动服务
docker-compose up --build -d

# 4. 访问
# 游客端: http://localhost
# 管理后台: http://localhost/admin  (账号: admin / admin123)
# API文档: http://localhost:8000/docs (后端直连时)
```

### 方式二: 本地开发

```bash
# === 后端 ===
cd backend

# 安装依赖 (使用 uv)
uv sync

# 配置环境变量
cp ../.env.example ../.env
# 编辑 ../.env 填入 API Key

# 启动后端
uv run uvicorn app.main:app --reload --port 8000

# === 前端 (新终端) ===
cd frontend

# 安装依赖
npm install

# 启动前端
npm run dev
# 访问 http://localhost:5173
```

## ⚙️ 配置说明

在 `.env` 文件中配置以下参数：

| 变量 | 说明 | 示例 |
|------|------|------|
| `LLM_BASE_URL` | 大模型API地址 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| `LLM_API_KEY` | 大模型API密钥 | `sk-xxx` |
| `LLM_MODEL` | 模型名称 | `qwen-turbo` / `glm-4` / `deepseek-chat` |
| `EMBEDDING_BASE_URL` | 向量模型地址 | 同LLM或单独配置 |
| `EMBEDDING_API_KEY` | 向量模型密钥 | `sk-xxx` |
| `TTS_BASE_URL` | TTS服务地址 | 留空则关闭语音 |
| `ASR_BASE_URL` | ASR服务地址 | 留空则关闭语音 |
| `SECRET_KEY` | JWT密钥 | 随机字符串 |

### 支持的AI模型 (OpenAI兼容接口)

- **通义千问** (阿里云): `https://dashscope.aliyuncs.com/compatible-mode/v1`
- **智谱GLM** (智谱AI): `https://open.bigmodel.cn/api/paas/v4`
- **DeepSeek**: `https://api.deepseek.com/v1`
- **OpenAI**: `https://api.openai.com/v1`

## 📋 功能清单

### 游客交互端 ✅

- [x] 文本对话 — 输入问题获取AI回复
- [x] 智能问答 — 基于RAG的知识库检索增强
- [x] 3D数字人 — VRM模型加载与展示
- [x] 口型同步 — 基于拼音的Viseme时间轴生成
- [x] 表情驱动 — 情感自适应表情切换
- [x] 语音交互 — ASR/TTS接口预留
- [x] 个性化推荐 — 兴趣偏好路线推荐

### 管理后台 ✅

- [x] 登录认证 — JWT Token
- [x] 知识库管理 — 上传/编辑/删除文档，自动分块索引
- [x] 数字人配置 — 人设/声音/外观参数调节
- [x] 数据大屏 — 服务人次/满意度/热门问答统计
- [x] 感受度报告 — 情感分布分析与AI建议

## 🔧 核心技术

| 模块 | 技术方案 |
|------|---------|
| 3D数字人 | Three.js + @pixiv/three-vrm，VRM标准模型 |
| 口型同步 | pypinyin→Viseme映射，15种口型BlendShape驱动 |
| RAG引擎 | 向量检索(sqlite-vec) + BM25关键词，RRF融合排序 |
| 大模型 | OpenAI兼容接口，支持流式输出 |
| 情感分析 | 中文情感词典 + 规则判断 |
| 数据存储 | SQLite + SQLAlchemy异步ORM |

## 📝 API 文档

启动后端后访问 `http://localhost:8000/docs` 查看完整Swagger文档。

核心接口：

```
POST /api/chat          # 文本对话
POST /api/voice/asr     # 语音识别
POST /api/voice/tts     # 语音合成
GET  /api/knowledge     # 知识库列表
POST /api/knowledge/upload  # 上传文档
POST /api/recommend     # 路线推荐
GET  /api/analytics/dashboard  # 数据大屏
POST /api/auth/login    # 管理员登录
```

## 🧪 测试数据

项目包含灵山胜境景区的公开资料作为测试知识库：

- `灵山胜境 景点结构化数据集.docx` — 景点结构化信息
- `灵山胜境：历史、文化、景点特色与个性化游览指南.docx` — 文史讲解资料
- `景点景区旅游数据行为分析数据.xlsx` — 游客行为分析数据

首次启动后，可通过管理后台"知识库管理"上传这些文档以构建知识库。

## 👥 团队信息

第十五届中国软件杯大赛参赛作品

## 📄 License

MIT
