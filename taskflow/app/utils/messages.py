"""
User-facing message utilities for TaskFlow.
Provides friendly messages for users while logging technical errors.
"""


def get_welcome_message() -> str:
    """
    Get welcome message for first-time users.
    
    Returns:
        Welcome message string
    """
    return (
        "👋 Hey! I'm TaskFlow, your AI assistant.\n\n"
        "I can help you with:\n"
        "✈️ Search flights\n"
        "💰 Track product prices\n"
        "⏰ Set reminders\n"
        "❓ Ask me anything!\n\n"
        "Try: 'Find flights to Mumbai next Friday'"
    )


def get_help_message() -> str:
    """
    Get help message showing capabilities and examples.
    
    Returns:
        Help message string
    """
    return (
        "📚 TaskFlow Help\n\n"
        "I can help you with:\n\n"
        "✈️ Flight Search:\n"
        "  • 'Find flights from Delhi to Mumbai on Dec 15'\n"
        "  • 'Cheap flights to Goa tomorrow'\n\n"
        "💰 Price Tracking:\n"
        "  • 'Track iPhone 15 price on Amazon'\n"
        "  • 'Check my tracked items'\n"
        "  • 'Stop tracking [product name]'\n\n"
        "⏰ Reminders:\n"
        "  • 'Remind me to call doctor tomorrow at 3pm'\n"
        "  • 'Set reminder for meeting on Dec 20 at 2pm'\n"
        "  • 'Show my reminders'\n\n"
        "❓ General Chat:\n"
        "  • Ask me anything!\n\n"
        "Type 'help' anytime to see this message again."
    )


def get_friendly_error_message(error_type: str = "general") -> str:
    """
    Get friendly error message for users.
    Technical errors are logged but not shown to users.
    
    Args:
        error_type: Type of error (initialization, processing, api, etc.)
        
    Returns:
        Friendly error message
    """
    messages = {
        "initialization": (
            "⚠️ Sorry, I'm not fully initialized yet. "
            "Please try again in a moment."
        ),
        "processing": (
            "😅 Oops, something went wrong processing your message. "
            "Could you try rephrasing your request?"
        ),
        "api": (
            "🌐 I'm having trouble connecting to external services. "
            "Please try again in a moment."
        ),
        "general": (
            "😅 Oops, something went wrong. Try again?"
        )
    }
    
    return messages.get(error_type, messages["general"])

