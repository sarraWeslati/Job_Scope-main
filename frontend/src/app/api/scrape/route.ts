import { NextResponse } from "next/server";

const BACKEND_BASE = process.env.BACKEND_URL || "http://127.0.0.1:8000";

export async function POST(request: Request) {
  // Proxy the request to the backend enqueue endpoint
  try {
    const body = await request.text();
    const res = await fetch(`${BACKEND_BASE}/api/scrape`, {
      method: "POST",
      headers: { "content-type": request.headers.get("content-type") || "application/json" },
      body: body || undefined,
    });
    const data = await res.text();
    return new NextResponse(data, { status: res.status, headers: { "content-type": res.headers.get("content-type") || "application/json" } });
  } catch (e) {
    return NextResponse.json({ message: "Proxy error", detail: String(e) }, { status: 502 });
  }
}