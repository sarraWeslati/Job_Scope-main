"use client";
import JobList from "../components/JobList";
import JobFilters from "../components/JobFilters";

export default function JobsPage() {
  return (
    <main className="p-6">
      <h1 className="text-xl font-bold">Offres demploi</h1>
      <JobFilters />
      <JobList />
    </main>
  );
}