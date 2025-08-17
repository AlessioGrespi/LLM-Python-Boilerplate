# Ultimate LLM Toolkit - Usage Examples

This document shows how to use the Ultimate LLM Toolkit in your own projects.

## Installation

### From Local Development
```bash
# Clone the repository
git clone https://github.com/AlessioGrespi/LLM-Python-Boilerplate.git
cd LLM-Python-Boilerplate

# Install in development mode
pip install -e .
```

### From GitHub
```bash
pip install git+https://github.com/AlessioGrespi/LLM-Python-Boilerplate.git
```

## Basic Usage

### 1. Simple Chat with LLM

```python
from ultimate_llm_toolkit import LLMToolkit

# Create toolkit instance
toolkit = LLMToolkit()

# Chat with default model (anthropic-sonnet)
response = toolkit.chat("What is the capital of France?")
print(response['content'])

# Chat with specific model
response = toolkit.chat("Explain quantum computing", model="gpt-4.1-mini")
print(response['content'])
```

### 2. Using Different Models

```python
from ultimate_llm_toolkit import LLMToolkit

toolkit = LLMToolkit()

# AWS Bedrock models
response = toolkit.chat("Hello!", model="anthropic-sonnet")
response = toolkit.chat("Hello!", model="llama-3-3-70b")
response = toolkit.chat("Hello!", model="mistral-large")

# Azure OpenAI models
response = toolkit.chat("Hello!", model="gpt-4.1-mini")
```

### 3. Conversation Management

```python
from ultimate_llm_toolkit import LLMToolkit

toolkit = LLMToolkit()

# Start a conversation
response1 = toolkit.chat("My name is Alice")
response2 = toolkit.chat("What's my name?")

# The toolkit automatically maintains conversation history
print(f"Response: {response2['content']}")
```

### 4. Using Tools

#### BBC News Tool
```python
from ultimate_llm_toolkit import get_bbc_latest_news, get_bbc_news_summary

# Get latest news
news = get_bbc_latest_news()
print(f"Latest news: {news['articles'][0]['title']}")

# Get news summary by category
tech_news = get_bbc_news_summary(category="technology")
print(f"Tech news summary: {tech_news['summary']}")
```

#### Wikipedia Tool
```python
from ultimate_llm_toolkit import search_wikipedia, get_wikipedia_page

# Search Wikipedia
results = search_wikipedia("artificial intelligence", limit=5)
for result in results['results']:
    print(f"- {result['title']}: {result['snippet']}")

# Get specific page content
page = get_wikipedia_page("Python (programming language)")
print(f"Page content: {page['content'][:200]}...")
```

### 5. Advanced Configuration

```python
from ultimate_llm_toolkit import LLMToolkit

toolkit = LLMToolkit(default_model="gpt-4.1-mini")

# Custom parameters
response = toolkit.chat(
    "Write a short story",
    temperature=0.9,
    max_tokens=500,
    system_prompt="You are a creative storyteller"
)
```

### 6. Direct Model Router Usage

```python
from ultimate_llm_toolkit import model_router

# Direct model calls
response = model_router(
    prompt="What is machine learning?",
    model="anthropic-sonnet",
    temperature=0.7,
    max_tokens=200
)

print(f"Response: {response['content']}")
print(f"Provider: {response['provider']}")
print(f"Model: {response['model']}")
```

## Environment Setup

Create a `.env` file in your project:

```bash
# AWS Bedrock (for AWS models)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1

# Azure OpenAI (for Azure models)
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
```

## Error Handling

```python
from ultimate_llm_toolkit import LLMToolkit

toolkit = LLMToolkit()

try:
    response = toolkit.chat("Hello!", model="unknown-model")
except ValueError as e:
    print(f"Model error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Available Models

### AWS Bedrock Models
- `anthropic-sonnet` - Claude 3 Sonnet
- `anthropic-haiku` - Claude 3 Haiku
- `llama-3-3-70b` - Llama 3 70B
- `llama-3-2-3b` - Llama 3 2B
- `mistral-large` - Mistral Large
- `mistral-small` - Mistral Small
- `mixtral-8x7b` - Mixtral 8x7B

### Azure OpenAI Models
- `gpt-4.1-mini` - GPT-4.1 Mini
- Any custom deployment name you have configured

## Tool Functions

### BBC RSS Tools
- `get_bbc_latest_news()` - Get latest news
- `get_bbc_news_summary(category)` - Get news by category
- `get_bbc_public_figures()` - Get public figures news
- `get_bbc_rss_feed(category)` - Get raw RSS feed

### Wikipedia Tools
- `search_wikipedia(query, limit)` - Search Wikipedia
- `get_wikipedia_page(title)` - Get specific page content
- `get_multiple_people_wikipedia_pages(names)` - Get multiple pages

## Integration Examples

### Flask Web Application
```python
from flask import Flask, request, jsonify
from ultimate_llm_toolkit import LLMToolkit

app = Flask(__name__)
toolkit = LLMToolkit()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    response = toolkit.chat(
        data['message'],
        model=data.get('model', 'anthropic-sonnet')
    )
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
```

### FastAPI Application
```python
from fastapi import FastAPI
from pydantic import BaseModel
from ultimate_llm_toolkit import LLMToolkit

app = FastAPI()
toolkit = LLMToolkit()

class ChatRequest(BaseModel):
    message: str
    model: str = "anthropic-sonnet"

@app.post("/chat")
async def chat(request: ChatRequest):
    response = toolkit.chat(request.message, model=request.model)
    return response
```

## Troubleshooting

### Common Issues

1. **Missing Environment Variables**: Ensure your `.env` file is properly configured
2. **Model Not Found**: Check the model name spelling and availability
3. **Import Errors**: Make sure the package is installed correctly
4. **Authentication Errors**: Verify your API keys and credentials

### Getting Help

- Check the [README.md](README.md) for project overview
- Review [SYSTEM_DOCUMENTATION.md](SYSTEM_DOCUMENTATION.md) for technical details
- Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for quick commands
