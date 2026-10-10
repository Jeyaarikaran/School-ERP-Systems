import createClient from "openapi-fetch";

// We import the generated types (assuming user runs `npm run generate:api`)
// import type { paths } from "./api-schema";

// Since we cannot run openapi-typescript right now, we define a fallback interface.
export interface SuccessEnvelope<T = any> {
  success: boolean;
  data: T;
  message: string;
  meta: {
    request_id: string;
    pagination?: { page: number; limit: number; total: number; total_pages: number };
    next_cursor?: string;
  };
}

export interface ErrorEnvelope {
  success: boolean;
  error: {
    code: string;
    message: string;
    details: any[];
  };
  meta: {
    request_id: string;
  };
}

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export const apiClient = createClient<any>({
  baseUrl: BACKEND_URL,
  headers: {
    "X-Request-ID": crypto.randomUUID(),
  }
});
