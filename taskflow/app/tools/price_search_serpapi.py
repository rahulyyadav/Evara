"""
Product price search implementation using SerpAPI.
This is extracted as a separate method for the price tracker.
"""
import logging
import asyncio
import json
from typing import Optional, Dict, Any, List

logger = logging.getLogger("taskflow")

try:
    from serpapi import GoogleSearch
    SERPAPI_AVAILABLE = True
except ImportError:
    SERPAPI_AVAILABLE = False
    GoogleSearch = None

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None


async def search_product_price_with_serpapi(
    product_name: str,
    serpapi_key: str,
    gemini_model: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Search for product price using SerpAPI Google Shopping.
    
    Args:
        product_name: Product name to search
        serpapi_key: SerpAPI key
        gemini_model: Optional Gemini model for price extraction
        
    Returns:
        Dictionary with product price information
    """
    if not SERPAPI_AVAILABLE:
        return {
            "success": False,
            "message": "SerpAPI is not available. Please install: pip install google-search-results"
        }
    
    try:
        logger.info(f"🔍 Searching SerpAPI for: {product_name}")
        
        # Use Google Shopping search for better price results
        params = {
            "engine": "google_shopping",
            "q": product_name,
            "api_key": serpapi_key,
            "location": "India",  # Set to India for rupee prices
            "hl": "en",
            "gl": "in",
            "num": 5  # Get top 5 results for better accuracy
        }
        
        # Run search in thread pool (SerpAPI is synchronous)
        loop = asyncio.get_event_loop()
        search = await loop.run_in_executor(None, lambda: GoogleSearch(params))
        results = await loop.run_in_executor(None, search.get_dict)
        
        logger.debug(f"SerpAPI raw results: {json.dumps(results, indent=2)[:500]}")
        
        # Extract shopping results
        shopping_results = results.get("shopping_results", [])
        
        if not shopping_results:
            return {
                "success": False,
                "message": f"No products found for '{product_name}'. Try being more specific (e.g., include brand, model, or specs)."
            }
        
        # Get the best matching product (first result is usually most relevant)
        best_match = shopping_results[0]
        
        # Extract price
        price_str = best_match.get("price", "")
        extracted_price = best_match.get("extracted_price")
        
        # Try to get numeric price
        price = None
        if extracted_price:
            price = float(extracted_price)
        elif price_str:
            # Parse price from string (e.g., "₹50,000", "$500", "50000")
            price = parse_price_from_string(price_str)
        
        if not price:
            # Try using Gemini to extract price if available
            if gemini_model:
                price = await extract_price_with_gemini(best_match, gemini_model)
        
        if not price:
            return {
                "success": False,
                "message": f"Found '{best_match.get('title', product_name)}' but couldn't extract the price. Try a different product or be more specific."
            }
        
        # Build result
        result = {
            "success": True,
            "title": best_match.get("title", product_name),
            "price": price,
            "url": best_match.get("link", ""),
            "source": best_match.get("source", "Google Shopping"),
            "thumbnail": best_match.get("thumbnail", ""),
            "rating": best_match.get("rating"),
            "reviews": best_match.get("reviews"),
            "delivery": best_match.get("delivery", ""),
        }
        
        logger.info(f"✅ Found product: {result['title']} - ₹{price:,.2f}")
        return result
        
    except Exception as e:
        logger.error(f"Error searching product with SerpAPI: {e}", exc_info=True)
        return {
            "success": False,
            "message": f"Error searching for product: {str(e)}"
        }


def parse_price_from_string(price_str: str) -> Optional[float]:
    """
    Parse price from various string formats.
    
    Examples:
        "₹50,000" -> 50000.0
        "$500.99" -> 500.99
        "50000" -> 50000.0
        "Rs. 1,50,000" -> 150000.0
    """
    import re
    
    try:
        # Remove currency symbols and text
        price_str = price_str.replace('₹', '').replace('$', '').replace('Rs', '').replace('INR', '')
        price_str = price_str.replace(',', '').strip()
        
        # Extract first number found
        match = re.search(r'(\d+\.?\d*)', price_str)
        if match:
            return float(match.group(1))
        
        return None
    except:
        return None


async def extract_price_with_gemini(product_data: Dict[str, Any], gemini_model: Any) -> Optional[float]:
    """
    Use Gemini to extract price from product data when standard parsing fails.
    
    Args:
        product_data: Product data dictionary from SerpAPI
        gemini_model: Gemini model instance
        
    Returns:
        Extracted price or None
    """
    try:
        prompt = f"""Extract the price from this product data. Return ONLY the numeric price value (without currency symbols or commas).

Product data:
{json.dumps(product_data, indent=2)}

Instructions:
- Look for price, extracted_price, or any price-related fields
- Convert to a single numeric value (e.g., "₹50,000" -> 50000)
- If you find the price, respond with ONLY the number (e.g., "50000" or "50000.99")
- If no price found, respond with "null"

Your response (numeric price only):"""
        
        response = await asyncio.to_thread(gemini_model.generate_content, prompt)
        
        if response and response.text:
            result = response.text.strip()
            
            # Try to parse as float
            try:
                if result.lower() == "null":
                    return None
                # Remove any remaining non-numeric characters except decimal point
                import re
                numeric_str = re.sub(r'[^\d.]', '', result)
                return float(numeric_str)
            except:
                return None
        
        return None
        
    except Exception as e:
        logger.debug(f"Gemini price extraction failed: {e}")
        return None

