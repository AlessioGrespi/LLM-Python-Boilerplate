# LLM Python Boilerplate - Quick Reference

## Model Router Quick Start

```python
from ultimate_llm_toolkit.model_router import model_router

# Basic usage
response = model_router(
    prompt="Your prompt here",
    model="anthropic-sonnet",
    temperature=0.7,
    max_tokens=100
)
print(response['content'])
```

## Common Model Patterns

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

## Tool Usage Patterns

### Direct Tool Calls
```python
from ultimate_llm_toolkit.bbc_rss import get_bbc_public_figures
from ultimate_llm_toolkit.wikipedia_api import search_wikipedia, get_wikipedia_page
from ultimate_llm_toolkit import LLMToolkit

# BBC RSS
bbc_result = get_bbc_public_figures()
print(f"Found {bbc_result['total_figures']} public figures")

# Wikipedia
wiki_result = search_wikipedia("Donald Trump", limit=5)
if wiki_result.get('success'):
    print(f"Found: {wiki_result['results'][0]['title']}")

# Using the toolkit
toolkit = LLMToolkit()
news = toolkit.get_news(category="technology")
print(f"Latest tech news: {news['articles'][0]['title']}")
```

### Tools with Model Router
```python
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
    }
]

response = model_router(
    prompt="Get current public figures and find their Wikipedia pages",
    model="anthropic-sonnet",
    tools=tools,
    temperature=0.7
)
```

## Conversation Patterns

### Simple Conversation
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

response = model_router(
    prompt="Hello!",
    model="anthropic-sonnet",
    messages=messages,
    temperature=0.7
)

messages.append({"role": "user", "content": "Hello!"})
messages.append({"role": "assistant", "content": response['content']})
```

### Multi-turn with Tools
```python
messages = [
    {"role": "system", "content": "You are a research assistant with access to news and Wikipedia data."}
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_bbc_public_figures",
            "description": "Get public figures from BBC RSS feed",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    }
]

# Turn 1
response1 = model_router(
    prompt="Get me current public figures from the news",
    model="anthropic-sonnet",
    messages=messages,
    tools=tools,
    temperature=0.7
)

messages.append({"role": "user", "content": "Get me current public figures from the news"})
messages.append({"role": "assistant", "content": response1['content']})

# Turn 2
response2 = model_router(
    prompt="Tell me more about the first person you found",
    model="anthropic-sonnet",
    messages=messages,
    tools=tools,
    temperature=0.7
)
```

## Chained Tool Patterns

### Manual Chaining
```python
# Step 1: Get data from first tool
bbc_result = get_bbc_public_figures()

# Step 2: Process with second tool
if bbc_result.get('public_figures'):
    for figure in bbc_result['public_figures'][:3]:
        wiki_result = find_person_wikipedia_page(figure['name'])
        if wiki_result.get('success'):
            print(f"{figure['name']}: {wiki_result['page_info']['title']}")

# Step 3: Analyze with AI
analysis_prompt = f"Analyze these figures: {bbc_result['public_figures'][:3]}"
response = model_router(prompt=analysis_prompt, model="anthropic-sonnet")
```

### AI-Driven Chaining
```python
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
    prompt="Get public figures from BBC news and research the first 3 people",
    model="anthropic-sonnet",
    tools=tools,
    temperature=0.7
)
```

## Error Handling Patterns

### Basic Error Handling
```python
try:
    response = model_router(
        prompt="Your prompt",
        model="anthropic-sonnet",
        temperature=0.7
    )
    print(response['content'])
except Exception as e:
    print(f"Error: {e}")
```

### Fallback Detection
```python
response = model_router(
    prompt="Your prompt",
    model="non-existent-model"
)

if response.get('fallback_used'):
    print(f"Warning: Used fallback model {response['model']}")
    print(f"Original model: {response['original_model']}")
    print(f"Reason: {response['fallback_reason']}")
```

### Tool Error Handling
```python
try:
    result = get_bbc_public_figures()
    if result.get('success', True):  # Most tools return success=True by default
        print(f"Found {result['total_figures']} figures")
    else:
        print(f"Tool failed: {result.get('error')}")
except Exception as e:
    print(f"Tool error: {e}")
```

## System Prompt Patterns

### AWS Bedrock System Prompts
```python
response = model_router(
    prompt="What's the weather like?",
    model="llama-3-3-70b",
    system_prompt="You are a helpful weather assistant. Always provide accurate information.",
    temperature=0.7
)
```

### Azure OpenAI System Prompts (via messages)
```python
messages = [
    {"role": "system", "content": "You are a coding assistant. Always provide clear, well-documented code examples."}
]

