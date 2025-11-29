"use client";
import { useEffect, useState } from "react";

type Anomaly = { date: string; description: string; severity: "low" | "medium" | "high" };

export default function AnomalyAlert() {
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);

  useEffect(() => {
    fetch("/api/insights")
      .then((res) => res.json())
      .then((data) => setAnomalies(data.anomalies ?? []))
      .catch(() => setAnomalies([]));
  }, []);

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md">
      <h2 className="text-lg font-semibold mb-4">⚠️ Anomalies détectées</h2>
      {anomalies.length === 0 ? (
        <p>Aucune anomalie détectée.</p>
      ) : (
        <ul className="space-y-3">
          {anomalies.map((a, idx) => (
            <li key={idx} className="p-3 rounded bg-red-500 text-white">
              <div className="font-bold">{a.date}</div>
              <div>{a.description}</div>
              <div className="text-sm italic">Sévérité : {a.severity}</div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}