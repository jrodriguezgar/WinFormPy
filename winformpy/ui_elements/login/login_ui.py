"""
Login Form - Standalone Login Window
====================================

A modal login dialog/form that can be used for application authentication.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

try:
    from winformpy.winformpy import (
        Form, Panel, Label, Application,
        DockStyle, FormStartPosition, FormBorderStyle
    )
except ImportError:
    from winformpy import (
        Form, Panel, Label, Application,
        DockStyle, FormStartPosition, FormBorderStyle
    )

try:
    from .login_panel import LoginPanel, LoginView
    from .login_manager import LoginManager, LoginState
    from .login_backend import LoginBackend
except ImportError:
    from login_panel import LoginPanel, LoginView
    from login_manager import LoginManager, LoginState
    from login_backend import LoginBackend

from typing import Optional


class LoginForm(Form):
    """
    Standalone login form/dialog.
    
    Can be shown as a modal dialog that blocks until authentication
    is successful or the user cancels.
    
    Example:
        backend = MyAuthBackend()
        login_form = LoginForm(backend=backend)
        
        if login_form.ShowDialog():
            # User authenticated successfully
            user = login_form.authenticated_user
            print(f"Welcome, {user.display_name}!")
        else:
            # User cancelled
            print("Login cancelled")
    """
    
    def __init__(self, backend: LoginBackend = None, 
                 manager: LoginManager = None,
                 title: str = "Sign In",
                 width: int = 450,
                 height: int = 550):
        """
        Initialize the LoginForm.
        
        Args:
            backend: LoginBackend for authentication
            manager: Pre-configured LoginManager
            title: Window title
            width: Window width
            height: Window height
        """
        super().__init__()
        
        self.Text = title
        self.Width = width
        self.Height = height
        self.StartPosition = FormStartPosition.CenterScreen
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.MaximizeBox = False
        self.MinimizeBox = False
        
        self._authenticated_user: Optional[LoginState] = None
        self._dialog_result = False
        
        # Apply layout before adding controls
        self.ApplyLayout()
        
        # Create login panel
        self._login_panel = LoginPanel(
            self,
            props={'Dock': DockStyle.Fill},
            backend=backend,
            manager=manager
        )
        
        # Wire up events
        self._login_panel.LoginSuccess = self._on_login_success
        
        # Handle form closing
        self.FormClosing = self._on_form_closing
    
    def _on_login_success(self, state: LoginState):
        """Handle successful login."""
        self._authenticated_user = state
        self._dialog_result = True
        self.Close()
    
    def _on_form_closing(self, sender, e):
        """Handle form closing."""
        pass  # Allow closing
    
    @property
    def authenticated_user(self) -> Optional[LoginState]:
        """Get the authenticated user state."""
        return self._authenticated_user
    
    @property
    def is_authenticated(self) -> bool:
        """Check if login was successful."""
        return self._authenticated_user is not None and self._authenticated_user.is_authenticated
    
    @property
    def manager(self) -> LoginManager:
        """Get the login manager."""
        return self._login_panel.manager
    
    def ShowDialog(self) -> bool:
        """
        Show the login form as a modal dialog.
        
        Returns:
            True if user authenticated successfully, False if cancelled.
        """
        self._dialog_result = False
        self._authenticated_user = None
        super().ShowDialog()
        return self._dialog_result
    
    def show_change_password(self):
        """Show the change password view."""
        self._login_panel.show_change_password()
    
    def show_reset_password(self):
        """Show the reset password view."""
        self._login_panel.show_reset_password()


class ChangePasswordForm(Form):
    """
    Standalone change password form/dialog.
    
    Shows only the change password view for users who need to
    update their password.
    """
    
    def __init__(self, manager: LoginManager,
                 title: str = "Change Password",
                 width: int = 450,
                 height: int = 500):
        """
        Initialize the ChangePasswordForm.
        
        Args:
            manager: LoginManager with authenticated user
            title: Window title
            width: Window width
            height: Window height
        """
        super().__init__()
        
        self.Text = title
        self.Width = width
        self.Height = height
        self.StartPosition = FormStartPosition.CenterScreen
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.MaximizeBox = False
        self.MinimizeBox = False
        
        self._success = False
        
        # Apply layout
        self.ApplyLayout()
        
        # Create login panel
        self._login_panel = LoginPanel(
            self,
            props={'Dock': DockStyle.Fill},
            manager=manager
        )
        
        # Show change password view immediately
        self._login_panel.show_change_password()
        
        # Wire up success event
        self._login_panel.PasswordChangeSuccess = self._on_change_success
    
    def _on_change_success(self):
        """Handle successful password change."""
        self._success = True
        self.Close()
    
    @property
    def password_changed(self) -> bool:
        """Check if password was changed."""
        return self._success
    
    def ShowDialog(self) -> bool:
        """
        Show the form as a modal dialog.
        
        Returns:
            True if password was changed, False if cancelled.
        """
        self._success = False
        super().ShowDialog()
        return self._success


# Demo / Test
if __name__ == "__main__":
    from login_backend import LoginBackend, AuthResult, PasswordChangeResult
    
    # Demo backend
    class DemoBackend(LoginBackend):
        """Demo backend for testing."""
        
        def __init__(self):
            self._users = {
                'admin': {'password': 'admin123', 'name': 'Administrator'},
                'user': {'password': 'user123', 'name': 'Test User'}
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
    
    # Show login form
    backend = DemoBackend()
    login = LoginForm(backend=backend)
    
    if login.ShowDialog():
        print(f"Login successful! Welcome, {login.authenticated_user.display_name}")
    else:
        print("Login cancelled")
