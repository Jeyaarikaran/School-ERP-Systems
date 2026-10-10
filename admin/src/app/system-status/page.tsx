"use client";

import { useEffect, useState } from "react";
import { apiClient } from "@/lib/api-client";
import { useTranslations } from "next-intl";

export default function SystemStatusPage() {
  const t = useTranslations("SystemStatus");
  const [status, setStatus] = useState<"loading" | "ready" | "error" | "degraded">("loading");
  const [errorDetails, setErrorDetails] = useState<any>(null);

  useEffect(() => {
    async function checkStatus() {
      try {
        const { data, response, error } = await apiClient.GET("/ready", {} as any);
        if (response.status === 200 && data) {
          setStatus("ready");
        } else if (response.status === 503) {
          setStatus("degraded");
          setErrorDetails(error);
        } else {
          setStatus("error");
        }
      } catch (err) {
        setStatus("error");
      }
    }
    checkStatus();
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">{t("title")}</h1>
      
      {status === "loading" && <div className="animate-pulse">{t("loading")}</div>}
      
      {status === "ready" && (
        <div className="text-green-600 font-semibold">{t("ready")}</div>
      )}

      {status === "degraded" && (
        <div className="text-yellow-600">
          <div className="font-semibold">{t("degraded")}</div>
          <pre className="mt-2 p-2 bg-yellow-50 rounded text-sm">{JSON.stringify(errorDetails, null, 2)}</pre>
        </div>
      )}

      {status === "error" && (
        <div className="text-red-600 font-semibold">{t("error")}</div>
      )}
    </div>
  );
}
