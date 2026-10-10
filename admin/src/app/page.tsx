"use client";

import { Users, GraduationCap, Banknote, CalendarCheck, TrendingUp, Bus, BookOpen, Clock, CalendarDays, Award } from "lucide-react";
import { useAuth } from "@/components/AuthProvider";

export default function Home() {
  const { user } = useAuth();
  const role = user?.role || "student";

  // -------------------------------------------------------------
  // STUDENT DASHBOARD
  // -------------------------------------------------------------
  if (role === "student") {
    return (
      <div className="p-8 max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900">Student Dashboard</h1>
          <p className="text-slate-500 mt-1">Welcome back, {user?.email}! Here is your academic summary.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard title="My Attendance" value="98.5%" icon={CalendarCheck} color="bg-emerald-500" trend="Excellent" />
          <StatCard title="Upcoming Exams" value="3" icon={Award} color="bg-blue-500" trend="Next: Mathematics" />
          <StatCard title="Library Books" value="1 Due" icon={BookOpen} color="bg-purple-500" trend="Due in 2 days" />
          <StatCard title="Today's Classes" value="6" icon={Clock} color="bg-amber-500" trend="Next: Physics lab" />
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
          <h2 className="text-lg font-bold text-slate-900 mb-6">Today&apos;s Schedule</h2>
          <div className="space-y-4">
            <ActivityItem title="Mathematics (Mr. Sharma)" time="09:00 AM - 10:00 AM" icon={Clock} color="text-blue-600 bg-blue-100" />
            <ActivityItem title="Physics Lab (Mrs. Gupta)" time="10:15 AM - 11:45 AM" icon={Clock} color="text-purple-600 bg-purple-100" />
            <ActivityItem title="Lunch Break" time="11:45 AM - 12:30 PM" icon={CalendarDays} color="text-amber-600 bg-amber-100" />
            <ActivityItem title="Computer Science (Mr. Iyer)" time="12:30 PM - 02:00 PM" icon={Clock} color="text-emerald-600 bg-emerald-100" />
          </div>
        </div>
      </div>
    );
  }

  // -------------------------------------------------------------
  // TEACHER DASHBOARD
  // -------------------------------------------------------------
  if (role === "teacher") {
    return (
      <div className="p-8 max-w-7xl mx-auto">
        <div className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Teacher Dashboard</h1>
            <p className="text-slate-500 mt-1">Manage your classes and students.</p>
          </div>
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium shadow-sm transition-colors">
            Mark Attendance
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard title="My Students" value="142" icon={Users} color="bg-blue-500" trend="Across 4 sections" />
          <StatCard title="Pending Assignments" value="28" icon={BookOpen} color="bg-amber-500" trend="Needs grading" />
          <StatCard title="Class Attendance" value="92%" icon={CalendarCheck} color="bg-emerald-500" trend="Class 10-A" />
          <StatCard title="Upcoming Classes" value="4" icon={Clock} color="bg-purple-500" trend="Today" />
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
          <h2 className="text-lg font-bold text-slate-900 mb-6">Recent Student Activity</h2>
          <div className="space-y-6">
            <ActivityItem title="Rahul submitted Physics Assignment" time="10 mins ago" icon={BookOpen} color="text-blue-600 bg-blue-100" />
            <ActivityItem title="Ananya marked absent" time="1 hour ago" icon={CalendarCheck} color="text-rose-600 bg-rose-100" />
          </div>
        </div>
      </div>
    );
  }

  // -------------------------------------------------------------
  // HR ADMIN DASHBOARD
  // -------------------------------------------------------------
  if (role === "hr_admin") {
    return (
      <div className="p-8 max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900">HR Dashboard</h1>
          <p className="text-slate-500 mt-1">Staff management and payroll overview.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatCard title="Total Staff" value="128" icon={Users} color="bg-blue-500" trend="Active employees" />
          <StatCard title="On Leave Today" value="4" icon={CalendarDays} color="bg-rose-500" trend="Requires substitutes" />
          <StatCard title="Payroll Disbursed" value="$125,000" icon={Banknote} color="bg-emerald-500" trend="This month" />
        </div>
      </div>
    );
  }

  // -------------------------------------------------------------
  // DEFAULT: SUPER ADMIN / SCHOOL ADMIN DASHBOARD
  // -------------------------------------------------------------
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">School Admin Dashboard</h1>
          <p className="text-slate-500 mt-1">Welcome back! Here&apos;s a high-level overview of the school.</p>
        </div>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium shadow-sm transition-colors">
          Generate Master Report
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard title="Total Students" value="1,248" icon={Users} color="bg-blue-500" trend="+12 this month" />
        <StatCard title="Teaching Staff" value="84" icon={GraduationCap} color="bg-purple-500" trend="+2 this month" />
        <StatCard title="Daily Attendance" value="94.2%" icon={CalendarCheck} color="bg-emerald-500" trend="On track" />
        <StatCard title="Fee Collection" value="$42,500" icon={Banknote} color="bg-amber-500" trend="85% collected" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Chart Area */}
        <div className="lg:col-span-2 bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-bold text-slate-900">Revenue Analytics (Strictly Admin)</h2>
            <TrendingUp className="text-slate-400 w-5 h-5" />
          </div>
          <div className="h-64 flex items-end justify-between gap-2 px-2">
            {[40, 70, 45, 90, 65, 100, 85].map((h, i) => (
              <div key={i} className="w-full bg-blue-100 rounded-t-md relative group">
                <div 
                  className="absolute bottom-0 w-full bg-blue-500 rounded-t-md transition-all duration-500" 
                  style={{ height: `${h}%` }}
                ></div>
              </div>
            ))}
          </div>
          <div className="flex justify-between mt-4 text-xs font-medium text-slate-500">
            <span>Jan</span><span>Feb</span><span>Mar</span><span>Apr</span><span>May</span><span>Jun</span><span>Jul</span>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
          <h2 className="text-lg font-bold text-slate-900 mb-6">Global Activity</h2>
          <div className="space-y-6">
            <ActivityItem title="New Student Enrolled" time="10 mins ago" icon={Users} color="text-blue-600 bg-blue-100" />
            <ActivityItem title="Term 2 Fees Paid" time="1 hour ago" icon={Banknote} color="text-emerald-600 bg-emerald-100" />
            <ActivityItem title="Bus 4 Delayed" time="2 hours ago" icon={Bus} color="text-amber-600 bg-amber-100" />
            <ActivityItem title="Library Book Issued" time="3 hours ago" icon={GraduationCap} color="text-purple-600 bg-purple-100" />
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon: Icon, color, trend }: { title: string, value: string, icon: any, color: string, trend: string }) {
  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex flex-col">
      <div className="flex justify-between items-start mb-4">
        <div className={`p-3 rounded-xl text-white ${color} shadow-sm`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
      <h3 className="text-slate-500 text-sm font-medium mb-1">{title}</h3>
      <p className="text-2xl font-bold text-slate-900 mb-2">{value}</p>
      <p className="text-xs text-slate-500 font-medium">{trend}</p>
    </div>
  );
}

function ActivityItem({ title, time, icon: Icon, color }: { title: string, time: string, icon: any, color: string }) {
  return (
    <div className="flex items-start gap-4">
      <div className={`p-2 rounded-lg ${color}`}>
        <Icon className="w-4 h-4" />
      </div>
      <div>
        <h4 className="text-sm font-bold text-slate-900">{title}</h4>
        <p className="text-xs text-slate-500 mt-0.5">{time}</p>
      </div>
    </div>
  );
}
