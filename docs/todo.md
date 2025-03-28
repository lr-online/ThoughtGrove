# 待办事项

## 进行中

### 前端完善与修复（优先级最高）
- [ ] 检查并完善现有页面
  - [ ] 首页（index.html）
    - [ ] 检查功能卡片显示效果，优化排版
    - [ ] 添加更多视觉吸引元素
    - [ ] 确保响应式布局在各种设备上正常显示
  - [ ] 登录页（login.html）
    - [ ] 完善表单验证逻辑
    - [ ] 添加错误提示样式和交互反馈
    - [ ] 修复记住我功能
    - [ ] 测试表单提交与API对接
  - [ ] 注册页（register.html）
    - [ ] 完善密码强度检查
    - [ ] 优化表单验证体验
    - [ ] 测试表单提交与API对接
  - [ ] 笔记列表页
    - [ ] 实现笔记卡片布局和基本样式
    - [ ] 添加笔记排序功能
    - [ ] 实现笔记搜索功能
    - [ ] 添加无笔记时的引导提示
  - [ ] 笔记详情页（note_detail.html）
    - [ ] 优化内容显示格式
    - [ ] 完善笔记操作按钮和功能
    - [ ] 添加笔记元数据显示
  - [ ] 笔记编辑器（note_editor.html）
    - [ ] 实现自动保存功能
    - [ ] 优化编辑区域样式和交互
    - [ ] 添加Markdown预览功能
    - [ ] 实现标签选择/添加功能

- [ ] 开发缺失的页面
  - [ ] 用户中心页面
    - [ ] 设计用户资料显示和编辑界面
    - [ ] 实现密码修改功能
    - [ ] 添加用户偏好设置
  - [ ] 标签管理页面
    - [ ] 设计标签列表和管理界面
    - [ ] 实现标签CRUD功能
    - [ ] 添加按标签筛选笔记功能
  - [ ] 笔记归档页面
    - [ ] 设计归档列表界面
    - [ ] 实现归档功能和管理
  - [ ] 错误页面（404、500等）
    - [ ] 设计友好的错误提示页面

- [ ] 全局UI/UX优化
  - [ ] 添加页面过渡动画
  - [ ] 实现内容加载骨架屏
  - [ ] 优化表单交互体验和反馈
  - [ ] 改进移动端导航和交互
  - [ ] 优化暗色主题下的视觉体验

- [ ] 前端功能完善
  - [ ] 优化主题切换功能
  - [ ] 实现用户设置持久化
  - [ ] 添加键盘快捷键支持
  - [ ] 实现错误处理和用户友好提示
  - [ ] 优化API请求管理和状态处理

### 优化现有功能
- [ ] 用户系统优化
  - [ ] 添加用户信息更新接口
  - [ ] 实现用户密码重置功能
  - [ ] 增加用户信息查询接口
  - [ ] 优化用户认证错误处理
- [ ] 笔记系统增强
  - [ ] 添加笔记分页查询功能
  - [ ] 实现笔记全文搜索
  - [ ] 支持笔记排序（创建时间/更新时间）
  - [ ] 添加笔记统计功能（总数/字数统计等）
- [ ] 系统健壮性提升
  - [ ] 完善错误处理和日志记录
  - [ ] 添加请求速率限制
  - [ ] 优化数据库查询性能
  - [ ] 增加单元测试覆盖率
- [ ] API文档完善
  - [ ] 更新OpenAPI文档描述
  - [ ] 添加请求/响应示例
  - [ ] 编写API使用指南
- [x] 前端代码优化
  - [x] 合并冗余的CSS文件
  - [x] 移除不需要的离线功能
  - [x] 删除冗余页面文件
  - [x] 简化Service Worker实现

### 标签系统
- [ ] 标签模型设计
  - [ ] 创建标签基础模型（TagBase）
  - [ ] 创建标签数据库模型（TagInDB）
  - [ ] 创建标签创建/更新模型
- [ ] 标签CRUD操作
  - [ ] 创建标签（create_tag）
  - [ ] 获取标签（get_tag）
  - [ ] 更新标签（update_tag）
  - [ ] 删除标签（delete_tag）
  - [ ] 获取用户所有标签（get_tags_by_user）
- [ ] 笔记-标签关联功能
  - [ ] 修改笔记模型，支持标签关联
  - [ ] 实现添加/移除标签功能
  - [ ] 实现按标签查询笔记功能
