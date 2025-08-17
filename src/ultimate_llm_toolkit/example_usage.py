#!/usr/bin/env python3
"""
Example usage of the model router function.
This script demonstrates how to use the model_router to call different models
from AWS Bedrock and Azure OpenAI seamlessly.
"""

from model_router import model_router, list_available_models, add_model_mapping

def example_basic_usage():
    """Example of basic usage with different models."""
    print("=== Basic Usage Examples ===\n")
    
    # Example 1: Using AWS Bedrock Claude model (converse API)
    try:
        response = model_router(
            prompt="What is the capital of France?",
            model="anthropic-sonnet",
            temperature=0.7,
            max_tokens=100
        )
        print(f"AWS Claude Response: {response['content']}")
        print(f"Provider: {response['provider']}")
        print(f"Model: {response['model']}\n")
    except Exception as e:
        print(f"AWS Claude Error: {e}\n")
    
    # Example 2: Using Azure OpenAI GPT model
    try:
        response = model_router(
            prompt="Explain quantum computing in simple terms.",
            model="gpt-4.1-mini",
            temperature=0.5,
            max_tokens=150
        )
        print(f"Azure GPT Response: {response['content']}")
        print(f"Provider: {response['provider']}")
        print(f"Model: {response['model']}\n")
    except Exception as e:
        print(f"Azure GPT Error: {e}\n")

def example_with_messages():
    """Example using message history for conversation context."""
    print("=== Conversation Context Example ===\n")
    
    # Create a conversation history
    messages = [
        {"role": "system", "content": "You are a helpful assistant that specializes in coding."},
        {"role": "user", "content": "What is Python?"},
        {"role": "assistant", "content": "Python is a high-level, interpreted programming language known for its simplicity and readability."},
        {"role": "user", "content": "What are its main features?"}
    ]
    
    try:
        response = model_router(
            prompt="",  # Empty prompt since we're using messages
            model="gpt-4.1-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=200
        )
        print(f"Conversation Response: {response['content']}")
        print(f"Token Usage: {response['usage']}\n")
    except Exception as e:
        print(f"Conversation Error: {e}\n")

def example_with_tools():
    """Example using tools for function calling."""
    print("=== Tools/Function Calling Example ===\n")
    
    # Define a simple tool
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA"
                        }
                    },
                    "required": ["location"]
                }
            }
        }
    ]
    
    try:
        response = model_router(
            prompt="What's the weather like in New York?",
            model="gpt-4.1-mini",
            tools=tools,
            temperature=0.7,
            max_tokens=100
        )
        print(f"Tool Response: {response['content']}")
        if response.get('tool_calls'):
            print(f"Tool Calls: {response['tool_calls']}")
        print(f"Provider: {response['provider']}\n")
    except Exception as e:
        print(f"Tools Error: {e}\n")

def example_custom_parameters():
    """Example with custom model parameters."""
    print("=== Custom Parameters Example ===\n")
    
    try:
        response = model_router(
            prompt="Write a creative story about a robot learning to paint.",
            model="anthropic-haiku",
            temperature=0.9,  # High creativity
            max_tokens=300,
            top_p=0.95,
            top_k=50,
            stop_sequences=["THE END", "END OF STORY"]
        )
        print(f"Creative Story: {response['content']}")
        print(f"Model: {response['model']}")
        print(f"Provider: {response['provider']}\n")
    except Exception as e:
        print(f"Custom Parameters Error: {e}\n")

def example_with_system_prompt():
    """Example using system prompt with AWS Bedrock."""
    print("=== System Prompt Example ===\n")
    
    try:
        response = model_router(
            prompt="What is the weather like today?",
            model="llama-3-3-70b",
            system_prompt="You are a helpful weather assistant. Always provide accurate and detailed weather information.",
            temperature=0.7,
            max_tokens=150
        )
        print(f"System Prompt Response: {response['content']}")
        print(f"Model: {response['model']}")
        print(f"Provider: {response['provider']}\n")
    except Exception as e:
        print(f"System Prompt Error: {e}\n")

def example_model_management():
    """Example of managing model mappings."""
    print("=== Model Management Example ===\n")
    
    # List available models
    available_models = list_available_models()
    print("Available AWS Models:")
    for model in available_models['aws'][:3]:  # Show first 3
        print(f"  - {model}")
    
    print("\nAvailable Azure Models:")
    for model in available_models['azure'][:3]:  # Show first 3
        print(f"  - {model}")
    
    # Add a custom model mapping
    print("\nAdding custom model mapping...")
    add_model_mapping("my-custom-gpt-model", "azure")
    print("Custom model mapping added successfully!\n")

def main():
    """Run all examples."""
    print("Model Router Examples\n" + "="*50 + "\n")
    
    # Run examples
    example_basic_usage()
    example_with_messages()
    example_with_tools()
    example_custom_parameters()
    example_with_system_prompt()
    example_model_management()
    
    print("All examples completed!")

if __name__ == "__main__":
    main() 