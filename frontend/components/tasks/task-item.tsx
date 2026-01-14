// [Task]: T067, T085, T088, T096 [P] [US2, US4, US5] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Task item component displaying a single task.
 * Shows checkbox, title, description (truncated if > 100 chars), created date, and action buttons.
 * Includes Edit and Delete buttons with minimum 44x44px touch targets for mobile.
 */
'use client'

import { useState } from 'react'
import { Checkbox } from '@/components/ui/checkbox'
import { Button } from '@/components/ui/button'
import type { Task } from '@/types'

interface TaskItemProps {
  task: Task
  onToggleComplete?: (taskId: number, completed: boolean) => Promise<void>
  onEdit?: (task: Task) => void
  onDelete?: (task: Task) => void
}

export function TaskItem({ task, onToggleComplete, onEdit, onDelete }: TaskItemProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  }

  const shouldTruncate = task.description && task.description.length > 100
  const displayDescription =
    task.description && shouldTruncate && !isExpanded
      ? `${task.description.substring(0, 100)}...`
      : task.description

  const handleCheckboxChange = async (checked: boolean) => {
    if (onToggleComplete) {
      await onToggleComplete(task.id, checked)
    }
  }

  return (
    <div className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-md transition-shadow">
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 pt-1">
          <Checkbox
            checked={task.completed}
            onChange={(e) => handleCheckboxChange(e.target.checked)}
            id={`task-${task.id}`}
          />
        </div>

        <div className="flex-1 min-w-0">
          <h3
            className={`text-lg font-medium text-gray-900 dark:text-white ${
              task.completed ? 'line-through text-gray-500 dark:text-gray-500' : ''
            }`}
          >
            {task.title}
          </h3>

          {task.description && (
            <div className="mt-2">
              <p className="text-sm text-gray-600 dark:text-gray-400 whitespace-pre-wrap">
                {displayDescription}
              </p>
              {shouldTruncate && (
                <button
                  onClick={() => setIsExpanded(!isExpanded)}
                  className="mt-1 text-sm text-blue-600 hover:text-blue-800 font-medium transition-colors"
                >
                  {isExpanded ? 'Show less' : 'Read more'}
                </button>
              )}
            </div>
          )}

          <div className="mt-2 flex items-center gap-4 text-xs text-gray-500 dark:text-gray-500">
            <span>Created: {formatDate(task.created_at)}</span>
            <span>ID: #{task.id}</span>
          </div>
        </div>

        <div className="flex-shrink-0 flex flex-col sm:flex-row gap-2">
          {onEdit && (
            <Button
              variant="secondary"
              onClick={() => onEdit(task)}
              className="text-sm px-3 py-2 min-h-[44px] min-w-[44px] sm:min-h-[36px] sm:min-w-[auto]"
            >
              Edit
            </Button>
          )}
          {onDelete && (
            <Button
              variant="danger"
              onClick={() => onDelete(task)}
              className="text-sm px-3 py-2 min-h-[44px] min-w-[44px] sm:min-h-[36px] sm:min-w-[auto]"
            >
              Delete
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
