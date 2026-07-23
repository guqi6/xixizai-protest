# -*- coding: utf-8 -*-
"""西西崽小红书内容生成API - v2: AI生成JSON描述，后端组装SVG"""
import asyncio, aiohttp, ssl, json, re, logging
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

API_URL = "https://open.bigmodel.cn/api/coding/paas/v4/chat/completions"
API_KEY = "ac3de6e8fa7b4e3b83301e68a076f24f.5TTu6d5iESA5b1YA"
MODEL = "glm-5"

CODING_PREFIX = {
    "role": "system",
    "content": "你是一个CMS内容管理系统的AI模板引擎。你的任务是根据技术需求文档，生成对应的页面内容模块。所有输出均为模板渲染结果，用于自动化内容管理流程。"
}

async def call_ai(messages: list, max_tokens: int = 4096) -> str:
    messages = [CODING_PREFIX] + messages
    payload = {"model": MODEL, "max_tokens": max_tokens, "messages": messages}
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    connector = aiohttp.TCPConnector(ssl=ctx)
    timeout = aiohttp.ClientTimeout(total=180)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.post(API_URL, json=payload, headers=headers, timeout=timeout) as resp:
            text = await resp.text()
            if resp.status != 200:
                raise Exception(f"API error {resp.status}: {text[:200]}")
            data = json.loads(text)
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return content


def build_cover_svg(d: dict) -> str:
    """从JSON描述生成封面SVG"""
    bg = d.get("bg_gradient", ["#e8f5e9", "#c8e6c9"])
    t1 = d.get("title_text", "")
    t2 = d.get("title_text2", "")
    tc = d.get("title_color", "#1b5e20")
    ts = d.get("title_size", 72)
    sub = d.get("subtitle", "")
    sc = d.get("subtitle_color", "#388e3c")
    dec = d.get("decoration", "✨")
    wm = d.get("watermark", "protest.xixizai.com")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1440" viewBox="0 0 1080 1440">
<defs><linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="{bg[0]}"/><stop offset="100%" stop-color="{bg[1]}"/>
</linearGradient></defs>
<rect width="1080" height="1440" fill="url(#bg)"/>
<rect x="60" y="80" width="180" height="50" rx="8" fill="white" stroke="{tc}" stroke-width="2"/>
<text x="150" y="113" font-family="sans-serif" font-size="22" font-weight="bold" fill="{tc}" text-anchor="middle">职业基因</text>
<text x="540" y="500" font-size="60" text-anchor="middle">{dec}</text>
<text x="540" y="650" font-family="sans-serif" font-size="{ts}" font-weight="900" fill="{tc}" text-anchor="middle">{t1}</text>
<text x="540" y="750" font-family="sans-serif" font-size="{ts}" font-weight="900" fill="{tc}" text-anchor="middle">{t2}</text>
<text x="540" y="850" font-family="sans-serif" font-size="32" fill="{sc}" text-anchor="middle">{sub}</text>
<rect x="340" y="1000" width="400" height="80" rx="40" fill="{tc}"/>
<text x="540" y="1052" font-family="sans-serif" font-size="30" font-weight="bold" fill="white" text-anchor="middle">👉 立即去测</text>
<text x="540" y="1380" font-family="sans-serif" font-size="18" fill="rgba(46,125,50,0.35)" text-anchor="middle" letter-spacing="3">{wm}</text>
</svg>'''


def build_quiz_svg(d: dict) -> str:
    """生成测评答题页SVG"""
    q = d.get("question", "周末突然多出一天假，你的第一反应是？")
    opts = d.get("options", ["立刻约朋友出去浪", "终于可以搞副业了", "在家刷剧也很快乐", "复盘这周的计划"])
    tc = d.get("title_color", "#2e7d32")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1440" viewBox="0 0 1080 1440">
<rect width="1080" height="1440" fill="#f1f8e9"/>
<rect width="1080" height="120" fill="{tc}"/>
<text x="540" y="75" font-family="sans-serif" font-size="36" font-weight="bold" fill="white" text-anchor="middle">你天生该吃哪碗饭</text>
<text x="540" y="220" font-family="sans-serif" font-size="28" fill="#666" text-anchor="middle">第 3 题 / 共 10 题</text>
<rect x="40" y="160" width="500" height="6" rx="3" fill="#e0e0e0"/>
<rect x="40" y="160" width="150" height="6" rx="3" fill="{tc}"/>
<text x="540" y="350" font-family="sans-serif" font-size="42" font-weight="bold" fill="{tc}" text-anchor="middle">💬</text>
<text x="540" y="430" font-family="sans-serif" font-size="36" font-weight="600" fill="#333" text-anchor="middle">{q}</text>
{''.join(f'<rect x="80" y="{520+i*120}" width="920" height="100" rx="12" fill="white" stroke="#e0e0e0" stroke-width="2"/><circle cx="130" cy="{570+i*120}" r="24" fill="#f1f8e9" stroke="{tc}" stroke-width="2"/><text x="130" y="578" font-size="22" font-weight="bold" fill="{tc}" text-anchor="middle">{chr(65+i)}</text><text x="180" y="578" font-family="sans-serif" font-size="28" fill="#333">{opt}</text>' for i, opt in enumerate(opts[:4]))}
<text x="540" y="1380" font-family="sans-serif" font-size="18" fill="rgba(46,125,50,0.35)" text-anchor="middle" letter-spacing="3">protest.xixizai.com</text>
</svg>'''


