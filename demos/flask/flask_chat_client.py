#!/usr/bin/env python3
"""
Flask Chat Client
Command-line client for interacting with the Flask chat server.
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any


class FlaskChatClient:
    """Client for interacting with the Flask chat server."""
    
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
        self.session_id = None
        self.session_stats = {}
        
    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Make HTTP request to the server."""
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return {"success": False, "error": str(e)}
    
    def health_check(self) -> bool:
        """Check if the server is healthy."""
        print("🏥 Checking server health...")
        result = self._make_request("GET", "/api/health")
        
        if result.get("success", False) or result.get("status") == "healthy":
            print("✅ Server is healthy!")
            print(f"   Active sessions: {result.get('active_sessions', 0)}")
            return True
        else:
            print("❌ Server is not responding properly")
            return False
    
    def create_session(self) -> bool:
        """Create a new chat session."""
        print("🆕 Creating new chat session...")
        result = self._make_request("POST", "/api/sessions")
        
        if result.get("success"):
            self.session_id = result["session_id"]
            self.session_stats = result["stats"]
            print(f"✅ Session created: {self.session_id}")
            return True
        else:
            print(f"❌ Failed to create session: {result.get('error')}")
            return False
    
    def send_message(self, message: str, model: str = "gpt-4.1-mini", max_tokens: int = 500, temperature: float = 0.7) -> Dict:
        """Send a message to the chat session."""
        if not self.session_id:
            print("❌ No active session. Create a session first.")
            return {"success": False, "error": "No active session"}
        
        print(f"\n📤 Sending message: {message[:50]}{'...' if len(message) > 50 else ''}")
        
        data = {
            "message": message,
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        result = self._make_request("POST", f"/api/sessions/{self.session_id}/chat", data)
        
        if result.get("success"):
            self._display_response(result)
            self.session_stats = result.get("session_stats", {})
        else:
            print(f"❌ Failed to send message: {result.get('error')}")
        
        return result
    
    def _display_response(self, result: Dict):
        """Display the response in a formatted way."""
        print(f"\n🤖 ASSISTANT RESPONSE:")
        print("=" * 50)
        
        # Show response content
        response_content = result.get("response", "")
        if response_content:
            print(f"💬 {response_content}")
        else:
            print("💬 (No text response)")
        
        # Show tool calls
        tool_calls = result.get("tool_calls", [])
        if tool_calls:
            print(f"\n🔧 TOOL CALLS DETECTED: {len(tool_calls)}")
            for i, tool_call in enumerate(tool_calls, 1):
                print(f"   {i}. {tool_call.get('name', 'Unknown')}")
                if tool_call.get('input'):
                    print(f"      Input: {tool_call['input']}")
        
        # Show tool results
        tool_results = result.get("tool_results", [])
        if tool_results:
            print(f"\n📊 TOOL RESULTS:")
            for i, result in enumerate(tool_results, 1):
                success = result.get("success", False)
                tool_name = result.get("tool_name", "Unknown")
                execution_time = result.get("execution_time", 0)
                
                status_icon = "✅" if success else "❌"
                print(f"   {i}. {status_icon} {tool_name} ({execution_time:.2f}s)")
                
                if success:
                    output_summary = result.get("output_summary", "No summary")
                    print(f"      📤 {output_summary}")
                else:
                    error = result.get("error", "Unknown error")
                    print(f"      ❌ {error}")
        
        # Show processing time
        processing_time = result.get("processing_time", 0)
        print(f"\n⏱️  Total processing time: {processing_time:.2f} seconds")
        
        # Show usage statistics
        usage = result.get("usage", {})
        if usage:
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            total_tokens = usage.get("total_tokens", 0)
            print(f"📊 Tokens: {prompt_tokens} prompt + {completion_tokens} completion = {total_tokens} total")
    
    def get_history(self) -> Dict:
        """Get conversation history."""
        if not self.session_id:
            print("❌ No active session.")
            return {"success": False, "error": "No active session"}
        
        print("📜 Getting conversation history...")
        result = self._make_request("GET", f"/api/sessions/{self.session_id}/history")
        
        if result.get("success"):
            history = result.get("history", [])
            print(f"✅ Retrieved {len(history)} messages")
            
            for i, msg in enumerate(history, 1):
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                timestamp = msg.get("timestamp", "")
                
                if role == "user":
                    print(f"   {i}. 👤 You: {content[:50]}{'...' if len(content) > 50 else ''}")
                elif role == "assistant":
                    print(f"   {i}. 🤖 Assistant: {content[:50]}{'...' if len(content) > 50 else ''}")
                    if msg.get("tool_calls"):
                        print(f"      🔧 {len(msg['tool_calls'])} tool calls made")
        else:
            print(f"❌ Failed to get history: {result.get('error')}")
        
        return result
    
    def get_stats(self) -> Dict:
        """Get session statistics."""
        if not self.session_id:
            print("❌ No active session.")
            return {"success": False, "error": "No active session"}
        
        print("📊 Getting session statistics...")
        result = self._make_request("GET", f"/api/sessions/{self.session_id}/stats")
        
        if result.get("success"):
            stats = result["stats"]
            print("✅ Session Statistics:")
            print(f"   📝 Messages exchanged: {stats.get('messages_exchanged', 0)}")
            print(f"   🔧 Tool calls made: {stats.get('tool_calls_made', 0)}")
            print(f"   🧠 Total tokens: {stats.get('total_tokens', 0)}")
            print(f"   🕐 Created: {stats.get('created_at', 'Unknown')}")
            print(f"   🕐 Last activity: {stats.get('last_activity', 'Unknown')}")
        else:
            print(f"❌ Failed to get stats: {result.get('error')}")
        
        return result
    
    def clear_history(self) -> bool:
        """Clear conversation history."""
        if not self.session_id:
            print("❌ No active session.")
            return False
        
        print("🧹 Clearing conversation history...")
        result = self._make_request("POST", f"/api/sessions/{self.session_id}/clear")
        
        if result.get("success"):
            print("✅ History cleared successfully")
            return True
        else:
            print(f"❌ Failed to clear history: {result.get('error')}")
            return False
    
    def get_available_tools(self) -> Dict:
        """Get list of available tools."""
        print("🔧 Getting available tools...")
        result = self._make_request("GET", "/api/tools")
        
        if result.get("success"):
            tools = result.get("tools", [])
            print(f"✅ Available tools ({len(tools)}):")
            for i, tool in enumerate(tools, 1):
                func = tool.get("function", {})
                name = func.get("name", "Unknown")
                description = func.get("description", "No description")
                print(f"   {i}. {name}")
                print(f"      📝 {description}")
        else:
            print(f"❌ Failed to get tools: {result.get('error')}")
        
        return result
    
    def list_sessions(self) -> Dict:
        """List all active sessions."""
        print("📋 Listing all sessions...")
        result = self._make_request("GET", "/api/sessions")
        
        if result.get("success"):
            sessions = result.get("sessions", [])
            total = result.get("total_sessions", 0)
            print(f"✅ Found {total} active sessions:")
            
            for session in sessions:
                session_id = session.get("session_id", "Unknown")
                stats = session.get("stats", {})
                messages = stats.get("messages_exchanged", 0)
                tool_calls = stats.get("tool_calls_made", 0)
                print(f"   📝 {session_id[:8]}... - {messages} messages, {tool_calls} tool calls")
        else:
            print(f"❌ Failed to list sessions: {result.get('error')}")
        
        return result
    
    def delete_session(self, session_id: str = None) -> bool:
        """Delete a session."""
        target_id = session_id or self.session_id
        
        if not target_id:
            print("❌ No session ID provided.")
            return False
        
        print(f"🗑️  Deleting session: {target_id}")
        result = self._make_request("DELETE", f"/api/sessions/{target_id}")
        
        if result.get("success"):
            print("✅ Session deleted successfully")
            if target_id == self.session_id:
                self.session_id = None
                self.session_stats = {}
            return True
        else:
            print(f"❌ Failed to delete session: {result.get('error')}")
            return False
    
    def _show_help(self):
        """Show help information."""
        print("\n📚 FLASK CHAT CLIENT HELP")
        print("=" * 50)
        print("Available commands:")
        print("  /help     - Show this help message")
        print("  /health   - Check server health")
        print("  /new      - Create new session")
        print("  /history  - Show conversation history")
        print("  /stats    - Show session statistics")
        print("  /clear    - Clear conversation history")
        print("  /tools    - Show available tools")
        print("  /sessions - List all sessions")
        print("  /delete   - Delete current session")
        print("  /quit     - Exit the client")
        print("  /exit     - Exit the client")
        print("\nExample prompts:")
        print("  • 'Get me the latest BBC news'")
        print("  • 'Find Wikipedia page for Albert Einstein'")
        print("  • 'Get BBC news summary for technology'")
        print("  • 'What's the weather like?' (no tools available)")
        print("=" * 50)
    
    def interactive_chat(self):
        """Start interactive chat mode."""
        print("🎭 FLASK CHAT CLIENT")
        print("=" * 60)
        print("Welcome to the Ultimate AI Personal Assistant (REST API Client)!")
        print("Type /help for available commands.")
        print("Type /quit to exit.")
        print("=" * 60)
        
        # Check server health first
        if not self.health_check():
            print("❌ Cannot connect to server. Make sure the Flask server is running.")
            return
        
        # Create a session
        if not self.create_session():
            print("❌ Failed to create session. Exiting.")
            return
        
        while True:
            try:
                # Get user input
                user_input = input("\n👤 You: ").strip()
                
                # Handle commands
                if user_input.lower() in ['/quit', '/exit']:
                    print("\n👋 Goodbye! Thanks for chatting!")
                    break
                elif user_input.lower() == '/help':
                    self._show_help()
                    continue
                elif user_input.lower() == '/health':
                    self.health_check()
                    continue
                elif user_input.lower() == '/new':
                    self.create_session()
                    continue
                elif user_input.lower() == '/history':
                    self.get_history()
                    continue
                elif user_input.lower() == '/stats':
                    self.get_stats()
                    continue
                elif user_input.lower() == '/clear':
                    self.clear_history()
                    continue
                elif user_input.lower() == '/tools':
                    self.get_available_tools()
                    continue
                elif user_input.lower() == '/sessions':
                    self.list_sessions()
                    continue
                elif user_input.lower() == '/delete':
                    self.delete_session()
                    continue
                elif not user_input:
                    continue
                
                # Send message
                self.send_message(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Chat interrupted. Goodbye!")
                break
            except EOFError:
                print("\n\n👋 End of input. Goodbye!")
                break


def main():
    """Main function to start the interactive chat client."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Flask Chat Client")
    parser.add_argument("--url", default="http://localhost:5001", 
                       help="Base URL of the Flask server (default: http://localhost:5001)")
    parser.add_argument("--command", choices=["health", "new", "tools", "sessions"], 
                       help="Run a single command and exit")
    parser.add_argument("--message", help="Send a single message (requires --command)")
    parser.add_argument("--session-id", help="Session ID for single commands")
    
    args = parser.parse_args()
    
    client = FlaskChatClient(args.url)
    
    if args.command:
        # Single command mode
        if args.command == "health":
            client.health_check()
        elif args.command == "new":
            client.create_session()
        elif args.command == "tools":
            client.get_available_tools()
        elif args.command == "sessions":
            client.list_sessions()
        elif args.command == "chat" and args.message:
            if not args.session_id:
                print("❌ Session ID required for chat command")
                return
            client.session_id = args.session_id
            client.send_message(args.message)
    else:
        # Interactive mode
        client.interactive_chat()


if __name__ == "__main__":
    main() 