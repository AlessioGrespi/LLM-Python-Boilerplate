
import os
import base64
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables from .env file
load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4.1-mini")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

# Initialize Azure OpenAI client with key-based authentication
def get_client():
    """Get Azure OpenAI client, initializing it when needed."""
    if not subscription_key:
        raise ValueError("AZURE_OPENAI_API_KEY environment variable is required. Please set it in your .env file.")
    
    if not endpoint:
        raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is required. Please set it in your .env file.")
    
    return AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=subscription_key,
        api_version="2025-01-01-preview",
    )

# Create client instance (will be created when first accessed)
client = None

# IMAGE_PATH = "YOUR_IMAGE_PATH"
# encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')

# # Prepare the chat prompt
# chat_prompt = [
#     {
#         "role": "system",
#         "content": [
#             {
#                 "type": "text",
#                 "text": "You are an AI assistant that helps people find information."
#             }
#         ]
#     }
# ]

# # Include speech result if speech is enabled
# messages = chat_prompt

# # Generate the completion
# completion = client.chat.completions.create(
#     model=deployment,
#     messages=messages,
#     max_tokens=800,
#     temperature=0.7,
#     top_p=0.95,
#     frequency_penalty=0,
#     presence_penalty=0,
#     stop=None,
#     stream=False
# )

# print(completion.to_json())
    