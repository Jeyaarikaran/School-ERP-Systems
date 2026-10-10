import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Edge Middleware for strict route protection
export function middleware(request: NextRequest) {
  const token = request.cookies.get("erp_access_token")?.value;
  const isLoginPage = request.nextUrl.pathname === "/login";

  // If no token and not on login page, redirect to login
  if (!token && !isLoginPage) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  // If token exists and trying to access login page, redirect to dashboard
  if (token && isLoginPage) {
    return NextResponse.redirect(new URL("/", request.url));
  }

  return NextResponse.next();
}

// Only run middleware on dashboard routes and login
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    "/((?!api|_next/static|_next/image|favicon.ico).*)",
  ],
};
