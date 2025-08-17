#!/usr/bin/env python3
"""
Debug Model Router
Test to see exactly what the model router returns when tools are passed.
"""

import sys
import os
import json

# Import from the ultimate_llm_toolkit package
from ultimate_llm_toolkit.model_router import model_router


def test_model_router_with_tools():
    """Test model router with tools and show raw response."""
    print("🔍 DEBUGGING MODEL ROUTER WITH TOOLS")
    print("=" * 60)
    
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
    
    # Test prompt
    prompt = "Can you get me the public figures from today's BBC news?"
    
    print(f"📝 Prompt: {prompt}")
    print(f"🔧 Tools: {json.dumps(tools, indent=2)}")
    print()
    
    try:
        print("🔄 Calling model_router...")
        response = model_router(
            prompt=prompt,
            model="mistral-small",
            tools=tools,
            max_tokens=300,
            temperature=0.7
        )
        
        print("✅ Model router call successful")
        print()
        print("📊 RAW RESPONSE:")
        print("=" * 40)
        print(json.dumps(response, indent=2, default=str))
        print("=" * 40)
        
        # Analyze the response
        print("\n🔍 RESPONSE ANALYSIS:")
        print(f"Content length: {len(response.get('content', ''))}")
        print(f"Content: '{response.get('content', '')}'")
        print(f"Tool calls: {response.get('tool_calls')}")
        print(f"Usage: {response.get('usage')}")
        print(f"Model: {response.get('model')}")
        print(f"Provider: {response.get('provider')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def test_model_router_without_tools():
    """Test model router without tools for comparison."""
    print("\n🔍 DEBUGGING MODEL ROUTER WITHOUT TOOLS")
    print("=" * 60)
    
    # Test prompt
    prompt = "Hello! How are you today?"
    
    print(f"📝 Prompt: {prompt}")
    print(f"🔧 Tools: None")
    print()
    
    try:
        print("🔄 Calling model_router...")
        response = model_router(
            prompt=prompt,
            model="mistral-small",
            max_tokens=300,
            temperature=0.7
        )
        
        print("✅ Model router call successful")
        print()
        print("📊 RAW RESPONSE:")
        print("=" * 40)
        print(json.dumps(response, indent=2, default=str))
        print("=" * 40)
        
        # Analyze the response
        print("\n🔍 RESPONSE ANALYSIS:")
        print(f"Content length: {len(response.get('content', ''))}")
        print(f"Content: '{response.get('content', '')}'")
        print(f"Tool calls: {response.get('tool_calls')}")
        print(f"Usage: {response.get('usage')}")
        print(f"Model: {response.get('model')}")
        print(f"Provider: {response.get('provider')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Run debug tests."""
    test_model_router_with_tools()
    test_model_router_without_tools()


if __name__ == "__main__":
    main() 