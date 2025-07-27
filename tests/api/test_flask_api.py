#!/usr/bin/env python3
"""
Test Flask API
Demonstration script showing how to use the Flask chat server API.
"""

import requests
import json
import time
from datetime import datetime


class FlaskAPITester:
    """Test class for demonstrating Flask API usage."""
    
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
        self.session_id = None
    
    def _make_request(self, method: str, endpoint: str, data: dict = None) -> dict:
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
    
    def test_health_check(self):
        """Test health check endpoint."""
        print("🏥 Testing health check...")
        result = self._make_request("GET", "/api/health")
        print(f"Result: {json.dumps(result, indent=2)}")
        return result
    
    def test_create_session(self):
        """Test session creation."""
        print("\n🆕 Testing session creation...")
        result = self._make_request("POST", "/api/sessions")
        print(f"Result: {json.dumps(result, indent=2)}")
        
        if result.get("success"):
            self.session_id = result["session_id"]
            print(f"✅ Session created: {self.session_id}")
        
        return result
    
    def test_get_tools(self):
        """Test getting available tools."""
        print("\n🔧 Testing get available tools...")
        result = self._make_request("GET", "/api/tools")
        print(f"Result: {json.dumps(result, indent=2)}")
        return result
    
    def test_send_message(self, message: str, model: str = "gpt-4.1-mini"):
        """Test sending a message."""
        if not self.session_id:
            print("❌ No session ID available")
            return None
        
        print(f"\n📤 Testing send message: {message}")
        data = {
            "message": message,
            "model": model,
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        result = self._make_request("POST", f"/api/sessions/{self.session_id}/chat", data)
        print(f"Result: {json.dumps(result, indent=2)}")
        return result
    
    def test_get_history(self):
        """Test getting conversation history."""
        if not self.session_id:
            print("❌ No session ID available")
            return None
        
        print("\n📜 Testing get conversation history...")
        result = self._make_request("GET", f"/api/sessions/{self.session_id}/history")
        print(f"Result: {json.dumps(result, indent=2)}")
        return result
    
    def test_get_stats(self):
        """Test getting session statistics."""
        if not self.session_id:
            print("❌ No session ID available")
            return None
        
        print("\n📊 Testing get session statistics...")
        result = self._make_request("GET", f"/api/sessions/{self.session_id}/stats")
        print(f"Result: {json.dumps(result, indent=2)}")
        return result
    
    def test_list_sessions(self):
        """Test listing all sessions."""
        print("\n📋 Testing list all sessions...")
        result = self._make_request("GET", "/api/sessions")
        print(f"Result: {json.dumps(result, indent=2)}")
        return result
    
    def test_clear_history(self):
        """Test clearing conversation history."""
        if not self.session_id:
            print("❌ No session ID available")
            return None
        
        print("\n🧹 Testing clear conversation history...")
        result = self._make_request("POST", f"/api/sessions/{self.session_id}/clear")
        print(f"Result: {json.dumps(result, indent=2)}")
        return result
    
    def test_delete_session(self):
        """Test deleting the session."""
        if not self.session_id:
            print("❌ No session ID available")
            return None
        
        print(f"\n🗑️  Testing delete session: {self.session_id}")
        result = self._make_request("DELETE", f"/api/sessions/{self.session_id}")
        print(f"Result: {json.dumps(result, indent=2)}")
        
        if result.get("success"):
            self.session_id = None
        
        return result
    
    def run_full_test(self):
        """Run a complete test of all API endpoints."""
        print("🚀 Starting Flask API Test Suite")
        print("=" * 60)
        
        # Test 1: Health check
        self.test_health_check()
        
        # Test 2: Get available tools
        self.test_get_tools()
        
        # Test 3: Create session
        self.test_create_session()
        
        if not self.session_id:
            print("❌ Failed to create session. Stopping tests.")
            return
        
        # Test 4: Send a message that should trigger tool calls
        self.test_send_message("Get me the latest BBC news")
        
        # Test 5: Send another message
        self.test_send_message("Find Wikipedia page for Albert Einstein")
        
        # Test 6: Get conversation history
        self.test_get_history()
        
        # Test 7: Get session statistics
        self.test_get_stats()
        
        # Test 8: List all sessions
        self.test_list_sessions()
        
        # Test 9: Clear history
        self.test_clear_history()
        
        # Test 10: Get history after clearing
        self.test_get_history()
        
        # Test 11: Delete session
        self.test_delete_session()
        
        print("\n✅ Test suite completed!")


def test_specific_scenarios():
    """Test specific scenarios with different message types."""
    print("\n🎯 Testing Specific Scenarios")
    print("=" * 60)
    
    tester = FlaskAPITester()
    
    # Create a session
    tester.test_create_session()
    if not tester.session_id:
        print("❌ Failed to create session. Stopping scenario tests.")
        return
    
    # Scenario 1: Message that should trigger BBC news tool
    print("\n📰 Scenario 1: BBC News Request")
    tester.test_send_message("Get me the latest BBC news headlines")
    
    # Scenario 2: Message that should trigger Wikipedia tool
    print("\n📚 Scenario 2: Wikipedia Request")
    tester.test_send_message("Find Wikipedia page for Donald Trump")
    
    # Scenario 3: Message that should trigger both tools
    print("\n🔄 Scenario 3: Multi-tool Request")
    tester.test_send_message("Get BBC news and find Wikipedia pages for the first 3 people mentioned")
    
    # Scenario 4: Message that doesn't need tools
    print("\n💬 Scenario 4: General Conversation")
    tester.test_send_message("Hello, how are you today?")
    
    # Scenario 5: Message with specific parameters
    print("\n⚙️  Scenario 5: Parameterized Request")
    tester.test_send_message("Get BBC news summary for technology category with maximum 5 articles")
    
    # Clean up
    tester.test_delete_session()
    
    print("\n✅ Scenario tests completed!")


def main():
    """Main function to run tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Flask API Tester")
    parser.add_argument("--url", default="http://localhost:5001", 
                       help="Base URL of the Flask server (default: http://localhost:5001)")
    parser.add_argument("--scenarios", action="store_true", 
                       help="Run specific scenario tests")
    parser.add_argument("--full", action="store_true", 
                       help="Run full test suite")
    
    args = parser.parse_args()
    
    if args.scenarios:
        test_specific_scenarios()
    elif args.full:
        tester = FlaskAPITester(args.url)
        tester.run_full_test()
    else:
        print("Please specify --scenarios or --full to run tests")
        print("Example:")
        print("  python test_flask_api.py --scenarios")
        print("  python test_flask_api.py --full")


if __name__ == "__main__":
    main() 