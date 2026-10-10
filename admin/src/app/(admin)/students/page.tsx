"use client";

import { useTranslations } from "next-intl";
import Link from "next/link";
import { useState } from "react";

export default function StudentsListPage() {
  const t = useTranslations("Students");
  const [searchTerm, setSearchTerm] = useState("");

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">{t("title")}</h1>
        <Link 
          href="/students/admission"
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded font-medium"
        >
          {t("admitBtn")}
        </Link>
      </div>
      
      <div className="bg-white rounded shadow p-4">
        <div className="flex gap-4 mb-4">
          <input 
            type="text" 
            placeholder={t("searchPlaceholder")}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="border p-2 rounded flex-1"
            aria-label={t("searchPlaceholder")}
          />
          <select className="border p-2 rounded" aria-label={t("classFilter")}>
            <option value="">{t("allClasses")}</option>
          </select>
        </div>
        
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b bg-gray-50">
              <th className="p-3 font-semibold text-gray-600">{t("columns.admissionNo")}</th>
              <th className="p-3 font-semibold text-gray-600">{t("columns.name")}</th>
              <th className="p-3 font-semibold text-gray-600">{t("columns.class")}</th>
              <th className="p-3 font-semibold text-gray-600">{t("columns.status")}</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td colSpan={4} className="p-8 text-center text-gray-500">
                {t("emptyState")}
              </td>
            </tr>
          </tbody>
        </table>
        
        <div className="mt-4 flex justify-between text-sm text-gray-500">
          <span>{t("pagination.showing", { count: 0, total: 0 })}</span>
          <div className="space-x-2">
            <button disabled className="px-2 py-1 border rounded opacity-50">{t("pagination.prev")}</button>
            <button disabled className="px-2 py-1 border rounded opacity-50">{t("pagination.next")}</button>
          </div>
        </div>
      </div>
    </div>
  );
}
