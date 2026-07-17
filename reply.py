import os
import sys
import json
import urllib.request
import urllib.error

# 读取你刚刚在 GitHub Settings 里存的 Key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("错误: 未配置有效的 API Key")
    sys.exit(1)

# 使用硅基流动的免费大模型接口
url = "https://api.siliconflow.cn/v1/chat/completions"

data = {
    "model": "Qwen/Qwen2.5-7B-Instruct", # 完全免费且极聪明的语言模型
    "messages": [
        {
            "role": "user",
            "content": "请帮我生成一份今天的早报简报，包含科技、财经和时事热点。"
        }
    ]
}

# 转换数据并设置 Headers
encoded_data = json.dumps(data).encode("utf-8")
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

req = urllib.request.Request(url, data=encoded_data, headers=headers, method="POST")

try:
    with urllib.request.urlopen(req) as response:
        response_body = response.read().decode("utf-8")
        result = json.loads(response_body)
        
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
