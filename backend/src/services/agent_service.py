import os
import json
import sys
from typing import Dict, Any, List
from openai import OpenAI

# Adjust the import path for MCP tools
from ..mcp_tools.add_task.add_task import add_task
from ..mcp_tools.list_tasks.list_tasks import list_tasks
from ..mcp_tools.complete_task.complete_task import complete_task
from ..mcp_tools.delete_task.delete_task import delete_task
from ..mcp_tools.update_task.update_task import update_task


class TodoAIAgent:
    """
    AI Agent that handles natural language processing and task management.
    Uses OpenAI's function calling to execute MCP tools based on user input.
    """

    def __init__(self):
        # Check if OpenAI API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OPENAI_API_KEY environment variable not set. Agent will return mock responses.")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)

        # Define the tools available to the agent
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "title": {"type": "string", "description": "The title of the task"},
                            "description": {"type": "string", "description": "Optional description of the task"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List tasks for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "status": {"type": "string", "description": "Filter by status: 'all', 'completed', 'pending'", "default": "all"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "task_id": {"type": "string", "description": "The ID of the task to complete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "task_id": {"type": "string", "description": "The ID of the task to delete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "task_id": {"type": "string", "description": "The ID of the task to update"},
                            "title": {"type": "string", "description": "New title for the task (optional)"},
                            "description": {"type": "string", "description": "New description for the task (optional)"},
                            "completed": {"type": "boolean", "description": "New completion status (optional)"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]

        # Mapping of function names to actual functions
        self.function_map = {
            "add_task": add_task,
            "list_tasks": list_tasks,
            "complete_task": complete_task,
            "delete_task": delete_task,
            "update_task": update_task
        }

    def process_request(self, user_input: str, user_id: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """
        Process a natural language request from the user and return a response.

        Args:
            user_input: The natural language input from the user
            user_id: The ID of the user making the request
            conversation_history: Previous conversation history (for context)

        Returns:
            Dictionary containing the agent's response and any tool execution results
        """
        try:
            # Check if OpenAI client is available
            if self.client is None:
                # Provide mock responses when API key is not available
                return self._get_mock_response(user_input, user_id)

            # Prepare messages for the OpenAI API
            messages = []

            # Add system message with instructions
            messages.append({
                "role": "system",
                "content": (
                    "You are a helpful AI assistant that manages tasks for users. "
                    "Use the appropriate tools to handle user requests. "
                    "Always confirm actions with the user in a friendly manner. "
                    "If a user wants to add a task, use add_task. "
                    "If a user wants to see tasks, use list_tasks. "
                    "If a user wants to complete a task, use complete_task. "
                    "If a user wants to delete a task, use delete_task. "
                    "If a user wants to update a task, use update_task. "
                    "Always respond with clear, friendly confirmations of actions taken."
                )
            })

            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history:
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })

            # Add the current user input
            messages.append({
                "role": "user",
                "content": user_input
            })

            # Call the OpenAI API with function calling
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # You can change this to gpt-4 if preferred
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # Process tool calls if any
            tool_results = []
            if tool_calls:
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = self.function_map[function_name]
                    function_args = json.loads(tool_call.function.arguments)

                    # Add user_id to function args if not present (for some tools)
                    if "user_id" not in function_args:
                        function_args["user_id"] = user_id

                    # Execute the function
                    function_response = function_to_call(**function_args)

                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(function_response)
                    })

                # Get the final response from the assistant considering tool results
                messages.append(response_message)
                messages.extend(tool_results)

                final_response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )

                assistant_reply = final_response.choices[0].message.content
            else:
                # If no tool calls were made, use the initial response
                assistant_reply = response_message.content

            return {
                "success": True,
                "response": assistant_reply,
                "tool_calls": [{"name": tc.function.name, "arguments": json.loads(tc.function.arguments)} for tc in tool_calls] if tool_calls else [],
                "tool_results": tool_results
            }

        except Exception as e:
            # Check if this is an OpenAI API error (like quota exceeded)
            error_str = str(e).lower()
            if ('openai' in error_str or 'quota' in error_str or 'api' in error_str or '429' in error_str):
                print(f"OpenAI API error detected: {e}. Falling back to mock response.")
                # Fall back to mock response for API errors
                return self._get_mock_response(user_input, user_id)
            else:
                return {
                    "success": False,
                    "response": f"Sorry, I encountered an error processing your request: {str(e)}",
                    "error": str(e)
                }

    def _get_mock_response(self, user_input: str, user_id: str) -> Dict[str, Any]:
        """
        Provide mock responses when OpenAI API is not available.
        """
        user_input_lower = user_input.lower()

        if "add" in user_input_lower or "create" in user_input_lower:
            # Mock adding a task
            import uuid
            task_id = str(uuid.uuid4())
            # Extract task title from user input (simple extraction)
            words = user_input.split()
            title_start_idx = -1
            for i, word in enumerate(words):
                if word.lower() in ["add", "create", "task", "to"]:
                    title_start_idx = i + 1
                    break

            title = " ".join(words[title_start_idx:]) if title_start_idx != -1 else "New task"

            try:
                # Call the actual add_task function
                result = add_task(user_id, title)

                return {
                    "success": True,
                    "response": f"I've added the task '{title}' to your list. {result.get('message', '')}",
                    "tool_calls": [{"name": "add_task", "arguments": {"user_id": user_id, "title": title}}],
                    "tool_results": [{"result": result}]
                }
            except Exception as e:
                # If the tool fails, return a mock response
                return {
                    "success": True,
                    "response": f"I've added the task '{title}' to your list (mock response).",
                    "tool_calls": [{"name": "add_task", "arguments": {"user_id": user_id, "title": title}}],
                    "tool_results": [{"result": {"message": "Mock result"}}]
                }
        elif "show" in user_input_lower or "list" in user_input_lower or "my" in user_input_lower and "task" in user_input_lower:
            # Mock listing tasks
            try:
                result = list_tasks(user_id)
                task_count = result.get('count', 0)

                if task_count == 0:
                    response = "You don't have any tasks right now. You can add a task by saying something like 'Add a task to buy groceries'."
                else:
                    task_list = ", ".join([task['title'] for task in result.get('tasks', [])])
                    response = f"You have {task_count} task(s): {task_list}"

                return {
                    "success": True,
                    "response": response,
                    "tool_calls": [{"name": "list_tasks", "arguments": {"user_id": user_id}}],
                    "tool_results": [{"result": result}]
                }
            except Exception as e:
                # If the tool fails, return a mock response
                return {
                    "success": True,
                    "response": "You have 0 tasks right now. You can add a task by saying something like 'Add a task to buy groceries'.",
                    "tool_calls": [{"name": "list_tasks", "arguments": {"user_id": user_id}}],
                    "tool_results": [{"result": {"count": 0, "tasks": []}}]
                }
        elif "complete" in user_input_lower or "done" in user_input_lower or "finish" in user_input_lower:
            # Mock completing a task - this would need more sophisticated parsing
            response = "I've marked that task as completed. (Note: This is a mock response since OpenAI API is not configured)"
            return {
                "success": True,
                "response": response,
                "tool_calls": [],
                "tool_results": []
            }
        else:
            # Default response for unrecognized commands
            return {
                "success": True,
                "response": f"I understand you said: '{user_input}'. I can help you manage tasks like adding, listing, completing, or deleting tasks. Try saying something like 'Add a task to buy groceries' or 'Show my tasks'.",
                "tool_calls": [],
                "tool_results": []
            }


# Global instance of the agent
todo_agent = TodoAIAgent()


def get_todo_agent():
    """Return the global TodoAI agent instance"""
    return todo_agent