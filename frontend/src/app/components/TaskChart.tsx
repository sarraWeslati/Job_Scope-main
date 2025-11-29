"use client";
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

// Enregistrement des modules Chart.js
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function TaskChart() {
  const data = {
    labels: ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"],
    datasets: [
      {
        label: "Tâches complétées",
        data: [12, 19, 14, 20, 17, 22, 25], // données mock
        backgroundColor: "rgba(255, 99, 132, 0.5)",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: "top" as const },
      title: { display: true, text: "Progression des tâches" },
    },
  };

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md">
      <Bar data={data} options={options} />
    </div>
  );
}