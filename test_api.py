import requests
import json
import sys

def test_create_role():
    url = "http://localhost:5000/api/v1/roles"
    headers = {"Content-Type": "application/json"}
    data = {
        "name": "测试角色",
        "description": "测试描述"
    }
    
    print(f"正在测试URL: {url}")
    print(f"发送数据: {json.dumps(data, ensure_ascii=False)}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 404:
            print("错误: 404 Not Found - API端点不存在")
            print("可能的原因:")
            print("1. 应用未正确运行")
            print("2. URL路径不正确")
            print("3. 路由未正确注册")
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到服务器，请确保Flask应用正在运行")
    except Exception as e:
        print(f"发生错误: {str(e)}")
    
if __name__ == "__main__":
    test_create_role() 