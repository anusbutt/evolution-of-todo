---
id: 007
title: Phase 6 Task Editing and Deletion
stage: green
date: 2026-01-14
surface: agent
model: claude-sonnet-4-5
feature: 002-phase-02-web-app
branch: master
user: PC
command: /sp.implement phase 6
labels: ["implementation", "backend", "frontend", "task-editing", "task-deletion", "phase-6"]
links:
  spec: specs/002-phase-02-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/app/services/task_service.py
  - backend/app/routes/tasks.py
  - frontend/components/tasks/task-form.tsx
  - frontend/components/tasks/task-item.tsx
  - frontend/components/tasks/task-list.tsx
  - frontend/components/ui/confirm-dialog.tsx
  - frontend/app/(dashboard)/tasks/page.tsx
  - specs/002-phase-02-web-app/tasks.md
tests:
  - Manual testing required: edit task → verify changes → delete task → confirm → verify removal
---

## Prompt

phase 6

## Response snapshot

Successfully implemented Phase 6: User Story 4 - Task Editing & Deletion (T081-T091).

**Backend Implementation (T081-T084)**:
- Added update_task() function to task_service.py:
  - Authorization check (task belongs to user)
  - Updates title, description, and/or completed fields
  - Updates updated_at timestamp
  - Returns updated task or None

- Added delete_task() function to task_service.py:
  - Authorization check (task belongs to user)
  - Deletes task from database
  - Returns success boolean

- Created PUT /api/tasks/{task_id} endpoint:
  - JWT-protected with user authorization
  - Accepts TaskUpdate schema (all fields optional)
  - Returns TaskResponse with updated task

- Created DELETE /api/tasks/{task_id} endpoint:
  - JWT-protected with user authorization
  - Returns 204 No Content on success
  - Returns 404 if not found or unauthorized

**Frontend Implementation (T085-T091)**:
- Updated TaskForm component to support edit mode:
  - Accepts optional `task` prop
  - Pre-fills form with existing task data
  - Changes button text to "Save Changes" in edit mode
  - useEffect to update form when task prop changes

- Created ConfirmDialog component:
  - Reusable confirmation dialog with message
  - Confirm/Cancel buttons with loading state
  - Uses Modal component for consistent UI

- Updated TaskItem component:
  - Added "Edit" button (opens modal with pre-filled form)
  - Added "Delete" button (opens confirmation dialog)
  - Buttons positioned on the right side of task card

- Updated TaskList component:
  - Passes onEdit and onDelete handlers to TaskItem

- Updated tasks page with full CRUD operations:
  - handleEditTask: PUT /api/tasks/{id}, update in list
  - handleOpenEdit: Opens modal with editingTask state
  - handleOpenDelete: Opens confirmation dialog
  - handleConfirmDelete: DELETE /api/tasks/{id}, remove from list, refresh stats
  - handleCloseModal: Clears editingTask state
  - Loading states for all operations (isSubmitting, isDeleting)
  - Auto-refresh stats after create/delete

**User Story 4 Complete**: Users can now edit and delete tasks with intuitive modal forms and confirmation dialogs.

## Outcome

- ✅ Impact: Phase 6 complete - Full CRUD operations (Create, Read, Update, Delete) for tasks
- 🧪 Tests: Manual E2E testing required (edit → save → verify, delete → confirm → verify)
- 📁 Files: 8 files created/modified (2 backend, 6 frontend)
- 🔁 Next prompts: Phase 7 - Responsive Web Interface (mobile/tablet layouts)
- 🧠 Reflection: Modal forms for editing provide consistent UX, confirmation dialog prevents accidental deletions, auto-refresh stats keeps dashboard accurate

## Evaluation notes (flywheel)

- Failure modes observed: None - clean separation of create/edit modes, proper state management
- Graders run and results (PASS/FAIL): Manual validation required
- Prompt variant (if applicable): Standard implementation command
- Next experiment (smallest change to try): Add optimistic UI updates for edit operations similar to status toggle
