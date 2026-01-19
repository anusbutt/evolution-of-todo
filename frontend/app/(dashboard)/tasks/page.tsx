// [Task]: T069-T071, T076, T079-T080, T087, T090-T091, T105 [US2, US3, US4, US6] | [Spec]: specs/002-phase-02-web-app/spec.md
// [Task]: T026, T027, T028, T042-T045 [US6, US1] | [Spec]: specs/003-phase-03-ai-chatbot/spec.md
/**
 * Tasks page - main task management interface.
 * Displays task list with add/edit/delete functionality, modal forms, task statistics,
 * and AI chat sidebar for natural language task management.
 */
'use client'

import { useState, useEffect } from 'react'
import { TaskList } from '@/components/tasks/task-list'
import { TaskForm } from '@/components/tasks/task-form'
import { TaskStats } from '@/components/tasks/task-stats'
import { TaskSearch } from '@/components/tasks/task-search'
import { Modal } from '@/components/ui/modal'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { Button } from '@/components/ui/button'
import { ChatSidebar, ChatToggle, type Message } from '@/components/chat'
import { apiRequest, ApiError } from '@/lib/api-client'
import { sendChatMessage } from '@/services/chat'
import type { Task } from '@/types'

interface TaskStatistics {
  total: number
  completed: number
  incomplete: number
  completion_percentage: number
}

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [searchResults, setSearchResults] = useState<Task[] | null>(null)
  const [isSearching, setIsSearching] = useState(false)
  const [stats, setStats] = useState<TaskStatistics | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [editingTask, setEditingTask] = useState<Task | null>(null)
  const [deletingTask, setDeletingTask] = useState<Task | null>(null)
  const [isDeleting, setIsDeleting] = useState(false)

  // Chat sidebar state (Phase 3)
  const [isChatOpen, setIsChatOpen] = useState(false)
  const [chatMessages, setChatMessages] = useState<Message[]>([])
  const [isChatLoading, setIsChatLoading] = useState(false)
  // T065: Controlled chat input for preserving text on error
  const [chatInputValue, setChatInputValue] = useState('')
  // T063: Persist conversation_id in localStorage for session continuity
  const [conversationId, setConversationId] = useState<string | undefined>(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('chat_conversation_id') || undefined
    }
    return undefined
  })

  // Fetch tasks and stats on mount
  useEffect(() => {
    fetchTasks()
    fetchStats()
  }, [])

  const fetchTasks = async () => {
    setIsLoading(true)
    setError(null)

    try {
      const data = await apiRequest<Task[]>('/api/tasks', {
        method: 'GET',
      })
      setTasks(data)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError('Failed to load tasks. Please try again.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  const fetchStats = async () => {
    try {
      const data = await apiRequest<TaskStatistics>('/api/tasks/stats', {
        method: 'GET',
      })
      setStats(data)
    } catch (err) {
      console.error('Failed to fetch stats:', err)
      // Don't show error for stats, just log it
    }
  }

  const handleCreateTask = async (data: { title: string; description?: string }) => {
    setIsSubmitting(true)

    try {
      const newTask = await apiRequest<Task>('/api/tasks', {
        method: 'POST',
        body: JSON.stringify(data),
      })

      // Add new task to the beginning of the list
      setTasks([newTask, ...tasks])
      setIsModalOpen(false)
      await fetchStats() // Refresh stats
    } catch (err) {
      if (err instanceof ApiError) {
        throw new Error(err.message)
      } else {
        throw new Error('Failed to create task. Please try again.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleEditTask = async (data: { title: string; description?: string }) => {
    if (!editingTask) return

    setIsSubmitting(true)

    try {
      const updatedTask = await apiRequest<Task>(`/api/tasks/${editingTask.id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
      })

      // Update task in list
      setTasks((prevTasks) =>
        prevTasks.map((task) => (task.id === updatedTask.id ? updatedTask : task))
      )
      setEditingTask(null)
      setIsModalOpen(false)
    } catch (err) {
      if (err instanceof ApiError) {
        throw new Error(err.message)
      } else {
        throw new Error('Failed to update task. Please try again.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleOpenEdit = (task: Task) => {
    setEditingTask(task)
    setIsModalOpen(true)
  }

  const handleOpenDelete = (task: Task) => {
    setDeletingTask(task)
  }

  const handleConfirmDelete = async () => {
    if (!deletingTask) return

    setIsDeleting(true)

    try {
      await apiRequest(`/api/tasks/${deletingTask.id}`, {
        method: 'DELETE',
      })

      // Remove task from list
      setTasks((prevTasks) => prevTasks.filter((task) => task.id !== deletingTask.id))
      setDeletingTask(null)
      await fetchStats() // Refresh stats
    } catch (err) {
      console.error('Failed to delete task:', err)
      // Could show error toast here
    } finally {
      setIsDeleting(false)
    }
  }

  const handleCloseModal = () => {
    setIsModalOpen(false)
    setEditingTask(null)
  }

  const handleToggleComplete = async (taskId: number, completed: boolean) => {
    // Optimistic UI update
    const previousTasks = tasks
    setTasks((prevTasks) =>
      prevTasks.map((task) =>
        task.id === taskId ? { ...task, completed } : task
      )
    )

    try {
      // Call PATCH /api/tasks/{taskId}/status
      await apiRequest<Task>(`/api/tasks/${taskId}/status`, {
        method: 'PATCH',
      })

      // Refresh stats after successful toggle
      await fetchStats()
    } catch (err) {
      // Revert optimistic update on error
      setTasks(previousTasks)
      console.error('Failed to toggle task status:', err)
    }
  }

  // T042-T045: Chat message handler connected to real API
  const handleSendChatMessage = async (message: string) => {
    // Add user message to chat
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: message,
      timestamp: new Date(),
    }
    setChatMessages((prev) => [...prev, userMessage])
    setIsChatLoading(true)
    // T065: Clear input optimistically, will restore on error
    setChatInputValue('')

    try {
      // T042: Call chat API service
      const response = await sendChatMessage(message, conversationId)

      // T043: Display AI response in ChatSidebar
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: response.response,
        timestamp: new Date(response.timestamp),
      }
      setChatMessages((prev) => [...prev, assistantMessage])

      // T063: Store conversation ID for subsequent messages and persist
      setConversationId(response.conversation_id)
      if (typeof window !== 'undefined') {
        localStorage.setItem('chat_conversation_id', response.conversation_id)
      }

      // T045: Auto-refresh task list when task_updated is true
      if (response.task_updated) {
        await fetchTasks()
        await fetchStats()
      }
    } catch (err) {
      // T065: Restore input text on error
      setChatInputValue(message)
      // T061: Error handling - show user-friendly error message
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: err instanceof ApiError
          ? `Sorry, I encountered an error: ${err.message}`
          : 'Sorry, I\'m having trouble processing that request. Please try again.',
        timestamp: new Date(),
      }
      setChatMessages((prev) => [...prev, errorMessage])
      console.error('Chat error:', err)
    } finally {
      // T044: Loading indicator is handled by isChatLoading state
      setIsChatLoading(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">⚠️</div>
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
          Error loading tasks
        </h3>
        <p className="text-gray-600 dark:text-gray-400 mb-4">{error}</p>
        <Button variant="primary" onClick={fetchTasks}>
          Retry
        </Button>
      </div>
    )
  }

  // Display search results if searching, otherwise display all tasks
  const displayedTasks = searchResults !== null ? searchResults : tasks
  const taskCount = isSearching ? displayedTasks.length : tasks.length

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">My Tasks</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            {isSearching ? (
              <>
                {taskCount} {taskCount === 1 ? 'result' : 'results'} found
              </>
            ) : (
              <>
                {taskCount} {taskCount === 1 ? 'task' : 'tasks'}
              </>
            )}
          </p>
        </div>
        <Button variant="primary" onClick={() => setIsModalOpen(true)}>
          Add Task
        </Button>
      </div>

      {stats && <TaskStats stats={stats} />}

      <TaskSearch
        onSearchResults={setSearchResults}
        onSearchStateChange={setIsSearching}
      />

      <TaskList
        tasks={displayedTasks}
        onToggleComplete={handleToggleComplete}
        onEdit={handleOpenEdit}
        onDelete={handleOpenDelete}
      />

      <Modal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        title={editingTask ? 'Edit Task' : 'Create New Task'}
      >
        <TaskForm
          task={editingTask || undefined}
          onSubmit={editingTask ? handleEditTask : handleCreateTask}
          onCancel={handleCloseModal}
          isSubmitting={isSubmitting}
        />
      </Modal>

      <ConfirmDialog
        isOpen={!!deletingTask}
        title="Delete Task"
        message={`Are you sure you want to delete "${deletingTask?.title}"? This action cannot be undone.`}
        confirmText="Delete"
        cancelText="Cancel"
        onConfirm={handleConfirmDelete}
        onCancel={() => setDeletingTask(null)}
        isLoading={isDeleting}
      />

      {/* Chat Sidebar (Phase 3) */}
      <ChatToggle
        isOpen={isChatOpen}
        onClick={() => setIsChatOpen(!isChatOpen)}
      />
      <ChatSidebar
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
        messages={chatMessages}
        onSendMessage={handleSendChatMessage}
        isLoading={isChatLoading}
        inputValue={chatInputValue}
        onInputChange={setChatInputValue}
      />
    </div>
  )
}
