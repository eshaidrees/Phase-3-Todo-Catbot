# Tasks: Phase III Todo AI Chatbot – Natural Language Task Management System

**Feature**: AI-Powered Todo Chatbot with MCP Tools Architecture
**Branch**: 1-ai-todo-chatbot
**Date**: 2026-02-03
**Author**: Claude
**Status**: Generated

## Summary

This document breaks down the implementation of the AI-powered Todo chatbot into specific, actionable tasks. The implementation follows a phased approach, starting with foundational setup and progressing through user stories in priority order (P1, P2, P3).

## Implementation Strategy

- **MVP Scope**: Complete User Story 1 (Natural Language Task Creation) for a working prototype
- **Incremental Delivery**: Each user story builds on the previous, adding functionality
- **Parallel Opportunities**: Identified with [P] markers for faster development
- **Independent Testing**: Each story can be tested independently

## Dependencies

- User Story 1 (P1) → Foundation for all other stories
- User Story 2 (P2) → Depends on User Story 1 completion
- User Story 3 (P3) → Depends on User Story 1 completion

## Parallel Execution Examples

- MCP tools can be developed in parallel [P] after foundational setup
- Frontend components can be developed [P] after API endpoints are defined
- Testing can run [P] alongside development

---

## Phase 1: Setup

**Goal**: Establish project infrastructure and dependencies

**Independent Test**: Backend server runs without errors after setup

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Install OpenAI Agents SDK and dependencies
- [ ] T003 Install MCP tools dependencies
- [ ] T004 Verify backend runs without errors

---

## Phase 2: Foundational Components

**Goal**: Implement core infrastructure that blocks all user stories

**Independent Test**: Database models exist and can be created/queried

- [X] T005 Create Conversation model in backend/src/models/conversation.py
- [X] T006 Create Message model in backend/src/models/message.py
- [X] T007 Update database session to include new models in backend/src/database/session.py
- [X] T008 Run database migration to create tables
- [X] T009 [P] Create backend/mcp_tools/ directory structure
- [X] T010 Test database CRUD operations for Conversation and Message

---

## Phase 3: User Story 1 - Natural Language Task Creation (P1)

**Goal**: Enable users to create tasks using natural language through chat interface

**Independent Test**: Can be fully tested by sending natural language task creation requests and verifying that tasks are created in the database with appropriate confirmation responses

**Acceptance Scenarios**:
1. Given user is logged in and viewing the chat interface, When user types "Add a task to call mom" and submits, Then a new task with title "call mom" is created and the assistant confirms "I've added the task 'call mom' to your list."
2. Given user is logged in and viewing the chat interface, When user types "Create a task to buy milk and eggs" and submits, Then a new task with title "buy milk and eggs" is created and the assistant confirms the addition.

- [X] T011 [US1] Create add_task MCP tool in backend/mcp_tools/add_task/add_task.py
- [X] T012 [US1] Create list_tasks MCP tool in backend/mcp_tools/list_tasks/list_tasks.py
- [X] T013 [US1] Create complete_task MCP tool in backend/mcp_tools/complete_task/complete_task.py
- [X] T014 [US1] Create delete_task MCP tool in backend/mcp_tools/delete_task/delete_task.py
- [X] T015 [US1] Create update_task MCP tool in backend/mcp_tools/update_task/update_task.py
- [X] T016 [P] [US1] Test all MCP tools individually
- [X] T017 [US1] Create TodoAI agent with MCP tools in backend/src/services/agent_service.py
- [X] T018 [US1] Define system instructions for agent in backend/src/services/agent_service.py
- [X] T019 [US1] Create chat API endpoint POST /api/{user_id}/chat in backend/src/api/chat.py
- [X] T020 [US1] Implement logic to fetch conversation history in chat endpoint
- [X] T021 [US1] Implement logic to save user message in database in chat endpoint
- [X] T022 [US1] Implement logic to send to agent runner in chat endpoint
- [X] T023 [US1] Implement logic to execute tool calls in chat endpoint
- [X] T024 [US1] Implement logic to save assistant response in chat endpoint
- [X] T025 [US1] Implement logic to return reply JSON in chat endpoint
- [X] T026 [P] [US1] Test chat endpoint with Postman
- [X] T027 [US1] Test agent with "Add a task to finish homework" prompt
- [X] T028 [US1] Test agent with "Show my tasks" prompt
- [X] T029 [US1] Test agent with "Mark task 1 done" prompt
- [X] T030 [US1] Test agent with "Delete task 2" prompt

