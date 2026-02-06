# Quickstart Guide: Phase III Todo AI Chatbot

**Feature**: AI-Powered Todo Chatbot with MCP Tools Architecture
**Date**: 2026-02-03

## Prerequisites

- Python 3.11+
- pip package manager
- PostgreSQL-compatible database (Neon recommended)
- OpenAI API key
- Node.js 18+ (for frontend development)

## Setup Instructions

### 1. Clone and Initialize Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Environment Configuration
Create a `.env` file in the backend directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://username:password@host:port/database_name
ENVIRONMENT=development
```

#### Database Initialization
```bash
cd backend
python -m src.database.session  # This will create the required tables
```

### 3. MCP Tools Setup

The MCP tools are located in `backend/mcp_tools/` and provide the following functionality:

- `add_task`: Create new tasks via natural language
- `list_tasks`: Retrieve user's tasks
- `complete_task`: Mark tasks as completed
- `delete_task`: Remove tasks from user's list
- `update_task`: Modify existing tasks

Each tool follows the interface: `function(user_id: str, **kwargs) -> dict`

### 4. Start the Backend Server

```bash
cd backend
python main.py
```

The server will start on `http://localhost:8000`

### 5. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Usage Examples

### Natural Language Commands

Once the system is running, users can interact with the AI assistant using commands like:

- "Add a task to buy groceries tomorrow"
- "Show me my pending tasks"
- "Complete the meeting prep task"
- "Delete the old appointment task"
- "Update the project deadline task to next week"

### API Testing

You can test the chat API directly:

```bash
curl -X POST http://localhost:8000/api/user-uuid-here/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to call mom"}'
```

## Development Workflow

### Running Tests

Backend tests:
```bash
cd backend
pytest
```

### Database Migrations

If you need to make changes to the data model:

1. Update the SQLModel definitions in `backend/src/models/`
2. Run the database initialization again to recreate tables (for development)
3. For production, implement proper migration scripts

### Adding New MCP Tools

To add a new MCP tool:

1. Create a new directory in `backend/mcp_tools/`
2. Implement the tool function with proper error handling
3. Register the tool with the AI agent
4. Update the agent's instructions to recognize the new capability

## Troubleshooting

### Common Issues

- **OpenAI API errors**: Verify your API key is correctly set in the environment
- **Database connection errors**: Check your DATABASE_URL configuration
- **Tool not found errors**: Ensure all MCP tools are properly registered with the agent
- **Conversation persistence issues**: Verify that conversation and message tables exist

### Environment Variables

Required environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key for the agent
- `DATABASE_URL`: Connection string for your PostgreSQL database
- `ENVIRONMENT`: Set to "development" or "production"