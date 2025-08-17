# Installation Guide for Ultimate LLM Toolkit

## Quick Installation

To use the Ultimate LLM Toolkit in any repository, you have several options:

### Option 1: Install from Source (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/AlessioGrespi/LLM-Python-Boilerplate.git

# Install in development mode
pip install -e ./LLM-Python-Boilerplate
```

### Option 2: Install from Local Path

If you already have the repository cloned somewhere:

```bash
# Install from your local copy
pip install -e /path/to/LLM-Python-Boilerplate
```

### Option 3: Install Dependencies Only

If you want to copy the source code directly:

```bash
pip install boto3 openai python-dotenv httpx pandas numpy feedparser beautifulsoup4 requests pydantic typing-extensions
```

## Verify Installation

After installation, you should be able to import the library:

```python
# Test import
from ultimate_llm_toolkit import LLMToolkit
from ultimate_llm_toolkit.model_router import model_router

print("✅ Library imported successfully!")
```

## Setup Environment Variables

Create a `.env` file in your repository with your API credentials:

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

## Test the Installation

Copy the test script to your repository and run it:

```bash
# Copy the test script
cp /path/to/LLM-Python-Boilerplate/test_llm_hello_installed.py ./

# Run the test
python test_llm_hello_installed.py
```

## Troubleshooting

### Import Error: "No module named 'ultimate_llm_toolkit'"

**Solution:** The package isn't installed. Install it using one of the options above.

```bash
# Check if it's installed
pip list | grep ultimate-llm-toolkit

# If not found, install it
pip install -e /path/to/LLM-Python-Boilerplate
```

### Environment Variables Not Found

**Solution:** Make sure your `.env` file is in the same directory where you're running the script.

```bash
# Check current directory
pwd

# List files to see if .env exists
ls -la

# Create .env if missing
touch .env
# Then add your API credentials
```

### API Errors

**Solution:** Verify your API credentials are correct and have sufficient credits.

## Package Information

- **Package Name:** `ultimate-llm-toolkit`
- **Import Name:** `ultimate_llm_toolkit`
- **Version:** 1.0.0
- **Python Version:** 3.8+

## Support

If you encounter issues:
1. Check that the package is properly installed: `pip list | grep ultimate-llm-toolkit`
2. Verify your `.env` file has the correct variable names
3. Ensure your API keys are valid and have sufficient credits
4. Check the main repository for updates and documentation
