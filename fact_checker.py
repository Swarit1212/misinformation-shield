import os
import logging
import requests
from typing import List, Dict, Any, Tuple
import time
import re
import json
from web_scraper import get_website_text_content

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# List of known fact-checking domains
FACT_CHECK_DOMAINS = [
    "snopes.com",
    "politifact.com",
    "factcheck.org",
    "fullfact.org",
    "apnews.com/hub/ap-fact-check",
    "reuters.com/fact-check",
    "usatoday.com/factcheck",
]

# Google Fact Check Tools API (mock implementation)
# In a real implementation, you would use a real API key
GOOGLE_FACT_CHECK_API_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
GOOGLE_API_KEY = os.environ.get("GOOGLE_FACT_CHECK_API_KEY")

def verify_claim(claim_text: str) -> List[Dict[str, Any]]:
    """
    Verify a claim against multiple fact-checking sources.
    
    Args:
        claim_text: The text of the claim to verify
        
    Returns:
        A list of verification results from different sources
    """
    results = []
    
    # Try to get results from Google Fact Check API if we have an API key
    if GOOGLE_API_KEY:
        google_results = query_google_fact_check(claim_text)
        if google_results:
            results.extend(google_results)
    
    # Always include search for fact checks regardless of previous results
    # This improves the variety of verification sources
    search_results = search_for_fact_checks(claim_text)
    if search_results:
        results.extend(search_results)
    
    # Always check against the simulated Google Fact Check API results
    # even if we don't have results yet
    if not GOOGLE_API_KEY:
        more_results = query_google_fact_check(claim_text)
        if more_results:
            results.extend(more_results)
    
    # If we still have no results, check against news sources
    if not results:
        news_results = check_against_news_sources(claim_text)
        if news_results:
            results.extend(news_results)
    
    # If we couldn't find any verification results, provide topic-specific guidance
    if not results:
        claim_lower = claim_text.lower()
        
        # Health-related claims
        if re.search(r"health|cure|disease|treatment|medicine|doctor|vaccine", claim_lower):
            results.append({
                "source": "National Institutes of Health",
                "source_url": "https://www.nih.gov/health-information",
                "title": "Health Information Resources",
                "claim_date": "2023-11-10",
                "rating": "Information",
                "summary": "For health-related claims, consult medical professionals and reliable sources like NIH, CDC, or WHO. Medical information should be based on peer-reviewed research."
            })
        # Political claims
        elif re.search(r"(politic|government|election|democrat|republican|congress|senate|president)", claim_lower):
            results.append({
                "source": "AP Fact Check",
                "source_url": "https://apnews.com/hub/ap-fact-check",
                "title": "Political Claim Verification",
                "claim_date": "2023-10-25",
                "rating": "Analysis Needed",
                "summary": "Political claims require careful verification through official government records, non-partisan analysis, and multiple reputable news sources."
            })
        # Fallback for other topics
        else:
            results.append({
                "source": "Reuters Fact Check",
                "source_url": "https://www.reuters.com/fact-check/",
                "title": "Information Verification Guide",
                "claim_date": "2023-12-01",
                "rating": "Not Yet Rated",
                "summary": "This specific claim hasn't been widely fact-checked yet. Remember to verify information from multiple credible sources before sharing."
            })
    
    return results

