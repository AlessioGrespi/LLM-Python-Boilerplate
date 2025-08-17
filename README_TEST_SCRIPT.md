# LLM-Python-Boilerplate Test Script

This directory contains test scripts for the LLM-Python-Boilerplate library.

## Files

- **`test_llm_hello_fixed.py`** - Test script for local development (uses local source code)
- **`test_llm_hello_installed.py`** - Test script for installed library (can be used in any repository)

## Using the Test Script in Another Repository

### Option 1: Install from PyPI (when available)
```bash
pip install ultimate-llm-toolkit
```

### Option 2: Install from Source
```bash
# Clone the repository
git clone https://github.com/yourusername/LLM-Python-Boilerplate.git

# Install in development mode
pip install -e ./LLM-Python-Boilerplate
```

### Option 3: Install Dependencies Only
```bash
# Install required dependencies
pip install boto3 openai python-dotenv
```

## Setup

1. **Copy the test script** to your repository:
   ```bash
   cp test_llm_hello_installed.py /path/to/your/repo/
   ```

2. **Create a `.env` file** in your repository with your API credentials:
   ```bash
   # AWS Bedrock
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_REGION=us-east-1
   
   # Azure OpenAI
   AZURE_OPENAI_API_KEY=your_azure_api_key
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_VERSION=2025-01-01-preview
   ```

3. **Run the test script**:
   ```bash
   python test_llm_hello_installed.py
   ```

## What the Test Script Does

The test script will:

1. **Check your environment** - Verify `.env` file and API credentials
2. **Test imports** - Ensure the library can be imported
3. **Test AWS Bedrock** - Connect to Mistral Small via AWS
4. **Test Azure OpenAI** - Connect to GPT-4.1 Mini via Azure
5. **Show results** - Display comprehensive test results and available models

## Expected Output

When everything is working correctly, you should see:

```
🚀 Starting LLM-Python-Boilerplate Library Tests (Installed Version)

🔍 Environment Information:
==================================================
✅ .env file found: /path/to/your/repo/.env
   AWS_ACCESS_KEY_ID: ✅ Set
   AWS_SECRET_ACCESS_KEY: ✅ Set
   AWS_REGION: ✅ Set
   AZURE_OPENAI_API_KEY: ✅ Set
   AZURE_OPENAI_ENDPOINT: ✅ Set

🧪 Testing library imports...
✅ LLMToolkit imported successfully
✅ model_router imported successfully
✅ list_available_models imported successfully
✅ Available models: 24 total

============================================================
🤖 Testing LLM-Python-Boilerplate Library (Installed Version)
============================================================
📡 Initializing LLM Toolkit...
📝 Sending prompt: 'Please say 'hello world' in a friendly way.'
--------------------------------------------------
🤖 LLM Response (via LLMToolkit):
'Hello there! It's a pleasure to say "Hello, World" to you...'
Provider: aws
Model: mistral-small
--------------------------------------------------
✅ AWS Bedrock test completed successfully!

🔵 Testing Azure OpenAI
==================================================
📡 Testing Azure OpenAI with gpt-4.1-mini...
📝 Sending prompt: 'Please say 'hello world' in a creative way.'
--------------------------------------------------
🤖 Azure OpenAI Response (via LLMToolkit):
'🌍✨ "Salutations, magnificent sphere of life!" ✨🌍'
Provider: azure
Model: gpt-4.1-mini
--------------------------------------------------
✅ Azure OpenAI test completed successfully!

🎯 Test Results Summary:
============================================================
  AWS Bedrock: ✅ PASSED
  Azure OpenAI: ✅ PASSED

🎉 All tests passed! Your LLM-Python-Boilerplate library is working perfectly!
```

## Troubleshooting

### Import Errors
- Make sure the library is installed: `pip list | grep ultimate-llm-toolkit`
- Check Python path: `python -c "import sys; print(sys.path)"`

### API Errors
- Verify your `.env` file has the correct variable names
- Check that your API keys are valid and have sufficient credits
- Ensure your AWS region and Azure endpoint are correct

### Environment Issues
- Make sure you're in the directory with your `.env` file
- Try setting environment variables manually: `export AWS_ACCESS_KEY_ID=your_key`

## Customization

You can modify the test script to:
- Test different models
- Use different prompts
- Add more comprehensive error handling
- Integrate with your CI/CD pipeline

## Support

If you encounter issues:
1. Check the [main repository](https://github.com/yourusername/LLM-Python-Boilerplate) for updates
2. Verify your API credentials and endpoints
3. Check the library's documentation and examples
