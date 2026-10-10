"use client";

import { useState } from "react";
import { CalendarDays, Save, CheckCircle2, XCircle, Clock, CalendarHeart } from "lucide-react";

// Mock Roster Data for Section 10-A
const initialRoster = [
  { id: "1", name: "Aarav Patel", rollNo: 1, status: "present" },
  { id: "2", name: "Diya Sharma", rollNo: 2, status: "present" },
  { id: "3", name: "Rohan Iyer", rollNo: 3, status: "absent" },
  { id: "4", name: "Ananya Singh", rollNo: 4, status: "late" },
  { id: "5", name: "Kabir Khan", rollNo: 5, status: "leave" },
];

export default function AttendancePage() {
  const [roster, setRoster] = useState(initialRoster);
  const [isSaving, setIsSaving] = useState(false);

  const handleStatusChange = (id: string, newStatus: string) => {
    setRoster(current => 
      current.map(student => 
        student.id === id ? { ...student, status: newStatus } : student
      )
    );
  };

  const handleSave = () => {
    setIsSaving(true);
    // Simulate API call to POST /attendance/sync
    setTimeout(() => {
      setIsSaving(false);
      alert("Attendance saved successfully! (Simulated)");
    }, 800);
  };

  const getStatusButtonClass = (studentStatus: string, targetStatus: string, activeClass: string) => {
    const isSelected = studentStatus === targetStatus;
    return `flex-1 py-2 px-3 rounded-lg text-sm font-medium border transition-all flex items-center justify-center gap-2 ${
      isSelected 
        ? activeClass + " border-transparent" 
        : "bg-white text-slate-500 border-slate-200 hover:bg-slate-50"
    }`;
  };

  return (
    <div className="p-8 max-w-5xl mx-auto h-[calc(100vh-64px)] overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 mb-2 flex items-center gap-3">
            <CalendarDays className="w-8 h-8 text-indigo-600" />
            Mark Attendance
          </h1>
          <p className="text-slate-500">
            Class 10 - Section A &nbsp;&bull;&nbsp; Date: {new Date().toLocaleDateString()}
          </p>
        </div>
        
        <button 
          onClick={handleSave}
          disabled={isSaving}
          className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white px-6 py-3 rounded-xl font-medium transition-colors flex items-center gap-2 shadow-sm"
        >
          <Save className="w-5 h-5" />
          {isSaving ? "Saving..." : "Submit Register"}
        </button>
      </div>

      {/* Interactive Roster Table */}
      <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 text-sm font-semibold uppercase tracking-wider">
              <th className="py-4 px-6 w-16 text-center">Roll</th>
              <th className="py-4 px-6 w-1/3">Student Name</th>
              <th className="py-4 px-6">Attendance Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {roster.map((student) => (
              <tr key={student.id} className="hover:bg-slate-50 transition-colors">
                <td className="py-5 px-6 font-semibold text-slate-400 text-center">{student.rollNo}</td>
                <td className="py-5 px-6 font-medium text-slate-900">{student.name}</td>
                <td className="py-5 px-6">
                  <div className="flex gap-2 max-w-lg">
                    <button 
                      onClick={() => handleStatusChange(student.id, 'present')}
                      className={getStatusButtonClass(student.status, 'present', 'bg-emerald-100 text-emerald-800')}
                    >
                      <CheckCircle2 className="w-4 h-4" /> Present
                    </button>
                    
                    <button 
                      onClick={() => handleStatusChange(student.id, 'absent')}
                      className={getStatusButtonClass(student.status, 'absent', 'bg-rose-100 text-rose-800')}
                    >
                      <XCircle className="w-4 h-4" /> Absent
                    </button>
                    
                    <button 
                      onClick={() => handleStatusChange(student.id, 'late')}
                      className={getStatusButtonClass(student.status, 'late', 'bg-amber-100 text-amber-800')}
                    >
                      <Clock className="w-4 h-4" /> Late
                    </button>

                    <button 
                      onClick={() => handleStatusChange(student.id, 'leave')}
                      className={getStatusButtonClass(student.status, 'leave', 'bg-blue-100 text-blue-800')}
                    >
                      <CalendarHeart className="w-4 h-4" /> Leave
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
