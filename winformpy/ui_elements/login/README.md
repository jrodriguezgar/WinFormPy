# 🔐 Login UI Element

A complete login/authentication component with support for external backends.

> ⚠️ **Architecture-agnostic**: This component delegates authentication operations to an **external backend** (`LoginBackend`). You provide the integration with your database, LDAP, OAuth, REST API, or any other authentication system.

> **📦 Component Structure**: This module provides:
> - `LoginPanel` - Embeddable panel for any Form/Panel
> - `LoginForm` - Standalone dialog that **uses LoginPanel internally**

## Quick Demo

Run the built-in demos to see the component in action:

```bash
# Embeddable panel demo (with mock backend)
python winformpy/ui_elements/login/login_panel.py

# Standalone form demo
python winformpy/ui_elements/login/login_ui.py
```

## 📖 Overview

The Login UI Element provides:

- ✅ Username/password login form
- ✅ Password change with strength indicator
- ✅ Password reset request
- ✅ Remember me option
- ✅ Modern, responsive design
- ✅ Event-driven architecture
- ✅ Pluggable authentication backend

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│  UI Layer                                           │
│  - LoginForm (standalone dialog)                    │
│  - LoginPanel (embeddable component)                │
│  - ChangePasswordForm (password change dialog)      │
│    → Uses LoginManager                              │
├─────────────────────────────────────────────────────┤
│  Service Layer                                      │
│  - LoginManager                                     │
│    → State management                               │
│    → Event handling                                 │
│    → Delegates to backend                           │
├─────────────────────────────────────────────────────┤
│  ⚠️ EXTERNAL (not part of this project)             │
│  LoginBackend Implementation                        │
│    → Must be provided by YOU                        │
│    → Database, LDAP, OAuth, REST API, etc.          │
└─────────────────────────────────────────────────────┘
```

---

## 📋 LoginBackend Contract (External)

The external backend must implement `LoginBackend` and provide authentication logic:

```python
from winformpy.ui_elements.login import LoginBackend, AuthResult, PasswordChangeResult

class MyAuthBackend(LoginBackend):
    def authenticate(self, username: str, password: str) -> AuthResult:
        """
        Authenticate a user.
        
        Returns:
            AuthResult with success=True and user data, or
            AuthResult with success=False and error message
        """
        # Your authentication logic here
        if self._verify_credentials(username, password):
            return AuthResult(
                success=True,
                user_id="123",
                username=username,
                display_name="John Doe",
                email="john@example.com"
            )
        return AuthResult(success=False, error="Invalid username or password")
    
    def change_password(self, username: str, old_password: str, new_password: str) -> PasswordChangeResult:
        """
        Change a user's password.
        
        Returns:
            PasswordChangeResult with success=True, or
            PasswordChangeResult with success=False and error message
        """
        # Verify old password first
        if not self._verify_credentials(username, old_password):
            return PasswordChangeResult(success=False, error="Current password is incorrect")
        
        # Update password
        self._update_password(username, new_password)
        return PasswordChangeResult(success=True)
```

### Required Methods

| Method | Description |
|--------|-------------|
| `authenticate(username, password)` | Verify credentials and return AuthResult |
| `change_password(username, old_pw, new_pw)` | Change password and return PasswordChangeResult |

### Optional Methods (with defaults)

| Method | Description | Default |
|--------|-------------|---------|
| `validate_password(password)` | Check password strength | Basic validation |
| `reset_password(email)` | Send password reset | Returns False |
| `logout(token)` | Invalidate session | Returns True |
| `get_password_requirements()` | Get requirements for display | Basic requirements |

---

## 📦 Components

| Component | Type | Description |
|-----------|------|-------------|
| `LoginBackend` | ABC | Abstract base class for backends (implement externally) |
| `LoginManager` | Service | State management and event handling |
| `LoginPanel` | Panel | Embeddable login component |
| `LoginForm` | Form | Standalone login dialog |
| `ChangePasswordForm` | Form | Standalone password change dialog |

### Data Classes

| Class | Description |
|-------|-------------|
| `AuthResult` | Result of authentication (success, user_id, username, etc.) |
| `PasswordChangeResult` | Result of password change (success, error) |
| `PasswordValidation` | Password validation results (is_valid, strength, errors) |
| `LoginState` | Current login state (is_authenticated, username, etc.) |
| `PasswordStrength` | Enum: WEAK, FAIR, GOOD, STRONG, VERY_STRONG |

---

## 🚀 Quick Start

### Using LoginForm (Standalone Dialog)

```python
from winformpy.ui_elements.login import LoginForm, LoginBackend, AuthResult, PasswordChangeResult

# Create your backend
class DatabaseBackend(LoginBackend):
    def __init__(self, db):
        self.db = db
    
    def authenticate(self, username, password):
        user = self.db.get_user(username)
        if user and verify_hash(password, user.password_hash):
            return AuthResult(
                success=True,
                user_id=str(user.id),
                username=user.username,
                display_name=user.full_name
            )
        return AuthResult(success=False, error="Invalid credentials")
    
    def change_password(self, username, old_password, new_password):
        auth = self.authenticate(username, old_password)
        if not auth.success:
            return PasswordChangeResult(success=False, error="Current password is incorrect")
        
        self.db.update_password(username, hash_password(new_password))
        return PasswordChangeResult(success=True)

