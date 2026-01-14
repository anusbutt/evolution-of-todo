// [Task]: T033 [P] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Reusable Modal component with overlay and keyboard support.
 * Closes on outside click and ESC key press.
 */
'use client'

import { ReactNode, useEffect, useRef } from 'react'
import { clsx } from 'clsx'

export interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title?: string
  children: ReactNode
  className?: string
}

export function Modal({ isOpen, onClose, title, children, className }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null)

  // Handle ESC key press
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && isOpen) {
        onClose()
      }
    }

    document.addEventListener('keydown', handleEscape)
    return () => document.removeEventListener('keydown', handleEscape)
  }, [isOpen, onClose])

  // Handle click outside modal
  const handleOverlayClick = (event: React.MouseEvent<HTMLDivElement>) => {
    if (event.target === event.currentTarget) {
      onClose()
    }
  }

  if (!isOpen) return null

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-0 md:p-4"
      onClick={handleOverlayClick}
    >
      <div
        ref={modalRef}
        className={clsx(
          'bg-white dark:bg-gray-900 rounded-none md:rounded-lg shadow-xl w-full h-full md:h-auto md:w-auto md:max-w-lg md:max-h-[90vh] overflow-auto',
          className
        )}
      >
        {title && (
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
              {title}
            </h2>
          </div>
        )}
        <div className="px-6 py-4">{children}</div>
      </div>
    </div>
  )
}
