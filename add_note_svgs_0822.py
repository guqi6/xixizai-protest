#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-08-22 给10篇新笔记（第6-15篇）生成SVG封面 + admin批量下载功能"""
import io, sys

FONT = "PingFang SC,Microsoft YaHei,sans-serif"

def text(x, y, s, size, fill, w=800, anchor='start', opacity=None):
    op = ' opacity="%s"' % opacity if opacity else ''
    return ('<text x="%s" y="%s" text-anchor="%s" font-family="%s" font-size="%s" '
            'font-weight="%s" fill="%s"%s>%s</text>') % (x, y, anchor, FONT, size, w, fill, op, s)

# ============ A组：暖橙奶油系（天生吃哪碗饭系列，编号6-10） ============
def makeA(lead, l1, hl, l2, big, ask):
    hl_size = 88
    hl_w = len(hl) * (hl_size + 6) + 56
    s = []
    s.append('<svg xmlns="http://www.w3.org/2000/svg" width="1242" height="1660" viewBox="0 0 1242 1660">')
    s.append('<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#FFF9EC"/><stop offset="100%" stop-color="#FFE8CB"/></linearGradient>')
    s.append('<filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#C77E2E" flood-opacity=".18"/></filter></defs>')
    s.append('<rect width="1242" height="1660" fill="url(#bg)"/>')
    s.append('<circle cx="1095" cy="148" r="210" fill="#FFD9A0" opacity=".5"/>')
    s.append('<circle cx="96" cy="1478" r="255" fill="#FFD0DE" opacity=".28"/>')
    s.append('<text x="104" y="256" font-family="Arial, sans-serif" font-size="230" font-weight="900" fill="#FFB86B" opacity=".42">&#8220;</text>')
    # 顶部标签
    s.append('<g filter="url(#sh)"><rect x="106" y="312" width="330" height="76" rx="38" fill="#2F2730"/></g>')
    s.append(text(271, 363, '天赋｜职业方向', 33, '#FFFFFF', 700, 'middle'))
    # 正文行
    if lead:
        s.append(text(105, 498, lead, 58, '#A08055', 700))
        y1, yh, y2, y3, ydiv, yask = 655, 700, 975, 1150, 1250, 1338
        s.append(text(105, y1, l1, 80, '#3D2E1E', 800))
        s.append('<g filter="url(#sh)"><rect x="95" y="%d" width="%d" height="140" rx="24" fill="#FF7A2F"/></g>' % (yh, hl_w))
        s.append(text(123, yh + 97, hl, hl_size, '#FFFFFF', 900))
        s.append(text(105, y2, l2, 78, '#3D2E1E', 800))
        s.append(text(105, y3, big, 126, '#FF5B2E', 900))
    else:
        y1, yh, y2, y3, ydiv, yask = 575, 618, 890, 1068, 1172, 1262
        s.append(text(105, y1, l1, 80, '#3D2E1E', 800))
        s.append('<g filter="url(#sh)"><rect x="95" y="%d" width="%d" height="140" rx="24" fill="#FF7A2F"/></g>' % (yh, hl_w))
        s.append(text(123, yh + 97, hl, hl_size, '#FFFFFF', 900))
        s.append(text(105, y2, l2, 78, '#3D2E1E', 800))
        s.append(text(105, y3, big, 126, '#FF5B2E', 900))
    # 分割线+提问+收藏
    s.append('<rect x="105" y="%d" width="1032" height="3" rx="2" fill="#F0C89A"/>' % ydiv)
    s.append(text(105, yask, ask, 46, '#8A6D4F', 700))
    s.append('<g filter="url(#sh)"><rect x="105" y="1400" width="410" height="90" rx="45" fill="#F97316"/></g>')
    s.append(text(310, 1458, '♡ 建议先收藏', 39, '#FFFFFF', 800, 'middle'))
    s.append('<circle cx="1078" cy="1442" r="18" fill="#2BB8A0"/>')
    s.append('<circle cx="1133" cy="1394" r="11" fill="#FF9BBB"/>')
    s.append('<path d="M1032 1508 C1078 1462 1121 1474 1158 1422" fill="none" stroke="#FFC48A" stroke-width="10" stroke-linecap="round"/>')
    s.append('</svg>')
    return ''.join(s)

# ============ B组：深蓝紫星空金冠系（高阶系列，编号11-15） ============
STARS = [(180,120,4,.5),(380,80,3,.35),(620,150,5,.25),(860,90,3,.4),(1080,200,4,.5),(240,900,3,.2),
         (1140,760,4,.3),(980,1150,3,.25),(150,1180,4,.3),(1060,960,2,.4),(90,700,3,.25),(760,60,2,.35)]
