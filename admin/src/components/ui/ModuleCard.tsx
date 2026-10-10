import { ElementType } from "react";
import Link from "next/link";

interface ModuleCardProps {
  title: string;
  description: string;
  icon: ElementType;
  colorScheme?: "blue" | "indigo" | "emerald" | "rose" | "amber" | "slate" | "green";
  onClick?: () => void;
  href?: string;
}

const colorMap = {
  blue: "bg-blue-50 text-blue-600",
  indigo: "bg-indigo-50 text-indigo-600",
  emerald: "bg-emerald-50 text-emerald-600",
  rose: "bg-rose-50 text-rose-600",
  amber: "bg-amber-50 text-amber-600",
  slate: "bg-slate-100 text-slate-700",
  green: "bg-green-50 text-green-600",
};

export function ModuleCard({ 
  title, 
  description, 
  icon: Icon, 
  colorScheme = "blue",
  onClick,
  href
}: ModuleCardProps) {
  const content = (
    <div 
      onClick={onClick}
      className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex items-start gap-4 hover:shadow-md transition-shadow cursor-pointer group h-full"
    >
      <div className={`p-3 rounded-lg transition-colors ${colorMap[colorScheme]}`}>
        <Icon className="w-6 h-6" />
      </div>
      <div>
        <h3 className="font-semibold text-slate-900 group-hover:text-blue-600 transition-colors">{title}</h3>
        <p className="text-sm text-slate-500 mt-1 leading-relaxed">{description}</p>
      </div>
    </div>
  );

  if (href) {
    return <Link href={href} className="block h-full">{content}</Link>;
  }

  return content;
}
