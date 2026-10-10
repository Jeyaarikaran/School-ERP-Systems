"use client";

import { useState, useEffect } from "react";

export default function ClassesPage() {
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchClasses() {
      try {
        const res = await fetch("/api/v1/academics/classes", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        if (!res.ok) {
          if (res.status === 401 || res.status === 403) {
            throw new Error("Unauthorized or Forbidden");
          }
          throw new Error("Failed to fetch classes");
        }
        const data = await res.json();
        setClasses(data.data || []);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchClasses();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Classes</h1>
      
      {loading && <p>Loading classes...</p>}
      {error && <p className="text-red-500">{error}</p>}
      
      {!loading && !error && classes.length === 0 && (
        <p>No classes found.</p>
      )}

      {!loading && !error && classes.length > 0 && (
        <table className="min-w-full bg-white border border-gray-200">
          <thead>
            <tr>
              <th className="py-2 px-4 border-b text-left">Name</th>
              <th className="py-2 px-4 border-b text-left">Level</th>
            </tr>
          </thead>
          <tbody>
            {classes.map((cls: any) => (
              <tr key={cls.id}>
                <td className="py-2 px-4 border-b">{cls.name}</td>
                <td className="py-2 px-4 border-b">{cls.level}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
