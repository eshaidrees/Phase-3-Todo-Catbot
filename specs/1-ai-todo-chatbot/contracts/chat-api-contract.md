# API Contract: Chat Endpoint for Todo AI Chatbot

**Feature**: AI-Powered Todo Chatbot with MCP Tools Architecture
**Endpoint**: `POST /api/{user_id}/chat`
**Date**: 2026-02-03

## Purpose

This endpoint serves as the primary interface between the frontend chat UI and the AI agent. It handles natural language requests from users, processes them through the AI agent with MCP tools, and returns structured responses.

## Request

### Path Parameters
- `user_id` (string, required): UUID of the authenticated user

### Request Body
```json
{
  "message": "Add a task to buy groceries tomorrow",
  "conversation_id": "optional-conversation-uuid-if-existing"
}
```

**Fields**:
- `message`: The natural language command from the user (required)
- `conversation_id`: UUID of existing conversation to continue (optional, new conversation created if omitted)

## Response

### Success Response (200 OK)
```json
{
  "success": true,
  "conversation_id": "uuid-of-conversation",
  "response": "I've added the task 'buy groceries tomorrow' to your list.",
  "operation": {
    "type": "add_task",
    "result": {
      "success": true,
      "task_id": "uuid-of-created-task",
      "message": "Task 'buy groceries tomorrow' added successfully"
    }
  },
  "timestamp": "2026-02-03T10:30:00Z"
}
```

### Error Response (4xx/5xx)
```json
{
  "success": false,
  "error": "Human-readable error message",
  "details": {
    "code": "ERROR_CODE",
    "message": "Detailed error information"
  },
  "timestamp": "2026-02-03T10:30:00Z"
}
```

## Processing Flow

1. Validate user_id format (must be valid UUID)
2. Fetch conversation history from DB (create new if conversation_id not provided)
3. Store new user message in database
4. Send conversation history + new message to AI agent
5. Agent processes message and may call MCP tools
6. MCP tools execute database operations
7. Agent generates response based on tool results
8. Store assistant response in database
9. Return structured response to frontend

## Error Cases

- **400 Bad Request**: Invalid user_id format, empty message
- **404 Not Found**: User_id doesn't correspond to existing user
- **500 Internal Server Error**: AI agent or MCP tools failure
- **503 Service Unavailable**: External AI service unavailable

## Security Considerations

- User_id must match authenticated user (validated by auth middleware)
- Rate limiting applied per user_id
- Input sanitization for message content
- No sensitive data exposed in error messages