---
id: 2
title: create-impl-plan
stage: plan
date: 2026-02-03
surface: agent
model: claude-opus-4-5-20251101
feature: ai-todo-chatbot
branch: 1-ai-todo-chatbot
user: user
command: /sp.plan "Phase III Todo AI Chatbot – Implementation Plan..."
labels: ["planning", "architecture", "ai", "todo", "mcp-tools"]
links:
  spec: "specs/1-ai-todo-chatbot/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/1-ai-todo-chatbot/plan.md"
  - "specs/1-ai-todo-chatbot/research.md"
  - "specs/1-ai-todo-chatbot/data-model.md"
  - "specs/1-ai-todo-chatbot/contracts/chat-api-contract.md"
  - "specs/1-ai-todo-chatbot/quickstart.md"
tests: []
---

# Prompt History Record: Create Implementation Plan for AI Todo Chatbot

## Original Prompt

Phase III Todo AI Chatbot – Implementation Plan

Goal:
Extend the Phase II Todo web app into an AI-native system where users manage tasks through natural language using an agent + MCP tools architecture.

Phase 1 – Database & Models
Objective: Support conversational memory and AI-driven operations.

Tasks:
- Reuse existing Task model from Phase II
- Create Conversation model:
  - id, user_id, created_at, updated_at
- Create Message model:
  - id, conversation_id, user_id, role (user/assistant), content, created_at
- Add database migrations
- Test CRUD for Conversation and Message tables

Deliverable:
Database supports tasks + chat history persistence.

---

Phase 2 – MCP Tools Layer (Tool Server)
Objective: Expose task operations as AI-callable tools.

Tasks:
- Create backend/mcp_tools/ folder
- Implement tools:
  - add_task
  - list_tasks
  - complete_task
  - delete_task
  - update_task
- Each tool:
  - Accepts user_id + parameters
  - Interacts with DB using SQLModel
  - Returns structured JSON response
- Handle edge cases (task not found, invalid ID)

Deliverable:
All task logic accessible through MCP tools only.

---

Phase 3 – AI Agent Setup
Objective: Enable natural language → tool calls.

Tasks:
- Define agent (TodoAI) using Agents SDK
- Add system instructions:
  - Map intents to tools
  - Always confirm actions
  - Handle errors gracefully
- Register all 5 MCP tools with the agent
- Test with sample prompts:
  - "Add a task to buy milk"
  - "Show pending tasks"
  - "Mark task 2 complete"

Deliverable:
Agent correctly selects tools based on user language.

---

Phase 4 – Chat API Endpoint (FastAPI)
Objective: Connect frontend chat to the AI agent.

Tasks:
- Create POST /api/{user_id}/chat
- On request:
  1. Fetch conversation history from DB
  2. Store new user message
  3. Send history + message to agent runner
  4. Receive assistant response + tool calls
  5. Store assistant message
  6. Return response JSON
- Ensure server remains stateless

Deliverable:
Working AI chat endpoint connected to DB and agent.

---

Phase 5 – Frontend Chat Interface
Objective: Replace buttons with conversation UI.

Tasks:
- Integrate OpenAI ChatKit UI
- Build chat window:
  - Message list
  - Input box
- Send messages to /api/{user_id}/chat
- Display assistant responses
- Maintain conversation_id between requests

Deliverable:
Users manage tasks entirely through chat.

---

Phase 6 – Error Handling & Polish
Objective: Make the system robust and user-friendly.

Tasks:
- Friendly messages for:
  - Task not found
  - Empty task list
  - Invalid commands
- Improve assistant confirmations
- Test restart scenario (server restart → conversation resumes)
- Validate all tools return correct JSON

Deliverable:
Stable, user-friendly AI Todo chatbot.

---

Final Outcome:
A fully working AI-powered Todo system where:
- Chat = primary interface
- Agent = decision-maker
- MCP tools = task operators
- Database = conversation memory
- Server = stateless and scalable

## Response Summary

Successfully created the implementation plan for the Phase III Todo AI Chatbot in `specs/1-ai-todo-chatbot/plan.md`. The plan includes:

- Complete technical context with technology stack
- Constitution compliance check
- Project structure with backend and frontend organization
- Complexity tracking for architectural decisions

Additionally, created:
- Research document with technology analysis
- Data model with entity relationships
- API contracts for the chat endpoint
- Quickstart guide for developers

All artifacts follow the template structure and provide a solid foundation for the next phase of development.

## Outcome

Implementation plan created successfully with all required supporting documents. Ready for task breakdown phase.