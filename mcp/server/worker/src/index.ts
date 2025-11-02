export interface Env {
  APP_ID?: string;
  PRIVATE_KEY?: string;
  INSTALLATION_ID?: string;
}

function json(data: unknown, init: ResponseInit = {}) {
  const headers = new Headers(init.headers);
  headers.set("content-type", "application/json; charset=utf-8");
  return new Response(JSON.stringify(data, null, 2),  { ...init, headers });
}


export default {
  async fetch(req: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(req.url);
    if (url.pathname === "/health") {
      return json({ ok: true, ts: new Date().toISOString() });
    }
    if (url.pathname === "/tools/list" && req.method === "GET") {
      return json({
        tools: [
          { name: "github.create_ref", description: "Create a branch (ref) in a repo" },
          { name: "github.create_or_update_file", description: "Create or update a file in a repo" },
          { name: "github.create_pr", description: "Create a pull request" },
          { name: "github.merge_pr", description: "Merge a pull request" },
          { name: "github.delete_branch", description: "Delete a branch" }
        ],
        ready: Boolean(env.APP_ID && env.PRIVATE_KEY && env.INSTALLATION_ID)
      });
    }
    if (url.pathname === "/sse" && req.method === "GET") {
      const stream = new TransformStream();
      const writer = stream.writable.getWriter();
      const enc = new TextEncoder();
      await writer.write(enc.encode(`event: ready\ndata: ${JSON.stringify({ ts: Date.now() }) }\n\n`));
      writer.close();
      return new Response(stream.readable, {
        headers: {
          "content-type": "text/event-stream",
          "cache-control": "no-cache",
          "connection": "keep-alive"
        }
      });
    }
    if (url.pathname === "/tools/call" && req.method === "POST") {
      // Placeholder: echo back request. Wire to GitHub App in next step.
      const body = await req.json().catch(() => ({}));
      return json( { ok: true, echn: body, note: "wire-up to GitHub App in next step" });
    }
    return new Response("Not found", { status: 404 });
  }
};