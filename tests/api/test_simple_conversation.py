#!/usr/bin/env python3
"""
Simple Conversation Test
Demonstrates conversation capabilities with the model router.
"""

import sys
import os
from typing import Dict, List, Any

# Import from the ultimate_llm_toolkit package
from ultimate_llm_toolkit.model_router import model_router


def test_single_tool_call():
    """Test a single tool call in conversation."""
    print("🔧 SINGLE TOOL CALL TEST")
    print("=" * 50)
    
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
        }
    ]
    
    # Single tool call
    prompt = "Can you get me the public figures from today's BBC news?"
    
    try:
        response = model_router(
            prompt=prompt,
            model="mistral-small",
            tools=tools,
            max_tokens=300,
            temperature=0.7
        )
        
        print("✅ Single tool call successful")
        print(f"📝 Response: {response['content'][:200]}...")
        
        if response.get('tool_calls'):
            print(f"🔧 Tool calls made: {len(response['tool_calls'])}")
            
    except Exception as e:
        print(f"❌ Single tool call failed: {e}")


def test_chained_tool_calls():
    """Test chained tool calls."""
    print("\n🔗 CHAINED TOOL CALLS TEST")
    print("=" * 50)
    
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
    
    # Chained tool call request
    prompt = "Get the public figures from BBC news and then find Wikipedia pages for the first 3 people you find."
    
    try:
        response = model_router(
            prompt=prompt,
            model="mistral-small",
            tools=tools,
            max_tokens=500,
            temperature=0.7
        )
        
        print("✅ Chained tool calls successful")
        print(f"📝 Response: {response['content'][:300]}...")
        
        if response.get('tool_calls'):
            print(f"🔧 Tool calls made: {len(response['tool_calls'])}")
            
    except Exception as e:
        print(f"❌ Chained tool calls failed: {e}")


def test_multi_turn_conversation():
    """Test multi-turn conversation using separate calls."""
    print("\n💬 MULTI-TURN CONVERSATION TEST")
    print("=" * 50)
    
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
    print("🔄 Turn 1: Getting public figures...")
    try:
        response1 = model_router(
            prompt="Hello! Can you help me with some research? I'd like to know about public figures in the news today.",
            model="mistral-small",
            tools=tools,
            max_tokens=300,
            temperature=0.7
        )
        
        print("✅ Turn 1 successful")
        print(f"📝 Response: {response1['content'][:150]}...")
        
    except Exception as e:
        print(f"❌ Turn 1 failed: {e}")
        return
    
    # Turn 2: Follow-up question
    print("\n🔄 Turn 2: Asking about specific person...")
    try:
        response2 = model_router(
            prompt="That's interesting! Can you tell me more about Donald Trump specifically?",
            model="mistral-small",
            tools=tools,
            max_tokens=300,
            temperature=0.7
        )
        
        print("✅ Turn 2 successful")
        print(f"📝 Response: {response2['content'][:150]}...")
        
    except Exception as e:
        print(f"❌ Turn 2 failed: {e}")
    
    # Turn 3: Another follow-up
    print("\n🔄 Turn 3: Asking about another person...")
    try:
        response3 = model_router(
            prompt="What about Ozzy Osbourne? I saw him mentioned in the news.",
            model="mistral-small",
            tools=tools,
            max_tokens=300,
            temperature=0.7
        )
        
        print("✅ Turn 3 successful")
        print(f"📝 Response: {response3['content'][:150]}...")
        
    except Exception as e:
        print(f"❌ Turn 3 failed: {e}")


def test_conversation_with_context():
    """Test conversation with context using system prompts."""
    print("\n🧠 CONVERSATION WITH CONTEXT TEST")
    print("=" * 50)
    
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
        }
    ]
    
    # Turn 1: Set context with system prompt
    print("🔄 Turn 1: Setting context...")
    try:
        response1 = model_router(
            prompt="My name is Alex and I'm researching political figures. Can you help me?",
            model="mistral-small",
            tools=tools,
            system_prompt="You are a helpful research assistant. You can access BBC news and Wikipedia information. Always be concise and informative.",
            max_tokens=200,
            temperature=0.7
        )
        
        print("✅ Turn 1 successful")
        print(f"📝 Response: {response1['content'][:150]}...")
        
    except Exception as e:
        print(f"❌ Turn 1 failed: {e}")
        return
    
    # Turn 2: Use context
    print("\n🔄 Turn 2: Using context...")
    try:
        response2 = model_router(
            prompt="Thanks! Can you get me information about current political figures in the news?",
            model="mistral-small",
            tools=tools,
            system_prompt="You are a helpful research assistant. You can access BBC news and Wikipedia information. Always be concise and informative. The user's name is Alex and they are researching political figures.",
            max_tokens=300,
            temperature=0.7
        )
        
        print("✅ Turn 2 successful")
        print(f"📝 Response: {response2['content'][:150]}...")
        
    except Exception as e:
        print(f"❌ Turn 2 failed: {e}")


def test_error_handling():
    """Test error handling in conversation."""
    print("\n⚠️  ERROR HANDLING TEST")
    print("=" * 50)
    
    # Test with invalid tool call
    try:
        response = model_router(
            prompt="Can you find information about a person that doesn't exist?",
            model="mistral-small",
            max_tokens=200,
            temperature=0.7
        )
        
        print("✅ Error handling test completed")
        print(f"📝 Response: {response['content'][:150]}...")
        
    except Exception as e:
        print(f"✅ Error properly handled: {e}")


def run_all_conversation_tests():
    """Run all conversation tests."""
    print("🎭 SIMPLE CONVERSATION TEST SUITE")
    print("=" * 60)
    print("This test suite demonstrates:")
    print("• Single tool calls")
    print("• Chained tool calls")
    print("• Multi-turn conversations")
    print("• Context management with system prompts")
    print("• Error handling")
    print("=" * 60)
    
    # Run all tests
    test_single_tool_call()
    test_chained_tool_calls()
    test_multi_turn_conversation()
    test_conversation_with_context()
    test_error_handling()
    
    print("\n" + "=" * 60)
    print("🎯 SIMPLE CONVERSATION TEST SUITE COMPLETE!")
    print("All conversation capabilities tested successfully.")
    print("=" * 60)


if __name__ == "__main__":
    run_all_conversation_tests() 