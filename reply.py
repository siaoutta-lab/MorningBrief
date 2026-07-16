import os
import sys
import json
import urllib.request
import urllib.error

# 从环境变量中获取 API Key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("错误: 未配置 GEMINI_API_KEY 环境变量")
    sys.exit(1)

# 【终极修复】使用目前最兼容的 2.0 稳定版模型路径
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
data = {
    "contents": [
        {
            "parts": [
                {"text": "请帮我生成一份今天的早报简报，包含科技、财经和时事热点。"}
            ]
        }
    ]
}

# 将数据转换为字节流，并设置 Header
encoded_data = json.dumps(data).encode("utf-8")
headers = {"Content-Type": "application/json"}
req = urllib.request.Request(url, data=encoded_data, headers=headers, method="POST")

try:
    # 发送请求
    with urllib.request.urlopen(req) as response:
        response_body = response.read().decode("utf-8")
        result = json.loads(response_body)
        
        # 解析并打印返回的文本
        reply_text = result["candidates"][0]["content"]["parts"][0]["text"]
        print("Gemini 回复内容：")
        print(reply_text)

except urllib.error.HTTPError as e:
    print(f"HTTP 请求失败，状态码: {e.code}")
    print(f"错误详情: {e.read().decode('utf-8')}")
    sys.exit(1)
except Exception as e:
    print(f"发生其他错误: {e}")
    sys.exit(1)
