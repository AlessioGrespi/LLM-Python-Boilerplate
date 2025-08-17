"""
Ultimate LLM Toolkit - A comprehensive LLM inference library

This package provides:
- Multi-provider LLM support (AWS Bedrock, Azure OpenAI)
- Tool integration (RSS feeds, Wikipedia, web search)
- Conversation management
- Easy-to-use API for LLM interactions

Quick Start:
    from ultimate_llm_toolkit import LLMToolkit
    
    # Create toolkit instance
    toolkit = LLMToolkit()
    
    # Chat with any supported model
    response = toolkit.chat("Hello!", model="anthropic-sonnet")
    
    # Use tools
    news = toolkit.get_news(category="technology")
"""

__version__ = "1.0.0"
__author__ = "Alessio"

# Core imports
from .model_router import (
    model_router,
    call_aws_bedrock,
    call_azure_openai,
    get_provider_for_model,
    list_available_models,
    add_model_mapping
)

from .azure import get_client
from .aws_bedrock import bedrock_client

# Tool imports
from .bbc_rss import (
    get_bbc_latest_news,
    get_bbc_news_summary,
    get_bbc_public_figures,
    get_bbc_rss_feed
)

from .wikipedia_api import (
    search_wikipedia,
    get_wikipedia_page,
    get_multiple_people_wikipedia_pages
)

# Main toolkit class
from .toolkit import LLMToolkit

__all__ = [
    # Core functionality
    'LLMToolkit',
    'model_router',
    'call_aws_bedrock',
    'call_azure_openai',
    'get_provider_for_model',
    'list_available_models',
    'add_model_mapping',
    
    # Clients
    'get_client',
    'bedrock_client',
    
    # Tools
    'get_bbc_latest_news',
    'get_bbc_news_summary',
    'get_bbc_public_figures',
    'get_bbc_rss_feed',
    'search_wikipedia',
    'get_wikipedia_page',
    'get_multiple_people_wikipedia_pages',
] 