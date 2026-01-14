// [Task]: T066, T086 [P] [US2, US4] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Task form component for creating new tasks or editing existing tasks.
 * Validates title (1-200 chars) and description (0-1000 chars).
 * Supports edit mode by accepting a task prop to pre-fill form.
 */
'use client'

import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import type { Task } from '@/types'

// Zod schema matching backend validation
const taskFormSchema = z.object({
  title: z
    .string()
    .min(1, 'Title is required')
    .max(200, 'Title must be less than 200 characters')
    .refine((val) => val.trim().length > 0, 'Title cannot be only whitespace'),
  description: z
    .string()
    .max(1000, 'Description must be less than 1000 characters')
    .optional()
    .default(''),
})

type TaskFormData = z.infer<typeof taskFormSchema>

interface TaskFormProps {
  task?: Task  // If provided, form is in edit mode
  onSubmit: (data: TaskFormData) => Promise<void>
  onCancel: () => void
  isSubmitting?: boolean
}

export function TaskForm({ task, onSubmit, onCancel, isSubmitting = false }: TaskFormProps) {
  const [apiError, setApiError] = useState<string | null>(null)
  const isEditMode = !!task

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<TaskFormData>({
    resolver: zodResolver(taskFormSchema),
    defaultValues: {
      title: task?.title || '',
      description: task?.description || '',
    },
  })

  // Update form when task prop changes
  useEffect(() => {
    if (task) {
      reset({
        title: task.title,
        description: task.description || '',
      })
    }
  }, [task, reset])

  const handleFormSubmit = async (data: TaskFormData) => {
    setApiError(null)

    try {
      await onSubmit(data)
      if (!isEditMode) {
        reset() // Clear form on success (only for create mode)
      }
    } catch (error) {
      if (error instanceof Error) {
        setApiError(error.message)
      } else {
        setApiError(isEditMode ? 'Failed to update task. Please try again.' : 'Failed to create task. Please try again.')
      }
    }
  }

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
      <Input
        label="Title"
        type="text"
        placeholder="Enter task title"
        error={errors.title?.message}
        {...register('title')}
        fullWidth
        autoFocus
      />

      <div className="space-y-2">
        <label
          htmlFor="description"
          className="block text-sm font-medium text-gray-700 dark:text-gray-300"
        >
          Description (optional)
        </label>
        <textarea
          id="description"
          placeholder="Enter task description"
          className="w-full px-3 py-2 text-base border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-2 focus:ring-primary focus:border-primary dark:bg-gray-800 dark:text-white resize-vertical min-h-[100px]"
          {...register('description')}
        />
        {errors.description && (
          <span className="text-sm text-red-600 dark:text-red-400">
            {errors.description.message}
          </span>
        )}
      </div>

      {apiError && (
        <div className="p-4 bg-red-100 border border-red-500 rounded-md">
          <p className="text-sm text-red-600 dark:text-red-400">{apiError}</p>
        </div>
      )}

      <div className="flex gap-4 justify-end">
        <Button type="button" variant="secondary" onClick={onCancel} disabled={isSubmitting}>
          Cancel
        </Button>
        <Button type="submit" variant="primary" disabled={isSubmitting}>
          {isSubmitting
            ? (isEditMode ? 'Saving...' : 'Creating...')
            : (isEditMode ? 'Save Changes' : 'Create Task')}
        </Button>
      </div>
    </form>
  )
}
