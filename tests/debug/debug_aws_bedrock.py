#!/usr/bin/env python3
"""
Debug AWS Bedrock Response
Test to see the actual AWS Bedrock response structure.
"""

import sys
import os
import json

# Add the necessary paths
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src', 'core'))

from aws_bedrock import bedrock_client


def test_aws_bedrock_response():
    """Test AWS Bedrock directly and see the response structure."""
    print("🔍 DEBUGGING AWS BEDROCK RESPONSE")
    print("=" * 60)
    
    # Simple test without tools
    request_params = {
        "modelId": "mistral.mistral-small-2402-v1:0",
        "messages": [
            {
                "role": "user",
                "content": [{"text": "Hello! How are you today?"}]
            }
        ],
        "inferenceConfig": {
            "temperature": 0.7,
            "maxTokens": 100
        }
    }
    
    print("📝 Request:")
    print(json.dumps(request_params, indent=2))
    print()
    
    try:
        print("🔄 Calling AWS Bedrock...")
        response = bedrock_client.converse(**request_params)
        
        print("✅ AWS Bedrock call successful")
        print()
        print("📊 RAW AWS BEDROCK RESPONSE:")
        print("=" * 40)
        print(json.dumps(response, indent=2, default=str))
        print("=" * 40)
        
        # Analyze the response structure
        print("\n🔍 RESPONSE STRUCTURE ANALYSIS:")
        print(f"Response type: {type(response)}")
        print(f"Response keys: {list(response.keys()) if hasattr(response, 'keys') else 'No keys'}")
        
        if hasattr(response, 'get'):
            print(f"Has 'content': {response.get('content') is not None}")
            print(f"Has 'usage': {response.get('usage') is not None}")
            print(f"Has 'responseMetadata': {response.get('responseMetadata') is not None}")
            
            if response.get('content'):
                print(f"Content type: {type(response['content'])}")
                print(f"Content length: {len(response['content'])}")
                for i, item in enumerate(response['content']):
                    print(f"  Content item {i}: {item}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def test_aws_bedrock_with_tools():
    """Test AWS Bedrock with tools and see the response structure."""
    print("\n🔍 DEBUGGING AWS BEDROCK WITH TOOLS")
    print("=" * 60)
    
    # Test with tools
    tools = [
        {
            "toolSpec": {
                "name": "get_bbc_public_figures",
                "description": "Get public figures from BBC RSS feed",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
        }
    ]
    
    request_params = {
        "modelId": "mistral.mistral-small-2402-v1:0",
        "messages": [
            {
                "role": "user",
                "content": [{"text": "Can you get me the public figures from today's BBC news?"}]
            }
        ],
        "inferenceConfig": {
            "temperature": 0.7,
            "maxTokens": 300
        },
        "toolConfig": {
            "tools": tools
        }
    }
    
    print("📝 Request with tools:")
    print(json.dumps(request_params, indent=2))
    print()
    
    try:
        print("🔄 Calling AWS Bedrock with tools...")
        response = bedrock_client.converse(**request_params)
        
        print("✅ AWS Bedrock call with tools successful")
        print()
        print("📊 RAW AWS BEDROCK RESPONSE WITH TOOLS:")
        print("=" * 40)
        print(json.dumps(response, indent=2, default=str))
        print("=" * 40)
        
        # Analyze the response structure
        print("\n🔍 RESPONSE STRUCTURE ANALYSIS:")
        print(f"Response type: {type(response)}")
        print(f"Response keys: {list(response.keys()) if hasattr(response, 'keys') else 'No keys'}")
        
        if hasattr(response, 'get'):
            print(f"Has 'content': {response.get('content') is not None}")
            print(f"Has 'usage': {response.get('usage') is not None}")
            print(f"Has 'responseMetadata': {response.get('responseMetadata') is not None}")
            
            if response.get('content'):
                print(f"Content type: {type(response['content'])}")
                print(f"Content length: {len(response['content'])}")
                for i, item in enumerate(response['content']):
                    print(f"  Content item {i}: {item}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Run debug tests."""
    test_aws_bedrock_response()
    test_aws_bedrock_with_tools()


if __name__ == "__main__":
    main() 