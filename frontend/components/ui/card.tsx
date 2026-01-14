// [Task]: T034 [P] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Reusable Card component for containing task items and content.
 */
import { HTMLAttributes } from 'react'
import { clsx } from 'clsx'

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  hover?: boolean
}

export function Card({ hover = false, className, children, ...props }: CardProps) {
  const baseStyles = 'bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 border border-gray-200 dark:border-gray-700'

  const hoverStyles = hover
    ? 'transition-shadow duration-200 hover:shadow-lg'
    : ''

  return (
    <div className={clsx(baseStyles, hoverStyles, className)} {...props}>
      {children}
    </div>
  )
}
