# API Contract: Todo Full-Stack Web Application

## Base URL
```
https://api.yourapp.com (production)
http://localhost:8000 (development)
```

## Authentication
All endpoints require JWT authentication in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

JWT token is obtained via Better Auth upon successful login/registration.

## API Endpoints

### Authentication Endpoints
These are handled by Better Auth and not part of our custom API.

### Task Management Endpoints

#### GET /api/{user_id}/tasks
**Description**: Retrieve all tasks for a specific user
**Authentication**: Required
**Parameters**:
- user_id (path): UUID of the authenticated user
- limit (query, optional): Number of tasks to return (default: 50, max: 100)
- offset (query, optional): Number of tasks to skip for pagination (default: 0)
- completed (query, optional): Filter by completion status (true/false)

**Response**:
- 200 OK: Array of task objects
```json
[
  {
    "id": "uuid-string",
    "title": "Task title",
    "description": "Task description or null",
    "completed": false,
    "due_date": "2023-12-31T10:00:00Z or null",
    "created_at": "2023-11-20T15:30:00Z",
    "updated_at": "2023-11-20T15:30:00Z",
    "user_id": "user-uuid-string"
  }
]
```
- 401 Unauthorized: Invalid or missing JWT
- 403 Forbidden: User attempting to access another user's tasks
- 404 Not Found: User ID does not exist

#### POST /api/{user_id}/tasks
**Description**: Create a new task for a specific user
**Authentication**: Required
**Parameters**:
- user_id (path): UUID of the authenticated user

**Request Body**:
```json
{
  "title": "Task title (required)",
  "description": "Task description (optional)",
  "due_date": "2023-12-31T10:00:00Z (optional, ISO 8601 format)"
}
```

**Response**:
- 201 Created: Successfully created task
```json
{
  "id": "new-task-uuid",
  "title": "Task title",
  "description": "Task description or null",
  "completed": false,
  "due_date": "2023-12-31T10:00:00Z or null",
  "created_at": "2023-11-20T15:30:00Z",
  "updated_at": "2023-11-20T15:30:00Z",
  "user_id": "user-uuid-string"
}
```
- 400 Bad Request: Invalid request body
- 401 Unauthorized: Invalid or missing JWT
- 403 Forbidden: User attempting to create task for another user
- 422 Unprocessable Entity: Validation errors

#### GET /api/{user_id}/tasks/{id}
**Description**: Retrieve a specific task for a user
**Authentication**: Required
**Parameters**:
- user_id (path): UUID of the authenticated user
- id (path): UUID of the task to retrieve

**Response**:
- 200 OK: Task object
```json
{
  "id": "task-uuid-string",
  "title": "Task title",
  "description": "Task description or null",
  "completed": false,
  "due_date": "2023-12-31T10:00:00Z or null",
  "created_at": "2023-11-20T15:30:00Z",
  "updated_at": "2023-11-20T15:30:00Z",
  "user_id": "user-uuid-string"
}
```
- 401 Unauthorized: Invalid or missing JWT
- 403 Forbidden: User attempting to access another user's task
- 404 Not Found: Task or user does not exist

#### PUT /api/{user_id}/tasks/{id}
**Description**: Update a specific task for a user
**Authentication**: Required
**Parameters**:
- user_id (path): UUID of the authenticated user
- id (path): UUID of the task to update

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description or null",
  "completed": false,
  "due_date": "2023-12-31T10:00:00Z or null"
}
```

**Response**:
- 200 OK: Updated task object
```json
{
  "id": "task-uuid-string",
  "title": "Updated task title",
  "description": "Updated task description or null",
  "completed": false,
  "due_date": "2023-12-31T10:00:00Z or null",
  "created_at": "2023-11-20T15:30:00Z",
  "updated_at": "2023-11-20T16:45:00Z",  // updated timestamp
  "user_id": "user-uuid-string"
}
```
- 400 Bad Request: Invalid request body
- 401 Unauthorized: Invalid or missing JWT
- 403 Forbidden: User attempting to update another user's task
- 404 Not Found: Task or user does not exist
- 422 Unprocessable Entity: Validation errors

#### DELETE /api/{user_id}/tasks/{id}
**Description**: Delete a specific task for a user
**Authentication**: Required
**Parameters**:
- user_id (path): UUID of the authenticated user
- id (path): UUID of the task to delete

**Response**:
- 204 No Content: Task successfully deleted
- 401 Unauthorized: Invalid or missing JWT
- 403 Forbidden: User attempting to delete another user's task
- 404 Not Found: Task or user does not exist

#### PATCH /api/{user_id}/tasks/{id}/complete
**Description**: Update the completion status of a specific task
**Authentication**: Required
**Parameters**:
- user_id (path): UUID of the authenticated user
- id (path): UUID of the task to update

**Request Body**:
```json
{
  "completed": true
}
```

**Response**:
- 200 OK: Updated task object with new completion status
```json
{
  "id": "task-uuid-string",
  "title": "Task title",
  "description": "Task description or null",
  "completed": true,  // updated status
  "due_date": "2023-12-31T10:00:00Z or null",
  "created_at": "2023-11-20T15:30:00Z",
  "updated_at": "2023-11-20T17:20:00Z",  // updated timestamp
  "user_id": "user-uuid-string"
}
```
- 400 Bad Request: Invalid request body (completed field missing or not boolean)
- 401 Unauthorized: Invalid or missing JWT
- 403 Forbidden: User attempting to update another user's task
- 404 Not Found: Task or user does not exist
- 422 Unprocessable Entity: Validation errors

## Error Responses
All error responses follow this structure:
```json
{
  "detail": "Human-readable error message"
}
```

## Common HTTP Status Codes
- 200 OK: Request successful
- 201 Created: Resource successfully created
- 204 No Content: Request successful, no content to return
- 400 Bad Request: Invalid request format
- 401 Unauthorized: Missing or invalid authentication
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Resource does not exist
- 422 Unprocessable Entity: Request validation failed
- 500 Internal Server Error: Unexpected server error