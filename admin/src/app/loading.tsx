"use client";

import { Loader2 } from "lucide-react";

export default function Loading() {
  return (
    <div className="flex h-[80vh] w-full flex-col items-center justify-center space-y-4">
      <div className="bg-blue-50 p-4 rounded-full">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
      <p className="text-sm font-medium text-slate-500 animate-pulse">
        Loading dashboard modules...
      </p>
    </div>
  );
}
