'use client';

import { useState, useRef, useEffect } from 'react';
import { useAuth } from '@/src/contexts/AuthContext';
import { v4 as uuidv4 } from 'uuid';

export default function ChatPage() {
  const [messages, setMessages] = useState<Array<{
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
  }>>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [loadingState, setLoadingState] = useState<'checking' | 'authenticated' | 'unauthenticated'>('checking');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { isAuthenticated, userId, loading } = useAuth();

  // Check authentication status
  useEffect(() => {
    const checkAuth = () => {
      if (isAuthenticated && userId) {
        setLoadingState('authenticated');

        // Load conversation from localStorage
        const savedConversationId = localStorage.getItem(`chat-conversation-${userId}`);
        if (savedConversationId) {
          setConversationId(savedConversationId);

          // Load conversation history from localStorage
          const savedMessages = localStorage.getItem(`chat-messages-${savedConversationId}`);
          if (savedMessages) {
            try {
              const parsedMessages = JSON.parse(savedMessages).map((msg: { id: string; role: 'user' | 'assistant'; content: string; timestamp: string }) => ({
                ...msg,
                timestamp: new Date(msg.timestamp)
              }));
              setMessages(parsedMessages);
            } catch (e) {
              console.error('Error parsing saved messages:', e);
            }
          }
        } else {
          // Do not create a conversation ID here - let the backend handle it
          setConversationId(null);
        }
      } else {
        setLoadingState('unauthenticated');
      }
    };

    // Check auth status after component mounts
    if (!loading) {
      checkAuth();
    }

    // Listen for auth changes
    const handleStorageChange = () => {
      if (!loading) {
        checkAuth();
      }
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [isAuthenticated, userId, loading]);

  // Ensure we have a valid token before making API calls
  const ensureValidToken = () => {
    const token = localStorage.getItem('token');
    if (!token || !isAuthenticated) {
      setLoadingState('unauthenticated');
      return false;
    }
    return true;
  };

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim() || isLoading || loadingState !== 'authenticated' || !ensureValidToken()) {
      return;
    }

    // userId is already available from the context
    if (!userId) {
      return;
    }

    // Add user message to the chat
    const userMessage = {
      id: uuidv4(),
      role: 'user' as const,
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the backend API
      const token = localStorage.getItem('token');

      // Only make the request if we have a valid token
      if (!token) {
        throw new Error('No authentication token available');
      }

      // Make the initial request
      let response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          message: inputValue,
          conversation_id: conversationId || null
        }),
      });

      let isRetryAttempt = false;

      // If we get a 404 error, remove the invalid conversation ID and retry once
      if (response.status === 404) {
        console.warn('Conversation not found, resetting conversation state and retrying...');

        isRetryAttempt = true;

        // Remove the invalid conversation ID from localStorage and state
        if (conversationId) {
          localStorage.removeItem(`chat-conversation-${userId}`);
          setConversationId(null);
        }

        // Retry the request with conversation_id: null
        response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/${userId}/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            message: inputValue,
            conversation_id: null
          }),
        });
      }

      if (!response.ok) {
        // If this was a retry attempt and it failed, throw a specific error
        if (isRetryAttempt) {
          const errorText = await response.text();
          console.error('API Error after retry:', response.status, errorText);
          throw new Error(`HTTP error after retry! status: ${response.status}, message: ${errorText}`);
        } else {
          // For non-404 errors on first attempt, throw the error normally
          const errorText = await response.text();
          console.error('API Error:', response.status, errorText);
          throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }
      }

      const data = await response.json();

      // Add assistant message to the chat
      const assistantMessage = {
        id: uuidv4(),
        role: 'assistant' as const,
        content: data.response || 'Sorry, I encountered an error processing your request.',
        timestamp: new Date()
      };

      setMessages(prev => {
        const updatedMessages = [...prev, assistantMessage];

        // Save messages to localStorage with the updated message list
        // After a 404 reset, we might have a new conversation_id from the backend
        const conversationToUse = data.conversation_id || conversationId;
        if (conversationToUse) {
          localStorage.setItem(
            `chat-messages-${conversationToUse}`,
            JSON.stringify(updatedMessages)
          );
        }

        return updatedMessages;
      });

      // Save conversation to localStorage if it's a new conversation
      if (data.conversation_id && data.conversation_id !== conversationId) {
        setConversationId(data.conversation_id);
        localStorage.setItem(`chat-conversation-${userId}`, data.conversation_id);
      } else if (data.conversation_id && !conversationId) {
        // If we didn't have a conversation ID yet (e.g., after a 404 reset), save the one from the backend
        setConversationId(data.conversation_id);
        localStorage.setItem(`chat-conversation-${userId}`, data.conversation_id);
      }
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to the chat
      const errorMessage = {
        id: uuidv4(),
        role: 'assistant' as const,
        content: typeof error === 'string' ? error : (error instanceof Error ? error.message : 'Sorry, I encountered an error. Please try again.'),
        timestamp: new Date()
      };

      setMessages(prev => {
        const updatedMessages = [...prev, errorMessage];

        // Save messages to localStorage with the error message
        // Use the current conversationId (which might be null if we had a 404 and reset it)
        const conversationToUse = conversationId;
        if (conversationToUse) {
          localStorage.setItem(
            `chat-messages-${conversationToUse}`,
            JSON.stringify(updatedMessages)
          );
        }

        return updatedMessages;
      });
    } finally {
      setIsLoading(false);
    }
  };

  if (loadingState === 'checking' || loading) {
    return <div className="flex items-center justify-center h-screen bg-gray-50">Checking authentication...</div>;
  }

  if (loadingState === 'unauthenticated') {
    return <div className="flex items-center justify-center h-screen bg-gray-50">Please sign in to access the chat.</div>;
  }

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 py-3 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <h1 className="text-lg sm:text-xl font-semibold text-gray-800 flex items-center">
            <span className="bg-gradient-to-r from-blue-500 to-purple-600 text-transparent bg-clip-text">
              Todo AI Assistant
            </span>
          </h1>
          <div className="text-sm text-gray-500 hidden sm:block">
            Conversation: {conversationId?.substring(0, 8) || 'N/A'}
          </div>
        </div>
      </header>

      {/* Chat Container */}
      <div className="flex-1 overflow-hidden">
        <div className="max-w-4xl mx-auto h-full flex flex-col">
          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 pb-20">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-center px-4">
                <div className="mb-8 max-w-md">
                  <h2 className="text-xl font-semibold text-gray-800 mb-3">Welcome to Todo AI Assistant</h2>
                  <p className="text-gray-600 mb-6">Manage your tasks with natural language commands.</p>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-8">
                    <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
                      <h3 className="font-medium text-gray-800 mb-2">Examples:</h3>
                      <ul className="text-sm text-left text-gray-600 space-y-1">
                        <li className="flex items-start">
                          <span className="text-green-500 mr-2">•</span> &quot;Add a task to buy groceries&quot;
                        </li>
                        <li className="flex items-start">
                          <span className="text-green-500 mr-2">•</span> &quot;Show my tasks&quot;
                        </li>
                      </ul>
                    </div>
                    <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
                      <h3 className="font-medium text-gray-800 mb-2">&nbsp;</h3>
                      <ul className="text-sm text-left text-gray-600 space-y-1">
                        <li className="flex items-start">
                          <span className="text-green-500 mr-2">•</span> &quot;Complete task 1&quot;
                        </li>
                        <li className="flex items-start">
                          <span className="text-green-500 mr-2">•</span> &quot;Delete the meeting task&quot;
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex mb-4 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[85%] sm:max-w-[75%] rounded-2xl px-4 py-3 ${
                      message.role === 'user'
                        ? 'bg-blue-500 text-white rounded-br-none'
                        : 'bg-white text-gray-800 border border-gray-200 rounded-bl-none shadow-sm'
                    }`}
                  >
                    <div className="whitespace-pre-wrap break-words">{message.content}</div>
                    <div
                      className={`text-xs mt-1 text-right ${
                        message.role === 'user' ? 'text-blue-200' : 'text-gray-500'
                      }`}
                    >
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="flex justify-start mb-4">
                <div className="max-w-[75%] bg-white text-gray-800 border border-gray-200 rounded-2xl rounded-bl-none px-4 py-3 shadow-sm">
                  <div className="flex items-center">
                    <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce mr-1"></div>
                    <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce mr-1 delay-75"></div>
                    <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce delay-150"></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="fixed bottom-0 left-0 right-0 bg-white text-black border-t border-gray-200 p-4">
            <div className="max-w-4xl mx-auto">
              <form onSubmit={handleSubmit} className="flex gap-2">
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Message Todo AI Assistant..."
                  className="flex-1 border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
                  disabled={isLoading}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSubmit(e);
                    }
                  }}
                />
                <button
                  type="submit"
                  className="bg-blue-500 text-white rounded-xl px-5 py-3 hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200 shadow-sm min-w-[80px]"
                  disabled={isLoading || !inputValue.trim()}
                >
                  {isLoading ? (
                    <div className="flex justify-center">
                      <div className="h-2 w-2 bg-white rounded-full animate-bounce mr-1"></div>
                      <div className="h-2 w-2 bg-white rounded-full animate-bounce mr-1 delay-75"></div>
                      <div className="h-2 w-2 bg-white rounded-full animate-bounce delay-150"></div>
                    </div>
                  ) : (
                    'Send'
                  )}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}