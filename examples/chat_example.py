import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from winformpy import Form, Application
from winformpy.ui_elements.chat import ChatPanel

class ChatExample(Form):
    def __init__(self):
        super().__init__({
            'Text': 'WinFormPy Assistant Demo',
            'Width': 550,
            'Height': 700
        })
        
        self.chat = ChatPanel(self)
        
        # Simulate some history
        self.chat.manager.receive_message("Welcome to the Chat Example!")
        self.chat.manager.receive_message("This component mimics a standard chat interface.")


if __name__ == "__main__":
    app = ChatExample()
    Application.Run(app)
