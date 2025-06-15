# Flask 版本管理系统 API 文档

本 API 文档涵盖了用户、产品、版本、文件等主要资源的接口说明，适用于 Web 前端对接。

接口地址：http://127.0.0.1:5000/api/v1
---

## 用户相关接口

### 获取所有用户
- **URL**: `/users`
- **方法**: GET
- **参数**: 无
- **返回**: 用户列表（JSON 数组）

### 创建新用户
- **URL**: `/users`
- **方法**: POST
- **参数**（JSON Body）:
  - `username` (string, 必填)
  - `email` (string, 必填)
  - `password` (string, 必填)
  - `is_admin` (bool, 选填)
- **返回**: 新建用户对象（JSON）

### 获取用户信息
- **URL**: `/users/<user_id>`
- **方法**: GET
- **参数**: 路径参数 `user_id`
- **返回**: 用户对象（JSON）

### 更新用户信息
- **URL**: `/users/<user_id>`
- **方法**: PUT
- **参数**（JSON Body）: 可更新字段
- **返回**: 更新后的用户对象（JSON）

### 删除用户
- **URL**: `/users/<user_id>`
- **方法**: DELETE
- **参数**: 路径参数 `user_id`
- **返回**: 删除结果（JSON）

---

## 产品相关接口

### 获取产品列表
- **URL**: `/products`
- **方法**: GET
- **参数**（Query）:
  - `page` (int, 选填)
  - `per_page` (int, 选填)
  - `status` (string, 选填)
- **返回**: 产品分页列表（JSON）

### 创建新产品
- **URL**: `/products`
- **方法**: POST
- **参数**（JSON Body）:
  - `name` (string, 必填)
  - `description` (string, 选填)
  - `code` (string, 必填)
  - `status` (string, 选填)
- **返回**: 新建产品对象（JSON）

### 获取产品详情
- **URL**: `/products/<product_id>`
- **方法**: GET
- **参数**: 路径参数 `product_id`
- **返回**: 产品对象（JSON）

### 更新产品信息
- **URL**: `/products/<product_id>`
- **方法**: PUT
- **参数**（JSON Body）: 可更新字段
- **返回**: 更新后的产品对象（JSON）

### 删除产品
- **URL**: `/products/<product_id>`
- **方法**: DELETE
- **参数**: 路径参数 `product_id`
- **返回**: 删除结果（JSON）

---

## 版本相关接口

### 获取版本列表（按产品）
- **URL**: `/versions`
- **方法**: GET
- **参数**（Query）:
  - `product_id` (int, 必填)
  - `page` (int, 选填)
  - `per_page` (int, 选填)
  - `status` (string, 选填)
- **返回**: 版本分页列表（JSON）

### 创建新版本
- **URL**: `/versions`
- **方法**: POST
- **参数**（JSON Body）:
  - `product_id` (int, 必填)
  - `version_number` (string, 必填)
  - `description` (string, 选填)
  - `release_notes` (string, 选填)
  - `author_id` (int, 必填)
  - `status` (string, 选填)
- **返回**: 新建版本对象（JSON）

### 获取版本详情
- **URL**: `/versions/<version_id>`
- **方法**: GET
- **参数**: 路径参数 `version_id`
- **返回**: 版本对象（JSON）

### 更新版本信息
- **URL**: `/versions/<version_id>`
- **方法**: PUT
- **参数**（JSON Body）: 可更新字段（不允许更改 product_id 和 author_id）
- **返回**: 更新后的版本对象（JSON）

### 删除版本
- **URL**: `/versions/<version_id>`
- **方法**: DELETE
- **参数**: 路径参数 `version_id`
- **返回**: 删除结果（JSON）

### 获取产品的版本历史
- **URL**: `/products/<product_id>/versions`
- **方法**: GET
- **参数**（Query）:
  - `page` (int, 选填)
  - `per_page` (int, 选填)
  - `status` (string, 选填)
- **返回**: 产品及其版本历史（JSON）

### 获取版本状态变更历史

- URL: `/api/versions/<version_id>/status-history`
- 方法: `GET`
- 描述: 获取特定版本的状态变更历史，包括创建、状态变更、锁定/解锁等操作
- 响应:
  ```json
  {
    "success": true,
    "data": {
      "version": {
        "id": 1,
        "version_number": "1.0.0",
        "description": "初始版本",
        "status": "released",
        "product_id": 1,
        "author_id": 1,
        "created_at": "2023-12-01T09:30:00",
        "updated_at": "2023-12-10T11:20:00",
        "released_at": "2023-12-10T11:15:00",
        "file_count": 3,
        "lock_status": true
      },
      "history": [
        {
          "operator_name": "张三",
          "operator_id": 1,
          "operation_type": "创建",
          "operation_time": "2023-12-01 09:30:00",
          "details": "{\"product_id\":1,\"product_name\":\"客户管理系统\",\"version_number\":\"1.0.0\",\"description\":\"初始创建\",\"status\":\"开发中\"}"
        },
        {
          "operator_name": "李四",
          "operator_id": 2,
          "operation_type": "状态变更",
          "operation_time": "2023-12-05 14:20:00",
          "details": "{\"product_id\":1,\"product_name\":\"客户管理系统\",\"version_number\":\"1.0.0\",\"changes\":{\"status\":{\"old\":\"开发中\",\"new\":\"测试中\"}}}"
        },
        {
          "operator_name": "王五",
          "operator_id": 3,
          "operation_type": "发布",
          "operation_time": "2023-12-10 11:15:00",
          "details": "{\"product_id\":1,\"product_name\":\"客户管理系统\",\"version_number\":\"1.0.0\",\"changes\":{\"status\":{\"old\":\"测试中\",\"new\":\"已发布\"}}}"
        },
        {
          "operator_name": "王五",
          "operator_id": 3,
          "operation_type": "锁定",
          "operation_time": "2023-12-10 11:20:00",
          "details": "{\"product_id\":1,\"product_name\":\"客户管理系统\",\"version_number\":\"1.0.0\",\"changes\":{\"lock_status\":{\"old\":\"false\",\"new\":\"true\"}}}"
        }
      ]
    }
  }
  ```

