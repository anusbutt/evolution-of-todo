// [Task]: T051 [US1] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Login form component with validation using React Hook Form and Zod.
 * Authenticates user with email and password.
 */
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { apiRequest, ApiError } from '@/lib/api-client'

// Zod schema for login validation
const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(1, 'Password is required'),
})

type LoginFormData = z.infer<typeof loginSchema>

export function LoginForm() {
  const router = useRouter()
  const [apiError, setApiError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  })

  const onSubmit = async (data: LoginFormData) => {
    setIsSubmitting(true)
    setApiError(null)

    try {
      // POST /api/auth/login
      await apiRequest('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify(data),
      })

      // Redirect to tasks page on success
      router.push('/tasks')
    } catch (error) {
      if (error instanceof ApiError) {
        setApiError(error.message)
      } else {
        setApiError('An unexpected error occurred. Please try again.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <Input
        label="Email"
        type="email"
        placeholder="you@example.com"
        error={errors.email?.message}
        {...register('email')}
        fullWidth
      />

      <Input
        label="Password"
        type="password"
        placeholder="Your password"
        error={errors.password?.message}
        {...register('password')}
        fullWidth
      />

      {apiError && (
        <div className="p-4 bg-red-100 border border-red-500 rounded-md">
          <p className="text-sm text-red-600 dark:text-red-400">{apiError}</p>
        </div>
      )}

      <Button type="submit" variant="primary" fullWidth disabled={isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Log In'}
      </Button>
    </form>
  )
}
