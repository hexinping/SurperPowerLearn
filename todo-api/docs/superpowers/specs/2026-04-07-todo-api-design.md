# Todo API 设计规格

## 概述

使用 Python + FastAPI + SQLAlchemy + SQLite 构建一个简单的待办事项 REST API，支持增删改查（CRUD）操作。不需要认证，不需要分页/筛选，保持最简。

## 架构

采用分层架构，职责清晰：

```
todo-api/
├── todo_api/
│   ├── __init__.py      # 包标识
│   ├── main.py          # FastAPI 应用入口 + 路由
│   ├── database.py      # 数据库连接配置
│   ├── models.py        # SQLAlchemy 数据模型
│   ├── schemas.py       # Pydantic 请求/响应模型
│   └── crud.py          # 数据库 CRUD 操作
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # pytest 配置、测试数据库 fixture
│   └── test_api.py      # API 端点测试
└── requirements.txt     # 依赖清单
```

**职责分工：**

- `database.py` — 创建 SQLAlchemy 引擎和会话工厂
- `models.py` — 定义数据库表结构（TodoItem）
- `schemas.py` — 定义 API 输入/输出的数据格式和验证规则
- `crud.py` — 封装所有数据库操作
- `main.py` — 定义 4 个 REST 端点，串联各层

## 数据模型

### 数据库模型（TodoItem 表）

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | Integer, 主键, 自增 | 唯一标识 |
| `title` | String(200), 非空 | 待办事项标题 |
| `description` | Text, 可选, 默认 None | 待办事项详细描述，无长度限制 |
| `completed` | Boolean, 默认 False | 是否已完成 |
| `created_at` | DateTime, 默认当前时间 | 创建时间 |

### Pydantic Schema

| Schema | 用途 | 字段 |
|--------|------|------|
| `TodoCreate` | 创建请求 | title (必填, 1-200字符), description (可选) |
| `TodoUpdate` | 更新请求 | title (可选), description (可选), completed (可选) |
| `TodoResponse` | 响应输出 | id, title, description, completed, created_at |

## API 端点

| 方法 | 路径 | 说明 | 请求体 | 响应 |
|------|------|------|--------|------|
| `POST` | `/todos` | 创建待办事项 | `TodoCreate` | `201` + `TodoResponse` |
| `GET` | `/todos` | 获取所有待办事项 | 无 | `200` + `List[TodoResponse]` |
| `PUT` | `/todos/{id}` | 更新待办事项 | `TodoUpdate` | `200` + `TodoResponse` |
| `DELETE` | `/todos/{id}` | 删除待办事项 | 无 | `204` 无内容 |

## 错误处理

| 场景 | 状态码 | 说明 |
|------|--------|------|
| 资源不存在 | `404` | GET/PUT/DELETE 找不到对应 id 时返回 |
| 标题为空或超长 | `422` | Pydantic 自动验证，标题需 1-200 字符 |

## 测试策略

使用 `pytest` + FastAPI 的 `TestClient`，配合内存 SQLite 数据库（`:memory:`），每个测试独立事务，互不影响。

**测试用例：**

| 测试 | 验证点 |
|------|--------|
| 创建待办事项 | 返回 201，字段正确，id 自动生成 |
| 创建带描述的待办事项 | 返回 201，description 字段正确 |
| 创建时标题为空 | 返回 422 验证错误 |
| 获取所有待办事项 | 返回列表，包含已创建的项 |
| 更新待办事项 | 返回 200，字段已更新（含 description） |
| 更新不存在的项 | 返回 404 |
| 删除待办事项 | 返回 204，再查询确认已删除 |
| 删除不存在的项 | 返回 404 |

## 约束和假设

- Python 3.12+
- 不需要认证
- 不需要分页、筛选、搜索
- SQLite 文件存储在项目根目录（`todo.db`）
- 开发阶段使用 `uvicorn` 运行
