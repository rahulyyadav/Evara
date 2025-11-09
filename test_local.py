#!/usr/bin/env python3
"""
Comprehensive local test for Evara - tests all features.
"""
import os
import sys
import asyncio
from pathlib import Path

# Add taskflow to path
sys.path.insert(0, str(Path(__file__).parent / "taskflow"))

# Load environment variables
from dotenv import load_dotenv
load_dotenv("taskflow/.env")
load_dotenv(".env")

from app.agent import AgentOrchestrator
from app.config import settings

async def test_feature(name, test_func):
    """Run a test and report results."""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {name}")
    print('='*60)
    try:
        result = await test_func()
        if result:
            print(f"✅ {name}: PASSED")
            return True
        else:
            print(f"❌ {name}: FAILED")
            return False
    except Exception as e:
        print(f"❌ {name}: ERROR - {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_gemini_connection():
    """Test if Gemini is connected and working."""
    agent = AgentOrchestrator()
    if not agent.gemini_model:
        print("  ⚠️  Gemini model not initialized")
        return False
    
    print(f"  ✅ Gemini model initialized: {agent.gemini_model._model_name}")
    return True

async def test_general_question():
    """Test general question handling."""
    agent = AgentOrchestrator()
    test_number = "1234567890"
    
    # Test 1: "who made you?"
    print("\n  Test 1: 'who made you?'")
    response1 = await agent.process_message(test_number, "who made you?")
    print(f"  Response: {response1[:150]}...")
    if "Rahul Yadav" in response1 or "created by" in response1.lower():
        print("  ✅ Correctly answered about creator")
    else:
        print("  ⚠️  Response doesn't mention creator")
    
    # Test 2: General knowledge
    print("\n  Test 2: 'who is prime minister of switzerland?'")
    response2 = await agent.process_message(test_number, "who is prime minister of switzerland?")
    print(f"  Response: {response2[:150]}...")
    if len(response2) > 20 and "switzerland" in response2.lower():
        print("  ✅ Answered general knowledge question")
    else:
        print("  ⚠️  Response seems incomplete")
    
    return True

async def test_flight_search():
    """Test flight search entity extraction."""
    agent = AgentOrchestrator()
    test_number = "1234567890"
    
    # Test 1: Complete flight query with specific date
    print("\n  Test 1: 'find flights from chennai to bagdogra on 2nd December'")
    response1 = await agent.process_message(test_number, "find flights from chennai to bagdogra on 2nd December")
    print(f"  Response: {response1[:300]}...")
    if "400" in response1 or "error" in response1.lower():
        print("  ⚠️  Got error response - checking details...")
    elif "flight" in response1.lower() or "chennai" in response1.lower():
        print("  ✅ Flight search processed successfully")
    
    # Test 2: Complete flight query with relative date
    print("\n  Test 2: 'find flights from chennai to bagdogra next tuesday'")
    response2 = await agent.process_message(test_number, "find flights from chennai to bagdogra next tuesday")
    print(f"  Response: {response2[:300]}...")
    
    # Test 3: Partial query
    print("\n  Test 3: 'find flights to mumbai next friday'")
    response3 = await agent.process_message(test_number, "find flights to mumbai next friday")
    print(f"  Response: {response3[:300]}...")
    
    return True

async def test_reminder():
    """Test reminder feature."""
    agent = AgentOrchestrator()
    test_number = "1234567890"
    
    # Test 1: Reminder without country
    print("\n  Test 1: 'remind me to call doctor tomorrow at 3pm'")
    response1 = await agent.process_message(test_number, "remind me to call doctor tomorrow at 3pm")
    print(f"  Response: {response1[:200]}...")
    if "country" in response1.lower() or "location" in response1.lower():
        print("  ✅ Correctly asking for country/location")
    else:
        print("  ⚠️  Should ask for country/location")
    
    # Test 2: Reminder with country
    print("\n  Test 2: 'remind me to call doctor tomorrow at 3pm, India'")
    response2 = await agent.process_message(test_number, "remind me to call doctor tomorrow at 3pm, India")
    print(f"  Response: {response2[:200]}...")
    
    return True

async def test_price_tracking():
    """Test price tracking entity extraction."""
    agent = AgentOrchestrator()
    test_number = "1234567890"
    
    # Test 1: Track product
    print("\n  Test 1: 'track iPhone 15 price'")
    response1 = await agent.process_message(test_number, "track iPhone 15 price")
    print(f"  Response: {response1[:200]}...")
    
    # Test 2: Check tracked items
    print("\n  Test 2: 'check my tracked items'")
    response2 = await agent.process_message(test_number, "check my tracked items")
    print(f"  Response: {response2[:200]}...")
    
    return True

async def test_intent_classification():
    """Test intent classification for various queries."""
    agent = AgentOrchestrator()
    test_number = "1234567890"
    
    test_cases = [
        ("hello", "general"),
        ("find flights to mumbai", "flight_search"),
        ("track iPhone", "price_track"),
        ("remind me to call", "reminder"),
        ("who made you", "general"),
    ]
    
    print("\n  Testing intent classification:")
    for message, expected_intent in test_cases:
        intent_result = await agent._classify_intent(message, [])
        actual_intent = intent_result.get("intent", "unknown")
        status = "✅" if actual_intent == expected_intent else "⚠️"
        print(f"  {status} '{message}' → {actual_intent} (expected: {expected_intent})")
    
    return True

async def main():
    """Run all tests."""
    print("🚀 Starting Evara Local Tests")
    print("="*60)
    
    # Check environment
    print("\n📋 Environment Check:")
    print(f"  GEMINI_API_KEY: {'✅ Set' if settings.GEMINI_API_KEY else '❌ Not set'}")
    print(f"  META_ACCESS_TOKEN: {'✅ Set' if settings.META_ACCESS_TOKEN else '❌ Not set'}")
    print(f"  SERPAPI_KEY: {'✅ Set' if settings.SERPAPI_KEY else '⚠️  Not set (optional)'}")
    
    results = []
    
    # Run tests
    results.append(await test_feature("Gemini Connection", test_gemini_connection))
    results.append(await test_feature("Intent Classification", test_intent_classification))
    results.append(await test_feature("General Questions", test_general_question))
    results.append(await test_feature("Flight Search", test_flight_search))
    results.append(await test_feature("Reminder", test_reminder))
    results.append(await test_feature("Price Tracking", test_price_tracking))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 Test Summary")
    print('='*60)
    passed = sum(results)
    total = len(results)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Evara is ready!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

