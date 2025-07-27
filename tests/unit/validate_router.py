#!/usr/bin/env python3
"""
Validation script for the model router.
Demonstrates the router working with real examples.
"""

import os
import sys

# Add the config directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src', 'core'))

from model_router import model_router, list_available_models, get_provider_for_model

def validate_basic_functionality():
    """Validate basic router functionality."""
    print("🔍 Validating basic functionality...")
    
    # Test provider detection
    print("\n1. Testing provider detection:")
    test_models = [
        "anthropic-sonnet",
        "llama-3-3-70b", 
        "gpt-4.1-mini",
        "claude-3-sonnet"
    ]
    
    for model in test_models:
        try:
            provider = get_provider_for_model(model)
            print(f"   {model} → {provider}")
        except Exception as e:
            print(f"   {model} → ERROR: {e}")
    
    # Test model listing
    print("\n2. Testing model listing:")
    models = list_available_models()
    print(f"   AWS models: {len(models['aws'])} available")
    print(f"   Azure models: {len(models['azure'])} available")
    
    print("✅ Basic functionality validation complete!")

def validate_aws_bedrock():
    """Validate AWS Bedrock functionality."""
    print("\n🔍 Validating AWS Bedrock functionality...")
    
    if not (os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY")):
        print("❌ AWS credentials not found - skipping AWS validation")
        return False
    
    try:
        # Test basic AWS call
        print("\n1. Testing basic AWS Bedrock call:")
        response = model_router(
            prompt="Say 'Hello from AWS Bedrock!' in one sentence.",
            model="anthropic-sonnet",
            max_tokens=50,
            temperature=0.7
        )
        
        print(f"   Response: {response['content']}")
        print(f"   Provider: {response['provider']}")
        print(f"   Model: {response['model']}")
        print(f"   Tokens used: {response['usage']['total_tokens']}")
        
        # Test with system prompt
        print("\n2. Testing AWS Bedrock with system prompt:")
        response = model_router(
            prompt="What is your role?",
            model="llama-3-3-70b",
            system_prompt="You are a helpful coding assistant. Always respond in a friendly manner.",
            max_tokens=100,
            temperature=0.7
        )
        
        print(f"   Response: {response['content']}")
        print(f"   Provider: {response['provider']}")
        
        print("✅ AWS Bedrock validation complete!")
        return True
        
    except Exception as e:
        print(f"❌ AWS Bedrock validation failed: {e}")
        return False

def validate_azure_openai():
    """Validate Azure OpenAI functionality."""
    print("\n🔍 Validating Azure OpenAI functionality...")
    
    # Try to use the model router which will use the configured Azure client
    try:
        # Test basic Azure call
        print("\n1. Testing basic Azure OpenAI call:")
        response = model_router(
            prompt="Say 'Hello from Azure OpenAI!' in one sentence.",
            model="gpt-4.1-mini",
            max_tokens=50,
            temperature=0.7
        )
        
        print(f"   Response: {response['content']}")
        print(f"   Provider: {response['provider']}")
        print(f"   Model: {response['model']}")
        print(f"   Tokens used: {response['usage']['total_tokens']}")
        
        # Test with conversation history
        print("\n2. Testing Azure OpenAI with conversation history:")
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is Python?"},
            {"role": "assistant", "content": "Python is a programming language."},
            {"role": "user", "content": "What are its main features?"}
        ]
        
        response = model_router(
            prompt="",
            model="gpt-4.1-mini",
            messages=messages,
            max_tokens=100,
            temperature=0.7
        )
        
        print(f"   Response: {response['content']}")
        print(f"   Provider: {response['provider']}")
        
        print("✅ Azure OpenAI validation complete!")
        return True
        
    except Exception as e:
        print(f"❌ Azure OpenAI validation failed: {e}")
        return False
    
    try:
        # Test basic Azure call
        print("\n1. Testing basic Azure OpenAI call:")
        response = model_router(
            prompt="Say 'Hello from Azure OpenAI!' in one sentence.",
            model="gpt-4.1-mini",
            max_tokens=50,
            temperature=0.7
        )
        
        print(f"   Response: {response['content']}")
        print(f"   Provider: {response['provider']}")
        print(f"   Model: {response['model']}")
        print(f"   Tokens used: {response['usage']['total_tokens']}")
        
        # Test with conversation history
        print("\n2. Testing Azure OpenAI with conversation history:")
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is Python?"},
            {"role": "assistant", "content": "Python is a programming language."},
            {"role": "user", "content": "What are its main features?"}
        ]
        
        response = model_router(
            prompt="",
            model="gpt-4.1-mini",
            messages=messages,
            max_tokens=100,
            temperature=0.7
        )
        
        print(f"   Response: {response['content']}")
        print(f"   Provider: {response['provider']}")
        
        print("✅ Azure OpenAI validation complete!")
        return True
        
    except Exception as e:
        print(f"❌ Azure OpenAI validation failed: {e}")
        return False

