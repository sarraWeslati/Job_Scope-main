"use client";
import SkillChart from "./SkillChart";
import TaskChart from "./TaskChart";

export default function ChartSection({ reloadKey }: { reloadKey?: number }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <SkillChart reloadKey={reloadKey} />
      <TaskChart />
    </div>
  );
}