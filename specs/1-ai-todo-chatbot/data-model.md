# Data Model: Phase III Todo AI Chatbot

**Feature**: AI-Powered Todo Chatbot with MCP Tools Architecture
**Date**: 2026-02-03

## Entity Overview

The system consists of three primary entities: Task (reused from Phase II), Conversation, and Message. These entities support the natural language task management system with conversation persistence.

## Entity Details

### Task (Reused from Phase II)

**Description**: Represents a user's todo item with attributes like title, description, completion status, and timestamps

**Fields**:
- `id`: UUID (Primary Key, auto-generated)
- `title`: String (max_length=255, required)
- `description`: String (optional, nullable)
- `completed`: Boolean (default: false)
- `due_date`: DateTime (optional, nullable)
- `user_id`: UUID (Foreign Key to User, indexed)
- `created_at`: DateTime (auto-generated)
- `updated_at`: DateTime (auto-generated)

**Validation Rules**:
- Title must be 1-255 characters
- User_id must reference an existing user
- Due date must be in the future (if provided)

**State Transitions**:
- `pending` → `completed` when task is marked as done
- `completed` → `pending` when task is unmarked (optional feature)

### Conversation

**Description**: Contains a collection of messages between a user and the AI assistant, associated with a specific user

**Fields**:
- `id`: UUID (Primary Key, auto-generated)
- `user_id`: UUID (Foreign Key to User, indexed)
- `title`: String (auto-generated from first message or summary, optional)
- `created_at`: DateTime (auto-generated)
- `updated_at`: DateTime (auto-generated, updated with last message)

**Validation Rules**:
- User_id must reference an existing user
- Created_at must be before updated_at

### Message

**Description**: Individual exchanges within a conversation, including both user inputs and assistant responses

**Fields**:
- `id`: UUID (Primary Key, auto-generated)
- `conversation_id`: UUID (Foreign Key to Conversation, indexed)
- `user_id`: UUID (Foreign Key to User, indexed)
- `role`: String (enum: 'user' or 'assistant', required)
- `content`: Text (required)
- `tool_calls`: JSON (nullable, for storing AI tool calls)
- `tool_responses`: JSON (nullable, for storing tool results)
- `created_at`: DateTime (auto-generated)

**Validation Rules**:
- Conversation_id must reference an existing conversation
- Role must be either 'user' or 'assistant'
- Content must not be empty
- User_id must match the conversation owner

## Relationships

```
User (1) ←→ (Many) Task
User (1) ←→ (Many) Conversation
User (1) ←→ (Many) Message

Conversation (1) ←→ (Many) Message
```

## Indexing Strategy

- Task: Index on user_id for efficient user-specific queries
- Conversation: Index on user_id for efficient user-specific queries
- Message: Index on conversation_id for efficient conversation retrieval
- Message: Composite index on (conversation_id, created_at) for chronological ordering

## Constraints

- All entities use UUID primary keys for distributed system compatibility
- Foreign key constraints ensure referential integrity
- Timestamps are automatically managed by the database/models
- Soft deletes (if needed) will be handled via a 'deleted_at' field pattern