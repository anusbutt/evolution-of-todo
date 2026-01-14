// [Task]: T035 [P] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Reusable Checkbox component with accessibility labels.
 * Controlled component for task completion status.
 */
import { InputHTMLAttributes, forwardRef } from 'react'
import { clsx } from 'clsx'

export interface CheckboxProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string
}

export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  ({ label, className, id, ...props }, ref) => {
    const checkboxStyles = clsx(
      'h-6 w-6 sm:h-5 sm:w-5 rounded border-gray-300 dark:border-gray-600',
      'text-blue-600 focus:ring-blue-500 focus:ring-2 focus:ring-offset-2 accent-blue-600',
      'cursor-pointer transition-colors duration-200',
      'dark:bg-gray-800',
      className
    )

    const inputId = id || `checkbox-${Math.random().toString(36).substr(2, 9)}`

    return (
      <div className="flex items-center gap-2">
        <input
          ref={ref}
          type="checkbox"
          id={inputId}
          className={checkboxStyles}
          {...props}
        />
        {label && (
          <label
            htmlFor={inputId}
            className="text-sm font-medium text-gray-700 dark:text-gray-300 cursor-pointer select-none"
          >
            {label}
          </label>
        )}
      </div>
    )
  }
)

Checkbox.displayName = 'Checkbox'
