# DeepSeek API 配置指南

## 问题诊断

如果 AI 功能无法使用，通常是因为 DeepSeek API Key 未配置。

## 配置步骤

### 1. 获取 DeepSeek API Key

1. 访问 [DeepSeek 官网](https://www.deepseek.com/)
2. 注册/登录账号
3. 进入 API 管理页面
4. 创建新的 API Key
5. 复制 API Key（格式类似：`sk-xxxxxxxxxxxxxxxxxxxxx`）

### 2. 配置 API Key

在 `codespace/backend` 目录下创建或编辑 `.env` 文件：

```env
DEEPSEEK_API_KEY=sk-your-api-key-here
DEEPSEEK_API_URL=https://api.deepseek.com/v1
```

**示例：**
```env
DEEPSEEK_API_KEY=sk-1234567890abcdefghijklmnopqrstuvwxyz
DEEPSEEK_API_URL=https://api.deepseek.com/v1
```

### 3. 重启后端服务

配置完成后，需要重启后端服务才能生效：

```powershell
# 停止当前后端（Ctrl+C）
# 然后重新启动
cd codespace\backend
.\venv\Scripts\activate
uvicorn app.main:socket_app --host 0.0.0.0 --port 8000 --reload
```

### 4. 验证配置

启动后端后，在浏览器控制台或使用 curl 测试：

```javascript
// 在浏览器控制台测试
fetch('http://localhost:8000/ai/companion', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_JWT_TOKEN'
  },
  body: JSON.stringify({
    message: 'Hello'
  })
})
.then(r => r.json())
.then(console.log)
```

## 常见错误

### 错误1: "AI功能未配置"
- **原因**: `DEEPSEEK_API_KEY` 未设置或为空
- **解决**: 检查 `.env` 文件中的 `DEEPSEEK_API_KEY` 是否正确配置

### 错误2: "无法连接到AI服务"
- **原因**: 网络问题或 API URL 错误
- **解决**: 检查网络连接和 `DEEPSEEK_API_URL` 配置

### 错误3: "API returned error 401"
- **原因**: API Key 无效或已过期
- **解决**: 重新生成 API Key 并更新配置

### 错误4: "API returned error 429"
- **原因**: API 调用频率超限
- **解决**: 等待一段时间后重试，或升级 API 套餐

## 注意事项

1. **不要将 API Key 提交到 Git**
   - 确保 `.env` 文件在 `.gitignore` 中
   - 不要将 API Key 硬编码在代码中

2. **API Key 安全**
   - 不要分享你的 API Key
   - 定期轮换 API Key
   - 如果泄露，立即撤销并重新生成

3. **费用说明**
   - DeepSeek API 可能有使用费用
   - 查看 DeepSeek 官网了解定价信息
   - 设置使用限额避免意外费用

## 测试配置

运行以下 Python 脚本测试配置：

```python
# test_deepseek.py
import asyncio
from app.config import settings
from app.utils.deepseek import chat_completion

async def test():
    print(f"API URL: {settings.DEEPSEEK_API_URL}")
    print(f"API Key: {'已设置' if settings.DEEPSEEK_API_KEY else '未设置'}")
    
    if not settings.DEEPSEEK_API_KEY:
        print("❌ 请先配置 DEEPSEEK_API_KEY")
        return
    
    response = await chat_completion([
        {"role": "user", "content": "Hello"}
    ])
    
    if "error" in response:
        print(f"❌ 错误: {response['error']}")
    else:
        print(f"✅ 成功: {response['choices'][0]['message']['content']}")

if __name__ == "__main__":
    asyncio.run(test())
```

运行：
```powershell
cd codespace\backend
python test_deepseek.py
```

