// 验证admin.html脚本语法 + 运行时笔记数（带DOM stub）
const fs = require('fs');
const html = fs.readFileSync('admin.html', 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
let lastErr = null;
for (const s of scripts) {
  try { new Function(s); } catch (e) { lastErr = e; }
}
if (lastErr) { console.log('SYNTAX ERROR:', lastErr.message); process.exit(1); }
console.log('syntax OK, script blocks:', scripts.length);

// DOM stub
const elStub = {
  innerHTML: '', textContent: '', value: '',
  addEventListener: () => {}, classList: { add: () => {}, remove: () => {} },
  appendChild: () => {}, style: {}, onclick: null,
};
global.document = {
  getElementById: () => elStub,
  querySelectorAll: () => [],
  querySelector: () => elStub,
  createElement: () => elStub,
  addEventListener: () => {},
  body: elStub,
};
global.window = global;
global.localStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };
global.navigator = { clipboard: { writeText: () => Promise.resolve() } };
global.fetch = () => Promise.resolve({ ok: true, json: () => Promise.resolve({}) });

const main = scripts[scripts.length - 1];
let notes;
try {
  notes = new Function('document', 'window', 'localStorage', 'navigator', 'fetch',
    main + '\n; return notes;')(global.document, global.window, global.localStorage, global.navigator, global.fetch);
} catch (e) {
  console.log('eval error:', e.message); process.exit(1);
}
console.log('notes.length =', notes.length);
console.log('last 10 titles:');
notes.slice(-10).forEach((n, i) => console.log(' ', notes.length - 10 + i + 1, n.title));
const bad = notes.filter(n => !n.title || !n.body || !n.comment || !n.imagePrompt);
console.log('missing-field notes:', bad.length);
// 高阶系列型号去重检查：确认新5篇型号未与旧篇目撞标题
const titles = notes.map(n => n.title);
const dup = titles.filter((t, i) => titles.indexOf(t) !== i);
console.log('duplicate titles:', dup.length ? dup : 'none');
