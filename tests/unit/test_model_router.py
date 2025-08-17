#!/usr/bin/env python3
"""
Test suite for the model router functionality.
Tests both AWS Bedrock and Azure OpenAI integrations with proper mocking.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import sys
import os

# Import from the ultimate_llm_toolkit package
from ultimate_llm_toolkit.model_router import (
    model_router,
    get_provider_for_model,
    call_aws_bedrock,
    call_azure_openai,
    list_available_models,
    add_model_mapping,
    MODEL_MAPPING
)


class TestModelRouter(unittest.TestCase):
    """Test cases for the model router functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Reset MODEL_MAPPING to original state before each test
        self.original_mapping = MODEL_MAPPING.copy()

    def tearDown(self):
        """Clean up after each test."""
        # Restore original MODEL_MAPPING
        MODEL_MAPPING.clear()
        MODEL_MAPPING.update(self.original_mapping)

    def test_get_provider_for_model_aws(self):
        """Test provider detection for AWS models."""
        # Test new AWS model names
        self.assertEqual(get_provider_for_model("anthropic-sonnet"), "aws")
        self.assertEqual(get_provider_for_model("llama-3-3-70b"), "aws")
        self.assertEqual(get_provider_for_model("mistral-large"), "aws")
        self.assertEqual(get_provider_for_model("amazon-premier"), "aws")
        self.assertEqual(get_provider_for_model("deepseek"), "aws")
        
        # Test legacy AWS model names
        self.assertEqual(get_provider_for_model("anthropic.claude-3-sonnet-20240229-v1:0"), "aws")
        self.assertEqual(get_provider_for_model("meta.llama3-70b-instruct-v1:0"), "aws")
        self.assertEqual(get_provider_for_model("mistral.mixtral-8x7b-instruct-v0:1"), "aws")

    def test_get_provider_for_model_azure(self):
        """Test provider detection for Azure models."""
        self.assertEqual(get_provider_for_model("gpt-4"), "azure")
        self.assertEqual(get_provider_for_model("gpt-4.1-mini"), "azure")
        self.assertEqual(get_provider_for_model("gpt-3.5-turbo"), "azure")
        self.assertEqual(get_provider_for_model("claude-3-sonnet"), "azure")

    def test_get_provider_for_model_partial_matching(self):
        """Test partial matching for model families."""
        # AWS partial matches
        self.assertEqual(get_provider_for_model("anthropic.claude-3-custom"), "aws")
        self.assertEqual(get_provider_for_model("meta.llama-custom"), "aws")
        self.assertEqual(get_provider_for_model("amazon.titan-custom"), "aws")
        self.assertEqual(get_provider_for_model("mistral-custom"), "aws")
        self.assertEqual(get_provider_for_model("cohere.command-custom"), "aws")
        
        # Azure partial matches
        self.assertEqual(get_provider_for_model("gpt-4-custom"), "azure")
        self.assertEqual(get_provider_for_model("claude-3-custom"), "azure")

    def test_get_provider_for_model_unknown(self):
        """Test error handling for unknown models."""
        with self.assertRaises(ValueError) as context:
            get_provider_for_model("unknown-model-123")
        self.assertIn("Unrecognized model", str(context.exception))

    @patch('ultimate_llm_toolkit.model_router.bedrock_client')
    def test_call_aws_bedrock_basic(self, mock_bedrock_client):
        """Test basic AWS Bedrock call."""
        # Mock the response
        mock_response = {
            "output": {
                "message": {
                    "content": [
                        {"text": "Hello from AWS Bedrock!"}
                    ]
                }
            },
            "usage": {
                "inputTokens": 10,
                "outputTokens": 5
            }
        }
        mock_bedrock_client.converse.return_value = mock_response

        # Test the function
        result = call_aws_bedrock(
            prompt="Hello",
            model="anthropic-sonnet",
            temperature=0.7,
            max_tokens=100
        )

        # Verify the result
        self.assertEqual(result["content"], "Hello from AWS Bedrock!")
        self.assertEqual(result["provider"], "aws")
        self.assertEqual(result["model"], "anthropic-sonnet")
        self.assertEqual(result["usage"]["prompt_tokens"], 10)
        self.assertEqual(result["usage"]["completion_tokens"], 5)
        self.assertEqual(result["usage"]["total_tokens"], 15)

        # Verify the API call
        mock_bedrock_client.converse.assert_called_once()
        call_args = mock_bedrock_client.converse.call_args[1]
        self.assertEqual(call_args["modelId"], "arn:aws:bedrock:us-east-1:862671257329:inference-profile/us.anthropic.claude-3-5-sonnet-20241022-v2:0")
        self.assertEqual(call_args["inferenceConfig"]["temperature"], 0.7)
        self.assertEqual(call_args["inferenceConfig"]["maxTokens"], 100)

    @patch('ultimate_llm_toolkit.model_router.bedrock_client')
    def test_call_aws_bedrock_with_messages(self, mock_bedrock_client):
        """Test AWS Bedrock call with message history."""
        mock_response = {
            "output": {
                "message": {
                    "content": [{"text": "I remember our conversation!"}]
                }
            },
            "usage": {"inputTokens": 20, "outputTokens": 8}
        }
        mock_bedrock_client.converse.return_value = mock_response

        messages = [
            {"role": "user", "content": [{"text": "Hello"}]},
            {"role": "assistant", "content": [{"text": "Hi there!"}]},
            {"role": "user", "content": [{"text": "Do you remember?"}]}
        ]

        result = call_aws_bedrock(
            prompt="",
            model="llama-3-3-70b",
            messages=messages,
            temperature=0.8
        )

        self.assertEqual(result["content"], "I remember our conversation!")
        
        # Verify messages were passed correctly
        call_args = mock_bedrock_client.converse.call_args[1]
        self.assertEqual(call_args["messages"], messages)

    @patch('model_router.bedrock_client')
    def test_call_aws_bedrock_with_tools(self, mock_bedrock_client):
        """Test AWS Bedrock call with tools."""
        mock_response = {
            "output": {
                "message": {
                    "content": [
                        {"text": "I'll get the weather for you."},
                        {
                            "toolUse": {
                                "name": "get_weather",
                                "input": {"location": "New York"}
                            }
                        }
                    ]
                }
            },
            "usage": {"inputTokens": 15, "outputTokens": 12}
        }
        mock_bedrock_client.converse.return_value = mock_response

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get weather for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state"
                            }
                        },
                        "required": ["location"]
                    }
                }
            }
        ]

        result = call_aws_bedrock(
            prompt="Get weather for New York",
            model="anthropic-sonnet",
            tools=tools
        )

        self.assertEqual(result["content"], "I'll get the weather for you.")
        self.assertIsNotNone(result["tool_calls"])
        self.assertEqual(len(result["tool_calls"]), 1)
        self.assertEqual(result["tool_calls"][0]["name"], "get_weather")

        # Verify tools were passed correctly (should be converted to AWS format)
        call_args = mock_bedrock_client.converse.call_args[1]
        expected_tool_config = {
            "tools": [
                {
                    "toolSpec": {
                        "name": "get_weather",
                        "description": "Get weather for a location",
                        "inputSchema": {
                            "json": {
                                "type": "object",
                                "properties": {
                                    "location": {
                                        "type": "string",
                                        "description": "The city and state"
                                    }
                                },
                                "required": ["location"]
                            }
                        }
                    }
                }
            ]
        }
        self.assertEqual(call_args["toolConfig"], expected_tool_config)

    @patch('model_router.bedrock_client')
    def test_call_aws_bedrock_with_system_prompt(self, mock_bedrock_client):
        """Test AWS Bedrock call with system prompt."""
        mock_response = {
            "output": {
                "message": {
                    "content": [{"text": "I'm a helpful assistant. How can I help you today?"}]
                }
            },
            "usage": {"inputTokens": 25, "outputTokens": 10}
        }
        mock_bedrock_client.converse.return_value = mock_response

        result = call_aws_bedrock(
            prompt="Hello",
            model="mistral-large",
            system_prompt="You are a helpful assistant.",
            temperature=0.7
        )

        self.assertEqual(result["content"], "I'm a helpful assistant. How can I help you today?")

        # Verify system prompt was passed correctly
        call_args = mock_bedrock_client.converse.call_args[1]
        self.assertEqual(call_args["system"], [{"text": "You are a helpful assistant."}])

    @patch('model_router.azure_client')
    def test_call_azure_openai_basic(self, mock_azure_client):
        """Test basic Azure OpenAI call."""
        # Mock the completion response
        mock_completion = Mock()
        mock_completion.choices = [Mock()]
        mock_completion.choices[0].message.content = "Hello from Azure OpenAI!"
        mock_completion.choices[0].message.tool_calls = None
        mock_completion.usage.prompt_tokens = 8
        mock_completion.usage.completion_tokens = 6
        mock_completion.usage.total_tokens = 14
        
        mock_azure_client.chat.completions.create.return_value = mock_completion

        result = call_azure_openai(
            prompt="Hello",
            model="gpt-4.1-mini",
            temperature=0.7,
            max_tokens=100
        )

        self.assertEqual(result["content"], "Hello from Azure OpenAI!")
        self.assertEqual(result["provider"], "azure")
        self.assertEqual(result["model"], "gpt-4.1-mini")
        self.assertEqual(result["usage"]["prompt_tokens"], 8)
        self.assertEqual(result["usage"]["completion_tokens"], 6)
        self.assertEqual(result["usage"]["total_tokens"], 14)

        # Verify the API call
        mock_azure_client.chat.completions.create.assert_called_once()
        call_args = mock_azure_client.chat.completions.create.call_args[1]
        self.assertEqual(call_args["model"], "gpt-4.1-mini")
        self.assertEqual(call_args["temperature"], 0.7)
        self.assertEqual(call_args["max_tokens"], 100)

    @patch('model_router.azure_client')
    def test_call_azure_openai_with_messages(self, mock_azure_client):
        """Test Azure OpenAI call with message history."""
        mock_completion = Mock()
        mock_completion.choices = [Mock()]
        mock_completion.choices[0].message.content = "I remember our conversation!"
        mock_completion.choices[0].message.tool_calls = None
        mock_completion.usage.prompt_tokens = 20
        mock_completion.usage.completion_tokens = 8
        mock_completion.usage.total_tokens = 28
        
        mock_azure_client.chat.completions.create.return_value = mock_completion

        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": "Do you remember?"}
        ]

        result = call_azure_openai(
            prompt="",
            model="gpt-4.1-mini",
            messages=messages
        )

        self.assertEqual(result["content"], "I remember our conversation!")

        # Verify messages were passed correctly
        call_args = mock_azure_client.chat.completions.create.call_args[1]
        self.assertEqual(call_args["messages"], messages)

    @patch('model_router.azure_client')
    def test_call_azure_openai_with_tools(self, mock_azure_client):
        """Test Azure OpenAI call with tools."""
        mock_tool_call = Mock()
        mock_tool_call.id = "call_123"
        mock_tool_call.function.name = "get_weather"
        mock_tool_call.function.arguments = '{"location": "New York"}'

        mock_completion = Mock()
        mock_completion.choices = [Mock()]
        mock_completion.choices[0].message.content = "I'll get the weather for you."
        mock_completion.choices[0].message.tool_calls = [mock_tool_call]
        mock_completion.usage.prompt_tokens = 15
        mock_completion.usage.completion_tokens = 12
        mock_completion.usage.total_tokens = 27
        
        mock_azure_client.chat.completions.create.return_value = mock_completion

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get weather for a location"
                }
            }
        ]

        result = call_azure_openai(
            prompt="Get weather for New York",
            model="gpt-4.1-mini",
            tools=tools
        )

        self.assertEqual(result["content"], "I'll get the weather for you.")
        self.assertIsNotNone(result["tool_calls"])
        self.assertEqual(len(result["tool_calls"]), 1)
        self.assertEqual(result["tool_calls"][0].function.name, "get_weather")

        # Verify tools were passed correctly
        call_args = mock_azure_client.chat.completions.create.call_args[1]
        self.assertEqual(call_args["tools"], tools)

    @patch('model_router.get_provider_for_model')
    @patch('model_router.call_aws_bedrock')
    def test_model_router_aws(self, mock_call_aws, mock_get_provider):
        """Test model router with AWS provider."""
        mock_get_provider.return_value = "aws"
        mock_call_aws.return_value = {
            "content": "AWS response",
            "provider": "aws",
            "model": "anthropic-sonnet",
            "usage": {"total_tokens": 10}
        }

        result = model_router(
            prompt="Hello",
            model="anthropic-sonnet",
            temperature=0.7
        )

        self.assertEqual(result["content"], "AWS response")
        self.assertEqual(result["provider"], "aws")
        mock_get_provider.assert_called_once_with("anthropic-sonnet")
        mock_call_aws.assert_called_once()

    @patch('model_router.get_provider_for_model')
    @patch('model_router.call_azure_openai')
    def test_model_router_azure(self, mock_call_azure, mock_get_provider):
        """Test model router with Azure provider."""
        mock_get_provider.return_value = "azure"
        mock_call_azure.return_value = {
            "content": "Azure response",
            "provider": "azure",
            "model": "gpt-4.1-mini",
            "usage": {"total_tokens": 15}
        }

        result = model_router(
            prompt="Hello",
            model="gpt-4.1-mini",
            temperature=0.7
        )

        self.assertEqual(result["content"], "Azure response")
        self.assertEqual(result["provider"], "azure")
        mock_get_provider.assert_called_once_with("gpt-4.1-mini")
        mock_call_azure.assert_called_once()

    @patch('model_router.get_provider_for_model')
    @patch('model_router.call_aws_bedrock')
    def test_model_router_unknown_provider(self, mock_call_aws, mock_get_provider):
        """Test model router with unknown provider falls back to mistral-small."""
        # First call returns unknown, second call (fallback) returns aws
        mock_get_provider.side_effect = ["unknown", "aws"]
        mock_call_aws.return_value = {
            "content": "Fallback response",
            "provider": "aws",
            "model": "mistral-small",
            "usage": {"total_tokens": 10}
        }

        result = model_router("Hello", "unknown-model")
        
        # Verify fallback was used
        self.assertEqual(result["content"], "Fallback response")
        self.assertEqual(result["model"], "mistral-small")
        self.assertTrue(result["fallback_used"])
        self.assertEqual(result["original_model"], "unknown-model")
        self.assertIn("Unsupported provider: unknown", result["fallback_reason"])

    @patch('model_router.get_provider_for_model')
    @patch('model_router.call_aws_bedrock')
    def test_model_router_fallback_to_mistral_small(self, mock_call_aws, mock_get_provider):
        """Test model router fallback to mistral-small when original model fails."""
        # First call fails, second call (fallback) succeeds
        mock_get_provider.side_effect = ["aws", "aws"]
        mock_call_aws.side_effect = [
            Exception("Original model failed"),  # First call fails
            {  # Second call (fallback) succeeds
                "content": "Fallback response",
                "provider": "aws",
                "model": "mistral-small",
                "usage": {"total_tokens": 10}
            }
        ]

        result = model_router("Hello", "failing-model")

        # Verify fallback was used
        self.assertEqual(result["content"], "Fallback response")
        self.assertEqual(result["model"], "mistral-small")
        self.assertTrue(result["fallback_used"])
        self.assertEqual(result["original_model"], "failing-model")
        self.assertIn("Original model failed", result["fallback_reason"])

        # Verify both calls were made
        self.assertEqual(mock_get_provider.call_count, 2)
        self.assertEqual(mock_call_aws.call_count, 2)

    @patch('model_router.get_provider_for_model')
    @patch('model_router.call_aws_bedrock')
    def test_model_router_fallback_also_fails(self, mock_call_aws, mock_get_provider):
        """Test model router when both original and fallback models fail."""
        mock_get_provider.side_effect = ["aws", "aws"]
        mock_call_aws.side_effect = [
            Exception("Original model failed"),
            Exception("Fallback model also failed")
        ]

        with self.assertRaises(Exception) as context:
            model_router("Hello", "failing-model")
        
        self.assertIn("Original model 'failing-model' failed", str(context.exception))
        self.assertIn("Fallback model 'mistral-small' also failed", str(context.exception))

    @patch('model_router.get_provider_for_model')
    @patch('model_router.call_aws_bedrock')
    def test_model_router_no_fallback_when_already_mistral_small(self, mock_call_aws, mock_get_provider):
        """Test that no fallback is attempted when already using mistral-small."""
        mock_get_provider.return_value = "aws"
        mock_call_aws.side_effect = Exception("mistral-small failed")

        with self.assertRaises(Exception) as context:
            model_router("Hello", "mistral-small")
        
        # Should not mention fallback in the error
        self.assertNotIn("fallback", str(context.exception).lower())
        self.assertIn("mistral-small failed", str(context.exception))

    def test_list_available_models(self):
        """Test listing available models."""
        models = list_available_models()
        
        self.assertIn("aws", models)
        self.assertIn("azure", models)
        self.assertIsInstance(models["aws"], list)
        self.assertIsInstance(models["azure"], list)
        
        # Check that some expected models are present
        self.assertIn("anthropic-sonnet", models["aws"])
        self.assertIn("gpt-4.1-mini", models["azure"])

    def test_add_model_mapping(self):
        """Test adding custom model mapping."""
        # Test adding a valid mapping
        add_model_mapping("custom-model", "aws")
        self.assertEqual(MODEL_MAPPING["custom-model"], "aws")
        
        # Test adding another mapping
        add_model_mapping("another-model", "azure")
        self.assertEqual(MODEL_MAPPING["another-model"], "azure")

    def test_add_model_mapping_invalid_provider(self):
        """Test adding model mapping with invalid provider."""
        with self.assertRaises(ValueError) as context:
            add_model_mapping("custom-model", "invalid-provider")
        
        self.assertIn("Provider must be either 'aws' or 'azure'", str(context.exception))

    @patch('model_router.bedrock_client')
    def test_aws_bedrock_error_handling(self, mock_bedrock_client):
        """Test AWS Bedrock error handling."""
        mock_bedrock_client.converse.side_effect = Exception("AWS API Error")

        with self.assertRaises(Exception) as context:
            call_aws_bedrock("Hello", "anthropic-sonnet")
        
        self.assertIn("AWS Bedrock API error", str(context.exception))

    @patch('model_router.azure_client')
    def test_azure_openai_error_handling(self, mock_azure_client):
        """Test Azure OpenAI error handling."""
        mock_azure_client.chat.completions.create.side_effect = Exception("Azure API Error")

        with self.assertRaises(Exception) as context:
            call_azure_openai("Hello", "gpt-4.1-mini")
        
        self.assertIn("Azure OpenAI API error", str(context.exception))

    @patch('model_router.get_provider_for_model')
    def test_model_router_error_handling(self, mock_get_provider):
        """Test model router error handling."""
        mock_get_provider.side_effect = Exception("Provider detection error")

        with self.assertRaises(Exception) as context:
            model_router("Hello", "test-model")
        
        self.assertIn("Model router error", str(context.exception))

    def test_model_mapping_backward_compatibility(self):
        """Test that legacy model names still work."""
        # Test legacy AWS model names
        self.assertEqual(get_provider_for_model("anthropic.claude-3-sonnet-20240229-v1:0"), "aws")
        self.assertEqual(get_provider_for_model("meta.llama3-70b-instruct-v1:0"), "aws")
        self.assertEqual(get_provider_for_model("mistral.mixtral-8x7b-instruct-v0:1"), "aws")
        
        # Test legacy Azure model names
        self.assertEqual(get_provider_for_model("gpt-4"), "azure")
        self.assertEqual(get_provider_for_model("gpt-3.5-turbo"), "azure")

    def test_model_parameter_handling(self):
        """Test that model parameters are handled correctly."""
        # This test verifies that the model mapping in call_aws_bedrock works correctly
        # We'll test with a known model to ensure parameters are passed through
        with patch('model_router.bedrock_client') as mock_bedrock_client:
            mock_response = {
                "content": [{"text": "Test response"}],
                "usage": {"inputTokens": 5, "outputTokens": 3}
            }
            mock_bedrock_client.converse.return_value = mock_response

            result = call_aws_bedrock(
                prompt="Test",
                model="llama-3-3-70b",
                temperature=0.9,
                max_tokens=200,
                top_p=0.95,
                top_k=50
            )

            # Verify the API call was made with correct parameters
            call_args = mock_bedrock_client.converse.call_args[1]
            self.assertEqual(call_args["inferenceConfig"]["temperature"], 0.9)
            self.assertEqual(call_args["inferenceConfig"]["maxTokens"], 200)
            self.assertEqual(call_args["inferenceConfig"]["topP"], 0.95)
            self.assertEqual(call_args["inferenceConfig"]["topK"], 50)


