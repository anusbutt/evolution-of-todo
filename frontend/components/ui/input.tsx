// [Task]: T032 [P] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Reusable Input component with error state support.
 * Supports text, email, and password input types.
 */
import { InputHTMLAttributes, forwardRef } from 'react'
import { clsx } from 'clsx'

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  fullWidth?: boolean
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, fullWidth = false, className, ...props }, ref) => {
    const baseStyles =
      'px-4 py-2 text-base border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200'

    const errorStyles = error
      ? 'border-red-500 focus:ring-red-500'
      : 'border-gray-300 dark:border-gray-600'

    const widthStyles = fullWidth ? 'w-full' : ''

    const inputStyles = clsx(
      baseStyles,
      errorStyles,
      widthStyles,
      'bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100',
      className
    )

    return (
      <div className={clsx('flex flex-col gap-1', fullWidth && 'w-full')}>
        {label && (
          <label
            htmlFor={props.id}
            className="text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            {label}
          </label>
        )}
        <input ref={ref} className={inputStyles} {...props} />
        {error && <span className="text-sm text-red-500">{error}</span>}
      </div>
    )
  }
)

Input.displayName = 'Input'
