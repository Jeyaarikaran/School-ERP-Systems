import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    
    // Proxy to backend
    const res = await fetch(`${BACKEND_URL}/api/v1/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Request-ID': crypto.randomUUID(),
      },
      body: JSON.stringify(body),
    });

    const data = await res.json();

    if (res.ok && data.success && data.data.access_token) {
      // Set HttpOnly cookies
      cookies().set('access_token', data.data.access_token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
        maxAge: 15 * 60, // 15 mins
        path: '/',
      });
      
      cookies().set('refresh_token', data.data.refresh_token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
        maxAge: 30 * 24 * 60 * 60, // 30 days
        path: '/',
      });

      // Do not leak tokens to frontend
      return NextResponse.json({ success: true, message: data.message });
    }

    // Pass through error
    return NextResponse.json(data, { status: res.status });
  } catch (error) {
    return NextResponse.json(
      { success: false, error: { code: 'INTERNAL_ERROR', message: 'BFF Error' } },
      { status: 500 }
    );
  }
}
