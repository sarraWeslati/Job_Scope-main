"use client";
import { useEffect, useState } from "react";

type Recommendation = {
  title: string;
  company: string;
  location: string;
  score: number; // matching score
};

export default function Recommendations() {
  const [recs, setRecs] = useState<Recommendation[]>([]);

  useEffect(() => {
    fetch("/api/match", { method: "GET" })
      .then((res) => res.json())
      .then((data) => setRecs(data.recommendations ?? []))
      .catch(() => setRecs([]));
  }, []);

  return (
    <div className="border p-4 rounded">
      <h2 className="font-semibold mb-2">Recommandations basées sur votre profil</h2>
      {recs.length === 0 ? (
        <p>Aucune recommandation pour le moment.</p>
      ) : (
        <ul className="space-y-2">
          {recs.map((r, idx) => (
            <li key={idx} className="border p-2 rounded">
              <div className="font-semibold">{r.title}</div>
              <div className="text-sm text-gray-600">
                {r.company} — {r.location}
              </div>
              <div className="text-sm">Score: {r.score.toFixed(2)}</div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}