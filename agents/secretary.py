import redis
import boto3
from botocore.exceptions import ClientError
from model_calling.invoke import call_model
from config.redis import save_to_redis
from tools.config.tool_index import tool_config
from tools.config.tool_router import tool_router

# model = "llama-3-1-70b"
# model = "mistral-large"
model = "anthropic-haiku"




system_prompts = [
    {
        "text": """
            You are a helpful of secretary with a myriad of tools, help your boss with the tasks asked of you. If you need to ask questions do so. 
"""
    }
]


# Tool for building (as per your request)
def save_memory(tool_message):
    print("save memory")

    return tool_message  # Return the output message to the caller

def generate_conversation(system_prompts, messages, tool_config, session_id):
    """Generates conversation and handles tool use requests."""
    response = call_model(model, messages, system_prompts, tool_config)

    output_message = response["output"]["message"]
    stop_reason = response.get("stopReason")
    print("convo response", response)

    # Handle tool use requests.
    if stop_reason == "tool_use":
        tool_output = tool_router(output_message)  # Get tool result
        tool_use_id = output_message["content"][1]["toolUse"]["toolUseId"]  # Extract toolUseId
        print("Tool output:", tool_output)

        # Return both the tool's output and assistant response
        return {
            "output_message": output_message,  # Assistant response
            "tool_output": tool_output,  # Tool response
            "tool_use_id": tool_use_id  # Tool usage identifier
        }
    else:
        # Save model response to Redis
        save_to_redis(session_id, "model", output_message["content"][0]["text"])

    return {"output_message": output_message}

def main(session_id):
    """Main function to handle continuous conversation with tool support."""
    messages = []

    try:
        print("How can I help you? (type 'quit' to exit).")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "quit":
                print("Ending the conversation. Goodbye!")
                quit()

            # Save user input to Redis
            save_to_redis(session_id, "user", user_input)

            # Add user input to conversation history.
            messages.append({"role": "user", "content": [{"text": user_input}]})

            # Generate response with tool support.
            convo_result = generate_conversation(
                system_prompts,
                messages,
                tool_config,
                session_id,
            )

            output_message = convo_result["output_message"]
            tool_output = convo_result.get("tool_output")

            # Handle the assistant's response
            if "content" in output_message:
                print("Model:", output_message["content"][0]["text"])

            # Handle tool output
            if tool_output:
                print("Tool Output:", tool_output["content"][0]["json"])

            messages.append(output_message)

    except ClientError as err:
        print(f"A client error occurred: {err.response['Error']['Message']}")
        return {"content": [{"text": "A client error occurred."}]}


if __name__ == "__main__":
    main()


