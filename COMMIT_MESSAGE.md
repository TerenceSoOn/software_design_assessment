# Commit Message

```
feat: 添加聊天图片功能并修复多个问题

## 主要功能
- ✨ 实现聊天图片发送功能（支持纯图片、纯文本、图片+文本）
- 📸 图片上传、预览和显示功能
- 🔄 Socket.IO 实时图片消息推送

## 修复
- 🔧 修复前后端连接问题（.env API URL 配置）
- 🔧 修复 bcrypt 版本兼容性问题
- 🔧 修复随机聊天匹配逻辑（防止自己匹配自己）

## 改进
- 📝 改进 DeepSeek API 错误处理和提示
- 📝 添加详细的调试日志
- 📝 添加配置指南和测试工具

## 数据库变更
- 添加 image_url 字段到 private_messages 和 random_chat_history 表
- 迁移文件: 6f0be8497fd4_add_image_url_to_messages
```

