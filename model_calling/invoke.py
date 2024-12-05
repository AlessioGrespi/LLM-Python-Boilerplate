
from config.aws import bedrock_client    
temperature = 0.9
    
def call_model(model, messages, system_prompts, tool_config):
    match model:
        case "llama-3-1-70b":
            model_id = "arn:aws:bedrock:us-east-1:862671257329:inference-profile/us.meta.llama3-1-70b-instruct-v1:0"
            temperature = 0.9
        case "mixtral-8x7b":
            model_id = "mistral.mixtral-8x7b-instruct-v0:1"
        case "amazon-premier":
            model_id = 'amazon.titan-text-premier-v1:0'
        case "mistral-large":
            model_id = "mistral.mistral-large-2402-v1:0"
            temperature = 0.9
        case "mistral-small":
            model_id = "mistral.mistral-small-2402-v1:0"
            temperature = 0.9
        case "anthropic-sonnet":
            model_id = "arn:aws:bedrock:us-east-1:862671257329:inference-profile/us.anthropic.claude-3-5-sonnet-20241022-v2:0"
            temperature = 0.9
        case "anthropic-haiku":
            model_id = "arn:aws:bedrock:us-east-1:862671257329:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0"
            temperature = 0.9
    
    inference_config = {"temperature": temperature}
    
    
    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        system=system_prompts,
        inferenceConfig=inference_config,
        toolConfig=tool_config
    )
    
    return response