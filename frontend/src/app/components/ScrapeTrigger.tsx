"use client";
import { useState } from "react";

export default function ScrapeTrigger() {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");

  const handleScrape = async () => {
    setLoading(true);
    setStatus("");
    try {
      const res = await fetch("/api/scrape", { method: "POST" });
      const data = await res.json();
      setStatus(data.message || "Scraping terminé !");
    } catch {
      setStatus("Erreur lors du scraping.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md">
      <h2 className="text-lg font-semibold mb-2">📡 Lancer le scraping</h2>
      <button
        onClick={handleScrape}
        disabled={loading}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Scraping en cours..." : "Démarrer"}
      </button>
      {status && <p className="mt-2 text-sm">{status}</p>}
    </div>
  );
}