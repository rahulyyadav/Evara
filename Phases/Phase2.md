Now create the core agent orchestration logic in agent.py.

This agent should:

1. Use Google Gemini API to understand user intent
2. Decide which tool to use based on the message
3. Execute tools and handle errors gracefully
4. Maintain conversation state and memory
5. Format responses naturally for WhatsApp

Agent Architecture:

- Intent Classification: Determine what user wants (flight search, price tracking, reminder, general chat)
- Tool Selection: Choose appropriate tool based on intent
- Tool Execution: Call tool with extracted parameters
- Response Generation: Format tool output into natural language
- Memory Management: Remember user preferences and context

Intent Categories:

1. "flight_search" - User wants to search flights
2. "price_track" - User wants to track product prices
3. "reminder" - User wants to set a reminder
4. "status_check" - Check status of previous tasks
5. "general" - Casual conversation

Agent Flow:

1. Receive message from webhook
2. Load user memory (past conversations, preferences)
3. Use Gemini to classify intent and extract entities
4. If tool needed: execute tool, get result
5. Generate natural response using Gemini
6. Save context to memory
7. Return formatted message

Key Requirements:

- Use Gemini 1.5 Flash (free tier, fast)
- Implement retry logic for API failures
- Handle ambiguous requests (ask clarifying questions)
- Keep responses concise for WhatsApp (under 1600 chars)
- Log all agent decisions for debugging

Create agent.py with:

1. AgentOrchestrator class
2. process_message() async method
3. \_classify_intent() using Gemini
4. \_execute_tool() with error handling
5. \_generate_response() for natural language
6. Integration with memory store

Use structured prompts for Gemini to get consistent JSON responses for intent classification.
