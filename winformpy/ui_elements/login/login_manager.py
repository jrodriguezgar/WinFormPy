"""
Login Manager - Service Layer
=============================

Manages authentication state and delegates operations to the external backend.

Architecture:
┌─────────────────────────────────────────────────────┐
│  UI Layer (LoginPanel / LoginForm)                  │
│    → Visual components and user interaction         │
└─────────────────────┬───────────────────────────────┘
                      │ uses
┌─────────────────────▼───────────────────────────────┐
│  Service Layer (LoginManager) ← YOU ARE HERE        │
│    → State management                               │
│    → Event handling                                 │
│    → Delegates to backend                           │
└─────────────────────┬───────────────────────────────┘
                      │ delegates
┌─────────────────────▼───────────────────────────────┐
│  ⚠️ EXTERNAL (not part of this project)             │
│  LoginBackend Implementation                        │
│    → Must be provided by YOU                        │
└─────────────────────────────────────────────────────┘
"""

from typing import Optional, Callable
from dataclasses import dataclass

try:
    from .login_backend import (
        LoginBackend, AuthResult, PasswordChangeResult, 
        PasswordValidation, PasswordStrength
    )
except ImportError:
    from login_backend import (
        LoginBackend, AuthResult, PasswordChangeResult,
        PasswordValidation, PasswordStrength
    )


@dataclass
class LoginState:
    """Current login state."""
    is_authenticated: bool = False
    user_id: Optional[str] = None
    username: Optional[str] = None
    display_name: Optional[str] = None
    email: Optional[str] = None
    token: Optional[str] = None
    requires_password_change: bool = False


class LoginManager:
    """
    Service layer for authentication operations.
    
    Manages login state and delegates authentication operations to an
    external backend. Provides events for UI components to respond to
    authentication state changes.
    
    Example:
        backend = MyAuthBackend()
        manager = LoginManager(backend)
        
        manager.LoginSuccess = lambda user: print(f"Welcome, {user.display_name}!")
        manager.LoginFailed = lambda error: print(f"Error: {error}")
        
        manager.login("username", "password")
    """
    
    def __init__(self, backend: Optional[LoginBackend] = None):
        """
        Initialize the LoginManager.
        
        Args:
            backend: Optional LoginBackend for authentication.
                     Must be provided for actual authentication to work.
        """
        self._backend = backend
        self._state = LoginState()
        
        # Event handlers
        self.LoginSuccess: Callable[[LoginState], None] = lambda state: None
        self.LoginFailed: Callable[[str], None] = lambda error: None
        self.LogoutComplete: Callable[[], None] = lambda: None
        self.PasswordChangeSuccess: Callable[[], None] = lambda: None
        self.PasswordChangeFailed: Callable[[str], None] = lambda error: None
        self.PasswordResetSent: Callable[[], None] = lambda: None
        self.PasswordResetFailed: Callable[[str], None] = lambda error: None
    
    @property
    def backend(self) -> Optional[LoginBackend]:
        """Get the current backend."""
        return self._backend
    
    @backend.setter
    def backend(self, value: Optional[LoginBackend]):
        """Set the authentication backend."""
        self._backend = value
    
    @property
    def has_backend(self) -> bool:
        """Check if a backend is configured."""
        return self._backend is not None
    
    @property
    def state(self) -> LoginState:
        """Get the current login state."""
        return self._state
    
    @property
    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated."""
        return self._state.is_authenticated
    
    @property
    def current_user(self) -> Optional[str]:
        """Get current username if authenticated."""
        return self._state.username if self._state.is_authenticated else None
    
    def login(self, username: str, password: str) -> AuthResult:
        """
        Attempt to authenticate a user.
        
        Args:
            username: User's username or email
            password: User's password
            
        Returns:
            AuthResult with authentication outcome
        """
        if not self._backend:
            error = "No authentication backend configured"
            self.LoginFailed(error)
            return AuthResult(success=False, error=error)
        
        result = self._backend.authenticate(username, password)
        
        if result.success:
            self._state = LoginState(
                is_authenticated=True,
                user_id=result.user_id,
                username=result.username,
                display_name=result.display_name,
                email=result.email,
                token=result.token,
                requires_password_change=result.requires_password_change
            )
            self.LoginSuccess(self._state)
        else:
            self._state = LoginState()
            self.LoginFailed(result.error or "Authentication failed")
        
        return result
    
    def logout(self) -> bool:
        """
        Logout the current user.
        
        Returns:
            True if logout was successful
        """
        if self._backend and self._state.token:
            self._backend.logout(self._state.token)
        
        self._state = LoginState()
        self.LogoutComplete()
        return True
    
    def change_password(self, old_password: str, new_password: str) -> PasswordChangeResult:
        """
        Change the current user's password.
        
        Args:
            old_password: Current password for verification
            new_password: New password to set
            
        Returns:
            PasswordChangeResult with outcome
        """
        if not self._backend:
            error = "No authentication backend configured"
            self.PasswordChangeFailed(error)
            return PasswordChangeResult(success=False, error=error)
        
        if not self._state.is_authenticated or not self._state.username:
            error = "User is not authenticated"
            self.PasswordChangeFailed(error)
            return PasswordChangeResult(success=False, error=error)
        
        # Validate new password
        validation = self._backend.validate_password(new_password)
        if not validation.is_valid:
            error = "; ".join(validation.errors)
            self.PasswordChangeFailed(error)
            return PasswordChangeResult(success=False, error=error)
        
        result = self._backend.change_password(
            self._state.username, 
            old_password, 
            new_password
        )
        
        if result.success:
            self._state.requires_password_change = False
            self.PasswordChangeSuccess()
        else:
            self.PasswordChangeFailed(result.error or "Password change failed")
        
        return result
    
    def reset_password(self, email: str) -> bool:
        """
        Request a password reset.
        
        Args:
            email: User's email address
            
        Returns:
            True if reset request was sent
        """
        if not self._backend:
            self.PasswordResetFailed("No authentication backend configured")
            return False
        
        if self._backend.reset_password(email):
            self.PasswordResetSent()
            return True
        else:
            self.PasswordResetFailed("Failed to send password reset")
            return False
    
    def validate_password(self, password: str) -> PasswordValidation:
        """
        Validate a password against requirements.
        
        Args:
            password: Password to validate
            
        Returns:
            PasswordValidation with results
        """
        if not self._backend:
            # Default validation if no backend
            return PasswordValidation(is_valid=len(password) >= 8)
        
        return self._backend.validate_password(password)
    
    def get_password_requirements(self) -> dict:
        """
        Get password requirements for display.
        
        Returns:
            Dictionary with requirement information
        """
        if not self._backend:
            return {'description': 'Password must be at least 8 characters'}
        
        return self._backend.get_password_requirements()
