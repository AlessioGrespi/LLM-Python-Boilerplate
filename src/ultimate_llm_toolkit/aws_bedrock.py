import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# We'll access environment variables when needed, not at module level

def get_bedrock_client():
    """
    Get or create the bedrock client. This function creates the client
    only when it's actually needed, avoiding import-time errors.
    
    Returns:
        boto3.client: The bedrock client
        
    Raises:
        ValueError: If required AWS credentials are not configured
    """
    # Access environment variables when the function is called
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION")
    
    if not aws_region:
        raise ValueError("AWS_REGION environment variable is not set")
    
    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are not set")
    
    return boto3.client(
        "bedrock-runtime",
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

# Keep the old variable for backward compatibility, but make it a property
# that only creates the client when accessed
class LazyBedrockClient:
    def __init__(self):
        self._client = None
    
    def __getattr__(self, name):
        if self._client is None:
            self._client = get_bedrock_client()
        return getattr(self._client, name)

# Create a lazy client instance
bedrock_client = LazyBedrockClient()
