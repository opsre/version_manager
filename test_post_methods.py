import requests
import os

# 配置
API_URL = "http://127.0.0.1:5000/api/v1"
VERSION_ID = 1  # 使用已创建的版本ID

# 使用POST方法获取文件列表
def get_files_with_post():
    url = f"{API_URL}/files"
    data = {'version_id': VERSION_ID}
    
    try:
        response = requests.post(url, data=data)
        print(f"文件列表请求状态码: {response.status_code}")
        if response.status_code == 200:
            files = response.json()
            print(f"找到 {len(files)} 个文件:")
            for i, file in enumerate(files):
                print(f"{i+1}. ID: {file['id']}, 文件名: {file['original_filename']}")
            return files
        else:
            print(f"获取文件列表失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"获取文件列表出错: {str(e)}")
        return None

# 使用POST方法下载文件
def download_file_with_post(file_id, output_path):
    url = f"{API_URL}/files/download/{file_id}"
    
    try:
        response = requests.post(url, stream=True)
        print(f"下载文件请求状态码: {response.status_code}")
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"文件下载成功: {output_path}")
            return True
        else:
            print(f"下载失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"下载过程中出错: {str(e)}")
        return False

if __name__ == "__main__":
    print("使用POST方法测试文件接口...")
    
    # 获取文件列表
    files = get_files_with_post()
    
    if files and len(files) > 0:
        # 下载第一个文件
        file_id = files[0]['id']
        download_path = f"post_downloaded_file_{file_id}.txt"
        print(f"尝试下载文件ID: {file_id}")
        download_file_with_post(file_id, download_path)
    else:
        print("没有找到文件，无法执行下载测试") 