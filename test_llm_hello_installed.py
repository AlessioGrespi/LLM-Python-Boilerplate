#!/usr/bin/env python3
"""
Test script for the installed LLM-Python-Boilerplate library.
This script will ask LLMs to say "hello world" using both AWS Bedrock and Azure OpenAI.

Use this script in any repository where you have installed the library via pip:
pip install ultimate-llm-toolkit

Or install from source:
pip install -e /path/to/LLM-Python-Boilerplate
"""

import os
from ultimate_llm_toolkit import LLMToolkit
from ultimate_llm_toolkit.model_router import model_router

def test_llm_hello():
    """Test the LLM library by asking it to say hello world."""
    
    print("🤖 Testing LLM-Python-Boilerplate Library (Installed Version)")
    print("=" * 60)
    
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
        
        print("✅ AWS Bedrock test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ AWS Bedrock test failed: {str(e)}")
        print("\n💡 Make sure you have:")
        print("   - Set up your .env file with appropriate API keys")
        print("   - Configured the LLM provider you want to use")
        print("   - Internet connection for API calls")
        print("\n🔧 Environment variables needed:")
        print("   For AWS Bedrock: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION")
        print("   For Azure OpenAI: AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT")
        return False

def test_azure_openai():
    """Test Azure OpenAI by asking it to say hello world."""
    
    print("\n🔵 Testing Azure OpenAI")
    print("=" * 50)
    
    try:
        # Check if Azure credentials are available
        azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        if not azure_api_key:
            print("⚠️  AZURE_OPENAI_API_KEY not found in environment variables")
            print("   Skipping Azure OpenAI test")
            return False
        
        print("📡 Testing Azure OpenAI with gpt-4.1-mini...")
        
        # Create a simple prompt
        prompt = "Please say 'hello world' in a creative way."
        
        print(f"📝 Sending prompt: '{prompt}'")
        print("-" * 50)
        
        # Test using the toolkit
        toolkit = LLMToolkit(default_model="gpt-4.1-mini")
        response = toolkit.chat(
            message=prompt,
            model="gpt-4.1-mini",
            temperature=0.7,
            max_tokens=100
        )
        
        print("🤖 Azure OpenAI Response (via LLMToolkit):")
        print(f"'{response.get('content', 'No content')}'")
        print(f"Provider: {response.get('provider', 'Unknown')}")
        print(f"Model: {response.get('model', 'Unknown')}")
        print("-" * 50)
        
        # Test using direct model_router
        print("🔄 Testing direct model_router with Azure...")
        direct_response = model_router(
            prompt=prompt,
            model="gpt-4.1-mini",
            temperature=0.7,
            max_tokens=100
        )
        
        print("🤖 Azure OpenAI Response (via model_router):")
        print(f"'{direct_response.get('content', 'No content')}'")
        print(f"Provider: {direct_response.get('provider', 'Unknown')}")
        print(f"Model: {direct_response.get('model', 'Unknown')}")
        print("-" * 50)
        
        print("✅ Azure OpenAI test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Azure OpenAI test failed: {str(e)}")
        print("\n💡 Make sure you have:")
        print("   - Set AZURE_OPENAI_API_KEY in your .env file")
        print("   - Set AZURE_OPENAI_ENDPOINT (required)")
        print("   - Set DEPLOYMENT_NAME if using a custom deployment")
        return False

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
        print("\n💡 Make sure you have installed the library:")
        print("   pip install ultimate-llm-toolkit")
        print("   or")
        print("   pip install -e /path/to/LLM-Python-Boilerplate")
        return False

def show_environment_info():
    """Show information about the current environment and library."""
    print("\n🔍 Environment Information:")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"✅ .env file found: {os.path.abspath(env_file)}")
        
        # Check AWS credentials
        aws_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION")
        
        print(f"   AWS_ACCESS_KEY_ID: {'✅ Set' if aws_key else '❌ Not set'}")
        print(f"   AWS_SECRET_ACCESS_KEY: {'✅ Set' if aws_secret else '❌ Not set'}")
        print(f"   AWS_REGION: {'✅ Set' if aws_region else '❌ Not set'}")
        
        # Check Azure credentials
        azure_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        
        print(f"   AZURE_OPENAI_API_KEY: {'✅ Set' if azure_key else '❌ Not set'}")
        print(f"   AZURE_OPENAI_ENDPOINT: {'✅ Set' if azure_endpoint else '❌ Not set'}")
        
    else:
        print(f"⚠️  .env file not found in current directory")
        print(f"   Current directory: {os.getcwd()}")
        print(f"   Create a .env file with your API credentials")
    
    # Show library version info
    try:
        import ultimate_llm_toolkit
        print(f"📦 Library location: {ultimate_llm_toolkit.__file__}")
    except Exception as e:
        print(f"❌ Could not determine library location: {e}")

if __name__ == "__main__":
    print("🚀 Starting LLM-Python-Boilerplate Library Tests (Installed Version)\n")
    
    # Show environment information
    show_environment_info()
    
    # First test imports
    if test_simple_import():
        print("\n" + "="*60)
        # Then test actual LLM functionality
        aws_success = test_llm_hello()
        
        # Test Azure OpenAI if credentials are available
        azure_success = test_azure_openai()
        
        # Show available models summary
        print("\n" + "="*60)
        print("📋 Available Models Summary:")
        print("=" * 60)
        try:
            toolkit = LLMToolkit()
            available_models = toolkit.list_models()
            for provider, models in available_models.items():
                print(f"  {provider.upper()}: {', '.join(models[:5])}{'...' if len(models) > 5 else ''}")
        except Exception as e:
            print(f"  ❌ Could not retrieve model list: {str(e)}")
        
        # Final summary
        print("\n" + "="*60)
        print("🎯 Test Results Summary:")
        print("=" * 60)
        print(f"  AWS Bedrock: {'✅ PASSED' if aws_success else '❌ FAILED'}")
        print(f"  Azure OpenAI: {'✅ PASSED' if azure_success else '❌ FAILED'}")
        
        if aws_success and azure_success:
            print("\n🎉 All tests passed! Your LLM-Python-Boilerplate library is working perfectly!")
        elif aws_success or azure_success:
            print("\n⚠️  Partial success. Some tests passed, some failed.")
        else:
            print("\n❌ All tests failed. Please check your configuration.")
        
    else:
        print("\n❌ Import test failed. Cannot proceed with LLM tests.")
        print("\n📋 Installation Instructions:")
        print("   1. Install the library: pip install ultimate-llm-toolkit")
        print("   2. Or install from source: pip install -e /path/to/LLM-Python-Boilerplate")
        print("   3. Set up your .env file with API credentials")
        print("   4. Run this script again")
