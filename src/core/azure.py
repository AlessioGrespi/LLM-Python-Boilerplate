
import os
import base64
from openai import AzureOpenAI

endpoint = os.getenv("ENDPOINT_URL", "https://azure-is-ass.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4.1-mini")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "DYKx0m1bmRjBCIl7dgazsxAsO3GEJo9z9hoL2S70zMv5QNbRDogXJQQJ99BGACYeBjFXJ3w3AAABACOGUzAU")

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)

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
    