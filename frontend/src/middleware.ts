import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// Protected routes that require authentication
const PROTECTED_ROUTES = ['/dashboard', '/deals', '/calculator'];
const AUTH_ROUTES = ['/sign-in', '/sign-up'];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get('arbiedge_token')?.value;

  // Redirect authenticated users away from auth pages
  if (AUTH_ROUTES.some(r => pathname.startsWith(r)) && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  // Redirect unauthenticated users from protected routes
  if (PROTECTED_ROUTES.some(r => pathname.startsWith(r)) && !token) {
    const signInUrl = new URL('/sign-in', request.url);
    signInUrl.searchParams.set('redirect', pathname);
    return NextResponse.redirect(signInUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    '/dashboard/:path*',
    '/deals/:path*',
    '/calculator/:path*',
    '/sign-in',
    '/sign-up',
  ],
};
