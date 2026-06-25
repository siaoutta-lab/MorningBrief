import os
import http.client
import json
import time

def get_morning_brief():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found.")
        return

    payload = json.dumps({
        "contents": [{
            "parts": [{
                "text": (
                    "请作为一名深耕东南亚及全球市场的专业新闻主编与资深金融科技评论员，利用你最新的联网搜索能力，"
                    "搜集过去24小时全球与东盟最核心的动态。严格按照以下要求的结构、标题和【逐句中英文对照】格式生成一份《MorningBrief | SEA Edition》。\n\n"
                    "【核心内容偏向】：\n"
                    "你的报道和分析必须具备强烈的 FinTech（金融科技）直觉，高度关注资本流动、数字结算基础设施、稳定币跨境应用、AI基础设施投资的ROI、以及东南亚科技出海的资金链动态。\n\n"
                    "【严格排版要求】：\n"
                    "1. 必须包含以下 1 至 7 的所有板块，板块名称和副标题必须与模板完全一致。\n"
                    "2. 所有新闻详情、分析、洞察，必须采用【一句英文、一句中文】的逐句对照格式。\n"
                    "3. 明确写出每一项的具体信息来源（Source 来源）。\n"
                    "4. 'Executive Insight 今日洞察' 和 'One-Line Takeaway 一句话总结' 必须深刻体现金融科技、数字资产结算、跨境资本流向与数字基础设施投资的融合视角。\n\n"
                    "【输出模板结构】：\n"
                    "MorningBrief | SEA Edition\n"
                    "[当前日期] | Bangkok Time\n"
                    "Global Events • Markets • FinTech • Technology • Energy • ASEAN\n\n"
                    "1. Top Stories\n"
                    "全球重大事件\n"
                    "[国旗] [英文新闻标题]\n"
                    "[中文新闻标题]\n"
                    "[英文详情描述]\n"
                    "[中文详情描述]\n"
                    "Why it matters | 为什么重要\n"
                    "[英文逻辑推导]\n"
                    "[中文逻辑推导]\n"
                    "Source 来源\n"
                    "[具体信源名称]\n\n"
                    "2. Markets\n"
                    "资本市场\n"
                    "Market Theme\n"
                    "今日市场主线\n"
                    "[中英文逐句对照]\n"
                    "What Investors Are Avoiding\n"
                    "资金相对回避\n"
                    "[中英文逐句对照]\n"
                    "Source 来源\n"
                    "[具体信源名称]\n\n"
                    "3. FinTech\n"
                    "金融科技\n"
                    "[中英文逐句对照]\n"
                    "Source 来源\n"
                    "[具体信源名称]\n\n"
                    "4. Technology\n"
                    "科技\n"
                    "[中英文逐句对照]\n"
                    "Source 来源\n"
                    "[具体信源名称]\n\n"
                    "5. Energy & Infrastructure\n"
                    "能源与基础设施\n"
                    "[中英文逐句对照]\n"
                    "Source 来源\n"
                    "[具体信源名称]\n\n"
                    "6. Thailand & ASEAN\n"
                    "泰国与东盟\n"
                    "[中英文逐句对照]\n"
                    "Source 来源\n"
                    "[具体信源名称]\n\n"
                    "7. Investment Watchlist\n"
                    "投资观察\n"
                    "Macro 宏观 / Technology 科技 / Energy 能源 / Thailand 泰国\n\n"
                    "Executive Insight\n"
                    "今日洞察\n"
                    "English\n"
                    "[英文洞察]\n"
                    "中文\n"
                    "[中文洞察]\n\n"
                    "Source Summary\n"
                    "今日信源统计\n"
                    "[列出所用信源表格]\n\n"
                    "One-Line Takeaway\n"
                    "一句话总结\n"
                    "[英文总结]\n"
                    "[中文总结]"
                )
            }]
        }],
        "tools": [{"google_search": {}}]
    })
    
    headers = {'Content-Type': 'application/json'}
    url = f"/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    # 核心升级：增加3次自动重试机制
    for attempt in range(1, 4):
        print(f"正在尝试请求 Gemini API (第 {attempt} 次)...")
        try:
            conn = http.client.HTTPSConnection("generativelanguage.googleapis.com")
            conn.request("POST", url, payload, headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            result = json.loads(data)
            
            if "error" in result:
                print(f"API 提示错误: {result['error']['message']}")
                if "demand" in result["error"]["message"].lower() and attempt < 3:
                    print("服务器拥堵，等待 5 秒后重试...")
                    time.sleep(5)
                    continue
                else:
                    raise Exception(result["error"]["message"])
            
            brief_text = result['candidates'][0]['content']['parts'][0]['text']
            
            # 成功拿到数据，写入文件
            with open("brief_output.txt", "w", encoding="utf-8") as f:
                f.write(brief_text)
            print("早报生成成功，文件已写入 brief_output.txt")
            return
            
        except Exception as e:
            print(f"当前尝试发生错误: {e}")
            if attempt < 3:
                print("等待 5 秒后尝试下一次重试...")
                time.sleep(5)
            else:
                # 如果试了3次都失败，强制写入一个错误说明文件，确保发邮件步骤不崩溃
                error_fallback = f"抱歉，今早由于 Gemini 服务器异常拥堵，未能成功抓取到新闻。具体错误原因: {e}"
                with open("brief_output.txt", "w", encoding="utf-8") as f:
                    f.write(error_fallback)
                print("已写入兜底错误报告，允许工作流继续发信。")

if __name__ == "__main__":
    get_morning_brief()
