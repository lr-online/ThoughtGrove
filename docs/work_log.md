# 工作日志

## 2024-03-20

### 项目初始化
1. 创建了基础工程文件：
   - [x] `pyproject.toml`: 配置了项目依赖和开发工具
   - [x] `Dockerfile`: 设置了应用容器构建配置
   - [x] `docker-compose.yml`: 配置了应用服务和MongoDB服务
   - [x] `.gitignore`: 配置了版本控制忽略规则
   - [x] `.env.example`: 创建了环境变量示例文件

### 基础项目结构搭建
1. 创建了主要应用目录结构：
   - `thoughtgrove/`: 主应用目录
     - `main.py`: 应用入口文件
     - `core/config.py`: 配置管理模块
     - `db/mongodb.py`: 数据库连接模块
     - `models/base.py`: 基础模型类
   - `tests/`: 测试目录
     - `conftest.py`: 测试配置文件
     - `test_main.py`: 主应用测试文件

### 开发环境设置
1. 创建了开发环境配置文件：
   - [x] 创建 `.env` 文件，配置开发环境变量
2. 安装项目依赖：
   - [x] 使用 Poetry 安装所有依赖包
   - [x] 安装开发工具（pytest, black, isort 等）
3. 运行基础测试：
   - [x] 成功运行基础测试用例
   - [x] 验证主应用入口正常工作

### 用户认证系统开发
1. 创建了用户相关模块：
   - [x] `models/user.py`: 用户模型类（包含数据验证）
   - [x] `core/security.py`: 安全工具函数（密码哈希、JWT）
   - [x] `crud/user.py`: 用户数据库操作
2. 编写并运行测试：
   - [x] 用户模型测试（创建、更新、验证）
   - [x] 所有测试通过

### 技术选型
1. 包管理：使用 Poetry 进行 Python 包管理
   - 配置了主要依赖：FastAPI, MongoDB, OpenAI 等
   - 配置了开发依赖：pytest, black, isort 等
2. 部署方案：使用 Docker Compose
   - 应用服务：基于 Python 3.12
   - 数据库：MongoDB
   - 网络：使用 bridge 网络隔离服务

### 代码规范和优化
1. 导入路径规范化：
   - [x] 将所有相对导入路径修改为绝对导入路径
   - [x] 更新了以下文件的导入语句：
     - `models/user.py`
     - `core/security.py`
     - `crud/user.py`
     - `db/mongodb.py`
   - 经验总结：始终使用绝对导入路径，避免使用相对导入，这样可以：
     - 提高代码可读性和可维护性
     - 避免深层嵌套导入时的混淆
     - 防止重构时的路径错误
     - 使代码结构更清晰

2. Pydantic V2 迁移：
   - [x] 更新了模型配置，使用 `ConfigDict` 替代类基础配置 
   - [x] 为 `User` 和 `UserInDB` 模型都应用了 `model_config`
   - [x] 使用 `field_validator` 替代废弃的 `validator`
   - [x] 采用 `field_serializer` 替代 `json_encoders`
   - [x] 所有测试通过，**成功移除所有警告**
   - Pydantic V2 迁移经验：
     - 使用 `model_config = ConfigDict(...)` 替代 `class Config`
     - 使用 `@field_validator` 替代 `@validator`
     - 使用 `@field_serializer` 实现自定义序列化
     - 使用 `populate_by_name=True` 替代 `allow_population_by_field_name`

### 下一步计划
1. 实现用户认证API：
   - [ ] 用户注册接口
   - [ ] 用户登录接口
   - [ ] JWT认证中间件

## 2023-11-15
- 项目初始化
  - 创建了基本的项目结构
  - 设置了 FastAPI 框架
  - 配置了 Docker 环境
  - 初始化了 Git 仓库

## 2023-11-16
- 完善了项目结构
  - 添加了配置模块
  - 添加了数据库连接模块
  - 添加了基础模型类
- 添加了工具函数
  - 添加了密码哈希和验证函数
  - 添加了 JWT 令牌生成和验证函数

