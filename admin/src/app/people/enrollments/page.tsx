"use client";

import { useState, useEffect } from "react";

export default function EnrollmentsPage() {
  const [enrollments, setEnrollments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchEnrollments() {
      try {
        const res = await fetch("/api/v1/people/student-enrollments", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        if (!res.ok) {
          throw new Error("Failed to fetch enrollments");
        }
        const data = await res.json();
        setEnrollments(data.data || []);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    // We would need to implement the GET /student-enrollments API 
    // Since Phase 4 specifies POST /student-enrollments, we will display an empty state for now 
    // to simulate the UI, or hit a query endpoint.
    setLoading(false);
  }, []);

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Student Enrollments</h1>
        <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
          New Enrollment
        </button>
      </div>
      
      {loading && <p>Loading enrollments...</p>}
      {error && <p className="text-red-500">{error}</p>}
      
      {!loading && !error && enrollments.length === 0 && (
        <div className="bg-white p-8 border border-gray-200 rounded-lg text-center">
          <p className="text-gray-500 mb-4">No active enrollments found for the current academic year.</p>
          <button className="px-4 py-2 bg-gray-100 text-gray-800 rounded hover:bg-gray-200">
            Bulk Import Enrollments
          </button>
        </div>
      )}

      {/* Table would go here */}
    </div>
  );
}
