"use client";

import { useTranslations } from "next-intl";
import { useState } from "react";

export default function AdmissionWizardPage() {
  const t = useTranslations("Admission");
  const [step, setStep] = useState(1);
  const [guardianPhone, setGuardianPhone] = useState("");
  const [showDuplicatePrompt, setShowDuplicatePrompt] = useState(false);

  // Mocking the duplicate check
  const handleNext = () => {
    if (step === 2 && guardianPhone === "1234567890" && !showDuplicatePrompt) {
      setShowDuplicatePrompt(true);
      return;
    }
    setShowDuplicatePrompt(false);
    setStep(s => s + 1);
  };

  return (
    <div className="max-w-3xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-8">{t("title")}</h1>
      
      <div className="flex justify-between mb-8 border-b pb-4">
        <span className={step >= 1 ? "text-blue-600 font-bold" : "text-gray-400"}>1. {t("steps.details")}</span>
        <span className={step >= 2 ? "text-blue-600 font-bold" : "text-gray-400"}>2. {t("steps.guardians")}</span>
        <span className={step >= 3 ? "text-blue-600 font-bold" : "text-gray-400"}>3. {t("steps.documents")}</span>
        <span className={step >= 4 ? "text-blue-600 font-bold" : "text-gray-400"}>4. {t("steps.review")}</span>
      </div>

      <div className="bg-white shadow rounded p-6 min-h-[300px]">
        {step === 1 && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold">{t("details.heading")}</h2>
            <input type="text" placeholder={t("details.firstName")} className="border p-2 w-full rounded" />
            <input type="date" className="border p-2 w-full rounded" aria-label={t("details.dob")} />
          </div>
        )}
        
        {step === 2 && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold">{t("guardians.heading")}</h2>
            <input 
              type="tel" 
              placeholder={t("guardians.phone")} 
              value={guardianPhone}
              onChange={(e) => setGuardianPhone(e.target.value)}
              className="border p-2 w-full rounded" 
            />
            {showDuplicatePrompt && (
              <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mt-4">
                <p className="text-sm text-yellow-700">{t("guardians.duplicateWarning")}</p>
                <button 
                  className="mt-2 bg-yellow-600 text-white px-3 py-1 rounded text-sm"
                  onClick={() => handleNext()}
                >
                  {t("guardians.confirmLink")}
                </button>
              </div>
            )}
          </div>
        )}

        {step === 3 && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold">{t("documents.heading")}</h2>
            <input type="file" className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" />
          </div>
        )}

        {step === 4 && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold">{t("review.heading")}</h2>
            <p className="text-gray-600 text-sm">{t("review.summary")}</p>
          </div>
        )}
      </div>

      <div className="flex justify-between mt-6">
        <button 
          onClick={() => setStep(s => Math.max(1, s - 1))}
          disabled={step === 1}
          className="px-4 py-2 border rounded text-gray-600 disabled:opacity-50"
        >
          {t("common.back")}
        </button>
        <button 
          onClick={handleNext}
          disabled={step === 4}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {step === 4 ? t("common.submit") : t("common.next")}
        </button>
      </div>
    </div>
  );
}
