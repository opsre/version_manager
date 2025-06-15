import requests
import os

# 配置
API_URL = "http://127.0.0.1:5000/api/v1"
VERSION_ID = 1  # 使用已创建的版本ID
UPLOADER_ID = 3  # 使用已创建的用户ID
TEST_FILE_PATH = "test.txt"  # 测试文件路径

# 创建测试文件
def create_test_file():
    with open(TEST_FILE_PATH, "w") as f:
        f.write("这是一个测试文件内容。\n" * 100)
    return os.path.abspath(TEST_FILE_PATH)

# 上传文件
def upload_file(file_path):
    print(f"准备上传文件: {file_path}")
    
    url = f"{API_URL}/files/upload"
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {
            'version_id': VERSION_ID,
            'uploader_id': UPLOADER_ID
        }
        
        try:
            response = requests.post(url, files=files, data=data)
            if response.status_code == 201:
                result = response.json()
                print(f"文件上传成功! ID: {result['id']}")
                return result
            else:
                print(f"上传失败: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"上传过程中出错: {str(e)}")
            return None

# 获取文件列表
def get_files():
    url = f"{API_URL}/files"
    params = {'version_id': VERSION_ID}
    
    try:
        response = requests.get(url, params=params)
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

# 下载文件
def download_file(file_id, output_path):
    url = f"{API_URL}/files/download/{file_id}"
    print(f"下载文件URL: {url}")
    
    try:
        response = requests.get(url, stream=True)
        print(f"下载响应状态码: {response.status_code}")
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
    # 创建测试文件
    file_path = create_test_file()
    print(f"测试文件已创建: {file_path}")
    
    # 上传文件
    uploaded_file = upload_file(file_path)
    
    if uploaded_file:
        # 获取文件列表
        files = get_files()
        
        if files and len(files) > 0:
            # 下载新上传的文件
            file_id = uploaded_file['id']  # 使用刚上传的文件ID
            download_path = f"downloaded_{os.path.basename(file_path)}"
            print(f"尝试下载文件ID: {file_id}")
            download_file(file_id, download_path) 