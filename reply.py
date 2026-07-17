import os
import sys
import json
import urllib.request
import urllib.error

# 直接读取 GitHub Actions 自带的系统 Token，不需要你手动去加 Secrets 了！
api_key = os.environ.get("GITHUB_TOKEN")
if not api_key:
    # 兼容备用：如果你在本地测，或者配了别的名字
    api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("错误: 未配置有效的 Token")
    sys.exit(1)

# 使用 GitHub 官方免费提供给开发者的 API 终点（完全免费，且绝不封禁 Actions IP）
url = "https://models.inference.ai.azure.com/chat/completions"

data = {
    "model": "gpt-4o-mini", # 使用性能优异且完全免费的 gpt-4o-mini
    "messages": [
        {
            "role": "user",
            "content": "请帮我生成一份今天的早报简报，包含科技、财经和时事热点。"
        }
    ]
}

# 将数据转换为字节流，并设置 Header（注意：GitHub Models 要求必须带 User-Agent）
encoded_data = json.dumps(data).encode("utf-8")
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    "User-Agent": "GitHub-Actions-Script"
}

req = urllib.request.Request(url, data=encoded_data, headers=headers, method="POST")

try:
    # 发送请求
    with urllib.request.urlopen(req) as response:
        response_body = response.read().decode("utf-8")
        result = json.loads(response_body)
        
        # 解析并打印返回的文本
        reply_text = result["choices"][0]["message"]["content"]
        print("AI 早报回复内容：")
        print(reply_text)
        
except urllib.error.HTTPError as e:
    print(f"HTTP 请求失败，状态码: {e.code}")
    print(f"错误详情: {e.read().decode('utf-8')}")
    sys.exit(1)
except Exception as e:
    print(f"发生其他错误: {e}")
    sys.exit(1)
