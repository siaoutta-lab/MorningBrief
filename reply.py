import os
import requests
import json

def get_morning_brief():
    # 从系统变量获取你刚刚填写的最新 Key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("错误: 未配置有效的 GEMINI_API_KEY")
        return None

    # 升级为最新的 v1beta 接口，完美兼容 AQ. 开头的新版 Key
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # 构造请求内容
    data = {
        "contents": [{
            "parts": [{
                "text": "请帮我生成一份今天的科技与AI行业早报，包含3-5条核心新闻简述，语言要精炼。"
            }]
        }]
    }

    try:
        print("正在尝试使用新接口请求 Gemini API...")
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            # 解析生成的文本内容
            brief_text = result['candidates'][0]['content']['parts'][0]['text']
            print("早报生成成功！")
            return brief_text
        else:
            print(f"HTTP 请求失败，状态码: {response.status_code}")
            print(f"错误详情: {response.text}")
            return None
    except Exception as e:
        print(f"请求发生异常: {e}")
        return None

if __name__ == "__main__":
    brief = get_morning_brief()
    if brief:
        # 将生成的早报写入临时文件，供后续步骤读取（例如发邮件或保存）
        with open("brief.txt", "w", encoding="utf-8") as f:
            f.write(brief)
