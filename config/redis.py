import redis
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT", 6379))  # Default to 6379 if not set
redis_password = os.getenv("REDIS_PASSWORD")
redis_ssl = os.getenv("REDIS_SSL", "True").lower() in ["true", "1", "t", "y", "yes"]  # Convert to boolean

# Redis connection
r = redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    ssl=redis_ssl
)

# Save conversation message to Redis
def save_to_redis(session_id, role, content):
    """
    Saves a conversation message to Redis under a session ID.
    Args:
        session_id (str): The unique ID for the user's conversation session.
        role (str): The role of the message sender ('user' or 'model').
        content (str): The message content.
    """
    redis_key = f"conversation:{session_id}"
    message = {"role": role, "content": content}
    r.rpush(redis_key, str(message))  # Store messages as strings

def get_conversation_from_redis(session_id):
    """
    Retrieves the conversation history for a given session ID from Redis.
    Args:
        session_id (str): The unique ID for the user's conversation session.
    Returns:
        list: The conversation history as a list of messages.
    """
    redis_key = f"conversation:{session_id}"
    messages = r.lrange(redis_key, 0, -1)
    return [eval(message) for message in messages]  # Convert back to dict
