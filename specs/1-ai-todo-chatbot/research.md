# Research: Phase III Todo AI Chatbot Implementation

**Feature**: AI-Powered Todo Chatbot with MCP Tools Architecture
**Date**: 2026-02-03

## Research Summary

This document consolidates research findings for implementing the AI-powered todo chatbot with MCP tools architecture. All identified unknowns have been resolved.

## Technology Stack Analysis

### AI Framework: OpenAI Agents SDK

**Decision**: Use OpenAI Agents SDK for natural language processing and tool selection
**Rationale**:
- Provides robust tool calling capabilities for MCP integration
- Well-documented API for creating assistants that can call functions
- Integrates seamlessly with existing Python backend infrastructure
- Supports conversation threading and context management

**Alternatives considered**:
- LangChain: More complex for this specific use case
- Custom NLP: Would require significant development time
- Anthropic Claude: Different API structure, potentially more expensive

### MCP Tools Architecture

**Decision**: Implement MCP tools as separate Python modules
**Rationale**:
- Maintains clear separation between AI intent processing and database operations
- Enables stateless server architecture as required
- Provides structured JSON responses for consistent API behavior
- Follows the constraint that "all task operations must go through MCP tools"

### Database: Neon PostgreSQL with SQLModel

**Decision**: Continue using existing database infrastructure
**Rationale**:
- Already established in the project with proven models
- SQLModel provides excellent Python-to-SQL mapping
- Neon offers serverless scalability and familiar PostgreSQL syntax
- Supports the required data models (Task, Conversation, Message)

## MCP Tool Design Patterns

### Tool Signature Convention

**Decision**: All tools follow signature `function(user_id: str, **kwargs) -> dict`
**Rationale**:
- Consistent interface simplifies agent integration
- User_id ensures proper data isolation
- Flexible kwargs accommodate different parameter needs
- Dict return provides structured response format

### Error Handling Pattern

**Decision**: All tools return structured responses with success/error indicators
**Rationale**:
- Enables consistent error handling in the AI agent
- Provides clear feedback to users about operation outcomes
- Maintains system stability when operations fail
- Supports the requirement for graceful error handling

## API Design Considerations

### Stateless Server Architecture

**Decision**: Fetch conversation history on each request, no in-memory state
**Rationale**:
- Meets the constraint of "no in-memory conversation state"
- Ensures system reliability and scalability
- Supports server restarts without data loss
- Simplifies deployment and scaling

### Authentication Integration

**Decision**: Leverage existing Better Auth implementation
**Rationale**:
- Reuses existing authentication infrastructure
- Maintains consistency with Phase II architecture
- Reduces development time and potential security issues
- Aligns with project's security-first principle

## Frontend Integration

### ChatKit UI Selection

**Decision**: Implement OpenAI ChatKit UI for conversation interface
**Rationale**:
- Matches constraint of "ChatKit-based chat interface only"
- Provides polished user experience for conversational interfaces
- Integrates well with backend API endpoints
- Reduces custom UI development time

## Data Model Requirements

### Conversation Model Design

**Decision**: Store conversation context with user association
**Rationale**:
- Enables conversation persistence across sessions
- Supports the "conversation history persists in database" requirement
- Maintains user data isolation
- Facilitates context-aware AI responses

### Message Model Design

**Decision**: Include role-based messaging (user/assistant) with timestamps
**Rationale**:
- Supports conversation thread reconstruction
- Enables AI to understand interaction context
- Provides audit trail of user interactions
- Facilitates debugging and monitoring