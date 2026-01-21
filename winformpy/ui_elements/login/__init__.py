"""
Login UI Element
================

A complete login/authentication component with external backend support.

Components:
    - LoginBackend: Abstract base class for authentication backends (EXTERNAL)
    - LoginManager: Service layer for authentication operations
    - LoginPanel: Embeddable login panel
    - LoginForm: Standalone login dialog
    - ChangePasswordForm: Standalone change password dialog

Data Classes:
    - AuthResult: Result of authentication attempt
    - PasswordChangeResult: Result of password change attempt
    - PasswordValidation: Password validation results
    - LoginState: Current authentication state
    - PasswordStrength: Password strength levels

Example:
    from winformpy.ui_elements.login import (
        LoginForm, LoginBackend, AuthResult, PasswordChangeResult
    )
    
    # Create your backend (EXTERNAL - not part of WinFormPy)
    class MyAuthBackend(LoginBackend):
        def authenticate(self, username, password):
            # Your authentication logic
            if check_credentials(username, password):
                return AuthResult(success=True, username=username)
            return AuthResult(success=False, error="Invalid credentials")
        
        def change_password(self, username, old_pw, new_pw):
            # Your password change logic
            if update_password(username, old_pw, new_pw):
                return PasswordChangeResult(success=True)
            return PasswordChangeResult(success=False, error="Failed to change password")
    
    # Use with LoginForm
    backend = MyAuthBackend()
    login = LoginForm(backend=backend)
    
    if login.ShowDialog():
        user = login.authenticated_user
        print(f"Welcome, {user.display_name}!")
"""

from .login_backend import (
    LoginBackend,
    AuthResult,
    PasswordChangeResult,
    PasswordValidation,
    PasswordStrength
)

from .login_manager import (
    LoginManager,
    LoginState
)

from .login_panel import (
    LoginPanel,
    LoginView
)

from .login_ui import (
    LoginForm,
    ChangePasswordForm
)

__all__ = [
    # Backend (Abstract - must be implemented externally)
    'LoginBackend',
    
    # Data classes
    'AuthResult',
    'PasswordChangeResult',
    'PasswordValidation',
    'PasswordStrength',
    'LoginState',
    
    # Service layer
    'LoginManager',
    
    # UI Components
    'LoginPanel',
    'LoginForm',
    'ChangePasswordForm',
    'LoginView',
]
