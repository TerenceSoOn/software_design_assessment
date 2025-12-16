"""
测试 DeepSeek API 配置
运行此脚本来验证 DeepSeek API Key 是否正确配置
"""
import asyncio
import sys
from app.config import settings
from app.utils.deepseek import chat_completion

async def test_deepseek():
    """测试 DeepSeek API 配置和连接"""
    print("=" * 60)
    print("DeepSeek API 配置测试")
    print("=" * 60)
    print()
    
    # 检查配置
    print("📋 配置检查:")
    print(f"   API URL: {settings.DEEPSEEK_API_URL}")
    
    if not settings.DEEPSEEK_API_KEY or settings.DEEPSEEK_API_KEY.strip() == "":
        print("   ❌ API Key: 未设置")
        print()
        print("🔧 配置步骤:")
        print("   1. 访问 https://www.deepseek.com/ 获取 API Key")
        print("   2. 在 codespace/backend/.env 文件中添加:")
        print("      DEEPSEEK_API_KEY=sk-your-api-key-here")
        print("   3. 重启后端服务")
        print()
        return False
    else:
        # 只显示前10个字符和后10个字符，中间用...代替
        key_display = settings.DEEPSEEK_API_KEY[:10] + "..." + settings.DEEPSEEK_API_KEY[-10:] if len(settings.DEEPSEEK_API_KEY) > 20 else settings.DEEPSEEK_API_KEY
        print(f"   ✅ API Key: {key_display}")
    print()
    
    # 测试 API 调用
    print("🧪 测试 API 调用...")
    try:
        response = await chat_completion([
            {"role": "user", "content": "Hello, please respond with just 'OK' to confirm the connection."}
        ])
        
        if "error" in response:
            error_type = response.get("error_type", "unknown")
            error_msg = response.get("error", "Unknown error")
            
            print(f"   ❌ API 调用失败")
            print(f"   错误类型: {error_type}")
            print(f"   错误信息: {error_msg}")
            print()
            
            if error_type == "missing_api_key":
                print("💡 解决方案:")
                print("   在 .env 文件中设置 DEEPSEEK_API_KEY")
            elif error_type == "api_error":
                status_code = response.get("status_code", "unknown")
                if status_code == 401:
                    print("💡 解决方案:")
                    print("   API Key 无效或已过期，请重新生成并更新配置")
                elif status_code == 429:
                    print("💡 解决方案:")
                    print("   API 调用频率超限，请稍后重试")
                else:
                    print("💡 请检查 API Key 和网络连接")
            elif error_type == "connection_error":
                print("💡 解决方案:")
                print("   检查网络连接和 API URL 配置")
            
            return False
        else:
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"   ✅ API 调用成功")
            print(f"   响应: {content[:100]}...")
            print()
            print("🎉 DeepSeek API 配置正确，可以正常使用 AI 功能！")
            return True
            
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(test_deepseek())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\n测试中断")
        sys.exit(1)

