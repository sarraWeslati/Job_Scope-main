import { NextResponse } from "next/server";

const BACKEND_BASE = process.env.BACKEND_URL || "http://127.0.0.1:8000";

export async function GET(_request: Request, { params }: { params: { jobId: string } }) {
  const { jobId } = params;
  try {
    const res = await fetch(`${BACKEND_BASE}/api/scrape/status/${encodeURIComponent(jobId)}`);
    const text = await res.text();
    return new NextResponse(text, { status: res.status, headers: { "content-type": res.headers.get("content-type") || "application/json" } });
  } catch (e) {
    return NextResponse.json({ message: "Proxy error", detail: String(e) }, { status: 502 });
  }
}
