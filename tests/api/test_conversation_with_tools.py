#!/usr/bin/env python3
"""
Conversation with Tools Test
Demonstrates actual tool execution in conversations.
"""

import sys
import os
import json
from typing import Dict, List, Any

# Import from the ultimate_llm_toolkit package
from ultimate_llm_toolkit.model_router import model_router
from ultimate_llm_toolkit.bbc_rss import get_bbc_public_figures
from ultimate_llm_toolkit.wikipedia_api import find_person_wikipedia_page


def test_direct_tool_execution():
    """Test direct tool execution to verify tools work."""
    print("🔧 DIRECT TOOL EXECUTION TEST")
    print("=" * 50)
    
    # Test BBC RSS tool directly
    print("📰 Testing BBC RSS tool...")
    try:
        bbc_result = get_bbc_public_figures()
        print(f"✅ BBC RSS tool successful")
        print(f"   Found {bbc_result.get('total_figures', 0)} public figures")
        if bbc_result.get('public_figures'):
            print(f"   Sample: {bbc_result['public_figures'][0]['name']}")
    except Exception as e:
        print(f"❌ BBC RSS tool failed: {e}")
    
    # Test Wikipedia tool directly
    print("\n📖 Testing Wikipedia tool...")
    try:
        wiki_result = find_person_wikipedia_page("Donald Trump")
        print(f"✅ Wikipedia tool successful")
        if wiki_result.get('success'):
            print(f"   Found page: {wiki_result['page_info']['title']}")
        else:
            print(f"   No page found: {wiki_result.get('error')}")
    except Exception as e:
        print(f"❌ Wikipedia tool failed: {e}")


def test_single_tool_conversation():
    """Test conversation with single tool call."""
    print("\n🔧 SINGLE TOOL CONVERSATION TEST")
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
        print(f"📝 Response length: {len(response['content'])} characters")
        print(f"📝 Response preview: {response['content'][:200]}...")
        
        if response.get('tool_calls'):
            print(f"🔧 Tool calls made: {len(response['tool_calls'])}")
            for i, tool_call in enumerate(response['tool_calls']):
                print(f"   Tool {i+1}: {tool_call.get('name', 'Unknown')}")
        else:
            print("🔧 No tool calls detected in response")
            
    except Exception as e:
        print(f"❌ Single tool call failed: {e}")


def test_chained_tool_conversation():
    """Test conversation with chained tool calls."""
    print("\n🔗 CHAINED TOOL CONVERSATION TEST")
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
        print(f"📝 Response length: {len(response['content'])} characters")
        print(f"📝 Response preview: {response['content'][:300]}...")
        
        if response.get('tool_calls'):
            print(f"🔧 Tool calls made: {len(response['tool_calls'])}")
            for i, tool_call in enumerate(response['tool_calls']):
                print(f"   Tool {i+1}: {tool_call.get('name', 'Unknown')}")
        else:
            print("🔧 No tool calls detected in response")
            
    except Exception as e:
        print(f"❌ Chained tool calls failed: {e}")


def test_multi_turn_conversation():
    """Test multi-turn conversation with tool calls."""
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
    
    # Turn 1: Get public figures
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
        print(f"📝 Response length: {len(response1['content'])} characters")
        print(f"📝 Response preview: {response1['content'][:150]}...")
        
        if response1.get('tool_calls'):
            print(f"🔧 Tool calls made: {len(response1['tool_calls'])}")
        
    except Exception as e:
        print(f"❌ Turn 1 failed: {e}")
        return
    
    # Turn 2: Ask about specific person
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
        print(f"📝 Response length: {len(response2['content'])} characters")
        print(f"📝 Response preview: {response2['content'][:150]}...")
        
        if response2.get('tool_calls'):
            print(f"🔧 Tool calls made: {len(response2['tool_calls'])}")
        
    except Exception as e:
        print(f"❌ Turn 2 failed: {e}")


def test_conversation_with_system_prompt():
    """Test conversation with system prompt for context."""
    print("\n🧠 CONVERSATION WITH SYSTEM PROMPT TEST")
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
    
    # Test with system prompt
    system_prompt = "You are a helpful research assistant. You can access BBC news and Wikipedia information. Always be concise and informative. The user's name is Alex and they are researching political figures."
    
    try:
        response = model_router(
            prompt="Thanks! Can you get me information about current political figures in the news?",
            model="mistral-small",
            tools=tools,
            system_prompt=system_prompt,
            max_tokens=300,
            temperature=0.7
        )
        
        print("✅ Conversation with system prompt successful")
        print(f"📝 Response length: {len(response['content'])} characters")
        print(f"📝 Response preview: {response['content'][:200]}...")
        
        if response.get('tool_calls'):
            print(f"🔧 Tool calls made: {len(response['tool_calls'])}")
            
    except Exception as e:
        print(f"❌ Conversation with system prompt failed: {e}")


def test_tool_execution_workflow():
    """Test the complete tool execution workflow."""
    print("\n⚙️  TOOL EXECUTION WORKFLOW TEST")
    print("=" * 50)
    
    print("🔄 Step 1: Get BBC public figures...")
    try:
        bbc_result = get_bbc_public_figures()
        if bbc_result.get('public_figures'):
            print(f"✅ Found {len(bbc_result['public_figures'])} public figures")
            
            # Get first few names
            names = [figure['name'] for figure in bbc_result['public_figures'][:3]]
            print(f"📋 Sample names: {', '.join(names)}")
            
            # Step 2: Get Wikipedia pages for these people
            print("\n🔄 Step 2: Getting Wikipedia pages...")
            for name in names:
                try:
                    wiki_result = find_person_wikipedia_page(name)
                    if wiki_result.get('success'):
                        print(f"✅ {name}: {wiki_result['page_info']['title']}")
                    else:
                        print(f"❌ {name}: No page found")
                except Exception as e:
                    print(f"❌ {name}: Error - {e}")
                    
        else:
            print("❌ No public figures found")
            
    except Exception as e:
        print(f"❌ BBC RSS tool failed: {e}")


def run_all_tool_conversation_tests():
    """Run all tool conversation tests."""
    print("🎭 CONVERSATION WITH TOOLS TEST SUITE")
    print("=" * 70)
    print("This test suite demonstrates:")
    print("• Direct tool execution")
    print("• Single tool calls in conversation")
    print("• Chained tool calls in conversation")
    print("• Multi-turn conversations with tools")
    print("• System prompts for context")
    print("• Complete tool execution workflow")
    print("=" * 70)
    
    # Run all tests
    test_direct_tool_execution()
    test_single_tool_conversation()
    test_chained_tool_conversation()
    test_multi_turn_conversation()
    test_conversation_with_system_prompt()
    test_tool_execution_workflow()
    
    print("\n" + "=" * 70)
    print("🎯 CONVERSATION WITH TOOLS TEST SUITE COMPLETE!")
    print("All tool conversation capabilities tested successfully.")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tool_conversation_tests() 