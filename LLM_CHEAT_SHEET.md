# LLM Python Boilerplate - LLM Cheat Sheet

A comprehensive cheat sheet for LLMs to understand and use the library effectively. This document assumes you're using `model_router` for all interactions.

## 🚀 Quick Installation

### From GitHub
```bash
pip install git+https://github.com/AlessioGrespi/LLM-Python-Boilerplate.git
```

### From Local Development
```bash
git clone https://github.com/AlessioGrespi/LLM-Python-Boilerplate.git
cd LLM-Python-Boilerplate
pip install -e .
```

## ⚙️ Environment Setup (.env file)

Create a `.env` file in your project root:

```env
# AWS Bedrock Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
```

## 🔥 Quick Start - Single Query

```python
from ultimate_llm_toolkit.model_router import model_router

# Simple query with AWS Bedrock
response = model_router(
    prompt="What is the capital of France?",
    model="anthropic-sonnet",
    temperature=0.7,
    max_tokens=100
)
print(response['content'])

# Simple query with Azure OpenAI
response = model_router(
    prompt="Explain quantum computing in simple terms",
    model="gpt-4.1-mini",
    temperature=0.5,
    max_tokens=150
)
print(response['content'])
```

## 💬 Simple Conversation

```python
from ultimate_llm_toolkit.model_router import model_router

# Initialize conversation
messages = [
    {"role": "system", "content": "You are a helpful coding assistant."},
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language."},
    {"role": "user", "content": "What are its main features?"}
]

# Continue conversation
response = model_router(
    prompt="",  # Empty prompt when using messages
    model="gpt-4.1-mini",
    messages=messages,
    temperature=0.7
)

# Add to conversation history
messages.append({"role": "user", "content": "What are its main features?"})
messages.append({"role": "assistant", "content": response['content']})
```

## 🛠️ Tool Use with Model Router

### Tools Index

```python
from ultimate_llm_toolkit.model_router import model_router

# Define available tools
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
            "name": "search_wikipedia",
            "description": "Search Wikipedia for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum results (default: 5)"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# Use tools with model router
response = model_router(
    prompt="Get me current public figures from BBC news",
    model="anthropic-sonnet",
    tools=tools,
    temperature=0.7
)
```

### AI-Driven Tool Chaining

```python
from ultimate_llm_toolkit.model_router import model_router

# Define comprehensive tool set
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
            "name": "search_wikipedia",
            "description": "Search Wikipedia for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {"type": "integer", "description": "Maximum results"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_wikipedia_page",
            "description": "Get specific Wikipedia page content",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Page title"}
                },
                "required": ["title"]
            }
        }
    }
]

# Let AI orchestrate tool usage
response = model_router(
    prompt="Get public figures from BBC news and research the first 3 people on Wikipedia",
    model="anthropic-sonnet",
    tools=tools,
    temperature=0.7
)
```

## 🎯 Available Models

### AWS Bedrock Models
```python
# Claude models
response = model_router(prompt="...", model="anthropic-sonnet")
response = model_router(prompt="...", model="anthropic-haiku")

# Llama models
response = model_router(prompt="...", model="llama-3-3-70b")
response = model_router(prompt="...", model="llama-3-2-3b")

# Mistral models
response = model_router(prompt="...", model="mistral-large")
response = model_router(prompt="...", model="mistral-small")
```

### Azure OpenAI Models
```python
# GPT models
response = model_router(prompt="...", model="gpt-4")
response = model_router(prompt="...", model="gpt-4o-mini")
response = model_router(prompt="...", model="gpt-3.5-turbo")

# Claude models
response = model_router(prompt="...", model="claude-3-sonnet")
response = model_router(prompt="...", model="claude-3-haiku")
```

## 🔧 Advanced Patterns

### System Prompts (AWS Bedrock)
```python
response = model_router(
    prompt="What's the weather like?",
    model="llama-3-3-70b",
    system_prompt="You are a helpful weather assistant. Always provide accurate information.",
    temperature=0.7
)
```

### Custom Parameters
```python
response = model_router(
    prompt="Write a creative story about a robot",
    model="anthropic-haiku",
    temperature=0.9,
    max_tokens=300,
    top_p=0.95,
    top_k=50,
    stop_sequences=["THE END", "END OF STORY"]
)
```

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

## 📊 Response Format

All responses follow this structure:
```python
{
    "content": "The model's response text",
    "tool_calls": [...],  # Only present if tools were used
    "usage": {
        "prompt_tokens": 10,
        "completion_tokens": 50,
        "total_tokens": 60
    },
    "model": "model-name",
    "provider": "aws" or "azure"
}
```

## 🚨 Important Notes

### Tool Calling Limitations
- **AWS Bedrock**: Tool calling through model_router needs refinement
- **Azure OpenAI**: Full tool calling support available
- **Fallback**: Automatically falls back to `mistral-small` on errors

### Message Format
- **AWS Bedrock**: Expects specific message format, system role not supported
- **Azure OpenAI**: Standard OpenAI message format
- **Content Field**: AWS Bedrock expects list of dicts with "text" key

### Environment Variables
- **Required**: AWS credentials for Bedrock, Azure credentials for OpenAI
- **Optional**: Tool-specific API keys (Brave, Weather, etc.)
- **Validation**: Credentials validated at runtime, not import time

## 🔍 Helper Functions

```python
from ultimate_llm_toolkit.model_router import list_available_models, add_model_mapping

# List available models
models = list_available_models()
print(f"AWS models: {models['aws']}")
print(f"Azure models: {models['azure']}")

# Add custom model mapping
add_model_mapping("my-custom-model", "azure")
```

## 💡 Best Practices

1. **Start Simple**: Begin with basic queries before adding tools
2. **Handle Errors**: Always implement proper error handling
3. **Monitor Usage**: Check token usage and API costs
4. **Use Fallbacks**: Leverage automatic fallback for reliability
5. **Validate Inputs**: Check tool parameters before execution
6. **Cache Results**: Implement caching for frequently requested data

## 🎯 Common Use Cases

### Research Assistant
```python
def research_assistant(query):
    tools = [/* tool definitions */]
    return model_router(
        prompt=query,
        model="anthropic-sonnet",
        tools=tools,
        temperature=0.7
    )
```

### News Summarizer
```python
def news_summarizer():
    # Get news data first
    # Then use AI to summarize
    response = model_router(
        prompt="Summarize this news data...",
        model="anthropic-sonnet",
        temperature=0.7
    )
    return response
```

### Interactive Chat Bot
```python
def chat_bot():
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    tools = [/* tool definitions */]
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'quit':
            break
            
        response = model_router(
            prompt=user_input,
            model="anthropic-sonnet",
            messages=messages,
            tools=tools,
            temperature=0.7
        )
        
        print(f"Assistant: {response['content']}")
        messages.append({"role": "user", "content": user_input})
        messages.append({"role": "assistant", "content": response['content']})
```

---

**Remember**: This library is designed for **demonstration purposes**. The tools provided are examples to show how to integrate external APIs with LLMs, not production-ready tools for end users.
