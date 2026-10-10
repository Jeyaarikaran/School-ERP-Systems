/**
 * Base API Client for Next.js to communicate with the FastAPI Backend.
 * Automatically handles auth tokens and standardized error responses.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export class APIError extends Error {
  constructor(public status: number, public data: any) {
    super(`API Error: ${status} - ${data?.detail || "Unknown error"}`);
  }
}

function getAuthToken() {
  if (typeof window !== "undefined") {
    return localStorage.getItem("access_token");
  }
  return null;
}

export const api = {
  async get<T>(endpoint: string, customToken?: string): Promise<T> {
    const token = customToken || getAuthToken();
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const res = await fetch(`${API_BASE}${endpoint}`, { headers });
    if (!res.ok) {
      if (res.status === 401 && typeof window !== "undefined") {
        localStorage.removeItem("access_token");
        window.location.href = "/login";
      }
      throw new APIError(res.status, await res.json().catch(() => ({})));
    }
    return res.json();
  },

  async post<T>(endpoint: string, body: any, customToken?: string): Promise<T> {
    const token = customToken || getAuthToken();
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const res = await fetch(`${API_BASE}${endpoint}`, {
      method: "POST",
      headers,
      body: JSON.stringify(body),
    });
    
    if (!res.ok) {
      if (res.status === 401 && typeof window !== "undefined") {
        localStorage.removeItem("access_token");
        window.location.href = "/login";
      }
      throw new APIError(res.status, await res.json().catch(() => ({})));
    }
    return res.json();
  },

  async login(identifier: string, password: string, school_code?: string) {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ identifier, password, school_code }),
    });

    if (!res.ok) {
      throw new APIError(res.status, await res.json().catch(() => ({})));
    }
    const data = await res.json();
    if (typeof window !== "undefined") {
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      localStorage.setItem("user", JSON.stringify(data.user));
    }
    return data;
  },

  async logout() {
    try {
      await this.post("/auth/logout", {});
    } catch (e) {
      console.warn("Logout failed on backend", e);
    } finally {
      if (typeof window !== "undefined") {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");
        window.location.href = "/login";
      }
    }
  }
};