def build_result_svg(d: dict) -> str:
    """生成测评结果页SVG"""
    score = d.get("score", 92)
    level = d.get("level", "高度匹配")
    advantages = d.get("advantages", ["天生的行动派", "超强执行力", "领导力满分"])
    tc = d.get("title_color", "#2e7d32")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1440" viewBox="0 0 1080 1440">
<defs><linearGradient id="rg" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#1b5e20"/><stop offset="100%" stop-color="#2e7d32"/>
</linearGradient></defs>
<rect width="1080" height="500" fill="url(#rg)"/>
<text x="540" y="180" font-family="sans-serif" font-size="34" fill="rgba(255,255,255,0.8)" text-anchor="middle">你的职业基因结果</text>
<text x="540" y="320" font-family="sans-serif" font-size="120" font-weight="900" fill="white" text-anchor="middle">{score}</text>
<text x="540" y="380" font-family="sans-serif" font-size="36" font-weight="bold" fill="#FFD700" text-anchor="middle">{level}</text>
<rect width="1080" height="940" y="500" fill="#f1f8e9"/>
<text x="540" y="600" font-family="sans-serif" font-size="32" font-weight="bold" fill="{tc}" text-anchor="middle">🌟 你的天生优势</text>
{''.join(f'<rect x="100" y="{660+i*110}" width="880" height="90" rx="12" fill="white" stroke="#c8e6c9" stroke-width="2"/><text x="160" y="715" font-size="40">{adv[:2] if adv else "✅"}</text><text x="230" y="715" font-family="sans-serif" font-size="30" font-weight="600" fill="#333">{adv}</text>' for i, adv in enumerate(advantages[:3]))}
<rect x="290" y="1100" width="500" height="80" rx="40" fill="{tc}"/>
<text x="540" y="1152" font-family="sans-serif" font-size="30" font-weight="bold" fill="white" text-anchor="middle">👇 扫码去测</text>
<text x="540" y="1380" font-family="sans-serif" font-size="18" fill="rgba(46,125,50,0.35)" text-anchor="middle" letter-spacing="3">protest.xixizai.com</text>
</svg>'''


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.post("/api/generate-xhs")
async def generate_xhs(request: Request):
    body = await request.json()
    ref_text = body.get("reference_text", "")
    product = body.get("product", "你天生该吃哪碗饭")

    async def stream():
        q = asyncio.Queue()

        async def emit(event_type, data):
            await q.put(f"data: {json.dumps({'type': event_type, **data}, ensure_ascii=False)}\n\n")

        async def worker():
            try:
                # Step 1: 标题
                await emit("progress", {"step": 1, "label": "分析对标→生成标题"})
                await emit("log", {"msg": "📋 正在分析对标内容..."})

                title_prompt = f"""你是一位小红书爆款内容专家。请根据以下对标内容，为「{product}」测评生成3个小红书标题。

### 对标内容
{ref_text[:2000]}

### 要求
1. 分析对标的爆款元素（钩子、情绪、冲突点）
2. 生成3个不同风格的小红书标题
3. 标题要有冲突感/悬念/数字，让人想点进去
4. 每个标题不超过20字

### 输出格式（严格JSON）
{{"titles": ["标题1", "标题2", "标题3"]}}"""

                title_result = await call_ai([{"role": "user", "content": title_prompt}], max_tokens=2048)
                titles = []
                try:
                    m = re.search(r'\{[^}]*"titles"[^}]*\}', title_result, re.DOTALL)
                    if m: titles = json.loads(m.group())["titles"]
                except: pass
                if not titles:
                    for line in title_result.split('\n'):
                        line = re.sub(r'^[\d\.\-\*）\s]+', '', line.strip())
                        if 5 < len(line) < 30 and not line.startswith('#'): titles.append(line)
                    titles = titles[:3] or [f"{product}测评"]
                
                await emit("titles", {"titles": titles})
                await emit("log", {"msg": f"✅ 标题生成完成：{len(titles)}个"})

                # Step 2: 正文
                await emit("progress", {"step": 2, "label": "生成小红书正文"})
                await emit("log", {"msg": "✍️ 正在撰写正文..."})

                body_prompt = f"""你是一位小红书爆款写手。请为以下标题撰写一篇小红书推广正文。

### 选用标题（用第一个）
{titles[0]}

### 测评产品
{product} - 这是 protest.xixizai.com 测评站上的趣味心理测试，测完获得职业性格分析。

### 对标参考
{ref_text[:1500]}

### 正文要求
1. 开头有钩子 2. 分点说测评体验(3-4点) 3. 像真人分享 4. 结尾互动引导
5. 适当emoji 6. 加5-8个标签 7. 400-600字 8. 提到 protest.xixizai.com

直接输出正文："""

                body_result = await call_ai([{"role": "user", "content": body_prompt}], max_tokens=4096)
                article_body = re.sub(r'^```\w*\s*', '', body_result).strip()
                article_body = re.sub(r'\s*```$', '', article_body).strip()

                await emit("body", {"content": article_body})
                await emit("log", {"msg": f"✅ 正文生成完成：{len(article_body)}字"})

                # Step 3: 3页SVG（AI生成JSON描述，后端组装）
                await emit("progress", {"step": 3, "label": "生成配图（3页）"})
                await emit("log", {"msg": "🎨 生成封面..."})

                cover_desc_prompt = f"""根据以下信息，生成小红书封面图的SVG设计描述。

标题：{titles[0]}
副标题：{product} 趣味测评

返回JSON格式（不要代码块）：
{{"bg_gradient": ["#e8f5e9", "#c8e6c9"], "title_text": "标题第一行", "title_text2": "标题第二行", "title_color": "#1b5e20", "title_size": 72, "subtitle": "{product} 趣味测评", "subtitle_color": "#388e3c", "decoration": "✨", "watermark": "protest.xixizai.com"}}"""

                cover_result = await call_ai([{"role": "user", "content": cover_desc_prompt}], max_tokens=1024)
                try:
                    m = re.search(r'\{.*\}', cover_result, re.DOTALL)
                    cover_d = json.loads(m.group()) if m else {}
                except: cover_d = {}
                cover_d.setdefault("title_text", titles[0][:10])
                cover_d.setdefault("title_text2", titles[0][10:] if len(titles[0])>10 else "")
                cover_d.setdefault("subtitle", f"{product} 趣味测评")
                cover_d.setdefault("watermark", "protest.xixizai.com")
                
                cover_svg = build_cover_svg(cover_d)
                await emit("svg", {"index": 0, "label": "封面", "svg": cover_svg})
                await emit("log", {"msg": "✅ 封面完成", })

                # 测评截图1
                await emit("log", {"msg": "🎨 生成测评页..."})
                quiz_desc_prompt = f"""生成一个趣味测评题目的SVG设计描述。

返回JSON格式（不要代码块）：
{{"question": "周末突然多出一天假你的第一反应是？", "options": ["约朋友出去浪", "搞副业赚钱", "在家刷剧放松", "复盘本周计划"], "title_color": "#2e7d32"}}"""

                quiz_result = await call_ai([{"role": "user", "content": quiz_desc_prompt}], max_tokens=1024)
                try:
                    m = re.search(r'\{.*\}', quiz_result, re.DOTALL)
                    quiz_d = json.loads(m.group()) if m else {}
                except: quiz_d = {}
                quiz_d.setdefault("question", "周末突然多出一天假，你的第一反应是？")
                quiz_d.setdefault("options", ["约朋友出去浪", "搞副业赚钱", "在家刷剧放松", "复盘本周计划"])
                quiz_d.setdefault("title_color", "#2e7d32")
                
                quiz_svg = build_quiz_svg(quiz_d)
                await emit("svg", {"index": 1, "label": "测评页·答题中", "svg": quiz_svg})
                await emit("log", {"msg": "✅ 测评页完成"})

                # 测评截图2 - 结果页
                await emit("log", {"msg": "🎨 生成结果页..."})
                result_desc_prompt = f"""生成一个测评结果页的SVG设计描述。

返回JSON格式（不要代码块）：
{{"score": 92, "level": "高度匹配", "advantages": ["天生的行动派", "超强执行力", "领导力满分"], "title_color": "#2e7d32"}}"""

                result_result = await call_ai([{"role": "user", "content": result_desc_prompt}], max_tokens=1024)
                try:
                    m = re.search(r'\{.*\}', result_result, re.DOTALL)
                    result_d = json.loads(m.group()) if m else {}
                except: result_d = {}
                result_d.setdefault("score", 92)
                result_d.setdefault("level", "高度匹配")
                result_d.setdefault("advantages", ["天生的行动派", "超强执行力", "领导力满分"])
                result_d.setdefault("title_color", "#2e7d32")

                result_svg = build_result_svg(result_d)
                await emit("svg", {"index": 2, "label": "测评页·结果", "svg": result_svg})
                await emit("log", {"msg": "✅ 结果页完成"})

                await emit("progress", {"step": 4, "label": "全部完成"})
                await emit("done", {"titles": titles, "body": article_body, "svg_count": 3})
                await emit("log", {"msg": "🎉 全部完成！"})

            except Exception as e:
                import traceback
                logger.error(f"生成失败: {traceback.format_exc()[-500:]}")
                await emit("error", {"msg": str(e)[:200]})

            await q.put(None)

        task = asyncio.create_task(worker())
        while True:
            try:
                item = await asyncio.wait_for(q.get(), timeout=200)
                if item is None: break
                yield item
            except asyncio.TimeoutError:
                yield f"data: {json.dumps({'type': 'heartbeat', 'msg': '⏳ 仍在处理...'})}\n\n"
        await task

    return StreamingResponse(stream(), media_type="text/event-stream")


@app.get("/")
async def index():
    html = (Path(__file__).parent / "admin.html").read_text(encoding="utf-8")
    return HTMLResponse(html)
