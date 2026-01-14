// [Task]: T050 [US1] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Signup form component with validation using React Hook Form and Zod.
 * Validates email format, name length, and password strength.
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

// Zod schema matching backend validation
const signupSchema = z.object({
  email: z.string().email('Invalid email address'),
  name: z.string().min(1, 'Name is required').max(255, 'Name must be less than 255 characters'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[a-zA-Z]/, 'Password must contain at least one letter')
    .regex(/[0-9]/, 'Password must contain at least one number'),
})

type SignupFormData = z.infer<typeof signupSchema>

export function SignupForm() {
  const router = useRouter()
  const [apiError, setApiError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema),
  })

  const onSubmit = async (data: SignupFormData) => {
    setIsSubmitting(true)
    setApiError(null)

    try {
      // POST /api/auth/signup
      await apiRequest('/api/auth/signup', {
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
        label="Name"
        type="text"
        placeholder="Your name"
        error={errors.name?.message}
        {...register('name')}
        fullWidth
      />

      <Input
        label="Password"
        type="password"
        placeholder="At least 8 characters with letter and number"
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
        {isSubmitting ? 'Creating account...' : 'Sign Up'}
      </Button>
    </form>
  )
}
