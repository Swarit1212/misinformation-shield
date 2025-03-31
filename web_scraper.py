import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urlparse
import trafilatura

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_website_text_content(url: str) -> str:
    """
    This function takes a url and returns the main text content of the website.
    The text content is extracted using trafilatura and easier to understand.
    
    Args:
        url: The URL of the website to scrape
        
    Returns:
        A string containing the main text content of the website
    """
    try:
        # Send a request to the website
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            logger.warning(f"Failed to download content from {url}")
            return ""
            
        text = trafilatura.extract(downloaded)
        if not text:
            logger.warning(f"Failed to extract text from {url}")
            return ""
            
        return text
    except Exception as e:
        logger.error(f"Error scraping website {url}: {e}")
        return ""

def fetch_fact_check_article(url: str) -> dict:
    """
    Fetch a fact-checking article and extract relevant information.
    
    Args:
        url: The URL of the fact-checking article
        
    Returns:
        A dictionary containing information about the fact-check
    """
    result = {
        "url": url,
        "title": "",
        "content": "",
        "rating": "",
        "claim": "",
        "date": "",
    }
    
    try:
        # Get the domain to determine which parser to use
        domain = urlparse(url).netloc
        
        # Get the full text content
        result["content"] = get_website_text_content(url)
        
        # Use Beautiful Soup for more targeted extraction if needed
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract the title
        result["title"] = soup.title.text.strip() if soup.title else ""
        
        # Extract rating and other information based on the domain
        if "snopes.com" in domain:
            # Extract Snopes-specific information
            rating_elem = soup.select_one(".rating-label")
            if rating_elem:
                result["rating"] = rating_elem.text.strip()
                
            claim_elem = soup.select_one(".claim-text")
            if claim_elem:
                result["claim"] = claim_elem.text.strip()
                
        elif "politifact.com" in domain:
            # Extract PolitiFact-specific information
            rating_elem = soup.select_one(".meter-label")
            if rating_elem:
                result["rating"] = rating_elem.text.strip()
                
            claim_elem = soup.select_one(".statement__text")
            if claim_elem:
                result["claim"] = claim_elem.text.strip()
        
        # Add more site-specific parsers as needed
                
    except Exception as e:
        logger.error(f"Error parsing fact-check article {url}: {e}")
    
    return result
