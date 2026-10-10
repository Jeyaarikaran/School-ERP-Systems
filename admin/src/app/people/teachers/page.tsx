"use client";

import { useState, useEffect } from "react";

export default function TeachersPage() {
  const [teachers, setTeachers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchTeachers() {
      try {
        // Assuming we combine staff endpoint filtering by 'teacher'
        const res = await fetch("/api/v1/people/teachers", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        if (!res.ok) {
          throw new Error("Failed to fetch teachers");
        }
        const data = await res.json();
        setTeachers(data.data || []);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchTeachers();
  }, []);

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Teachers</h1>
        <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
          Add Teacher
        </button>
      </div>
      
      {loading && <p>Loading teachers...</p>}
      {error && <p className="text-red-500">{error}</p>}
      
      {!loading && !error && teachers.length === 0 && (
        <p>No teachers found.</p>
      )}

      {!loading && !error && teachers.length > 0 && (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border border-gray-200 shadow-sm rounded-lg">
            <thead className="bg-gray-50">
              <tr>
                <th className="py-3 px-4 border-b text-left text-sm font-semibold text-gray-600">ID</th>
                <th className="py-3 px-4 border-b text-left text-sm font-semibold text-gray-600">Specialization</th>
                <th className="py-3 px-4 border-b text-left text-sm font-semibold text-gray-600">Qualification</th>
                <th className="py-3 px-4 border-b text-left text-sm font-semibold text-gray-600">Actions</th>
              </tr>
            </thead>
            <tbody>
              {teachers.map((t: any) => (
                <tr key={t.id} className="hover:bg-gray-50 transition-colors">
                  <td className="py-3 px-4 border-b text-sm font-medium text-gray-800">{t.id.slice(0, 8)}</td>
                  <td className="py-3 px-4 border-b text-sm text-gray-600">{t.specialization || 'N/A'}</td>
                  <td className="py-3 px-4 border-b text-sm text-gray-600">{t.qualification || 'N/A'}</td>
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