# Show login dialog
backend = DatabaseBackend(my_database)
login = LoginForm(backend=backend)

if login.ShowDialog():
    user = login.authenticated_user
    print(f"Welcome, {user.display_name}!")
    # Continue to main application
else:
    print("Login cancelled")
```

### Using LoginPanel (Embedded)

```python
from winformpy import Form, Application, DockStyle
from winformpy.ui_elements.login import LoginPanel

class MainForm(Form):
    def __init__(self, backend):
        super().__init__()
        self.Text = "My Application"
        self.Width = 500
        self.Height = 600
        self.ApplyLayout()
        
        # Create login panel
        self.login_panel = LoginPanel(
            self,
            props={'Dock': DockStyle.Fill},
            backend=backend
        )
        
        # Handle login success
        self.login_panel.LoginSuccess = self.on_login_success
    
    def on_login_success(self, state):
        print(f"Logged in as {state.username}")
        # Hide login panel, show main content
        self.login_panel.Visible = False
        self.show_main_content()

backend = MyBackend()
app = MainForm(backend)
Application.Run(app)
```

### Customizing with Sub-Properties

LoginPanel supports sub-properties for configuring internal elements:

```python
from winformpy import Form, Application, DockStyle, Font, FontStyle
from winformpy.ui_elements.login import LoginPanel

form = Form({'Text': 'Custom Login', 'Width': 500, 'Height': 600})
form.ApplyLayout()

# Configure internal elements with sub-properties
login = LoginPanel(form, props={
    'Dock': DockStyle.Fill,
    'BackColor': '#F5F5F5',
    
    # Configure title label
    'Title': {
        'Text': 'Welcome Back',
        'Font': Font('Segoe UI', 28, FontStyle.Bold),
        'ForeColor': '#1A1A1A'
    },
    
    # Configure subtitle
    'Subtitle': {
        'Text': 'Please sign in to continue',
        'ForeColor': '#666666'
    },
    
    # Configure input fields
    'Inputs': {
        'Width': 380,
        'Height': 40,
        'BackColor': '#FFFFFF',
        'Font': Font('Segoe UI', 12)
    },
    
    # Configure sign-in button
    'Button': {
        'Text': 'Log In',
        'BackColor': '#107C10',  # Green
        'ForeColor': '#FFFFFF',
        'Height': 50,
        'Font': Font('Segoe UI', 12, FontStyle.Bold)
    },
    
    # Configure links (forgot password, etc.)
    'Links': {
        'ForeColor': '#0078D4'
    }
}, backend=my_backend)

Application.Run(form)
```

#### Available Sub-Properties

| Sub-Property | Keys | Description |
|--------------|------|-------------|
| `Title` | `Text`, `Font`, `ForeColor` | Main title label ("Sign In") |
| `Subtitle` | `Text`, `Font`, `ForeColor` | Subtitle text below title |
| `Inputs` | `Width`, `Height`, `BackColor`, `Font` | Username/password input fields |
| `Button` | `Text`, `BackColor`, `ForeColor`, `Height`, `Font` | Primary action button |
| `Links` | `ForeColor` | Link labels (forgot password, etc.) |

---

## 🔧 Backend Examples

### Database Backend (SQLite)

```python
import sqlite3
import hashlib
from winformpy.ui_elements.login import LoginBackend, AuthResult, PasswordChangeResult

class SQLiteBackend(LoginBackend):
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username, password):
        cursor = self.conn.execute(
            "SELECT id, username, display_name, email FROM users WHERE username=? AND password_hash=?",
            (username, self._hash_password(password))
        )
        row = cursor.fetchone()
        
        if row:
            return AuthResult(
                success=True,
                user_id=str(row[0]),
                username=row[1],
                display_name=row[2],
                email=row[3]
            )
        return AuthResult(success=False, error="Invalid username or password")
    
    def change_password(self, username, old_password, new_password):
        # Verify old password
        auth = self.authenticate(username, old_password)
        if not auth.success:
            return PasswordChangeResult(success=False, error="Current password is incorrect")
        
        # Update password
        self.conn.execute(
            "UPDATE users SET password_hash=? WHERE username=?",
            (self._hash_password(new_password), username)
        )
        self.conn.commit()
        return PasswordChangeResult(success=True)
```

### REST API Backend

```python
import requests
from winformpy.ui_elements.login import LoginBackend, AuthResult, PasswordChangeResult

