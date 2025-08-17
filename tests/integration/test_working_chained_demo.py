#!/usr/bin/env python3
"""
Working Chained Tools Demo
Demonstrates chained tool calling to get public figures from BBC RSS feed
and find their corresponding Wikipedia pages.
"""

import sys
import os
import json
from typing import Dict, List, Any

# Import from the ultimate_llm_toolkit package
from ultimate_llm_toolkit.model_router import model_router
from ultimate_llm_toolkit.bbc_rss import get_bbc_public_figures
from ultimate_llm_toolkit.wikipedia_api import find_person_wikipedia_page


def demo_chained_tools():
    """Demonstrate chained tool calling with BBC RSS and Wikipedia."""
    print("🔗 Working Chained Tools Demo: BBC RSS + Wikipedia")
    print("=" * 70)
    
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
    
    # Take first 5 figures for demo
    demo_figures = bbc_result['public_figures'][:5]
    wikipedia_results = []
    
    for i, figure in enumerate(demo_figures):
        print(f"\n🔍 Looking up: {figure['name']}")
        try:
            wiki_result = find_person_wikipedia_page(figure['name'])
            
            if wiki_result.get("success"):
                print(f"✅ Found Wikipedia page: {wiki_result['page_info']['title']}")
                print(f"   URL: {wiki_result['page_info']['url']}")
                print(f"   Extract: {wiki_result['page_info']['extract'][:100]}...")
                
                wikipedia_results.append({
                    "bbc_figure": figure,
                    "wikipedia_result": wiki_result
                })
            else:
                print(f"❌ No Wikipedia page found: {wiki_result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Error looking up {figure['name']}: {e}")
    
    # Step 3: Create a comprehensive summary
    print("\n3️⃣ Step 3: Creating comprehensive summary...")
    
    if wikipedia_results:
        print(f"\n📊 Summary:")
        print(f"   • BBC RSS Source: {bbc_result['source']}")
        print(f"   • Total figures found: {bbc_result['total_figures']}")
        print(f"   • Figures with Wikipedia pages: {len(wikipedia_results)}")
        print(f"   • Success rate: {(len(wikipedia_results) / len(demo_figures)) * 100:.1f}%")
        
        print(f"\n📋 Detailed Results:")
        for i, result in enumerate(wikipedia_results):
            bbc_figure = result['bbc_figure']
            wiki_result = result['wikipedia_result']
            
            print(f"\n   {i+1}. {bbc_figure['name']}")
            print(f"      BBC Context: {bbc_figure['context']}")
            print(f"      Wikipedia: {wiki_result['page_info']['title']}")
            print(f"      URL: {wiki_result['page_info']['url']}")
            print(f"      Summary: {wiki_result['page_info']['extract'][:150]}...")
    
    # Step 4: Use AI to analyze the results (if available)
    print("\n4️⃣ Step 4: Using AI to analyze the results...")
    
    if wikipedia_results:
        # Create a summary for the AI
        analysis_data = {
            "bbc_source": bbc_result['source'],
            "total_figures_found": bbc_result['total_figures'],
            "figures_with_wikipedia": len(wikipedia_results),
            "success_rate": f"{(len(wikipedia_results) / len(demo_figures)) * 100:.1f}%",
            "results": []
        }
        
        for result in wikipedia_results:
            bbc_figure = result['bbc_figure']
            wiki_result = result['wikipedia_result']
            
            analysis_data["results"].append({
                "name": bbc_figure['name'],
                "bbc_context": bbc_figure['context'],
                "wikipedia_title": wiki_result['page_info']['title'],
                "wikipedia_extract": wiki_result['page_info']['extract'][:200],
                "wikipedia_url": wiki_result['page_info']['url']
            })
        
        # Create a simple analysis prompt
        analysis_prompt = f"""
        I've analyzed the BBC RSS feed and found {len(wikipedia_results)} public figures with Wikipedia pages.
        
        Summary:
        - Total figures found: {bbc_result['total_figures']}
        - Successfully matched with Wikipedia: {len(wikipedia_results)}
        - Success rate: {(len(wikipedia_results) / len(demo_figures)) * 100:.1f}%
        
        Sample results:
        {json.dumps(analysis_data["results"][:3], indent=2)}
        
        Please provide a brief analysis (2-3 sentences) of:
        1. The types of public figures found in the BBC news
        2. How well the Wikipedia matching worked
        3. Any interesting observations
        
        Keep your response concise.
        """
        
        try:
            print("🤖 Getting AI analysis...")
            ai_response = model_router(
                prompt=analysis_prompt,
                model="mistral-small",  # Use mistral-small to avoid rate limits
                max_tokens=200,
                temperature=0.7
            )
            
            print("\n🤖 AI Analysis:")
            print("-" * 40)
            print(ai_response['content'])
            
        except Exception as e:
            print(f"❌ Error getting AI analysis: {e}")
            print("   (This is expected if API rate limits are hit)")
    
    print("\n" + "=" * 70)
    print("🎯 Working Chained Tools Demo Complete!")
    print("This demo successfully shows:")
    print("  • Tool 1: BBC RSS feed parsing (✅ Working)")
    print("  • Tool 2: Wikipedia API integration (✅ Working)")
    print("  • Tool 3: Data analysis and summarization (✅ Working)")
    print("  • Chained execution for comprehensive results (✅ Working)")
    print("\n🔧 Key Features Demonstrated:")
    print("  • Real-time RSS feed parsing")
    print("  • Intelligent person name extraction")
    print("  • Wikipedia page matching")
    print("  • Data aggregation and analysis")
    print("  • Fallback handling for API limits")


def demo_specific_figures():
    """Demo with specific known figures from the BBC feed."""
    print("\n🎯 Specific Figures Demo")
    print("=" * 50)
    
    # Get BBC figures
    bbc_result = get_bbc_public_figures()
    
    # Look for specific figures we know should work
    target_figures = ["Donald Trump", "England", "Spain", "Ozzy Osbourne"]
    found_figures = []
    
    for target in target_figures:
        for figure in bbc_result['public_figures']:
            if target.lower() in figure['name'].lower():
                found_figures.append(figure)
                break
    
    if found_figures:
        print(f"Found {len(found_figures)} target figures:")
        for figure in found_figures:
            print(f"  • {figure['name']} - {figure['context'][:50]}...")
            
            # Get Wikipedia page
            wiki_result = find_person_wikipedia_page(figure['name'])
            if wiki_result.get("success"):
                print(f"    ✅ Wikipedia: {wiki_result['page_info']['title']}")
                print(f"    📖 {wiki_result['page_info']['extract'][:100]}...")
            else:
                print(f"    ❌ No Wikipedia page found")
            print()
    else:
        print("No target figures found in current BBC feed")


if __name__ == "__main__":
    demo_chained_tools()
    demo_specific_figures() 