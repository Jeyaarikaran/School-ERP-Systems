"use client";

import { useState } from "react";
import { MessageSquare, Send, Bell, AlertTriangle, Users, Clock } from "lucide-react";

// Mock Data for Phase 8 Communication Outbox
const initialMessages = [
  { id: "1", title: "Mid-Term Exam Schedule", audience: "Class 10", channels: ["FCM", "Email"], status: "sent", date: "Oct 5, 2026, 09:00 AM" },
  { id: "2", title: "Bus Delay: Route 4", audience: "Route 4 Parents", channels: ["SMS", "FCM"], status: "sent", date: "Oct 5, 2026, 07:30 AM" },
  { id: "3", title: "Fee Reminder (Q3)", audience: "Defaulters", channels: ["Email", "SMS"], status: "queued", date: "Oct 5, 2026, 02:00 PM" },
];

export default function CommunicationPage() {
  const [messages, setMessages] = useState(initialMessages);
  const [isDrafting, setIsDrafting] = useState(false);

  return (
    <div className="p-8 max-w-7xl mx-auto h-[calc(100vh-64px)] overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 mb-2 flex items-center gap-3">
            <MessageSquare className="w-8 h-8 text-violet-600" />
            Communication Hub
          </h1>
          <p className="text-slate-500">Manage announcements, emergency alerts, and push notifications (Phase 8)</p>
        </div>
        
        <div className="flex gap-4">
          <button className="bg-rose-100 hover:bg-rose-200 text-rose-700 px-5 py-2.5 rounded-xl font-medium transition-colors flex items-center gap-2">
            <AlertTriangle className="w-5 h-5" />
            Emergency Alert
          </button>
          <button 
            onClick={() => setIsDrafting(!isDrafting)}
            className="bg-violet-600 hover:bg-violet-700 text-white px-5 py-2.5 rounded-xl font-medium transition-colors flex items-center gap-2 shadow-sm"
          >
            <Send className="w-5 h-5" />
            New Announcement
          </button>
        </div>
      </div>

      {isDrafting && (
        <div className="mb-8 bg-white p-6 rounded-2xl shadow-sm border border-slate-200 animate-in fade-in slide-in-from-top-4">
          <h2 className="text-lg font-bold text-slate-800 mb-4">Draft Announcement</h2>
          <div className="space-y-4">
            <input type="text" placeholder="Announcement Title" className="w-full p-3 rounded-xl border border-slate-200 bg-slate-50 outline-none focus:ring-2 focus:ring-violet-500" />
            <textarea placeholder="Write your message here..." rows={4} className="w-full p-3 rounded-xl border border-slate-200 bg-slate-50 outline-none focus:ring-2 focus:ring-violet-500"></textarea>
            
            <div className="flex gap-6">
              <div className="flex-1">
                <label className="block text-sm font-semibold text-slate-600 mb-2">Target Audience</label>
                <select className="w-full p-3 rounded-xl border border-slate-200 bg-slate-50 outline-none focus:ring-2 focus:ring-violet-500">
                  <option>All Parents</option>
                  <option>Specific Class/Section</option>
                  <option>All Staff</option>
                </select>
              </div>
              <div className="flex-1">
                <label className="block text-sm font-semibold text-slate-600 mb-2">Delivery Channels</label>
                <div className="flex gap-4 items-center h-12">
                  <label className="flex items-center gap-2 text-slate-700 font-medium cursor-pointer"><input type="checkbox" defaultChecked className="w-4 h-4 rounded text-violet-600 focus:ring-violet-500" /> Push (FCM)</label>
                  <label className="flex items-center gap-2 text-slate-700 font-medium cursor-pointer"><input type="checkbox" defaultChecked className="w-4 h-4 rounded text-violet-600 focus:ring-violet-500" /> Email</label>
                  <label className="flex items-center gap-2 text-slate-700 font-medium cursor-pointer"><input type="checkbox" className="w-4 h-4 rounded text-violet-600 focus:ring-violet-500" /> SMS (Fallback)</label>
                </div>
              </div>
            </div>
            
            <div className="flex justify-end gap-3 mt-4">
              <button onClick={() => setIsDrafting(false)} className="px-5 py-2.5 rounded-xl font-medium text-slate-600 hover:bg-slate-100">Cancel</button>
              <button onClick={() => setIsDrafting(false)} className="px-5 py-2.5 rounded-xl font-medium text-white bg-violet-600 hover:bg-violet-700">Dispatch via Outbox</button>
            </div>
          </div>
        </div>
      )}

      {/* Outbox / History Table */}
      <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
        <div className="px-6 py-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <h3 className="font-bold text-slate-800 flex items-center gap-2">
            <Bell className="w-5 h-5 text-slate-400" /> Recent Dispatches
          </h3>
        </div>
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-white border-b border-slate-100 text-slate-400 text-sm font-semibold uppercase tracking-wider">
              <th className="py-4 px-6">Message Title</th>
              <th className="py-4 px-6">Audience</th>
              <th className="py-4 px-6">Channels</th>
              <th className="py-4 px-6">Status / Time</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {messages.map((msg) => (
              <tr key={msg.id} className="hover:bg-slate-50 transition-colors">
                <td className="py-4 px-6 font-medium text-slate-900">{msg.title}</td>
                <td className="py-4 px-6 text-slate-600 flex items-center gap-2"><Users className="w-4 h-4 text-slate-400" /> {msg.audience}</td>
                <td className="py-4 px-6">
                  <div className="flex gap-2">
                    {msg.channels.map(ch => (
                      <span key={ch} className="px-2 py-1 bg-slate-100 text-slate-600 rounded text-xs font-semibold">{ch}</span>
                    ))}
                  </div>
                </td>
                <td className="py-4 px-6">
                  <div className="flex items-center gap-3">
                    <span className={`w-2 h-2 rounded-full ${msg.status === 'sent' ? 'bg-emerald-500' : 'bg-amber-500'}`}></span>
                    <div>
                      <div className="text-sm font-semibold text-slate-900 capitalize">{msg.status}</div>
                      <div className="text-xs text-slate-500 flex items-center gap-1"><Clock className="w-3 h-3" /> {msg.date}</div>
                    </div>
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
