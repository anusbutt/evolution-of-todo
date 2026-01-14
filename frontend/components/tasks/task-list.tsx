// [Task]: T068 [P] [US2] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Task list component displaying array of tasks.
 * Shows empty state if no tasks exist.
 */
'use client'

import { TaskItem } from './task-item'
import type { Task } from '@/types'

interface TaskListProps {
  tasks: Task[]
  onToggleComplete?: (taskId: number, completed: boolean) => Promise<void>
  onEdit?: (task: Task) => void
  onDelete?: (task: Task) => void
}

export function TaskList({ tasks, onToggleComplete, onEdit, onDelete }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">📝</div>
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
          No tasks yet
        </h3>
        <p className="text-gray-600 dark:text-gray-400">
          Add your first task to get started!
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onToggleComplete={onToggleComplete}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  )
}
