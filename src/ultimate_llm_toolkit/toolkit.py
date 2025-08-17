"""
Main LLM Toolkit class providing a clean interface for LLM interactions
"""

import os
from typing import Dict, List, Optional, Any, Union
from dotenv import load_dotenv

from .model_router import model_router, list_available_models
from .bbc_rss import get_bbc_news_summary, get_bbc_latest_news
from .wikipedia_api import search_wikipedia, get_wikipedia_page

# Load environment variables
load_dotenv()

class LLMToolkit:
    """
    Main LLM Toolkit class providing easy access to LLM models and tools.
    
    This class wraps the underlying functionality into a simple, intuitive interface
    that handles model selection, conversation management, and tool usage.
    """
    
    def __init__(self, default_model: str = "anthropic-sonnet"):
        """
        Initialize the LLM Toolkit.
        
        Args:
            default_model (str): Default model to use for chat interactions
        """
        self.default_model = default_model
        self.conversation_history = []
        self.available_models = list_available_models()
        
        # Check if required environment variables are set
        self._check_environment()
    
    def _check_environment(self):
        """Check if required environment variables are configured."""
        required_vars = {
            'aws': ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_DEFAULT_REGION'],
            'azure': ['AZURE_OPENAI_API_KEY', 'AZURE_OPENAI_ENDPOINT']
        }
        
        missing_vars = []
        for provider, vars_list in required_vars.items():
            for var in vars_list:
                if not os.getenv(var):
                    missing_vars.append(f"{provider}: {var}")
        
        if missing_vars:
            print(f"Warning: Missing environment variables: {', '.join(missing_vars)}")
            print("Some functionality may not work properly.")
    
    def chat(
        self,
        message: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send a chat message to the LLM model.
        
        Args:
            message (str): The user's message
            model (str, optional): Model to use (defaults to self.default_model)
            temperature (float): Model temperature (0.0 to 1.0)
            max_tokens (int): Maximum tokens in response
            system_prompt (str, optional): System prompt to set context
            **kwargs: Additional model parameters
            
        Returns:
            Dict[str, Any]: Model response with content, provider, and metadata
        """
        model = model or self.default_model
        
        # Prepare messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add conversation history
        messages.extend(self.conversation_history)
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        try:
            response = model_router(
                prompt=message,
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": response.get('content', '')})
            
            return response
            
        except Exception as e:
            error_response = {
                'content': f"Error: {str(e)}",
                'provider': 'unknown',
                'model': model,
                'error': str(e)
            }
            return error_response
    
    def get_news(self, category: Optional[str] = None, max_articles: int = 10) -> Dict[str, Any]:
        """
        Get latest news using BBC RSS feed.
        
        Args:
            category (str, optional): News category to filter by
            max_articles (int): Maximum number of articles to return
            
        Returns:
            Dict[str, Any]: News data with articles and metadata
        """
        try:
            if category:
                return get_bbc_news_summary(category=category, max_articles=max_articles)
            else:
                return get_bbc_latest_news()
        except Exception as e:
            return {'error': str(e), 'articles': []}
    
    def search_wiki(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Search Wikipedia for information.
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results to return
            
        Returns:
            Dict[str, Any]: Wikipedia search results
        """
        try:
            return search_wikipedia(query, max_results=max_results)
        except Exception as e:
            return {'error': str(e), 'results': []}
    
    def get_wiki_summary(self, title: str) -> Dict[str, Any]:
        """
        Get a Wikipedia article summary.
        
        Args:
            title (str): Article title
            
        Returns:
            Dict[str, Any]: Article summary and metadata
        """
        try:
            return get_wikipedia_summary(title)
        except Exception as e:
            return {'error': str(e), 'summary': ''}
    
    def list_models(self) -> List[str]:
        """
        Get list of available models.
        
        Returns:
            List[str]: List of available model names
        """
        return self.available_models
    
    def set_default_model(self, model: str):
        """
        Set the default model for chat interactions.
        
        Args:
            model (str): Model name to set as default
        """
        if model in self.available_models:
            self.default_model = model
        else:
            raise ValueError(f"Model '{model}' not found. Available models: {self.available_models}")
    
    def clear_conversation(self):
        """Clear the conversation history."""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get the current conversation history.
        
        Returns:
            List[Dict[str, str]]: List of conversation messages
        """
        return self.conversation_history.copy()
    
    def summarize_conversation(self, model: Optional[str] = None) -> str:
        """
        Get an LLM-generated summary of the current conversation.
        
        Args:
            model (str, optional): Model to use for summarization
            
        Returns:
            str: Conversation summary
        """
        if not self.conversation_history:
            return "No conversation to summarize."
        
        conversation_text = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in self.conversation_history
        ])
        
        summary_prompt = f"Please provide a brief summary of this conversation:\n\n{conversation_text}"
        
        try:
            response = self.chat(summary_prompt, model=model, temperature=0.3, max_tokens=200)
            return response.get('content', 'Failed to generate summary.')
        except Exception as e:
            return f"Error generating summary: {str(e)}"

