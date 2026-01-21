"""
Login Panel - Embeddable Login Component
=========================================

A modern login panel that can be embedded in any Form or Panel.
Supports login, password change, and password reset views.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

try:
    from winformpy.winformpy import (
        Panel, Label, TextBox, Button, LinkLabel, CheckBox,
        DockStyle, AnchorStyles, ContentAlignment, Font, FontStyle,
        PictureBox, ProgressBar
    )
except ImportError:
    from winformpy import (
        Panel, Label, TextBox, Button, LinkLabel, CheckBox,
        DockStyle, AnchorStyles, ContentAlignment, Font, FontStyle,
        PictureBox, ProgressBar
    )

try:
    from .login_manager import LoginManager
    from .login_backend import LoginBackend, PasswordStrength
except ImportError:
    from login_manager import LoginManager
    from login_backend import LoginBackend, PasswordStrength

from typing import Optional, Callable
from enum import Enum


class LoginView(Enum):
    """Available views in the login panel."""
    LOGIN = "login"
    CHANGE_PASSWORD = "change_password"
    RESET_PASSWORD = "reset_password"


class LoginPanel(Panel):
    """
    Embeddable login panel with modern styling.
    
    Features:
        - Username/password login form
        - Remember me checkbox
        - Password change form with strength indicator
        - Password reset request form
        - Customizable styling and branding
        - Event handlers for all authentication outcomes
    
    Example:
        from winformpy.ui_elements.login import LoginPanel, LoginBackend
        
        class MyBackend(LoginBackend):
            def authenticate(self, username, password):
                # Your auth logic
                pass
            def change_password(self, username, old_pw, new_pw):
                # Your password change logic
                pass
        
        backend = MyBackend()
        login_panel = LoginPanel(form, backend=backend)
        login_panel.LoginSuccess = lambda state: print(f"Welcome {state.username}")
    """
    
    # Color scheme
    COLORS = {
        'background': '#FFFFFF',
        'primary': '#0078D4',
        'primary_hover': '#106EBE',
        'text': '#1A1A1A',
        'text_secondary': '#666666',
        'border': '#CCCCCC',
        'error': '#D13438',
        'success': '#107C10',
        'warning': '#FFB900',
        'input_bg': '#FFFFFF',
        'input_border': '#8A8A8A',
        'strength_weak': '#D13438',
        'strength_fair': '#FFB900',
        'strength_good': '#107C10',
        'strength_strong': '#0078D4',
    }
    
    def __init__(self, master_form, props: dict = None, 
                 backend: LoginBackend = None,
                 manager: LoginManager = None):
        """
        Initialize the LoginPanel.
        
        Args:
            master_form: Parent Form or Panel
            props: Optional properties dictionary. Supports sub-properties for internal elements:
                - 'Title': {'Font': Font(...), 'ForeColor': '#000', 'Text': 'Sign In', ...}
                - 'Subtitle': {'Font': Font(...), 'ForeColor': '#666', ...}
                - 'Inputs': {'Width': 340, 'Height': 40, 'BackColor': '#FFF', ...}
                - 'Button': {'BackColor': '#0078D4', 'ForeColor': '#FFF', 'Height': 45, ...}
                - 'Links': {'ForeColor': '#0078D4', ...}
            backend: Optional LoginBackend for authentication
            manager: Optional pre-configured LoginManager
            
        Example:
            login = LoginPanel(form, props={
                'Width': 450,
                'Height': 600,
                'Title': {'Text': 'Welcome', 'ForeColor': '#333'},
                'Button': {'BackColor': '#107C10', 'Height': 50},
                'Inputs': {'Width': 380}
            }, backend=my_auth)
        """
        # Extract sub-properties before passing to parent
        self._title_props = props.pop('Title', {}) if props else {}
        self._subtitle_props = props.pop('Subtitle', {}) if props else {}
        self._inputs_props = props.pop('Inputs', {}) if props else {}
        self._button_props = props.pop('Button', {}) if props else {}
        self._links_props = props.pop('Links', {}) if props else {}
        
        defaults = {
            'Width': 400,
            'Height': 500,
            'BackColor': self.COLORS['background'],
        }
        if props:
            defaults.update(props)
        
        super().__init__(master_form, defaults)
        
        # Apply sub-properties to internal settings (instance copy)
        self.COLORS = self.COLORS.copy()
        if 'ForeColor' in self._title_props:
            self.COLORS['text'] = self._title_props['ForeColor']
        if 'ForeColor' in self._links_props:
            self.COLORS['primary'] = self._links_props['ForeColor']
        if 'BackColor' in self._button_props:
            self.COLORS['primary'] = self._button_props['BackColor']
        
        # Setup manager
        if manager:
            self.manager = manager
        else:
            self.manager = LoginManager(backend)
        
        # Wire up manager events
        self.manager.LoginSuccess = self._on_login_success
        self.manager.LoginFailed = self._on_login_failed
        self.manager.PasswordChangeSuccess = self._on_password_change_success
        self.manager.PasswordChangeFailed = self._on_password_change_failed
        
        # External event handlers
        self.LoginSuccess: Callable = lambda state: None
        self.LoginFailed: Callable = lambda error: None
        self.PasswordChangeSuccess: Callable = lambda: None
        self.PasswordChangeFailed: Callable = lambda error: None
        self.ForgotPasswordClick: Callable = lambda: None
        
        # State
        self._current_view = LoginView.LOGIN
        self._views = {}
        
        # Build UI
        self._build_ui()
        self._show_view(LoginView.LOGIN)
    
    def _build_ui(self):
        """Build the login panel UI."""
        # Build all views
        self._build_login_view()
        self._build_change_password_view()
        self._build_reset_password_view()
    
    def _build_login_view(self):
        """Build the login form view."""
        view = Panel(self, {
            'Left': 0, 'Top': 0,
            'Width': self.Width,
            'Height': self.Height,
            'BackColor': self.COLORS['background'],
            'Visible': False
        })
        
        # Keep references to all widgets in this view
        self._login_view_widgets = []
        
        # Get configurable dimensions from sub-properties
        input_width = self._inputs_props.get('Width', self.Width - 60)
        input_height = self._inputs_props.get('Height', 35)
        button_height = self._button_props.get('Height', 45)
        left_margin = (self.Width - input_width) // 2
        
        y = 40
        
        # Title - apply Title sub-properties
        title_text = self._title_props.get('Text', 'Sign In')
        title_font = self._title_props.get('Font', Font('Segoe UI', 24, FontStyle.Regular))
        title_color = self._title_props.get('ForeColor', self.COLORS['text'])
        
        self._login_title = Label(view, {
            'Text': title_text,
            'Left': left_margin, 'Top': y,
            'Width': input_width,
            'Height': 50,
            'Font': title_font,
            'ForeColor': title_color
        })
        y += 65
        
        # Subtitle - apply Subtitle sub-properties
        subtitle_text = self._subtitle_props.get('Text', 'Enter your credentials to continue')
        subtitle_font = self._subtitle_props.get('Font', Font('Segoe UI', 10))
        subtitle_color = self._subtitle_props.get('ForeColor', self.COLORS['text_secondary'])
        
        self._login_subtitle = Label(view, {
            'Text': subtitle_text,
            'Left': left_margin, 'Top': y,
            'Width': input_width,
            'Height': 20,
            'Font': subtitle_font,
            'ForeColor': subtitle_color
        })
        y += 40
        
        # Username label
        self._username_label = Label(view, {
            'Text': 'Username or Email',
            'Left': left_margin, 'Top': y,
            'Width': input_width,
            'Height': 20,
            'Font': Font('Segoe UI', 10),
            'ForeColor': self.COLORS['text']
        })
        y += 22
        
        # Username input - apply Inputs sub-properties
        input_bg = self._inputs_props.get('BackColor', '#FFFFFF')
        input_font = self._inputs_props.get('Font', Font('Segoe UI', 11))
        
        self._username_input = TextBox(view, {
            'Left': left_margin, 'Top': y,
            'Width': input_width,
            'Height': input_height,
            'Font': input_font,
            'BackColor': input_bg,
            'BorderStyle': 'FixedSingle'
        })
        y += input_height + 15
        
        # Password label
        self._password_label = Label(view, {
            'Text': 'Password',
            'Left': left_margin, 'Top': y,
            'Width': input_width,
            'Height': 20,
            'Font': Font('Segoe UI', 10),
            'ForeColor': self.COLORS['text']
        })
        y += 22
        
        # Password input - apply Inputs sub-properties
        self._password_input = TextBox(view, {
            'Left': left_margin, 'Top': y,
            'Width': input_width,
            'Height': input_height,
            'Font': input_font,
            'BackColor': input_bg,
            'BorderStyle': 'FixedSingle',
            'PasswordChar': '●'
        })
        y += input_height + 10
        
        # Remember me & Forgot password row
        link_color = self._links_props.get('ForeColor', self.COLORS['primary'])
        
        self._remember_me = CheckBox(view, {
            'Text': 'Remember me',
            'Left': left_margin, 'Top': y,
            'Width': 150,
            'Height': 25,
            'Font': Font('Segoe UI', 10),
            'ForeColor': self.COLORS['text']
        })
        
        self._forgot_link = LinkLabel(view, {
            'Text': 'Forgot password?',
            'Left': left_margin + input_width - 120, 'Top': y,
            'Width': 120,
            'Height': 25,
            'Font': Font('Segoe UI', 10),
            'TextAlign': ContentAlignment.MiddleRight,
            'ForeColor': link_color
        })
        self._forgot_link.Click = lambda s, e: self._show_view(LoginView.RESET_PASSWORD)
        y += 40
        
        # Error message label (hidden by default)
        self._login_error_label = Label(view, {
            'Text': '',
            'Left': left_margin, 'Top': y,
            'Width': input_width,
            'Height': 30,
            'Font': Font('Segoe UI', 9),
            'ForeColor': self.COLORS['error'],
            'Visible': False
        })
        y += 35
        
        # Login button - apply Button sub-properties
        button_text = self._button_props.get('Text', 'Sign In')
        button_bg = self._button_props.get('BackColor', self.COLORS['primary'])
        button_fg = self._button_props.get('ForeColor', '#FFFFFF')
        button_font = self._button_props.get('Font', Font('Segoe UI', 11, FontStyle.Bold))
        
        self._login_button = Button(view, {
            'Text': button_text,
            'Left': left_margin, 'Top': y,
            'Width': input_width,
            'Height': button_height,
            'Font': button_font,
            'BackColor': button_bg,
            'ForeColor': button_fg,
            'FlatStyle': 'Flat'
        })
        self._login_button.Click = self._on_login_click
        y += button_height + 15
        
        # Change password link (for when password change is required)
        self._change_pw_link = LinkLabel(view, {
            'Text': 'Need to change your password?',
            'Left': left_margin, 'Top': y,
            'Width': input_width,
            'Height': 25,
            'Font': Font('Segoe UI', 10),
            'TextAlign': ContentAlignment.MiddleCenter,
            'ForeColor': link_color
        })
        self._change_pw_link.Click = lambda s, e: self._show_view(LoginView.CHANGE_PASSWORD)
        
        self._views[LoginView.LOGIN] = view
    
    def _build_change_password_view(self):
        """Build the change password form view."""
        view = Panel(self, {
            'Left': 0, 'Top': 0,
            'Width': self.Width,
            'Height': self.Height,
            'BackColor': self.COLORS['background'],
            'Visible': False
        })
        
        y = 40
        
        # Title
        self._change_title = Label(view, {
            'Text': 'Change Password',
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 50,
            'Font': Font('Segoe UI', 24, FontStyle.Regular),
            'ForeColor': self.COLORS['text']
        })
        y += 65
        
        # Current password label
        self._current_pw_label = Label(view, {
            'Text': 'Current Password',
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 20,
            'Font': Font('Segoe UI', 10),
            'ForeColor': self.COLORS['text']
        })
        y += 22
        
        self._current_pw_input = TextBox(view, {
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 35,
            'Font': Font('Segoe UI', 11),
            'BorderStyle': 'FixedSingle',
            'PasswordChar': '●'
        })
        y += 50
        
        # New password label
        self._new_pw_label = Label(view, {
            'Text': 'New Password',
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 20,
            'Font': Font('Segoe UI', 10),
            'ForeColor': self.COLORS['text']
        })
        y += 22
        
        self._new_pw_input = TextBox(view, {
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 35,
            'Font': Font('Segoe UI', 11),
            'BorderStyle': 'FixedSingle',
            'PasswordChar': '●'
        })
        self._new_pw_input.TextChanged = self._on_new_password_changed
        y += 40
        
        # Password strength indicator
        self._strength_label = Label(view, {
            'Text': '',
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 20,
            'Font': Font('Segoe UI', 9),
            'ForeColor': self.COLORS['text_secondary']
        })
        y += 25
        
        self._strength_bar = ProgressBar(view, {
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 8,
            'Minimum': 0,
            'Maximum': 5,
            'Value': 0
        })
        y += 25
        
        # Confirm password label
        self._confirm_pw_label = Label(view, {
            'Text': 'Confirm New Password',
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 20,
            'Font': Font('Segoe UI', 10),
            'ForeColor': self.COLORS['text']
        })
        y += 22
        
        self._confirm_pw_input = TextBox(view, {
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 35,
            'Font': Font('Segoe UI', 11),
            'BorderStyle': 'FixedSingle',
            'PasswordChar': '●'
        })
        y += 50
        
        # Error message
        self._change_error_label = Label(view, {
            'Text': '',
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 30,
            'Font': Font('Segoe UI', 9),
            'ForeColor': self.COLORS['error'],
            'Visible': False
        })
        y += 35
        
        # Change button
        self._change_button = Button(view, {
            'Text': 'Change Password',
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 45,
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'BackColor': self.COLORS['primary'],
            'ForeColor': '#FFFFFF',
            'FlatStyle': 'Flat'
        })
        self._change_button.Click = self._on_change_password_click
        y += 55
        
        # Back to login link
        self._change_back_link = LinkLabel(view, {
            'Text': '← Back to Sign In',
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 25,
            'Font': Font('Segoe UI', 10)
        })
        self._change_back_link.Click = lambda s, e: self._show_view(LoginView.LOGIN)
        
        self._views[LoginView.CHANGE_PASSWORD] = view
    
    def _build_reset_password_view(self):
        """Build the password reset request view."""
        view = Panel(self, {
            'Left': 0, 'Top': 0,
            'Width': self.Width,
            'Height': self.Height,
            'BackColor': self.COLORS['background'],
            'Visible': False
        })
        
        y = 40
        
        # Title
        self._reset_title = Label(view, {
            'Text': 'Reset Password',
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 50,
            'Font': Font('Segoe UI', 24, FontStyle.Regular),
            'ForeColor': self.COLORS['text']
        })
        y += 65
        
        # Instructions
        self._reset_instructions = Label(view, {
            'Text': 'Enter your email address and we\'ll send you\ninstructions to reset your password.',
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 50,
            'Font': Font('Segoe UI', 10),
            'ForeColor': self.COLORS['text_secondary']
        })
        y += 60
        
        # Email label
        self._reset_email_label = Label(view, {
            'Text': 'Email Address',
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 20,
            'Font': Font('Segoe UI', 10),
            'ForeColor': self.COLORS['text']
        })
        y += 22
        
        self._reset_email_input = TextBox(view, {
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 35,
            'Font': Font('Segoe UI', 11),
            'BorderStyle': 'FixedSingle'
        })
        y += 50
        
        # Success message (hidden)
        self._reset_success_label = Label(view, {
            'Text': 'Password reset email sent! Check your inbox.',
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 30,
            'Font': Font('Segoe UI', 10),
            'ForeColor': self.COLORS['success'],
            'Visible': False
        })
        
        # Error message (hidden)
        self._reset_error_label = Label(view, {
            'Text': '',
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 30,
            'Font': Font('Segoe UI', 9),
            'ForeColor': self.COLORS['error'],
            'Visible': False
        })
        y += 40
        
        # Reset button
        self._reset_button = Button(view, {
            'Text': 'Send Reset Link',
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 45,
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'BackColor': self.COLORS['primary'],
            'ForeColor': '#FFFFFF',
            'FlatStyle': 'Flat'
        })
        self._reset_button.Click = self._on_reset_click
        y += 55
        
        # Back to login link
        self._reset_back_link = LinkLabel(view, {
            'Text': '← Back to Sign In',
            'Left': 30, 'Top': y,
            'Width': self.Width - 60,
            'Height': 25,
            'Font': Font('Segoe UI', 10)
        })
        self._reset_back_link.Click = lambda s, e: self._show_view(LoginView.LOGIN)
        
        self._views[LoginView.RESET_PASSWORD] = view
    
    def _show_view(self, view: LoginView):
        """Switch to a specific view."""
        for v in self._views.values():
            v.Visible = False
        
        self._views[view].Visible = True
        self._current_view = view
        
        # Clear fields and errors when switching views
        self._clear_errors()
    
    def _clear_errors(self):
        """Clear all error messages."""
        self._login_error_label.Text = ''
        self._login_error_label.Visible = False
        self._change_error_label.Text = ''
        self._change_error_label.Visible = False
        self._reset_error_label.Text = ''
        self._reset_error_label.Visible = False
        self._reset_success_label.Visible = False
    
    def _show_login_error(self, message: str):
        """Show error on login view."""
        self._login_error_label.Text = message
        self._login_error_label.Visible = True
    
    def _show_change_error(self, message: str):
        """Show error on change password view."""
        self._change_error_label.Text = message
        self._change_error_label.Visible = True
    
    def _on_login_click(self, sender, e):
        """Handle login button click."""
        self._clear_errors()
        
        username = self._username_input.Text.strip()
        password = self._password_input.Text
        
        if not username:
            self._show_login_error("Please enter your username or email")
            return
        
        if not password:
            self._show_login_error("Please enter your password")
            return
        
        # Disable button during login
        self._login_button.Enabled = False
        self._login_button.Text = "Signing in..."
        
        # Attempt login
        result = self.manager.login(username, password)
        
        # Re-enable button
        self._login_button.Enabled = True
        self._login_button.Text = "Sign In"
        
        if result.success and result.requires_password_change:
            self._show_view(LoginView.CHANGE_PASSWORD)
    
    def _on_change_password_click(self, sender, e):
        """Handle change password button click."""
        self._clear_errors()
        
        current_pw = self._current_pw_input.Text
        new_pw = self._new_pw_input.Text
        confirm_pw = self._confirm_pw_input.Text
        
        if not current_pw:
            self._show_change_error("Please enter your current password")
            return
        
        if not new_pw:
            self._show_change_error("Please enter a new password")
            return
        
        if new_pw != confirm_pw:
            self._show_change_error("Passwords do not match")
            return
        
        # Validate password
        validation = self.manager.validate_password(new_pw)
        if not validation.is_valid:
            self._show_change_error(validation.errors[0] if validation.errors else "Invalid password")
            return
        
        # Disable button during operation
        self._change_button.Enabled = False
        self._change_button.Text = "Changing..."
        
        # Attempt password change
        self.manager.change_password(current_pw, new_pw)
        
        # Re-enable button
        self._change_button.Enabled = True
        self._change_button.Text = "Change Password"
    
    def _on_reset_click(self, sender, e):
        """Handle reset password button click."""
        self._clear_errors()
        
        email = self._reset_email_input.Text.strip()
        
        if not email:
            self._reset_error_label.Text = "Please enter your email address"
            self._reset_error_label.Visible = True
            return
        
        # Disable button
        self._reset_button.Enabled = False
        self._reset_button.Text = "Sending..."
        
        success = self.manager.reset_password(email)
        
        # Re-enable button
        self._reset_button.Enabled = True
        self._reset_button.Text = "Send Reset Link"
        
        if success:
            self._reset_success_label.Visible = True
        else:
            self._reset_error_label.Text = "Failed to send reset email"
            self._reset_error_label.Visible = True
    
    def _on_new_password_changed(self, sender, e):
        """Update password strength indicator."""
        password = self._new_pw_input.Text
        
        if not password:
            self._strength_label.Text = ""
            self._strength_bar.Value = 0
            return
        
        validation = self.manager.validate_password(password)
        
        strength_names = {
            PasswordStrength.WEAK: ("Weak", self.COLORS['strength_weak']),
            PasswordStrength.FAIR: ("Fair", self.COLORS['strength_fair']),
            PasswordStrength.GOOD: ("Good", self.COLORS['strength_good']),
            PasswordStrength.STRONG: ("Strong", self.COLORS['strength_strong']),
            PasswordStrength.VERY_STRONG: ("Very Strong", self.COLORS['strength_strong']),
        }
        
        name, color = strength_names.get(validation.strength, ("Weak", self.COLORS['strength_weak']))
        self._strength_label.Text = f"Password strength: {name}"
        self._strength_label.ForeColor = color
        self._strength_bar.Value = validation.strength.value
    
    def _on_login_success(self, state):
        """Handle successful login."""
        self.LoginSuccess(state)
    
    def _on_login_failed(self, error):
        """Handle login failure."""
        self._show_login_error(error)
        self.LoginFailed(error)
    
    def _on_password_change_success(self):
        """Handle successful password change."""
        # Clear fields
        self._current_pw_input.Text = ""
        self._new_pw_input.Text = ""
        self._confirm_pw_input.Text = ""
        self._strength_bar.Value = 0
        self._strength_label.Text = ""
        
        # Show login view with success message
        self._show_view(LoginView.LOGIN)
        self._login_error_label.Text = "Password changed successfully!"
        self._login_error_label.ForeColor = self.COLORS['success']
        self._login_error_label.Visible = True
        
        self.PasswordChangeSuccess()
    
    def _on_password_change_failed(self, error):
        """Handle password change failure."""
        self._show_change_error(error)
        self.PasswordChangeFailed(error)
    
    # Public methods
    def show_login(self):
        """Show the login view."""
        self._show_view(LoginView.LOGIN)
    
    def show_change_password(self):
        """Show the change password view."""
        self._show_view(LoginView.CHANGE_PASSWORD)
    
    def show_reset_password(self):
        """Show the reset password view."""
        self._show_view(LoginView.RESET_PASSWORD)
    
    def clear(self):
        """Clear all input fields."""
        self._username_input.Text = ""
        self._password_input.Text = ""
        self._current_pw_input.Text = ""
        self._new_pw_input.Text = ""
        self._confirm_pw_input.Text = ""
        self._reset_email_input.Text = ""
        self._clear_errors()
    
    @property
    def remember_me(self) -> bool:
        """Get remember me checkbox state."""
        return self._remember_me.Checked
    
    @property
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self.manager.is_authenticated


# =============================================================================
# Example Usage
# =============================================================================
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    
    from winformpy.winformpy import Form, Panel, Label, DockStyle, Font, FontStyle
    from login_backend import LoginBackend, AuthResult, PasswordChangeResult, PasswordValidation, PasswordStrength
    from login_manager import LoginManager
    
    # =========================================================================
    # Demo Backend - Simulates authentication (replace with real implementation)
    # =========================================================================
    class DemoLoginBackend(LoginBackend):
        """Demo backend with hardcoded credentials for testing."""
        
        def __init__(self):
            # Demo users: username -> password
            self._users = {
                'admin': 'Admin123!',
                'user': 'User123!',
                'demo': 'Demo123!'
            }
        
        def authenticate(self, username: str, password: str) -> AuthResult:
            """Authenticate user against demo database."""
            if not username or not password:
                return AuthResult(False, "Username and password are required")
            
            if username not in self._users:
                return AuthResult(False, "Invalid username or password")
            
            if self._users[username] != password:
                return AuthResult(False, "Invalid username or password")
            
            return AuthResult(
                success=True,
                message="Login successful!",
                user_data={'username': username, 'role': 'admin' if username == 'admin' else 'user'}
            )
        
        def change_password(self, username: str, current_password: str, new_password: str) -> PasswordChangeResult:
            """Change user password."""
            # Verify current password
            if username not in self._users:
                return PasswordChangeResult(False, "User not found")
            
            if self._users[username] != current_password:
                return PasswordChangeResult(False, "Current password is incorrect")
            
            # Validate new password
            validation = self.validate_password(new_password)
            if not validation.is_valid:
                return PasswordChangeResult(False, validation.message)
            
            # Update password
            self._users[username] = new_password
            return PasswordChangeResult(True, "Password changed successfully!")
        
        def validate_password(self, password: str) -> PasswordValidation:
            """Validate password strength."""
            if len(password) < 8:
                return PasswordValidation(False, "Password must be at least 8 characters", PasswordStrength.WEAK)
            
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_digit = any(c.isdigit() for c in password)
            has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
            
            score = sum([has_upper, has_lower, has_digit, has_special])
            
            if score < 2:
                return PasswordValidation(False, "Password too weak. Add uppercase, numbers or symbols.", PasswordStrength.WEAK)
            elif score == 2:
                return PasswordValidation(True, "Password strength: Fair", PasswordStrength.FAIR)
            elif score == 3:
                return PasswordValidation(True, "Password strength: Good", PasswordStrength.GOOD)
            else:
                return PasswordValidation(True, "Password strength: Strong", PasswordStrength.STRONG)
        
        def request_password_reset(self, email: str) -> bool:
            """Simulate sending password reset email."""
            print(f"[Demo] Password reset email would be sent to: {email}")
            return True
        
        def logout(self, username: str) -> bool:
            """Logout user."""
            print(f"[Demo] User '{username}' logged out")
            return True
    
    # =========================================================================
    # Demo Application
    # =========================================================================
    def main():
        # Create main form
        form = Form()
        form.Text = "Login Panel Demo"
        form.Width = 450
        form.Height = 600
        form.StartPosition = 'CenterScreen'
        form.ApplyLayout()
        
        # Create backend and manager
        backend = DemoLoginBackend()
        manager = LoginManager(backend)
        
        # Create login panel
        login_panel = LoginPanel(form, props={
            'Dock': DockStyle.Fill
        }, manager=manager)
        
        # Handle login success
        def on_login_success(sender, args):
            user = args.get('user_data', {})
            print(f"✓ Login successful! User: {user.get('username')}, Role: {user.get('role')}")
            # Here you would typically:
            # - Hide login panel
            # - Show main application
            # - Store session token
        
        # Handle login failure
        def on_login_failed(sender, args):
            print(f"✗ Login failed: {args.get('message')}")
        
        # Handle password change
        def on_password_changed(sender, args):
            print(f"✓ Password changed successfully!")
            login_panel.show_login()  # Return to login view
        
        # Handle logout
        def on_logout(sender, args):
            print(f"→ User logged out")
            login_panel.clear()
            login_panel.show_login()
        
        # Connect events
        manager.on_login_success = on_login_success
        manager.on_login_failed = on_login_failed
        manager.on_password_changed = on_password_changed
        manager.on_logout = on_logout
        
        # Print demo instructions
        print("=" * 50)
        print("Login Panel Demo")
        print("=" * 50)
        print("\nDemo Credentials:")
        print("  - admin / Admin123!")
        print("  - user  / User123!")
        print("  - demo  / Demo123!")
        print("\nFeatures:")
        print("  - Click 'Forgot Password?' to test reset flow")
        print("  - After login, use manager.show_change_password()")
        print("=" * 50)
        
        # Run application
        form.ShowDialog()
    
    main()
