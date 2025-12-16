# 🚀 快速创建分支并提交代码

## 一键执行命令（按顺序执行）

### 1. 创建新分支
```bash
git checkout -b feature/chat-image-support
```

### 2. 更新 .gitignore（已自动更新）
```bash
# .gitignore 已更新，无需操作
```

### 3. 添加文件（排除敏感文件）
```bash
# 添加所有代码文件
git add codespace/backend/app/
git add codespace/backend/alembic/versions/6f0be8497fd4_add_image_url_to_messages.py
git add codespace/frontend/src/
git add codespace/frontend/vite.config.js

# 添加文档和工具
git add CHANGELOG.md
git add codespace/backend/DEEPSEEK_SETUP.md
git add codespace/backend/test_connection.py
git add codespace/backend/test_deepseek.py
git add codespace/frontend/DIAGNOSIS.md
git add .gitignore

# 注意：.env 文件会被自动排除（已在 .gitignore 中）
```

### 4. 检查将要提交的文件
```bash
git status
```

**确认以下文件不会被提交：**
- ❌ `codespace/frontend/.env` 
- ❌ `codespace/backend/static/uploads/*.jpg`
- ❌ `*.db` 文件

### 5. 提交代码
```bash
git commit -F GIT_COMMIT.txt
```

### 6. 推送到远程
```bash
git push -u origin feature/chat-image-support
```

### 7. 在 GitHub 创建 Pull Request
1. 访问：https://github.com/TerenceSoOn/software_design_assessment
2. 点击 "Compare & pull request" 按钮
3. 填写 PR 信息（参考下面的模板）

---

## 📝 PR 描述模板

```markdown
## ✨ 功能更新
- 实现聊天图片发送功能（支持纯图片、纯文本、图片+文本混合）
- 图片上传、预览和实时推送功能

## 🔧 修复
- 修复前后端连接问题（.env API URL 配置）
- 修复 bcrypt 版本兼容性问题  
- 修复随机聊天匹配逻辑（防止自己匹配自己）

## 🛠️ 改进
- 改进 DeepSeek API 错误处理和提示
- 添加详细的调试日志和测试工具

## 📦 数据库变更
- 添加 `image_url` 字段到 `private_messages` 和 `random_chat_history` 表
- 迁移文件: `6f0be8497fd4_add_image_url_to_messages.py`

## ✅ 测试清单
- [x] 可以发送纯图片消息
- [x] 可以发送图片+文本混合消息
- [x] 图片在双方都能正常显示
- [x] 前后端连接正常
- [x] 随机聊天匹配正常

## 📸 截图
[可以添加功能截图]
```

---

## ⚠️ 如果遇到问题

### 问题1: 推送被拒绝
```bash
# 先拉取最新代码
git checkout main
git pull origin main

# 重新创建分支
git checkout -b feature/chat-image-support
# 重新添加和提交文件
```

### 问题2: 想撤销提交
```bash
# 撤销最后一次提交（保留修改）
git reset HEAD~1

# 完全撤销修改（危险！）
git reset --hard HEAD~1
```

### 问题3: 想修改提交信息
```bash
# 修改最后一次提交信息
git commit --amend -m "新的提交信息"
git push -f origin feature/chat-image-support  # 需要强制推送
```

---

## 🔄 后续更新（如果代码有修改）

```bash
# 1. 确保在正确的分支
git checkout feature/chat-image-support

# 2. 添加修改的文件
git add <修改的文件>

# 3. 提交
git commit -m "fix: 修复图片显示问题"

# 4. 推送
git push
```

