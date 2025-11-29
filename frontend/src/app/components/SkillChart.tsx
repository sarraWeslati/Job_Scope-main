"use client";
import { useEffect, useState } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

// ⚠️ Enregistrement obligatoire des scales et éléments
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

type Skill = { name: string; count: number };

export default function SkillChart() {
  const [skills, setSkills] = useState<Skill[]>([]);

  useEffect(() => {
    fetch("/api/insights")
      .then((res) => res.json())
      .then((data) => setSkills(data.skills ?? []))
      .catch(() => setSkills([]));
  }, []);

  const data = {
    labels: skills.map((s) => s.name),
    datasets: [
      {
        label: "Demande",
        data: skills.map((s) => s.count),
        backgroundColor: "rgba(75,192,192,0.6)",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: "top" as const },
      title: { display: true, text: "Compétences demandées" },
    },
  };

  return (
    <div className="border p-4 rounded">
      <h2 className="font-semibold mb-2">Top compétences demandées</h2>
      {skills.length > 0 ? <Bar data={data} options={options} /> : <p>Aucune donnée.</p>}
    </div>
  );
}