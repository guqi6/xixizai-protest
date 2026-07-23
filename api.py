# -*- coding: utf-8 -*-
"""西西崽小红书内容生成API"""
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

async def call_ai(messages: list, max_tokens: int = 8192) -> str:
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


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.post("/api/generate-xhs")
async def generate_xhs(request: Request):
    """流式生成小红书内容：标题→正文→3页SVG"""
    body = await request.json()
    ref_text = body.get("reference_text", "")
    ref_images = body.get("reference_images", [])  # base64 list
    product = body.get("product", "Zoho企业邮箱")

    async def stream():
        import queue as _q
        q = asyncio.Queue()

        async def emit(event_type, data):
            await q.put(f"data: {json.dumps({'type': event_type, **data}, ensure_ascii=False)}\n\n")

        async def worker():
            try:
                # ===== Step 1: 分析对标 + 生成标题 =====
                await emit("progress", {"step": 1, "label": "分析对标→生成标题"})
                await emit("log", {"msg": "📋 正在分析对标内容..."})

                title_prompt = f"""你是一位小红书爆款内容专家。请根据以下对标内容，为「{product}」生成3个小红书标题。

### 对标内容
{ref_text[:2000]}

### 要求
1. 分析对标的爆款元素（钩子、情绪、冲突点）
2. 生成3个不同风格的小红书标题
3. 标题要有冲突感/悬念/数字，让人想点进去
4. 不要太标题党，要和产品相关
5. 每个标题不超过20字

### 输出格式（严格JSON）
```json
{{"titles": ["标题1", "标题2", "标题3"]}}
```"""

                title_result = await call_ai([{"role": "user", "content": title_prompt}], max_tokens=2048)
                
                # 解析标题
                titles = []
                try:
                    m = re.search(r'\{[^}]*"titles"[^}]*\}', title_result, re.DOTALL)
                    if m:
                        titles = json.loads(m.group())["titles"]
                except:
                    pass
                if not titles:
                    # fallback: 按行提取
                    for line in title_result.split('\n'):
                        line = re.sub(r'^[\d\.\-\*）\s]+', '', line.strip())
                        if 5 < len(line) < 30 and not line.startswith('#'):
                            titles.append(line)
                    titles = titles[:3] or [f"{product}深度测评"]

                await emit("titles", {"titles": titles})
                await emit("log", {"msg": f"✅ 标题生成完成：{len(titles)}个"})

                # ===== Step 2: 生成正文 =====
                await emit("progress", {"step": 2, "label": "生成小红书正文"})
                await emit("log", {"msg": "✍️ 正在撰写正文..."})

                body_prompt = f"""你是一位小红书爆款写手。请为以下标题撰写一篇小红书推广正文。

### 选用标题（用第一个）
{titles[0]}

### 产品信息
{product} - 专业企业邮箱服务，支持自定义域名、多账号管理、日历协作、大附件发送。

### 对标参考风格
{ref_text[:1500]}

### 正文要求
1. 开头有钩子，让人想继续看
2. 分点说产品优势（3-4个核心卖点）
3. 融入测评体验感（像真人使用后的感受）
4. 结尾有互动引导
5. 适当用emoji但不要太多
6. 加5-8个相关标签（#企业邮箱 #外贸邮箱 等）
7. 总字数400-600字
8. 提到 protest.xixizai.com 测评站（让用户去测）

直接输出正文内容，不要代码块。"""

                body_result = await call_ai([{"role": "user", "content": body_prompt}], max_tokens=4096)
                article_body = body_result.strip()
                # 去掉可能的代码块包裹
                article_body = re.sub(r'^```\w*\s*', '', article_body)
                article_body = re.sub(r'\s*```$', '', article_body)

                await emit("body", {"content": article_body})
                await emit("log", {"msg": f"✅ 正文生成完成：{len(article_body)}字"})

                # ===== Step 3: 生成3页SVG =====
                await emit("progress", {"step": 3, "label": "生成配图（3页）"})
                
                svgs = []

                # 封面
                await emit("log", {"msg": "🎨 生成封面..."})
                cover_prompt = f"""你是SVG设计专家。生成一张小红书封面SVG。

### 要求
- 尺寸 1080×1440
- 主标题：{titles[0]}
- 副标题：{product}深度测评
- 配色：Zoho蓝色系 #4A7CF7 + 白色 + 高亮黄 #F5C842
- 风格：现代简洁，大字冲击力，有装饰元素
- 底部加 protest.xixizai.com 水印
- 标题文字不能溢出，内容多时用tspan换行
- 直接输出SVG代码，不要代码块

直接输出SVG："""

                cover_svg = await call_ai([{"role": "user", "content": cover_prompt}], max_tokens=4096)
                cover_svg = re.sub(r'^```\w*\s*', '', cover_svg).strip()
                cover_svg = re.sub(r'\s*```$', '', cover_svg).strip()
                svg_match = re.search(r'<svg.*?</svg>', cover_svg, re.DOTALL)
                if svg_match:
                    cover_svg = svg_match.group()
                svgs.append({"label": "封面", "svg": cover_svg})
                await emit("svg", {"index": 0, "label": "封面", "svg": cover_svg})
                await emit("log", {"msg": "✅ 封面完成"})

                # 测评截图1 - 测试中
                await emit("log", {"msg": "🎨 生成测评截图1..."})
                page2_prompt = f"""你是SVG设计专家。生成一张小红书配图SVG，模拟测评网站的测试页面截图。

### 要求
- 尺寸 1080×1440
- 内容：模拟 protest.xixizai.com 测评网站的一道测试题页面
- 页面顶部有「{product}适配度测评」标题栏
- 中间显示一道有趣的选择题（关于企业邮箱使用场景）
- 4个选项（A/B/C/D风格）
- 底部有进度条（第3题/共10题）
- 配色：绿色系 #2e7d32 + 白色背景 + 浅绿卡片
- 风格像真实的在线测评工具截图
- 底部加 protest.xixizai.com 水印
- 直接输出SVG代码，不要代码块

直接输出SVG："""

                page2_svg = await call_ai([{"role": "user", "content": page2_prompt}], max_tokens=4096)
                page2_svg = re.sub(r'^```\w*\s*', '', page2_svg).strip()
                page2_svg = re.sub(r'\s*```$', '', page2_svg).strip()
                svg_match = re.search(r'<svg.*?</svg>', page2_svg, re.DOTALL)
                if svg_match:
                    page2_svg = svg_match.group()
                svgs.append({"label": "测评页·答题中", "svg": page2_svg})
                await emit("svg", {"index": 1, "label": "测评页·答题中", "svg": page2_svg})
                await emit("log", {"msg": "✅ 测评截图1完成"})

                # 测评截图2 - 结果页
                await emit("log", {"msg": "🎨 生成测评截图2..."})
                page3_prompt = f"""你是SVG设计专家。生成一张小红书配图SVG，模拟测评网站的结果页面截图。

### 要求
- 尺寸 1080×1440
- 内容：模拟 protest.xixizai.com 测评网站的结果页
- 顶部显示「你的{product}适配度」
- 中间显示一个大分数（如 92分）和评级（如「高度匹配」）
- 下面列出3个匹配优势点（带emoji图标）
- 配色：绿色系 #2e7d32 + 金色高亮 #FFD700 + 白色背景
- 风格像真实的测评结果分享图
- 底部有「扫码去测」引导 + protest.xixizai.com 水印
- 直接输出SVG代码，不要代码块

直接输出SVG："""

                page3_svg = await call_ai([{"role": "user", "content": page3_prompt}], max_tokens=4096)
                page3_svg = re.sub(r'^```\w*\s*', '', page3_svg).strip()
                page3_svg = re.sub(r'\s*```$', '', page3_svg).strip()
                svg_match = re.search(r'<svg.*?</svg>', page3_svg, re.DOTALL)
                if svg_match:
                    page3_svg = svg_match.group()
                svgs.append({"label": "测评页·结果", "svg": page3_svg})
                await emit("svg", {"index": 2, "label": "测评页·结果", "svg": page3_svg})
                await emit("log", {"msg": "✅ 测评截图2完成"})

                # ===== 完成 =====
                await emit("progress", {"step": 4, "label": "全部完成"})
                await emit("done", {"titles": titles, "body": article_body, "svg_count": len(svgs)})
                await emit("log", {"msg": f"🎉 全部完成！{len(titles)}标题 + 正文 + {len(svgs)}配图"})

            except Exception as e:
                import traceback
                logger.error(f"生成失败: {traceback.format_exc()[-500:]}")
                await emit("error", {"msg": str(e)[:200]})

            await q.put(None)  # sentinel

        task = asyncio.create_task(worker())
        
        while True:
            try:
                item = await asyncio.wait_for(q.get(), timeout=200)
                if item is None:
                    break
                yield item
            except asyncio.TimeoutError:
                yield f"data: {json.dumps({'type': 'heartbeat', 'msg': '⏳ 仍在处理...'})}\n\n"

        await task

    return StreamingResponse(stream(), media_type="text/event-stream")


@app.get("/")
async def index():
    html = (Path(__file__).parent / "admin.html").read_text(encoding="utf-8")
    return HTMLResponse(html)
