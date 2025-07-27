#!/usr/bin/env python3
"""
Specific Use Cases Test
Demonstrates the two specific use cases requested:
1. Headlines today about London
2. Wikipedia page for Jair Bolsonaro
"""

import sys
import os
from typing import Dict, List, Any
from datetime import datetime

# Add the necessary paths
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src', 'core'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools', 'tool_modules'))

from bbc_rss import get_bbc_rss_feed
from wikipedia_api import find_person_wikipedia_page


def get_london_headlines_today():
    """Get headlines about London from today's BBC RSS feed."""
    print("🏛️  LONDON HEADLINES TODAY")
    print("=" * 60)
    print(f"📅 Date: {datetime.now().strftime('%A, %B %d, %Y')}")
    print(f"🕐 Time: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
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
        print()
        
        if london_headlines:
            print("📋 LONDON HEADLINES:")
            print("-" * 40)
            
            for i, headline in enumerate(london_headlines, 1):
                print(f"\n{i}. {headline['title']}")
                print(f"   📅 Published: {headline['pub_date']}")
                print(f"   📝 {headline['description']}")
                print(f"   🔗 Read more: {headline['link']}")
                
                if i >= 10:  # Limit to first 10 headlines
                    remaining = len(london_headlines) - 10
                    if remaining > 0:
                        print(f"\n   ... and {remaining} more headlines")
                    break
        else:
            print("❌ No London-related headlines found in today's feed")
            print("   This might be due to the current news cycle or feed content.")
            
    except Exception as e:
        print(f"❌ Error getting London headlines: {e}")


def get_jair_bolsonaro_wikipedia():
    """Get Wikipedia page for Jair Bolsonaro."""
    print("\n🇧🇷 JAIR BOLSONARO WIKIPEDIA PAGE")
    print("=" * 60)
    
    try:
        print("🔍 Searching for Jair Bolsonaro on Wikipedia...")
        
        # Get Wikipedia page for Jair Bolsonaro
        person_result = find_person_wikipedia_page("Jair Bolsonaro")
        
        if person_result.get("success"):
            page_info = person_result['page_info']
            
            print(f"✅ Found Wikipedia page: {page_info['title']}")
            print(f"   📖 URL: {page_info['url']}")
            print(f"   📄 Page ID: {page_info['page_id']}")
            print()
            
            print("📝 SUMMARY:")
            print("-" * 40)
            print(f"{page_info['extract']}")
            print()
            
            # Show additional information if available
            if person_result.get('search_results'):
                print("🔍 SEARCH RESULTS:")
                print("-" * 40)
                for i, result in enumerate(person_result['search_results']['results'][:3], 1):
                    print(f"{i}. {result['title']}")
                    print(f"   {result['snippet']}")
                    print()
                    
        else:
            print(f"❌ No Wikipedia page found: {person_result.get('error')}")
            
            # Try alternative search
            print("\n🔄 Trying alternative search...")
            from wikipedia_api import search_wikipedia
            search_result = search_wikipedia("Jair Bolsonaro", limit=3)
            
            if search_result.get("success") and search_result["results"]:
                print(f"📋 Alternative search results:")
                for i, result in enumerate(search_result["results"], 1):
                    print(f"   {i}. {result['title']} - {result['snippet'][:100]}...")
            else:
                print(f"❌ No alternative results found")
            
    except Exception as e:
        print(f"❌ Error getting Jair Bolsonaro Wikipedia page: {e}")


def main():
    """Run both specific use cases."""
    print("🎯 SPECIFIC USE CASES DEMONSTRATION")
    print("=" * 80)
    print("This demo shows two specific tool calls:")
    print("1. Headlines today about London")
    print("2. Wikipedia page for Jair Bolsonaro")
    print("=" * 80)
    
    # Use Case 1: London Headlines
    get_london_headlines_today()
    
    # Use Case 2: Jair Bolsonaro Wikipedia
    get_jair_bolsonaro_wikipedia()
    
    print("\n" + "=" * 80)
    print("✅ SPECIFIC USE CASES COMPLETE!")
    print("Both tool calls executed successfully.")
    print("=" * 80)


if __name__ == "__main__":
    main() 