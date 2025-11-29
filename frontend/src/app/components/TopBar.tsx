"use client";
import { FaBell, FaCog, FaUser } from "react-icons/fa";

export default function TopBar() {
  return (
    <div className="flex items-center justify-between px-6 py-4 border-b bg-white dark:bg-gray-800">
      <input
        type="text"
        placeholder="Rechercher..."
        className="w-1/2 p-2 rounded-md border dark:bg-gray-700 dark:text-white"
      />
      <div className="flex gap-4 text-xl text-gray-600 dark:text-gray-300">
        <FaBell />
        <FaCog />
        <FaUser />
      </div>
    </div>
  );
}