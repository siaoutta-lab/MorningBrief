import os
import requests
import json

def get_morning_brief():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("错误: 未配置有效的 GEMINI_API_KEY")
        return None

    # 使用 39 号最熟悉的标准官方路径
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
        print("正在尝试请求 Gemini API (第 1 次)...")
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            brief_text = result['candidates'][0]['content']['parts'][0]['text']
            print("早报生成成功！")
            return brief_text
        else:
            # 如果谷歌又抽风限额，自动切换到硅基流动备份，确保 100% 成功
            print("官方接口受限，正在切换到备用稳定接口...")
            alt_url = "https://api.siliconflow.cn/v1/chat/completions"
            alt_headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            alt_data = {
                "model": "THUDM/glm-4-9b-chat",
                "messages": [{"role": "user", "content": "请帮我生成一份今天的科技与AI行业早报，包含3-5条核心新闻简述，语言要精炼。"}]
            }
            alt_resp = requests.post(alt_url, headers=alt_headers, json=alt_data)
            if alt_resp.status_code == 200:
                print("备用接口生成成功！")
                return alt_resp.json()['choices'][0]['message']['content']
            
            print(f"所有接口请求失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"请求发生异常: {e}")
        return None

if __name__ == "__main__":
    brief = get_morning_brief()
    if brief:
        # ⚠️ 关键修正：必须写入 brief_output.txt，后面的发邮件步骤才能找到它！
        with open("brief_output.txt", "w", encoding="utf-8") as f:
            f.write(brief)
        print("早报生成成功，文件已写入 brief_output.txt")
