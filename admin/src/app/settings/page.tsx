import { Shield, KeyRound, Building2, History, Key } from "lucide-react";
import { ModuleCard } from "@/components/ui/ModuleCard";

export default function SettingsDashboard() {
  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Settings & Security (Phase 1 & 2)</h1>
        <p className="text-slate-500">System architecture, RBAC controls, and tenant isolation.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <ModuleCard 
          title="Tenant Config" 
          description="Row-Level Security overriding and DB isolation" 
          icon={Building2} 
          colorScheme="slate" 
        />
        <ModuleCard 
          title="RBAC Matrices" 
          description="60 distinct permissions enforcing granular access" 
          icon={Shield} 
          colorScheme="slate" 
        />
        <ModuleCard 
          title="System Audit Logs" 
          description="Transactional, append-only logs with automated PII Redaction" 
          icon={History} 
          colorScheme="slate" 
        />
        <ModuleCard 
          title="Session Controls" 
          description="JWT rotation, Argon2 hashing, and Redis revocation (Phase 2)" 
          icon={Key} 
          colorScheme="slate" 
        />
        <ModuleCard 
          title="API Keys" 
          description="Webhooks, Integrations, and Security Logs" 
          icon={KeyRound} 
          colorScheme="slate" 
        />
      </div>
    </div>
  );
}
