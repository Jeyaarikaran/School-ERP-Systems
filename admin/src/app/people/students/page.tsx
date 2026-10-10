"use client";

import { useState, useEffect } from "react";

export default function StudentsPage() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchStudents() {
      try {
        const res = await fetch("/api/v1/people/students", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        if (!res.ok) {
          if (res.status === 401 || res.status === 403) {
            throw new Error("Unauthorized or Forbidden");
          }
          throw new Error("Failed to fetch students");
        }
        const data = await res.json();
        setStudents(data.data || []);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchStudents();
  }, []);

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Students</h1>
        <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
          Add Student
        </button>
      </div>
      
      {loading && <p>Loading students...</p>}
      {error && <p className="text-red-500">{error}</p>}
      
      {!loading && !error && students.length === 0 && (
        <p>No students found.</p>
      )}

      {!loading && !error && students.length > 0 && (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border border-gray-200 shadow-sm rounded-lg">
            <thead className="bg-gray-50">
              <tr>
                <th className="py-3 px-4 border-b text-left text-sm font-semibold text-gray-600">Admission No</th>
                <th className="py-3 px-4 border-b text-left text-sm font-semibold text-gray-600">Name</th>
                <th className="py-3 px-4 border-b text-left text-sm font-semibold text-gray-600">Gender</th>
                <th className="py-3 px-4 border-b text-left text-sm font-semibold text-gray-600">Status</th>
                <th className="py-3 px-4 border-b text-left text-sm font-semibold text-gray-600">Actions</th>
              </tr>
            </thead>
            <tbody>
              {students.map((student: any) => (
                <tr key={student.id} className="hover:bg-gray-50 transition-colors">
                  <td className="py-3 px-4 border-b text-sm">{student.admission_no}</td>
                  <td className="py-3 px-4 border-b text-sm font-medium text-gray-800">{student.full_name}</td>
                  <td className="py-3 px-4 border-b text-sm text-gray-600 capitalize">{student.gender}</td>
                  <td className="py-3 px-4 border-b text-sm">
                    <span className={`px-2 py-1 rounded-full text-xs font-semibold
                      ${student.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                      {student.status.toUpperCase()}
                    </span>
                  </td>
                  <td className="py-3 px-4 border-b text-sm">
                    <button className="text-blue-600 hover:text-blue-800 mr-3">Edit</button>
                    <button className="text-gray-600 hover:text-gray-800">View</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
