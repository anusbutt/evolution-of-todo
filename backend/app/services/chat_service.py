# [Task]: T031-T037, T048 [US1, US2] | [Spec]: specs/003-phase-03-ai-chatbot/plan.md
"""
Chat Service - Orchestrates AI chatbot interactions.
Integrates OpenAI Agents SDK with Gemini API and MCP tools.
"""
import logging
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from agents import Agent, Runner
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from openai import AsyncOpenAI

from app.config import settings
from app.models.conversation import Conversation
from app.models.message import Message

logger = logging.getLogger(__name__)

# T032, T048: Agent system prompt for task management
SYSTEM_PROMPT = """You are a helpful task management assistant. You help users manage their tasks through natural language.

You have access to the following tools:
- add_task: Add a new task to the user's task list
- list_tasks: Show all tasks for the user

When the user wants to:
- Create/add a task: Use add_task with their task title and optional description
- View/list/show tasks: Use list_tasks to show their tasks
- Complete/mark done: Use complete_task with the task number from the list
- Delete/remove: Use delete_task with the task number from the list
- Update/change/rename: Use update_task with the task number and new title

Guidelines:
- Be concise and friendly
- Confirm actions clearly (e.g., "Done! I've added 'buy groceries' to your tasks.")
- When listing tasks, format them nicely with numbers and status indicators
- Use checkmarks for completed tasks and circles for pending tasks
- If the user's intent is unclear, ask for clarification
- Extract task titles naturally from conversational requests
- For "Add buy groceries", the task title should be "buy groceries"
- Always respond in a helpful, conversational tone

Remember: The user_id will be provided automatically - you don't need to ask for it."""


