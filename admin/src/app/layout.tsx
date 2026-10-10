import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/Sidebar";
import { Header } from "@/components/Header";
import { QueryProvider } from "@/components/QueryProvider";
import { AuthProvider } from "@/components/AuthProvider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "School ERP Admin",
  description: "Administrative dashboard for the multi-tenant School ERP",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={inter.className}>
      <body>
        <QueryProvider>
          <AuthProvider>
            <div className="min-h-screen bg-slate-50 flex">
              <Sidebar />
              <div className="flex-1 flex flex-col min-h-screen md:pl-64">
                <Header />
                <main className="flex-1 pb-10">
                  {children}
                </main>
              </div>
            </div>
          </AuthProvider>
        </QueryProvider>
      </body>
    </html>
  );
}
