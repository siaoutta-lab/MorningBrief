import os
import sys
import json
import requests

# 从环境变量中获取 API Key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("错误: 未配置 GEMINI_API_KEY 环境变量")
    sys.exit(1)

# 构建请求的 URL 和 Payload
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
headers = {"Content-Type": "application/json"}
payload = {
    "contents": [
        {
            "parts": [
                {"text": "请帮我生成一份今天的早报简报，包含科技、财经和时事热点。"}
            ]
        }
    ]
}

try:
    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    # 解析并打印返回的文本
    result = response.json()
    reply_text = result["candidates"][0]["content"]["parts"][0]["text"]
    print("Gemini 回复内容：")
    print(reply_text)
    
except Exception as e:
    print(f"请求失败: {e}")
    if 'response' in locals() and response.text:
        print(f"错误详情: {response.text}")
    sys.exit(1)
