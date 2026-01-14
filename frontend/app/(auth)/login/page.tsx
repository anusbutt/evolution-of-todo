// [Task]: T049 [US1] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Login page with LoginForm and link to signup.
 */
import Link from 'next/link'
import { LoginForm } from '@/components/forms/LoginForm'
import { Card } from '@/components/ui/card'

export default function LoginPage() {
  return (
    <Card className="p-8">
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Welcome back
          </h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
            Log in to your account to continue
          </p>
        </div>

        <LoginForm />

        <div className="text-center text-sm">
          <span className="text-gray-600 dark:text-gray-400">
            Don't have an account?{' '}
          </span>
          <Link
            href="/signup"
            className="text-blue-600 hover:text-blue-800 font-medium transition-colors"
          >
            Sign up
          </Link>
        </div>
      </div>
    </Card>
  )
}
