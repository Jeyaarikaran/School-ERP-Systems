import Link from "next/link";
import { AlertCircle, ArrowLeft } from "lucide-react";

export default function NotFound() {
  return (
    <div className="flex h-[80vh] w-full flex-col items-center justify-center text-center px-4">
      <div className="bg-rose-50 p-4 rounded-full mb-6">
        <AlertCircle className="h-10 w-10 text-rose-500" />
      </div>
      <h2 className="text-3xl font-bold text-slate-900 mb-2">404 - Page Not Found</h2>
      <p className="text-slate-500 max-w-md mb-8">
        The module or dashboard you are looking for does not exist or has been moved in the latest release.
      </p>
      <Link 
        href="/"
        className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 transition-colors shadow-sm"
      >
        <ArrowLeft className="w-4 h-4" />
        Return to Dashboard
      </Link>
    </div>
  );
}
