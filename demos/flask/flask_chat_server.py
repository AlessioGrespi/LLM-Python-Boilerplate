#!/usr/bin/env python3
"""
Flask Chat Server
REST API server for interactive chat with tool calling functionality.
"""

import sys
import os
import json
import time
import uuid
from datetime import datetime
from typing import Dict, List, Any
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add the necessary paths
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src', 'core'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools', 'tool_modules'))

from model_router import model_router
from bbc_rss import get_bbc_public_figures, bbc_rss_tool
from wikipedia_api import find_person_wikipedia_page, wikipedia_api_tool

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for sessions (in production, use Redis or database)
sessions = {}

class ChatSession:
    """Represents a chat session with conversation history and statistics."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.conversation_history = []
        self.tool_calls_made = 0
        self.total_tokens = 0
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        
        # Define available tools
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_bbc_latest_news",
                    "description": "Get the latest BBC news headlines and summaries",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_bbc_news_summary",
                    "description": "Get a summary of current BBC news with categorized articles",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "description": "Filter by category (e.g., 'politics', 'technology', 'sports', 'business')"
                            },
                            "max_articles": {
                                "type": "integer",
                                "description": "Maximum number of articles to return",
                                "default": 10
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "find_person_wikipedia_page",
                    "description": "Find Wikipedia page for a specific person",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "person_name": {
                                "type": "string",
                                "description": "Name of the person to search for"
                            }
                        },
                        "required": ["person_name"]
                    }
                }
            }
        ]
        
        # Tool function mapping
        self.tool_functions = {
            "get_bbc_latest_news": self._execute_bbc_latest_news,
            "get_bbc_news_summary": self._execute_bbc_news_summary,
            "find_person_wikipedia_page": self._execute_wikipedia_tool
        }
    
    def _execute_bbc_latest_news(self, **kwargs):
        """Execute BBC latest news tool."""
        start_time = time.time()
        try:
            from bbc_rss import get_bbc_latest_news
            result = get_bbc_latest_news()
            execution_time = time.time() - start_time
            
            return {
                "success": True,
                "result": result,
                "execution_time": execution_time,
                "tool_name": "get_bbc_latest_news",
                "input": kwargs,
                "output_summary": f"BBC Latest News ({result['total_articles']} articles)"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "execution_time": time.time() - start_time,
                "tool_name": "get_bbc_latest_news",
                "input": kwargs
            }

    def _execute_bbc_news_summary(self, **kwargs):
        """Execute BBC news summary tool."""
        category = kwargs.get('category')
        max_articles = kwargs.get('max_articles', 10)
        
        start_time = time.time()
        try:
            from bbc_rss import get_bbc_news_summary
            result = get_bbc_news_summary(category, max_articles)
            execution_time = time.time() - start_time
            
            return {
                "success": True,
                "result": result,
                "execution_time": execution_time,
                "tool_name": "get_bbc_news_summary",
                "input": kwargs,
                "output_summary": f"BBC News Summary ({result['total_articles']} articles)"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "execution_time": time.time() - start_time,
                "tool_name": "get_bbc_news_summary",
                "input": kwargs
            }
    
    def _execute_wikipedia_tool(self, **kwargs):
        """Execute Wikipedia tool."""
        person_name = kwargs.get('person_name', '')
        
        start_time = time.time()
        try:
            result = find_person_wikipedia_page(person_name)
            execution_time = time.time() - start_time
            
            if result.get('success'):
                page_info = result['page_info']
                output_summary = f"Found Wikipedia page: {page_info['title']}"
            else:
                output_summary = f"No Wikipedia page found for: {person_name}"
            
            return {
                "success": True,
                "result": result,
                "execution_time": execution_time,
                "tool_name": "find_person_wikipedia_page",
                "input": kwargs,
                "output_summary": output_summary
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "execution_time": time.time() - start_time,
                "tool_name": "find_person_wikipedia_page",
                "input": kwargs
            }
    
    def _execute_tool_call(self, tool_call):
        """Execute a tool call and return the result."""
        # Handle different tool call formats (AWS Bedrock vs Azure OpenAI)
        if hasattr(tool_call, 'function'):
            # Azure OpenAI format
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
        else:
            # AWS Bedrock format
            tool_name = tool_call.get('name', '')
            tool_args = tool_call.get('input', {})
        
        if tool_name in self.tool_functions:
            return self.tool_functions[tool_name](**tool_args)
        else:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}",
                "tool_name": tool_name,
                "input": tool_args
            }
    
    def process_message(self, message: str, model: str = "gpt-4.1-mini", max_tokens: int = 500, temperature: float = 0.7):
        """Process a user message and return the response."""
        self.last_activity = datetime.now()
        
        # Add to conversation history (provider-agnostic format)
        self.conversation_history.append({
            "role": "user", 
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Make API call
        start_time = time.time()
        
        try:
            response = model_router(
                prompt=message,
                model=model,
                messages=self.conversation_history,
                tools=self.tools,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            processing_time = time.time() - start_time
            
            # Extract usage statistics from initial response
            usage = response.get('usage', {})
            if usage:
                self.total_tokens += usage.get('total_tokens', 0)
            
            # Handle tool calls
            tool_calls = response.get('tool_calls', [])
            tool_results = []
            
            if tool_calls:
                self.tool_calls_made += len(tool_calls)
                
                # Add tool calls to conversation history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response.get('content', ''),
                    "tool_calls": tool_calls,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Execute tools and add results to conversation history
                for tool_call in tool_calls:
                    result = self._execute_tool_call(tool_call)
                    tool_results.append(result)
                    
                    # Handle different tool call formats for ID extraction
                    if hasattr(tool_call, 'id'):
                        # Azure OpenAI format
                        tool_call_id = tool_call.id
                    else:
                        # AWS Bedrock format
                        tool_call_id = tool_call.get('id', '')
                    
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": json.dumps(result, indent=2),
                        "timestamp": datetime.now().isoformat()
                    })
                
                # Make follow-up call with tool results
                if tool_results:
                    try:
                        follow_up_response = model_router(
                            prompt="",  # No new prompt needed
                            model=model,
                            messages=self.conversation_history,
                            tools=self.tools,
                            max_tokens=max_tokens,
                            temperature=temperature
                        )
                        
                        # Add follow-up response to conversation history
                        self.conversation_history.append({
                            "role": "assistant",
                            "content": follow_up_response.get('content', ''),
                            "timestamp": datetime.now().isoformat(),
                            "follow_up": True
                        })
                        
                        # Update usage statistics for follow-up
                        follow_up_usage = follow_up_response.get('usage', {})
                        if follow_up_usage:
                            self.total_tokens += follow_up_usage.get('total_tokens', 0)
                        
                        # Return the follow-up response instead
                        return {
                            "success": True,
                            "response": follow_up_response.get('content', ''),
                            "tool_calls": tool_calls,
                            "tool_results": tool_results,
                            "processing_time": processing_time,
                            "usage": usage,
                            "follow_up_usage": follow_up_usage,
                            "session_stats": self.get_stats()
                        }
                        
                    except Exception as follow_up_error:
                        # If follow-up fails, continue with original response
                        print(f"Follow-up call failed: {follow_up_error}")
            
            # Add assistant response to history (if no tool calls or follow-up failed)
            if not tool_calls:
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response.get('content', ''),
                    "timestamp": datetime.now().isoformat()
                })
            
            return {
                "success": True,
                "response": response.get('content', ''),
                "tool_calls": tool_calls,
                "tool_results": tool_results,
                "processing_time": processing_time,
                "usage": usage,
                "session_stats": self.get_stats()
            }
            
        except Exception as e:
            error_response = {
                "success": False,
                "error": str(e),
                "processing_time": time.time() - start_time
            }
            
            self.conversation_history.append({
                "role": "assistant",
                "content": f"Error: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "error": True
            })
            
            return error_response
    
    def get_stats(self):
        """Get session statistics."""
        return {
            "session_id": self.session_id,
            "messages_exchanged": len(self.conversation_history),
            "tool_calls_made": self.tool_calls_made,
            "total_tokens": self.total_tokens,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat()
        }
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        self.tool_calls_made = 0
        self.total_tokens = 0
        self.last_activity = datetime.now()
        return {"success": True, "message": "Conversation history cleared"}


def get_or_create_session(session_id: str = None) -> ChatSession:
    """Get existing session or create a new one."""
    if session_id is None:
        session_id = str(uuid.uuid4())
    
    if session_id not in sessions:
        sessions[session_id] = ChatSession(session_id)
    
    return sessions[session_id]


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_sessions": len(sessions)
    })


@app.route('/api/sessions', methods=['POST'])
def create_session():
    """Create a new chat session."""
    session_id = str(uuid.uuid4())
    session = get_or_create_session(session_id)
    
    return jsonify({
        "success": True,
        "session_id": session_id,
        "message": "Session created successfully",
        "stats": session.get_stats()
    })


@app.route('/api/sessions/<session_id>/chat', methods=['POST'])
def chat(session_id):
    """Send a message to the chat session."""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                "success": False,
                "error": "Message is required"
            }), 400
        
        message = data['message']
        model = data.get('model', 'mistral-small')
        max_tokens = data.get('max_tokens', 500)
        temperature = data.get('temperature', 0.7)
        
        session = get_or_create_session(session_id)
        result = session.process_message(message, model, max_tokens, temperature)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/sessions/<session_id>/history', methods=['GET'])
def get_history(session_id):
    """Get conversation history for a session."""
    try:
        session = get_or_create_session(session_id)
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "history": session.conversation_history,
            "stats": session.get_stats()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/sessions/<session_id>/clear', methods=['POST'])
def clear_history(session_id):
    """Clear conversation history for a session."""
    try:
        session = get_or_create_session(session_id)
        result = session.clear_history()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/sessions/<session_id>/stats', methods=['GET'])
def get_stats(session_id):
    """Get session statistics."""
    try:
        session = get_or_create_session(session_id)
        
        return jsonify({
            "success": True,
            "stats": session.get_stats()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/tools', methods=['GET'])
def get_available_tools():
    """Get list of available tools."""
    try:
        # Use a temporary session to get tools
        temp_session = ChatSession("temp")
        
        return jsonify({
            "success": True,
            "tools": temp_session.tools
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/sessions', methods=['GET'])
def list_sessions():
    """List all active sessions."""
    try:
        session_list = []
        for session_id, session in sessions.items():
            session_list.append({
                "session_id": session_id,
                "stats": session.get_stats()
            })
        
        return jsonify({
            "success": True,
            "sessions": session_list,
            "total_sessions": len(sessions)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete a session."""
    try:
        if session_id in sessions:
            del sessions[session_id]
            return jsonify({
                "success": True,
                "message": f"Session {session_id} deleted successfully"
            })
        else:
            return jsonify({
                "success": False,
                "error": f"Session {session_id} not found"
            }), 404
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    print("🚀 Starting Flask Chat Server...")
    print("=" * 50)
    print("Available endpoints:")
    print("  GET  /api/health              - Health check")
    print("  POST /api/sessions            - Create new session")
    print("  GET  /api/sessions            - List all sessions")
    print("  POST /api/sessions/<id>/chat  - Send message")
    print("  GET  /api/sessions/<id>/history - Get conversation history")
    print("  POST /api/sessions/<id>/clear - Clear history")
    print("  GET  /api/sessions/<id>/stats - Get session stats")
    print("  DELETE /api/sessions/<id>     - Delete session")
    print("  GET  /api/tools               - Get available tools")
    print("=" * 50)
    print("Server will start on http://localhost:5001")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5001) 