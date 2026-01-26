"""
Web Browser Demo - Full-featured browser with tabs

This example demonstrates:
- Tabbed browsing
- Navigation controls (Back, Forward, Refresh, Home)
- Address bar with URL input
- Favorites management
- History tracking
- Downloads tracking
- Menu bar with full options
"""

import sys
import os

# Add project root to path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy.winformpy import Application
from winformpy.ui_elements.web_browser.web_browser_ui import WebBrowserUI


def main():
    """Run web browser demo."""
    print("=" * 60)
    print("  WEB BROWSER DEMO")
    print("=" * 60)
    
    # Check if tkinterweb is available
    try:
        import tkinterweb  # External dependency, not part of WinFormPy
    except ImportError:
        print("\n⚠️  ERROR: tkinterweb is not installed")
        print("\nThe WebBrowser component requires the tkinterweb library.")
        print("\nTo install it, run:")
        print("  pip install tkinterweb")
        print("\nOr with uv:")
        print("  uv pip install tkinterweb")
        print()
        return
    
    print("\nFeatures:")
    print("  • Tabbed browsing (Ctrl+T new, Ctrl+W close)")
    print("  • Navigation (Back, Forward, Refresh, Home)")
    print("  • Favorites (Ctrl+D to add, Ctrl+I sidebar)")
    print("  • History (Ctrl+H sidebar)")
    print("  • Downloads (Ctrl+J sidebar)")
    print("  • Keyboard shortcuts (F5 refresh, F11 fullscreen)")
    print("  • Menu bar with full options")
    print("  • Status bar with progress")
    print()
    print("Starting browser...")
    
    browser = WebBrowserUI()
    Application.Run(browser)


if __name__ == "__main__":
    main()
