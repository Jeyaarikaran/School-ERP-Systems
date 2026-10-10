import { useState, useRef, useEffect, useCallback } from "react";
import { apiClient } from "@/lib/api-client";

export type ImportState = "idle" | "uploading" | "validating" | "validated" | "failed" | "cancelled" | "expired" | "committing" | "completed";

export function useBulkImport() {
  const [state, setState] = useState<ImportState>("idle");
  const [jobId, setJobId] = useState<string | null>(null);
  const [errors, setErrors] = useState<any[]>([]);
  
  const pollingRef = useRef<NodeJS.Timeout | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);
  const backoffDelay = useRef(2000); // starts at 2s

  const clearPolling = useCallback(() => {
    if (pollingRef.current) {
      clearTimeout(pollingRef.current);
      pollingRef.current = null;
    }
  }, []);

  const cancelRequest = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
  }, []);

  useEffect(() => {
    // Stop polling on unmount
    return () => {
      clearPolling();
      cancelRequest();
    };
  }, [clearPolling, cancelRequest]);

  const uploadFile = async (file: File) => {
    setState("uploading");
    setErrors([]);
    backoffDelay.current = 2000;
    
    abortControllerRef.current = new AbortController();
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/api/v1/imports", {
        method: "POST",
        body: formData,
        headers: { "Idempotency-Key": crypto.randomUUID() },
        signal: abortControllerRef.current.signal
      });
      
      const data = await res.json();
      if (res.ok && data.success) {
        setJobId(data.data.job_id);
        setState("validating");
        pollJobStatus(data.data.job_id);
      } else {
        setState("failed");
      }
    } catch (e: any) {
      if (e.name === 'AbortError') {
        setState("cancelled");
      } else {
        setState("failed");
      }
    }
  };

  const pollJobStatus = async (id: string) => {
    try {
      const { data, response, error } = await apiClient.GET("/imports/{id}", {
        params: { path: { id } }
      });

      if (response.status === 200 && data) {
        // @ts-ignore - The backend wraps responses in a { data: ... } envelope
        const status = data.data?.status;
        if (status === "validated") {
          setState("validated");
          return; // done polling
        } else if (status === "failed") {
          setState("failed");
          await fetchErrors(id);
          return;
        } else if (status === "completed") {
          setState("completed");
          return;
        } else if (status === "expired") {
          setState("expired");
          return;
        }
      } else if (response.status === 404) {
        setState("expired");
        return;
      }
      
      // continue polling with backoff (max 10s)
      backoffDelay.current = Math.min(backoffDelay.current * 1.5, 10000);
      pollingRef.current = setTimeout(() => pollJobStatus(id), backoffDelay.current);
    } catch (e) {
      setState("failed");
    }
  };

  const fetchErrors = async (id: string) => {
    try {
      const { data, response } = await apiClient.GET("/imports/{id}/errors", { params: { path: { id } }});
      if (response.status === 200 && data) {
        // @ts-ignore
        setErrors(data.data?.errors || []);
      }
    } catch (e) {
      // Ignored
    }
  };

  const commitJob = async (validOnly: boolean = false) => {
    if (!jobId) return;
    setState("committing");
    try {
      await apiClient.POST("/imports/{id}/commit", {
        params: { path: { id: jobId } },
        body: { valid_rows_only: validOnly }
      });
      backoffDelay.current = 2000; // Reset backoff
      pollJobStatus(jobId);
    } catch (e) {
      setState("failed");
    }
  };

  const downloadErrorReport = () => {
    if (errors.length === 0) return;
    const csvContent = "data:text/csv;charset=utf-8," 
      + "Row,Column,Message\n" 
      + errors.map(e => `${e.row},${e.column},"${e.message}"`).join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `import_errors_${jobId}.csv`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  return { state, uploadFile, commitJob, errors, downloadErrorReport, cancelRequest };
}
