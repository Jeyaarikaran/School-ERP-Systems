"use client";

import { useEffect } from "react";
import { AlertTriangle, RefreshCcw } from "lucide-react";

export default function ErrorBoundary({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // In a real app, log this to Sentry/Datadog
    console.error("UI Crash Caught by Boundary:", error);
  }, [error]);

  return (
    <div className="flex h-[80vh] w-full flex-col items-center justify-center text-center px-4">
      <div className="bg-rose-50 p-4 rounded-full mb-6">
        <AlertTriangle className="h-10 w-10 text-rose-600" />
      </div>
      <h2 className="text-3xl font-bold text-slate-900 mb-2">Something went wrong!</h2>
      <p className="text-slate-500 max-w-md mb-8">
        The application encountered an unexpected error. Our engineers have been notified.
      </p>
      <button
        onClick={() => reset()}
        className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-slate-900 text-white font-medium hover:bg-slate-800 transition-colors shadow-sm"
      >
        <RefreshCcw className="w-4 h-4" />
        Try again
      </button>
    </div>
  );
}
