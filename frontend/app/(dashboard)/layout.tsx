// [Task]: T065 [P] [US2] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Dashboard layout wrapper for authenticated pages.
 * Includes header with logout button and responsive padding.
 */
import { ReactNode } from 'react'
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'
import { Header } from '@/components/layout/Header'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

async function getCurrentUser() {
  const cookieStore = await cookies()
  const token = cookieStore.get('access_token')

  if (!token) {
    redirect('/login')
  }

  const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
    headers: {
      Cookie: `access_token=${token.value}`,
    },
    cache: 'no-store',
  }).catch(() => null)

  if (!response || !response.ok) {
    redirect('/login')
  }

  return await response.json()
}

export default async function DashboardLayout({ children }: { children: ReactNode }) {
  const user = await getCurrentUser()

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header userName={user.name} />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  )
}
