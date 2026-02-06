---
description: "Task list for Todo Full-Stack Web Application implementation"
---

# Tasks: Todo Full-Stack Web Application

**Input**: Design documents from `/specs/001-todo-full-stack-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks as requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume web app structure - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure with backend/ and frontend/ directories
- [x] T002 Create Python virtual environment in backend/ (venv)
- [x] T003 Activate venv and install FastAPI, SQLModel, Uvicorn, Neon dependencies
- [x] T004 Initialize Next.js 16+ project with Better Auth in frontend/
- [x] T005 [P] Configure linting and formatting tools for both backend and frontend
---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Setup database schema and migrations framework with Neon PostgreSQL in backend/src/database/
- [x] T007 [P] Implement Better Auth authentication framework in frontend/src/lib/auth.ts and backend/src/api/deps.py
- [x] T008 [P] Setup API routing and middleware structure in backend/src/api/routes/
- [x] T009 Create User and Task models based on data-model.md in backend/src/models/
- [x] T0010 Configure error handling and logging infrastructure in backend/src/utils/
- [x] T011 Setup environment configuration management in backend/.env and frontend/.env.local
- [x] T012 Create database session management in backend/src/database/session.py
- [x] T013 Setup CORS middleware for frontend-backend communication in backend/src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Login (Priority: P1) 🎯 MVP

**Goal**: Allow users to create accounts with email and password, verify their account, and log in to access their personal todo list

**Independent Test**: Register a new user, verify the account, log in, and access the application to see a basic dashboard

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T014 [P] [US1] Contract test for authentication endpoints in backend/tests/contract/test_auth.py
- [ ] T015 [P] [US1] Integration test for registration/login flow in backend/tests/integration/test_auth_flow.py

### Implementation for User Story 1

- [x] T016 [P] [US1] Create User model in backend/src/models/user.py
- [x] T017 [P] [US1] Create authentication service in backend/src/services/auth.py
- [x] T018 [US1] Implement registration endpoint in backend/src/api/routes/auth.py
- [x] T019 [US1] Implement login endpoint in backend/src/api/routes/auth.py
- [x] T020 [US1] Create JWT token handling in backend/src/utils/token.py
- [x] T021 [US1] Implement email verification logic in backend/src/services/auth.py
- [x] T022 [US1] Create Better Auth integration in frontend/src/lib/auth.ts
- [x] T023 [US1] Create registration page in frontend/src/app/register/page.tsx
- [x] T024 [US1] Create login page in frontend/src/app/login/page.tsx
- [x] T025 [US1] Create dashboard page skeleton in frontend/src/app/dashboard/page.tsx
- [x] T026 [US1] Implement JWT token management in frontend/src/lib/api.ts

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Create, Read, Update, Delete (CRUD) Tasks (Priority: P1)

**Goal**: Allow authenticated users to create new todo tasks, view existing tasks, update task details, and delete tasks

**Independent Test**: Log in as an authenticated user and perform all CRUD operations on tasks

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T027 [P] [US2] Contract test for task CRUD endpoints in backend/tests/contract/test_tasks.py
- [ ] T028 [P] [US2] Integration test for task management flow in backend/tests/integration/test_task_flow.py

### Implementation for User Story 2

- [x] T029 [P] [US2] Create Task model in backend/src/models/task.py
- [x] T030 [P] [US2] Create task service in backend/src/services/task_service.py
- [x] T031 [US2] Implement GET /api/{user_id}/tasks endpoint in backend/src/api/routes/tasks.py
- [x] T032 [US2] Implement POST /api/{user_id}/tasks endpoint in backend/src/api/routes/tasks.py
- [x] T033 [US2] Implement GET /api/{user_id}/tasks/{id} endpoint in backend/src/api/routes/tasks.py
- [x] T034 [US2] Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/src/api/routes/tasks.py
- [x] T035 [US2] Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/src/api/routes/tasks.py
- [x] T036 [US2] Create task API client in frontend/src/lib/api.ts
- [x] T037 [US2] Create TaskList component in frontend/src/components/TaskList/TaskList.tsx
- [x] T038 [US2] Create TaskForm component in frontend/src/components/TaskForm/TaskForm.tsx
- [x] T039 [US2] Implement task CRUD functionality in dashboard page frontend/src/app/dashboard/page.tsx
- [x] T040 [US2] Add user ID validation middleware in backend/src/api/deps.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Tasks as Complete/Incomplete (Priority: P2)

**Goal**: Allow authenticated users to mark tasks as complete or incomplete to track their progress

**Independent Test**: Log in as an authenticated user and mark tasks as complete/incomplete, observing the visual changes

### Tests for User Story 3 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T041 [P] [US3] Contract test for task completion endpoint in backend/tests/contract/test_task_completion.py
- [ ] T042 [P] [US3] Integration test for task completion flow in backend/tests/integration/test_task_completion.py

### Implementation for User Story 3

- [x] T043 [US3] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/src/api/routes/tasks.py
- [x] T044 [US3] Update task service to handle completion toggle in backend/src/services/task_service.py
- [x] T045 [US3] Add completion toggle functionality to TaskList component in frontend/src/components/TaskList/TaskList.tsx
- [x] T046 [US3] Update task display to show completion status in frontend/src/components/TaskList/TaskList.tsx
- [x] T047 [US3] Add optimistic UI updates for task completion in frontend/src/components/TaskList/TaskList.tsx

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Responsive UI Across Devices (Priority: P2)

**Goal**: Ensure the application interface adapts to provide optimal usability on desktop, tablet, and mobile devices

**Independent Test**: Access the application on different device sizes and verify the layout adapts appropriately

### Tests for User Story 4 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T048 [P] [US4] Responsive UI tests for different screen sizes in frontend/tests/components/test_responsive_ui.js

### Implementation for User Story 4

- [x] T049 [US4] Create responsive layout components in frontend/src/components/Layout/
- [x] T050 [US4] Implement CSS Grid/Flexbox for responsive design in frontend/src/styles/globals.css
- [x] T051 [US4] Add media queries for tablet and mobile breakpoints in frontend/src/styles/globals.css
- [x] T052 [US4] Update TaskList component for mobile optimization in frontend/src/components/TaskList/TaskList.tsx
- [x] T053 [US4] Update TaskForm component for mobile optimization in frontend/src/components/TaskForm/TaskForm.tsx
- [x] T054 [US4] Create mobile navigation in frontend/src/components/Navigation/MobileNav.tsx
- [x] T055 [US4] Test responsive behavior across devices in frontend/src/app/page.tsx

**Checkpoint**: All user stories should now work responsively across devices

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T056 [P] Documentation updates in README.md and docs/
- [x] T057 Add proper error handling and user feedback throughout the UI
- [x] T058 Performance optimization for task loading and rendering
- [x] T059 [P] Additional unit tests in backend/tests/unit/ and frontend/tests/
- [x] T060 Security hardening: input validation, SQL injection protection, XSS prevention
- [x] T061 Run quickstart.md validation to ensure setup instructions work
- [x] T062 Add loading states and error boundaries in frontend components
- [x] T063 Implement proper session management and logout functionality
- [x] T064 Add data persistence validation tests
- [x] T065 Final integration testing of all features together

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 for authentication
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 and US2 for tasks
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Depends on US1, US2, US3 for UI

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 2

```bash
# Launch all tests for User Story 2 together:
Task: "Contract test for task CRUD endpoints in backend/tests/contract/test_tasks.py"
Task: "Integration test for task management flow in backend/tests/integration/test_task_flow.py"

# Launch all models for User Story 2 together:
Task: "Create Task model in backend/src/models/task.py"
Task: "Create task service in backend/src/services/task_service.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Registration/Login)
4. Complete Phase 4: User Story 2 (Task CRUD)
5. **STOP and VALIDATE**: Test User Stories 1 & 2 independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence