#!/usr/bin/env python3
"""
Wikipedia API Tool
Searches and fetches information from Wikipedia using their API.
"""

import requests
import json
from typing import Dict, List, Any, Optional
import logging
from urllib.parse import quote

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Wikipedia API base URL
WIKIPEDIA_API_BASE = "https://en.wikipedia.org/api/rest_v1"


def search_wikipedia(query: str, limit: int = 10) -> Dict[str, Any]:
    """
    Search Wikipedia for articles matching the query.
    
    Args:
        query (str): Search query
        limit (int): Maximum number of results to return
        
    Returns:
        Dict[str, Any]: Search results with metadata
    """
    try:
        logger.info(f"Searching Wikipedia for: {query}")
        
        # Use Wikipedia's search API (correct endpoint)
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "srlimit": limit,
            "utf8": 1
        }
        
        response = requests.get(search_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract search results
        search_results = []
        if "query" in data and "search" in data["query"]:
            for page in data["query"]["search"]:
                result = {
                    "title": page.get("title", ""),
                    "page_id": page.get("pageid", ""),
                    "snippet": page.get("snippet", ""),
                    "url": f"https://en.wikipedia.org/wiki/{page.get('title', '').replace(' ', '_')}"
                }
                search_results.append(result)
        
        return {
            "query": query,
            "total_results": len(search_results),
            "results": search_results,
            "success": True
        }
        
    except requests.RequestException as e:
        logger.error(f"Failed to search Wikipedia: {e}")
        return {
            "query": query,
            "error": f"Failed to search Wikipedia: {str(e)}",
            "success": False
        }
    except Exception as e:
        logger.error(f"Unexpected error searching Wikipedia: {e}")
        return {
            "query": query,
            "error": f"Error searching Wikipedia: {str(e)}",
            "success": False
        }


def get_wikipedia_page(title: str) -> Dict[str, Any]:
    """
    Get detailed information about a Wikipedia page.
    
    Args:
        title (str): Page title (can be URL-encoded)
        
    Returns:
        Dict[str, Any]: Page information
    """
    try:
        logger.info(f"Fetching Wikipedia page: {title}")
        
        # Get page content using Wikipedia API
        api_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "extracts|info",
            "exintro": 1,
            "explaintext": 1,
            "inprop": "url",
            "utf8": 1
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract page information
        pages = data.get("query", {}).get("pages", {})
        page_info = {"success": False}
        
        for page_id, page_data in pages.items():
            if page_id != "-1":  # Page exists
                page_info = {
                    "title": page_data.get("title", ""),
                    "page_id": page_data.get("pageid", ""),
                    "extract": page_data.get("extract", ""),
                    "url": page_data.get("fullurl", ""),
                    "canonicalurl": page_data.get("canonicalurl", ""),
                    "content_urls": {
                        "desktop": {
                            "page": page_data.get("fullurl", "")
                        }
                    },
                    "success": True
                }
                break
        
        return page_info
        
    except requests.RequestException as e:
        logger.error(f"Failed to fetch Wikipedia page: {e}")
        return {
            "title": title,
            "error": f"Failed to fetch Wikipedia page: {str(e)}",
            "success": False
        }
    except Exception as e:
        logger.error(f"Unexpected error fetching Wikipedia page: {e}")
        return {
            "title": title,
            "error": f"Error fetching Wikipedia page: {str(e)}",
            "success": False
        }


def find_person_wikipedia_page(person_name: str) -> Dict[str, Any]:
    """
    Find Wikipedia page for a specific person.
    
    Args:
        person_name (str): Name of the person to search for
        
    Returns:
        Dict[str, Any]: Person's Wikipedia information
    """
    try:
        logger.info(f"Finding Wikipedia page for person: {person_name}")
        
        # First, search for the person
        search_results = search_wikipedia(person_name, limit=5)
        
        if not search_results.get("success", False):
            return search_results
        
        # Look for the best match
        best_match = None
        for result in search_results["results"]:
            title = result["title"].lower()
            person_lower = person_name.lower()
            
            # Check for exact match or very close match
            if (person_lower in title or 
                title in person_lower or 
                person_lower.replace(" ", "_") in title or
                title.replace("_", " ") in person_lower):
                best_match = result
                break
        
        # If no exact match, take the first result
        if not best_match and search_results["results"]:
            best_match = search_results["results"][0]
        
        if best_match:
            # Get detailed page information
            page_info = get_wikipedia_page(best_match["title"])
            
            return {
                "person_name": person_name,
                "search_results": search_results,
                "best_match": best_match,
                "page_info": page_info,
                "success": True
            }
        else:
            return {
                "person_name": person_name,
                "error": "No Wikipedia page found for this person",
                "success": False
            }
            
    except Exception as e:
        logger.error(f"Error finding Wikipedia page for person: {e}")
        return {
            "person_name": person_name,
            "error": f"Error finding Wikipedia page: {str(e)}",
            "success": False
        }


def get_multiple_people_wikipedia_pages(person_names: List[str]) -> Dict[str, Any]:
    """
    Get Wikipedia pages for multiple people.
    
    Args:
        person_names (List[str]): List of person names
        
    Returns:
        Dict[str, Any]: Wikipedia information for all people
    """
    try:
        logger.info(f"Finding Wikipedia pages for {len(person_names)} people")
        
        results = []
        successful = 0
        failed = 0
        
        for person_name in person_names:
            person_result = find_person_wikipedia_page(person_name)
            results.append(person_result)
            
            if person_result.get("success", False):
                successful += 1
            else:
                failed += 1
        
        return {
            "total_people": len(person_names),
            "successful": successful,
            "failed": failed,
            "results": results,
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error processing multiple people: {e}")
        return {
            "error": f"Error processing multiple people: {str(e)}",
            "success": False
        }


# Tool function for integration with the model router
def wikipedia_api_tool(action: str, **kwargs) -> Dict[str, Any]:
    """
    Tool function for Wikipedia API operations.
    
    Args:
        action (str): The action to perform ('search', 'get_page', 'find_person', 'get_multiple_people')
        **kwargs: Additional arguments
        
    Returns:
        Dict[str, Any]: Tool response
    """
    try:
        if action == "search":
            query = kwargs.get('query', '')
            limit = kwargs.get('limit', 10)
            return search_wikipedia(query, limit)
        
        elif action == "get_page":
            title = kwargs.get('title', '')
            return get_wikipedia_page(title)
        
        elif action == "find_person":
            person_name = kwargs.get('person_name', '')
            return find_person_wikipedia_page(person_name)
        
        elif action == "get_multiple_people":
            person_names = kwargs.get('person_names', [])
            return get_multiple_people_wikipedia_pages(person_names)
        
        else:
            raise ValueError(f"Unknown action: {action}")
            
    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }


if __name__ == "__main__":
    # Test the tool
    try:
        # Test search
        print("Testing Wikipedia search...")
        search_result = search_wikipedia("Donald Trump")
        print(f"Search results: {search_result['total_results']} found")
        
        # Test person lookup
        print("\nTesting person lookup...")
        person_result = find_person_wikipedia_page("Donald Trump")
        if person_result.get("success"):
            print(f"Found page: {person_result['page_info']['title']}")
            print(f"Extract: {person_result['page_info']['extract'][:100]}...")
        else:
            print(f"Error: {person_result.get('error')}")
            
    except Exception as e:
        print(f"Error: {e}") 