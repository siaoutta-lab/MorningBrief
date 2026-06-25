import os
import http.client
import json

def get_morning_brief():
    # 1. 从 GitHub 保险箱中读取我们存好的 Key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found.")
        return

    # 2. 建立与 Google Gemini API 的连接
    conn = http.client.HTTPSConnection("generativelanguage.googleapis.com")
    
    # 3. 构造请求内容（让 Gemini 联网搜索最新科技/财经动态并生成简报）
    payload = json.dumps({
        "contents": [{
            "parts": [{
                "text": "请作为一名专业的新闻主编，利用你最新的联网搜索能力，搜集过去24小时全球最核心的科技、AI与财经动态。为我生成一份精致的《MorningBrief 晨间简报》。要求：1. 使用中文；2. 包含 3-5 条核心新闻；3. 每条新闻提供简短摘要，并附带可能的新闻线索或参考来源说明；4. 排版清晰、具备可读性。"
            }]
        }],
        # 开启 Google 搜索作为工具（实现实时联网功能）
        "tools": [{"google_search": {}}]
    })
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    # 4. 发送请求给 Gemini 1.5 Flash 模型
    url = f"/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    conn.request("POST", url, payload, headers)
    
    res = conn.getresponse()
    data = res.read()
    
    # 5. 解析并打印结果
    try:
        result = json.loads(data.decode("utf-8"))
        brief_text = result['candidates'][0]['content']['parts'][0]['text']
        print("\n" + "="*20 + " MorningBrief " + "="*20)
        print(brief_text)
        print("="*54 + "\n")
        
        # 将结果保存到本地，方便后续发送邮件或存档
        with open("brief_output.txt", "w", encoding="utf-8") as f:
            f.write(brief_text)
            
    except Exception as e:
        print("解析返回数据失败，错误信息:", e)
        print("原始返回数据:", data.decode("utf-8"))

if __name__ == "__main__":
    get_morning_brief()
