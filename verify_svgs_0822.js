// 验证SVG XML合法 + 导出2张预览PNG（暖橙/星空各1张）
const fs = require('fs');
const { execSync } = require('child_process');
const html = fs.readFileSync('admin.html', 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
const main = scripts[scripts.length - 1];

const elStub = { innerHTML: '', textContent: '', value: '', addEventListener: () => {}, classList: { add: () => {}, remove: () => {} }, appendChild: () => {}, style: {}, onclick: null };
global.document = { getElementById: () => elStub, querySelectorAll: () => [], querySelector: () => elStub, createElement: () => elStub, addEventListener: () => {}, body: elStub, head: elStub };
global.window = global;
global.localStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };
global.navigator = { clipboard: { writeText: () => Promise.resolve() } };
global.fetch = () => Promise.resolve({ ok: true, json: () => Promise.resolve({}) });

const notes = new Function('document', 'window', 'localStorage', 'navigator', 'fetch', main + '\n; return notes;')(
  global.document, global.window, global.localStorage, global.navigator, global.fetch);

// 1) XML合法性
const violations = [];
notes.forEach((n, i) => {
  if (!n.svg) return;
  const m = n.svg.match(/<svg[\s\S]*<\/svg>/);
  if (!m) { violations.push((i + 1) + ': no svg tag'); return; }
  const opens = (n.svg.match(/<(?!\/)(?!br)(?!hr)/g) || []).length;
  const closes = (n.svg.match(/<\/|\/>/g) || []).length;
  // 粗查：每个开标签应有闭标签或自闭合
  if (opens > closes + 1) violations.push((i + 1) + ': tag mismatch open=' + opens + ' close=' + closes);
  if (!n.svg.includes('</svg>')) violations.push((i + 1) + ': missing </svg>');
  if (n.svg.includes("'")) violations.push((i + 1) + ': contains single quote');
});
console.log('svg count:', notes.filter(n => n.svg).length, '/ 15');
console.log('violations:', violations.length ? violations : 'none');

// 2) 导出第6篇和第14篇SVG文件供转PNG预览
fs.writeFileSync('/tmp/preview_06.svg', notes[5].svg);
fs.writeFileSync('/tmp/preview_11.svg', notes[10].svg);
fs.writeFileSync('/tmp/preview_15.svg', notes[14].svg);
console.log('previews exported: /tmp/preview_06.svg /tmp/preview_11.svg /tmp/preview_15.svg');

// 3) 新函数存在性
['noteFname','dlNoteSvg','dlNoteJpg','copyNoteSvg','previewNoteSvg','closeSvgPreview','loadJsZip','batchDlSvg','batchDlJpg'].forEach(f => {
  if (!main.includes('function ' + f)) console.log('MISSING fn:', f);
});
console.log('functions check done');
