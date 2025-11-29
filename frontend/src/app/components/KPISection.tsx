"use client";

export default function KPISection() {
  const cards = [
    { label: "Offres scrappées", value: "1,245", icon: "🗂️", color: "bg-blue-500" },
    { label: "CV analysés", value: "87", icon: "📄", color: "bg-green-500" },
    { label: "Matching réalisés", value: "312", icon: "🔗", color: "bg-orange-500" },
    { label: "Alertes anomalies", value: "3", icon: "⚠️", color: "bg-red-500" },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card, idx) => (
        <div key={idx} className={`p-4 rounded-lg shadow-md text-white ${card.color}`}>
          <div className="text-2xl">{card.icon}</div>
          <div className="mt-2 text-sm">{card.label}</div>
          <div className="text-xl font-bold">{card.value}</div>
        </div>
      ))}
    </div>
  );
}