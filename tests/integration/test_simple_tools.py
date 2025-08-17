#!/usr/bin/env python3
"""
Simple Tools Test
Test basic tool functionality with the model router.
"""

import sys
import os

# Import from the ultimate_llm_toolkit package
from ultimate_llm_toolkit.model_router import model_router
from ultimate_llm_toolkit.bbc_rss import get_bbc_public_figures
from ultimate_llm_toolkit.wikipedia_api import find_person_wikipedia_page


def test_individual_tools():
    """Test individual tools work correctly."""
    print("🧪 Testing Individual Tools")
    print("=" * 40)
    
    # Test BBC RSS tool
    print("\n1️⃣ Testing BBC RSS Tool:")
    try:
        bbc_result = get_bbc_public_figures()
        print(f"✅ BBC RSS: Found {bbc_result['total_figures']} public figures")
        
        # Show first 3 figures
        for i, figure in enumerate(bbc_result['public_figures'][:3]):
            print(f"   {i+1}. {figure['name']}")
        
    except Exception as e:
        print(f"❌ BBC RSS Error: {e}")
    
    # Test Wikipedia tool
    print("\n2️⃣ Testing Wikipedia Tool:")
    try:
        wiki_result = find_person_wikipedia_page("Donald Trump")
        if wiki_result.get("success"):
            print(f"✅ Wikipedia: Found page for Donald Trump")
            print(f"   Title: {wiki_result['page_info']['title']}")
            print(f"   URL: {wiki_result['page_info']['url']}")
        else:
            print(f"❌ Wikipedia Error: {wiki_result.get('error')}")
            
    except Exception as e:
        print(f"❌ Wikipedia Error: {e}")


def test_model_router_with_tools():
    """Test model router with tools."""
    print("\n🤖 Testing Model Router with Tools")
    print("=" * 40)
    
    # Define simple tools
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
    
    # Test with a simple prompt
    prompt = "Please get the public figures from BBC RSS feed and tell me how many were found."
    
    try:
        print("📝 Sending prompt to model router...")
        response = model_router(
            prompt=prompt,
            model="anthropic-sonnet",
            tools=tools,
            max_tokens=200,
            temperature=0.7
        )
        
        print("\n📋 Response:")
        print("-" * 20)
        print(response['content'])
        
        if response.get('tool_calls'):
            print(f"\n🔧 Tool calls detected: {len(response['tool_calls'])}")
            for i, tool_call in enumerate(response['tool_calls']):
                print(f"  {i+1}. {tool_call['name']}")
        else:
            print("\n⚠️  No tool calls detected")
            
    except Exception as e:
        print(f"❌ Model Router Error: {e}")


def test_direct_tool_integration():
    """Test direct integration of tools with model router."""
    print("\n🔗 Testing Direct Tool Integration")
    print("=" * 40)
    
    try:
        # Get BBC figures
        print("📰 Getting BBC public figures...")
        bbc_result = get_bbc_public_figures()
        
        if bbc_result['public_figures']:
            # Get first figure
            first_figure = bbc_result['public_figures'][0]
            print(f"🔍 Looking up: {first_figure['name']}")
            
            # Get Wikipedia page
            wiki_result = find_person_wikipedia_page(first_figure['name'])
            
            if wiki_result.get("success"):
                # Create a summary for AI
                summary = f"""
                I found a public figure from BBC news: {first_figure['name']}
                BBC Context: {first_figure['context']}
                
                Wikipedia Information:
                Title: {wiki_result['page_info']['title']}
                URL: {wiki_result['page_info']['url']}
                Extract: {wiki_result['page_info']['extract'][:200]}...
                
                Please provide a brief analysis of this person based on the BBC context and Wikipedia information.
                """
                
                print("🤖 Getting AI analysis...")
                ai_response = model_router(
                    prompt=summary,
                    model="anthropic-sonnet",
                    max_tokens=300,
                    temperature=0.7
                )
                
                print("\n📋 AI Analysis:")
                print("-" * 20)
                print(ai_response['content'])
                
            else:
                print(f"❌ No Wikipedia page found for {first_figure['name']}")
        else:
            print("❌ No public figures found in BBC RSS")
            
    except Exception as e:
        print(f"❌ Integration Error: {e}")


if __name__ == "__main__":
    test_individual_tools()
    test_model_router_with_tools()
    test_direct_tool_integration() 