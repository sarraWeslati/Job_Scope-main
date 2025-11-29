import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    anomalies: [
      {
        date: "2025-11-20",
        description: "Pic soudain de demandes pour 'Prompt Engineer'",
        severity: "high",
      },
      {
        date: "2025-11-18",
        description: "Baisse inhabituelle des offres en Data Science",
        severity: "medium",
      },
    ],
  });
}