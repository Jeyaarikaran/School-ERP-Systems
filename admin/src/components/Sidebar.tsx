"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  GraduationCap, 
  CalendarDays, 
  Bus, 
  Banknote, 
  MessageSquare, 
  LineChart, 
  Settings,
  Library as LibraryIcon,
  Users,
  FileSpreadsheet,
  ShieldCheck,
  LogOut
} from "lucide-react";
import { useAuth } from "./AuthProvider";

const allNavigation = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard, roles: ["super_admin", "school_admin", "teacher", "student", "parent", "hr_admin"] },
  { name: "Academics", href: "/academics", icon: GraduationCap, roles: ["super_admin", "school_admin", "teacher", "student", "parent"] },
  { name: "Students", href: "/students", icon: Users, roles: ["super_admin", "school_admin", "teacher"] },
  { name: "Attendance", href: "/attendance", icon: CalendarDays, roles: ["super_admin", "school_admin", "teacher", "student", "parent", "hr_admin"] },
  { name: "Transport", href: "/transport", icon: Bus, roles: ["super_admin", "school_admin", "student", "parent"] },
  { name: "Finance", href: "/finance", icon: Banknote, roles: ["super_admin", "school_admin", "parent", "hr_admin"] },
  { name: "Communication", href: "/communication", icon: MessageSquare, roles: ["super_admin", "school_admin", "teacher", "student", "parent", "hr_admin"] },
  { name: "Library", href: "/library", icon: LibraryIcon, roles: ["super_admin", "school_admin", "student", "teacher"] },
  { name: "Reports", href: "/reports", icon: FileSpreadsheet, roles: ["super_admin", "school_admin", "teacher", "hr_admin"] },
  { name: "Insights & AI", href: "/insights", icon: LineChart, roles: ["super_admin", "school_admin"] },
  { name: "Settings", href: "/settings", icon: Settings, roles: ["super_admin", "school_admin", "hr_admin"] },
];

export function Sidebar() {
  const pathname = usePathname();
  const { logout, user } = useAuth();

  if (pathname === "/login") return null;

  // Filter navigation based on user role (default to student if no role is found)
  const userRole = user?.role || "student";
  const permittedNavigation = allNavigation.filter(item => item.roles.includes(userRole));

  return (
    <div className="flex h-screen w-64 flex-col border-r border-slate-200 bg-white fixed top-0 left-0">
      <div className="flex h-16 items-center px-6 border-b border-slate-100">
        <Link href="/" className="flex items-center gap-2">
          <div className="bg-blue-600 p-1.5 rounded-lg">
            <ShieldCheck className="w-5 h-5 text-white" />
          </div>
          <div className="flex flex-col">
            <span className="text-lg font-bold tracking-tight text-slate-900 leading-none">EduCore ERP</span>
            <span className="text-[10px] font-bold text-blue-600 uppercase tracking-wider mt-1">{userRole.replace('_', ' ')} PORTAL</span>
          </div>
        </Link>
      </div>
      
      <div className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
        {permittedNavigation.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
          const Icon = item.icon;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive 
                  ? "bg-blue-50 text-blue-700" 
                  : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
              }`}
            >
              <Icon className={`w-5 h-5 ${isActive ? "text-blue-600" : "text-slate-400"}`} />
              {item.name}
            </Link>
          );
        })}
      </div>

      <div className="p-4 border-t border-slate-100">
        <button
          onClick={logout}
          className="flex w-full items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-rose-600 hover:bg-rose-50 transition-colors"
        >
          <LogOut className="w-5 h-5" />
          Logout
        </button>
      </div>
    </div>
  );
}
