"use client";

import { useTranslations } from "next-intl";
import { useBulkImport } from "@/hooks/useBulkImport";

export default function BulkImportPage() {
  const t = useTranslations("BulkImport");
  const { state, uploadFile, commitJob, errors, downloadErrorReport, cancelRequest } = useBulkImport();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      uploadFile(e.target.files[0]);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-6">{t("title")}</h1>

      <div className="bg-white rounded shadow p-6">
        {state === "idle" && (
          <div className="border-2 border-dashed border-gray-300 rounded p-12 text-center">
            <h3 className="text-lg font-medium text-gray-700 mb-2">{t("upload.heading")}</h3>
            <p className="text-sm text-gray-500 mb-4">{t("upload.hint")}</p>
            <input type="file" onChange={handleFileChange} className="mx-auto block text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" accept=".csv,.xlsx" />
          </div>
        )}

        {(state === "uploading" || state === "validating") && (
          <div className="text-center p-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">{state === "uploading" ? t("status.uploading") : t("status.validating")}</p>
            <button onClick={cancelRequest} className="mt-4 text-red-600 hover:underline text-sm">{t("common.cancel")}</button>
          </div>
        )}

        {state === "validated" && (
          <div className="p-6 text-center">
            <div className="text-green-600 text-5xl mb-4">✓</div>
            <h3 className="text-xl font-semibold mb-2">{t("status.validatedHeading")}</h3>
            <p className="text-gray-600 mb-6">{t("status.validatedSub")}</p>
            <div className="flex justify-center gap-4">
              <button onClick={() => window.location.reload()} className="px-4 py-2 border rounded text-gray-600">{t("common.cancel")}</button>
              <button onClick={() => commitJob(false)} className="px-4 py-2 bg-blue-600 text-white rounded">{t("actions.commitAll")}</button>
            </div>
          </div>
        )}

        {state === "failed" && errors.length > 0 && (
          <div className="p-6">
            <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
              <h3 className="text-red-700 font-bold">{t("status.failedHeading")}</h3>
              <p className="text-sm text-red-600">{t("status.failedSub", { count: errors.length })}</p>
            </div>
            
            <button onClick={downloadErrorReport} className="mb-4 text-blue-600 hover:underline text-sm font-medium">
              {t("actions.downloadErrors")}
            </button>

            <div className="max-h-64 overflow-y-auto border rounded">
              <table className="w-full text-sm text-left">
                <thead className="bg-gray-50 sticky top-0">
                  <tr>
                    <th className="p-2 border-b">Row</th>
                    <th className="p-2 border-b">Column</th>
                    <th className="p-2 border-b">Error</th>
                  </tr>
                </thead>
                <tbody>
                  {errors.slice(0, 100).map((err, i) => (
                    <tr key={i} className="border-b">
                      <td className="p-2">{err.row}</td>
                      <td className="p-2">{err.column}</td>
                      <td className="p-2 text-red-600">{err.message}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="mt-6 flex justify-end gap-4">
               <button onClick={() => window.location.reload()} className="px-4 py-2 border rounded text-gray-600">{t("common.retry")}</button>
               <button onClick={() => commitJob(true)} className="px-4 py-2 bg-yellow-500 text-white rounded">{t("actions.commitValidOnly")}</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