- [ ] 标签API接口
  - [ ] 标签管理接口（CRUD）
  - [ ] 笔记标签关联接口

## 待开始
- [ ] 用户界面增强
  - [ ] 添加过渡动画和交互反馈
  - [ ] 优化表单交互体验
  - [ ] 添加内容加载骨架屏
  - [ ] 前后端集成测试
    - [ ] 建立模拟API响应环境
    - [ ] 编写端到端测试用例
    - [ ] 测试所有API交互场景
    - [ ] 测试数据同步和错误处理

- [ ] AI园丁助手
  - [ ] AI交互模型设计
    - [ ] 会话模型设计
    - [ ] AI请求/响应模型设计
  - [ ] OpenAI集成
    - [ ] API客户端封装
    - [ ] 请求构建与处理
    - [ ] 错误处理与重试机制
  - [ ] AI功能实现
    - [ ] 内容分析功能
    - [ ] 对话交互功能
    - [ ] 思维拓展功能
  - [ ] AI API接口
    - [ ] 对话接口
    - [ ] 内容分析接口
    - [ ] 思维拓展接口
- [ ] 部署与性能优化
  - [ ] 完善Docker配置
  - [ ] 数据库索引优化
  - [ ] API响应缓存
  - [ ] 错误监控与日志

## 已完成
- [x] 项目规划
  - [x] 确定技术栈
  - [x] 制定开发计划
  - [x] 创建项目文档
- [x] 代码规范优化
  - [x] 修改相对导入路径为绝对导入
  - [x] 升级Pydantic V2特性
- [x] 项目初始化
  - [x] 创建 pyproject.toml
  - [x] 创建 Dockerfile
  - [x] 创建 docker-compose.yml
  - [x] 创建 .gitignore
  - [x] 创建 .env.example
- [x] 创建基础项目结构
  - [x] 创建主应用目录结构
  - [x] 创建基础配置文件
  - [x] 创建数据库连接模块
  - [x] 创建基础模型类
  - [x] 创建测试目录和基础测试
- [x] 设置开发环境
  - [x] 安装项目依赖
  - [x] 配置开发工具
  - [x] 运行基础测试
- [x] 用户认证系统
  - [x] 编写用户模型和测试
  - [x] 创建安全工具函数
  - [x] 创建用户数据库操作
  - [x] 实现用户认证API
    - [x] 用户注册接口
    - [x] 用户登录接口
    - [x] JWT认证中间件
    - [x] 编写认证API测试用例
      - [x] 测试用例编写完成
- [x] 环境配置优化
  - [x] 简化测试环境配置（使用本地MongoDB）
  - [x] 更新测试文档
- [x] 随笔记录系统
  - [x] 创建笔记模型和验证
  - [x] 实现笔记CRUD操作
  - [x] 实现笔记API
  - [x] 编写笔记相关测试
- [x] 前端页面基础开发
  - [x] 页面设计
    - [x] 设计整体布局和风格（体现"拙园"特色）
    - [x] 创建响应式设计方案（适配电脑/手机/平板）
    - [x] 设计组件库和样式系统
  - [x] 基础页面开发
    - [x] 实现注册页面
    - [x] 实现登录页面
    - [x] 实现主页/导航页面
  - [x] 笔记功能页面初步实现
    - [x] 基础笔记列表页面
    - [x] 基础笔记详情页面
    - [x] 基础笔记创建/编辑页面
  - [x] 初步功能集成
    - [x] 实现前端路由系统
    - [x] 集成API请求服务
    - [x] 实现状态管理
    - [x] 添加错误处理和加载状态
  - [x] PWA支持
    - [x] 添加Web App Manifest
    - [x] 实现Service Worker
    - [x] 配置缓存策略
    - [x] 添加安装提示功能
    - [x] 测试跨平台安装体验
  - [x] 主题系统
    - [x] 实现主题色彩更新（中国传统山水画配色）
    - [x] 完善深色主题配色（中国传统夜色风格）
  - [x] 图片资源完善
    - [x] 创建应用图标（多种尺寸）
    - [x] 创建基本favicon
    - [x] 优化UI元素图标
    - [x] 添加功能引导截图
    - [x] 准备应用商店和文档图片


## 注意事项
1. 所有环境变量配置都通过 .env 文件管理
2. 开发时遵循测试驱动开发（TDD）原则
3. 及时更新文档和工作日志
4. 所有导入使用绝对路径
5. 使用 tree 或 find 命令检查目录结构，避免遗漏文件
