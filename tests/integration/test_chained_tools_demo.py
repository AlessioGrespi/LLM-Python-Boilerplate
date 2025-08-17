#!/usr/bin/env python3
"""
Chained Tools Demo
Demonstrates chained tool calling to get public figures from BBC RSS feed
and find their corresponding Wikipedia pages.
"""

import sys
import os
import json
from typing import Dict, List, Any

# Import from the ultimate_llm_toolkit package
from ultimate_llm_toolkit.model_router import model_router
from ultimate_llm_toolkit.bbc_rss import get_bbc_public_figures, bbc_rss_tool
from ultimate_llm_toolkit.wikipedia_api import find_person_wikipedia_page, wikipedia_api_tool


def demo_chained_tools():
    """Demonstrate chained tool calling with BBC RSS and Wikipedia."""
    print("🔗 Chained Tools Demo: BBC RSS + Wikipedia")
    print("=" * 60)
    
    # Step 1: Get public figures from BBC RSS
    print("\n1️⃣ Step 1: Getting public figures from BBC RSS feed...")
    try:
        bbc_result = get_bbc_public_figures()
        
        if not bbc_result.get("public_figures"):
            print("❌ No public figures found in BBC RSS feed")
            return
        
        print(f"✅ Found {bbc_result['total_figures']} public figures from BBC RSS")
        
        # Show some examples
        print("\n📰 Sample public figures found:")
        for i, figure in enumerate(bbc_result['public_figures'][:5]):
            print(f"  {i+1}. {figure['name']}")
            print(f"     Context: {figure['context'][:60]}...")
            if figure.get('title'):
                print(f"     Title: {figure['title']}")
            print()
        
    except Exception as e:
        print(f"❌ Error getting BBC public figures: {e}")
        return
    
    # Step 2: Find Wikipedia pages for the public figures
    print("\n2️⃣ Step 2: Finding Wikipedia pages for public figures...")
    
    # Take first 3 figures for demo
    demo_figures = bbc_result['public_figures'][:3]
    wikipedia_results = []
    
    for i, figure in enumerate(demo_figures):
        print(f"\n🔍 Looking up: {figure['name']}")
        try:
            wiki_result = find_person_wikipedia_page(figure['name'])
            
            if wiki_result.get("success"):
                print(f"✅ Found Wikipedia page: {wiki_result['page_info']['title']}")
                print(f"   URL: {wiki_result['page_info']['content_urls']['desktop']['page']}")
                print(f"   Extract: {wiki_result['page_info']['extract'][:100]}...")
                
                wikipedia_results.append({
                    "bbc_figure": figure,
                    "wikipedia_result": wiki_result
                })
            else:
                print(f"❌ No Wikipedia page found: {wiki_result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Error looking up {figure['name']}: {e}")
    
    # Step 3: Use AI to analyze and summarize the results
    print("\n3️⃣ Step 3: Using AI to analyze and summarize the results...")
    
    if wikipedia_results:
        # Create a summary for the AI
        summary_data = {
            "bbc_source": bbc_result['source'],
            "total_figures_found": bbc_result['total_figures'],
            "figures_with_wikipedia": len(wikipedia_results),
            "results": []
        }
        
        for result in wikipedia_results:
            bbc_figure = result['bbc_figure']
            wiki_result = result['wikipedia_result']
            
            summary_data["results"].append({
                "name": bbc_figure['name'],
                "bbc_context": bbc_figure['context'],
                "wikipedia_title": wiki_result['page_info']['title'],
                "wikipedia_extract": wiki_result['page_info']['extract'][:200],
                "wikipedia_url": wiki_result['page_info']['content_urls']['desktop']['page']
            })
        
        # Ask AI to analyze the results
        analysis_prompt = f"""
        I've analyzed the BBC RSS feed and found {len(wikipedia_results)} public figures with Wikipedia pages.
        
        Here's the data:
        {json.dumps(summary_data, indent=2)}
        
        Please provide a brief analysis of:
        1. The types of public figures found in the BBC news
        2. How well the Wikipedia matching worked
        3. Any interesting patterns or observations
        4. Suggestions for improving the tool chain
        
        Keep your response concise and informative.
        """
        
        try:
            ai_response = model_router(
                prompt=analysis_prompt,
                model="anthropic-sonnet",
                max_tokens=300,
                temperature=0.7
            )
            
            print("\n🤖 AI Analysis:")
            print("-" * 40)
            print(ai_response['content'])
            
        except Exception as e:
            print(f"❌ Error getting AI analysis: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Chained Tools Demo Complete!")
    print("This demo shows:")
    print("  • Tool 1: BBC RSS feed parsing")
    print("  • Tool 2: Wikipedia API integration")
    print("  • Tool 3: AI analysis and summarization")
    print("  • Chained execution for comprehensive results")


def demo_with_model_router_tools():
    """Demonstrate using tools through the model router."""
    print("\n🔧 Advanced Demo: Using Tools Through Model Router")
    print("=" * 60)
    
    # Define the tools for the model router
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
    
    # Create a prompt that will trigger tool usage
    tool_prompt = """
    Please help me analyze the current news by:
    1. Getting public figures from the BBC RSS feed
    2. Finding Wikipedia pages for the first 3 public figures found
    3. Providing a brief summary of what you found
    
    Use the available tools to gather this information.
    """
    
    try:
        print("🤖 Asking AI to use tools for analysis...")
        
        response = model_router(
            prompt=tool_prompt,
            model="anthropic-sonnet",
            tools=tools,
            max_tokens=500,
            temperature=0.7
        )
        
        print("\n📋 AI Response:")
        print("-" * 40)
        print(response['content'])
        
        if response.get('tool_calls'):
            print(f"\n🔧 Tool calls made: {len(response['tool_calls'])}")
            for i, tool_call in enumerate(response['tool_calls']):
                print(f"  {i+1}. {tool_call['name']}")
        
    except Exception as e:
        print(f"❌ Error in advanced demo: {e}")


if __name__ == "__main__":
    # Run the basic demo
    demo_chained_tools()
    
    # Run the advanced demo with model router tools
    demo_with_model_router_tools() 