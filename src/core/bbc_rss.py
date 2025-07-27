#!/usr/bin/env python3
"""
BBC RSS Feed Tool
Fetches and parses BBC RSS feeds to extract news articles and public figures.
"""

import requests
import xml.etree.ElementTree as ET
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_bbc_rss_feed(feed_url: str = "https://feeds.bbci.co.uk/news/rss.xml?edition=uk") -> Dict[str, Any]:
    """
    Fetch and parse BBC RSS feed.
    
    Args:
        feed_url (str): URL of the BBC RSS feed
        
    Returns:
        Dict[str, Any]: Parsed RSS feed data with articles and metadata
    """
    try:
        logger.info(f"Fetching BBC RSS feed from: {feed_url}")
        
        # Fetch the RSS feed
        response = requests.get(feed_url, timeout=10)
        response.raise_for_status()
        
        # Parse XML
        root = ET.fromstring(response.content)
        
        # Extract feed metadata
        channel = root.find('channel')
        if channel is None:
            raise ValueError("Invalid RSS feed format: no channel element found")
        
        feed_data = {
            "title": _get_text(channel, 'title'),
            "description": _get_text(channel, 'description'),
            "link": _get_text(channel, 'link'),
            "last_updated": _get_text(channel, 'lastBuildDate'),
            "articles": []
        }
        
        # Extract articles
        for item in channel.findall('item'):
            article = {
                "title": _get_text(item, 'title'),
                "description": _get_text(item, 'description'),
                "link": _get_text(item, 'link'),
                "pub_date": _get_text(item, 'pubDate'),
                "guid": _get_text(item, 'guid'),
                "category": _get_text(item, 'category')
            }
            feed_data["articles"].append(article)
        
        logger.info(f"Successfully parsed {len(feed_data['articles'])} articles")
        return feed_data
        
    except requests.RequestException as e:
        logger.error(f"Failed to fetch RSS feed: {e}")
        raise Exception(f"Failed to fetch BBC RSS feed: {str(e)}")
    except ET.ParseError as e:
        logger.error(f"Failed to parse RSS XML: {e}")
        raise Exception(f"Failed to parse RSS feed XML: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise Exception(f"Error processing BBC RSS feed: {str(e)}")


def extract_public_figures_from_articles(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Extract public figures from article titles and descriptions.
    
    Args:
        articles (List[Dict]): List of articles from RSS feed
        
    Returns:
        List[Dict]: List of public figures with their context
    """
    public_figures = []
    
    # Common patterns for public figures
    patterns = [
        r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b',  # First Last names
        r'\b([A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+)\b',  # First Middle Last names
        r'\b([A-Z][a-z]+ [A-Z][a-z]+-[A-Z][a-z]+)\b',  # Hyphenated last names
    ]
    
    # Common titles and prefixes
    titles = [
        'Prime Minister', 'President', 'King', 'Queen', 'Prince', 'Princess',
        'Sir', 'Dame', 'Lord', 'Lady', 'Dr', 'Professor', 'Prof',
        'CEO', 'Director', 'Manager', 'Coach', 'Captain'
    ]
    
    for article in articles:
        text_to_search = f"{article['title']} {article['description']}"
        
        # Look for titled figures
        for title in titles:
            title_pattern = rf'\b({title}\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'
            matches = re.finditer(title_pattern, text_to_search, re.IGNORECASE)
            for match in matches:
                figure_name = match.group(1)
                public_figures.append({
                    "name": figure_name,
                    "title": title,
                    "context": article['title'],
                    "article_link": article['link'],
                    "source": "BBC RSS"
                })
        
        # Look for name patterns
        for pattern in patterns:
            matches = re.finditer(pattern, text_to_search)
            for match in matches:
                name = match.group(1)
                
                # Filter out common words that aren't names
                if _is_likely_person_name(name):
                    public_figures.append({
                        "name": name,
                        "title": None,
                        "context": article['title'],
                        "article_link": article['link'],
                        "source": "BBC RSS"
                    })
    
    # Remove duplicates while preserving order
    seen = set()
    unique_figures = []
    for figure in public_figures:
        name_key = figure['name'].lower()
        if name_key not in seen:
            seen.add(name_key)
            unique_figures.append(figure)
    
    logger.info(f"Extracted {len(unique_figures)} unique public figures")
    return unique_figures


def get_bbc_public_figures() -> Dict[str, Any]:
    """
    Get public figures from BBC RSS feed.
    
    Returns:
        Dict[str, Any]: Public figures data with metadata
    """
    try:
        # Get RSS feed
        feed_data = get_bbc_rss_feed()
        
        # Extract public figures
        public_figures = extract_public_figures_from_articles(feed_data['articles'])
        
        return {
            "source": "BBC RSS Feed",
            "feed_title": feed_data['title'],
            "feed_description": feed_data['description'],
            "last_updated": feed_data['last_updated'],
            "total_articles": len(feed_data['articles']),
            "public_figures": public_figures,
            "total_figures": len(public_figures)
        }
        
    except Exception as e:
        logger.error(f"Failed to get BBC public figures: {e}")
        raise Exception(f"Failed to get BBC public figures: {str(e)}")


def get_bbc_news_summary(category: Optional[str] = None, max_articles: int = 10) -> Dict[str, Any]:
    """
    Get a summary of current BBC news with categorized articles.
    
    Args:
        category (Optional[str]): Filter by category (e.g., 'politics', 'technology', 'sports')
        max_articles (int): Maximum number of articles to return
        
    Returns:
        Dict[str, Any]: News summary with categorized articles and key topics
    """
    try:
        # Get RSS feed
        feed_data = get_bbc_rss_feed()
        
        # Filter articles if category is specified
        articles = feed_data['articles']
        if category:
            category_lower = category.lower()
            articles = [
                article for article in articles 
                if category_lower in article.get('category', '').lower() or
                   category_lower in article.get('title', '').lower() or
                   category_lower in article.get('description', '').lower()
            ]
        
        # Limit articles
        articles = articles[:max_articles]
        
        # Categorize articles
        categories = {}
        for article in articles:
            cat = article.get('category', 'General')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(article)
        
        # Extract key topics and public figures
        public_figures = extract_public_figures_from_articles(articles)
        
        # Create summary
        summary = {
            "source": "BBC News",
            "feed_title": feed_data['title'],
            "last_updated": feed_data['last_updated'],
            "total_articles": len(articles),
            "categories": categories,
            "key_topics": list(categories.keys()),
            "public_figures": public_figures,
            "top_headlines": [article['title'] for article in articles[:5]],
            "summary": f"Latest news from BBC covering {len(categories)} categories with {len(articles)} articles"
        }
        
        logger.info(f"Generated news summary with {len(articles)} articles across {len(categories)} categories")
        return summary
        
    except Exception as e:
        logger.error(f"Failed to get BBC news summary: {e}")
        raise Exception(f"Failed to get BBC news summary: {str(e)}")


def get_bbc_latest_news() -> Dict[str, Any]:
    """
    Get the latest BBC news headlines and summaries.
    
    Returns:
        Dict[str, Any]: Latest news with headlines and brief summaries
    """
    try:
        # Get RSS feed
        feed_data = get_bbc_rss_feed()
        
        # Get latest articles (first 10)
        latest_articles = feed_data['articles'][:10]
        
        # Create news summary
        news_summary = {
            "source": "BBC News",
            "last_updated": feed_data['last_updated'],
            "total_articles": len(latest_articles),
            "headlines": [],
            "breaking_news": [],
            "top_stories": []
        }
        
        for i, article in enumerate(latest_articles):
            headline_info = {
                "title": article['title'],
                "description": article['description'],
                "link": article['link'],
                "category": article.get('category', 'General'),
                "pub_date": article['pub_date']
            }
            
            news_summary["headlines"].append(headline_info)
            
            # Identify breaking news (recent articles)
            if i < 3:
                news_summary["breaking_news"].append(headline_info)
            
            # Top stories (first 5)
            if i < 5:
                news_summary["top_stories"].append(headline_info)
        
        # Extract public figures for context
        public_figures = extract_public_figures_from_articles(latest_articles)
        news_summary["key_figures"] = public_figures[:10]  # Top 10 figures
        
        logger.info(f"Generated latest news summary with {len(latest_articles)} headlines")
        return news_summary
        
    except Exception as e:
        logger.error(f"Failed to get BBC latest news: {e}")
        raise Exception(f"Failed to get BBC latest news: {str(e)}")


def _get_text(element: ET.Element, tag: str) -> str:
    """Helper function to safely extract text from XML element."""
    child = element.find(tag)
    return child.text if child is not None else ""


def _is_likely_person_name(name: str) -> bool:
    """Check if a string is likely to be a person's name."""
    # Filter out common non-name words
    common_words = {
        'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
        'after', 'above', 'below', 'between', 'among', 'within', 'without',
        'against', 'toward', 'towards', 'upon', 'across', 'behind', 'beneath',
        'beside', 'beyond', 'inside', 'outside', 'under', 'over', 'around',
        'along', 'down', 'off', 'out', 'away', 'back', 'forth', 'forward',
        'backward', 'upward', 'downward', 'north', 'south', 'east', 'west',
        'northern', 'southern', 'eastern', 'western', 'central', 'middle',
        'high', 'low', 'big', 'small', 'large', 'tiny', 'huge', 'massive',
        'new', 'old', 'young', 'fresh', 'stale', 'hot', 'cold', 'warm',
        'cool', 'bright', 'dark', 'light', 'heavy', 'strong', 'weak',
        'good', 'bad', 'great', 'terrible', 'wonderful', 'awful', 'nice',
        'mean', 'kind', 'cruel', 'happy', 'sad', 'angry', 'calm', 'quiet',
        'loud', 'soft', 'hard', 'easy', 'difficult', 'simple', 'complex',
        'clear', 'confusing', 'obvious', 'hidden', 'visible', 'invisible',
        'open', 'closed', 'full', 'empty', 'complete', 'incomplete',
        'finished', 'unfinished', 'done', 'undone', 'ready', 'unready',
        'prepared', 'unprepared', 'organized', 'disorganized', 'clean',
        'dirty', 'neat', 'messy', 'tidy', 'untidy', 'orderly', 'chaotic',
        'peaceful', 'violent', 'safe', 'dangerous', 'secure', 'insecure',
        'stable', 'unstable', 'steady', 'unsteady', 'firm', 'loose',
        'tight', 'loose', 'fast', 'slow', 'quick', 'gradual', 'sudden',
        'immediate', 'delayed', 'early', 'late', 'on', 'off', 'start',
        'stop', 'begin', 'end', 'continue', 'pause', 'resume', 'break',
        'fix', 'repair', 'damage', 'destroy', 'build', 'create', 'make',
        'do', 'have', 'get', 'take', 'give', 'send', 'receive', 'accept',
        'reject', 'approve', 'deny', 'allow', 'prevent', 'block', 'help',
        'hinder', 'support', 'oppose', 'agree', 'disagree', 'like',
        'dislike', 'love', 'hate', 'want', 'need', 'must', 'should',
        'could', 'would', 'can', 'will', 'shall', 'may', 'might'
    }
    
    words = name.lower().split()
    if len(words) < 2:
        return False
    
    # Check if any word is in the common words list
    for word in words:
        if word in common_words:
            return False
    
    # Check if it looks like a proper name (starts with capital letters)
    if not re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+$', name):
        return False
    
    return True


# Tool function for integration with the model router
def bbc_rss_tool(action: str, **kwargs) -> Dict[str, Any]:
    """
    Tool function for BBC RSS operations.
    
    Args:
        action (str): The action to perform ('get_feed', 'get_public_figures', 'get_news_summary', 'get_latest_news')
        **kwargs: Additional arguments
        
    Returns:
        Dict[str, Any]: Tool response
    """
    try:
        if action == "get_feed":
            feed_url = kwargs.get('feed_url', "https://feeds.bbci.co.uk/news/rss.xml?edition=uk")
            return get_bbc_rss_feed(feed_url)
        
        elif action == "get_public_figures":
            return get_bbc_public_figures()
        
        elif action == "get_news_summary":
            category = kwargs.get('category')
            max_articles = kwargs.get('max_articles', 10)
            return get_bbc_news_summary(category, max_articles)
        
        elif action == "get_latest_news":
            return get_bbc_latest_news()
        
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
        result = get_bbc_public_figures()
        print("BBC Public Figures:")
        print(f"Total figures found: {result['total_figures']}")
        for figure in result['public_figures'][:5]:  # Show first 5
            print(f"- {figure['name']} (Context: {figure['context'][:50]}...)")
    except Exception as e:
        print(f"Error: {e}") 