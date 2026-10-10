"use client";

import { Bell, Search, Menu } from "lucide-react";
import { usePathname } from "next/navigation";

export function Header() {
  const pathname = usePathname();
  
  if (pathname === "/login") return null;

  return (
    <header className="h-16 border-b border-slate-200 bg-white/80 backdrop-blur-md sticky top-0 z-40">
      <div className="flex h-full items-center justify-between px-4 sm:px-6 lg:px-8">
        
        {/* Mobile menu button */}
        <button className="lg:hidden p-2 -ml-2 text-slate-500 hover:text-slate-900">
          <Menu className="w-6 h-6" />
        </button>

        {/* Global Search */}
        <div className="flex-1 flex max-w-2xl px-4 lg:px-0">
          <div className="relative w-full max-w-md hidden md:block">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-4 w-4 text-slate-400" />
            </div>
            <input
              type="text"
              placeholder="Search students, staff, or settings... (Press '/')"
              className="block w-full pl-10 pr-3 py-2 border border-slate-200 rounded-lg leading-5 bg-slate-50 placeholder-slate-400 focus:outline-none focus:bg-white focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors"
            />
          </div>
        </div>

        {/* Right Nav */}
        <div className="flex items-center gap-4">
          <button className="relative p-2 text-slate-400 hover:text-slate-500 transition-colors">
            <Bell className="w-5 h-5" />
            <span className="absolute top-1.5 right-1.5 block h-2 w-2 rounded-full bg-rose-500 ring-2 ring-white" />
          </button>
          
          <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-blue-600 to-purple-600 flex items-center justify-center text-white font-medium text-sm shadow-sm ring-2 ring-white">
            JD
          </div>
        </div>
      </div>
    </header>
  );
}
