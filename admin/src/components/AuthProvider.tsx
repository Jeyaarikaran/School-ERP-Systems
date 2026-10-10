"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";

interface User {
  id: string;
  email: string;
  role: string;
  school_id: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (token: string, user: User) => void;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    // Check local storage for token on mount
    const storedToken = localStorage.getItem("erp_token");
    const storedUser = localStorage.getItem("erp_user");
    
    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    // Auth Guard
    if (!loading && !token && pathname !== "/login") {
      router.push("/login");
    }
  }, [loading, token, pathname, router]);

  const login = (newToken: string, newUser: User) => {
    localStorage.setItem("erp_token", newToken);
    localStorage.setItem("erp_user", JSON.stringify(newUser));
    
    // 🔥 FIX: Set the cookie so Next.js middleware doesn't block the redirect!
    document.cookie = `erp_access_token=${newToken}; path=/`;

    setToken(newToken);
    setUser(newUser);
    router.push("/");
  };

  const logout = () => {
    localStorage.removeItem("erp_token");
    localStorage.removeItem("erp_user");
    document.cookie = "erp_access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;";
    setToken(null);
    setUser(null);
    router.push("/login");
  };

  if (loading) return null;

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
