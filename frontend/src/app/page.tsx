"use client"; // car tu utilises des composants client
import { useState } from "react";
import Sidebar from "./components/Sidebar";
import TopBar from "./components/TopBar";
import KPISection from "./components/KPISection";
import ChartSection from "./components/ChartSection";
import Recommendations from "./components/Recommendations";
import CVUploader from "./components/CVUploader";
import ScrapeTrigger from "./components/ScrapeTrigger";
import AnomalyAlert from "./components/AnomalyAlert";

export default function DashboardPage() {
  const [reloadKey, setReloadKey] = useState(0);

  const handleScrapeComplete = () => {
    // bump the key to force charts to refresh
    setReloadKey((k) => k + 1);
  };

  return (
    <div className="flex h-screen bg-gray-100 dark:bg-gray-900">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <TopBar />
        <main className="app-main p-6 space-y-6 overflow-y-auto">
          <div className="card">
            <KPISection />
          </div>

          <div className="card">
            <ScrapeTrigger onComplete={handleScrapeComplete} />
          </div>

          <div className="card">
            <CVUploader />
          </div>

          <div className="card">
            <Recommendations />
          </div>

          <div className="card">
            <ChartSection reloadKey={reloadKey} />
          </div>

          <div className="card">
            <AnomalyAlert />
          </div>
        </main>
      </div>
    </div>
  );
}