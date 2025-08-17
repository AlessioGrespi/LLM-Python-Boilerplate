# Model Router

A seamless model router that can switch between AWS Bedrock and Azure OpenAI based on the model name. This allows you to use different AI models from different providers with a single, unified interface.

## Features

- **Seamless Provider Switching**: Automatically routes to AWS Bedrock or Azure OpenAI based on model name
- **Automatic Fallback**: Falls back to `mistral-small` when the requested model fails or is unavailable
- **Unified Interface**: Single function call for all models regardless of provider
- **Message History Support**: Maintain conversation context across multiple calls
- **Tools/Function Calling**: Support for function calling on compatible models
- **Flexible Parameters**: Pass any model-specific parameters through kwargs
- **Error Handling**: Comprehensive error handling with provider-specific error messages
- **Extensible**: Easy to add new models and providers

## Supported Models

### AWS Bedrock Models (Converse API)
- **Anthropic Claude**: `anthropic-sonnet`, `anthropic-haiku` (latest versions)
- **Amazon Titan**: `amazon-premier` (latest version)
- **Meta Llama**: `llama-3-2-3b`, `llama-3-3-70b`, `llama-3-1-70b`
- **Mistral**: `mistral-large`, `mistral-small`, `mixtral-8x7b`
- **DeepSeek**: `deepseek` (latest version)
- **Cohere**: `cohere.command-r-v1:0`, `cohere.command-r-plus-v1:0`

*Note: Legacy model names are still supported for backward compatibility.*

### Azure OpenAI Models
- **GPT Models**: `gpt-4`, `gpt-4-turbo`, `gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo`, `gpt-35-turbo`, `gpt-4.1-mini`
- **Claude Models**: `claude-3-sonnet`, `claude-3-haiku`, `claude-3-opus`

## Installation

1. Ensure you have the required dependencies:
```bash
pip install boto3 openai python-dotenv
```

2. Set up your environment variables in a `.env` file:
```env
# AWS Bedrock Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1

# Azure OpenAI Configuration
ENDPOINT_URL=https://your-resource.openai.azure.com/
DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_KEY=your_azure_api_key
```

## Basic Usage

```python
from config.model_router import model_router

# Simple prompt with AWS Bedrock
response = model_router(
    prompt="What is the capital of France?",
    model="anthropic-sonnet",
    temperature=0.7,
    max_tokens=100
)
print(response['content'])

# Simple prompt with Azure OpenAI
response = model_router(
    prompt="Explain quantum computing in simple terms.",
    model="gpt-4.1-mini",
    temperature=0.5,
    max_tokens=150
)
print(response['content'])
```

### Automatic Fallback

The model router automatically falls back to `mistral-small` when:
- The requested model doesn't exist
- The requested model fails to respond
- There are API errors with the requested model
- Any other failure occurs

When a fallback occurs, the response includes additional metadata:
```python
response = model_router(
    prompt="Hello world",
    model="non-existent-model"
)

print(response['content'])  # Response from mistral-small
print(response['fallback_used'])  # True
print(response['original_model'])  # "non-existent-model"
print(response['fallback_reason'])  # Error message explaining why fallback was needed
```

## Advanced Usage

### With Message History

```python
messages = [
    {"role": "system", "content": "You are a helpful coding assistant."},
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language."},
    {"role": "user", "content": "What are its main features?"}
]

response = model_router(
    prompt="",  # Empty prompt when using messages
    model="gpt-4.1-mini",
    messages=messages,
    temperature=0.7,
    max_tokens=200
)
```

### With Tools/Function Calling

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and state"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

response = model_router(
    prompt="What's the weather like in New York?",
    model="gpt-4.1-mini",
    tools=tools,
    temperature=0.7,
    max_tokens=100
)
```

### Custom Parameters

```python
response = model_router(
    prompt="Write a creative story about a robot.",
    model="anthropic-haiku",
    temperature=0.9,
    max_tokens=300,
    top_p=0.95,
    top_k=50,
    stop_sequences=["THE END", "END OF STORY"]
)
```

### With System Prompt (AWS Bedrock)

```python
response = model_router(
    prompt="What is the weather like today?",
    model="llama-3-3-70b",
    system_prompt="You are a helpful weather assistant. Always provide accurate and detailed weather information.",
    temperature=0.7,
    max_tokens=150
)
```

## Response Format

All responses follow a consistent format:

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

## Helper Functions

### List Available Models

```python
from config.model_router import list_available_models

models = list_available_models()
print("AWS Models:", models['aws'])
print("Azure Models:", models['azure'])
```

### Add Custom Model Mapping

```python
from config.model_router import add_model_mapping

add_model_mapping("my-custom-model", "azure")
```

## Error Handling

The router provides detailed error messages for different scenarios:

```python
try:
    response = model_router(
        prompt="Hello",
        model="unknown-model",
        temperature=0.7
    )
except ValueError as e:
    print(f"Model not recognized: {e}")
except Exception as e:
    print(f"API error: {e}")
```

## Configuration

### Environment Variables

Make sure to set up the following environment variables:

**For AWS Bedrock:**
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `AWS_REGION`: AWS region (e.g., us-east-1)

**For Azure OpenAI:**
- `ENDPOINT_URL`: Your Azure OpenAI endpoint
- `DEPLOYMENT_NAME`: Your deployment name
- `AZURE_OPENAI_API_KEY`: Your Azure API key

### Model Mapping

The router uses a predefined mapping to determine which provider to use for each model. You can extend this mapping by:

1. Adding entries to the `MODEL_MAPPING` dictionary in the code
2. Using the `add_model_mapping()` function at runtime
3. The router also supports partial matching for model families

## Examples

See `example_usage.py` for comprehensive examples of all features.

## Testing

Tests are located in the `tests/` directory at the root level:

```bash
# Run all tests
python tests/run_tests.py

# Run only unit tests
python tests/run_tests.py --unit

# Run integration tests
python tests/run_tests.py --integration

# Check environment setup
python tests/run_tests.py --check-env

# Run validation script
python tests/validate_router.py

# Demo fallback functionality
python tests/test_fallback_demo.py
```

The test suite includes comprehensive coverage of:
- Unit tests for all functions
- Integration tests with real API calls
- Fallback functionality testing
- Error handling scenarios

## Troubleshooting

### Common Issues

1. **Model not recognized**: Add the model to `MODEL_MAPPING` or use `add_model_mapping()`
2. **Authentication errors**: Check your environment variables and API keys
3. **Rate limiting**: Implement retry logic or use different models
4. **Tool calling not working**: Ensure the model supports function calling (most Azure GPT models do)

### Debug Mode

To debug issues, you can check which provider is being used:

```python
from config.model_router import get_provider_for_model

provider = get_provider_for_model("your-model-name")
print(f"Provider: {provider}")
```

## Contributing

To add support for new models or providers:

1. Add the model to the `MODEL_MAPPING` dictionary
2. Implement the appropriate calling function if needed
3. Update the response parsing logic
4. Add tests and examples

## License

This project is part of the LLM Python Boilerplate project. 