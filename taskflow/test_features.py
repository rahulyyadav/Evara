#!/usr/bin/env python3
"""
Test script for TaskFlow features.
Simulates WhatsApp messages to test all functionality.
"""
import asyncio
import httpx
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
TEST_PHONE = "whatsapp:+1234567890"


async def send_test_message(message: str, message_sid: str = None) -> Dict[str, Any]:
    """
    Send a test message to the webhook endpoint.
    
    Args:
        message: Message body to send
        message_sid: Optional message SID
        
    Returns:
        Response data
    """
    if message_sid is None:
        message_sid = f"test_{hash(message) % 10000}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/webhook",
                data={
                    "From": TEST_PHONE,
                    "Body": message,
                    "MessageSid": message_sid,
                    "NumMedia": "0"
                },
                timeout=30.0
            )
            return {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "message": message
            }
        except Exception as e:
            return {
                "status_code": 0,
                "success": False,
                "error": str(e),
                "message": message
            }


async def test_health_check():
    """Test health check endpoint."""
    print("\n" + "="*80)
    print("🏥 Testing Health Check")
    print("="*80)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/health")
            data = response.json()
            print(f"✅ Status: {data.get('status')}")
            print(f"✅ App: {data.get('app')}")
            print(f"✅ Twilio Configured: {data.get('twilio_configured')}")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False


async def test_flight_search():
    """Test flight search feature."""
    print("\n" + "="*80)
    print("✈️  Testing Flight Search")
    print("="*80)
    
    test_cases = [
        "flights from Delhi to Mumbai on Dec 15",
        "cheap flights to Goa tomorrow",
        "flights from Bangalore to Chennai next Friday"
    ]
    
    results = []
    for message in test_cases:
        print(f"\n📤 Sending: {message}")
        result = await send_test_message(message)
        results.append(result)
        if result["success"]:
            print(f"✅ Response received (Status: {result['status_code']})")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    return all(r["success"] for r in results)


async def test_price_tracking():
    """Test price tracking feature."""
    print("\n" + "="*80)
    print("📦 Testing Price Tracking")
    print("="*80)
    
    test_cases = [
        ("Track iPhone 15 price on Amazon", "track"),
        ("Check tracked items", "check"),
        ("Show my tracked products", "check"),
    ]
    
    results = []
    for message, action in test_cases:
        print(f"\n📤 Sending: {message}")
        result = await send_test_message(message)
        results.append(result)
        if result["success"]:
            print(f"✅ Response received (Status: {result['status_code']})")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    return all(r["success"] for r in results)


async def test_reminders():
    """Test reminder feature."""
    print("\n" + "="*80)
    print("⏰ Testing Reminders")
    print("="*80)
    
    test_cases = [
        ("Remind me to call doctor tomorrow at 3pm", "set"),
        ("Set reminder for meeting on Dec 20 at 2pm", "set"),
        ("Show my reminders", "list"),
        ("List all reminders", "list"),
    ]
    
    results = []
    for message, action in test_cases:
        print(f"\n📤 Sending: {message}")
        result = await send_test_message(message)
        results.append(result)
        if result["success"]:
            print(f"✅ Response received (Status: {result['status_code']})")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    return all(r["success"] for r in results)


async def test_general_chat():
    """Test general conversation."""
    print("\n" + "="*80)
    print("💬 Testing General Chat")
    print("="*80)
    
    test_cases = [
        "Hello",
        "What can you do?",
        "Help me",
    ]
    
    results = []
    for message in test_cases:
        print(f"\n📤 Sending: {message}")
        result = await send_test_message(message)
        results.append(result)
        if result["success"]:
            print(f"✅ Response received (Status: {result['status_code']})")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    return all(r["success"] for r in results)


async def main():
    """Run all tests."""
    print("\n" + "🚀"*40)
    print("TaskFlow Feature Testing")
    print("🚀"*40)
    print(f"\nTesting against: {BASE_URL}")
    print(f"Test phone number: {TEST_PHONE}")
    
    # Check if server is running
    try:
        async with httpx.AsyncClient() as client:
            await client.get(f"{BASE_URL}/health", timeout=5.0)
        print("\n✅ Server is running!")
    except Exception as e:
        print(f"\n❌ Server is not running! Please start it first.")
        print(f"   Error: {e}")
        print(f"\n   Start server with: python3 -m app.main")
        return
    
    # Run tests
    results = {}
    
    results["health"] = await test_health_check()
    await asyncio.sleep(1)
    
    results["flight_search"] = await test_flight_search()
    await asyncio.sleep(1)
    
    results["price_tracking"] = await test_price_tracking()
    await asyncio.sleep(1)
    
    results["reminders"] = await test_reminders()
    await asyncio.sleep(1)
    
    results["general_chat"] = await test_general_chat()
    
    # Summary
    print("\n" + "="*80)
    print("📊 Test Summary")
    print("="*80)
    
    for feature, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {feature.replace('_', ' ').title()}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check server logs for details.")


if __name__ == "__main__":
    asyncio.run(main())

