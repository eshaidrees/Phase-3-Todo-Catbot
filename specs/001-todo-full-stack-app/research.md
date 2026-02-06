# Research: Todo Full-Stack Web Application

## Architectural Decisions

### 1. JWT Handling: Store in Memory vs Secure Cookie

**Decision**: Store JWT in browser memory/storage with secure practices

**Rationale**:
- Security: Storing in httpOnly cookies would prevent XSS attacks but makes frontend access difficult
- Usability: Memory storage allows easier frontend access for API calls
- Balance: Using sessionStorage with proper security headers provides good balance
- Better Auth handles the secure aspects of JWT management

**Alternatives considered**:
- HttpOnly cookies: More secure but harder to work with in SPAs
- LocalStorage: Vulnerable to XSS attacks
- Memory-only storage: Most secure against both XSS and CSRF but requires more complex management

### 2. API Structure: Nested `/api/{user_id}/tasks` vs `/tasks?user_id=`

**Decision**: Use `/api/{user_id}/tasks` structure

**Rationale**:
- Clarity: Makes the user context explicit in the URL
- Security: Provides clear isolation between user resources
- REST compliance: Follows resource-oriented design principles
- Simplicity: Easier to implement middleware for user validation

**Alternatives considered**:
- Query parameter approach: Less clear resource hierarchy
- Header-based user identification: Less RESTful, harder to debug

### 3. Task Completion Toggle: PATCH vs PUT

**Decision**: Use PATCH endpoint for task completion

**Rationale**:
- REST consistency: PATCH is designed for partial updates
- Semantics: Changing completion status is a partial update of the task
- Efficiency: Only sends the changed field(s)
- Convention: Industry standard for toggle operations

**Alternatives considered**:
- PUT: Requires sending the entire resource, less efficient for toggles
- Custom endpoints: Less RESTful, more complex routing

### 4. Single FastAPI App vs Modular Routers

**Decision**: Use modular router structure within single FastAPI app

**Rationale**:
- Scalability: Allows organized growth of API endpoints
- Maintainability: Clear separation of concerns between different API sections
- Speed: Single app reduces complexity while still providing modularity
- Best practice: Standard FastAPI pattern for medium-sized applications

**Alternatives considered**:
- Multiple FastAPI apps: Overkill for this use case, more complex deployment
- Monolithic single file: Not maintainable as application grows

## Technology Integration Patterns

### Next.js + FastAPI Integration
- API routes in Next.js for SSR if needed
- Direct API calls from frontend to backend service
- Environment variables for API endpoint configuration
- Proxy setup for development to avoid CORS issues

### Better Auth + FastAPI JWT Validation
- Better Auth manages user sessions and JWT issuance
- Frontend attaches JWT to API requests via Authorization header
- FastAPI middleware validates JWT signature and extracts user identity
- User ID from JWT used to filter database queries

### SQLModel + Neon PostgreSQL
- SQLModel for type-safe database models
- Alembic for migration management
- Connection pooling for performance
- Neon's serverless features for scalability

## Security Considerations

### Authentication Flow
1. User registers/logins via Better Auth
2. Better Auth issues JWT with user claims
3. Frontend stores JWT securely (preferably in memory)
4. All API requests include JWT in Authorization header
5. FastAPI middleware validates JWT and extracts user_id
6. Backend filters data based on authenticated user_id

### Data Isolation
- All queries filtered by user_id extracted from JWT
- Middleware ensures user can only access their own resources
- Foreign key constraints in database for additional safety
- Input validation on all endpoints

## Performance Considerations

### Caching Strategy
- Client-side caching for task lists (with refresh mechanism)
- Server-side connection pooling
- Database indexing on user_id and frequently queried fields

### Database Optimization
- Indexes on user_id for fast filtering
- Efficient pagination for large task lists
- Connection pooling to handle concurrent requests