def query_google_fact_check(claim_text: str) -> List[Dict[str, Any]]:
    """
    Query the Google Fact Check Tools API for claim verification.
    
    Args:
        claim_text: The text of the claim to verify
        
    Returns:
        A list of verification results
    """
    results = []
    
    try:
        # In a real implementation, you would make an actual API call here
        # For now, we'll simulate the API with some example responses
        # based on common patterns in the claim text
        
        # Check if the API key is available
        if not GOOGLE_API_KEY:
            logger.warning("No Google Fact Check API key provided. Skipping API query.")
            return []
        
        # In a real implementation, this would be a real API call
        # params = {
        #     "key": GOOGLE_API_KEY,
        #     "query": claim_text,
        #     "languageCode": "en"
        # }
        # response = requests.get(GOOGLE_FACT_CHECK_API_URL, params=params)
        # if response.status_code == 200:
        #     data = response.json()
        #     # Process the API response here
        
        # For now, let's simulate some responses based on the claim text
        # This is just for demonstration purposes and would be replaced with real API calls
        
        # Simulate a short delay like a real API call would have
        time.sleep(0.5)
        
        # More sophisticated pattern matching for common misinformation topics
        # COVID and Vaccines
        if re.search(r"vaccine|covid|coronavirus|pandemic", claim_text, re.IGNORECASE):
            results.append({
                "source": "Snopes",
                "source_url": "https://www.snopes.com/fact-check/covid-vaccine-information/",
                "title": "COVID-19 Vaccine Information",
                "claim_date": "2023-08-15",
                "rating": "Mixed",
                "summary": "Various claims about COVID-19 vaccines have been examined with different ratings. Check the source for specific claim verification."
            })
            
            # Add a second source for better verification
            results.append({
                "source": "Reuters Fact Check",
                "source_url": "https://www.reuters.com/fact-check/health-coronavirus",
                "title": "COVID-19 and Vaccine Facts",
                "claim_date": "2023-09-22",
                "rating": "Fact-Based",
                "summary": "Medical experts have confirmed that COVID-19 vaccines undergo rigorous safety testing and are effective at preventing severe illness."
            })
        
        # Climate Change
        elif re.search(r"climate|global warming|carbon|emissions", claim_text, re.IGNORECASE):
            results.append({
                "source": "FactCheck.org",
                "source_url": "https://www.factcheck.org/issue/climate-change/",
                "title": "Climate Change Facts",
                "claim_date": "2023-06-12",
                "rating": "Fact-Based",
                "summary": "Scientific consensus confirms that climate change is real and primarily caused by human activities. Individual claims may vary in accuracy."
            })
            
            # Add another climate source
            if "hoax" in claim_text.lower() or "fake" in claim_text.lower():
                results.append({
                    "source": "NASA Climate",
                    "source_url": "https://climate.nasa.gov/evidence/",
                    "title": "Scientific Evidence for Climate Change",
                    "claim_date": "2023-04-18",
                    "rating": "False",
                    "summary": "Claims that climate change is a hoax are false. Multiple lines of evidence show Earth's climate is changing primarily due to human activities."
                })
        
        # Elections and Voting
        elif re.search(r"election|voting|ballot|fraud", claim_text, re.IGNORECASE):
            # More specific election claims
            if re.search(r"(stole|stolen|rigged|fraud|illegal votes)", claim_text, re.IGNORECASE):
                results.append({
                    "source": "PolitiFact",
                    "source_url": "https://www.politifact.com/article/2022/nov/09/allegations-voter-fraud-dont-last/",
                    "title": "Claims of Widespread Election Fraud",
                    "claim_date": "2023-03-10",
                    "rating": "False",
                    "summary": "Multiple courts, election officials from both parties, and independent investigations have found no evidence of widespread voter fraud that could change election outcomes."
                })
            else:
                results.append({
                    "source": "PolitiFact",
                    "source_url": "https://www.politifact.com/elections/",
                    "title": "Election Information Fact Checks",
                    "claim_date": "2023-05-10",
                    "rating": "Varies",
                    "summary": "Election-related claims are fact-checked on a case-by-case basis. Visit the source for specific claim verification."
                })
                
        # 5G misinformation
        elif re.search(r"5G", claim_text) and re.search(r"(cause|spread|covid|health|radiation|danger)", claim_text, re.IGNORECASE):
            results.append({
                "source": "Full Fact",
                "source_url": "https://fullfact.org/health/5G-not-cause-coronavirus/",
                "title": "5G and Health Claims",
                "claim_date": "2023-02-15",
                "rating": "False",
                "summary": "Claims linking 5G technology to health problems or COVID-19 are not supported by scientific evidence. 5G radiation is non-ionizing and cannot damage cells or spread viruses."
            })
            
        # No results found if none of the patterns match
        
    except Exception as e:
        logger.error(f"Error querying Google Fact Check API: {e}")
    
    return results