class APIBackend(LoginBackend):
    def __init__(self, api_url):
        self.api_url = api_url
    
    def authenticate(self, username, password):
        response = requests.post(
            f"{self.api_url}/auth/login",
            json={"username": username, "password": password}
        )
        
        if response.status_code == 200:
            data = response.json()
            return AuthResult(
                success=True,
                user_id=data.get("user_id"),
                username=data.get("username"),
                display_name=data.get("display_name"),
                token=data.get("token")
            )
        
        error = response.json().get("error", "Authentication failed")
        return AuthResult(success=False, error=error)
    
    def change_password(self, username, old_password, new_password):
        response = requests.post(
            f"{self.api_url}/auth/change-password",
            json={
                "username": username,
                "old_password": old_password,
                "new_password": new_password
            }
        )
        
        if response.status_code == 200:
            return PasswordChangeResult(success=True)
        
        error = response.json().get("error", "Password change failed")
        return PasswordChangeResult(success=False, error=error)
```

### LDAP Backend

```python
import ldap
from winformpy.ui_elements.login import LoginBackend, AuthResult, PasswordChangeResult

class LDAPBackend(LoginBackend):
    def __init__(self, ldap_server, base_dn):
        self.ldap_server = ldap_server
        self.base_dn = base_dn
    
    def authenticate(self, username, password):
        try:
            conn = ldap.initialize(self.ldap_server)
            user_dn = f"uid={username},{self.base_dn}"
            conn.simple_bind_s(user_dn, password)
            
            # Get user info
            result = conn.search_s(user_dn, ldap.SCOPE_BASE)
            attrs = result[0][1]
            
            return AuthResult(
                success=True,
                username=username,
                display_name=attrs.get('cn', [b''])[0].decode(),
                email=attrs.get('mail', [b''])[0].decode()
            )
        except ldap.INVALID_CREDENTIALS:
            return AuthResult(success=False, error="Invalid credentials")
        except ldap.LDAPError as e:
            return AuthResult(success=False, error=str(e))
    
    def change_password(self, username, old_password, new_password):
        # LDAP password change implementation
        try:
            conn = ldap.initialize(self.ldap_server)
            user_dn = f"uid={username},{self.base_dn}"
            conn.simple_bind_s(user_dn, old_password)
            conn.passwd_s(user_dn, old_password, new_password)
            return PasswordChangeResult(success=True)
        except ldap.INVALID_CREDENTIALS:
            return PasswordChangeResult(success=False, error="Current password is incorrect")
        except ldap.LDAPError as e:
            return PasswordChangeResult(success=False, error=str(e))
```

---

## 🎨 Customization

### Custom Colors

```python
# Override panel colors
LoginPanel.COLORS = {
    'background': '#1E1E1E',      # Dark background
    'primary': '#0EA5E9',          # Custom accent color
    'primary_hover': '#0284C7',
    'text': '#FFFFFF',
    'text_secondary': '#A3A3A3',
    'border': '#404040',
    'error': '#EF4444',
    'success': '#22C55E',
    'input_bg': '#2D2D2D',
    'input_border': '#525252',
    'strength_weak': '#EF4444',
    'strength_fair': '#F59E0B',
    'strength_good': '#22C55E',
    'strength_strong': '#0EA5E9',
}
```

### Custom Password Validation

```python
class StrictBackend(LoginBackend):
    def validate_password(self, password):
        errors = []
        suggestions = []
        
        if len(password) < 12:
            errors.append("Password must be at least 12 characters")
        
        if not any(c.isupper() for c in password):
            errors.append("Must contain uppercase letter")
        
        if not any(c.islower() for c in password):
            errors.append("Must contain lowercase letter")
        
        if not any(c.isdigit() for c in password):
            errors.append("Must contain a number")
        
        if not any(c in "!@#$%^&*" for c in password):
            errors.append("Must contain special character (!@#$%^&*)")
        
        # Custom: no common words
        common = ['password', '123456', 'qwerty']
        if any(word in password.lower() for word in common):
            errors.append("Password contains common pattern")
        
        return PasswordValidation(
            is_valid=len(errors) == 0,
            strength=self._calculate_strength(password),
            errors=errors,
            suggestions=suggestions
        )
```

---

## 📚 Events

### LoginPanel / LoginForm Events

| Event | Parameters | Description |
|-------|------------|-------------|
| `LoginSuccess` | `LoginState` | Fired on successful login |
| `LoginFailed` | `str (error)` | Fired on login failure |
| `PasswordChangeSuccess` | None | Fired on successful password change |
| `PasswordChangeFailed` | `str (error)` | Fired on password change failure |
| `ForgotPasswordClick` | None | Fired when forgot password is clicked |

### LoginManager Events

| Event | Parameters | Description |
|-------|------------|-------------|
| `LoginSuccess` | `LoginState` | Fired on successful login |
| `LoginFailed` | `str (error)` | Fired on login failure |
| `LogoutComplete` | None | Fired after logout |
| `PasswordChangeSuccess` | None | Fired on successful password change |
| `PasswordChangeFailed` | `str (error)` | Fired on password change failure |
| `PasswordResetSent` | None | Fired when reset email is sent |
| `PasswordResetFailed` | `str (error)` | Fired on reset failure |

---

## 📁 File Structure

```
login/
├── __init__.py          # Exports
├── login_backend.py     # LoginBackend ABC, data classes
├── login_manager.py     # LoginManager service
├── login_panel.py       # LoginPanel embeddable component
├── login_ui.py          # LoginForm, ChangePasswordForm
└── README.md            # This file
```
