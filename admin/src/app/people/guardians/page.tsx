"use client";

import { useState, useEffect } from "react";

export default function GuardiansPage() {
  const [guardians, setGuardians] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchGuardians() {
      try {
        const res = await fetch("/api/v1/people/parents", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        if (!res.ok) {
          throw new Error("Failed to fetch guardians");
        }
        const data = await res.json();
        setGuardians(data.data || []);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchGuardians();
  }, []);

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Guardians / Parents</h1>
        <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
          Add Guardian
        </button>
      </div>
      
      {loading && <p>Loading guardians...</p>}
      {error && <p className="text-red-500">{error}</p>}
      
      {!loading && !error && guardians.length === 0 && (
        <p>No guardians found.</p>
      )}

      {!loading && !error && guardians.length > 0 && (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border border-gray-200 shadow-sm rounded-lg">
            <thead className="bg-gray-50">
              <tr>
                <th className="py-3 px-4 border-b text-left text-sm font-semibold text-gray-600">Name</th>
                <th className="py-3 px-4 border-b text-left text-sm font-semibold text-gray-600">Phone</th>
                <th className="py-3 px-4 border-b text-left text-sm font-semibold text-gray-600">Email</th>
                <th className="py-3 px-4 border-b text-left text-sm font-semibold text-gray-600">Actions</th>
              </tr>
            </thead>
            <tbody>
              {guardians.map((g: any) => (
                <tr key={g.id} className="hover:bg-gray-50 transition-colors">
                  <td className="py-3 px-4 border-b text-sm font-medium text-gray-800">{g.full_name}</td>
                  <td className="py-3 px-4 border-b text-sm text-gray-600">{g.phone}</td>
                  <td className="py-3 px-4 border-b text-sm text-gray-600">{g.email || 'N/A'}</td>
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