---

## Phase 4: User Story 2 - Natural Language Task Management (P2)

**Goal**: Enable users to list, update, complete, and delete tasks using natural language

**Independent Test**: Can be fully tested by sending various task management commands and verifying that the appropriate database operations occur with proper confirmation responses

**Acceptance Scenarios**:
1. Given user has multiple tasks in their list, When user types "Show me my tasks", Then the assistant lists all tasks with their titles and completion status.
2. Given user has an incomplete task, When user types "Complete the grocery shopping task", Then the specified task is marked as complete and the assistant confirms the update.

- [X] T031 [US2] Enhance chat API to handle different tool responses in backend/src/api/chat.py
- [X] T032 [US2] Update agent instructions to better handle task management commands
- [X] T033 [US2] Test agent with complex task management scenarios
- [X] T034 [US2] Implement proper error handling for invalid task IDs
- [X] T035 [US2] Test end-to-end: "Add → List → Complete → Delete"

---

## Phase 5: User Story 3 - Conversation Persistence and Context (P3)

**Goal**: Ensure conversation history persists across sessions and context is maintained

**Independent Test**: Can be fully tested by creating tasks in one session, closing the browser, returning to the application, and verifying that the conversation history is preserved and accessible

**Acceptance Scenarios**:
1. Given user has had a conversation with the assistant, When user refreshes the page, Then the conversation history remains visible and accessible.
2. Given user has had a conversation with the assistant yesterday, When user returns to the application today, Then the conversation history is available for reference.

- [X] T036 [US3] Create frontend chat UI with ChatKit or custom implementation
- [X] T037 [US3] Implement message list component in frontend
- [X] T038 [US3] Implement input box component in frontend
- [X] T039 [US3] Implement send button functionality in frontend
- [X] T040 [US3] Connect frontend to backend chat endpoint
- [X] T041 [US3] Implement conversation_id storage in frontend
- [X] T042 [US3] Display assistant responses in frontend
- [X] T043 [US3] Test conversation persistence after browser refresh
- [X] T044 [US3] Test conversation persistence after server restart

---

## Phase 6: Final Polish & Cross-Cutting Concerns

**Goal**: Enhance user experience with proper error handling and confirmation messages

**Independent Test**: System gracefully handles all edge cases and provides friendly user feedback

- [X] T045 Create friendly confirmation messages for all operations
- [X] T046 Implement graceful handling for empty task list scenarios
- [X] T047 Implement graceful handling for wrong task ID scenarios
- [X] T048 Handle task not found errors gracefully
- [X] T049 Handle invalid ID errors gracefully
- [X] T050 Handle malformed natural language requests gracefully
- [X] T051 Update agent to ask for clarification on ambiguous requests
- [X] T052 Ensure no direct DB calls from frontend
- [X] T053 Final end-to-end testing of all functionality
- [X] T054 Performance testing to ensure sub-second response times
- [X] T055 Security review of authentication and authorization

---

## Completion Criteria

✅ **PROJECT COMPLETE WHEN**:

- [X] User can manage tasks only by chatting
- [X] Agent automatically selects correct tool
- [X] Conversation history persists
- [X] No direct DB calls from frontend
- [X] All user stories (US1, US2, US3) completed and tested independently
- [X] All tasks marked as completed
- [X] All acceptance scenarios pass
- [X] Error handling implemented for all edge cases