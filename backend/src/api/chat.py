from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import Optional, List
import uuid
import json
from datetime import datetime

from ..database.session import get_session
from ..models.message import Message, MessageCreate
from ..models.conversation import Conversation, ConversationCreate
from ..models.chat import ChatRequest, ChatResponse
from ..services.agent_service import get_todo_agent
from ..api.deps import get_current_user
from ..models.user import User


router = APIRouter(tags=["chat"])


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    message_data: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Main chat endpoint that handles natural language requests from users,
    processes them through the AI agent, and returns structured responses.
    """
    # Verify that the user_id in the path matches the authenticated user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user's chat")
    """
    Main chat endpoint that handles natural language requests from users,
    processes them through the AI agent, and returns structured responses.

    Args:
        user_id: The UUID of the authenticated user
        message_data: Contains 'message' and optional 'conversation_id'
        session: Database session for queries

    Returns:
        Structured response with conversation ID and AI response
    """
    try:
        # Validate user_id format
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid user_id format")

        # Verify that the user_id in the path matches the authenticated user
        if str(current_user.id) != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this user's chat")

        # Verify that the current_user object is valid
        if not current_user or not current_user.id:
            raise HTTPException(status_code=401, detail="Invalid user session")

        # Extract message and conversation_id from request
        user_message = message_data.message.strip()
        if not user_message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        conversation_id_str = message_data.conversation_id

        # Get or create conversation
        if conversation_id_str:
            try:
                conversation_id = uuid.UUID(conversation_id_str)
                # Verify conversation exists and belongs to user
                conversation = session.get(Conversation, conversation_id)
                if not conversation or str(conversation.user_id) != user_id:
                    raise HTTPException(status_code=404, detail="Conversation not found")
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid conversation_id format")
        else:
            # Create new conversation
            conversation = Conversation(
                user_id=user_uuid,
                title=f"Chat started {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        # Save user message to database
        user_message_obj = Message(
            conversation_id=conversation.id,
            user_id=user_uuid,
            role="user",
            content=user_message,
            created_at=datetime.now()
        )
        session.add(user_message_obj)
        session.commit()
        session.refresh(user_message_obj)

        # Fetch conversation history for context
        conversation_history = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at)
        ).all()

        # Format history for the agent
        formatted_history = []
        for msg in conversation_history[:-1]:  # Exclude the current message
            formatted_history.append({
                "role": msg.role,
                "content": msg.content
            })

        # Get the AI agent and process the request
        agent = get_todo_agent()
        agent_response = agent.process_request(
            user_input=user_message,
            user_id=user_id,
            conversation_history=formatted_history
        )

        # Extract the assistant's reply
        assistant_reply = agent_response.get("response", "I'm sorry, I couldn't process that request.")

        # Create and save assistant message
        assistant_message = Message(
            conversation_id=conversation.id,
            user_id=user_uuid,  # For assistant messages, this could be NULL or a system ID
            role="assistant",
            content=assistant_reply,
            created_at=datetime.now(),
            tool_calls=json.dumps(agent_response.get("tool_calls", [])) if agent_response.get("tool_calls") else None,
            tool_responses=json.dumps(agent_response.get("tool_results", [])) if agent_response.get("tool_results") else None
        )
        session.add(assistant_message)
        session.commit()
        session.refresh(assistant_message)

        # Prepare response
        response_data = {
            "success": True,
            "conversation_id": str(conversation.id),
            "response": assistant_reply,
            "timestamp": datetime.now().isoformat()
        }

        # Add operation details if available
        if agent_response.get("tool_calls"):
            response_data["operation"] = {
                "type": agent_response["tool_calls"][0]["name"] if agent_response["tool_calls"] else "unknown",
                "result": agent_response.get("tool_results", [{}])[0] if agent_response.get("tool_results") else {}
            }

        return response_data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Additional utility endpoints for testing and management

@router.get("/{user_id}/conversations")
async def list_user_conversations(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    List all conversations for a specific user.
    """
    try:
        user_uuid = uuid.UUID(user_id)

        # Verify that the user_id in the path matches the authenticated user
        if str(current_user.id) != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this user's conversations")

        conversations = session.exec(
            select(Conversation)
            .where(Conversation.user_id == user_uuid)
            .order_by(Conversation.updated_at.desc())
        ).all()

        return {
            "success": True,
            "conversations": [
                {
                    "id": str(conv.id),
                    "title": conv.title,
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat()
                } for conv in conversations
            ]
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving conversations: {str(e)}")


@router.get("/{user_id}/conversation/{conversation_id}/messages")
async def get_conversation_messages(
    user_id: str,
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all messages for a specific conversation.
    """
    try:
        user_uuid = uuid.UUID(user_id)
        conv_uuid = uuid.UUID(conversation_id)

        # Verify that the user_id in the path matches the authenticated user
        if str(current_user.id) != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this user's conversations")

        # Verify conversation belongs to user
        conversation = session.get(Conversation, conv_uuid)
        if not conversation or str(conversation.user_id) != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")

        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conv_uuid)
            .order_by(Message.created_at)
        ).all()

        return {
            "success": True,
            "messages": [
                {
                    "id": str(msg.id),
                    "role": msg.role,
                    "content": msg.content,
                    "created_at": msg.created_at.isoformat(),
                    "tool_calls": msg.tool_calls,
                    "tool_responses": msg.tool_responses
                } for msg in messages
            ]
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving messages: {str(e)}")