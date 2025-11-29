"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import {
  FaHome,
  FaBriefcase,
  FaChartLine,
  FaBell,
  FaMoon,
  FaSun,
  FaBars,
} from "react-icons/fa";

export default function Sidebar() {
  const [active, setActive] = useState("dashboard");
  const [darkMode, setDarkMode] = useState(false);
  const [collapsed, setCollapsed] = useState(true);

  const items = [
    { id: "dashboard", label: "Dashboard", icon: <FaHome /> },
    { id: "jobs", label: "Offres", icon: <FaBriefcase /> },
    { id: "trends", label: "Tendances", icon: <FaChartLine /> },
    { id: "notifications", label: "Notifications", icon: <FaBell /> },
  ];

  return (
    <motion.aside
      initial={{ width: "80px" }}
      animate={{ width: collapsed ? "80px" : "260px" }}
      onMouseEnter={() => setCollapsed(false)}
      onMouseLeave={() => setCollapsed(true)}
      className={`h-screen flex flex-col backdrop-blur-md bg-white/30 dark:bg-gray-900/40
        shadow-xl border-r border-gray-200 dark:border-gray-700 transition-all duration-300
        text-gray-800 dark:text-gray-100`}
    >
      {/* Logo + bouton */}
      <div className="p-4 flex items-center justify-between border-b border-gray-300 dark:border-gray-700">
        {!collapsed && (
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">J</div>
            <span className="text-lg font-semibold">JobScope</span>
          </div>
        )}
        <button onClick={() => setCollapsed(!collapsed)} className="text-xl">
          <FaBars />
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 mt-4 px-2">
        {items.map((item) => (
          <motion.button
            key={item.id}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setActive(item.id)}
            className={`flex items-center gap-3 w-full px-4 py-2 text-left rounded-md mb-2
              transition-colors duration-200 hover:bg-blue-100 dark:hover:bg-blue-900
              ${active === item.id ? "bg-blue-500 text-white" : ""}`}
          >
            <span className="text-xl">{item.icon}</span>
            {!collapsed && <span className="text-sm font-medium">{item.label}</span>}
          </motion.button>
        ))}
      </nav>

      {/* Dark mode toggle */}
      <div className="p-4 border-t border-gray-300 dark:border-gray-700 flex items-center justify-between">
        {!collapsed && <span className="text-sm">Mode</span>}
        <button
          onClick={() => setDarkMode(!darkMode)}
          className="p-2 rounded-full bg-gray-200 dark:bg-gray-700"
        >
          {darkMode ? <FaSun /> : <FaMoon />}
        </button>
      </div>

      {/* Avatar */}
      <div className="mt-auto p-4 flex items-center gap-3 border-t border-gray-300 dark:border-gray-700">
        <img src="https://via.placeholder.com/32" className="rounded-full" />
        {!collapsed && (
          <div>
            <p className="text-sm font-semibold">Sarra</p>
            <p className="text-xs text-gray-500 dark:text-gray-400">Connectée</p>
          </div>
        )}
      </div>
    </motion.aside>
  );
}