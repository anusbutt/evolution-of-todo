// [Task]: T029 | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * TypeScript type definitions for Phase 2 frontend.
 * Defines interfaces for User, Task, API responses, and errors.
 */

/**
 * User entity representing an authenticated user.
 */
export interface User {
  id: number
  email: string
  name: string
  created_at: string
  updated_at: string
}

/**
 * Task entity representing a todo item.
 */
export interface Task {
  id: number
  user_id: number
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string
}

/**
 * API error response structure.
 */
export interface ApiError {
  detail: string
  code: string
  field?: string
  details?: any
}

/**
 * Authentication response from signup/login endpoints.
 */
export interface AuthResponse {
  id: number
  email: string
  name: string
  created_at: string
  updated_at: string
}

/**
 * Task response from task endpoints.
 */
export interface TaskResponse {
  id: number
  user_id: number
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string
}

/**
 * Task list response.
 */
export interface TaskListResponse {
  tasks: TaskResponse[]
  total: number
}

/**
 * Task statistics response.
 */
export interface TaskStats {
  total: number
  completed: number
  incomplete: number
  completion_percentage: number
}

/**
 * Task creation/update payload.
 */
export interface TaskCreatePayload {
  title: string
  description?: string
}

/**
 * Task update payload.
 */
export interface TaskUpdatePayload {
  title?: string
  description?: string
}

/**
 * User signup payload.
 */
export interface SignupPayload {
  email: string
  name: string
  password: string
}

/**
 * User login payload.
 */
export interface LoginPayload {
  email: string
  password: string
}