response = model_router(
    prompt="Write a Python function to sort a list",
    model="gpt-4.1-mini",
    messages=messages,
    temperature=0.7
)
```

## Parameter Patterns

### Common Parameters
```python
response = model_router(
    prompt="Your prompt",
    model="anthropic-sonnet",
    temperature=0.7,      # 0.0-1.0 (creativity)
    max_tokens=100,       # Response length limit
    top_p=0.95,          # Nucleus sampling
    top_k=50,            # Top-k sampling
    stop_sequences=["END", "STOP"]  # Stop generation
)
```

### Model-Specific Parameters
```python
# AWS Bedrock specific
response = model_router(
    prompt="Your prompt",
    model="anthropic-sonnet",
    temperature=0.7,
    max_tokens=100,
    anthropic_version="2023-06-01"  # Claude version
)

# Azure OpenAI specific
response = model_router(
    prompt="Your prompt",
    model="gpt-4.1-mini",
    temperature=0.7,
    max_tokens=100,
    presence_penalty=0.1,  # Reduce repetition
    frequency_penalty=0.1  # Reduce repetition
)
```

## Testing Patterns

### Test Individual Tools
```python
# Test BBC RSS
from ultimate_llm_toolkit.bbc_rss import get_bbc_public_figures
result = get_bbc_public_figures()
print(f"BBC RSS test: {result.get('total_figures', 0)} figures found")

# Test Wikipedia
from ultimate_llm_toolkit.wikipedia_api import search_wikipedia
result = search_wikipedia("Donald Trump", limit=1)
print(f"Wikipedia test: {'Success' if result.get('success') else 'Failed'}")

# Test using toolkit
from ultimate_llm_toolkit import LLMToolkit
toolkit = LLMToolkit()
news = toolkit.get_news()
print(f"News test: {len(news.get('articles', []))} articles found")
```

### Test Model Router
```python
# Test basic functionality
response = model_router(
    prompt="Hello, world!",
    model="mistral-small",
    temperature=0.7
)
print(f"Model router test: {len(response['content'])} characters")

# Test with tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_bbc_public_figures",
            "description": "Get public figures from BBC RSS feed",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    }
]

response = model_router(
    prompt="Get current public figures",
    model="anthropic-sonnet",
    tools=tools,
    temperature=0.7
)
print(f"Tool integration test: {'Success' if response.get('tool_calls') else 'No tools used'}")
```

## Environment Setup

### Required Environment Variables
```env
# AWS Bedrock
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1

# Azure OpenAI
ENDPOINT_URL=https://your-resource.openai.azure.com/
DEPLOYMENT_NAME=your-deployment
AZURE_OPENAI_API_KEY=your_key

# Tool-specific (if needed)
BRAVE_API_KEY=your_brave_key
```

### Check Environment
```python
from ultimate_llm_toolkit.model_router import list_available_models

# Check available models
models = list_available_models()
print(f"AWS models: {len(models['aws'])}")
print(f"Azure models: {len(models['azure'])}")

# Test connection
try:
    response = model_router(
        prompt="Test",
        model="mistral-small",
        max_tokens=10
    )
    print("✅ Environment setup successful")
except Exception as e:
    print(f"❌ Environment setup failed: {e}")
```

## Common Use Cases

### Research Assistant
```python
def research_assistant(query):
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
    bbc_result = get_bbc_public_figures()
    
    if bbc_result.get('public_figures'):
        summary_prompt = f"""
        Summarize the current news based on these public figures:
        {bbc_result['public_figures'][:5]}
        
        Provide a brief overview of what's happening in the news today.
        """
        
        return model_router(
            prompt=summary_prompt,
            model="anthropic-sonnet",
            temperature=0.7
        )
```

### Interactive Chat Bot
```python
def chat_bot():
    messages = [
        {"role": "system", "content": "You are a helpful assistant with access to news and Wikipedia data."}
    ]
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_bbc_public_figures",
                "description": "Get public figures from BBC RSS feed",
                "parameters": {"type": "object", "properties": {}, "required": []}
            }
        }
    ]
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'quit':
            break
            
        messages.append({"role": "user", "content": user_input})
        
        response = model_router(
            prompt="",
            model="anthropic-sonnet",
            messages=messages,
            tools=tools,
            temperature=0.7
        )
        
        print(f"Assistant: {response['content']}")
        messages.append({"role": "assistant", "content": response['content']})
```

## Performance Tips

### Model Selection
- **Fast responses**: `mistral-small`, `gpt-4o-mini`
- **High quality**: `anthropic-sonnet`, `gpt-4`
- **Creative tasks**: `anthropic-haiku`, `gpt-4o`
- **Complex reasoning**: `anthropic-sonnet`, `gpt-4`

### Tool Optimization
- Cache frequently requested data
- Implement rate limiting
- Use appropriate timeouts
- Validate inputs before processing

### Conversation Management
- Keep message history manageable
- Reset conversations for new topics
- Monitor token usage
- Use clear system prompts 