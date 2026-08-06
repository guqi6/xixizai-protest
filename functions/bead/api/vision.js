// Cloudflare Pages Function: 拼豆视觉AI代理
// 浏览器 → 此代理 → bigmodel.cn coding端点（解决CORS）
// API Key 由用户在前端填写，通过请求头传递，不存储在服务端

export async function onRequestPost({ request }) {
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  };

  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const body = await request.json();
    const apiKey = request.headers.get('Authorization') || '';

    // 尝试 coding 端点，如果失败则尝试普通端点
    const endpoints = [
      'https://open.bigmodel.cn/api/coding/paas/v4/chat/completions',
      'https://open.bigmodel.cn/api/paas/v4/chat/completions',
    ];

    let lastError = null;
    for (const url of endpoints) {
      try {
        const resp = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': apiKey,
          },
          body: JSON.stringify(body),
        });

        const data = await resp.text();

        if (resp.status === 200) {
          return new Response(data, {
            status: 200,
            headers: { 'Content-Type': 'application/json', ...corsHeaders },
          });
        }

        // 如果是404/400（模型不存在），尝试下一个端点
        if (resp.status === 404 || resp.status === 400) {
          lastError = { status: resp.status, body: data };
          continue;
        }

        // 其他错误（401/429等）直接返回
        return new Response(data, {
          status: resp.status,
          headers: { 'Content-Type': 'application/json', ...corsHeaders },
        });
      } catch (e) {
        lastError = { status: 502, body: e.message };
      }
    }

    return new Response(JSON.stringify(lastError || { error: 'All endpoints failed' }), {
      status: lastError?.status || 502,
      headers: { 'Content-Type': 'application/json', ...corsHeaders },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 502,
      headers: { 'Content-Type': 'application/json', ...corsHeaders },
    });
  }
}
