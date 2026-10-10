"use client";

import { useState } from "react";
import { FileText, Save, FileCheck2, Calculator, AlertCircle } from "lucide-react";

// Mock Mark Sheet Data (Phase 6)
const maxMarks = 100;
const initialStudents = [
  { id: "1", name: "Aarav Patel", marks: 85, attendance: "present" },
  { id: "2", name: "Diya Sharma", marks: 92, attendance: "present" },
  { id: "3", name: "Rohan Iyer", marks: 0, attendance: "absent" },
  { id: "4", name: "Ananya Singh", marks: 78, attendance: "present" },
  { id: "5", name: "Kabir Khan", marks: 45, attendance: "present" },
];

export default function MarkSheetPage() {
  const [students, setStudents] = useState(initialStudents);
  const [isSaving, setIsSaving] = useState(false);
  const [isLocked, setIsLocked] = useState(false);

  const handleMarkChange = (id: string, newMarks: string) => {
    if (isLocked) return;
    
    // Decimal math check per Phase 6 rules
    let parsedMarks = parseFloat(newMarks);
    if (isNaN(parsedMarks)) parsedMarks = 0;
    if (parsedMarks > maxMarks) parsedMarks = maxMarks;
    if (parsedMarks < 0) parsedMarks = 0;

    setStudents(current => 
      current.map(student => 
        student.id === id ? { ...student, marks: parsedMarks } : student
      )
    );
  };

  const handleAttendanceChange = (id: string, newStatus: string) => {
    if (isLocked) return;
    setStudents(current => 
      current.map(student => 
        student.id === id ? { ...student, attendance: newStatus, marks: newStatus === 'absent' ? 0 : student.marks } : student
      )
    );
  };

  const handleSave = () => {
    setIsSaving(true);
    setTimeout(() => {
      setIsSaving(false);
    }, 800);
  };

  const handleSubmitToPrincipal = () => {
    if (confirm("Are you sure you want to submit this mark sheet for approval? You will no longer be able to edit it.")) {
      setIsLocked(true);
    }
  };

  return (
    <div className="p-8 max-w-5xl mx-auto h-[calc(100vh-64px)] overflow-y-auto">
      <div className="flex items-center justify-between mb-8 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 mb-2 flex items-center gap-3">
            <FileText className="w-8 h-8 text-indigo-600" />
            Mark Sheet Entry
          </h1>
          <p className="text-slate-500">
            Mid-Term Exam &nbsp;&bull;&nbsp; Class 10-A &nbsp;&bull;&nbsp; Mathematics (Max: {maxMarks})
          </p>
        </div>
        
        <div className="flex gap-4">
          <button 
            onClick={handleSave}
            disabled={isLocked || isSaving}
            className="bg-slate-100 hover:bg-slate-200 disabled:opacity-50 text-slate-700 px-6 py-3 rounded-xl font-medium transition-colors flex items-center gap-2"
          >
            <Save className="w-5 h-5" />
            Save Draft
          </button>
          <button 
            onClick={handleSubmitToPrincipal}
            disabled={isLocked}
            className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white px-6 py-3 rounded-xl font-medium transition-colors flex items-center gap-2 shadow-sm"
          >
            <FileCheck2 className="w-5 h-5" />
            {isLocked ? "Submitted" : "Submit to Principal"}
          </button>
        </div>
      </div>

      {isLocked && (
        <div className="mb-6 bg-blue-50 border border-blue-200 rounded-xl p-4 flex items-start gap-3 text-blue-800">
          <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
          <div className="text-sm">
            <strong className="block mb-1">Mark Sheet Locked</strong>
            This mark sheet has been submitted for approval. You cannot make further edits. Any corrections require Principal approval via the `marks.approve` permission.
          </div>
        </div>
      )}

      <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 text-sm font-semibold uppercase tracking-wider">
              <th className="py-4 px-6 w-1/3">Student Name</th>
              <th className="py-4 px-6 w-1/4">Status</th>
              <th className="py-4 px-6 w-1/4">Marks (Out of {maxMarks})</th>
              <th className="py-4 px-6 text-right">Pass/Fail</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {students.map((student) => (
              <tr key={student.id} className="hover:bg-slate-50 transition-colors">
                <td className="py-4 px-6 font-medium text-slate-900">{student.name}</td>
                <td className="py-4 px-6">
                  <select 
                    value={student.attendance}
                    onChange={(e) => handleAttendanceChange(student.id, e.target.value)}
                    disabled={isLocked}
                    className="p-2 rounded-lg border border-slate-200 bg-white focus:ring-2 focus:ring-indigo-500 outline-none disabled:opacity-50"
                  >
                    <option value="present">Present</option>
                    <option value="absent">Absent</option>
                    <option value="exempt">Medical Exempt</option>
                  </select>
                </td>
                <td className="py-4 px-6">
                  <div className="relative max-w-[120px]">
                    <Calculator className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                    <input 
                      type="number" 
                      value={student.marks}
                      onChange={(e) => handleMarkChange(student.id, e.target.value)}
                      disabled={isLocked || student.attendance === 'absent'}
                      className="w-full pl-9 pr-4 py-2 rounded-lg border border-slate-200 bg-white focus:ring-2 focus:ring-indigo-500 outline-none disabled:opacity-50 disabled:bg-slate-50 font-semibold"
                    />
                  </div>
                </td>
                <td className="py-4 px-6 text-right">
                  {student.attendance === 'absent' ? (
                    <span className="text-rose-600 font-bold text-sm bg-rose-50 px-3 py-1 rounded-full">F (ABS)</span>
                  ) : student.marks >= 35 ? (
                    <span className="text-emerald-600 font-bold text-sm bg-emerald-50 px-3 py-1 rounded-full">PASS</span>
                  ) : (
                    <span className="text-rose-600 font-bold text-sm bg-rose-50 px-3 py-1 rounded-full">FAIL</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
