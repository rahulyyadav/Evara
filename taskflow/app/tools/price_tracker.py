"""
Price tracking tool for TaskFlow.
Uses Google Shopping API (via SerpAPI) for product price search.
Falls back to web scraping if API is not available.
"""
import asyncio
import logging
import re
import uuid
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from urllib.parse import urlparse, quote

try:
    from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeoutError
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Browser = None
    Page = None
    PlaywrightTimeoutError = None

try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False
    BeautifulSoup = None

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

try:
    from serpapi import GoogleSearch
    SERPAPI_AVAILABLE = True
except ImportError:
    SERPAPI_AVAILABLE = False
    GoogleSearch = None

import httpx

from ..config import settings
from ..memory import MemoryStore

logger = logging.getLogger("taskflow")


class PriceTrackerTool:
    """Tool for tracking product prices using web scraping."""
    
    def __init__(self, memory_store: Optional[MemoryStore] = None):
        """
        Initialize the price tracker tool.
        
        Args:
            memory_store: MemoryStore instance for persisting tracked products
        """
        self.memory_store = memory_store or MemoryStore()
        self.browser: Optional[Browser] = None
        self._playwright = None
        
        if not PLAYWRIGHT_AVAILABLE and not BEAUTIFULSOUP_AVAILABLE:
            logger.warning("Neither Playwright nor BeautifulSoup installed - price tracking will not work")
        elif not PLAYWRIGHT_AVAILABLE:
            logger.info("Playwright not installed - will try BeautifulSoup (limited functionality)")
        elif not BEAUTIFULSOUP_AVAILABLE:
            logger.info("BeautifulSoup not installed - will use Playwright only")
    
    async def _ensure_browser(self) -> Browser:
        """Ensure browser is initialized."""
        if not PLAYWRIGHT_AVAILABLE:
            raise Exception("Playwright is not installed. Please install it with: pip install playwright && playwright install")
        
        if self.browser is None:
            self._playwright = await async_playwright().start()
            self.browser = await self._playwright.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            logger.debug("Browser initialized for price tracking")
        
        return self.browser
    
    async def track_product(
        self,
        user_number: str,
        url: Optional[str] = None,
        product_name: Optional[str] = None,
        target_price: Optional[float] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Track a product's price.
        
        Args:
            user_number: User's phone number
            url: Product URL (preferred)
            product_name: Product name for search (if URL not provided)
            target_price: Target price for alerts
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with tracking status or error message
        """
        logger.info(f"📦 Price tracking requested: {product_name or url}")
        
        if not PLAYWRIGHT_AVAILABLE and not BEAUTIFULSOUP_AVAILABLE:
            return {
                "success": False,
                "message": "Price tracking requires either Playwright or BeautifulSoup. Please install one: 'pip install playwright beautifulsoup4'",
                "tool": "price_tracker"
            }
        
        try:
            # If URL provided, use it directly
            if url:
                if not self._is_valid_url(url):
                    return {
                        "success": False,
                        "message": "I couldn't access that page. Check the URL?",
                        "tool": "price_tracker"
                    }
                
                if not self._is_amazon_url(url):
                    return {
                        "success": False,
                        "message": "Currently only Amazon.in is supported. Flipkart support coming soon! 📦",
                        "tool": "price_tracker"
                    }
                
                product_data = await self._scrape_product(url)
                if not product_data:
                    return {
                        "success": False,
                        "message": "I couldn't scrape that product. Please check the URL or try again later.",
                        "tool": "price_tracker"
                    }
            
            # If product name provided, search using Google Shopping API
            elif product_name:
                # First try SerpAPI Google Shopping search (fastest and most reliable)
                product_data = await self._search_product_with_serpapi(product_name)
                
                # If SerpAPI fails, fall back to web scraping
                if not product_data:
                    logger.info("SerpAPI search failed, falling back to Amazon scraping")
                    product_data = await self._search_and_get_product(product_name)
                
                if not product_data:
                    return {
                        "success": False,
                        "message": f"❌ Couldn't find '{product_name}' on shopping sites. Please check the product name and try again.",
                        "tool": "price_tracker"
                    }
            
            else:
                return {
                    "success": False,
                    "needs_clarification": True,
                    "message": "I need either a product URL or product name to track. Which one do you have?",
                    "tool": "price_tracker"
                }
            
            # Generate product ID
            product_id = str(uuid.uuid4())
            product_data["id"] = product_id
            product_data["target_price"] = target_price
            product_data["url"] = product_data.get("url", url)
            
            # Save to memory
            self.memory_store.add_tracked_product(user_number, product_data)
            
            # Format response
            price_str = f"₹{product_data.get('current_price', 0):,.0f}" if product_data.get('current_price') else "N/A"
            target_str = f"₹{target_price:,.0f}" if target_price else "not set"
            
            response = (
                f"📦 Tracking: {product_data.get('title', 'Product')}\n"
                f"💰 Current: {price_str}\n"
            )
            
            if target_price:
                response += f"📉 I'll alert you if price drops below {target_str}\n"
            
            tracked_count = len(self.memory_store.get_tracked_products(user_number))
            response += f"\nYou're tracking {tracked_count} item(s) total."
            
            return {
                "success": True,
                "message": response,
                "product_id": product_id,
                "tool": "price_tracker"
            }
            
        except Exception as e:
            logger.error(f"Error tracking product: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"Sorry, I encountered an error: {str(e)}",
                "tool": "price_tracker"
            }
    
    async def get_tracked_items(self, user_number: str) -> Dict[str, Any]:
        """
        Get all tracked items for a user.
        
        Args:
            user_number: User's phone number
            
        Returns:
            Dictionary with tracked items
        """
        logger.info(f"Getting tracked items for {user_number}")
        
        try:
            items = self.memory_store.get_tracked_products(user_number)
            
            if not items:
                return {
                    "success": True,
                    "items": [],
                    "message": "You're not tracking any items yet. Send me a product URL or name to start tracking!",
                    "tool": "price_tracker"
                }
            
            # Format items for display
            formatted_items = []
            for item in items:
                price_str = f"₹{item.get('current_price', 0):,.0f}" if item.get('current_price') else "N/A"
                formatted_items.append({
                    "id": item.get("id"),
                    "title": item.get("title", "Unknown"),
                    "price": price_str,
                    "url": item.get("url", ""),
                    "target_price": item.get("target_price"),
                    "tracked_since": item.get("tracked_since", "")
                })
            
            # Build response message
            message = f"📦 You're tracking {len(items)} item(s):\n\n"
            for i, item in enumerate(formatted_items, 1):
                message += f"{i}. {item['title']}\n"
                message += f"   💰 {item['price']}\n"
                if item.get('target_price'):
                    message += f"   📉 Alert if below ₹{item['target_price']:,.0f}\n"
                message += "\n"
            
            return {
                "success": True,
                "items": formatted_items,
                "message": message.strip(),
                "tool": "price_tracker"
            }
            
        except Exception as e:
            logger.error(f"Error getting tracked items: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"Error retrieving tracked items: {str(e)}",
                "tool": "price_tracker"
            }
    
    async def stop_tracking(self, user_number: str, product_id: Optional[str] = None, product_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Stop tracking a product.
        
        Args:
            user_number: User's phone number
            product_id: Product ID to stop tracking
            product_name: Product name to stop tracking (if ID not provided)
            
        Returns:
            Dictionary with removal status
        """
        logger.info(f"Stop tracking requested for {user_number}: {product_id or product_name}")
        
        try:
            items = self.memory_store.get_tracked_products(user_number)
            
            if not items:
                return {
                    "success": False,
                    "message": "You're not tracking any items.",
                    "tool": "price_tracker"
                }
            
            # Find product to remove
            product_to_remove = None
            
            if product_id:
                product_to_remove = next((item for item in items if item.get("id") == product_id), None)
            elif product_name:
                # Try to find by name (case-insensitive partial match)
                product_name_lower = product_name.lower()
                for item in items:
                    if product_name_lower in item.get("title", "").lower():
                        product_to_remove = item
                        break
            
            if not product_to_remove:
                return {
                    "success": False,
                    "message": "Couldn't find that product in your tracked items. Use 'check tracked items' to see what you're tracking.",
                    "tool": "price_tracker"
                }
            
            # Remove product
            removed = self.memory_store.remove_tracked_product(user_number, product_to_remove.get("id"))
            
            if removed:
                return {
                    "success": True,
                    "message": f"✅ Stopped tracking: {product_to_remove.get('title', 'Product')}\n\nYou're now tracking {len(items) - 1} item(s).",
                    "tool": "price_tracker"
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to remove product. Please try again.",
                    "tool": "price_tracker"
                }
                
        except Exception as e:
            logger.error(f"Error stopping tracking: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "tool": "price_tracker"
            }
    
    async def check_prices(self, user_number: Optional[str] = None) -> Dict[str, Any]:
        """
        Check prices for all tracked items (or for a specific user).
        
        Args:
            user_number: Optional user number to check prices for
            
        Returns:
            Dictionary with price check results
        """
        logger.info(f"Checking prices for tracked items")
        
        if not PLAYWRIGHT_AVAILABLE:
            return {
                "success": False,
                "message": "Playwright not available for price checking.",
                "tool": "price_tracker"
            }
        
        try:
            # Get all tracked items (or for specific user)
            if user_number:
                items = self.memory_store.get_tracked_products(user_number)
            else:
                # Get all users' tracked items (for background job)
                all_items = []
                # This would require iterating through all users - simplified for now
                items = []
            
            if not items:
                return {
                    "success": True,
                    "message": "No items to check.",
                    "tool": "price_tracker"
                }
            
            # Check prices for each item
            updates = []
            for item in items:
                try:
                    url = item.get("url")
                    if not url:
                        continue
                    
                    product_data = await self._scrape_product(url)
                    if product_data and product_data.get("current_price"):
                        old_price = item.get("current_price", 0)
                        new_price = product_data.get("current_price", 0)
                        
                        # Update in memory
                        self.memory_store.update_tracked_product(
                            user_number or item.get("user_number", ""),
                            item.get("id"),
                            {
                                "current_price": new_price,
                                "last_checked": datetime.now().isoformat()
                            }
                        )
                        
                        updates.append({
                            "product": item.get("title"),
                            "old_price": old_price,
                            "new_price": new_price,
                            "dropped": new_price < old_price if old_price else False
                        })
                        
                except Exception as e:
                    logger.warning(f"Error checking price for {item.get('title')}: {e}")
                    continue
            
            return {
                "success": True,
                "updates": updates,
                "message": f"Checked {len(items)} item(s). {len(updates)} updated.",
                "tool": "price_tracker"
            }
            
        except Exception as e:
            logger.error(f"Error checking prices: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"Error checking prices: {str(e)}",
                "tool": "price_tracker"
            }
    
    async def _search_product_with_serpapi(self, product_name: str) -> Optional[Dict[str, Any]]:
        """
        Search for product using Google Shopping via SerpAPI.
        
        Args:
            product_name: Product name to search
            
        Returns:
            Product data dictionary with title, price, url, etc. or None
        """
        if not SERPAPI_AVAILABLE:
            logger.debug("SerpAPI not available")
            return None
        
        if not settings.SERPAPI_KEY:
            logger.debug("SERPAPI_KEY not configured")
            return None
        
        try:
            logger.info(f"🔍 Searching Google Shopping for: {product_name}")
            
            # Search Google Shopping
            search = GoogleSearch({
                "q": product_name,
                "engine": "google_shopping",
                "api_key": settings.SERPAPI_KEY,
                "gl": "in",  # India
                "hl": "en"
            })
            
            results = search.get_dict()
            shopping_results = results.get("shopping_results", [])
            
            if not shopping_results:
                logger.warning(f"No shopping results found for: {product_name}")
                return None
            
            # Get top 5 results
            top_results = shopping_results[:5]
            
            # Use Gemini to select the best match if available
            if self.gemini_model and len(top_results) > 1:
                selected_result = await self._select_best_product_with_gemini(product_name, top_results)
                if selected_result:
                    return self._format_serpapi_result(selected_result)
            
            # Otherwise, use the first result
            best_result = top_results[0]
            return self._format_serpapi_result(best_result)
            
        except Exception as e:
            logger.error(f"Error searching with SerpAPI: {e}", exc_info=True)
            return None
    
    def _format_serpapi_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Format SerpAPI result into standardized product data."""
        try:
            # Extract price
            price_str = result.get("extracted_price") or result.get("price", "0")
            try:
                if isinstance(price_str, (int, float)):
                    price = float(price_str)
                else:
                    # Remove currency symbols and commas
                    price = float(re.sub(r'[^\d.]', '', str(price_str)))
            except:
                price = 0.0
            
            return {
                "title": result.get("title", "Unknown Product"),
                "current_price": price,
                "url": result.get("link", ""),
                "source": result.get("source", "Google Shopping"),
                "rating": result.get("rating"),
                "reviews": result.get("reviews"),
                "thumbnail": result.get("thumbnail"),
                "tracked_since": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error formatting SerpAPI result: {e}")
            return None
    
    async def _select_best_product_with_gemini(
        self,
        query: str,
        results: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Use Gemini to intelligently select the best matching product."""
        try:
            # Prepare results for Gemini
            results_text = []
            for i, result in enumerate(results):
                title = result.get("title", "Unknown")
                price = result.get("extracted_price") or result.get("price", "N/A")
                source = result.get("source", "Unknown")
                rating = result.get("rating", "N/A")
                results_text.append(f"{i+1}. {title}\n   Price: {price}\n   Source: {source}\n   Rating: {rating}")
            
            prompt = f"""User is searching for: "{query}"

Here are the top product results:

{chr(10).join(results_text)}

Which result is the BEST match for what the user is looking for?
Consider:
1. Product name relevance to search query
2. Price reasonableness
3. Source reliability
4. Ratings if available

Respond with ONLY the number (1-{len(results)}) of the best match. Just the number, nothing else."""

            response = self.gemini_model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract number
            match = re.search(r'(\d+)', response_text)
            if match:
                index = int(match.group(1)) - 1
                if 0 <= index < len(results):
                    logger.info(f"Gemini selected result #{index+1} for '{query}'")
                    return results[index]
            
            # Fallback to first result
            return results[0]
            
        except Exception as e:
            logger.error(f"Error in Gemini product selection: {e}")
            return results[0] if results else None
    
    async def _search_and_get_product(self, product_name: str) -> Optional[Dict[str, Any]]:
        """
        Search for a product on Amazon and get the first result.
        
        Args:
            product_name: Product name to search for
            
        Returns:
            Product data dictionary or None
        """
        try:
            browser = await self._ensure_browser()
            page = await browser.new_page()
            
            # Search on Amazon.in
            search_url = f"https://www.amazon.in/s?k={quote(product_name)}"
            logger.debug(f"Searching Amazon: {search_url}")
            
            await page.goto(search_url, wait_until="networkidle", timeout=30000)
            
            # Wait for search results
            try:
                await page.wait_for_selector('[data-component-type="s-search-result"]', timeout=10000)
            except PlaywrightTimeoutError:
                logger.warning("Search results not found")
                await page.close()
                return None
            
            # Get first product link
            first_product = await page.query_selector('[data-component-type="s-search-result"] a.a-link-normal')
            if not first_product:
                await page.close()
                return None
            
            product_url = await first_product.get_attribute("href")
            if product_url and not product_url.startswith("http"):
                product_url = f"https://www.amazon.in{product_url}"
            
            await page.close()
            
            # Scrape the product page
            if product_url:
                return await self._scrape_product(product_url)
            
            return None
            
        except Exception as e:
            logger.error(f"Error searching product: {e}", exc_info=True)
            return None
    
    async def _scrape_product(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape product information from Amazon.in.
        Tries BeautifulSoup first (lighter, no browser needed), falls back to Playwright if needed.
        
        Args:
            url: Product URL
            
        Returns:
            Product data dictionary or None
        """
        if not self._is_amazon_url(url):
            logger.warning(f"Non-Amazon URL provided: {url}")
            return None
        
        # Try BeautifulSoup first (lighter, no browser needed)
        if BEAUTIFULSOUP_AVAILABLE:
            result = await self._scrape_with_beautifulsoup(url)
            if result:
                logger.debug("✅ Successfully scraped with BeautifulSoup")
                return result
            else:
                logger.debug("⚠️ BeautifulSoup failed, trying Playwright...")
        
        # Fall back to Playwright if BeautifulSoup failed or not available
        if PLAYWRIGHT_AVAILABLE:
            return await self._scrape_with_playwright(url)
        
        # Neither method available
        return None
    
    async def _scrape_with_beautifulsoup(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape product using BeautifulSoup (lighter, no browser needed).
        Works for static HTML content.
        
        Args:
            url: Product URL
            
        Returns:
            Product data dictionary or None
        """
        if not BEAUTIFULSOUP_AVAILABLE:
            return None
        
        try:
            logger.debug(f"Trying BeautifulSoup for: {url}")
            
            # Fetch page with httpx
            async with httpx.AsyncClient(timeout=15.0) as client:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5"
                }
                response = await client.get(url, headers=headers, follow_redirects=True)
                response.raise_for_status()
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(response.text, 'lxml')
                
                # Extract price (try multiple selectors)
                price = None
                price_selectors = [
                    '#priceblock_dealprice',
                    '#priceblock_ourprice',
                    '.a-price-whole',
                    '.a-price .a-offscreen',
                    '[data-a-color="price"] .a-offscreen',
                    '#priceblock_saleprice'
                ]
                
                for selector in price_selectors:
                    element = soup.select_one(selector)
                    if element:
                        price_text = element.get_text(strip=True)
                        price = self._parse_price(price_text)
                        if price:
                            break
                
                # Extract title
                title = None
                title_selectors = [
                    '#productTitle',
                    'h1.a-size-large',
                    'span#productTitle'
                ]
                
                for selector in title_selectors:
                    element = soup.select_one(selector)
                    if element:
                        title = element.get_text(strip=True)
                        if title:
                            break
                
                # Extract image
                image_url = None
                image_element = soup.select_one('#landingImage, #imgBlkFront')
                if image_element:
                    image_url = image_element.get('src') or image_element.get('data-src')
                
                # Check if we got essential data
                if not price and not title:
                    # BeautifulSoup might not work if content is loaded via JavaScript
                    logger.debug("BeautifulSoup couldn't extract data (likely JavaScript-rendered content)")
                    return None
                
                return {
                    "title": title or "Unknown Product",
                    "current_price": price,
                    "url": url,
                    "image_url": image_url,
                    "site": "amazon.in",
                    "last_checked": datetime.now().isoformat(),
                    "method": "beautifulsoup"
                }
                
        except Exception as e:
            logger.debug(f"BeautifulSoup scraping failed: {e}")
            return None
    
    async def _scrape_with_playwright(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape product using Playwright (handles JavaScript-rendered content).
        
        Args:
            url: Product URL
            
        Returns:
            Product data dictionary or None
        """
        if not PLAYWRIGHT_AVAILABLE:
            return None
        
        try:
            browser = await self._ensure_browser()
            page = await browser.new_page()
            
            # Set user agent to avoid blocking
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            })
            
            logger.debug(f"Scraping product with Playwright: {url}")
            await page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Wait for price element (multiple possible selectors)
            price = None
            title = None
            image_url = None
            
            try:
                # Try different price selectors (Amazon has multiple)
                price_selectors = [
                    '.a-price-whole',
                    '#priceblock_dealprice',
                    '#priceblock_ourprice',
                    '.a-price .a-offscreen',
                    '[data-a-color="price"] .a-offscreen'
                ]
                
                for selector in price_selectors:
                    try:
                        price_element = await page.wait_for_selector(selector, timeout=5000)
                        if price_element:
                            price_text = await price_element.inner_text()
                            price = self._parse_price(price_text)
                            if price:
                                break
                    except PlaywrightTimeoutError:
                        continue
                
                # Get title
                title_selectors = [
                    '#productTitle',
                    'h1.a-size-large',
                    'span#productTitle'
                ]
                
                for selector in title_selectors:
                    try:
                        title_element = await page.wait_for_selector(selector, timeout=5000)
                        if title_element:
                            title = await title_element.inner_text()
                            title = title.strip()
                            if title:
                                break
                    except PlaywrightTimeoutError:
                        continue
                
                # Get image
                try:
                    image_element = await page.query_selector('#landingImage, #imgBlkFront')
                    if image_element:
                        image_url = await image_element.get_attribute("src")
                except:
                    pass
                
            except Exception as e:
                logger.warning(f"Error extracting product data: {e}")
            
            await page.close()
            
            # Check if product is out of stock
            if not price and not title:
                return None
            
            return {
                "title": title or "Unknown Product",
                "current_price": price,
                "url": url,
                "image_url": image_url,
                "site": "amazon.in",
                "last_checked": datetime.now().isoformat(),
                "method": "playwright"
            }
            
        except PlaywrightTimeoutError:
            logger.error(f"Timeout scraping product: {url}")
            return None
        except Exception as e:
            logger.error(f"Error scraping product {url}: {e}", exc_info=True)
            return None
    
    def _parse_price(self, price_text: str) -> Optional[float]:
        """
        Parse price string to float.
        Handles ₹, commas, decimals.
        
        Args:
            price_text: Price string (e.g., "₹69,999", "69,999.00")
            
        Returns:
            Price as float or None
        """
        if not price_text:
            return None
        
        # Remove currency symbols and whitespace
        price_clean = re.sub(r'[₹$€£,\s]', '', price_text.strip())
        
        # Extract numbers (including decimals)
        price_match = re.search(r'(\d+\.?\d*)', price_clean)
        if price_match:
            try:
                return float(price_match.group(1))
            except ValueError:
                return None
        
        return None
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _is_amazon_url(self, url: str) -> bool:
        """Check if URL is from Amazon.in."""
        return "amazon.in" in url.lower()
    
    async def cleanup(self):
        """Cleanup browser resources."""
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None
    
    async def _close_browser(self):
        """Close browser (alias for cleanup for consistency)."""
        await self.cleanup()
