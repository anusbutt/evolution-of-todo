// [Task]: T048 [US1] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Signup page with SignupForm and link to login.
 */
import Link from 'next/link'
import { SignupForm } from '@/components/forms/SignupForm'
import { Card } from '@/components/ui/card'

export default function SignupPage() {
  return (
    <Card className="p-8">
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Create your account
          </h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
            Start managing your tasks today
          </p>
        </div>

        <SignupForm />

        <div className="text-center text-sm">
          <span className="text-gray-600 dark:text-gray-400">
            Already have an account?{' '}
          </span>
          <Link
            href="/login"
            className="text-blue-600 hover:text-blue-800 font-medium transition-colors"
          >
            Log in
          </Link>
        </div>
      </div>
    </Card>
  )
}
