#!/usr/bin/env python3
"""
Interactive Tools Demo
Real-time terminal interface for testing tools directly with input/output visualization.
"""

import sys
import os
import json
import time
from typing import Dict, List, Any

# Add the necessary paths
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src', 'core'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools', 'tool_modules'))

from bbc_rss import get_bbc_public_figures, get_bbc_rss_feed
from wikipedia_api import find_person_wikipedia_page, search_wikipedia, get_wikipedia_page


class InteractiveToolsDemo:
    """Interactive tools testing interface."""
    
    def __init__(self):
        self.tool_calls_made = 0
        self.total_execution_time = 0
        
        # Available tools
        self.tools = {
            "1": {
                "name": "get_bbc_public_figures",
                "description": "Get public figures from BBC RSS feed",
                "function": self._test_bbc_public_figures,
                "params": []
            },
            "2": {
                "name": "get_bbc_rss_feed",
                "description": "Get raw BBC RSS feed data",
                "function": self._test_bbc_rss_feed,
                "params": []
            },
            "3": {
                "name": "find_person_wikipedia_page",
                "description": "Find Wikipedia page for a specific person",
                "function": self._test_wikipedia_person,
                "params": ["person_name"]
            },
            "4": {
                "name": "search_wikipedia",
                "description": "Search Wikipedia for any topic",
                "function": self._test_wikipedia_search,
                "params": ["query"]
            },
            "5": {
                "name": "get_wikipedia_page",
                "description": "Get Wikipedia page by exact title",
                "function": self._test_wikipedia_page,
                "params": ["title"]
            },
            "6": {
                "name": "chained_demo",
                "description": "Demo: Get public figures and find their Wikipedia pages",
                "function": self._test_chained_demo,
                "params": []
            }
        }
    
    def _test_bbc_public_figures(self):
        """Test BBC public figures tool."""
        print("\n🔧 EXECUTING: get_bbc_public_figures")
        print("=" * 60)
        print("📥 Input: No parameters required")
        
        start_time = time.time()
        try:
            result = get_bbc_public_figures()
            execution_time = time.time() - start_time
            
            print(f"⏱️  Execution time: {execution_time:.2f} seconds")
            print(f"📤 Output: Found {result.get('total_figures', 0)} public figures")
            
            if result.get('public_figures'):
                print("\n📋 Sample public figures:")
                for i, figure in enumerate(result['public_figures'][:10], 1):
                    print(f"   {i:2d}. {figure['name']}")
                    if figure.get('title'):
                        print(f"       Title: {figure['title']}")
                    print(f"       Context: {figure['context'][:80]}...")
                    print(f"       Article: {figure['article_link']}")
                    print()
            
            return result
            
        except Exception as e:
            print(f"❌ Tool execution failed: {e}")
            return {"error": str(e)}
    
    def _test_bbc_rss_feed(self):
        """Test BBC RSS feed tool."""
        print("\n🔧 EXECUTING: get_bbc_rss_feed")
        print("=" * 60)
        print("📥 Input: No parameters required")
        
        start_time = time.time()
        try:
            result = get_bbc_rss_feed()
            execution_time = time.time() - start_time
            
            print(f"⏱️  Execution time: {execution_time:.2f} seconds")
            print(f"📤 Output: Retrieved {len(result.get('articles', []))} articles")
            
            if result.get('articles'):
                print("\n📰 Sample articles:")
                for i, article in enumerate(result['articles'][:5], 1):
                    print(f"   {i}. {article['title']}")
                    print(f"      Published: {article['pub_date']}")
                    print(f"      Link: {article['link']}")
                    print()
            
            return result
            
        except Exception as e:
            print(f"❌ Tool execution failed: {e}")
            return {"error": str(e)}
    
    def _test_wikipedia_person(self):
        """Test Wikipedia person search tool."""
        person_name = input("Enter person name: ").strip()
        if not person_name:
            print("❌ No person name provided")
            return
        
        print(f"\n🔧 EXECUTING: find_person_wikipedia_page")
        print("=" * 60)
        print(f"📥 Input: person_name = '{person_name}'")
        
        start_time = time.time()
        try:
            result = find_person_wikipedia_page(person_name)
            execution_time = time.time() - start_time
            
            print(f"⏱️  Execution time: {execution_time:.2f} seconds")
            
            if result.get('success'):
                page_info = result['page_info']
                print(f"📤 Output: Found page '{page_info['title']}'")
                print(f"   📖 URL: {page_info['url']}")
                print(f"   📄 Page ID: {page_info['page_id']}")
                print(f"   📝 Summary: {page_info['extract'][:200]}...")
                
                if result.get('search_results'):
                    print(f"\n🔍 Search results that led to this page:")
                    for i, search_result in enumerate(result['search_results']['results'][:3], 1):
                        print(f"   {i}. {search_result['title']}")
            else:
                print(f"📤 Output: No page found - {result.get('error', 'Unknown error')}")
            
            return result
            
        except Exception as e:
            print(f"❌ Tool execution failed: {e}")
            return {"error": str(e)}
    
    def _test_wikipedia_search(self):
        """Test Wikipedia search tool."""
        query = input("Enter search query: ").strip()
        if not query:
            print("❌ No search query provided")
            return
        
        print(f"\n🔧 EXECUTING: search_wikipedia")
        print("=" * 60)
        print(f"📥 Input: query = '{query}'")
        
        start_time = time.time()
        try:
            result = search_wikipedia(query, limit=5)
            execution_time = time.time() - start_time
            
            print(f"⏱️  Execution time: {execution_time:.2f} seconds")
            
            if result.get('success'):
                print(f"📤 Output: Found {result.get('total_results', 0)} results")
                print(f"\n📋 Search results:")
                for i, search_result in enumerate(result['results'], 1):
                    print(f"   {i}. {search_result['title']}")
                    print(f"      Page ID: {search_result['page_id']}")
                    print(f"      Snippet: {search_result['snippet'][:100]}...")
                    print(f"      URL: {search_result['url']}")
                    print()
            else:
                print(f"📤 Output: Search failed - {result.get('error', 'Unknown error')}")
            
            return result
            
        except Exception as e:
            print(f"❌ Tool execution failed: {e}")
            return {"error": str(e)}
    
    def _test_wikipedia_page(self):
        """Test Wikipedia page retrieval tool."""
        title = input("Enter page title: ").strip()
        if not title:
            print("❌ No page title provided")
            return
        
        print(f"\n🔧 EXECUTING: get_wikipedia_page")
        print("=" * 60)
        print(f"📥 Input: title = '{title}'")
        
        start_time = time.time()
        try:
            result = get_wikipedia_page(title)
            execution_time = time.time() - start_time
            
            print(f"⏱️  Execution time: {execution_time:.2f} seconds")
            
            if result.get('success'):
                print(f"📤 Output: Found page '{result['title']}'")
                print(f"   📖 URL: {result['url']}")
                print(f"   📄 Page ID: {result['page_id']}")
                print(f"   📝 Content: {result['extract'][:300]}...")
            else:
                print(f"📤 Output: Page not found - {result.get('error', 'Unknown error')}")
            
            return result
            
        except Exception as e:
            print(f"❌ Tool execution failed: {e}")
            return {"error": str(e)}
    
    def _test_chained_demo(self):
        """Test chained tool execution demo."""
        print("\n🔧 EXECUTING: Chained Demo - Get public figures and find Wikipedia pages")
        print("=" * 80)
        print("📥 Input: No parameters required")
        
        start_time = time.time()
        
        # Step 1: Get public figures
        print("\n🔄 Step 1: Getting public figures from BBC...")
        try:
            bbc_result = get_bbc_public_figures()
            if bbc_result.get('public_figures'):
                figures = bbc_result['public_figures'][:3]  # Get first 3
                print(f"✅ Found {len(figures)} public figures")
                
                # Step 2: Get Wikipedia pages for each
                print("\n🔄 Step 2: Getting Wikipedia pages...")
                for i, figure in enumerate(figures, 1):
                    print(f"\n   Processing {i}/{len(figures)}: {figure['name']}")
                    try:
                        wiki_result = find_person_wikipedia_page(figure['name'])
                        if wiki_result.get('success'):
                            page_info = wiki_result['page_info']
                            print(f"   ✅ Found: {page_info['title']}")
                            print(f"      URL: {page_info['url']}")
                        else:
                            print(f"   ❌ Not found: {wiki_result.get('error', 'Unknown error')}")
                    except Exception as e:
                        print(f"   ❌ Error: {e}")
                
                execution_time = time.time() - start_time
                print(f"\n⏱️  Total execution time: {execution_time:.2f} seconds")
                print("✅ Chained demo completed successfully!")
                
            else:
                print("❌ No public figures found")
                
        except Exception as e:
            print(f"❌ Chained demo failed: {e}")
    
    def _show_help(self):
        """Show help information."""
        print("\n📚 INTERACTIVE TOOLS DEMO HELP")
        print("=" * 60)
        print("Available tools:")
        for key, tool in self.tools.items():
            print(f"  {key}. {tool['name']}")
            print(f"     {tool['description']}")
            if tool['params']:
                print(f"     Parameters: {', '.join(tool['params'])}")
            else:
                print(f"     Parameters: None")
        print("\nCommands:")
        print("  /help     - Show this help message")
        print("  /stats    - Show execution statistics")
        print("  /quit     - Exit the demo")
        print("  /exit     - Exit the demo")
        print("=" * 60)
    
    def _show_stats(self):
        """Show execution statistics."""
        print("\n📊 EXECUTION STATISTICS")
        print("=" * 40)
        print(f"🔧 Tool calls made: {self.tool_calls_made}")
        print(f"⏱️  Total execution time: {self.total_execution_time:.2f} seconds")
        if self.tool_calls_made > 0:
            avg_time = self.total_execution_time / self.tool_calls_made
            print(f"📈 Average time per tool: {avg_time:.2f} seconds")
        print("=" * 40)
    
    def run(self):
        """Main demo loop."""
        print("🔧 INTERACTIVE TOOLS DEMO")
        print("=" * 60)
        print("Welcome to the Ultimate AI Personal Assistant Tools Demo!")
        print("Test tools directly and see their input/output in real-time.")
        print("Type /help for available tools and commands.")
        print("=" * 60)
        
        while True:
            try:
                # Get user input
                user_input = input("\n🔧 Select tool (1-6) or command: ").strip()
                
                # Handle commands
                if user_input.lower() in ['/quit', '/exit']:
                    print("\n👋 Goodbye! Thanks for testing the tools!")
                    break
                elif user_input.lower() == '/help':
                    self._show_help()
                    continue
                elif user_input.lower() == '/stats':
                    self._show_stats()
                    continue
                elif not user_input:
                    continue
                
                # Execute tool
                if user_input in self.tools:
                    tool = self.tools[user_input]
                    print(f"\n🚀 Executing: {tool['name']}")
                    
                    start_time = time.time()
                    result = tool['function']()
                    execution_time = time.time() - start_time
                    
                    self.tool_calls_made += 1
                    self.total_execution_time += execution_time
                    
                    print(f"\n✅ Tool execution completed in {execution_time:.2f} seconds")
                    
                else:
                    print(f"❌ Unknown tool or command: {user_input}")
                    print("💡 Type /help to see available options.")
                
            except KeyboardInterrupt:
                print("\n\n👋 Demo interrupted. Goodbye!")
                break
            except EOFError:
                print("\n\n👋 End of input. Goodbye!")
                break


def main():
    """Main function to start the interactive tools demo."""
    demo = InteractiveToolsDemo()
    demo.run()


if __name__ == "__main__":
    main() 