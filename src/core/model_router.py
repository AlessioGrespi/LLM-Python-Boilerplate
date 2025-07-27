import json
import os
from typing import Dict, List, Optional, Any, Union
from dotenv import load_dotenv

# Import the existing clients
try:
    from .aws_bedrock import bedrock_client
    from .azure import client as azure_client
except ImportError:
    # Fallback for direct execution
    from aws_bedrock import bedrock_client
    from azure import client as azure_client

# Load environment variables
load_dotenv()

# Model mapping configuration
MODEL_MAPPING = {
    # AWS Bedrock models (converse API)
    "llama-3-2-3b": "aws",
    "llama-3-3-70b": "aws",
    "llama-3-1-70b": "aws",
    "mixtral-8x7b": "aws",
    "amazon-premier": "aws",
    "mistral-large": "aws",
    "mistral-small": "aws",
    "anthropic-sonnet": "aws",
    "anthropic-haiku": "aws",
    "deepseek": "aws",
    
    # Legacy AWS Bedrock models (for backward compatibility)
    "anthropic.claude-3-sonnet-20240229-v1:0": "aws",
    "anthropic.claude-3-haiku-20240307-v1:0": "aws",
    "anthropic.claude-3-opus-20240229-v1:0": "aws",
    "amazon.titan-text-express-v1": "aws",
    "amazon.titan-text-lite-v1": "aws",
    "meta.llama2-13b-chat-v1": "aws",
    "meta.llama2-70b-chat-v1": "aws",
    "meta.llama3-8b-instruct-v1:0": "aws",
    "meta.llama3-70b-instruct-v1:0": "aws",
    "mistral.mistral-7b-instruct-v0:2": "aws",
    "mistral.mixtral-8x7b-instruct-v0:1": "aws",
    "cohere.command-r-v1:0": "aws",
    "cohere.command-r-plus-v1:0": "aws",
    
    # Azure OpenAI models (using deployment names)
    "gpt-4.1-mini": "azure",
}

def get_provider_for_model(model: str) -> str:
    """
    Determine which provider (AWS or Azure) to use based on the model name.
    
    Args:
        model (str): The model name/deployment name
        
    Returns:
        str: Either 'aws' or 'azure'
        
    Raises:
        ValueError: If the model is not recognized
    """
    # Check exact match first
    if model in MODEL_MAPPING:
        return MODEL_MAPPING[model]
    
    # Check partial matches for AWS Bedrock models
    if any(aws_model in model for aws_model in ["anthropic.claude", "amazon.titan", "meta.llama", "mistral", "cohere.command"]):
        return "aws"
    
    # Check partial matches for Azure models
    if any(azure_model in model.lower() for azure_model in ["gpt-", "claude-"]):
        return "azure"
    
    raise ValueError(f"Unrecognized model: {model}. Please check the model name or add it to MODEL_MAPPING.")