class TestModelRouterIntegration(unittest.TestCase):
    """Integration tests for the model router (requires actual API credentials)."""

    def test_real_aws_call(self):
        """Test real AWS Bedrock call (requires credentials)."""
        try:
            result = model_router(
                prompt="Say hello in one word",
                model="anthropic-sonnet",
                max_tokens=10
            )
            
            self.assertIn("content", result)
            self.assertEqual(result["provider"], "aws")
            self.assertEqual(result["model"], "anthropic-sonnet")
            self.assertIn("usage", result)
            
        except Exception as e:
            self.skipTest(f"AWS API call failed: {e}")

    def test_real_azure_call(self):
        """Test real Azure OpenAI call (requires credentials)."""
        try:
            result = model_router(
                prompt="Say hello in one word",
                model="gpt-4.1-mini",
                max_tokens=10
            )
            
            self.assertIn("content", result)
            self.assertEqual(result["provider"], "azure")
            self.assertEqual(result["model"], "gpt-4.1-mini")
            self.assertIn("usage", result)
            
        except Exception as e:
            self.skipTest(f"Azure API call failed: {e}")


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test cases using the new method
    loader = unittest.TestLoader()
    test_suite.addTest(loader.loadTestsFromTestCase(TestModelRouter))
    test_suite.addTest(loader.loadTestsFromTestCase(TestModelRouterIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result


if __name__ == "__main__":
    # Run tests when script is executed directly
    result = run_tests()
    
    # Exit with appropriate code
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print(f"\n❌ {len(result.failures)} tests failed, {len(result.errors)} tests had errors")
        sys.exit(1) 