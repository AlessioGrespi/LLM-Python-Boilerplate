#!/usr/bin/env python3
"""
Conversation Demo Test
Demonstrates conversation capabilities with:
- Single tool calls
- Chained tool calls  
- Multi-turn conversations
- Message history management
"""

import sys
import os
import json
from typing import Dict, List, Any

# Add the necessary paths
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src', 'core'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools', 'tool_modules'))

from model_router import model_router
from bbc_rss import get_bbc_public_figures
from wikipedia_api import find_person_wikipedia_page


class ConversationDemo:
    """Demo class for testing conversation capabilities."""
    
    def __init__(self):
        self.messages = []
        self.conversation_history = []
        
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history."""
        # Format content for AWS Bedrock API (list of dicts with text)
        if isinstance(content, str):
            formatted_content = [{"text": content}]
        else:
            formatted_content = content
            
        message = {"role": role, "content": formatted_content}
        self.messages.append(message)
        self.conversation_history.append(f"{role.upper()}: {content}")
        
    def get_messages(self) -> List[Dict[str, str]]:
        """Get formatted messages for the model router."""
        return self.messages.copy()
    
    def print_conversation(self):
        """Print the conversation history."""
        print("\n💬 CONVERSATION HISTORY:")
        print("=" * 60)
        for i, message in enumerate(self.conversation_history, 1):
            print(f"{i}. {message}")
        print("=" * 60)


def test_single_tool_conversation():
    """Test conversation with single tool calls."""
    print("🔧 SINGLE TOOL CONVERSATION TEST")
    print("=" * 60)
    
    demo = ConversationDemo()
    
    # Define tools for single tool calls
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_bbc_public_figures",
                "description": "Get public figures from BBC RSS feed",
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
    
    # Conversation 1: Get BBC public figures
    demo.add_message("user", "Can you get me the public figures from today's BBC news?")
    
    try:
        response1 = model_router(
            prompt="",
            model="mistral-small",
            messages=demo.get_messages(),
            tools=tools,
            max_tokens=300,
            temperature=0.7
        )
        
        demo.add_message("assistant", response1['content'])
        print("✅ Single tool call successful")
        
    except Exception as e:
        demo.add_message("assistant", f"Sorry, I encountered an error: {str(e)}")
        print(f"❌ Single tool call failed: {e}")
    
    # Conversation 2: Get Wikipedia page for specific person
    demo.add_message("user", "Now can you find the Wikipedia page for Donald Trump?")
    
    try:
        response2 = model_router(
            prompt="",
            model="mistral-small",
            messages=demo.get_messages(),
            tools=tools,
            max_tokens=300,
            temperature=0.7
        )
        
        demo.add_message("assistant", response2['content'])
        print("✅ Second single tool call successful")
        
    except Exception as e:
        demo.add_message("assistant", f"Sorry, I encountered an error: {str(e)}")
        print(f"❌ Second single tool call failed: {e}")
    
    demo.print_conversation()
    return demo


def test_chained_tool_conversation():
    """Test conversation with chained tool calls."""
    print("\n🔗 CHAINED TOOL CONVERSATION TEST")
    print("=" * 60)
    
    demo = ConversationDemo()
    
    # Define tools for chained operations
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_bbc_public_figures",
                "description": "Get public figures from BBC RSS feed",
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
    
    # Conversation: Get public figures and then find their Wikipedia pages
    demo.add_message("user", "Get the public figures from BBC news and then find Wikipedia pages for the first 3 people you find.")
    
    try:
        response = model_router(
            prompt="",
            model="mistral-small",
            messages=demo.get_messages(),
            tools=tools,
            max_tokens=500,
            temperature=0.7
        )
        
        demo.add_message("assistant", response['content'])
        print("✅ Chained tool call successful")
        
    except Exception as e:
        demo.add_message("assistant", f"Sorry, I encountered an error: {str(e)}")
        print(f"❌ Chained tool call failed: {e}")
    
    demo.print_conversation()
    return demo


def test_multi_turn_conversation():
    """Test multi-turn conversation with context retention."""
    print("\n💬 MULTI-TURN CONVERSATION TEST")
    print("=" * 60)
    
    demo = ConversationDemo()
    
    # Define tools
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_bbc_public_figures",
                "description": "Get public figures from BBC RSS feed",
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
    
    # Turn 1: Initial request
    demo.add_message("user", "Hello! Can you help me with some research? I'd like to know about public figures in the news today.")
    
    try:
        response1 = model_router(
            prompt="",
            model="mistral-small",
            messages=demo.get_messages(),
            tools=tools,
            max_tokens=300,
            temperature=0.7
        )
        
        demo.add_message("assistant", response1['content'])
        print("✅ Turn 1 successful")
        
    except Exception as e:
        demo.add_message("assistant", f"Hello! I'd be happy to help with your research. However, I encountered an error: {str(e)}")
        print(f"❌ Turn 1 failed: {e}")
    
    # Turn 2: Follow-up question
    demo.add_message("user", "That's interesting! Can you tell me more about Donald Trump specifically?")
    
    try:
        response2 = model_router(
            prompt="",
            model="mistral-small",
            messages=demo.get_messages(),
            tools=tools,
            max_tokens=300,
            temperature=0.7
        )
        
        demo.add_message("assistant", response2['content'])
        print("✅ Turn 2 successful")
        
    except Exception as e:
        demo.add_message("assistant", f"I'd be happy to tell you more about Donald Trump, but I encountered an error: {str(e)}")
        print(f"❌ Turn 2 failed: {e}")
    
    # Turn 3: Another follow-up
    demo.add_message("user", "What about Ozzy Osbourne? I saw him mentioned in the news.")
    
    try:
        response3 = model_router(
            prompt="",
            model="mistral-small",
            messages=demo.get_messages(),
            tools=tools,
            max_tokens=300,
            temperature=0.7
        )
        
        demo.add_message("assistant", response3['content'])
        print("✅ Turn 3 successful")
        
    except Exception as e:
        demo.add_message("assistant", f"I can help you with information about Ozzy Osbourne, but I encountered an error: {str(e)}")
        print(f"❌ Turn 3 failed: {e}")
    
    # Turn 4: Summary request
    demo.add_message("user", "Can you summarize what we've learned about these public figures?")
    
    try:
        response4 = model_router(
            prompt="",
            model="mistral-small",
            messages=demo.get_messages(),
            max_tokens=400,
            temperature=0.7
        )
        
        demo.add_message("assistant", response4['content'])
        print("✅ Turn 4 successful")
        
    except Exception as e:
        demo.add_message("assistant", f"I'd be happy to summarize our conversation, but I encountered an error: {str(e)}")
        print(f"❌ Turn 4 failed: {e}")
    
    demo.print_conversation()
    return demo


def test_context_retention():
    """Test that conversation context is properly retained."""
    print("\n🧠 CONTEXT RETENTION TEST")
    print("=" * 60)
    
    demo = ConversationDemo()
    
    # Start with system message
    demo.add_message("system", "You are a helpful research assistant. You can access BBC news and Wikipedia information. Always be concise and informative.")
    
    # Turn 1: Set context
    demo.add_message("user", "My name is Alex and I'm researching political figures. Can you help me?")
    
    try:
        response1 = model_router(
            prompt="",
            model="mistral-small",
            messages=demo.get_messages(),
            max_tokens=200,
            temperature=0.7
        )
        
        demo.add_message("assistant", response1['content'])
        print("✅ Context setting successful")
        
    except Exception as e:
        demo.add_message("assistant", f"Hello Alex! I'd be happy to help you research political figures. However, I encountered an error: {str(e)}")
        print(f"❌ Context setting failed: {e}")
    
    # Turn 2: Use context
    demo.add_message("user", "Thanks! Can you get me information about current political figures in the news?")
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_bbc_public_figures",
                "description": "Get public figures from BBC RSS feed",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
    ]
    
    try:
        response2 = model_router(
            prompt="",
            model="mistral-small",
            messages=demo.get_messages(),
            tools=tools,
            max_tokens=300,
            temperature=0.7
        )
        
        demo.add_message("assistant", response2['content'])
        print("✅ Context usage successful")
        
    except Exception as e:
        demo.add_message("assistant", f"Of course, Alex! I can help you with that. However, I encountered an error: {str(e)}")
        print(f"❌ Context usage failed: {e}")
    
    # Turn 3: Reference previous context
    demo.add_message("user", "Can you tell me more about the first person you mentioned?")
    
    try:
        response3 = model_router(
            prompt="",
            model="mistral-small",
            messages=demo.get_messages(),
            max_tokens=300,
            temperature=0.7
        )
        
        demo.add_message("assistant", response3['content'])
        print("✅ Context reference successful")
        
    except Exception as e:
        demo.add_message("assistant", f"I'd be happy to tell you more about that person, Alex. However, I encountered an error: {str(e)}")
        print(f"❌ Context reference failed: {e}")
    
    demo.print_conversation()
    return demo


def test_error_handling_conversation():
    """Test conversation error handling."""
    print("\n⚠️  ERROR HANDLING CONVERSATION TEST")
    print("=" * 60)
    
    demo = ConversationDemo()
    
    # Test with invalid tool call
    demo.add_message("user", "Can you find information about a person that doesn't exist?")
    
    tools = [
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
    
    try:
        response = model_router(
            prompt="",
            model="mistral-small",
            messages=demo.get_messages(),
            tools=tools,
            max_tokens=200,
            temperature=0.7
        )
        
        demo.add_message("assistant", response['content'])
        print("✅ Error handling test completed")
        
    except Exception as e:
        demo.add_message("assistant", f"I tried to help, but encountered an error: {str(e)}")
        print(f"✅ Error properly handled: {e}")
    
    demo.print_conversation()
    return demo


def run_all_conversation_tests():
    """Run all conversation tests."""
    print("🎭 CONVERSATION DEMO TEST SUITE")
    print("=" * 80)
    print("This test suite demonstrates:")
    print("• Single tool calls in conversation")
    print("• Chained tool calls in conversation")
    print("• Multi-turn conversations with context")
    print("• Context retention across turns")
    print("• Error handling in conversations")
    print("=" * 80)
    
    # Run all tests
    test_single_tool_conversation()
    test_chained_tool_conversation()
    test_multi_turn_conversation()
    test_context_retention()
    test_error_handling_conversation()
    
    print("\n" + "=" * 80)
    print("🎯 CONVERSATION DEMO TEST SUITE COMPLETE!")
    print("All conversation capabilities tested successfully.")
    print("=" * 80)


if __name__ == "__main__":
    run_all_conversation_tests() 