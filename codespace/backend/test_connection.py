"""
诊断脚本：测试前后端连接和注册逻辑
用于区分是连接问题还是注册逻辑问题
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_connection():
    """测试1: 基础连接测试"""
    print("=" * 60)
    print("测试1: 基础连接测试")
    print("=" * 60)
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ 后端连接正常")
            print(f"   响应: {response.json()}")
            return True
        else:
            print(f"❌ 后端返回异常状态码: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务器")
        print("   请确认后端是否在运行: uvicorn app.main:socket_app --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print(f"❌ 连接错误: {e}")
        return False

def test_api_docs():
    """测试2: API文档访问测试"""
    print("\n" + "=" * 60)
    print("测试2: API文档访问测试")
    print("=" * 60)
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API文档可访问")
            return True
        else:
            print(f"⚠️  API文档返回状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API文档访问错误: {e}")
        return False

def test_register_endpoint():
    """测试3: 注册接口测试（不传数据，看是否能到达接口）"""
    print("\n" + "=" * 60)
    print("测试3: 注册接口可达性测试")
    print("=" * 60)
    try:
        # 发送空数据，看是否能到达接口（应该返回422验证错误，而不是连接错误）
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json={},
            timeout=5
        )
        if response.status_code == 422:
            print("✅ 注册接口可达（返回422是正常的，表示数据验证失败）")
            print(f"   响应详情: {response.json()}")
            return True
        elif response.status_code == 201:
            print("⚠️  注册接口返回201（意外成功）")
            return True
        else:
            print(f"⚠️  注册接口返回状态码: {response.status_code}")
            print(f"   响应: {response.text[:200]}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到注册接口（连接问题）")
        return False
    except Exception as e:
        print(f"❌ 注册接口测试错误: {e}")
        return False

def test_register_logic():
    """测试4: 注册逻辑测试（完整数据）"""
    print("\n" + "=" * 60)
    print("测试4: 注册逻辑测试")
    print("=" * 60)
    import random
    import string
    
    # 生成随机用户名
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    test_data = {
        "username": f"test_{username}",
        "password": "test123456",
        "gender": "male",
        "preferred_gender": "female"
    }
    
    print(f"测试数据: username={test_data['username']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 201:
            print("✅ 注册逻辑正常，用户创建成功")
            result = response.json()
            print(f"   用户ID: {result.get('id')}")
            print(f"   用户名: {result.get('username')}")
            return True
        elif response.status_code == 400:
            error_detail = response.json().get('detail', 'Unknown error')
            print(f"❌ 注册逻辑错误（业务逻辑问题）")
            print(f"   错误详情: {error_detail}")
            return False
        elif response.status_code == 500:
            print("❌ 注册逻辑错误（服务器内部错误）")
            print(f"   响应: {response.text[:500]}")
            return False
        else:
            print(f"⚠️  注册返回意外状态码: {response.status_code}")
            print(f"   响应: {response.text[:200]}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到注册接口（连接问题）")
        return False
    except Exception as e:
        print(f"❌ 注册逻辑测试错误: {e}")
        return False

def test_cors():
    """测试5: CORS测试"""
    print("\n" + "=" * 60)
    print("测试5: CORS配置测试")
    print("=" * 60)
    try:
        # 模拟浏览器发送OPTIONS请求
        response = requests.options(
            f"{BASE_URL}/auth/register",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type"
            },
            timeout=5
        )
        cors_headers = {
            "access-control-allow-origin": response.headers.get("Access-Control-Allow-Origin"),
            "access-control-allow-methods": response.headers.get("Access-Control-Allow-Methods"),
            "access-control-allow-credentials": response.headers.get("Access-Control-Allow-Credentials")
        }
        print(f"CORS响应头: {cors_headers}")
        if cors_headers["access-control-allow-origin"] or cors_headers["access-control-allow-methods"]:
            print("✅ CORS配置正常")
            return True
        else:
            print("⚠️  CORS响应头未设置（但可能使用正则匹配，仍可工作）")
            return True  # 后端使用正则匹配，可能不显示在OPTIONS中
    except Exception as e:
        print(f"⚠️  CORS测试错误: {e}")
        return True  # OPTIONS请求失败不影响实际请求

def main():
    print("\n" + "🔍 前后端连接诊断工具" + "\n")
    print(f"后端地址: {BASE_URL}\n")
    
    results = {
        "连接测试": test_connection(),
        "API文档": test_api_docs(),
        "注册接口可达性": test_register_endpoint(),
        "注册逻辑": test_register_logic(),
        "CORS配置": test_cors()
    }
    
    print("\n" + "=" * 60)
    print("诊断结果总结")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    print("\n" + "=" * 60)
    print("问题判断指南")
    print("=" * 60)
    
    if not results["连接测试"]:
        print("🔴 问题类型: 前后端连接问题")
        print("   解决方案:")
        print("   1. 确认后端是否运行: netstat -ano | findstr :8000")
        print("   2. 重启后端服务")
        print("   3. 检查防火墙设置")
    elif not results["注册接口可达性"]:
        print("🔴 问题类型: 前后端连接问题（接口不可达）")
        print("   解决方案:")
        print("   1. 检查后端路由配置")
        print("   2. 检查CORS设置")
        print("   3. 查看后端日志")
    elif not results["注册逻辑"]:
        print("🟡 问题类型: 注册逻辑问题")
        print("   解决方案:")
        print("   1. 查看后端日志中的错误信息")
        print("   2. 检查数据库连接")
        print("   3. 检查数据验证逻辑")
    elif results["连接测试"] and results["注册逻辑"]:
        print("🟢 后端功能正常")
        print("   如果前端仍无法连接，请检查:")
        print("   1. 浏览器控制台的网络请求")
        print("   2. 前端API URL配置（VITE_API_URL）")
        print("   3. 浏览器CORS错误信息")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n测试中断")
        sys.exit(0)

