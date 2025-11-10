#!/usr/bin/env python3
"""
Test script to demonstrate memory-aware capabilities of Evara agent.

This script tests multi-turn conversations where the agent needs to:
1. Merge information across multiple turns
2. Remember context from previous messages
3. Handle follow-up questions intelligently
4. Provide context-aware responses
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from taskflow.app.agent import AgentOrchestrator
from taskflow.app.config import settings

# Test user number
TEST_USER = "+1234567890"


def print_separator(title=""):
    """Print a visual separator."""
    if title:
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
    else:
        print(f"\n{'-'*80}\n")


async def test_conversation(agent, messages, test_name):
    """
    Test a multi-turn conversation.
    
    Args:
        agent: AgentOrchestrator instance
        messages: List of user messages to send sequentially
        test_name: Name of the test
    """
    print_separator(f"TEST: {test_name}")
    
    for i, message in enumerate(messages, 1):
        print(f"👤 Turn {i} - User: {message}")
        response = await agent.process_message(TEST_USER, message)
        print(f"🤖 Turn {i} - Evara: {response}")
        print_separator()
        
        # Small delay between messages
        await asyncio.sleep(1)


async def main():
    """Run all memory-awareness tests."""
    print_separator("🧠 MEMORY-AWARENESS TEST SUITE")
    print("Testing Evara's ability to remember and use conversation context\n")
    
    if not settings.GEMINI_API_KEY:
        print("❌ ERROR: GEMINI_API_KEY not set!")
        print("Please set it in your .env file to run these tests.")
        return 1
    
    # Initialize agent
    print("🚀 Initializing Evara agent...")
    agent = AgentOrchestrator()
    
    if not agent.gemini_model:
        print("❌ ERROR: Gemini model not initialized!")
        return 1
    
    print("✅ Agent initialized successfully!\n")
    
    # =========================================================================
    # TEST 1: Flight Search - Information Split Across Turns
    # =========================================================================
    await test_conversation(
        agent,
        [
            "search flight for me on 2nd dec",  # Provides date only
            "chennai to bagdogra"  # Provides origin and destination
        ],
        "Flight Search - Information Split Across Turns"
    )
    
    # =========================================================================
    # TEST 2: Flight Search - Partial Information Then Complete
    # =========================================================================
    await test_conversation(
        agent,
        [
            "I want to fly to mumbai",  # Destination only
            "from bangalore tomorrow"  # Origin and date
        ],
        "Flight Search - Completing Partial Information"
    )
    
    # =========================================================================
    # TEST 3: Price Tracking - Follow-up Question
    # =========================================================================
    await test_conversation(
        agent,
        [
            "track iPhone 15 price",  # Track a product
            "what's the price now?"  # Follow-up referring to iPhone 15
        ],
        "Price Tracking - Follow-up Question"
    )
    
    # =========================================================================
    # TEST 4: Price Tracking - Contextual Reference
    # =========================================================================
    await test_conversation(
        agent,
        [
            "search me price of samsung s24",  # Search product
            "stop tracking that"  # Reference to previous product
        ],
        "Price Tracking - Contextual Reference"
    )
    
    # =========================================================================
    # TEST 5: Reminder - Clarification Across Turns
    # =========================================================================
    await test_conversation(
        agent,
        [
            "remind me",  # Incomplete request
            "to call doctor at 3pm tomorrow"  # Complete information
        ],
        "Reminder - Completing Information"
    )
    
    # =========================================================================
    # TEST 6: General Chat - Context Continuity
    # =========================================================================
    await test_conversation(
        agent,
        [
            "what is the capital of France?",
            "and what about Germany?",  # Follow-up question
            "which one is larger?"  # Referring to previous context
        ],
        "General Chat - Context Continuity"
    )
    
    # =========================================================================
    # TEST 7: Mixed Context - Switching Topics
    # =========================================================================
    await test_conversation(
        agent,
        [
            "search flight from delhi to goa on 5th dec",
            "what time is it in india?",
            "ok, make it for morning 9am"  # Referring to flight, not time
        ],
        "Mixed Context - Topic Switching"
    )
    
    # =========================================================================
    # TEST 8: Status Check After Multiple Actions
    # =========================================================================
    await test_conversation(
        agent,
        [
            "track iphone 15",
            "remind me to buy tickets at 5pm",
            "search flight mumbai to delhi",
            "what am i tracking and what are my reminders?"  # Status check
        ],
        "Status Check - After Multiple Actions"
    )
    
    # =========================================================================
    # TEST 9: Complex Multi-Turn Flight Search
    # =========================================================================
    await test_conversation(
        agent,
        [
            "I need to travel next week",
            "to bangalore",
            "from chennai",
            "on monday"
        ],
        "Complex Multi-Turn Flight Search"
    )
    
    # =========================================================================
    # TEST 10: Follow-up with Pronoun Reference
    # =========================================================================
    await test_conversation(
        agent,
        [
            "track macbook pro price",
            "is it available?",  # "it" refers to macbook pro
            "what's the best price for it?"  # "it" still refers to macbook pro
        ],
        "Follow-up with Pronoun Reference"
    )
    
    print_separator("✅ ALL TESTS COMPLETED")
    print("\nSummary:")
    print("- 10 memory-awareness tests executed")
    print("- Each test covers different aspects of context awareness")
    print("- Check responses to verify Evara is using conversation history\n")
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