def makeB(mtype, q, hl, sub1, sub2, ask, swap=False):
    hl_size = 84
    hl_w = len(hl) * (hl_size + 6) + 56
    s = []
    s.append('<svg xmlns="http://www.w3.org/2000/svg" width="1242" height="1660" viewBox="0 0 1242 1660">')
    s.append('<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#241D47"/><stop offset="100%" stop-color="#3B2F72"/></linearGradient>')
    s.append('<filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#000000" flood-opacity=".35"/></filter>')
    s.append('<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="0" stdDeviation="18" flood-color="#FFC94D" flood-opacity=".55"/></filter></defs>')
    s.append('<rect width="1242" height="1660" fill="url(#bg)"/>')
    for cx, cy, r, op in STARS:
        s.append('<circle cx="%d" cy="%d" r="%d" fill="#FFFFFF" opacity="%s"/>' % (cx, cy, r, op))
    # 顶部标签（金底黑字）
    s.append('<g filter="url(#sh)"><rect x="106" y="312" width="360" height="76" rx="38" fill="#FFC94D"/></g>')
    s.append(text(286, 363, 'MBTI｜阶位自查', 33, '#241C42', 800, 'middle'))
    # 皇冠
    cx0 = 621
    s.append('<g filter="url(#glow)"><path d="M%d 516 L%d 474 L%d 496 L%d 462 L%d 496 L%d 474 L%d 516 Z" fill="#FFC94D"/></g>'
             % (cx0 - 100, cx0 - 72, cx0 - 36, cx0, cx0 + 36, cx0 + 72, cx0 + 100))
    s.append('<circle cx="%d" cy="466" r="7" fill="#FFE08A"/><circle cx="%d" cy="452" r="9" fill="#FFE08A"/><circle cx="%d" cy="466" r="7" fill="#FFE08A"/>'
             % (cx0 - 72, cx0, cx0 + 72))
    # 型号大字
    s.append('<g filter="url(#glow)">%s</g>' % text(cx0, 668, mtype, 150, '#FFD24D', 900, 'middle'))
    # 问句
    s.append(text(cx0, 778, q, 62, '#FFFFFF', 800, 'middle'))
    # 高亮块 / 白行（可交换顺序）
    if not swap:
        s.append('<g filter="url(#sh)"><rect x="%d" y="830" width="%d" height="135" rx="24" fill="#3ECFB2"/></g>' % (cx0 - hl_w // 2, hl_w))
        s.append(text(cx0, 928, hl, hl_size, '#17303B', 900, 'middle'))
        s.append(text(cx0, 1092, sub1, 76, '#EDE9FF', 900, 'middle'))
    else:
        s.append(text(cx0, 912, sub1, 72, '#EDE9FF', 900, 'middle'))
        s.append('<g filter="url(#sh)"><rect x="%d" y="950" width="%d" height="135" rx="24" fill="#3ECFB2"/></g>' % (cx0 - hl_w // 2, hl_w))
        s.append(text(cx0, 1048, hl, hl_size, '#17303B', 900, 'middle'))
    s.append(text(cx0, 1180, sub2, 42, '#B4A6E8', 600, 'middle'))
    # 分割线+提问+收藏
    s.append('<rect x="105" y="1240" width="1032" height="3" rx="2" fill="#FFFFFF" opacity=".16"/>')
    s.append(text(105, 1338, ask, 46, '#CFC4F0', 700))
    s.append('<g filter="url(#sh)"><rect x="105" y="1400" width="410" height="90" rx="45" fill="#FFC94D"/></g>')
    s.append(text(310, 1458, '♡ 建议先收藏', 39, '#241C42', 800, 'middle'))
    s.append('<circle cx="1078" cy="1442" r="18" fill="#3ECFB2"/>')
    s.append('<circle cx="1133" cy="1394" r="11" fill="#FFC94D"/>')
    s.append('<path d="M1032 1508 C1078 1462 1121 1474 1158 1422" fill="none" stroke="#8F7BE0" stroke-width="10" stroke-linecap="round"/>')
    s.append('</svg>')
    return ''.join(s)

NOTES_SVG = [
    # 第6篇 天生吃哪碗饭
    ('你从小被夸到大的那个特点，就是你的饭碗',
     makeA(None, '你从小被夸到大的', '那个特点', '就是你的', '饭碗', '你被夸得最多的是什么？')),
    # 第7篇
    ('命运其实早就暗示过你，你一做就忘记时间的那件事',
     makeA('命运其实早就暗示过你', '你一做就', '忘记时间', '的那件事', '', '你上次忘记时间在做什么？')),
    # 第8篇
    ('你最容易生气的地方，藏着你天生该吃的那碗饭',
     makeA(None, '你最容易', '生气的地方', '藏着你的', '那碗饭', '你最忍不了什么？')),
    # 第9篇
    ('命运其实早就暗示过你，你绕来绕去绕回去的那个领域',
     makeA('命运其实早就暗示过你', '绕来绕去', '还是绕回去', '的那个领域', '', '你总绕回哪个领域？')),
    # 第10篇
    ('你讲起来两眼放光的东西，就是你该吃的那碗饭',
     makeA(None, '你讲起来', '两眼放光', '的东西，就是', '你的饭碗', '你聊什么会两眼放光？')),
    # 第11篇 高阶系列
    ('ISTP的高阶到底长什么样？他一天只说十句话，句句值钱',
     makeB('ISTP', '的高阶到底长什么样？', '一天十句话', '句句值钱', '不是冷漠，是节能', '你是话少的ISTP吗？')),
    # 第12篇
    ('ESFP的高阶到底有多可怕？她把全场变成自己的主场',
     makeB('ESFP', '的高阶到底有多可怕？', '她把全场变成', '自己的主场', '不是讨好，是掌控', '你一上台是兴奋还是想吐？')),
    # 第13篇（白行在前做对比）
    ('ESTP的高阶到底长什么样？别人还在开会，他已经把事办完了',
     makeB('ESTP', '的高阶到底长什么样？', '事已办完', '别人还在开会', '不是莽，是快准', '你是先干再说的人吗？', swap=True)),
    # 第14篇
    ('ISTJ的高阶到底有多可怕？他记得每一处细节，包括你没兑现的那句承诺',
     makeB('ISTJ', '的高阶到底有多可怕？', '他全都记得', '三个月前的原话', '细节即权力', '你说过的话敢不敢认？')),
    # 第15篇
    ('ESFJ的高阶到底有多可怕？她让所有人都舒服，但没人能拿捏她',
     makeB('ESFJ', '的高阶到底有多可怕？', '温柔，但有盾', '没人能拿捏她', '不是讨好，是本事', '你能笑着拒绝吗？')),
]

# 第7/9篇没有big词，布局上l2即收尾 → 微调：把l2字号放大些
# （生成时lead版l2字号78已可，不额外处理）

with io.open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1) 注入svg字段
count = 0
for title, svg in NOTES_SVG:
    old = "{title:'%s',imagePrompt:" % title
    assert html.count(old) == 1, 'anchor not unique: ' + title
    assert "'" not in svg, 'svg contains quote: ' + title
    html = html.replace(old, "{title:'%s',svg:'%s',imagePrompt:" % (title, svg))
    count += 1
print('svg injected:', count)

# 2) renderNotes 里加封面渲染块（插在AI首图提示词块之前）
anchor2 = "if(n.imagePrompt){h+='<div class=\"field\"><div class=\"field-label\"><span>🎨 AI首图提示词</span>"
assert html.count(anchor2) == 1, 'renderNotes anchor not unique'
svg_render = ("if(n.svg){h+='<div class=\"field\"><div class=\"field-label\"><span>\\ud83d\\uddbc\\ufe0f 封面SVG</span>"
              "<span><button class=\"copy-btn\" onclick=\"dlNoteSvg('+i+')\">\\u2b07\\ufe0fSVG</button> "
              "<button class=\"copy-btn\" onclick=\"dlNoteJpg('+i+')\">\\u2b07\\ufe0fJPG</button> "
              "<button class=\"copy-btn\" onclick=\"copyNoteSvg('+i+')\">\\ud83d\\udccb复制代码</button></span></div>"
              "<div style=\"margin-top:6px\"><img src=\"data:image/svg+xml;charset=utf-8,'+encodeURIComponent(n.svg)+'\" "
              "style=\"width:132px;border-radius:8px;border:1px solid #eee;cursor:zoom-in\" onclick=\"previewNoteSvg('+i+')\"></div></div>'}")
html = html.replace(anchor2, svg_render + anchor2)
print('renderNotes patched')

# 3) 批量下载控件 + 预览mask（插在notesList之前）
anchor3 = '<div id="notesList"></div>'
assert html.count(anchor3) == 1
batch_html = '''<div class="card">
<div class="card-title">📦 封面批量下载</div>
<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
<span style="font-size:14px">从第</span><input id="dlFrom" type="number" value="6" min="1" style="width:60px;padding:8px;border:1px solid #ddd;border-radius:8px">
<span style="font-size:14px">篇到第</span><input id="dlTo" type="number" value="15" min="1" style="width:60px;padding:8px;border:1px solid #ddd;border-radius:8px">
<span style="font-size:14px">篇</span>
<button class="copy-btn" onclick="batchDlSvg()" style="background:#2F2730;color:#fff;padding:9px 14px">📦 打包下载ZIP</button>
<button class="copy-btn" onclick="batchDlJpg()" style="background:#2F2730;color:#fff;padding:9px 14px">⬇ 逐个下载JPG</button>
</div>
<div style="font-size:12px;color:var(--tl);margin-top:6px">💡 ZIP装的是SVG源文件；JPG为1080×1440可直接发图。有封面的篇目在卡片里也会显示下载按钮。</div>
</div>
<div id="svgMask" onclick="closeSvgPreview()" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.75);z-index:9999;align-items:center;justify-content:center;padding:24px;cursor:zoom-out"><img id="svgPreviewImg" style="max-width:100%;max-height:92vh;border-radius:10px"></div>
'''
html = html.replace(anchor3, batch_html + anchor3)
print('batch UI injected')

# 4) JS函数（插到copySvgPrompt之前）
anchor4 = 'function copySvgPrompt(k){'
assert html.count(anchor4) == 1
js_funcs = '''function noteFname(i){return '第'+(i+1<10?'0':'')+(i+1)+'篇_'+notes[i].title.replace(/[#?!！，,。。「」（）()·]/g,'').slice(0,12)}
function dlNoteSvg(i){if(!notes[i]||!notes[i].svg){showToast('该篇暂无封面');return}var b=new Blob([notes[i].svg],{type:'image/svg+xml;charset=utf-8'});var a=document.createElement('a');a.download=noteFname(i)+'.svg';a.href=URL.createObjectURL(b);a.click();showToast('✅ '+a.download)}
function dlNoteJpg(i){if(!notes[i]||!notes[i].svg){showToast('该篇暂无封面');return}dlSvgTall(notes[i].svg,noteFname(i))}
function copyNoteSvg(i){if(!notes[i]||!notes[i].svg){showToast('该篇暂无封面');return}navigator.clipboard.writeText(notes[i].svg).then(function(){showToast('✅ SVG代码已复制')})}
function previewNoteSvg(i){document.getElementById('svgPreviewImg').src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(notes[i].svg);document.getElementById('svgMask').style.display='flex'}
function closeSvgPreview(){document.getElementById('svgMask').style.display='none'}
function loadJsZip(cb){if(window.JSZip){cb(true);return}var s=document.createElement('script');s.src='https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js';s.onload=function(){cb(true)};s.onerror=function(){showToast('⚠️ ZIP组件加载失败，改为逐个下载SVG');cb(false)};document.head.appendChild(s)}
function batchRange(){var f=parseInt(document.getElementById('dlFrom').value)||1,t=parseInt(document.getElementById('dlTo').value)||notes.length;if(f>t){var x=f;f=t;t=x}var items=[];for(var i=f-1;i<=t-1&&i<notes.length;i++){if(notes[i].svg)items.push(i)}return{f:f,t:t,items:items}}
function batchDlSvg(){var r=batchRange();if(!r.items.length){showToast('该范围没有封面');return}loadJsZip(function(ok){if(!ok){r.items.forEach(function(i2,k){setTimeout(function(){dlNoteSvg(i2)},k*400)});return}var zip=new JSZip();r.items.forEach(function(i3){zip.file(noteFname(i3)+'.svg',notes[i3].svg)});zip.generateAsync({type:'blob'}).then(function(b){var a=document.createElement('a');a.download='笔记封面_第'+r.f+'-'+r.t+'篇.zip';a.href=URL.createObjectURL(b);a.click();showToast('✅ 已打包'+r.items.length+'张SVG')})})}
function batchDlJpg(){var r=batchRange();if(!r.items.length){showToast('该范围没有封面');return}r.items.forEach(function(i2,k){setTimeout(function(){dlNoteJpg(i2)},k*800)});showToast('⏳ 开始逐个下载'+r.items.length+'张JPG')}
'''
html = html.replace(anchor4, js_funcs + anchor4)
print('js funcs injected')

with io.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('ALL DONE')
