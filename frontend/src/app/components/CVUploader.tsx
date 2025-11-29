"use client";
import { useState } from "react";

export default function CVUploader() {
  const [file, setFile] = useState<File | null>(null);
  const [recommendations, setRecommendations] = useState<any[]>([]);

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/match", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setRecommendations(data.recommendations || []);
  };

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md">
      <h2 className="text-lg font-semibold mb-2">📄 Upload CV</h2>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="mb-2"
      />
      <button
        onClick={handleUpload}
        className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
      >
        Envoyer
      </button>

      {recommendations.length > 0 && (
        <ul className="mt-4 space-y-2">
          {recommendations.map((rec, idx) => (
            <li key={idx} className="p-2 bg-gray-100 dark:bg-gray-700 rounded">
              {rec.title} — Score: {rec.match_score}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}