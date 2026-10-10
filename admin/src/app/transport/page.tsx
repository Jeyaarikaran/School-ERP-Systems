"use client";

import { useState } from "react";
import { Bus, MapPin, Users, Settings2, ShieldCheck, Route as RouteIcon } from "lucide-react";

// Mock Data for Phase 9 Transport
const mockRoutes = [
  { id: "R1", code: "RT-01", name: "North City Express", bus: "BUS-A 40-Seater", students: 35, status: "active" },
  { id: "R2", code: "RT-02", name: "South Suburbs Loop", bus: "BUS-B 30-Seater", students: 28, status: "active" },
  { id: "R3", code: "RT-03", name: "East Side Direct", bus: "BUS-C 50-Seater", students: 48, status: "maintenance" },
];

export default function TransportPage() {
  const [routes, setRoutes] = useState(mockRoutes);

  return (
    <div className="p-8 max-w-7xl mx-auto h-[calc(100vh-64px)] overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 mb-2 flex items-center gap-3">
            <Bus className="w-8 h-8 text-sky-600" />
            Transport Fleet
          </h1>
          <p className="text-slate-500">Manage routes, bus assignments, and boarding manifests (Phase 9)</p>
        </div>
        
        <div className="flex gap-4">
          <button className="bg-slate-100 hover:bg-slate-200 text-slate-700 px-5 py-2.5 rounded-xl font-medium transition-colors flex items-center gap-2">
            <RouteIcon className="w-5 h-5" />
            New Route
          </button>
        </div>
      </div>

      {/* Routes Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {routes.map(route => (
          <div key={route.id} className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow group">
            <div className={`h-2 ${route.status === 'active' ? 'bg-emerald-500' : 'bg-amber-500'}`} />
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <div className="text-xs font-bold text-slate-400 mb-1 tracking-wider">{route.code}</div>
                  <h3 className="text-xl font-bold text-slate-800">{route.name}</h3>
                </div>
                <button className="text-slate-300 hover:text-sky-600">
                  <Settings2 className="w-5 h-5" />
                </button>
              </div>
              
              <div className="space-y-3 mb-6">
                <div className="flex items-center gap-3 text-slate-600">
                  <div className="p-2 bg-slate-50 rounded-lg"><Bus className="w-4 h-4" /></div>
                  <span className="font-medium">{route.bus}</span>
                </div>
                <div className="flex items-center gap-3 text-slate-600">
                  <div className="p-2 bg-slate-50 rounded-lg"><Users className="w-4 h-4" /></div>
                  <span className="font-medium">{route.students} Enrolled Students</span>
                </div>
                <div className="flex items-center gap-3 text-slate-600">
                  <div className="p-2 bg-slate-50 rounded-lg"><MapPin className="w-4 h-4" /></div>
                  <span className="font-medium">12 Designated Stops</span>
                </div>
              </div>
              
              <div className="pt-4 border-t border-slate-100 flex gap-3">
                <button className="flex-1 bg-sky-50 text-sky-700 py-2 rounded-lg font-semibold text-sm hover:bg-sky-100 transition-colors">
                  View Manifest
                </button>
                <button className="flex-1 bg-white border border-slate-200 text-slate-600 py-2 rounded-lg font-semibold text-sm hover:bg-slate-50 transition-colors flex items-center justify-center gap-1">
                  <ShieldCheck className="w-4 h-4" /> Compliance
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
