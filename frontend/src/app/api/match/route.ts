import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    recommendations: [
      {
        title: "Frontend Developer (React/Next.js)",
        company: "TechCorp",
        location: "Tunis",
        score: 0.87,
      },
      {
        title: "Data Engineer (Python/ETL)",
        company: "DataWorks",
        location: "Nabeul",
        score: 0.81,
      },
    ],
  });
}