# Environment Variables Setup

This project uses environment variables to securely store API keys and configuration settings.

## Setup Instructions

1. **Create a `.env` file** in the root directory of the project with the following content:

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
ENDPOINT_URL=https://azure-is-ass.openai.azure.com/
DEPLOYMENT_NAME=gpt-4.1-mini

# Add other environment variables as needed
# OPENAI_API_KEY=your_openai_api_key_here
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
# AWS_ACCESS_KEY_ID=your_aws_access_key_here
# AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
```

2. **Replace the placeholder values** with your actual API keys and configuration.

3. **Never commit the `.env` file** to version control (it's already in `.gitignore`).

## Security Notes

- ✅ The `.env` file is already included in `.gitignore` to prevent accidental commits
- ✅ API keys are no longer hardcoded in the source code
- ✅ The application will validate that required environment variables are present
- ✅ Use different API keys for development and production environments

## Required Environment Variables

### Azure OpenAI
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key (required)
- `ENDPOINT_URL`: Azure OpenAI endpoint URL (optional, has default)
- `DEPLOYMENT_NAME`: Model deployment name (optional, has default)

## Testing the Setup

After creating your `.env` file, you can test that the environment variables are loaded correctly by running:

```bash
python -c "from src.core.azure import client; print('Azure client initialized successfully')"
```

If you see any errors about missing API keys, make sure your `.env` file is properly configured. 