"use client";
import { useState, useEffect } from "react";

// Définition du type Job
interface Job {
  title: string;
  company: string;
  location: string;
}

export default function JobList() {
  const [jobs, setJobs] = useState<Job[]>([]); // ← plus propre que any[]

  useEffect(() => {
    fetch("/api/jobs")
      .then((res) => res.json())
      .then((data: Job[]) => setJobs(data)) // typage explicite
      .catch(() => setJobs([]));
  }, []);

  return (
    <ul className="mt-4">
      {jobs.map((job, idx) => (
        <li key={idx} className="border p-2 mb-2">
          <h2 className="font-semibold">{job.title}</h2>
          <p>
            {job.company} - {job.location}
          </p>
        </li>
      ))}
    </ul>
  );
}