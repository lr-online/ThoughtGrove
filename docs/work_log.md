# 工作日志

## 2024-03-20

### 项目初始化
1. 创建了基础工程文件：
   - `pyproject.toml`: 配置了项目依赖和开发工具
   - `Dockerfile`: 设置了应用容器构建配置
   - `docker-compose.yml`: 配置了应用服务和MongoDB服务

### 技术选型
1. 包管理：使用 Poetry 进行 Python 包管理
   - 配置了主要依赖：FastAPI, MongoDB, OpenAI 等
   - 配置了开发依赖：pytest, black, isort 等
2. 部署方案：使用 Docker Compose
   - 应用服务：基于 Python 3.12
   - 数据库：MongoDB
   - 网络：使用 bridge 网络隔离服务

### 下一步计划
1. 创建基础项目结构
2. 设置开发环境
3. 开始编写测试用例
