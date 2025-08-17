#!/usr/bin/env python3
"""
Simple test script to verify the LLM-Python-Boilerplate library works.
This script will ask an LLM to say "hello world" using Mistral Small.
"""

import os
import sys

# Add the src directory to the Python path so we can import from local source
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ultimate_llm_toolkit import LLMToolkit
from ultimate_llm_toolkit.model_router import model_router

def test_llm_hello():
    """Test the LLM library by asking it to say hello world."""
    
    print("🤖 Testing LLM-Python-Boilerplate Library")
    print("=" * 50)
    
    try:
        # Method 1: Using the LLMToolkit class (recommended)
        print("📡 Initializing LLM Toolkit...")
        toolkit = LLMToolkit(default_model="mistral-small")
        
        # Create a simple prompt
        prompt = "Please say 'hello world' in a friendly way."
        
        print(f"📝 Sending prompt: '{prompt}'")
        print("-" * 50)
        
        # Get response from the LLM using the toolkit
        response = toolkit.chat(
            message=prompt,
            model="mistral-small",
            temperature=0.7,
            max_tokens=100
        )
        
        print("🤖 LLM Response (via LLMToolkit):")
        print(f"'{response.get('content', 'No content')}'")
        print(f"Provider: {response.get('provider', 'Unknown')}")
        print(f"Model: {response.get('model', 'Unknown')}")
        print("-" * 50)
        
        # Method 2: Using the model_router function directly
        print("🔄 Testing direct model_router function...")
        direct_response = model_router(
            prompt=prompt,
            model="mistral-small",
            temperature=0.7,
            max_tokens=100
        )
        
        print("🤖 LLM Response (via model_router):")
        print(f"'{direct_response.get('content', 'No content')}'")
        print(f"Provider: {direct_response.get('provider', 'Unknown')}")
        print(f"Model: {direct_response.get('model', 'Unknown')}")
        print("-" * 50)
        
        print("✅ Test completed successfully!")
        
        # Show available models
        print("\n📋 Available Models:")
        available_models = toolkit.list_models()
        for provider, models in available_models.items():
            print(f"  {provider.upper()}: {', '.join(models[:5])}{'...' if len(models) > 5 else ''}")
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        print("\n💡 Make sure you have:")
        print("   - Set up your .env file with appropriate API keys")
        print("   - Configured the LLM provider you want to use")
        print("   - Internet connection for API calls")
        print("\n🔧 Environment variables needed:")
        print("   For AWS Bedrock: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION")
        print("   For Azure OpenAI: AZURE_OPENAI_API_KEY, ENDPOINT_URL")

def test_simple_import():
    """Test that the library can be imported without errors."""
    print("🧪 Testing library imports...")
    
    try:
        # Test basic imports
        from ultimate_llm_toolkit import LLMToolkit
        print("✅ LLMToolkit imported successfully")
        
        from ultimate_llm_toolkit.model_router import model_router
        print("✅ model_router imported successfully")
        
        from ultimate_llm_toolkit.model_router import list_available_models
        print("✅ list_available_models imported successfully")
        
        # Test listing models without credentials
        models = list_available_models()
        print(f"✅ Available models: {len(models.get('aws', [])) + len(models.get('azure', []))} total")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting LLM-Python-Boilerplate Library Tests\n")
    
    # First test imports
    if test_simple_import():
        print("\n" + "="*50)
        # Then test actual LLM functionality
        test_llm_hello()
    else:
        print("\n❌ Import test failed. Cannot proceed with LLM tests.")
