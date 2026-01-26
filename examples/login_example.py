"""
Login Form Demo with Multiple Users

This example demonstrates:
- Login with multiple test users
- Password change functionality
- Authentication result handling
- User display names
"""

import sys
import os

# Add project root to path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy.ui_elements.login.login_ui import LoginForm
from winformpy.ui_elements.login.login_backend import LoginBackend, AuthResult, PasswordChangeResult


class DemoLoginBackend(LoginBackend):
    """Demo backend for testing with multiple users."""
    
    def __init__(self):
        self._users = {
            'admin': {'password': 'admin123', 'name': 'Administrator'},
            'user': {'password': 'user123', 'name': 'Test User'},
            'demo': {'password': 'demo', 'name': 'Demo User'}
        }
    
    def authenticate(self, username, password):
        user = self._users.get(username)
        if user and user['password'] == password:
            return AuthResult(
                success=True,
                user_id=username,
                username=username,
                display_name=user['name']
            )
        return AuthResult(success=False, error="Invalid username or password")
    
    def change_password(self, username, old_password, new_password):
        user = self._users.get(username)
        if not user:
            return PasswordChangeResult(success=False, error="User not found")
        if user['password'] != old_password:
            return PasswordChangeResult(success=False, error="Current password is incorrect")
        user['password'] = new_password
        return PasswordChangeResult(success=True)


def main():
    """Run login demo."""
    print("=" * 50)
    print("  LOGIN FORM DEMO")
    print("=" * 50)
    print("\nAvailable test users:")
    print("  • admin / admin123")
    print("  • user / user123")
    print("  • demo / demo")
    print()
    
    # Show login form
    backend = DemoLoginBackend()
    login = LoginForm(backend=backend)
    
    if login.ShowDialog():
        print(f"\n✓ Login successful!")
        print(f"  User ID: {login.authenticated_user.user_id}")
        print(f"  Username: {login.authenticated_user.username}")
        print(f"  Display Name: {login.authenticated_user.display_name}")
    else:
        print("\n✗ Login cancelled")


if __name__ == "__main__":
    main()
