#!/usr/bin/env python3
"""
Check if Chromium is needed and if it's installed.
"""
import sys

def check_chromium():
    """Check if Chromium is available for Playwright."""
    print("🔍 Checking Chromium Status...")
    print("="*60)
    
    # Check if Playwright is installed
    try:
        from playwright.async_api import async_playwright
        print("✅ Playwright package is installed")
    except ImportError:
        print("❌ Playwright package is NOT installed")
        print("   Install with: pip install playwright")
        return False
    
    # Check if Chromium browser is installed
    try:
        from playwright.sync_api import sync_playwright
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        browser.close()
        playwright.stop()
        print("✅ Chromium browser is installed and working")
        return True
    except Exception as e:
        error_msg = str(e)
        if "Executable doesn't exist" in error_msg or "BrowserType.launch" in error_msg:
            print("❌ Chromium browser is NOT installed")
            print("\n📦 To install Chromium (~170MB):")
            print("   playwright install chromium")
            print("\n💡 Note: Chromium is ONLY needed for price tracking feature")
            print("   Other features (flights, reminders, chat) work without it!")
            return False
        else:
            print(f"⚠️  Error checking Chromium: {e}")
            return False

def check_features_needing_chromium():
    """Show which features need Chromium."""
    print("\n" + "="*60)
    print("📋 Feature Requirements:")
    print("="*60)
    print("✅ Flight Search - NO Chromium needed (uses SerpAPI)")
    print("✅ Reminders - NO Chromium needed")
    print("✅ General Chat - NO Chromium needed")
    print("❌ Price Tracking - REQUIRES Chromium (for web scraping)")
    print("\n💡 You can use 75% of features without Chromium!")

if __name__ == "__main__":
    has_chromium = check_chromium()
    check_features_needing_chromium()
    
    print("\n" + "="*60)
    if has_chromium:
        print("✅ All features are ready to use!")
    else:
        print("⚠️  Price tracking won't work without Chromium")
        print("   But other features (flights, reminders) work fine!")
    print("="*60)

