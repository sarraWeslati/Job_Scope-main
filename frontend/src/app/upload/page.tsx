"use client";
import CVUploader from "../components/CVUploader";

export default function UploadPage() {
  return (
    <main className="p-6">
      <h1 className="text-xl font-bold">Uploader votre CV</h1>
      <CVUploader />
    </main>
  );
}