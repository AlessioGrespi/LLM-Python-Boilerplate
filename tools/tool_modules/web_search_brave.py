from time import sleep
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
disallowed_domains = eval(os.getenv("DISALLOWED_DOMAINS", "[]"))  # Convert string to list

def get_search_results(search_query, num_results=5, page=0):
    """Allows the user to make a web search based on the search query"""
    headers = {"Accept": "application/json", "X-Subscription-Token": BRAVE_API_KEY}
    response = requests.get(
        "https://api.search.brave.com/res/v1/web/search",
        params={"q": search_query,
                "count": num_results  # Max number of results to return
                },
        headers=headers,
        timeout=60
    )
    if not response.ok:
        raise Exception(f"HTTP error {response.status_code}")
    sleep(1)  # avoid Brave rate limit

    results = response.json().get("web", {}).get("results", [])
    simplified_results = [{'title': result.get('title'), 'url': result.get('url')} for result in results]
    return simplified_results
