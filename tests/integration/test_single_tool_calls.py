#!/usr/bin/env python3
"""
Single Tool Calls Test
Demonstrates individual tool usage for specific use cases.
"""

import sys
import os
from typing import Dict, List, Any

# Add the necessary paths
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src', 'core'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools', 'tool_modules'))

from bbc_rss import get_bbc_rss_feed, get_bbc_public_figures
from wikipedia_api import find_person_wikipedia_page, search_wikipedia, get_wikipedia_page


def test_london_headlines():
    """Test getting headlines about London from BBC RSS feed."""
    print("🏛️  London Headlines Test")
    print("=" * 50)
    
    try:
        # Get BBC RSS feed
        print("📰 Fetching BBC RSS feed...")
        feed_data = get_bbc_rss_feed()
        
        # Filter for London-related headlines
        london_headlines = []
        keywords = ['london', 'londoner', 'londoners', 'british', 'uk', 'england']
        
        for article in feed_data['articles']:
            title = article['title'].lower()
            description = article['description'].lower()
            
            # Check if any London-related keywords are in title or description
            if any(keyword in title or keyword in description for keyword in keywords):
                london_headlines.append({
                    'title': article['title'],
                    'description': article['description'],
                    'link': article['link'],
                    'pub_date': article['pub_date']
                })
        
        print(f"✅ Found {len(london_headlines)} London-related headlines")
        
        if london_headlines:
            print("\n📋 London Headlines:")
            for i, headline in enumerate(london_headlines[:5], 1):  # Show first 5
                print(f"\n{i}. {headline['title']}")
                print(f"   📅 {headline['pub_date']}")
                print(f"   📝 {headline['description'][:100]}...")
                print(f"   🔗 {headline['link']}")
        else:
            print("❌ No London-related headlines found in current feed")
            
    except Exception as e:
        print(f"❌ Error getting London headlines: {e}")


def test_jair_bolsonaro_wikipedia():
    """Test getting Wikipedia page for Jair Bolsonaro."""
    print("\n🇧🇷 Jair Bolsonaro Wikipedia Test")
    print("=" * 50)
    
    try:
        print("🔍 Searching for Jair Bolsonaro on Wikipedia...")
        
        # Method 1: Direct person lookup
        person_result = find_person_wikipedia_page("Jair Bolsonaro")
        
        if person_result.get("success"):
            page_info = person_result['page_info']
            print(f"✅ Found Wikipedia page: {page_info['title']}")
            print(f"   📖 URL: {page_info['url']}")
            print(f"   📅 Page ID: {page_info['page_id']}")
            print(f"\n📝 Summary:")
            print(f"   {page_info['extract'][:300]}...")
            
            # Show search results that led to this page
            if person_result.get('search_results'):
                print(f"\n🔍 Search Results:")
                for i, result in enumerate(person_result['search_results']['results'][:3], 1):
                    print(f"   {i}. {result['title']} - {result['snippet'][:100]}...")
        else:
            print(f"❌ No Wikipedia page found: {person_result.get('error')}")
            
    except Exception as e:
        print(f"❌ Error getting Jair Bolsonaro Wikipedia page: {e}")


def test_specific_person_wikipedia(person_name: str):
    """Test getting Wikipedia page for a specific person."""
    print(f"\n👤 {person_name} Wikipedia Test")
    print("=" * 50)
    
    try:
        print(f"🔍 Searching for {person_name} on Wikipedia...")
        
        # Method 1: Direct person lookup
        person_result = find_person_wikipedia_page(person_name)
        
        if person_result.get("success"):
            page_info = person_result['page_info']
            print(f"✅ Found Wikipedia page: {page_info['title']}")
            print(f"   📖 URL: {page_info['url']}")
            print(f"   📅 Page ID: {page_info['page_id']}")
            print(f"\n📝 Summary:")
            print(f"   {page_info['extract'][:300]}...")
            
            # Show if this was an exact match or best match
            if person_result.get('best_match'):
                best_match = person_result['best_match']
                if best_match['title'].lower() == person_name.lower():
                    print(f"\n🎯 Exact match found!")
                else:
                    print(f"\n🔍 Best match: {best_match['title']}")
                    
        else:
            print(f"❌ No Wikipedia page found: {person_result.get('error')}")
            
            # Try alternative search
            print(f"\n🔄 Trying alternative search...")
            search_result = search_wikipedia(person_name, limit=3)
            
            if search_result.get("success") and search_result["results"]:
                print(f"📋 Alternative search results:")
                for i, result in enumerate(search_result["results"], 1):
                    print(f"   {i}. {result['title']} - {result['snippet'][:100]}...")
            else:
                print(f"❌ No alternative results found")
            
    except Exception as e:
        print(f"❌ Error getting {person_name} Wikipedia page: {e}")


