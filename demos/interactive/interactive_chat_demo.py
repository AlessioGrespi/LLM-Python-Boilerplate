#!/usr/bin/env python3
"""
Interactive Chat Demo
Real-time terminal chat with the LLM showing tool calls and their input/output.
"""

import sys
import os
import json
import time
from typing import Dict, List, Any

# Add the necessary paths
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src', 'core'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools', 'tool_modules'))

from model_router import model_router
from bbc_rss import get_bbc_public_figures, bbc_rss_tool
from wikipedia_api import find_person_wikipedia_page, wikipedia_api_tool


class InteractiveChat:
    """Interactive chat interface with tool call visualization."""
    
    def __init__(self):
        self.conversation_history = []
        self.tool_calls_made = 0
        self.total_tokens = 0
        
        # Define available tools
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_bbc_latest_news",
                    "description": "Get the latest BBC news headlines and summaries",
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
                    "name": "get_bbc_news_summary",
                    "description": "Get a summary of current BBC news with categorized articles",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "description": "Filter by category (e.g., 'politics', 'technology', 'sports', 'business')"
                            },
                            "max_articles": {
                                "type": "integer",
                                "description": "Maximum number of articles to return",
                                "default": 10
                            }
                        },
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
        
        # Tool function mapping
        self.tool_functions = {
            "get_bbc_latest_news": self._execute_bbc_latest_news,
            "get_bbc_news_summary": self._execute_bbc_news_summary,
            "find_person_wikipedia_page": self._execute_wikipedia_tool
        }
    
    def _execute_bbc_latest_news(self, **kwargs):
        """Execute BBC latest news tool with detailed logging."""
        print("\n🔧 EXECUTING TOOL: get_bbc_latest_news")
        print("=" * 50)
        print("📥 Input: No parameters required")
        
        start_time = time.time()
        try:
            from bbc_rss import get_bbc_latest_news
            result = get_bbc_latest_news()
            execution_time = time.time() - start_time
            
            print(f"⏱️  Execution time: {execution_time:.2f} seconds")
            print(f"📤 Output: BBC Latest News ({result['total_articles']} articles)")
            
            # Format the result
            output = f"📰 BBC Latest News ({result['total_articles']} articles)\n"
            output += f"🕐 Last updated: {result['last_updated']}\n\n"
            
            # Breaking news
            if result.get('breaking_news'):
                output += "🚨 BREAKING NEWS:\n"
                for i, news in enumerate(result['breaking_news'][:3], 1):
                    output += f"   {i}. {news['title']}\n"
                output += "\n"
            
            # Top stories
            if result.get('top_stories'):
                output += "📋 TOP STORIES:\n"
                for i, story in enumerate(result['top_stories'][:5], 1):
                    output += f"   {i}. {story['title']}\n"
                    output += f"      📝 {story['description'][:100]}...\n"
                    output += f"      🏷️  {story['category']}\n\n"
            
            # Key figures
            if result.get('key_figures'):
                output += "👥 KEY FIGURES MENTIONED:\n"
                for i, figure in enumerate(result['key_figures'][:5], 1):
                    output += f"   {i}. {figure['name']}\n"
            
            print(output)
            return result
            
        except Exception as e:
            print(f"❌ Tool execution failed: {e}")
            return {"error": str(e)}

    def _execute_bbc_news_summary(self, **kwargs):
        """Execute BBC news summary tool with detailed logging."""
        category = kwargs.get('category')
        max_articles = kwargs.get('max_articles', 10)
        
        print(f"\n🔧 EXECUTING TOOL: get_bbc_news_summary")
        print("=" * 50)
        print(f"📥 Input: category = '{category}', max_articles = {max_articles}")
        
        start_time = time.time()
        try:
            from bbc_rss import get_bbc_news_summary
            result = get_bbc_news_summary(category, max_articles)
            execution_time = time.time() - start_time
            
            print(f"⏱️  Execution time: {execution_time:.2f} seconds")
            print(f"📤 Output: BBC News Summary ({result['total_articles']} articles)")
            
            # Format the result
            output = f"📰 BBC News Summary\n"
            if category:
                output += f"🏷️  Category: {category}\n"
            output += f"📊 Total articles: {result['total_articles']}\n"
            output += f"🕐 Last updated: {result['last_updated']}\n\n"
            
            # Categories
            if result.get('categories'):
                output += "📂 CATEGORIES:\n"
                for cat, articles in result['categories'].items():
                    output += f"   📁 {cat} ({len(articles)} articles)\n"
                    for i, article in enumerate(articles[:3], 1):  # Show first 3 per category
                        output += f"      {i}. {article['title']}\n"
                    output += "\n"
            
            # Top headlines
            if result.get('top_headlines'):
                output += "📋 TOP HEADLINES:\n"
                for i, headline in enumerate(result['top_headlines'][:5], 1):
                    output += f"   {i}. {headline}\n"
            
            print(output)
            return result
            
        except Exception as e:
            print(f"❌ Tool execution failed: {e}")
            return {"error": str(e)}
    
    def _execute_wikipedia_tool(self, **kwargs):
        """Execute Wikipedia tool with detailed logging."""
        person_name = kwargs.get('person_name', '')
        print(f"\n🔧 EXECUTING TOOL: find_person_wikipedia_page")
        print("=" * 50)
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
                print(f"   📝 Summary: {page_info['extract'][:100]}...")
            else:
                print(f"📤 Output: No page found - {result.get('error', 'Unknown error')}")
            
            return result
            
        except Exception as e:
            print(f"❌ Tool execution failed: {e}")
            return {"error": str(e)}
    
    def _execute_tool_call(self, tool_call):
        """Execute a tool call and return the result."""
        # Handle different tool call formats (AWS Bedrock vs Azure OpenAI)
        if hasattr(tool_call, 'function'):
            # Azure OpenAI format
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
        else:
            # AWS Bedrock format
            tool_name = tool_call.get('name', '')
            tool_args = tool_call.get('input', {})
        
        if tool_name in self.tool_functions:
            return self.tool_functions[tool_name](**tool_args)
        else:
            print(f"❌ Unknown tool: {tool_name}")
            return {"error": f"Unknown tool: {tool_name}"}
    
    def _process_response(self, response):
        """Process the model response and handle tool calls."""
        print(f"\n🤖 ASSISTANT RESPONSE:")
        print("=" * 50)
        
        # Show response content
        content = response.get('content', '')
        if content:
            print(f"💬 {content}")
        else:
            print("💬 (No text response)")
        
        # Handle tool calls
        tool_calls = response.get('tool_calls', [])
        if tool_calls:
            print(f"\n🔧 TOOL CALLS DETECTED: {len(tool_calls)}")
            self.tool_calls_made += len(tool_calls)
            
            tool_results = []
            for i, tool_call in enumerate(tool_calls, 1):
                print(f"\n🔄 Processing tool call {i}/{len(tool_calls)}...")
                result = self._execute_tool_call(tool_call)
                tool_results.append(result)
            
            # Add tool calls and results to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": content,
                "tool_calls": tool_calls
            })
            
            # Add tool results to conversation history
            for tool_call, result in zip(tool_calls, tool_results):
                # Handle different tool call formats for ID extraction
                if hasattr(tool_call, 'id'):
                    # Azure OpenAI format
                    tool_call_id = tool_call.id
                else:
                    # AWS Bedrock format
                    tool_call_id = tool_call.get('id', '')
                
                tool_result_content = json.dumps(result, indent=2)
                
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": tool_result_content
                })
            
            # If we have tool results, make another call to the model with the results
            if tool_results:
                print(f"\n🔄 Making follow-up call with tool results...")

                try:
                    follow_up_response = model_router(
                        prompt="",  # No new prompt needed
                        model="gpt-4.1-mini",
                        messages=self.conversation_history,
                        tools=self.tools,
                        max_tokens=500,
                        temperature=0.7
                    )
                    
                    # Process the follow-up response
                    self._process_follow_up_response(follow_up_response)
                    
                except Exception as e:
                    print(f"\n❌ Follow-up call failed: {e}")
            
            print(f"\n✅ Tool execution complete. {len(tool_results)} tools executed.")
        else:
            # No tool calls, just add the assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": content
            })
        
        # Show usage statistics
        usage = response.get('usage', {})
        if usage:
            self.total_tokens += usage.get('total_tokens', 0)
            print(f"\n📊 Usage: {usage.get('prompt_tokens', 0)} prompt + {usage.get('completion_tokens', 0)} completion = {usage.get('total_tokens', 0)} total tokens")
    
    def _process_follow_up_response(self, response):
        """Process the follow-up response after tool execution."""
        print(f"\n🤖 FOLLOW-UP RESPONSE:")
        print("=" * 50)
        
        # Show response content
        content = response.get('content', '')
        if content:
            print(f"💬 {content}")
        else:
            print("💬 (No text response)")
        
        # Add the follow-up response to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": content
        })
        
        # Show usage statistics
        usage = response.get('usage', {})
        if usage:
            self.total_tokens += usage.get('total_tokens', 0)
            print(f"\n📊 Follow-up Usage: {usage.get('prompt_tokens', 0)} prompt + {usage.get('completion_tokens', 0)} completion = {usage.get('total_tokens', 0)} total tokens")
    
    def _show_help(self):
        """Show help information."""
        print("\n📚 INTERACTIVE CHAT HELP")
        print("=" * 50)
        print("Available commands:")
        print("  /help     - Show this help message")
        print("  /tools    - Show available tools")
        print("  /stats    - Show conversation statistics")
        print("  /clear    - Clear conversation history")
        print("  /quit     - Exit the chat")
        print("  /exit     - Exit the chat")
        print("\nExample prompts:")
        print("  • 'Get me the public figures from BBC news'")
        print("  • 'Find Wikipedia page for Donald Trump'")
        print("  • 'Get public figures and find Wikipedia pages for the first 3'")
        print("  • 'What's the weather like?' (no tools available)")
        print("=" * 50)
    
    def _show_tools(self):
        """Show available tools."""
        print("\n🔧 AVAILABLE TOOLS")
        print("=" * 50)
        for i, tool in enumerate(self.tools, 1):
            func = tool['function']
            print(f"{i}. {func['name']}")
            print(f"   Description: {func['description']}")
            if func.get('parameters', {}).get('properties'):
                print(f"   Parameters: {list(func['parameters']['properties'].keys())}")
            else:
                print(f"   Parameters: None")
        print("=" * 50)
    
    def _show_stats(self):
        """Show conversation statistics."""
        print("\n📊 CONVERSATION STATISTICS")
        print("=" * 50)
        print(f"💬 Messages exchanged: {len(self.conversation_history)}")
        print(f"🔧 Tool calls made: {self.tool_calls_made}")
        print(f"🧠 Total tokens used: {self.total_tokens}")
        print("=" * 50)
    
    def _clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        self.tool_calls_made = 0
        self.total_tokens = 0
        print("\n🧹 Conversation history cleared!")
    
    def chat(self):
        """Main chat loop."""
        print("🎭 INTERACTIVE CHAT DEMO")
        print("=" * 60)
        print("Welcome to the Ultimate AI Personal Assistant!")
        print("Type /help for available commands.")
        print("Type /quit to exit.")
        print("=" * 60)
        
        while True:
            try:
                # Get user input
                user_input = input("\n👤 You: ").strip()
                
                # Handle commands
                if user_input.lower() in ['/quit', '/exit']:
                    print("\n👋 Goodbye! Thanks for chatting!")
                    break
                elif user_input.lower() == '/help':
                    self._show_help()
                    continue
                elif user_input.lower() == '/tools':
                    self._show_tools()
                    continue
                elif user_input.lower() == '/stats':
                    self._show_stats()
                    continue
                elif user_input.lower() == '/clear':
                    self._clear_history()
                    continue
                elif not user_input:
                    continue
                
                # Add to conversation history (provider-agnostic format)
                self.conversation_history.append({"role": "user", "content": user_input})
                
                # Make API call
                print(f"\n🔄 Processing your request...")
                start_time = time.time()
                

                
                try:
                    response = model_router(
                        prompt=user_input,
                        model="gpt-4.1-mini",
                        messages=self.conversation_history,
                        tools=self.tools,
                        max_tokens=500,
                        temperature=0.7
                    )
                    
                    processing_time = time.time() - start_time
                    print(f"⏱️  Processing time: {processing_time:.2f} seconds")
                    
                    # Process the response
                    self._process_response(response)
                    
                except Exception as e:
                    print(f"\n❌ Error: {e}")
                    print("💡 Try a different prompt or check your connection.")
                
            except KeyboardInterrupt:
                print("\n\n👋 Chat interrupted. Goodbye!")
                break
            except EOFError:
                print("\n\n👋 End of input. Goodbye!")
                break


def main():
    """Main function to start the interactive chat."""
    chat = InteractiveChat()
    chat.chat()


if __name__ == "__main__":
    main() 