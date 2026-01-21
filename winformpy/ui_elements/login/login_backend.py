"""
Login Backend Base Class
========================

This module defines the abstract interface for authentication backends.
The actual implementation must be provided externally by the application.

Architecture:
┌─────────────────────────────────────────────────────┐
│  LoginBackend (Abstract Base Class)                 │
│    → Interface for authentication operations        │
│    → Must be implemented externally                 │
└─────────────────────────────────────────────────────┘
                      │ implemented by
┌─────────────────────▼───────────────────────────────┐
│  ⚠️ EXTERNAL (not part of this project)             │
│  Your Authentication Backend                        │
│    → Database, LDAP, OAuth, REST API, etc.          │
└─────────────────────────────────────────────────────┘

Example implementation:
    class DatabaseLoginBackend(LoginBackend):
        def __init__(self, db_connection):
            self.db = db_connection
        
        def authenticate(self, username, password):
            user = self.db.query("SELECT * FROM users WHERE username=?", username)
            if user and verify_password(password, user.password_hash):
                return AuthResult(success=True, user_id=user.id, username=username)
            return AuthResult(success=False, error="Invalid credentials")
        
        def change_password(self, username, old_password, new_password):
            # Verify old password first
            auth = self.authenticate(username, old_password)
            if not auth.success:
                return PasswordChangeResult(success=False, error="Current password is incorrect")
            # Update password
            self.db.execute("UPDATE users SET password_hash=? WHERE username=?", 
                          hash_password(new_password), username)
            return PasswordChangeResult(success=True)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum


class PasswordStrength(Enum):
    """Password strength levels."""
    WEAK = 1
    FAIR = 2
    GOOD = 3
    STRONG = 4
    VERY_STRONG = 5


@dataclass
class AuthResult:
    """Result of an authentication attempt."""
    success: bool
    user_id: Optional[str] = None
    username: Optional[str] = None
    display_name: Optional[str] = None
    email: Optional[str] = None
    roles: List[str] = field(default_factory=list)
    token: Optional[str] = None
    error: Optional[str] = None
    requires_password_change: bool = False
    
    def __bool__(self):
        return self.success


@dataclass
class PasswordChangeResult:
    """Result of a password change attempt."""
    success: bool
    error: Optional[str] = None
    
    def __bool__(self):
        return self.success


@dataclass
class PasswordValidation:
    """Result of password validation."""
    is_valid: bool
    strength: PasswordStrength = PasswordStrength.WEAK
    errors: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    
    def __bool__(self):
        return self.is_valid


class LoginBackend(ABC):
    """
    Abstract base class for authentication backends.
    
    ⚠️ IMPORTANT: This class must be subclassed with a concrete implementation
    that connects to your actual authentication system (database, LDAP, OAuth, etc.)
    
    Required Methods:
        authenticate(username, password) -> AuthResult
        change_password(username, old_password, new_password) -> PasswordChangeResult
    
    Optional Methods (with default implementations):
        validate_password(password) -> PasswordValidation
        reset_password(email) -> bool
        logout(token) -> bool
        get_password_requirements() -> dict
    
    Example:
        class MyAuthBackend(LoginBackend):
            def authenticate(self, username, password):
                # Your authentication logic here
                if self._check_credentials(username, password):
                    return AuthResult(success=True, username=username)
                return AuthResult(success=False, error="Invalid credentials")
            
            def change_password(self, username, old_password, new_password):
                # Your password change logic here
                pass
    """
    
    @abstractmethod
    def authenticate(self, username: str, password: str) -> AuthResult:
        """
        Authenticate a user with username and password.
        
        Args:
            username: The user's username or email
            password: The user's password
            
        Returns:
            AuthResult with success=True and user data if authenticated,
            or success=False with error message if authentication failed.
        """
        pass
    
    @abstractmethod
    def change_password(self, username: str, old_password: str, new_password: str) -> PasswordChangeResult:
        """
        Change a user's password.
        
        Args:
            username: The user's username
            old_password: Current password for verification
            new_password: New password to set
            
        Returns:
            PasswordChangeResult with success=True if password was changed,
            or success=False with error message if change failed.
        """
        pass
    
    def validate_password(self, password: str) -> PasswordValidation:
        """
        Validate password strength and requirements.
        
        Override this method to implement custom password policies.
        Default implementation checks basic requirements.
        
        Args:
            password: Password to validate
            
        Returns:
            PasswordValidation with validation results and suggestions
        """
        errors = []
        suggestions = []
        
        # Check minimum length
        if len(password) < 8:
            errors.append("Password must be at least 8 characters")
        
        # Check for uppercase
        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")
            suggestions.append("Add an uppercase letter")
        
        # Check for lowercase
        if not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")
            suggestions.append("Add a lowercase letter")
        
        # Check for digit
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one number")
            suggestions.append("Add a number")
        
        # Check for special character
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in special_chars for c in password):
            suggestions.append("Add a special character for extra security")
        
        # Calculate strength
        score = 0
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if any(c.isupper() for c in password) and any(c.islower() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in special_chars for c in password):
            score += 1
        
        strength_map = {
            0: PasswordStrength.WEAK,
            1: PasswordStrength.WEAK,
            2: PasswordStrength.FAIR,
            3: PasswordStrength.GOOD,
            4: PasswordStrength.STRONG,
            5: PasswordStrength.VERY_STRONG
        }
        
        return PasswordValidation(
            is_valid=len(errors) == 0,
            strength=strength_map.get(score, PasswordStrength.WEAK),
            errors=errors,
            suggestions=suggestions
        )
    
    def reset_password(self, email: str) -> bool:
        """
        Initiate password reset for a user.
        
        Override to implement password reset functionality.
        Default implementation returns False (not implemented).
        
        Args:
            email: User's email address
            
        Returns:
            True if reset email was sent, False otherwise
        """
        return False
    
    def logout(self, token: Optional[str] = None) -> bool:
        """
        Logout the current user and invalidate any session/token.
        
        Override to implement session management.
        Default implementation returns True.
        
        Args:
            token: Optional session token to invalidate
            
        Returns:
            True if logout was successful
        """
        return True
    
    def get_password_requirements(self) -> dict:
        """
        Get password requirements for display to users.
        
        Override to customize requirements message.
        
        Returns:
            Dictionary with password requirements
        """
        return {
            'min_length': 8,
            'require_uppercase': True,
            'require_lowercase': True,
            'require_digit': True,
            'require_special': False,
            'description': 'Password must be at least 8 characters with uppercase, lowercase, and numbers.'
        }
