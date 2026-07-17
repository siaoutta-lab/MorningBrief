import os
import requests
import json

def get_morning_brief():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("错误: 未配置有效的 GEMINI_API_KEY")
        return None

    # 换回通用且最稳定的请求路径，把密钥放在 headers 里或者作为 query 参数传递
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": "请帮我生成一份今天的科技与AI行业早报，包含3-5条核心新闻简述，语言要精炼。"
            }]
        }]
    }

    try:
        print("正在尝试请求 Gemini API...")
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            # 兼容处理返回的文本解析
            try:
                brief_text = result['candidates'][0]['content']['parts'][0]['text']
                print("早报生成成功！")
                return brief_text
            except Exception as parse_err:
                print(f"解析响应内容失败: {parse_err}")
                print(f"收到的完整响应: {result}")
                return None
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
        with open("brief.txt", "w", encoding="utf-8") as f:
            f.write(brief)
