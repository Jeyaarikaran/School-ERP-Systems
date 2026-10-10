// Type definitions based on Phase 2 Database Architecture

export type RoleType = 
  | "super_admin" 
  | "school_admin" 
  | "teacher" 
  | "student" 
  | "parent" 
  | "librarian" 
  | "transport_admin";

export type EntityStatus = "active" | "suspended" | "archived";

export interface Tenant {
  id: string;
  code: string;
  name: string;
  status: EntityStatus;
  timezone: string;
}

export interface User {
  id: string;
  school_id: string | null;
  email: string;
  full_name: string;
  role: RoleType;
  status: "invited" | "active" | "suspended" | "deactivated";
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

// Module specific types
export interface Student {
  id: string;
  admission_no: string;
  full_name: string;
  status: string;
}
