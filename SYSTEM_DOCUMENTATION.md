# Ultimate AI Personal Assistant - System Documentation

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Model Router](#model-router)
4. [Tool System](#tool-system)
5. [Conversation Management](#conversation-management)
6. [Building New Tools](#building-new-tools)
7. [Best Practices](#best-practices)
8. [Examples](#examples)
9. [Troubleshooting](#troubleshooting)

## Overview

The Ultimate AI Personal Assistant is a sophisticated system that provides:
- **Unified Model Interface**: Seamlessly switch between AWS Bedrock and Azure OpenAI models
- **Modular Tool System**: Extensible tools for web search, news, Wikipedia, and more
- **Chained Tool Execution**: Combine multiple tools for complex workflows
- **Conversation Management**: Maintain context across multiple interactions
- **Automatic Fallback**: Robust error handling with automatic model fallback

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Model Router  │───▶│   Tool System   │───▶│  External APIs  │
│                 │    │                 │    │                 │
│ • AWS Bedrock   │    │ • BBC RSS       │    │ • Wikipedia     │
│ • Azure OpenAI  │    │ • Web Search    │    │ • News APIs     │
│ • Fallback      │    │ • Time/Date     │    │ • Weather APIs  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│  Conversation   │    │   Tool Router   │
│   Management    │    │                 │
│                 │    │ • Tool Registry │
│ • Message Hist  │    │ • Function Map  │
│ • Context       │    │ • Execution     │
└─────────────────┘    └─────────────────┘
```

## Model Router

The model router provides a unified interface for different AI providers.

### Basic Usage

```python
from config.model_router import model_router

# Simple prompt
response = model_router(
    prompt="What is the capital of France?",
    model="anthropic-sonnet",
    temperature=0.7,
    max_tokens=100
)
print(response['content'])
```

### Supported Models

**AWS Bedrock Models:**
- `anthropic-sonnet`, `anthropic-haiku` (Claude)
- `amazon-premier` (Titan)
- `llama-3-2-3b`, `llama-3-3-70b`, `llama-3-1-70b` (Meta Llama)
- `mistral-large`, `mistral-small`, `mixtral-8x7b` (Mistral)
- `deepseek` (DeepSeek)
- `cohere.command-r-v1:0`, `cohere.command-r-plus-v1:0` (Cohere)

**Azure OpenAI Models:**
- `gpt-4`, `gpt-4-turbo`, `gpt-4o`, `gpt-4o-mini`
- `gpt-3.5-turbo`, `gpt-35-turbo`, `gpt-4.1-mini`
- `claude-3-sonnet`, `claude-3-haiku`, `claude-3-opus`

### Advanced Features

**With Message History:**
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language."},
    {"role": "user", "content": "What are its features?"}
]

response = model_router(
    prompt="",
    model="gpt-4.1-mini",
    messages=messages,
    temperature=0.7
)
```

**With System Prompt (AWS Bedrock):**
```python
response = model_router(
    prompt="What's the weather like?",
    model="llama-3-3-70b",
    system_prompt="You are a weather assistant. Provide accurate information.",
    temperature=0.7
)
```

**Automatic Fallback:**
```python
response = model_router(
    prompt="Hello world",
    model="non-existent-model"  # Will fallback to mistral-small
)

if response.get('fallback_used'):
    print(f"Fell back from {response['original_model']} to {response['model']}")
    print(f"Reason: {response['fallback_reason']}")
```

## Tool System

The tool system provides modular, extensible functionality for external data access.

### Available Tools

**BBC RSS Tool:**
```python
from tools.tool_modules.bbc_rss import get_bbc_public_figures

# Get public figures from BBC news
result = get_bbc_public_figures()
print(f"Found {result['total_figures']} public figures")
```

**Wikipedia API Tool:**
```python
from tools.tool_modules.wikipedia_api import find_person_wikipedia_page

# Find Wikipedia page for a person
result = find_person_wikipedia_page("Donald Trump")
if result.get('success'):
    print(f"Found: {result['page_info']['title']}")
    print(f"URL: {result['page_info']['url']}")
```

**Web Search Tool:**
```python
from tools.tool_modules.web_search_brave import search_web

# Search the web
results = search_web("latest AI developments", count=5)
for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
```

### Tool Registry

The tool registry (`tools/config/tool_index.py`) defines all available tools:

```python
from tools.config.tool_index import get_tool_info, list_available_tools

# List all available tools
tools = list_available_tools()
print(f"Available tools: {tools}")

# Get tool information
tool_info = get_tool_info("bbc_rss")
print(f"BBC RSS functions: {list(tool_info['functions'].keys())}")
```

## Conversation Management

### Multi-turn Conversations

```python
# Initialize conversation
messages = [
    {"role": "system", "content": "You are a helpful research assistant."}
]

# Turn 1: Initial request
response1 = model_router(
    prompt="Can you help me research current political figures?",
    model="anthropic-sonnet",
    messages=messages,
    temperature=0.7
)

# Add to conversation history
messages.append({"role": "user", "content": "Can you help me research current political figures?"})
messages.append({"role": "assistant", "content": response1['content']})

# Turn 2: Follow-up
response2 = model_router(
    prompt="Tell me more about Donald Trump specifically.",
    model="anthropic-sonnet",
    messages=messages,
    temperature=0.7
)
```

### Conversation with Tools

```python
# Define tools for the conversation
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
            "description": "Find Wikipedia page for a person",
            "parameters": {
                "type": "object",
                "properties": {
                    "person_name": {
                        "type": "string",
                        "description": "Name of the person"
                    }
                },
                "required": ["person_name"]
            }
        }
    }
]

# Conversation with tool access
response = model_router(
    prompt="Get me information about current political figures in the news.",
    model="anthropic-sonnet",
    tools=tools,
    temperature=0.7
)
```

## Building New Tools

### Tool Structure

Each tool follows this structure:

```
tools/tool_modules/
├── your_tool.py          # Main tool implementation
└── __init__.py           # Module initialization
```

### Creating a New Tool

1. **Create the tool module:**

```python
# tools/tool_modules/weather_tool.py
import requests
from typing import Dict, Any

def get_weather(location: str) -> Dict[str, Any]:
    """
    Get weather information for a location.
    
    Args:
        location (str): City name or coordinates
        
    Returns:
        Dict[str, Any]: Weather information
    """
    try:
        # Your API call here
        response = requests.get(f"https://api.weatherapi.com/v1/current.json?key=YOUR_KEY&q={location}")
        data = response.json()
        
        return {
            "success": True,
            "location": location,
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "humidity": data["current"]["humidity"]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def weather_tool() -> Dict[str, Any]:
    """Tool function for model router integration."""
    return {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name or coordinates"
                }
            },
            "required": ["location"]
        }
    }
```

2. **Register the tool in the tool index:**

```python
# Add to tools/config/tool_index.py
TOOL_REGISTRY["weather_tool"] = {
    "name": "Weather Tool",
    "description": "Get current weather information",
    "module": "tools.tool_modules.weather_tool",
    "functions": {
        "get_weather": {
            "description": "Get current weather for a location",
            "parameters": {
                "location": {
                    "type": "string",
                    "description": "City name or coordinates",
                    "required": True
                }
            }
        }
    }
}
```

3. **Test the tool:**

```python
# Test direct usage
from tools.tool_modules.weather_tool import get_weather

result = get_weather("London")
print(f"Weather in London: {result}")

# Test with model router
tools = [weather_tool()]
response = model_router(
    prompt="What's the weather like in Paris?",
    model="anthropic-sonnet",
    tools=tools,
    temperature=0.7
)
```

### Tool Best Practices

1. **Error Handling**: Always return structured responses with success/error indicators
2. **Documentation**: Provide clear descriptions and parameter documentation
3. **Rate Limiting**: Implement appropriate rate limiting for external APIs
4. **Caching**: Consider caching for frequently requested data
5. **Validation**: Validate input parameters before processing

## Chained Tools

### Manual Chaining

```python
# Step 1: Get public figures from BBC
from tools.tool_modules.bbc_rss import get_bbc_public_figures
from tools.tool_modules.wikipedia_api import find_person_wikipedia_page

bbc_result = get_bbc_public_figures()
if bbc_result.get('public_figures'):
    # Step 2: Get Wikipedia pages for each figure
    for figure in bbc_result['public_figures'][:3]:
        wiki_result = find_person_wikipedia_page(figure['name'])
        if wiki_result.get('success'):
            print(f"{figure['name']}: {wiki_result['page_info']['title']}")
```

### AI-Driven Chaining

```python
# Let the AI decide which tools to use and in what order
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_bbc_public_figures",
            "description": "Get public figures from BBC RSS feed",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_person_wikipedia_page",
            "description": "Find Wikipedia page for a person",
            "parameters": {
                "type": "object",
                "properties": {
                    "person_name": {"type": "string", "description": "Person name"}
                },
                "required": ["person_name"]
            }
        }
    }
]

response = model_router(
    prompt="Get public figures from BBC news and find Wikipedia pages for the first 3 people.",
    model="anthropic-sonnet",
    tools=tools,
    temperature=0.7
)
```

## Best Practices

### Model Selection

1. **For General Tasks**: Use `anthropic-sonnet` or `gpt-4.1-mini`
2. **For Creative Tasks**: Use `anthropic-haiku` or `gpt-4o`
3. **For Fast Responses**: Use `mistral-small` or `gpt-4o-mini`
4. **For Complex Reasoning**: Use `anthropic-sonnet` or `gpt-4`

### Tool Usage

1. **Start Simple**: Begin with single tool calls before chaining
2. **Validate Results**: Always check tool response success indicators
3. **Handle Errors**: Implement proper error handling for tool failures
4. **Optimize Performance**: Use appropriate timeouts and caching

### Conversation Management

1. **Maintain Context**: Keep relevant message history
2. **Clear Instructions**: Provide clear system prompts
3. **Manage Length**: Monitor conversation length to avoid token limits
4. **Reset When Needed**: Start fresh conversations for new topics

### Error Handling

```python
try:
    response = model_router(
        prompt="Your prompt here",
        model="anthropic-sonnet",
        tools=tools,
        temperature=0.7
    )
    
    if response.get('fallback_used'):
        print(f"Warning: Used fallback model {response['model']}")
    
    print(response['content'])
    
except ValueError as e:
    print(f"Model error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Examples

### Complete Research Workflow

```python
from config.model_router import model_router
from tools.tool_modules.bbc_rss import get_bbc_public_figures
from tools.tool_modules.wikipedia_api import find_person_wikipedia_page

def research_workflow():
    """Complete research workflow example."""
    
    # Step 1: Get current news figures
    print("📰 Getting current public figures...")
    bbc_result = get_bbc_public_figures()
    
    if not bbc_result.get('public_figures'):
        print("No public figures found")
        return
    
    # Step 2: Research each figure
    research_results = []
    for figure in bbc_result['public_figures'][:3]:
        print(f"\n🔍 Researching: {figure['name']}")
        
        # Get Wikipedia information
        wiki_result = find_person_wikipedia_page(figure['name'])
        
        if wiki_result.get('success'):
            research_results.append({
                'name': figure['name'],
                'bbc_context': figure['context'],
                'wikipedia_info': wiki_result['page_info']
            })
    
    # Step 3: AI analysis
    if research_results:
        analysis_prompt = f"""
        I've researched {len(research_results)} public figures from current news.
        
        Results:
        {research_results}
        
        Please provide a brief analysis of these figures and their current relevance.
        """
        
        response = model_router(
            prompt=analysis_prompt,
            model="anthropic-sonnet",
            temperature=0.7
        )
        
        print("\n🤖 AI Analysis:")
        print(response['content'])

# Run the workflow
research_workflow()
```

### Interactive Chat Bot

```python
def interactive_chat():
    """Interactive chat with tool access."""
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_bbc_public_figures",
                "description": "Get public figures from BBC RSS feed",
                "parameters": {"type": "object", "properties": {}, "required": []}
            }
        },
        {
            "type": "function",
            "function": {
                "name": "find_person_wikipedia_page",
                "description": "Find Wikipedia page for a person",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "person_name": {"type": "string", "description": "Person name"}
                    },
                    "required": ["person_name"]
                }
            }
        }
    ]
    
    messages = [
        {"role": "system", "content": "You are a helpful research assistant with access to news and Wikipedia data."}
    ]
    
    print("🤖 Interactive Research Assistant")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            break
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = model_router(
                prompt="",
                model="anthropic-sonnet",
                messages=messages,
                tools=tools,
                temperature=0.7
            )
            
            print(f"Assistant: {response['content']}\n")
            messages.append({"role": "assistant", "content": response['content']})
            
        except Exception as e:
            print(f"Error: {e}\n")

# Run interactive chat
interactive_chat()
```

## Troubleshooting

### Common Issues

1. **Model Not Found**
   ```python
   # Check available models
   from config.model_router import list_available_models
   models = list_available_models()
   print(f"AWS models: {models['aws']}")
   print(f"Azure models: {models['azure']}")
   ```

2. **Tool Not Working**
   ```python
   # Test tool directly
   from tools.tool_modules.bbc_rss import get_bbc_public_figures
   result = get_bbc_public_figures()
   print(f"Tool result: {result}")
   ```

3. **Authentication Errors**
   - Check environment variables
   - Verify API keys are valid
   - Ensure proper AWS/Azure configuration

4. **Rate Limiting**
   - Implement retry logic
   - Use different models
   - Add delays between requests

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Test with debug info
response = model_router(
    prompt="Test prompt",
    model="anthropic-sonnet",
    temperature=0.7
)
```

### Environment Setup

Ensure your `.env` file contains:

```env
# AWS Bedrock
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1

# Azure OpenAI
ENDPOINT_URL=https://your-resource.openai.azure.com/
DEPLOYMENT_NAME=your-deployment
AZURE_OPENAI_API_KEY=your_key

# Tool-specific keys (if needed)
BRAVE_API_KEY=your_brave_key
WEATHER_API_KEY=your_weather_key
```

## Conclusion

This documentation provides a comprehensive guide to using the Ultimate AI Personal Assistant system. The modular architecture makes it easy to extend with new tools and models while maintaining a consistent interface.

For additional examples and testing, see the `tests/` directory for comprehensive test cases and demonstrations.

Remember to:
- Start with simple examples before building complex workflows
- Always handle errors gracefully
- Monitor API usage and costs
- Keep tools and models updated
- Test thoroughly before deploying to production 