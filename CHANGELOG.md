# 更新日志

## 2025-12-16

### 🔧 修复
- **前后端连接问题**: 修复前端 `.env` 文件中的 API URL 配置，从错误的 IP 地址改为 `localhost:8000`
- **后端依赖**: 修复 `bcrypt` 版本兼容性问题，降级到 3.2.2 以兼容 `passlib`
- **随机聊天匹配**: 添加防止自己匹配自己的逻辑，修复匹配兼容性检查

### ✨ 新功能
- **聊天图片支持**: 
  - 数据库模型添加 `image_url` 字段（`PrivateMessage` 和 `RandomChatHistory`）
  - 支持发送纯图片、纯文本、图片+文本混合消息
  - 图片上传功能（最大 5MB，支持常见图片格式）
  - 图片预览和点击放大查看
  - 实时图片消息推送（Socket.IO）

### 🛠️ 改进
- **DeepSeek API 错误处理**: 添加详细的错误信息和 API Key 检查
- **调试日志**: 添加 Socket.IO 匹配和消息传递的详细日志
- **错误提示**: 改进前端错误信息显示，提供更友好的用户提示

### 📝 文档
- 添加 `DEEPSEEK_SETUP.md` - DeepSeek API 配置指南
- 添加 `test_connection.py` - 前后端连接诊断工具
- 添加 `test_deepseek.py` - DeepSeek API 配置测试脚本

### 📦 数据库迁移
- `6f0be8497fd4` - 添加 `image_url` 字段到消息表