## 2023-11-17
- 优化了项目导入方式
  - 从相对导入修改为绝对导入
  - 在 tests 中更新导入路径
- 升级 Pydantic 到 V2
  - 修改了模型定义方式
  - 更新了验证逻辑

## 2023-11-18
- 实现用户认证功能
  - 完成用户模型和依赖项
  - 实现用户数据库操作
  - 创建用户注册和登录 API
  - 实现 JWT 认证中间件

## 2023-11-19
- 添加用户认证 API 测试
  - 编写用户注册和登录测试用例
  - 添加 JWT 中间件测试
  - 发现测试环境配置问题：需要配置 MongoDB 测试服务
  
## 2023-11-20
- 实现用户认证 API 功能
  - 完成用户注册接口
  - 完成用户登录接口
  - 实现JWT认证中间件
  - 编写认证API测试用例
  - 发现测试需要MongoDB服务配置
- 待解决问题
  - 需要在测试环境中配置MongoDB
  - 考虑使用Docker容器进行测试

## 2023-11-21
- 优化环境配置
  - 创建.env开发环境配置文件
  - 创建.env.test测试环境配置文件
  - 更新conftest.py加载测试环境变量
  - 添加Docker测试服务配置
  - 编写测试指南文档

## 2024-03-22
- 简化测试环境配置
  - 移除.env.test配置文件
  - 更新conftest.py使用默认环境配置
  - 从docker-compose.yml中移除test服务
  - 更新测试指南，简化为使用本地MongoDB服务
  - 使用docker启动独立的MongoDB服务用于测试

## 2024-03-24
- 代码修复与优化
  - 修复用户认证相关问题：
    - 修正create_user函数中MongoDB _id字段处理逻辑，确保正确返回UserInDB对象
    - 修复测试中的异步客户端使用方式，确保正确使用await关键字
  - 代码现代化更新：
    - 将过时的datetime.utcnow()替换为datetime.now(UTC)
    - 移除自定义event_loop fixture，使用pytest-asyncio提供的默认实现
  - 整体测试验证：
    - 所有14个测试用例全部通过
    - 解决了大部分警告信息
    - 确认项目基础功能完整可用
  - 时区处理策略确定：
    - 决定在数据库中统一使用UTC时间存储数据
    - 在API返回时将转换为北京时间供用户使用
    - 创建了时区转换工具函数(thoughtgrove/utils/datetime.py)
      - 实现了UTC与北京时间的相互转换
      - 提供了格式化输出函数，默认转为北京时间
      - 编写完整测试用例验证功能正确性
    - 更新了开发规则文档，添加时区处理指导

## 2024-03-27
- 随笔记录系统实现
  - 创建了笔记相关模型：
    - 实现了NoteBase、NoteCreate、NoteUpdate、Note和NoteInDB模型
    - 添加了字段验证，确保标题和内容不为空
  - 实现了笔记CRUD操作：
    - 创建笔记(create_note)
    - 获取笔记(get_note)
    - 更新笔记(update_note)
    - 删除笔记(delete_note)
    - 获取用户所有笔记(get_notes_by_user)
  - 实现了笔记API接口：
    - POST /api/notes/ - 创建笔记
    - GET /api/notes/{note_id} - 获取笔记
    - PUT /api/notes/{note_id} - 更新笔记
    - DELETE /api/notes/{note_id} - 删除笔记
    - GET /api/notes/ - 获取用户所有笔记
  - 编写测试：
    - 模型测试 - 验证模型字段和验证规则
    - CRUD测试 - 验证数据库操作
    - API测试 - 验证API接口功能
  - 修复认证相关问题：
    - 统一使用core.deps.py中的get_current_user函数
    - 修正JWT认证配置
  - 经验总结：
    - 使用tree或find命令查看文件结构，可以避免遗漏文件
    - 模块间依赖应统一管理，避免重复定义
    - 测试前应清除__pycache__缓存，避免导入冲突
