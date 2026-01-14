// [Task]: T027 | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Next.js middleware for authentication route protection.
 * Checks JWT cookie presence and redirects unauthenticated users to /login.
 */
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Get JWT token from httpOnly cookie
  const token = request.cookies.get('access_token')

  // Protected routes that require authentication
  const protectedRoutes = ['/tasks']

  // Auth routes that authenticated users shouldn't access
  const authRoutes = ['/login', '/signup']

  // Check if current route is protected
  const isProtectedRoute = protectedRoutes.some((route) => pathname.startsWith(route))

  // Check if current route is an auth route
  const isAuthRoute = authRoutes.some((route) => pathname.startsWith(route))

  // Redirect unauthenticated users from protected routes to login
  if (isProtectedRoute && !token) {
    const url = new URL('/login', request.url)
    return NextResponse.redirect(url)
  }

  // Redirect authenticated users from auth routes to tasks page
  if (isAuthRoute && token) {
    const url = new URL('/tasks', request.url)
    return NextResponse.redirect(url)
  }

  // Allow request to proceed
  return NextResponse.next()
}

// Configure which routes this middleware applies to
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public files (public folder)
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
