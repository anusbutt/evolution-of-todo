// [Task]: T031 [P] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Reusable Button component with multiple variants.
 * Supports primary, secondary, and danger styles.
 */
import { ButtonHTMLAttributes } from 'react'
import { clsx } from 'clsx'

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger'
  fullWidth?: boolean
}

export function Button({
  variant = 'primary',
  fullWidth = false,
  className,
  children,
  ...props
}: ButtonProps) {
  const baseStyles =
    'px-4 py-2 text-base rounded-md font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed'

  const variantStyles = {
    primary:
      'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500 dark:bg-blue-500 dark:hover:bg-blue-600',
    secondary:
      'bg-gray-500 text-white hover:bg-gray-600 focus:ring-gray-400 dark:bg-gray-600 dark:hover:bg-gray-500',
    danger:
      'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500 dark:bg-red-500 dark:hover:bg-red-600',
  }

  const widthStyles = fullWidth ? 'w-full' : ''

  return (
    <button
      className={clsx(baseStyles, variantStyles[variant], widthStyles, className)}
      {...props}
    >
      {children}
    </button>
  )
}
