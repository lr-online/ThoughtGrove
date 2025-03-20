# ThoughtGrove (拙园)

**培育思想的数字园林 | A Digital Garden for Cultivating Ideas**

<div align="center">

![ThoughtGrove Logo](https://via.placeholder.com/150?text=ThoughtGrove)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-green.svg)](https://www.python.org/downloads/)

</div>

## 📝 项目简介

ThoughtGrove（拙园）是一个私人思想园林系统，旨在为用户（主要是我的妻子）提供一个数字空间，用于记录随笔、培育想法、促进个人成长。系统内置AI助手作为"园丁"，辅助用户整理思绪、发现连接、深化思考。

名称"拙园"取自中国传统园林文化，"拙"有质朴、自然之意，寓意这是一个不求完美但真实自然的思想栖息地。

## 🌱 核心理念

ThoughtGrove 基于以下理念设计：

- **思想需要培育**：将零散念头视为可以生长的种子
- **反思促进成长**：通过定期回顾和思考整合提升认知深度
- **AI辅助而非替代**：AI园丁作为思考伙伴，而非决策者

## ✨ 主要功能

### 随笔记录系统
- 支持Markdown格式和多媒体内容嵌入
- 版本历史记录与回溯
- 自定义标签与AI智能标签
- 基础搜索功能

### 知识花园培育
- **思想种子系统**：
  - 快速记录思想火花
  - 种子状态管理（种子→幼苗→成熟）
  - 定期提醒"浇灌"未发展的思想种子
- **知识连接网络**：
  - 自动识别随笔间的主题关联
  - 可视化知识关联图谱
  - 智能推荐相关随笔

### 反思与成长机制
- **定期回顾**：
  - 自动生成周/月/季/年度思考摘要
  - 识别时间段内的核心主题和情感趋势
- **思想整合**：
  - AI辅助将分散随笔整合为系统性思考
  - 提供内容整合建议和框架
- **成长报告**：
  - 分析思考深度和广度的变化
  - 追踪关注主题的演变

### 创新功能
- **思想时间胶囊**：
  - 创建特定时间才能查看的随笔
  - 设置解锁条件和提醒
- **认知偏见提醒**：
  - 识别内容中可能存在的认知偏见
  - 提供多角度思考建议
- **创意激发工具**：
  - 基于历史内容生成个性化思考提示
  - 提供创意激发问题

### AI园丁助手
- 内容分析：分析随笔内容，提供反馈和建议
- 互动对话：基于随笔内容进行有意义的对话
- 思维拓展：提出相关问题，促进思考深化
- 智能标签建议：自动分析内容并推荐相关标签

## 🔧 技术栈

- **后端**：Python, FastAPI
- **数据库**：MongoDB
- **AI组件**：OpenAI SDK
- **前端**：React
- **身份认证**：JWT
- **部署**：Docker

## 🚀 安装与使用

### 环境要求
- Python 3.12+
- Node.js 16+
- MongoDB 5.0+
- Docker

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/yourusername/thought-grove.git
cd thought-grove

# 后端设置
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp config/.env.example config/.env
# 编辑 config/.env 文件，填入必要配置

# 前端设置
cd ../frontend
npm install
cp .env.example .env
# 编辑 .env 文件，填入必要配置

# 启动MongoDB（如果使用Docker）
cd ../backend
docker-compose -f docker/docker-compose.yml up -d mongodb

# 启动后端服务
cd backend
python -m uvicorn thought_grove.main:app --reload

# 启动前端服务（新终端）
cd frontend
npm run dev
```

## 📂 项目结构

```
thought-grove/
├── backend/                    # 后端代码目录
│   ├── docker/                # Docker 配置文件
│   ├── config/                # 配置文件
│   ├── docs/                  # 文档
│   ├── scripts/               # 工具脚本
│   ├── tests/                 # 测试文件
│   ├── thought_grove/         # Python 包
│   ├── setup.py              # 包配置文件
│   └── requirements.txt      # 依赖文件
│
├── frontend/                  # 前端代码目录
│   ├── src/                  # 源代码
│   ├── public/               # 静态文件
│   └── package.json         # 依赖配置
│
└── README.md                 # 项目说明
```

## 🤝 贡献指南

虽然此项目初期主要供个人使用，但欢迎提出建议和意见：

1. Fork 本仓库
2. 创建新分支 (`git checkout -b feature/amazing-idea`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-idea`)
5. 开启 Pull Request

## 📜 许可证

本项目采用 MIT 许可证 - 详情见 [LICENSE](LICENSE) 文件

## 🌟 致谢

特别感谢我的妻子，是她的灵感启发了这个项目的创建。ThoughtGrove 将成为我们共同培育思想的数字园林。

---

**ThoughtGrove** - 一隅拙朴的园林，万千思绪的家园。