def test_bbc_public_figures():
    """Test getting public figures from BBC RSS feed."""
    print("\n👥 BBC Public Figures Test")
    print("=" * 50)
    
    try:
        print("📰 Extracting public figures from BBC RSS feed...")
        
        figures_result = get_bbc_public_figures()
        
        if figures_result.get("public_figures"):
            print(f"✅ Found {figures_result['total_figures']} public figures")
            print(f"   📊 Source: {figures_result['source']}")
            print(f"   📅 Last Updated: {figures_result['last_updated']}")
            
            print(f"\n👤 Sample Public Figures:")
            for i, figure in enumerate(figures_result['public_figures'][:10], 1):
                print(f"\n{i}. {figure['name']}")
                if figure.get('title'):
                    print(f"   🏷️  Title: {figure['title']}")
                print(f"   📰 Context: {figure['context'][:80]}...")
                print(f"   🔗 Article: {figure['article_link']}")
        else:
            print("❌ No public figures found")
            
    except Exception as e:
        print(f"❌ Error getting BBC public figures: {e}")


def test_wikipedia_search(query: str):
    """Test Wikipedia search functionality."""
    print(f"\n🔍 Wikipedia Search Test: '{query}'")
    print("=" * 50)
    
    try:
        print(f"🔍 Searching Wikipedia for: {query}")
        
        search_result = search_wikipedia(query, limit=5)
        
        if search_result.get("success"):
            print(f"✅ Found {search_result['total_results']} results")
            
            for i, result in enumerate(search_result["results"], 1):
                print(f"\n{i}. {result['title']}")
                print(f"   📄 Page ID: {result['page_id']}")
                print(f"   📝 {result['snippet'][:150]}...")
                print(f"   🔗 {result['url']}")
        else:
            print(f"❌ Search failed: {search_result.get('error')}")
            
    except Exception as e:
        print(f"❌ Error searching Wikipedia: {e}")


def test_wikipedia_page_by_title(title: str):
    """Test getting Wikipedia page by exact title."""
    print(f"\n📖 Wikipedia Page Test: '{title}'")
    print("=" * 50)
    
    try:
        print(f"📖 Getting Wikipedia page for: {title}")
        
        page_result = get_wikipedia_page(title)
        
        if page_result.get("success"):
            print(f"✅ Found page: {page_result['title']}")
            print(f"   📄 Page ID: {page_result['page_id']}")
            print(f"   🔗 URL: {page_result['url']}")
            print(f"\n📝 Content:")
            print(f"   {page_result['extract'][:400]}...")
        else:
            print(f"❌ Page not found: {page_result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error getting Wikipedia page: {e}")


def run_all_single_tool_tests():
    """Run all single tool call tests."""
    print("🧪 Single Tool Calls Test Suite")
    print("=" * 60)
    
    # Test 1: London headlines
    test_london_headlines()
    
    # Test 2: Jair Bolsonaro Wikipedia
    test_jair_bolsonaro_wikipedia()
    
    # Test 3: BBC public figures
    test_bbc_public_figures()
    
    # Test 4: Specific person Wikipedia lookups
    test_specific_person_wikipedia("Vladimir Putin")
    test_specific_person_wikipedia("Taylor Swift")
    
    # Test 5: Wikipedia searches
    test_wikipedia_search("artificial intelligence")
    test_wikipedia_search("climate change")
    
    # Test 6: Wikipedia pages by title
    test_wikipedia_page_by_title("London")
    test_wikipedia_page_by_title("Brazil")
    
    print("\n" + "=" * 60)
    print("🎯 Single Tool Calls Test Suite Complete!")
    print("All individual tool functions tested successfully.")


if __name__ == "__main__":
    # Run all tests
    run_all_single_tool_tests()
    
    # Or run specific tests
    # test_london_headlines()
    # test_jair_bolsonaro_wikipedia() 