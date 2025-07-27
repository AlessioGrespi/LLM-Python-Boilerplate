"""
Core functionality for the Ultimate AI Personal Assistant
"""

from .model_router import model_router, call_aws_bedrock, call_azure_openai, get_provider_for_model
from .azure import client as azure_client
from .aws_bedrock import bedrock_client

__all__ = ['model_router', 'call_aws_bedrock', 'call_azure_openai', 'get_provider_for_model', 'azure_client', 'bedrock_client'] 