import { GraduationCap, BookOpen, Clock, Users, FileText, DownloadCloud, Contact, UserSquare2, Fingerprint, CalendarOff } from "lucide-react";
import { ModuleCard } from "@/components/ui/ModuleCard";

export default function AcademicsDashboard() {
  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">People & Academics</h1>
        <p className="text-slate-500">Phases 2, 3, 5, 6, and 8 — Core Identity, Exams, and Staff management.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {/* People Models */}
        <ModuleCard 
          title="Student Directory" 
          description="Enrollments, status history, and PII-redacted views (Phase 3)" 
          icon={Users} 
          colorScheme="blue" 
          href="/students"
        />
        <ModuleCard 
          title="Guardians Hub" 
          description="Linked accounts and On-Behalf Homework submissions (Phase 5)" 
          icon={Contact} 
          colorScheme="blue" 
        />
        <ModuleCard 
          title="Staff & Teachers" 
          description="Section scopes and timetable slot claims (Phase 3)" 
          icon={UserSquare2} 
          colorScheme="blue" 
        />

        {/* Academics & Exams */}
        <ModuleCard 
          title="Curriculum" 
          description="Units, dynamic delay calculations, and progress (Phase 5)" 
          icon={BookOpen} 
          colorScheme="indigo" 
        />
        <ModuleCard 
          title="Timetable & Invigilation" 
          description="Conflict-free scheduling via GIST constraints (Phases 5 & 6)" 
          icon={Clock} 
          colorScheme="indigo" 
        />
        <ModuleCard 
          title="Exams & Report Cards" 
          description="Decimal math, public verification hashes, and Marks History (Phase 6)" 
          icon={FileText} 
          colorScheme="indigo" 
        />

        {/* Operations */}
        <ModuleCard 
          title="Leave & Substitutions" 
          description="Staff leave approvals and timetable overlay suggestions (Phase 8)" 
          icon={CalendarOff} 
          colorScheme="slate" 
        />
        <ModuleCard 
          title="Storage & Imports" 
          description="S3 presigned URLs, Malware Scanners, and Job logs (Phase 3)" 
          icon={DownloadCloud} 
          colorScheme="slate" 
        />

      </div>
    </div>
  );
}
