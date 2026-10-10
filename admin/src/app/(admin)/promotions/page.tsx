"use client";

import { useTranslations } from "next-intl";
import { useState } from "react";

export default function PromotionsPage() {
  const t = useTranslations("Promotions");
  const [step, setStep] = useState(1);

  return (
    <div className="max-w-5xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-6">{t("title")}</h1>
      
      <div className="bg-white rounded shadow p-6">
        {step === 1 && (
          <div className="space-y-6">
            <h2 className="text-lg font-semibold">{t("step1.heading")}</h2>
            <div className="flex gap-4">
              <div className="flex-1">
                <label className="block text-sm font-medium text-gray-700 mb-1">{t("step1.fromYear")}</label>
                <select className="border p-2 w-full rounded" aria-label={t("step1.fromYear")}>
                  <option>2023-2024</option>
                </select>
              </div>
              <div className="flex-1">
                <label className="block text-sm font-medium text-gray-700 mb-1">{t("step1.toYear")}</label>
                <select className="border p-2 w-full rounded" aria-label={t("step1.toYear")}>
                  <option>2024-2025</option>
                </select>
              </div>
            </div>
            <button 
              onClick={() => setStep(2)}
              className="bg-blue-600 text-white px-4 py-2 rounded"
            >
              {t("actions.preview")}
            </button>
          </div>
        )}

        {step === 2 && (
          <div>
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold">{t("step2.heading")}</h2>
              <span className="text-sm text-yellow-600 bg-yellow-50 px-2 py-1 rounded">
                {t("step2.warnings", { count: 3 })}
              </span>
            </div>
            
            <div className="border rounded mb-6 overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-gray-50 border-b">
                  <tr>
                    <th className="p-3">{t("columns.student")}</th>
                    <th className="p-3">{t("columns.currentClass")}</th>
                    <th className="p-3">{t("columns.proposedClass")}</th>
                    <th className="p-3">{t("columns.status")}</th>
                    <th className="p-3">{t("columns.override")}</th>
                  </tr>
                </thead>
                <tbody>
                  {/* Mock data row */}
                  <tr className="border-b">
                    <td className="p-3">John Doe (ADM-001)</td>
                    <td className="p-3">Grade 5 - A</td>
                    <td className="p-3">Grade 6 - A</td>
                    <td className="p-3 text-green-600">✓ Promote</td>
                    <td className="p-3">
                      <select className="border p-1 text-xs rounded" aria-label={t("columns.override")}>
                        <option>Default (Promote)</option>
                        <option>Retain</option>
                        <option>Graduate</option>
                      </select>
                    </td>
                  </tr>
                  <tr className="border-b bg-yellow-50">
                    <td className="p-3">Jane Smith (ADM-002)</td>
                    <td className="p-3">Grade 5 - A</td>
                    <td className="p-3">-</td>
                    <td className="p-3 text-yellow-600">⚠ Missing Grades</td>
                    <td className="p-3">
                      <select className="border p-1 text-xs rounded" aria-label={t("columns.override")}>
                        <option>Default (Wait)</option>
                        <option>Force Promote</option>
                        <option>Retain</option>
                      </select>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div className="flex justify-between">
               <button onClick={() => setStep(1)} className="px-4 py-2 border rounded text-gray-600">{t("common.back")}</button>
               <button onClick={() => setStep(3)} className="px-4 py-2 bg-red-600 text-white rounded font-medium">{t("actions.execute")}</button>
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="text-center p-12">
            <div className="text-green-600 text-5xl mb-4">✓</div>
            <h3 className="text-xl font-semibold mb-2">{t("step3.successHeading")}</h3>
            <p className="text-gray-600 mb-6">{t("step3.successSub")}</p>
          </div>
        )}
      </div>
    </div>
  );
}
