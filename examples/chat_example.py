"""
Chat UI Demo - Messenger-style chat with smart responses

This example demonstrates:
- Custom response handler
- Smart message processing
- Welcome message
- Emoji support
- Feature demonstrations
"""

import sys
import os
from datetime import datetime

# Add project root to path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy.winformpy import Application
from winformpy.ui_elements.chat.chat_ui import ChatUI


def main():
    """Run chat UI demo with smart response handler."""
    
    print("=" * 60)
    print("ChatUI Demo - Messenger-Style Chat Interface")
    print("=" * 60)
    
    # Create chat UI
    chat = ChatUI(
        title="WinFormPy Messenger - Full Demo", 
        width=650, 
        height=800,
        user_name="You",
        assistant_name="WinFormPy Bot"
    )
    
    # Set custom response handler
    def smart_handler(message):
        msg_lower = message.lower()
        if 'hello' in msg_lower or 'hi' in msg_lower:
            return "Hello! 👋 How can I help you today?"
        elif 'help' in msg_lower:
            return ("I can help you with:\n"
                    "• 🔍 Search - Click the magnifying glass\n"
                    "• 😊 Emojis - Click the emoji button\n"
                    "• ⚙️ Settings - Toggle display options\n"
                    "• Right-click a message to copy/reply/delete")
        elif 'emoji' in msg_lower:
            return "Try the emoji bar! Click 😊 in the footer. 🎉✨🔥"
        elif 'time' in msg_lower:
            return f"The current time is {datetime.now().strftime('%H:%M:%S')} ⏰"
        else:
            return f"You said: '{message}'\n\nTry saying 'help' for more info!"
    
    chat.set_response_handler(smart_handler)
    
    # Add welcome message
    chat.send_message(
        "Welcome to WinFormPy Messenger! 🎉\n\n"
        "This demo showcases Messenger-style features:\n\n"
        "✓ Avatars and timestamps\n"
        "✓ Read status (✓✓)\n"
        "✓ Typing indicator\n"
        "✓ Emoji quick-access bar\n"
        "✓ Search in conversation (🔍)\n"
        "✓ Right-click context menu\n"
        "✓ Settings menu (⚙️)\n\n"
        "Try typing 'help' to learn more!"
    )
    
    print("\nDemo Features:")
    print("  • Avatars with initials (U/A)")
    print("  • Timestamps on each message")
    print("  • Read status checkmarks (✓✓)")
    print("  • Typing indicator animation")
    print("  • Emoji picker (click 😊)")
    print("  • Search bar (click 🔍)")
    print("  • Right-click for context menu")
    print("  • Settings menu (click ⚙️)")
    print("  • Export chat to file")
    print("\nStarting Messenger-style chat...")
    
    Application.Run(chat)


if __name__ == "__main__":
    main()
