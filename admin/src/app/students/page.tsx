"use client";

import { useState } from "react";
import { Search, Filter, MoreVertical, Plus, GraduationCap, ChevronLeft, ChevronRight, X } from "lucide-react";

// Mock Data matching the Phase 3 schema
const initialMockStudents = [
  { id: "1", admission_no: "ADM-2023-001", full_name: "Aarav Patel", status: "active", class: "10", section: "A" },
  { id: "2", admission_no: "ADM-2023-002", full_name: "Diya Sharma", status: "active", class: "10", section: "A" },
  { id: "3", admission_no: "ADM-2022-045", full_name: "Rohan Iyer", status: "transferred", class: "9", section: "B" },
  { id: "4", admission_no: "ADM-2024-012", full_name: "Ananya Singh", status: "active", class: "11", section: "C" },
  { id: "5", admission_no: "ADM-2021-103", full_name: "Kabir Khan", status: "archived", class: "12", section: "A" },
];

export default function StudentsDirectoryPage() {
  const [students, setStudents] = useState(initialMockStudents);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  
  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newStudent, setNewStudent] = useState({ full_name: "", class: "1", section: "A" });

  // Client-side filtering simulation
  const filteredStudents = students.filter(s => {
    const matchesSearch = s.full_name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          s.admission_no.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === "all" || s.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="p-8 max-w-7xl mx-auto h-[calc(100vh-64px)] overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 mb-2 flex items-center gap-3">
            <GraduationCap className="w-8 h-8 text-blue-600" />
            Student Directory
          </h1>
          <p className="text-slate-500">Manage enrollments, statuses, and profiles (Phase 3)</p>
        </div>
        <button 
          onClick={() => setIsModalOpen(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-xl font-medium transition-colors flex items-center gap-2 shadow-sm"
        >
          <Plus className="w-5 h-5" />
          Admit Student
        </button>
      </div>

      {/* Toolbar */}
      <div className="bg-white p-4 rounded-t-2xl border border-slate-200 border-b-0 flex gap-4 items-center justify-between">
        <div className="relative flex-1 max-w-md">
          <Search className="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input 
            type="text" 
            placeholder="Search by name or admission no..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none transition-all"
          />
        </div>
        
        <div className="flex gap-3">
          <div className="relative">
            <Filter className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <select 
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="pl-9 pr-8 py-2.5 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-blue-500/20 outline-none appearance-none font-medium text-slate-700 cursor-pointer"
            >
              <option value="all">All Statuses</option>
              <option value="active">Active</option>
              <option value="transferred">Transferred</option>
              <option value="archived">Archived</option>
            </select>
          </div>
        </div>
      </div>

      {/* Data Table */}
      <div className="bg-white border border-slate-200 rounded-b-2xl overflow-hidden shadow-sm">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 text-sm font-semibold uppercase tracking-wider">
              <th className="py-4 px-6">Admission No</th>
              <th className="py-4 px-6">Full Name</th>
              <th className="py-4 px-6">Class/Sec</th>
              <th className="py-4 px-6">Status</th>
              <th className="py-4 px-6 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {filteredStudents.length > 0 ? (
              filteredStudents.map((student) => (
                <tr key={student.id} className="hover:bg-blue-50/50 transition-colors group cursor-pointer">
                  <td className="py-4 px-6 font-medium text-slate-900">{student.admission_no}</td>
                  <td className="py-4 px-6 text-slate-700 font-medium">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center text-xs font-bold text-slate-600">
                        {student.full_name.charAt(0)}
                      </div>
                      {student.full_name}
                    </div>
                  </td>
                  <td className="py-4 px-6 text-slate-600">{student.class} - {student.section}</td>
                  <td className="py-4 px-6">
                    <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold
                      ${student.status === 'active' ? 'bg-emerald-100 text-emerald-700' : ''}
                      ${student.status === 'transferred' ? 'bg-amber-100 text-amber-700' : ''}
                      ${student.status === 'archived' ? 'bg-slate-100 text-slate-600' : ''}
                    `}>
                      {student.status.charAt(0).toUpperCase() + student.status.slice(1)}
                    </span>
                  </td>
                  <td className="py-4 px-6 text-right">
                    <button className="text-slate-400 hover:text-blue-600 transition-colors p-2 rounded-lg hover:bg-blue-50">
                      <MoreVertical className="w-5 h-5" />
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={5} className="py-12 text-center text-slate-500">
                  No students found matching your criteria.
                </td>
              </tr>
            )}
          </tbody>
        </table>
        
        {/* Pagination Footer */}
        <div className="bg-slate-50 border-t border-slate-200 p-4 flex items-center justify-between text-sm text-slate-600">
          <div>Showing 1 to {filteredStudents.length} of {students.length} entries</div>
          <div className="flex gap-2">
            <button className="p-2 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 disabled:opacity-50 text-slate-400 cursor-not-allowed">
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button className="p-2 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 disabled:opacity-50 text-slate-400 cursor-not-allowed">
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Admission Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-slate-900/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
          <div className="bg-white rounded-2xl w-full max-w-md shadow-xl overflow-hidden">
            <div className="flex justify-between items-center p-6 border-b border-slate-100">
              <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                <GraduationCap className="w-6 h-6 text-blue-600" />
                New Student Admission
              </h2>
              <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-slate-600 p-1">
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1">Full Legal Name</label>
                <input 
                  type="text" 
                  value={newStudent.full_name}
                  onChange={(e) => setNewStudent({...newStudent, full_name: e.target.value})}
                  className="w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none"
                  placeholder="e.g. Rahul Sharma"
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-1">Class</label>
                  <select 
                    value={newStudent.class}
                    onChange={(e) => setNewStudent({...newStudent, class: e.target.value})}
                    className="w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none bg-white"
                  >
                    {[1,2,3,4,5,6,7,8,9,10,11,12].map(c => (
                      <option key={c} value={c}>Class {c}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-1">Section</label>
                  <select 
                    value={newStudent.section}
                    onChange={(e) => setNewStudent({...newStudent, section: e.target.value})}
                    className="w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none bg-white"
                  >
                    {['A','B','C','D'].map(s => (
                      <option key={s} value={s}>Section {s}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            <div className="p-6 bg-slate-50 border-t border-slate-100 flex gap-3 justify-end">
              <button 
                onClick={() => setIsModalOpen(false)}
                className="px-5 py-2.5 rounded-xl font-medium text-slate-600 hover:bg-slate-200 transition-colors"
              >
                Cancel
              </button>
              <button 
                onClick={() => {
                  if (!newStudent.full_name.trim()) return alert('Name is required!');
                  setStudents([{
                    id: Date.now().toString(),
                    admission_no: `ADM-2026-${Math.floor(Math.random() * 900) + 100}`,
                    full_name: newStudent.full_name,
                    status: "active",
                    class: newStudent.class,
                    section: newStudent.section
                  }, ...students]);
                  setIsModalOpen(false);
                  setNewStudent({ full_name: "", class: "1", section: "A" });
                }}
                className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-xl font-medium transition-colors shadow-sm"
              >
                Admit Student
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
