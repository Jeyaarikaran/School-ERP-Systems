"use client";

import { useState } from "react";
import { FileSpreadsheet, FileText, Download, Filter, FileJson, Clock, RefreshCw } from "lucide-react";

// Mock Report Data (Phase 10)
const reportsList = [
  { id: "1", name: "Monthly Attendance Rollup", type: "CSV", status: "ready", date: "Oct 1, 2026", size: "2.4 MB" },
  { id: "2", name: "Q3 Fee Defaulters", type: "Excel", status: "processing", date: "Oct 5, 2026", size: "-" },
  { id: "3", name: "Mid-Term Results Summary", type: "PDF", status: "ready", date: "Sep 28, 2026", size: "5.1 MB" },
];

export default function ReportsPage() {
  const [reports, setReports] = useState(reportsList);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = () => {
    setIsGenerating(true);
    // Simulate API POST /exports -> 202 Accepted (Celery Job)
    setTimeout(() => {
      setReports([
        { id: "4", name: "Custom Student Roster", type: "Excel", status: "queued", date: "Oct 5, 2026", size: "-" },
        ...reports
      ]);
      setIsGenerating(false);
    }, 1000);
  };

  return (
    <div className="p-8 max-w-7xl mx-auto h-[calc(100vh-64px)] overflow-y-auto">
      <div className="flex items-center justify-between mb-8 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 mb-2 flex items-center gap-3">
            <FileSpreadsheet className="w-8 h-8 text-teal-600" />
            Reports & Analytics
          </h1>
          <p className="text-slate-500">Asynchronous report generation via Celery Background Workers (Phase 10)</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Report Generator Form */}
        <div className="lg:col-span-1 bg-white p-6 rounded-2xl shadow-sm border border-slate-200 h-fit">
          <h2 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
            <Filter className="w-5 h-5 text-teal-600" /> New Report
          </h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-slate-600 mb-2">Report Type</label>
              <select className="w-full p-2.5 rounded-xl border border-slate-200 bg-slate-50 outline-none focus:ring-2 focus:ring-teal-500">
                <option>Attendance Register (Monthly)</option>
                <option>Fee Defaulters List</option>
                <option>Exam Mark Sheets (Bulk)</option>
                <option>Student Master Data</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-semibold text-slate-600 mb-2">Date Range</label>
              <div className="flex gap-2">
                <input type="date" className="w-full p-2.5 rounded-xl border border-slate-200 bg-slate-50 outline-none text-sm" />
                <input type="date" className="w-full p-2.5 rounded-xl border border-slate-200 bg-slate-50 outline-none text-sm" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-600 mb-2">Export Format</label>
              <div className="flex gap-2">
                <button className="flex-1 py-2 rounded-lg border-2 border-teal-500 bg-teal-50 text-teal-700 font-medium flex items-center justify-center gap-1">
                  <FileSpreadsheet className="w-4 h-4" /> Excel
                </button>
                <button className="flex-1 py-2 rounded-lg border border-slate-200 bg-white text-slate-600 font-medium hover:bg-slate-50 flex items-center justify-center gap-1">
                  <FileText className="w-4 h-4" /> PDF
                </button>
                <button className="flex-1 py-2 rounded-lg border border-slate-200 bg-white text-slate-600 font-medium hover:bg-slate-50 flex items-center justify-center gap-1">
                  <FileJson className="w-4 h-4" /> CSV
                </button>
              </div>
            </div>

            <button 
              onClick={handleGenerate}
              disabled={isGenerating}
              className="w-full mt-4 bg-teal-600 hover:bg-teal-700 text-white px-5 py-3 rounded-xl font-medium transition-colors flex items-center justify-center gap-2 shadow-sm disabled:bg-teal-400"
            >
              {isGenerating ? <RefreshCw className="w-5 h-5 animate-spin" /> : <Download className="w-5 h-5" />}
              Generate Report
            </button>
          </div>
        </div>

        {/* Report Queue / History */}
        <div className="lg:col-span-2 bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
          <div className="px-6 py-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
            <h3 className="font-bold text-slate-800">Generated Reports Queue</h3>
            <button className="text-teal-600 hover:text-teal-700 text-sm font-medium flex items-center gap-1">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
          </div>
          
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-white border-b border-slate-100 text-slate-400 text-sm font-semibold uppercase tracking-wider">
                <th className="py-4 px-6">Report Name</th>
                <th className="py-4 px-6">Format</th>
                <th className="py-4 px-6">Status</th>
                <th className="py-4 px-6 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {reports.map((report) => (
                <tr key={report.id} className="hover:bg-slate-50 transition-colors">
                  <td className="py-4 px-6">
                    <div className="font-medium text-slate-900">{report.name}</div>
                    <div className="text-xs text-slate-500 mt-1">{report.date} &bull; {report.size}</div>
                  </td>
                  <td className="py-4 px-6">
                    <span className="px-2 py-1 bg-slate-100 text-slate-600 rounded text-xs font-semibold">{report.type}</span>
                  </td>
                  <td className="py-4 px-6">
                    {report.status === 'ready' ? (
                      <span className="inline-flex items-center gap-1 text-emerald-600 text-sm font-semibold">
                        <div className="w-2 h-2 rounded-full bg-emerald-500"></div> Ready
                      </span>
                    ) : report.status === 'processing' ? (
                      <span className="inline-flex items-center gap-1 text-amber-600 text-sm font-semibold">
                        <RefreshCw className="w-3 h-3 animate-spin" /> Processing
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 text-slate-500 text-sm font-semibold">
                        <Clock className="w-3 h-3" /> Queued
                      </span>
                    )}
                  </td>
                  <td className="py-4 px-6 text-right">
                    {report.status === 'ready' ? (
                      <button className="text-teal-600 hover:text-teal-800 font-medium text-sm flex items-center gap-1 float-right">
                        <Download className="w-4 h-4" /> Download
                      </button>
                    ) : (
                      <span className="text-slate-400 text-sm italic">Please wait...</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

      </div>
    </div>
  );
}
