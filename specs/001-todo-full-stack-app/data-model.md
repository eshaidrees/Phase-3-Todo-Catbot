# Data Model: Todo Full-Stack Web Application

## Entity Definitions

### User Entity
- **Fields**:
  - id: UUID (Primary Key)
  - email: String (Unique, Indexed)
  - hashed_password: String
  - is_verified: Boolean (Default: False)
  - created_at: DateTime (Auto-generated)
  - updated_at: DateTime (Auto-generated, Updates on modification)
- **Relationships**:
  - One-to-Many: User → Tasks (via user_id foreign key)
- **Validation Rules**:
  - Email must be valid email format
  - Email must be unique across all users
  - Password must meet minimum security requirements
- **State Transitions**:
  - Unverified (initial) → Verified (after email confirmation)

### Task Entity
- **Fields**:
  - id: UUID (Primary Key)
  - title: String (Required, Max 255 chars)
  - description: Text (Optional)
  - completed: Boolean (Default: False)
  - due_date: DateTime (Optional)
  - created_at: DateTime (Auto-generated)
  - updated_at: DateTime (Auto-generated, Updates on modification)
  - user_id: UUID (Foreign Key to User.id, Indexed)
- **Relationships**:
  - Many-to-One: Task → User (via user_id foreign key)
- **Validation Rules**:
  - Title must not be empty
  - User_id must reference an existing user
  - Due date must be in the future if provided
- **State Transitions**:
  - Incomplete (initial) → Complete (when marked as done)
  - Complete → Incomplete (when unmarked)

## Database Schema

### Tables

#### users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

#### tasks
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    due_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
```

## Relationships
- Users and Tasks: One-to-Many (One user can have many tasks)
- Referential Integrity: Tasks are deleted when their user is deleted (CASCADE)
- Access Control: Applications must filter tasks by user_id to enforce data isolation

## Constraints
- Primary Keys: All entities have UUID primary keys for distributed systems compatibility
- Foreign Keys: Enforce referential integrity between entities
- Unique Constraints: Email uniqueness in users table
- NOT NULL Constraints: Critical fields that must have values
- Check Constraints: Future expansion for data validation rules

## Indexing Strategy
- Primary indexes on all ID fields for fast lookups
- Index on user email for authentication queries
- Index on user_id in tasks for filtering by user
- Index on completion status for common queries
- Index on due_date for sorting and filtering by deadline