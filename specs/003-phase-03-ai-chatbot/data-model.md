# Data Model: Phase 3 - AI Chatbot

**Date**: 2026-01-15
**Feature**: 003-phase-03-ai-chatbot

## Overview

Phase 3 introduces two new entities for chat functionality while reusing existing `users` and `tasks` tables from Phase 2.

## Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────┐
│    users     │       │  conversations   │       │   messages   │
├──────────────┤       ├──────────────────┤       ├──────────────┤
│ id (PK)      │──────<│ id (PK)          │──────<│ id (PK)      │
│ email        │       │ user_id (FK)     │       │ conv_id (FK) │
│ hashed_pass  │       │ created_at       │       │ role         │
│ created_at   │       │ updated_at       │       │ content      │
└──────────────┘       └──────────────────┘       │ created_at   │
       │                                          └──────────────┘
       │
       │         ┌──────────────┐
       └────────<│    tasks     │
                 ├──────────────┤
                 │ id (PK)      │
                 │ user_id (FK) │
                 │ title        │
                 │ description  │
                 │ completed    │
                 │ created_at   │
                 │ updated_at   │
                 └──────────────┘
```

## Existing Entities (Phase 2)

### users
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email address |
| hashed_password | VARCHAR(255) | NOT NULL | Argon2 password hash |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW | Account creation time |

### tasks
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Unique identifier |
| user_id | INTEGER | FK(users.id), NOT NULL | Task owner |
| title | VARCHAR(255) | NOT NULL | Task title |
| description | TEXT | NULL | Optional description |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW | Creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW | Last update time |

**Indexes**: user_id, completed, created_at

---

## New Entities (Phase 3)

### conversations

Represents a chat session between a user and the AI assistant.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique conversation identifier |
| user_id | INTEGER | FK(users.id), NOT NULL | Conversation owner |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW | Session start time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW | Last activity time |

**Indexes**: user_id

**Relationships**:
- Belongs to: users (many-to-one)
- Has many: messages (one-to-many)

**Lifecycle**:
- Created when user sends first message (or explicitly)
- Deleted on user logout (session-based per constitution)

### messages

Represents a single message in a conversation.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique message identifier |
| conversation_id | UUID | FK(conversations.id), NOT NULL | Parent conversation |
| role | VARCHAR(20) | NOT NULL, CHECK(role IN ('user', 'assistant')) | Message author role |
| content | TEXT | NOT NULL | Message content |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW | Message timestamp |

**Indexes**: conversation_id, created_at

**Relationships**:
- Belongs to: conversations (many-to-one)

**Validation Rules**:
- role must be 'user' or 'assistant'
- content cannot be empty
- Messages ordered by created_at within conversation

---

## State Transitions

### Conversation States
```
                  ┌─────────────┐
 User sends  ────>│   ACTIVE    │<──── User sends
 first message    │             │      more messages
                  └──────┬──────┘
                         │
                         │ User logs out
                         ▼
                  ┌─────────────┐
                  │   DELETED   │
                  │  (removed)  │
                  └─────────────┘
```

### Task States (via MCP tools)
```
                  ┌─────────────┐
  add_task  ────> │   PENDING   │
                  │ completed=  │
                  │   false     │
                  └──────┬──────┘
                         │
        complete_task    │    complete_task
        (completed=true) │    (completed=false)
                         ▼
                  ┌─────────────┐
                  │  COMPLETED  │
                  │ completed=  │
                  │    true     │
                  └─────────────┘
```

---

## Migration Script

```sql
-- Migration: Add chat tables for Phase 3

-- Conversations table
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);

-- Messages table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);

-- Trigger to update conversation.updated_at on new message
CREATE OR REPLACE FUNCTION update_conversation_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE conversations SET updated_at = NOW() WHERE id = NEW.conversation_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_conversation_timestamp
AFTER INSERT ON messages
FOR EACH ROW EXECUTE FUNCTION update_conversation_timestamp();
```

---

## SQLModel Definitions

### Conversation Model
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: list["Message"] = Relationship(back_populates="conversation")
```

### Message Model
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Literal

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", nullable=False)
    role: Literal["user", "assistant"] = Field(nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
```

---

## Data Access Patterns

### Get or Create Conversation
```python
async def get_or_create_conversation(user_id: int, conversation_id: UUID | None) -> Conversation:
    if conversation_id:
        conv = await session.get(Conversation, conversation_id)
        if conv and conv.user_id == user_id:
            return conv
    # Create new conversation
    conv = Conversation(user_id=user_id)
    session.add(conv)
    await session.commit()
    return conv
```

### Add Message
```python
async def add_message(conversation_id: UUID, role: str, content: str) -> Message:
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    session.add(message)
    await session.commit()
    return message
```

### Get Conversation History
```python
async def get_messages(conversation_id: UUID, limit: int = 50) -> list[Message]:
    result = await session.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .limit(limit)
    )
    return result.all()
```

### Clear User Conversations (on logout)
```python
async def clear_user_conversations(user_id: int) -> None:
    await session.exec(
        delete(Conversation).where(Conversation.user_id == user_id)
    )
    await session.commit()
```
