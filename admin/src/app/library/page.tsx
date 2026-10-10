import { Library as LibraryIcon, BookMarked, BookUp, UsersRound } from "lucide-react";
import { ModuleCard } from "@/components/ui/ModuleCard";

export default function LibraryDashboard() {
  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Library (Phase 9)</h1>
        <p className="text-slate-500">Manage catalogues, circulation, and library memberships.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <ModuleCard 
          title="Catalogue" 
          description="Manage books, copies, and barcodes" 
          icon={BookMarked} 
          colorScheme="amber" 
        />
        <ModuleCard 
          title="Circulation" 
          description="Issue, return, and collect late fines" 
          icon={BookUp} 
          colorScheme="amber" 
        />
        <ModuleCard 
          title="Memberships" 
          description="Manage library card allocations" 
          icon={UsersRound} 
          colorScheme="amber" 
        />
      </div>
    </div>
  );
}