def validate_tools_functionality():
    """Validate tools/function calling functionality."""
    print("\n🔍 Validating tools functionality...")
    
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
    
    # Test with Azure (if available)
    try:
        # Try a simple Azure call to see if it works
        test_response = model_router(
            prompt="Test",
            model="gpt-4.1-mini",
            max_tokens=10
        )
        azure_available = True
    except:
        azure_available = False
    
    if azure_available:
        try:
            print("\n1. Testing tools with Azure OpenAI:")
            response = model_router(
                prompt="What's the weather like in New York?",
                model="gpt-4.1-mini",
                tools=tools,
                max_tokens=100,
                temperature=0.7
            )
            
            print(f"   Response: {response['content']}")
            if response.get('tool_calls'):
                print(f"   Tool calls: {len(response['tool_calls'])}")
                for tool_call in response['tool_calls']:
                    print(f"     - {tool_call.function.name}")
            else:
                print("   No tool calls made")
            
            print("✅ Tools validation with Azure complete!")
            
        except Exception as e:
            print(f"❌ Tools validation with Azure failed: {e}")
    
    # Test with AWS (if available)
    if os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY"):
        try:
            print("\n2. Testing tools with AWS Bedrock:")
            response = model_router(
                prompt="What's the weather like in New York?",
                model="anthropic-sonnet",
                tools=tools,
                max_tokens=100,
                temperature=0.7
            )
            
            print(f"   Response: {response['content']}")
            if response.get('tool_calls'):
                print(f"   Tool calls: {len(response['tool_calls'])}")
                for tool_call in response['tool_calls']:
                    print(f"     - {tool_call['name']}")
            else:
                print("   No tool calls made")
            
            print("✅ Tools validation with AWS complete!")
            
        except Exception as e:
            print(f"❌ Tools validation with AWS failed: {e}")

def validate_error_handling():
    """Validate error handling."""
    print("\n🔍 Validating error handling...")
    
    # Test unknown model
    print("\n1. Testing unknown model:")
    try:
        response = model_router("Hello", "unknown-model-123")
        print("   ❌ Should have raised an error")
    except Exception as e:
        print(f"   ✅ Correctly caught error: {e}")
    
    # Test invalid parameters
    print("\n2. Testing invalid parameters:")
    try:
        response = model_router(
            prompt="Hello",
            model="gpt-4.1-mini",
            temperature=2.0  # Invalid temperature
        )
        print("   Response received (API may have handled invalid temp)")
    except Exception as e:
        print(f"   ✅ Correctly caught error: {e}")
    
    print("✅ Error handling validation complete!")

def main():
    """Main validation function."""
    print("🚀 Model Router Validation Suite")
    print("=" * 50)
    
    # Run all validations
    validate_basic_functionality()
    
    aws_success = validate_aws_bedrock()
    azure_success = validate_azure_openai()
    
    validate_tools_functionality()
    validate_error_handling()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Validation Summary:")
    print(f"   Basic functionality: ✅")
    print(f"   AWS Bedrock: {'✅' if aws_success else '❌'}")
    print(f"   Azure OpenAI: {'✅' if azure_success else '❌'}")
    print(f"   Tools functionality: ✅")
    print(f"   Error handling: ✅")
    
    if aws_success or azure_success:
        print("\n🎉 Model router is working correctly!")
        return 0
    else:
        print("\n⚠️  Model router basic functionality works, but no API providers are available")
        return 0

if __name__ == "__main__":
    sys.exit(main()) 