"use client";

import { useState } from "react";
import { Banknote, CreditCard, Receipt, FileSignature, Check, X, ShieldAlert } from "lucide-react";

// Mock Ledger Data (Phase 7)
const initialLedger = [
  { id: "1", date: "Oct 1, 2026", type: "Fee Payment", student: "Aarav Patel", amount: 15000, status: "captured", mode: "card_pos" },
  { id: "2", date: "Oct 2, 2026", type: "Refund Request", student: "Rohan Iyer", amount: 2500, status: "requested", mode: "bank_transfer" },
  { id: "3", date: "Oct 3, 2026", type: "Adjustment", student: "Ananya Singh", amount: 1000, status: "approved", mode: "scholarship" },
  { id: "4", date: "Oct 4, 2026", type: "Fee Payment", student: "Kabir Khan", amount: 12000, status: "failed", mode: "upi_offline" },
  { id: "5", date: "Oct 5, 2026", type: "Refund Request", student: "Diya Sharma", amount: 5000, status: "requested", mode: "cheque" },
];

export default function FinancePage() {
  const [ledger, setLedger] = useState(initialLedger);

  // Simulates Phase 7 Two-Step Approval for Refunds
  const handleAction = (id: string, newStatus: string) => {
    setLedger(current => 
      current.map(entry => 
        entry.id === id ? { ...entry, status: newStatus } : entry
      )
    );
  };

  return (
    <div className="p-8 max-w-7xl mx-auto h-[calc(100vh-64px)] overflow-y-auto">
      <div className="flex items-center justify-between mb-8 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 mb-2 flex items-center gap-3">
            <Banknote className="w-8 h-8 text-green-600" />
            Financial Ledger
          </h1>
          <p className="text-slate-500">Immutable ledger, gateway webhooks, and refund approvals.</p>
        </div>
        <div className="flex gap-4">
          <button className="bg-slate-100 hover:bg-slate-200 text-slate-700 px-5 py-2.5 rounded-xl font-medium transition-colors flex items-center gap-2">
            <Receipt className="w-5 h-5" />
            Issue Receipt
          </button>
          <button className="bg-green-600 hover:bg-green-700 text-white px-5 py-2.5 rounded-xl font-medium transition-colors flex items-center gap-2 shadow-sm">
            <CreditCard className="w-5 h-5" />
            Collect Payment
          </button>
        </div>
      </div>

      <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 text-sm font-semibold uppercase tracking-wider">
              <th className="py-4 px-6">Date</th>
              <th className="py-4 px-6">Transaction Type</th>
              <th className="py-4 px-6">Student</th>
              <th className="py-4 px-6">Amount (₹)</th>
              <th className="py-4 px-6">Status</th>
              <th className="py-4 px-6 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {ledger.map((entry) => (
              <tr key={entry.id} className="hover:bg-slate-50 transition-colors">
                <td className="py-4 px-6 text-slate-500 font-medium">{entry.date}</td>
                <td className="py-4 px-6 text-slate-900 font-medium">
                  {entry.type}
                  <div className="text-xs text-slate-400 mt-1 uppercase tracking-wider">{entry.mode}</div>
                </td>
                <td className="py-4 px-6 text-slate-700">{entry.student}</td>
                <td className="py-4 px-6 font-semibold text-slate-900">
                  ₹{entry.amount.toLocaleString()}
                </td>
                <td className="py-4 px-6">
                  <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold
                    ${entry.status === 'captured' ? 'bg-emerald-100 text-emerald-700' : ''}
                    ${entry.status === 'approved' ? 'bg-blue-100 text-blue-700' : ''}
                    ${entry.status === 'requested' ? 'bg-amber-100 text-amber-700 border border-amber-200' : ''}
                    ${entry.status === 'failed' || entry.status === 'rejected' ? 'bg-rose-100 text-rose-700' : ''}
                  `}>
                    {entry.status.charAt(0).toUpperCase() + entry.status.slice(1)}
                  </span>
                </td>
                <td className="py-4 px-6 text-right">
                  {entry.status === 'requested' ? (
                    <div className="flex justify-end gap-2">
                      <button 
                        onClick={() => handleAction(entry.id, 'approved')}
                        title="Approve Refund"
                        className="p-2 bg-emerald-50 text-emerald-600 hover:bg-emerald-100 rounded-lg transition-colors"
                      >
                        <Check className="w-5 h-5" />
                      </button>
                      <button 
                        onClick={() => handleAction(entry.id, 'rejected')}
                        title="Reject Refund"
                        className="p-2 bg-rose-50 text-rose-600 hover:bg-rose-100 rounded-lg transition-colors"
                      >
                        <X className="w-5 h-5" />
                      </button>
                    </div>
                  ) : (
                    <button className="text-slate-400 hover:text-slate-600 transition-colors flex items-center gap-1 text-sm font-medium float-right">
                      <FileSignature className="w-4 h-4" /> View
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {/* Security Notice */}
      <div className="mt-6 bg-slate-50 border border-slate-200 rounded-xl p-4 flex items-start gap-3">
        <ShieldAlert className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
        <div className="text-sm text-slate-600">
          <strong className="text-slate-900 block mb-1">Row-Level Security Active</strong>
          As an Administrator, you cannot approve refund requests that you initiated yourself. The system enforces strict Separation of Duties (SoD) per Phase 7 compliance.
        </div>
      </div>
    </div>
  );
}
