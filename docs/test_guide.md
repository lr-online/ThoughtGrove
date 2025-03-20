# 测试指南

## 测试环境配置

ThoughtGrove项目使用MongoDB作为数据库，并采用pytest进行测试。测试过程中需要确保MongoDB服务正常运行。

## 本地运行测试

### 前提条件

1. 确保已安装Python 3.12+和pip
2. 确保MongoDB服务在本地27017端口运行
   ```bash
   # 可以使用Docker启动MongoDB服务
   docker run --name mongodb -d -p 27017:27017 mongo
   ```

### 运行测试

1. 进入poetry 环境：`poetry env activate`
2. 执行测试：`pytest`

## 测试结构

测试目录结构如下：

```
tests/
├── conftest.py        # 测试配置文件
├── test_api/          # API测试
│   ├── test_auth.py   # 认证API测试
│   └── ...
└── test_unit/         # 单元测试
    ├── test_models.py # 模型测试
    ├── test_utils.py  # 工具函数测试
    └── ...
```

## 注意事项

1. 测试使用应用配置的数据库（根据.env文件中的MONGODB_DB_NAME配置）
2. 每次测试会自动清理测试数据
3. 对于需要模拟的外部服务，使用`unittest.mock`或`pytest-mock`
4. 测试前请确保MongoDB服务已启动 