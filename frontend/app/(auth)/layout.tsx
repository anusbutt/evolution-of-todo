// [Task]: T047, T093 [US1, US5] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Auth layout wrapper for signup and login pages.
 * Centers auth forms with responsive padding and consistent styling.
 */
import { ReactNode } from 'react'

export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4 sm:px-6 md:px-8 py-12">
      <div className="max-w-md w-full mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            Todo App
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage your tasks efficiently
          </p>
        </div>
        {children}
      </div>
    </div>
  )
}
