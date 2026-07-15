import os
import http.client
import json
import time

def get_morning_brief():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found.")
        return

    # 重新构建了提示词，满足你的：
    # 1. 增加 The Nation, Bangkok Post, Thai Enquirer, Khaosod English 核心信源
    # 2. 宏观结构：国际 -> 东南亚 -> 泰国
    # 3. 泰国部分分类别：经济、政治、能源、科技、金融、民生，具体说事件
    # 4. 保留了你原有的中英文逐句对照、FinTech 直觉和一句话总结等优秀排版格式
    payload = json.dumps({
        "contents": [{
            "parts": [{
                "text": (
                    "请作为一名深耕东南亚及全球市场的专业新闻主编与资深金融科技评论员，利用你最新的联网搜索能力，"
                    "搜集过去24小时全球、东盟以及泰国的最核心动态。\n\n"
                    "【新增核心权威信源】：\n"
                    "在检索和生成泰国与东盟内容时，请务必重点参考并引入来自 The Nation (泰国民族报)、Bangkok Post (曼谷邮报)、"
                    "Thai Enquirer 以及 Khaosod English 的最新报道与核心评论。全球动态部分可参考麦肯锡、BBC、FT等。\n\n"
                    "【核心内容偏向】：\n"
                    "你的报道和分析必须具备强烈的 FinTech（金融科技）直觉，高度关注资本流动、数字结算基础设施、稳定币跨境应用、AI基础设施投资、以及东南亚科技出海的资金链动态。\n\n"
                    "【严格排版要求】：\n"
                    "1. 必须严格按照以下要求的结构、标题和【逐句中英文对照】格式生成。板块名称和副标题必须与模板完全一致。\n"
                    "2. 所有新闻详情、分析、洞察，必须采用【一句英文、一句中文】的逐句对照格式。\n"
                    "3. 明确写出每一项的具体信息来源（Source 来源）。\n\n"
                    "【输出模板结构】：\n"
                    "MorningBrief | SEA Edition\n"
                    "[当前日期] | Bangkok Time\n"
                    "Global Events • ASEAN • Thailand Deep-Dive\n\n"
                    "1. International Dynamic\n"
                    "国际动态\n"
                    "Economy & Finance | 经济与金融\n"
                    "[中英文逐句对照事件详情]\n"
                    "Politics & Energy | 政治与能源\n"
                    "[中英文逐句对照事件详情]\n"
                    "Technology & Society | 科技与民生\n"
                    "[中英文逐句对照事件详情]\n"
                    "Source 来源\n"
                    "[具体信源名称]\n\n"
                    "2. ASEAN Focus\n"
                    "东南亚聚焦\n"
                    "Economy & Finance | 经济与金融\n"
                    "[中英文逐句对照事件详情]\n"
                    "Politics & Energy | 政治与能源\n"
                    "[中英文逐句对照事件详情]\n"
                    "Technology & Society | 科技与民生\n"
                    "[中英文逐句对照事件详情]\n"
                    "Source 来源\n"
                    "[具体信源名称]\n\n"
                    "3. Thailand Deep-Dive\n"
                    "泰国专栏\n"
                    "Economy | 经济\n"
                    "[中英文逐句对照具体事件]\n"
                    "Politics | 政治\n"
                    "[中英文逐句对照具体事件]\n"
                    "Energy | 能源\n"
                    "[中英文逐句对照具体事件]\n"
                    "Technology | 科技\n"
                    "[中英文逐句对照具体事件]\n"
                    "Finance | 金融\n"
                    "[中英文逐句对照具体事件]\n"
                    "People's Livelihood | 民生\n"
                    "[中英文逐句对照具体事件]\n"
                    "Source 来源\n"
                    "[列出具体的泰国媒体来源，如 Bangkok Post, The Nation 等]\n\n"
                    "4. Investment Watchlist\n"
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
                error_fallback = f"抱歉，今早由于 Gemini 服务器异常拥堵，未能成功抓取到新闻。具体错误原因: {e}"
                with open("brief_output.txt", "w", encoding="utf-8") as f:
                    f.write(error_fallback)
                print("已写入兜底错误报告，允许工作流继续发信。")

if __name__ == "__main__":
    get_morning_brief()