---

## 文件相关接口

### 上传文件
- **URL**: `/files/upload`
- **方法**: POST
- **参数**（form-data）:
  - `file` (file, 必填)
  - `version_id` (int, 必填)
  - `uploader_id` (int, 必填)
- **返回**: 文件对象（JSON）

### 下载文件
- **URL**: `/files/download/<file_id>`
- **方法**: GET
- **参数**: 路径参数 `file_id`
- **返回**: 文件流

### 获取版本的所有文件
- **URL**: `/files`
- **方法**: GET
- **参数**（Query）:
  - `version_id` (int, 必填)
- **返回**: 文件列表（JSON）

---

## 操作日志API

### 获取操作日志列表

- URL: `/api/operation-logs`
- 方法: `GET`
- 描述: 获取操作日志列表，支持多种条件过滤
- 查询参数:
  - `page`: 页码，默认为1
  - `per_page`: 每页记录数，默认为20
  - `operation_type`: 操作类型，如"创建"、"更新"、"删除"、"状态变更"等
  - `object_type`: 对象类型，如"产品"、"版本"、"用户"等
  - `object_id`: 对象ID
  - `operator_id`: 操作人ID
  - `start_time`: 开始时间，ISO格式
  - `end_time`: 结束时间，ISO格式
- 响应:
  ```json
  {
    "success": true,
    "data": {
      "logs": [
        {
          "id": 1,
          "operation_time": "2024-01-20T10:30:45",
          "operation_type": "创建",
          "object_type": "产品",
          "object_name": "客户管理系统",
          "object_id": "PRD-001",
          "operator_id": 1,
          "operator_name": "张三",
          "details": "{\"name\":\"客户管理系统\",\"code\":\"PRD-001\",\"description\":\"客户管理系统\",\"status\":\"active\"}"
        },
        // ... 更多日志
      ],
      "total": 100,
      "pages": 5,
      "current_page": 1
    }
  }
  ```

### 获取单条操作日志详情

- URL: `/api/operation-logs/<log_id>`
- 方法: `GET`
- 描述: 获取单条操作日志详情
- 响应:
  ```json
  {
    "success": true,
    "data": {
      "id": 1,
      "operation_time": "2024-01-20T10:30:45",
      "operation_type": "创建",
      "object_type": "产品",
      "object_name": "客户管理系统",
      "object_id": "PRD-001",
      "operator_id": 1,
      "operator_name": "张三",
      "details": "{\"name\":\"客户管理系统\",\"code\":\"PRD-001\",\"description\":\"客户管理系统\",\"status\":\"active\"}"
    }
  }
  ```

### 获取特定对象的操作日志

- URL: `/api/objects/<object_type>/<object_id>/logs`
- 方法: `GET`
- 描述: 获取特定对象的所有操作日志
- 查询参数:
  - `page`: 页码，默认为1
  - `per_page`: 每页记录数，默认为20
- 响应:
  ```json
  {
    "success": true,
    "data": {
      "logs": [
        {
          "id": 1,
          "operation_time": "2024-01-20T10:30:45",
          "operation_type": "创建",
          "object_type": "产品",
          "object_name": "客户管理系统",
          "object_id": "PRD-001",
          "operator_id": 1,
          "operator_name": "张三",
          "details": "{\"name\":\"客户管理系统\",\"code\":\"PRD-001\",\"description\":\"客户管理系统\",\"status\":\"active\"}"
        },
        // ... 更多日志
      ],
      "total": 10,
      "pages": 1,
      "current_page": 1
    }
  }
  ```

### 获取特定用户的操作日志

- URL: `/api/users/<user_id>/logs`
- 方法: `GET`
- 描述: 获取特定用户的所有操作日志
- 查询参数:
  - `page`: 页码，默认为1
  - `per_page`: 每页记录数，默认为20
- 响应:
  ```json
  {
    "success": true,
    "data": {
      "logs": [
        {
          "id": 1,
          "operation_time": "2024-01-20T10:30:45",
          "operation_type": "创建",
          "object_type": "产品",
          "object_name": "客户管理系统",
          "object_id": "PRD-001",
          "operator_id": 1,
          "operator_name": "张三",
          "details": "{\"name\":\"客户管理系统\",\"code\":\"PRD-001\",\"description\":\"客户管理系统\",\"status\":\"active\"}"
        },
        // ... 更多日志
      ],
      "total": 20,
      "pages": 1,
      "current_page": 1
    }
  }
  ```

如需详细字段说明，请参考各资源的模型定义。 