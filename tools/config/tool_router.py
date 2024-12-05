from tools.tool_modules.time_and_date import get_time_and_timezone_info as time_and_date

def tool_router(output_message):
    """Routes tool requests to the appropriate tool and returns the result."""
    tool_requests = output_message["content"]

    for tool_request in tool_requests:
        if "toolUse" in tool_request:
            tool = tool_request["toolUse"]
            tool_use_id = tool["toolUseId"]  # Extract the tool use ID

            # Route the request to the appropriate tool
            match tool["name"]:
                case "time_and_date":
                    try:
                        time_info = time_and_date()  # Get the time and date info
                        return {
                            "toolUseId": tool_use_id,
                            "content": [{"json": time_info}],  # Returning as structured JSON
                            "status": "success"
                        }
                    except Exception as e:
                        return {
                            "toolUseId": tool_use_id,
                            "content": [{"text": f"Error fetching time info: {str(e)}"}],
                            "status": "error"
                        }

                # Handle unsupported tools
                case _:
                    return {
                        "toolUseId": tool_use_id,
                        "content": [{"text": f"Tool '{tool['name']}' is not supported."}],
                        "status": "error"
                    }
