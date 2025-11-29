"use client";
export default function JobFilters() {
  return (
    <div className="flex gap-4 mt-4">
      <input type="text" placeholder="Filtrer par mot-clé" className="border p-2" />
      <select className="border p-2">
        <option>Tous</option>
        <option>Remote</option>
        <option>On-site</option>
      </select>
    </div>
  );
}