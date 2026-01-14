// [Task]: T078, T108 [US3, US6] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Task statistics component displaying task completion metrics.
 * Shows total tasks, completed count, completion percentage, and incomplete count.
 */
'use client'

interface TaskStatsProps {
  stats: {
    total: number
    completed: number
    incomplete: number
    completion_percentage: number
  }
}

export function TaskStats({ stats }: TaskStatsProps) {
  const { total, completed, incomplete, completion_percentage } = stats

  // Show context-aware message when no tasks exist
  if (total === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <div className="flex items-center gap-3">
          <div className="text-4xl">📝</div>
          <div>
            <p className="text-lg font-semibold text-gray-900 dark:text-white">
              Total: 0 tasks
            </p>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Get started by adding your first task!
            </p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      <div className="flex flex-wrap items-center gap-6">
        <div>
          <p className="text-sm text-gray-600 dark:text-gray-400">Total Tasks</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">{total}</p>
        </div>

        <div className="h-12 w-px bg-gray-200 dark:bg-gray-700" />

        <div>
          <p className="text-sm text-gray-600 dark:text-gray-400">Completed</p>
          <p className="text-2xl font-bold text-green-600 dark:text-green-400">{completed}</p>
        </div>

        <div className="h-12 w-px bg-gray-200 dark:bg-gray-700" />

        <div>
          <p className="text-sm text-gray-600 dark:text-gray-400">Completion Rate</p>
          <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
            {completion_percentage}%
          </p>
        </div>

        <div className="h-12 w-px bg-gray-200 dark:bg-gray-700" />

        <div>
          <p className="text-sm text-gray-600 dark:text-gray-400">Incomplete</p>
          <p className="text-2xl font-bold text-gray-600 dark:text-gray-400">{incomplete}</p>
        </div>

        {/* Progress bar */}
        <div className="flex-1 min-w-[200px]">
          <div className="flex items-center gap-2 mb-1">
            <p className="text-xs text-gray-600 dark:text-gray-400">Progress</p>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
            <div
              className="bg-blue-600 dark:bg-blue-400 h-full rounded-full transition-all duration-300"
              style={{ width: `${completion_percentage}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  )
}