def call_aws_bedrock(
    prompt: str,
    model: str,
    messages: Optional[List[Dict[str, Any]]] = None,
    tools: Optional[List[Dict[str, Any]]] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Call AWS Bedrock model using the converse API.
    
    Args:
        prompt (str): The input prompt
        model (str): The model name
        messages (Optional[List[Dict]]): Message history
        tools (Optional[List[Dict]]): Tools configuration
        **kwargs: Additional model parameters
        
    Returns:
        Dict[str, Any]: The model response
    """
    try:
        # Model mapping for AWS Bedrock converse API
        model_mapping = {
            "llama-3-2-3b": "arn:aws:bedrock:us-east-1:862671257329:inference-profile/us.meta.llama3-2-3b-instruct-v1:0",
            "llama-3-3-70b": "arn:aws:bedrock:us-east-1:862671257329:inference-profile/us.meta.llama3-3-70b-instruct-v1:0",
            "llama-3-1-70b": "arn:aws:bedrock:us-east-1:862671257329:inference-profile/us.meta.llama3-1-70b-instruct-v1:0",
            "mixtral-8x7b": "mistral.mixtral-8x7b-instruct-v0:1",
            "amazon-premier": "amazon.titan-text-premier-v1:0",
            "mistral-large": "mistral.mistral-large-2402-v1:0",
            "mistral-small": "mistral.mistral-small-2402-v1:0",
            "anthropic-sonnet": "arn:aws:bedrock:us-east-1:862671257329:inference-profile/us.anthropic.claude-3-5-sonnet-20241022-v2:0",
            "anthropic-haiku": "arn:aws:bedrock:us-east-1:862671257329:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0",
            "deepseek": "arn:aws:bedrock:us-east-1:862671257329:inference-profile/us.deepseek.r1-v1:0",
            # Legacy model names for backward compatibility
            "anthropic.claude-3-sonnet-20240229-v1:0": "arn:aws:bedrock:us-east-1:862671257329:inference-profile/us.anthropic.claude-3-5-sonnet-20241022-v2:0",
            "anthropic.claude-3-haiku-20240307-v1:0": "arn:aws:bedrock:us-east-1:862671257329:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0",
            "anthropic.claude-3-opus-20240229-v1:0": "arn:aws:bedrock:us-east-1:862671257329:inference-profile/us.anthropic.claude-3-5-sonnet-20241022-v2:0",
            "amazon.titan-text-express-v1": "amazon.titan-text-premier-v1:0",
            "amazon.titan-text-lite-v1": "amazon.titan-text-premier-v1:0",
            "meta.llama2-13b-chat-v1": "arn:aws:bedrock:us-east-1:862671257329:inference-profile/us.meta.llama3-2-3b-instruct-v1:0",
            "meta.llama2-70b-chat-v1": "arn:aws:bedrock:us-east-1:862671257329:inference-profile/us.meta.llama3-3-70b-instruct-v1:0",
            "meta.llama3-8b-instruct-v1:0": "arn:aws:bedrock:us-east-1:862671257329:inference-profile/us.meta.llama3-2-3b-instruct-v1:0",
            "meta.llama3-70b-instruct-v1:0": "arn:aws:bedrock:us-east-1:862671257329:inference-profile/us.meta.llama3-3-70b-instruct-v1:0",
            "mistral.mistral-7b-instruct-v0:2": "mistral.mistral-small-2402-v1:0",
            "mistral.mixtral-8x7b-instruct-v0:1": "mistral.mixtral-8x7b-instruct-v0:1",
            "cohere.command-r-v1:0": "cohere.command-r-v1:0",
            "cohere.command-r-plus-v1:0": "cohere.command-r-plus-v1:0",
        }
        
        # Get the model ID
        model_id = model_mapping.get(model, model)
        
        # Set default temperature based on model type
        default_temperature = 0.9 if any(x in model_id.lower() for x in ["llama", "anthropic", "amazon-premier", "mistral-large", "mistral-small", "deepseek"]) else 0.7
        temperature = kwargs.get("temperature", default_temperature)
        
        # Prepare conversation messages
        if messages:
            # Convert messages to AWS Bedrock format
            conversation = []
            for msg in messages:
                role = msg.get("role")
                content = msg.get("content", "")
                
                # Convert content to AWS Bedrock format
                if isinstance(content, str):
                    content = [{"text": content}]
                elif isinstance(content, list):
                    # Already in AWS format, but ensure each item has 'text' or 'toolUse'
                    formatted_content = []
                    for item in content:
                        if isinstance(item, dict):
                            if "text" in item:
                                formatted_content.append({"text": item["text"]})
                            elif "toolUse" in item:
                                formatted_content.append({"toolUse": item["toolUse"]})
                        else:
                            formatted_content.append({"text": str(item)})
                    content = formatted_content
                else:
                    content = [{"text": str(content)}]
                
                conversation.append({
                    "role": role,
                    "content": content
                })
        else:
            # Otherwise, create a simple user message
            conversation = [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ]
        
        # Prepare inference configuration
        inference_config = {
            "temperature": temperature,
            "maxTokens": kwargs.get("max_tokens", 32000)
        }
        
        # Add optional parameters
        if "top_p" in kwargs:
            inference_config["topP"] = kwargs["top_p"]
        if "top_k" in kwargs:
            inference_config["topK"] = kwargs["top_k"]
        if "stop_sequences" in kwargs:
            inference_config["stopSequences"] = kwargs["stop_sequences"]
        
        # Prepare request parameters
        request_params = {
            "modelId": model_id,
            "messages": conversation,
            "inferenceConfig": inference_config
        }
        
        # Add tools if provided
        if tools:
            # Convert tools to AWS Bedrock format
            aws_tools = []
            for tool in tools:
                if tool.get("type") == "function":
                    aws_tools.append({
                        "toolSpec": {
                            "name": tool["function"]["name"],
                            "description": tool["function"]["description"],
                            "inputSchema": {
                                "json": tool["function"]["parameters"]
                            }
                        }
                    })
            request_params["toolConfig"] = {"tools": aws_tools}
        
        # Add system prompt if provided
        system_prompt = kwargs.get("system_prompt", "")
        if system_prompt and system_prompt.strip():
            request_params["system"] = [{"text": system_prompt}]
        
        # Make the API call using converse
        response = bedrock_client.converse(**request_params)
        
        # Extract the response content from the correct path
        response_content = ""
        tool_calls = None
        
        # AWS Bedrock response structure: response["output"]["message"]["content"]
        if response.get("output", {}).get("message", {}).get("content"):
            for content_item in response["output"]["message"]["content"]:
                if content_item.get("text"):
                    response_content += content_item["text"]
                elif content_item.get("toolUse"):
                    if tool_calls is None:
                        tool_calls = []
                    tool_calls.append(content_item["toolUse"])
        
        # Extract usage information
        usage = {}
        if response.get("usage"):
            usage = {
                "prompt_tokens": response["usage"].get("inputTokens", 0),
                "completion_tokens": response["usage"].get("outputTokens", 0),
                "total_tokens": response["usage"].get("inputTokens", 0) + response["usage"].get("outputTokens", 0)
            }
        
        return {
            "content": response_content,
            "tool_calls": tool_calls,
            "usage": usage,
            "model": model,
            "provider": "aws"
        }
        
    except Exception as e:
        raise Exception(f"AWS Bedrock API error: {str(e)}")

def call_azure_openai(
    prompt: str,
    model: str,
    messages: Optional[List[Dict[str, Any]]] = None,
    tools: Optional[List[Dict[str, Any]]] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Call Azure OpenAI model.
    
    Args:
        prompt (str): The input prompt
        model (str): The deployment name
        messages (Optional[List[Dict]]): Message history
        tools (Optional[List[Dict]]): Tools configuration
        **kwargs: Additional model parameters
        
    Returns:
        Dict[str, Any]: The model response
    """
    try:
        # Prepare messages
        if messages:
            # If messages are provided, use them directly
            chat_messages = messages
        else:
            # Otherwise, create a simple user message
            chat_messages = [{"role": "user", "content": prompt}]
        
        # Prepare the completion parameters
        completion_params = {
            "model": model,
            "messages": chat_messages,
            "max_tokens": kwargs.get("max_tokens", 32000),
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": kwargs.get("top_p", 0.9),
            "frequency_penalty": kwargs.get("frequency_penalty", 0),
            "presence_penalty": kwargs.get("presence_penalty", 0),
            "stream": kwargs.get("stream", False)
        }
        
        # Add tools if provided
        if tools:
            completion_params["tools"] = tools
            completion_params["tool_choice"] = kwargs.get("tool_choice", "auto")
        
        # Add stop sequences if provided
        if "stop_sequences" in kwargs:
            completion_params["stop"] = kwargs["stop_sequences"]
        
        # Make the API call
        completion = azure_client.chat.completions.create(**completion_params)
        
        # Extract the response
        response_content = completion.choices[0].message.content
        tool_calls = completion.choices[0].message.tool_calls if hasattr(completion.choices[0].message, 'tool_calls') else None
        
        return {
            "content": response_content,
            "tool_calls": tool_calls,
            "usage": {
                "prompt_tokens": completion.usage.prompt_tokens,
                "completion_tokens": completion.usage.completion_tokens,
                "total_tokens": completion.usage.total_tokens
            },
            "model": model,
            "provider": "azure"
        }
        
    except Exception as e:
        raise Exception(f"Azure OpenAI API error: {str(e)}")

def model_router(
    prompt: str,
    model: str,
    messages: Optional[List[Dict[str, Any]]] = None,
    tools: Optional[List[Dict[str, Any]]] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Router function that seamlessly switches between AWS Bedrock and Azure OpenAI
    based on the model name. Falls back to mistral-small if there's a failure or missing model.
    
    Args:
        prompt (str): The input prompt
        model (str): The model name/deployment name
        messages (Optional[List[Dict]]): Message history for conversation context
        tools (Optional[List[Dict]]): Tools configuration for function calling
        **kwargs: Additional model parameters (temperature, max_tokens, etc.)
        
    Returns:
        Dict[str, Any]: The model response with content, usage, and metadata
        
    Raises:
        Exception: If there's an API error even after fallback
    """
    original_model = model
    fallback_model = "mistral-small"
    
    try:
        # Determine which provider to use
        provider = get_provider_for_model(model)
        
        # Route to the appropriate provider
        if provider == "aws":
            return call_aws_bedrock(prompt, model, messages, tools, **kwargs)
        elif provider == "azure":
            return call_azure_openai(prompt, model, messages, tools, **kwargs)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
            
    except Exception as e:
        # If the original model failed, try with mistral-small as fallback
        if model != fallback_model:
            print(f"⚠️  Model '{original_model}' failed: {str(e)}")
            print(f"🔄 Falling back to '{fallback_model}'...")
            
            try:
                # Try with mistral-small
                provider = get_provider_for_model(fallback_model)
                
                if provider == "aws":
                    result = call_aws_bedrock(prompt, fallback_model, messages, tools, **kwargs)
                    # Add fallback info to the response
                    result["fallback_used"] = True
                    result["original_model"] = original_model
                    result["fallback_reason"] = str(e)
                    return result
                elif provider == "azure":
                    result = call_azure_openai(prompt, fallback_model, messages, tools, **kwargs)
                    # Add fallback info to the response
                    result["fallback_used"] = True
                    result["original_model"] = original_model
                    result["fallback_reason"] = str(e)
                    return result
                else:
                    raise ValueError(f"Fallback model '{fallback_model}' has unsupported provider: {provider}")
                    
            except Exception as fallback_error:
                # If even the fallback fails, raise the original error
                raise Exception(f"Model router error: Original model '{original_model}' failed: {str(e)}. Fallback model '{fallback_model}' also failed: {str(fallback_error)}")
        else:
            # If we're already using the fallback model and it failed, just raise the error
            raise Exception(f"Model router error: {str(e)}")

# Example usage and helper functions
def list_available_models() -> Dict[str, List[str]]:
    """
    List all available models grouped by provider.
    
    Returns:
        Dict[str, List[str]]: Dictionary with 'aws' and 'azure' keys containing model lists
    """
    aws_models = [model for model, provider in MODEL_MAPPING.items() if provider == "aws"]
    azure_models = [model for model, provider in MODEL_MAPPING.items() if provider == "azure"]
    
    return {
        "aws": aws_models,
        "azure": azure_models
    }

def add_model_mapping(model: str, provider: str) -> None:
    """
    Add a new model mapping to the router.
    
    Args:
        model (str): The model name
        provider (str): Either 'aws' or 'azure'
    """
    if provider not in ["aws", "azure"]:
        raise ValueError("Provider must be either 'aws' or 'azure'")
    
    MODEL_MAPPING[model] = provider
