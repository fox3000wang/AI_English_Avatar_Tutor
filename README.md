# AI_English_Avatar_Tutor

## 一、项目目标

本项目是一个面向 9 岁儿童的 AI 英语口语外教系统。

核心目标：

- iPad 打开网页即可使用
- AI老师通过语音与孩子互动
- 支持课程模式 + 自由聊天模式
- 家长可以在后台管理课程与学习记录

---

## 二、核心功能

### 1. 学生端（iPad）

- 点击开始上课
- 语音对话（ASR → LLM → TTS）
- AI英语老师互动（简单句、鼓励、纠错）
- 支持主题：科技 / 历史 / 文化 / 动物
- 显示 2D 数字人（Live2D）
- 自动保存对话记录

---

### 2. 家长后台

- 创建课程
- 排课
- 设置学习主题与难度
- 查看学习记录
- 查看AI生成的学习总结
- 查看孩子常见错误

---

### 3. 系统能力

- 实时语音交互
- 对话记忆（session级）
- 基础长期记忆（孩子画像）
- 安全控制（儿童模式）

---

## 三、技术架构

### 前端

- Next.js (App Router)
- React + TypeScript
- Tailwind CSS
- Live2D Web SDK

### 后端

- FastAPI（Python 3.11+）
- REST API

### AI能力

- ASR：Whisper API（或预留本地替换接口）
- LLM：OpenAI API（支持替换）
- TTS：OpenAI （可替换）

### 数据库

- PostgreSQL
- Redis（缓存 / session）

### 存储

- MinIO / S3（音频文件）

### 部署

- Docker + Docker Compose
- Nginx（反向代理）

---

## 四、项目结构（必须遵守）

project-root/
│
├── frontend/ # 前端项目（Next.js）
│ ├── app/
│ ├── components/
│ ├── hooks/
│ ├── services/
│ ├── types/
│ └── tests/
│
├── backend/ # 后端项目（FastAPI）
│ ├── app/
│ │ ├── api/
│ │ ├── core/
│ │ ├── services/
│ │ ├── models/
│ │ ├── schemas/
│ │ └── utils/
│ │
│ ├── tests/
│ └── main.py
│
├── infra/ # 部署相关
│ ├── docker/
│ ├── nginx/
│ └── docker-compose.yml
│
├── docs/ # 项目文档
│
└── README.md

---

## 五、开发规范（必须执行）

### 1. 前后端分离

- 前端与后端必须完全独立
- 通过 REST API 通信
- 不允许直接耦合

---

### 2. 代码规范

#### 前端

- 使用 TypeScript
- 所有组件必须类型定义
- 使用函数组件（禁止 class component）
- hooks 必须抽离到 `/hooks`
- API 请求统一在 `/services`

#### 后端

- 使用 FastAPI
- 使用 Pydantic 做数据校验
- 所有接口必须有 schema
- 业务逻辑放在 `services/`
- API 层只做请求分发

---

### 3. 测试规范

- 测试代码必须独立目录 `/tests`
- 不允许与业务代码混写
- 至少覆盖：
  - API接口测试
  - 核心业务逻辑测试

---

### 4. Git规范

- 每个功能一个分支
- commit message 格式：

feat: 新增语音识别模块
fix: 修复TTS播放问题
refactor: 重构对话服务

---

### 5. 环境变量管理

必须使用 `.env`：

OPENAI_API_KEY=
DATABASE_URL=
REDIS_URL=
TTS_PROVIDER=
ASR_PROVIDER=

---

## 六、核心模块设计

### 1. 语音链路（关键）

流程：

用户语音 → ASR → 文本
→ LLM → 回复文本
→ TTS → 音频
→ 前端播放 + 驱动数字人

---

### 2. AI老师 Prompt（必须实现）

```text
你是一位给9岁中国女孩上英语口语课的外教老师。

要求：
- 使用简单英语
- 每次最多说2句话
- 每次只问1个问题
- 语气鼓励、温柔
- 如果有语法错误：
  1. 先肯定
  2. 再自然纠正
  3. 给出正确表达

主题包括：
- animals
- science
- history
- culture
```

### 3. 数据库设计

必须实现以下表：

users
lessons
lesson_sessions
chat_messages
parent_settings

## 七、接口规范（示例）

语音输入
POST /api/v1/speech-to-text
AI对话
POST /api/v1/chat
TTS
POST /api/v1/text-to-speech

## 八、第一阶段目标（MVP）

必须实现：

语音对话（完整链路）
AI老师对话
iPad 页面
聊天记录保存

暂不实现：

复杂课程系统
长期记忆优化
3D数字人

## 九、性能要求

单次对话延迟 < 3 秒
TTS播放无明显卡顿
支持并发用户 ≥ 5

## 十、安全要求（儿童场景）

禁止生成不适合儿童内容
不允许讨论：
暴力
政治
成人内容
输出必须可控

## 十一、日志与监控

必须实现：
请求日志
错误日志
对话日志

## 十二、后续扩展（预留）

Live2D 表情控制
课程系统
家长后台
OpenClaw 接入（用于自动生成学习报告）

## 十三、开发优先级

按顺序实现：

基础后端（FastAPI）
语音识别
LLM对话
TTS
前端对话页面
聊天记录存储
Live2D集成

## 十四、禁止事项

不允许把所有代码写在一个文件
不允许没有类型定义
不允许跳过测试结构
不允许硬编码 API key
不允许前后端混写
十五、交付标准

## 项目必须具备：

可运行 Docker 环境
完整 README
一键启动（docker-compose up）
可在 iPad Safari 使用
