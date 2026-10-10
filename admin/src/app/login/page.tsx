"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/components/AuthProvider";
import { ShieldCheck, Loader2 } from "lucide-react";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const trimmedEmail = email.trim();
      const trimmedPassword = password.trim();

      // 🚀 FRONTEND DEMO BYPASS: MULTI-ROLE SUPPORT
      // Since the backend server is not running on port 8000 right now,
      // we will intercept hardcoded credentials and assign the correct mock role!
      
      const mockUsers: Record<string, string> = {
        "admin@school.edu": "super_admin",
        "principal@school.edu": "school_admin",
        "teacher@school.edu": "teacher",
        "student@school.edu": "student",
        "parent@school.edu": "parent",
        "librarian@school.edu": "librarian",
        "transport@school.edu": "transport_admin",
        "hr@school.edu": "hr_admin",
        "hari@student.com": "student", // Added Hari specifically
        "hariparent@school.com": "parent",
      };

      if (mockUsers[trimmedEmail] && (trimmedPassword === "demo123" || trimmedPassword === "hari@2006")) {
        const mockUser = {
          id: `usr-${mockUsers[trimmedEmail]}`,
          email: trimmedEmail,
          role: mockUsers[trimmedEmail],
          school_id: "sch-001"
        };
        login(`mock-jwt-token-${mockUsers[trimmedEmail]}`, mockUser);
        return;
      }

      // Legacy fallback for the old admin password
      if (trimmedEmail === "admin@school.edu" && trimmedPassword === "admin") {
        const mockUser = {
          id: "usr-123",
          email: email,
          role: "super_admin",
          school_id: "sch-001"
        };
        login("mock-jwt-token-777", mockUser);
        return;
      }

      // 1. Get Token (This will fail if backend is offline)
      const res = await api.login(trimmedEmail, trimmedPassword);
      
      // 2. Mock fetching the user details
      const mockUser = {
        id: "usr-123",
        email: trimmedEmail,
        role: "admin",
        school_id: "sch-123"
      };

      login(res.access_token, mockUser);
    } catch (err: any) {
      setError(err?.data?.detail || "Invalid credentials. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <div className="bg-blue-600 p-3 rounded-2xl shadow-lg shadow-blue-600/20">
            <ShieldCheck className="w-10 h-10 text-white" />
          </div>
        </div>
        <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-slate-900">
          Sign in to EduCore ERP
        </h2>
        <p className="mt-2 text-center text-sm text-slate-600">
          Secure Administrative Portal
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow-xl shadow-slate-200/50 sm:rounded-2xl sm:px-10 border border-slate-100">
          <form className="space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="bg-rose-50 border border-rose-200 text-rose-600 px-4 py-3 rounded-lg text-sm">
                {error}
              </div>
            )}
            
            <div>
              <label className="block text-sm font-medium leading-6 text-slate-900">
                Email address
              </label>
              <div className="mt-2">
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="block w-full rounded-lg border-0 py-2.5 text-slate-900 shadow-sm ring-1 ring-inset ring-slate-300 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6 px-3"
                  placeholder="admin@school.edu"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium leading-6 text-slate-900">
                Password
              </label>
              <div className="mt-2">
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="block w-full rounded-lg border-0 py-2.5 text-slate-900 shadow-sm ring-1 ring-inset ring-slate-300 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6 px-3"
                  placeholder="••••••••"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={isLoading}
                className="flex w-full justify-center items-center gap-2 rounded-lg bg-blue-600 px-3 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 transition-colors disabled:opacity-70 disabled:cursor-not-allowed"
              >
                {isLoading && <Loader2 className="w-4 h-4 animate-spin" />}
                Sign in
              </button>
            </div>
            
            <div className="relative mt-6">
              <div className="absolute inset-0 flex items-center" aria-hidden="true">
                <div className="w-full border-t border-slate-200"></div>
              </div>
              <div className="relative flex justify-center text-sm font-medium leading-6">
                <span className="bg-white px-6 text-slate-900">Or continue with</span>
              </div>
            </div>

            <div className="mt-6">
              <button
                type="button"
                onClick={() => alert('Google OAuth will be connected when the backend is running!')}
                className="flex w-full items-center justify-center gap-3 rounded-lg bg-white px-3 py-2.5 text-sm font-semibold text-slate-900 shadow-sm ring-1 ring-inset ring-slate-300 hover:bg-slate-50 focus-visible:ring-transparent transition-colors"
              >
                <svg className="h-5 w-5" aria-hidden="true" viewBox="0 0 24 24">
                  <path
                    d="M12.0003 4.75C13.7703 4.75 15.3553 5.36002 16.6053 6.54998L20.0303 3.125C17.9502 1.19 15.2353 0 12.0003 0C7.31028 0 3.25527 2.69 1.28027 6.60998L5.27028 9.70498C6.21525 6.86002 8.87028 4.75 12.0003 4.75Z"
                    fill="#EA4335"
                  />
                  <path
                    d="M23.49 12.275C23.49 11.49 23.415 10.73 23.3 10H12V14.51H18.47C18.18 15.99 17.34 17.25 16.08 18.1L19.945 21.1C22.2 19.01 23.49 15.92 23.49 12.275Z"
                    fill="#4285F4"
                  />
                  <path
                    d="M5.26498 14.2949C5.02498 13.5699 4.88501 12.7999 4.88501 11.9999C4.88501 11.1999 5.01998 10.4299 5.26498 9.7049L1.275 6.60986C0.46 8.22986 0 10.0599 0 11.9999C0 13.9399 0.46 15.7699 1.28 17.3899L5.26498 14.2949Z"
                    fill="#FBBC05"
                  />
                  <path
                    d="M12.0004 24.0001C15.2404 24.0001 17.9654 22.935 19.9454 21.095L16.0804 18.095C15.0054 18.82 13.6204 19.245 12.0004 19.245C8.8704 19.245 6.21537 17.135 5.26538 14.29L1.27539 17.385C3.25539 21.31 7.3104 24.0001 12.0004 24.0001Z"
                    fill="#34A853"
                  />
                </svg>
                <span className="text-sm font-semibold leading-6">Continue with Google</span>
              </button>
            </div>

            {/* QUICK DEMO LOGIN BUTTONS */}
            <div className="mt-8 pt-6 border-t border-slate-100">
              <p className="text-xs text-center text-slate-500 font-semibold uppercase tracking-wider mb-4">Quick Demo Login</p>
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => { setEmail("student@school.edu"); setPassword("demo123"); }}
                  className="px-3 py-2 text-xs font-medium bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors"
                >
                  Student Portal
                </button>
                <button
                  type="button"
                  onClick={() => { setEmail("teacher@school.edu"); setPassword("demo123"); }}
                  className="px-3 py-2 text-xs font-medium bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-colors"
                >
                  Teacher Portal
                </button>
                <button
                  type="button"
                  onClick={() => { setEmail("hr@school.edu"); setPassword("demo123"); }}
                  className="px-3 py-2 text-xs font-medium bg-amber-50 text-amber-700 rounded-lg hover:bg-amber-100 transition-colors"
                >
                  HR Portal
                </button>
                <button
                  type="button"
                  onClick={() => { setEmail("admin@school.edu"); setPassword("demo123"); }}
                  className="px-3 py-2 text-xs font-medium bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 transition-colors"
                >
                  Super Admin
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
