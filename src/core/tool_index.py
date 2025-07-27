#!/usr/bin/env python3
"""
Tool Index Configuration
Defines all available tools and their metadata for the Ultimate AI Personal Assistant.
"""

from typing import Dict, List, Any

# Tool registry with metadata
TOOL_REGISTRY = {
    "time_and_date": {
        "name": "Time and Date Tool",
        "description": "Get current time, date, and timezone information",
        "module": "tools.tool_modules.time_and_date",
        "functions": {
            "get_current_time": {
                "description": "Get current time in specified timezone",
                "parameters": {
                    "timezone": {
                        "type": "string",
                        "description": "Timezone (e.g., 'UTC', 'America/New_York')",
                        "required": False
                    }
                }
            },
            "get_current_date": {
                "description": "Get current date in specified format",
                "parameters": {
                    "format": {
                        "type": "string",
                        "description": "Date format (e.g., 'YYYY-MM-DD', 'DD/MM/YYYY')",
                        "required": False
                    }
                }
            }
        }
    },
    
    "web_search_brave": {
        "name": "Brave Web Search Tool",
        "description": "Search the web using Brave Search API",
        "module": "tools.tool_modules.web_search_brave",
        "functions": {
            "search_web": {
                "description": "Search the web for information",
                "parameters": {
                    "query": {
                        "type": "string",
                        "description": "Search query",
                        "required": True
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "required": False
                    }
                }
            }
        }
    },
    
    "bbc_rss": {
        "name": "BBC News Tool",
        "description": "Get current news, headlines, and summaries from BBC News",
        "module": "tools.tool_modules.bbc_rss",
        "functions": {
            "get_bbc_latest_news": {
                "description": "Get the latest BBC news headlines and summaries",
                "parameters": {}
            },
            "get_bbc_news_summary": {
                "description": "Get a summary of current BBC news with categorized articles",
                "parameters": {
                    "category": {
                        "type": "string",
                        "description": "Filter by category (e.g., 'politics', 'technology', 'sports', 'business')",
                        "required": False
                    },
                    "max_articles": {
                        "type": "integer",
                        "description": "Maximum number of articles to return",
                        "required": False,
                        "default": 10
                    }
                }
            },
            "get_bbc_public_figures": {
                "description": "Get public figures mentioned in BBC news",
                "parameters": {}
            },
            "get_bbc_rss_feed": {
                "description": "Fetch and parse BBC RSS feed",
                "parameters": {
                    "feed_url": {
                        "type": "string",
                        "description": "URL of the BBC RSS feed",
                        "required": False,
                        "default": "https://feeds.bbci.co.uk/news/rss.xml?edition=uk"
                    }
                }
            }
        }
    },
    
    "wikipedia_api": {
        "name": "Wikipedia API Tool",
        "description": "Search and fetch information from Wikipedia using their API",
        "module": "tools.tool_modules.wikipedia_api",
        "functions": {
            "search_wikipedia": {
                "description": "Search Wikipedia for articles matching the query",
                "parameters": {
                    "query": {
                        "type": "string",
                        "description": "Search query",
                        "required": True
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "required": False,
                        "default": 10
                    }
                }
            },
            "get_wikipedia_page": {
                "description": "Get detailed information about a Wikipedia page",
                "parameters": {
                    "title": {
                        "type": "string",
                        "description": "Page title",
                        "required": True
                    }
                }
            },
            "find_person_wikipedia_page": {
                "description": "Find Wikipedia page for a specific person",
                "parameters": {
                    "person_name": {
                        "type": "string",
                        "description": "Name of the person to search for",
                        "required": True
                    }
                }
            },
            "get_multiple_people_wikipedia_pages": {
                "description": "Get Wikipedia pages for multiple people",
                "parameters": {
                    "person_names": {
                        "type": "array",
                        "description": "List of person names",
                        "required": True
                    }
                }
            }
        }
    }
}


def get_tool_info(tool_name: str) -> Dict[str, Any]:
    """
    Get information about a specific tool.
    
    Args:
        tool_name (str): Name of the tool
        
    Returns:
        Dict[str, Any]: Tool information
    """
    return TOOL_REGISTRY.get(tool_name, {})


def list_available_tools() -> List[str]:
    """
    Get list of all available tool names.
    
    Returns:
        List[str]: List of tool names
    """
    return list(TOOL_REGISTRY.keys())


def get_tool_functions(tool_name: str) -> Dict[str, Any]:
    """
    Get functions available for a specific tool.
    
    Args:
        tool_name (str): Name of the tool
        
    Returns:
        Dict[str, Any]: Tool functions
    """
    tool_info = get_tool_info(tool_name)
    return tool_info.get("functions", {})


def get_tool_schema(tool_name: str, function_name: str) -> Dict[str, Any]:
    """
    Get JSON schema for a specific tool function.
    
    Args:
        tool_name (str): Name of the tool
        function_name (str): Name of the function
        
    Returns:
        Dict[str, Any]: Function schema
    """
    functions = get_tool_functions(tool_name)
    function_info = functions.get(function_name, {})
    
    if not function_info:
        return {}
    
    return {
        "name": function_name,
        "description": function_info.get("description", ""),
        "parameters": {
            "type": "object",
            "properties": function_info.get("parameters", {}),
            "required": [
                param for param, info in function_info.get("parameters", {}).items()
                if info.get("required", False)
            ]
        }
    }


def get_all_tool_schemas() -> List[Dict[str, Any]]:
    """
    Get JSON schemas for all available tools.
    
    Returns:
        List[Dict[str, Any]]: List of tool schemas
    """
    schemas = []
    
    for tool_name in list_available_tools():
        functions = get_tool_functions(tool_name)
        
        for function_name in functions:
            schema = get_tool_schema(tool_name, function_name)
            if schema:
                schemas.append(schema)
    
    return schemas


if __name__ == "__main__":
    # Print available tools
    print("Available Tools:")
    for tool_name in list_available_tools():
        tool_info = get_tool_info(tool_name)
        print(f"  • {tool_name}: {tool_info['description']}")
        
        functions = get_tool_functions(tool_name)
        for func_name in functions:
            print(f"    - {func_name}")
    
    print(f"\nTotal tools: {len(list_available_tools())}")
    print(f"Total functions: {len(get_all_tool_schemas())}") 