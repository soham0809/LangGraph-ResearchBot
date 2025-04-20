"""Free search utility functions using DuckDuckGo."""
from typing import List, Dict, Any
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import time

from utils.config import MAX_SEARCH_RESULTS, SEARCH_TIMEOUT


def search_web(query: str, max_results: int = MAX_SEARCH_RESULTS) -> List[Dict[str, Any]]:
    """Search the web using DuckDuckGo (no API key required).
    
    Args:
        query: The search query
        max_results: Maximum number of results to return
        
    Returns:
        List of search results with title, link, and snippet
    """
    results = []
    try:
        with DDGS() as ddgs:
            search_results = list(ddgs.text(query, max_results=max_results))
            
            for result in search_results:
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "content": result.get("body", ""),
                })
    except Exception as e:
        print(f"DuckDuckGo search error: {str(e)}")
        # If DDG fails, return an empty list but don't crash
        pass
    
    # Fetch webpage content for each result to get more context
    for result in results:
        content = fetch_webpage_content(result["url"])
        if content:
            result["raw_content"] = content
    
    return results


def fetch_webpage_content(url: str, timeout: int = SEARCH_TIMEOUT) -> str:
    """Fetch and extract text content from a webpage.
    
    Args:
        url: The URL to fetch
        timeout: Request timeout in seconds
        
    Returns:
        Extracted text content or empty string on failure
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        
        # Get text
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up text (remove excessive whitespace)
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limit text length to avoid overly large results
        return text[:10000]
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return "" 