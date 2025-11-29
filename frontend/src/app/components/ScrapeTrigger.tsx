"use client";
import { useState } from "react";

type Props = {
  onComplete?: () => void;
};

export default function ScrapeTrigger({ onComplete }: Props) {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");

  const handleScrape = async () => {
    setLoading(true);
    setStatus("");
      try {
      const res = await fetch("/api/scrape", { method: "POST" });
      const data = await res.json();
      if (!res.ok) throw new Error(data?.detail || data?.message || "Enqueue failed");
      const jobId = data.job_id;
      setStatus("Job enqueued: " + jobId + ". Attente du résultat...");

      // Poll for job status until done/failed
      const poll = async () => {
        try {
          const s = await fetch(`/api/scrape/status/${jobId}`);
          const j = await s.json();
          if (j.status === "done") {
            setStatus("Scraping terminé.");
            if (typeof onComplete === "function") onComplete();
            return;
          }
          if (j.status === "failed") {
            setStatus("Scraping échoué: " + (j.error || "unknown"));
            return;
          }
        } catch (e) {
          // ignore transient errors
        }
        setTimeout(poll, 2000);
      };
      setTimeout(poll, 1000);
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