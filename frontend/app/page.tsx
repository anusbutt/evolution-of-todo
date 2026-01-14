// [Task]: T052 [US1] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Landing page with welcome message and Sign Up / Log In CTAs.
 */
import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 px-4">
      <div className="max-w-4xl mx-auto text-center space-y-8">
        <div className="space-y-4">
          <h1 className="text-6xl font-bold text-gray-900 dark:text-white">
            Welcome to Todo App
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            The simple, powerful way to organize your tasks and boost your productivity.
            Start managing your tasks today.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link href="/signup">
            <Button variant="primary" className="min-w-[200px]">
              Sign Up
            </Button>
          </Link>
          <Link href="/login">
            <Button variant="secondary" className="min-w-[200px]">
              Log In
            </Button>
          </Link>
        </div>

        <div className="pt-8 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-3xl mx-auto">
          <div className="space-y-2">
            <div className="text-4xl">✓</div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Simple & Intuitive
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Clean interface that lets you focus on what matters
            </p>
          </div>
          <div className="space-y-2">
            <div className="text-4xl">🚀</div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Fast & Reliable
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Lightning-fast performance with secure authentication
            </p>
          </div>
          <div className="space-y-2">
            <div className="text-4xl">🎨</div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Beautiful Design
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Modern UI with dark mode support
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
