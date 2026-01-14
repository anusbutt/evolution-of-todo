// [Task]: T053, T094, T112 [US1, US5, US7] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Header component with user info and logout button.
 * Displays current user's name and provides logout functionality.
 * Responsive design: compact on mobile, full on desktop.
 */
'use client'

import { useRouter } from 'next/navigation'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { ThemeToggle } from '@/components/layout/theme-toggle'
import { apiRequest, ApiError } from '@/lib/api-client'

interface HeaderProps {
  userName: string
}

export function Header({ userName }: HeaderProps) {
  const router = useRouter()
  const [isLoggingOut, setIsLoggingOut] = useState(false)

  const handleLogout = async () => {
    setIsLoggingOut(true)

    try {
      // POST /api/auth/logout
      await apiRequest('/api/auth/logout', {
        method: 'POST',
      })

      // Redirect to home page after logout
      router.push('/')
    } catch (error) {
      if (error instanceof ApiError) {
        console.error('Logout failed:', error.message)
      } else {
        console.error('Unexpected error during logout')
      }
    } finally {
      setIsLoggingOut(false)
    }
  }

  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2 sm:gap-4">
            <h1 className="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white">
              Todo App
            </h1>
          </div>

          <div className="flex items-center gap-2 sm:gap-4">
            <span className="hidden sm:inline text-sm text-gray-600 dark:text-gray-300">
              Welcome, <span className="font-medium">{userName}</span>
            </span>
            <ThemeToggle />
            <Button
              variant="secondary"
              onClick={handleLogout}
              disabled={isLoggingOut}
              className="text-sm px-3 py-2"
            >
              {isLoggingOut ? 'Logging out...' : 'Log Out'}
            </Button>
          </div>
        </div>
      </div>
    </header>
  )
}