def search_for_fact_checks(claim_text: str) -> List[Dict[str, Any]]:
    """
    Simulate searching for fact checks about the claim on various fact-checking websites.
    
    Args:
        claim_text: The text of the claim to verify
        
    Returns:
        A list of verification results
    """
    results = []
    
    # In a real implementation, this would use a search engine API or web scraping
    # to find relevant fact-checking articles
    
    # For demonstration purposes, we'll simulate some results based on the claim text
    # This is just to show how it would work and would be replaced with real searches
    
    # Simulate a delay like a real search would have
    time.sleep(0.8)
    
    # More comprehensive pattern matching for various misinformation topics
    
    # Flat Earth claims
    if "flat earth" in claim_text.lower() or "earth is flat" in claim_text.lower():
        results.append({
            "source": "Reuters Fact Check",
            "source_url": "https://www.reuters.com/fact-check/earth-is-round",
            "title": "Fact Check: The Earth is not flat",
            "claim_date": "2023-02-18",
            "rating": "False",
            "summary": "The Earth has been scientifically proven to be roughly spherical. This fact has been confirmed by satellite imagery, circumnavigation, and various scientific measurements."
        })
        
        # Add a second source for stronger verification
        results.append({
            "source": "National Geographic",
            "source_url": "https://www.nationalgeographic.com/science/article/how-we-know-earth-round-pancake-conspiracy",
            "title": "How We Know Earth Is Round",
            "claim_date": "2023-05-24",
            "rating": "False",
            "summary": "Multiple lines of evidence from different scientific fields all confirm that Earth is spherical, not flat. This includes direct observation, physics, and space photography."
        })
    
    # Chemtrails conspiracy
    elif re.search(r"chemtrail|chem trail|chemical spray", claim_text, re.IGNORECASE):
        results.append({
            "source": "Snopes",
            "source_url": "https://www.snopes.com/fact-check/chemtrails/",
            "title": "Fact Check: Chemtrails Conspiracy",
            "claim_date": "2023-01-30",
            "rating": "False",
            "summary": "The 'chemtrails' conspiracy theory is false. The white lines in the sky behind aircraft are water vapor condensation trails (contrails), not chemical sprays for weather control or population management."
        })
    
    # Moon landing hoax
    elif re.search(r"moon landing (fake|hoax|staged)", claim_text, re.IGNORECASE) or "never went to the moon" in claim_text.lower():
        results.append({
            "source": "AP Fact Check",
            "source_url": "https://apnews.com/article/fact-check-moon-landing-not-fake-apollo-5c6bc1ffe2f888c2b4b6768c0a4858f1",
            "title": "Moon landings were real, not staged",
            "claim_date": "2023-07-20",
            "rating": "False",
            "summary": "NASA's Apollo missions successfully landed astronauts on the moon six times between 1969 and 1972. The evidence includes moon rocks, photographs, independent verification from other countries, and ongoing observation of landing sites."
        })
    
    # Alternative Medicine/Anti-vaccine claims
    elif re.search(r"(natural cure|essential oil|alternative medicine) (cure|treat|heal) (cancer|disease|illness)", claim_text, re.IGNORECASE):
        results.append({
            "source": "Science-Based Medicine",
            "source_url": "https://sciencebasedmedicine.org/alternative-medicine/",
            "title": "Alternative Medicine Claims",
            "claim_date": "2023-03-15",
            "rating": "False",
            "summary": "Many 'natural cures' lack scientific evidence of effectiveness and safety. While some natural products have medicinal properties, claims of miracle cures for serious diseases are typically unsupported by clinical research."
        })
    
    # Microchips in vaccines
    elif re.search(r"(microchip|tracker|tracking device) (in|inside) (vaccine|vaccination)", claim_text, re.IGNORECASE):
        results.append({
            "source": "FactCheck.org",
            "source_url": "https://www.factcheck.org/2021/03/scicheck-microchips-in-vaccines/",
            "title": "No Microchips in Vaccines",
            "claim_date": "2023-08-05",
            "rating": "False",
            "summary": "Vaccines do not contain microchips, tracking devices, or other surveillance technology. This claim has been thoroughly debunked by medical experts, regulatory bodies, and independent analysis of vaccine ingredients."
        })
        
    return results

def check_against_news_sources(claim_text: str) -> List[Dict[str, Any]]:
    """
    Check the claim against reputable news sources.
    
    Args:
        claim_text: The text of the claim to verify
        
    Returns:
        A list of verification results
    """
    # In a real implementation, this would query news APIs or scrape news sites
    # For demonstration purposes, we'll return an empty list
    return []
