# Git 分支创建和代码审核指南

## 📋 步骤概览

1. 创建新分支
2. 添加需要提交的文件（排除敏感文件和临时文件）
3. 提交代码
4. 推送到远程仓库
5. 创建 Pull Request

---

## 🚀 详细步骤

### 步骤 1: 创建新分支

```bash
# 从 main 分支创建新分支（推荐命名：feature/功能名称 或 fix/修复内容）
git checkout -b feature/chat-image-support

# 或者使用更具体的名称
git checkout -b feature/add-image-message-and-fixes
```

**分支命名规范：**
- `feature/功能名称` - 新功能
- `fix/修复内容` - 修复问题
- `refactor/重构内容` - 代码重构
- `docs/文档内容` - 文档更新

### 步骤 2: 检查并更新 .gitignore

在提交前，确保以下文件不会被提交：

```bash
# 检查 .gitignore 是否存在
cat .gitignore
```

**应该排除的文件：**
- `.env` 文件（包含敏感信息）
- `static/uploads/` 中的测试图片
- `__pycache__/`、`*.pyc`（Python 缓存）
- `node_modules/`（前端依赖）
- `*.db`（数据库文件）

### 步骤 3: 添加文件到暂存区

```bash
# 添加所有修改的文件（但排除 .gitignore 中的文件）
git add codespace/backend/app/
git add codespace/backend/alembic/versions/6f0be8497fd4_add_image_url_to_messages.py
git add codespace/frontend/src/
git add codespace/frontend/.env  # 注意：如果 .env 包含敏感信息，应该排除

# 添加文档文件
git add CHANGELOG.md
git add codespace/backend/DEEPSEEK_SETUP.md
git add codespace/backend/test_connection.py
git add codespace/backend/test_deepseek.py
git add codespace/frontend/DIAGNOSIS.md

# 或者一次性添加所有（推荐先检查）
git add -A
```

**⚠️ 重要：提交前检查**

```bash
# 查看将要提交的文件
git status

# 如果看到不应该提交的文件（如 .env、测试图片），取消暂存
git restore --staged codespace/frontend/.env
git restore --staged codespace/backend/static/uploads/*.jpg
```

### 步骤 4: 提交代码

```bash
# 使用之前创建的 commit message
git commit -F GIT_COMMIT.txt

# 或者手动输入
git commit -m "feat: 添加聊天图片功能并修复多个问题

- 实现聊天图片发送功能（支持纯图片、纯文本、图片+文本）
- 修复前后端连接问题和 bcrypt 兼容性
- 修复随机聊天匹配逻辑
- 改进 DeepSeek API 错误处理
- 添加 image_url 字段到消息表"
```

### 步骤 5: 推送到远程仓库

```bash
# 首次推送新分支
git push -u origin feature/chat-image-support

# 之后只需要
git push
```

### 步骤 6: 在 GitHub 上创建 Pull Request

1. **访问 GitHub 仓库**
   - 打开：https://github.com/TerenceSoOn/software_design_assessment

2. **创建 Pull Request**
   - 推送后，GitHub 会显示 "Compare & pull request" 按钮
   - 点击按钮，或手动进入 "Pull requests" → "New pull request"

3. **填写 PR 信息**
   - **Title（标题）**: `feat: 添加聊天图片功能并修复多个问题`
   - **Description（描述）**: 复制 `CHANGELOG.md` 或 `GIT_COMMIT.txt` 的内容
   - **Reviewers（审核者）**: 选择小组成员
   - **Labels（标签）**: 添加 `feature`、`enhancement` 等标签

4. **提交 PR**
   - 点击 "Create pull request"
   - 等待小组成员审核和评论

---

## 🔍 常用 Git 命令

### 查看状态
```bash
git status                    # 查看当前状态
git log --oneline            # 查看提交历史
git diff                      # 查看未暂存的修改
git diff --staged             # 查看已暂存的修改
```

### 分支操作
```bash
git branch                    # 查看所有分支
git branch -a                 # 查看所有分支（包括远程）
git checkout main             # 切换回 main 分支
git branch -d feature/xxx     # 删除本地分支（已合并）
```

### 撤销操作
```bash
git restore <file>            # 撤销工作区的修改
git restore --staged <file>   # 取消暂存
git reset HEAD~1              # 撤销最后一次提交（保留修改）
```

---

## ⚠️ 注意事项

1. **不要提交敏感信息**
   - `.env` 文件中的 API Key、密码等
   - 确保 `.gitignore` 正确配置

2. **不要提交大文件**
   - 测试图片、视频等
   - 数据库文件（.db）

3. **提交前测试**
   - 确保代码可以正常运行
   - 检查是否有语法错误

4. **保持分支干净**
   - 一个分支只做一件事
   - 提交信息清晰明确

---

## 📝 PR 模板示例

```markdown
## 变更内容
- ✨ 添加聊天图片发送功能
- 🔧 修复前后端连接问题
- 🔧 修复 bcrypt 兼容性问题

## 测试说明
- [x] 可以发送纯图片消息
- [x] 可以发送图片+文本混合消息
- [x] 图片在双方都能正常显示
- [x] 前后端连接正常

## 截图（如有）
[添加功能截图]

## 相关 Issue
#123（如果有）
```