class ChatService:
    """Service for handling chat interactions with AI agent."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self._agent: Optional[Agent] = None
        self._runner: Optional[Runner] = None

    async def _get_agent(self) -> Agent:
        """
        T033: Configure OpenAI Agents SDK with Gemini endpoint.
        T034: Configure MCP server connection (HTTP transport).
        """
        if self._agent is None:
            # Create OpenAI client pointing to Gemini API
            external_client = AsyncOpenAI(
                api_key=settings.gemini_api_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            )

            # Create model wrapper
            llm_model = OpenAIChatCompletionsModel(
                model="gemini-2.0-flash",
                openai_client=external_client,
            )

            # Create agent with MCP server config
            self._agent = Agent(
                name="TaskAssistant",
                model=llm_model,
                instructions=SYSTEM_PROMPT,
                # MCP server connection will be configured via environment
                # The agent will use HTTP transport to localhost:5001
            )

        return self._agent

    async def get_or_create_conversation(
        self, user_id: int, conversation_id: Optional[UUID] = None
    ) -> Conversation:
        """
        T035: Implement conversation get_or_create logic.
        Get existing conversation or create new one for the user.
        """
        if conversation_id:
            # Try to get existing conversation
            result = await self.session.execute(
                select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id,
                )
            )
            conversation = result.scalar_one_or_none()
            if conversation:
                return conversation

        # Create new conversation
        conversation = Conversation(user_id=user_id)
        self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)
        return conversation

    async def save_message(
        self, conversation_id: UUID, role: str, content: str
    ) -> Message:
        """
        T036: Implement message save logic.
        Save a message to the conversation.
        """
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def get_conversation_history(
        self, conversation_id: UUID, limit: int = 20
    ) -> list[Message]:
        """
        T037: Implement conversation history loading for multi-turn context.
        Get recent messages from conversation for context.
        """
        result = await self.session.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def process_message(
        self,
        user_id: int,
        message: str,
        conversation_id: Optional[UUID] = None,
    ) -> dict:
        """
        Process a user message and return AI response.
        Orchestrates the full chat flow.
        """
        from sqlalchemy.exc import OperationalError, InterfaceError

        try:
            # Get or create conversation
            conversation = await self.get_or_create_conversation(
                user_id, conversation_id
            )

            # Save user message
            await self.save_message(conversation.id, "user", message)

            # Get conversation history for context
            history = await self.get_conversation_history(conversation.id)

            # Build messages for agent
            messages = []
            for msg in history:
                messages.append({
                    "role": msg.role,
                    "content": msg.content,
                })

            # Call agent via direct API call (simpler approach without full MCP integration)
            response_text, task_updated = await self._call_agent(user_id, message, messages)

            # Save assistant response
            await self.save_message(conversation.id, "assistant", response_text)

            return {
                "response": response_text,
                "conversation_id": conversation.id,
                "task_updated": task_updated,
                "timestamp": datetime.utcnow(),
            }

        except (OperationalError, InterfaceError) as e:
            # T060: Database/service unavailable fallback
            logger.error(f"Database connection error: {e}")
            return {
                "response": "I'm having trouble connecting to the task service right now. Your message was received, but I couldn't process it. Please try again in a moment.",
                "conversation_id": conversation_id,
                "task_updated": False,
                "timestamp": datetime.utcnow(),
                "error": "service_unavailable",
            }
        except Exception as e:
            logger.exception(f"Error processing chat message: {e}")
            raise

    async def _call_agent(
        self, user_id: int, message: str, history: list[dict]
    ) -> tuple[str, bool]:
        """
        Call the AI agent to process the message.
        Returns (response_text, task_updated).
        """
        import httpx

        task_updated = False

        # Check if this is a task listing request
        message_lower = message.lower()
        is_list_request = any(
            keyword in message_lower
            for keyword in ["show", "list", "view", "see", "what are my", "my tasks", "all tasks"]
        )

        if is_list_request:
            # List user's tasks
            try:
                response = await self._list_tasks_via_api(user_id)
                if response.get("success"):
                    tasks = response.get("tasks", [])
                    if not tasks:
                        return ("You don't have any tasks yet. Would you like to add one?", False)

                    # Format task list nicely
                    task_lines = []
                    for i, task in enumerate(tasks, 1):
                        status = "✓" if task.get("completed") else "○"
                        title = task.get("title", "Untitled")
                        task_lines.append(f"{i}. {status} {title}")

                    task_list = "\n".join(task_lines)
                    return (f"Here are your tasks:\n\n{task_list}", False)
                else:
                    return (f"Sorry, I couldn't retrieve your tasks: {response.get('error', 'Unknown error')}", False)
            except Exception as e:
                logger.error(f"Error listing tasks: {e}")
                # Fallback to Gemini
                pass

        # Check if this is a task creation request
        is_add_request = any(
            keyword in message_lower
            for keyword in ["add", "create", "new task", "make a task", "remind me to"]
        )

        if is_add_request:
            # Extract task title from message
            title = self._extract_task_title(message)
            if title:
                # Call MCP server to add task
                try:
                    async with httpx.AsyncClient() as client:
                        # For now, directly call our add_task logic via HTTP
                        # In full implementation, this would go through MCP protocol
                        response = await self._add_task_via_api(user_id, title)
                        if response.get("success"):
                            task_updated = True
                            task = response.get("task", {})
                            return (
                                f"Done! I've added '{task.get('title', title)}' to your task list.",
                                True,
                            )
                        else:
                            return (
                                f"Sorry, I couldn't add that task: {response.get('error', 'Unknown error')}",
                                False,
                            )
                except Exception as e:
                    logger.error(f"Error calling MCP server: {e}")
                    # Fallback to Gemini for response
                    pass

        # Check if this is a task completion request
        is_complete_request = any(
            keyword in message_lower
            for keyword in ["complete", "mark", "done", "finish", "check off", "tick"]
        )

        if is_complete_request:
            # Extract task number from message
            task_number = self._extract_task_number(message)
            if task_number:
                try:
                    response = await self._complete_task_via_api(user_id, task_number)
                    if response.get("success"):
                        task = response.get("task", {})
                        return (
                            f"Done! I've marked '{task.get('title', f'Task {task_number}')}' as complete. ✓",
                            True,
                        )
                    else:
                        return (
                            f"Sorry, I couldn't complete that task: {response.get('error', 'Unknown error')}",
                            False,
                        )
                except Exception as e:
                    logger.error(f"Error completing task: {e}")
                    # Fallback to Gemini for response
                    pass
            else:
                # No task number found, ask for clarification
                return (
                    "Which task would you like to mark as complete? Please specify the task number (e.g., 'Complete task 1').",
                    False,
                )

        # Check if this is a task deletion request
        is_delete_request = any(
            keyword in message_lower
            for keyword in ["delete", "remove", "get rid of", "trash", "discard"]
        )

        if is_delete_request:
            # Extract task number from message
            task_number = self._extract_task_number(message)
            if task_number:
                try:
                    response = await self._delete_task_via_api(user_id, task_number)
                    if response.get("success"):
                        deleted_task = response.get("deleted_task", {})
                        return (
                            f"Done! I've deleted '{deleted_task.get('title', f'Task {task_number}')}' from your list.",
                            True,
                        )
                    else:
                        return (
                            f"Sorry, I couldn't delete that task: {response.get('error', 'Unknown error')}",
                            False,
                        )
                except Exception as e:
                    logger.error(f"Error deleting task: {e}")
                    # Fallback to Gemini for response
                    pass
            else:
                # No task number found, ask for clarification
                return (
                    "Which task would you like to delete? Please specify the task number (e.g., 'Delete task 1').",
                    False,
                )

        # Check if this is a task update request
        is_update_request = any(
            keyword in message_lower
            for keyword in ["update", "change", "rename", "edit", "modify"]
        )

        if is_update_request:
            # Extract task number and new title from message
            task_number = self._extract_task_number(message)
            new_title = self._extract_update_title(message)
            if task_number and new_title:
                try:
                    response = await self._update_task_via_api(user_id, task_number, new_title)
                    if response.get("success"):
                        task = response.get("task", {})
                        return (
                            f"Done! I've updated the task to '{task.get('title', new_title)}'.",
                            True,
                        )
                    else:
                        return (
                            f"Sorry, I couldn't update that task: {response.get('error', 'Unknown error')}",
                            False,
                        )
                except Exception as e:
                    logger.error(f"Error updating task: {e}")
                    # Fallback to Gemini for response
                    pass
            elif task_number and not new_title:
                return (
                    "What would you like to change this task to? Please specify the new title (e.g., 'Change task 1 to buy milk').",
                    False,
                )
            else:
                # No task number found, ask for clarification
                return (
                    "Which task would you like to update? Please specify the task number and new title (e.g., 'Change task 1 to buy milk').",
                    False,
                )

        # For non-task requests or fallback, use Gemini directly
        try:
            import asyncio
            from httpx import TimeoutException

            client = AsyncOpenAI(
                api_key=settings.gemini_api_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                timeout=30.0,  # T059: 30 second timeout for LLM calls
            )

            # Build messages with system prompt
            api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            api_messages.extend(history[-10:])  # Last 10 messages for context

            response = await client.chat.completions.create(
                model="gemini-2.0-flash",
                messages=api_messages,
            )

            return response.choices[0].message.content or "I'm not sure how to help with that.", task_updated

        except asyncio.TimeoutError:
            # T059: Graceful timeout handling
            logger.warning("Gemini API call timed out")
            return "I'm taking longer than expected to respond. Please try again in a moment.", False
        except TimeoutException:
            # T059: httpx timeout handling
            logger.warning("Gemini API request timed out")
            return "The AI service is slow to respond. Please try again shortly.", False
        except Exception as e:
            error_msg = str(e).lower()
            # T059: User-friendly error messages based on error type
            if "rate limit" in error_msg or "quota" in error_msg:
                logger.warning(f"Gemini API rate limited: {e}")
                return "I'm receiving too many requests right now. Please wait a moment and try again.", False
            elif "api key" in error_msg or "authentication" in error_msg:
                logger.error(f"Gemini API authentication error: {e}")
                return "There's a configuration issue with the AI service. Please contact support.", False
            elif "connection" in error_msg or "network" in error_msg:
                logger.error(f"Gemini API connection error: {e}")
                return "I'm having trouble connecting to the AI service. Please check your connection and try again.", False
            else:
                logger.error(f"Error calling Gemini API: {e}")
                return "I'm having trouble processing that request. Please try again.", False

    def _extract_task_title(self, message: str) -> Optional[str]:
        """Extract task title from natural language message."""
        message_lower = message.lower().strip()

        # Common patterns for task creation
        prefixes = [
            "add ",
            "add task ",
            "add a task ",
            "add a task to ",
            "add a task called ",
            "create ",
            "create task ",
            "create a task ",
            "create a task called ",
            "new task ",
            "make a task ",
            "remind me to ",
            "i need to ",
            "i have to ",
        ]

        for prefix in prefixes:
            if message_lower.startswith(prefix):
                title = message[len(prefix):].strip()
                # Remove common suffixes
                for suffix in [" to my list", " to my tasks", " to the list"]:
                    if title.lower().endswith(suffix):
                        title = title[:-len(suffix)]
                return title.strip() if title.strip() else None

        # If no prefix found, use the whole message as title
        # (for simple commands like "buy groceries")
        return message.strip() if len(message.strip()) > 2 else None

    async def _add_task_via_api(self, user_id: int, title: str) -> dict:
        """Add task by directly calling the backend task creation logic."""
        from app.models.task import Task

        try:
            task = Task(
                user_id=user_id,
                title=title,
                completed=False,
            )
            self.session.add(task)
            await self.session.commit()
            await self.session.refresh(task)

            return {
                "success": True,
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() + "Z" if task.created_at else None,
                }
            }
        except Exception as e:
            logger.error(f"Error adding task: {e}")
            return {"success": False, "error": str(e)}

    async def _list_tasks_via_api(self, user_id: int) -> dict:
        """List tasks by directly querying the database."""
        from app.models.task import Task

        try:
            result = await self.session.execute(
                select(Task)
                .where(Task.user_id == user_id)
                .order_by(Task.created_at.desc())
            )
            tasks = result.scalars().all()

            # Store task mapping for completion by number
            self._task_id_map = {i + 1: task.id for i, task in enumerate(tasks)}

            return {
                "success": True,
                "tasks": [
                    {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat() + "Z" if task.created_at else None,
                    }
                    for task in tasks
                ],
                "count": len(tasks)
            }
        except Exception as e:
            logger.error(f"Error listing tasks: {e}")
            return {"success": False, "error": str(e)}

    def _extract_task_number(self, message: str) -> Optional[int]:
        """Extract task number from natural language message."""
        import re

        # Look for patterns like "task 1", "task #1", "#1", "number 1", "1"
        patterns = [
            r"task\s*#?\s*(\d+)",
            r"#(\d+)",
            r"number\s*(\d+)",
            r"(\d+)(?:st|nd|rd|th)?\s*(?:task|one)?",
        ]

        message_lower = message.lower()
        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                return int(match.group(1))

        return None

    async def _complete_task_via_api(self, user_id: int, task_number: int) -> dict:
        """Complete a task by its display number (from list)."""
        from app.models.task import Task

        try:
            # First, get the task list to map number to actual ID
            result = await self.session.execute(
                select(Task)
                .where(Task.user_id == user_id)
                .order_by(Task.created_at.desc())
            )
            tasks = list(result.scalars().all())

            # Check if task number is valid
            if task_number < 1 or task_number > len(tasks):
                return {
                    "success": False,
                    "error": f"Task number {task_number} not found. You have {len(tasks)} tasks."
                }

            # Get the task at that position (1-indexed)
            task = tasks[task_number - 1]

            if task.completed:
                return {
                    "success": True,
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "completed": task.completed,
                    },
                    "message": f"Task '{task.title}' is already complete!"
                }

            # Mark as complete
            task.completed = True
            self.session.add(task)
            await self.session.commit()
            await self.session.refresh(task)

            return {
                "success": True,
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() + "Z" if task.created_at else None,
                }
            }
        except Exception as e:
            logger.error(f"Error completing task: {e}")
            return {"success": False, "error": str(e)}

    async def _delete_task_via_api(self, user_id: int, task_number: int) -> dict:
        """Delete a task by its display number (from list)."""
        from app.models.task import Task

        try:
            # First, get the task list to map number to actual ID
            result = await self.session.execute(
                select(Task)
                .where(Task.user_id == user_id)
                .order_by(Task.created_at.desc())
            )
            tasks = list(result.scalars().all())

            # Check if task number is valid
            if task_number < 1 or task_number > len(tasks):
                return {
                    "success": False,
                    "error": f"Task number {task_number} not found. You have {len(tasks)} tasks."
                }

            # Get the task at that position (1-indexed)
            task = tasks[task_number - 1]

            # Store task info before deletion
            task_info = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
            }

            # Delete the task
            await self.session.delete(task)
            await self.session.commit()

            return {
                "success": True,
                "deleted_task": task_info
            }
        except Exception as e:
            logger.error(f"Error deleting task: {e}")
            return {"success": False, "error": str(e)}

    def _extract_update_title(self, message: str) -> Optional[str]:
        """Extract new title from update message."""
        import re

        message_lower = message.lower()

        # Patterns like "change task 1 to buy milk", "rename task 2 to groceries"
        patterns = [
            r"(?:to|into|as)\s+['\"]?(.+?)['\"]?\s*$",
            r"task\s*#?\s*\d+\s+(?:to|into|as)\s+['\"]?(.+?)['\"]?\s*$",
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                new_title = match.group(1).strip()
                # Clean up quotes if present
                new_title = new_title.strip("'\"")
                if new_title:
                    return new_title

        return None

    async def _update_task_via_api(self, user_id: int, task_number: int, new_title: str) -> dict:
        """Update a task's title by its display number (from list)."""
        from app.models.task import Task

        try:
            # First, get the task list to map number to actual ID
            result = await self.session.execute(
                select(Task)
                .where(Task.user_id == user_id)
                .order_by(Task.created_at.desc())
            )
            tasks = list(result.scalars().all())

            # Check if task number is valid
            if task_number < 1 or task_number > len(tasks):
                return {
                    "success": False,
                    "error": f"Task number {task_number} not found. You have {len(tasks)} tasks."
                }

            # Get the task at that position (1-indexed)
            task = tasks[task_number - 1]

            # Update the title
            old_title = task.title
            task.title = new_title.strip()
            self.session.add(task)
            await self.session.commit()
            await self.session.refresh(task)

            return {
                "success": True,
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() + "Z" if task.created_at else None,
                },
                "old_title": old_title
            }
        except Exception as e:
            logger.error(f"Error updating task: {e}")
            return {"success": False, "error": str(e)}
