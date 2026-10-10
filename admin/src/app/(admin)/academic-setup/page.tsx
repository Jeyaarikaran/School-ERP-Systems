"use client";

import { useTranslations } from "next-intl";

export default function AcademicSetupPage() {
  const t = useTranslations("AcademicSetup");

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">{t("title")}</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <section className="bg-white p-6 rounded shadow">
          <h2 className="text-lg font-semibold mb-4">{t("years.title")}</h2>
          <div className="text-sm text-gray-500 mb-4">{t("years.description")}</div>
          <button className="bg-blue-600 text-white px-4 py-2 rounded">
            {t("years.createBtn")}
          </button>
          {/* Skeleton for table */}
          <div className="mt-4 border rounded p-4 text-center text-gray-400">
            {t("common.noData")}
          </div>
        </section>

        <section className="bg-white p-6 rounded shadow">
          <h2 className="text-lg font-semibold mb-4">{t("classes.title")}</h2>
          <div className="text-sm text-gray-500 mb-4">{t("classes.description")}</div>
          <button className="bg-blue-600 text-white px-4 py-2 rounded">
            {t("classes.cloneBtn")}
          </button>
          <div className="mt-4 border rounded p-4 text-center text-gray-400">
            {t("common.noData")}
          </div>
        </section>
      </div>
    </div>
  );
}
