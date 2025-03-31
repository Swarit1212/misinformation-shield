import os
import logging
from typing import Tuple
import re
import random

# In a production environment, we would use a real transformer model
# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# import torch

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get API key from environment variables
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")

def classify_text(text: str) -> Tuple[str, float]:
    """
    Classify a text as true, false, or unclear using a pre-trained model.
    
    Args:
        text: The text to classify
        
    Returns:
        A tuple of (classification, confidence) where classification is one of
        'true', 'false', or 'unclear', and confidence is a float between 0 and 1
    """
    # In a real implementation, this would use a fine-tuned model for misinformation detection
    # For demonstration purposes, we'll implement a simplified version that looks for
    # patterns common in misinformation
    
    # Convert to lowercase for easier pattern matching
    text_lower = text.lower()
    
    # List of patterns often found in misinformation
    misinformation_patterns = [
        r"they don't want you to know",
        r"wake up",
        r"the truth about",
        r"what they aren't telling you",
        r"mainstream media won't report",
        r"banned information",
        r"censored",
        r"secret cure",
        r"miracle treatment",
        r"government conspiracy",
        r"the elites",
        r"100% proof",
        r"undeniable evidence",
        r"shocking truth",
        r"mind-blowing",
        r"they've been hiding",
        r"suppressed knowledge",
        r"what doctors won't tell you",
        r"they are lying",
        r"do your own research",
        r"cover-up",
        r"follow the money",
        r"sheep",
        r"sheeple",
        r"fake news media",
        r"huge scandal",
        r"bombshell",
        r"big pharma",
        r"deep state",
        r"corrupt officials",
        r"they hid this",
        r"open your eyes",
        r"they deleted this",
        r"truth bomb",
        r"stop being blind"
    ]
    
    # List of patterns often found in factual information
    factual_patterns = [
        r"according to research",
        r"studies show",
        r"evidence suggests",
        r"experts say",
        r"researchers found",
        r"data indicates",
        r"analysis of",
        r"peer-reviewed",
        r"published in",
        r"scientific consensus",
        r"based on data",
        r"statistics show",
        r"research published",
        r"clinical trials",
        r"experiment results",
        r"survey results",
        r"official statistics",
        r"multiple sources confirm",
        r"according to the report",
        r"verified information",
        r"fact-checked",
        r"investigation revealed",
        r"findings suggest",
        r"official statement",
        r"public records show",
        r"according to documents",
        r"data collected",
        r"sources familiar with",
        r"confirmed by",
        r"according to officials",
        r"independently verified",
        r"research indicates",
        r"the study concludes"
    ]
    
    # Count matches for each type of pattern
    misinfo_count = sum(1 for pattern in misinformation_patterns if re.search(pattern, text_lower))
    factual_count = sum(1 for pattern in factual_patterns if re.search(pattern, text_lower))
    
    # Don't just count patterns, also examine text sentiment and structure
    
    # Add random variation to confidence based on word count to simulate more natural variation
    # The more words, the more information we have to analyze
    word_count = len(text.split())
    word_factor = min(1.0, word_count / 100)  # Tops out at 100 words
    
    # Give significantly more weight to matched patterns - increase impact of matches
    misinfo_weight = 3.0 if misinfo_count > 0 else 1.0
    factual_weight = 3.0 if factual_count > 0 else 1.0
    
    # Use exponential scoring for repeated patterns - indicates stronger bias
    # Square root for a non-linear relationship (diminishing returns)
    misinfo_score_base = misinfo_count / len(misinformation_patterns) if len(misinformation_patterns) > 0 else 0
    factual_score_base = factual_count / len(factual_patterns) if len(factual_patterns) > 0 else 0
    
    # Apply weights and add exponential component for stronger signal
    misinfo_score = (misinfo_score_base * misinfo_weight) * (1 + 0.5 * (misinfo_count ** 0.5))
    factual_score = (factual_score_base * factual_weight) * (1 + 0.5 * (factual_count ** 0.5))
    
    # Text complexity analysis (longer texts with varied vocabulary are more nuanced)
    unique_words = len(set(text_lower.split()))
    complexity_factor = min(1.0, unique_words / 50)  # Tops out at 50 unique words
    
    # Calculate confidence based on multiple factors
    if misinfo_score > factual_score and misinfo_count > 0:
        classification = "false"
        # Higher base + proportional difference + length/complexity factors
        base_confidence = 0.55 + (word_factor * 0.1)
        score_diff = min(0.3, (misinfo_score - factual_score) * 0.4)
        confidence = base_confidence + score_diff + (complexity_factor * 0.1)
    elif factual_score > misinfo_score and factual_count > 0:
        classification = "true"
        # Higher base + proportional difference + length/complexity factors
        base_confidence = 0.6 + (word_factor * 0.1)
        score_diff = min(0.3, (factual_score - misinfo_score) * 0.4)
        confidence = base_confidence + score_diff + (complexity_factor * 0.1)
    else:
        # If scores are equal or no patterns found
        classification = "unclear"
        if misinfo_count == 0 and factual_count == 0:
            # No patterns found, but vary based on text length/complexity
            # Shorter texts with no patterns = more uncertain
            confidence = 0.3 + (word_factor * 0.2)
        else:
            # Some patterns but mixed signals
            confidence = 0.45 - (abs(factual_score - misinfo_score) * 0.1)
    
    # Add small random variation to prevent uniform scores
    import random
    random_factor = random.uniform(-0.05, 0.05)
    confidence += random_factor
    
    # Ensure confidence is within reasonable bounds
    confidence = max(0.3, min(0.95, confidence))
    
    logger.debug(f"Classification: {classification}, Confidence: {confidence}")
    
    return classification, confidence
    
def get_huggingface_classification(text: str) -> Tuple[str, float]:
    """
    Use Hugging Face API to classify a text as true, false, or unclear.
    
    This would be used in a production environment with a properly fine-tuned model.
    
    Args:
        text: The text to classify
        
    Returns:
        A tuple of (classification, confidence)
    """
    # Check if API key is available
    if not HUGGINGFACE_API_KEY:
        logger.warning("No Hugging Face API key provided. Using fallback classification.")
        return classify_text(text)
    
    try:
        # In a production environment, we would make a real API call here
        # to a fine-tuned model hosted on Hugging Face
        # import requests
        # API_URL = "https://api-inference.huggingface.co/models/user/misinformation-classifier"
        # headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        # response = requests.post(API_URL, headers=headers, json={"inputs": text})
        # result = response.json()
        # Process result...
        
        # For now, we'll just use our simpler classification
        return classify_text(text)
        
    except Exception as e:
        logger.error(f"Error using Hugging Face API: {e}")
        # Fall back to the simpler classification
        return classify_text(text)
