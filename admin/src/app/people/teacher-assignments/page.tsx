"use client";

import { useState, useEffect } from "react";

export default function TeacherAssignmentsPage() {
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchAssignments() {
      try {
        const res = await fetch("/api/v1/people/teacher-assignments", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        if (!res.ok) {
          throw new Error("Failed to fetch assignments");
        }
        const data = await res.json();
        setAssignments(data.data || []);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    // We would need to implement the GET /teacher-assignments API 
    // Since Phase 4 specifies POST /teacher-assignments, we will display an empty state for now 
    // to simulate the UI, or hit a query endpoint.
    setLoading(false);
  }, []);

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Teacher Subject Assignments</h1>
        <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
          Assign Teacher
        </button>
      </div>
      
      {loading && <p>Loading assignments...</p>}
      {error && <p className="text-red-500">{error}</p>}
      
      {!loading && !error && assignments.length === 0 && (
        <div className="bg-white p-8 border border-gray-200 rounded-lg text-center">
          <p className="text-gray-500 mb-4">No teacher assignments found for the current academic year.</p>
        </div>
      )}

      {/* Table would go here */}
    </div>
  );
}
