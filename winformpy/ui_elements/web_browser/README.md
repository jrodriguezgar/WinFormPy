# 🌐 Web Browser Module

## 📖 Overview

**Web Browser Module** provides a WinForms-style WebBrowser control using tkinterweb as the rendering engine. Based on `System.Windows.Forms.WebBrowser` from Microsoft .NET.

> ✅ **Self-contained**: This component does NOT require an external backend. It uses `tkinterweb` for HTML rendering.

> **📦 Component Structure**: This module provides:
> - `WebBrowserPanel` - Embeddable panel for any Form/Panel
> - `WebBrowserUI` - Full browser with tabs that **uses WebBrowserPanel internally** (access via `.CurrentTab` property)

## Quick Demo

Run the built-in demos to see the component in action:

```bash
# Panel with navigation bar demo
python winformpy/ui_elements/web_browser/web_browser_panel.py

# Full browser with tabs demo
python winformpy/ui_elements/web_browser/web_browser_ui.py
```

### 🎯 Purpose

- **HTML Rendering**: Display web pages and HTML content
- **Navigation Controls**: Built-in back/forward/refresh/home functionality
- **WinForms API**: Familiar .NET-style programming model
- **Embeddable Panel**: Ready-to-use panel with navigation bar and status bar

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│  Visual Layer                                       │
│  - WebBrowser (Core Control - lightweight)          │
│  - WebBrowserPanel (Panel with nav bar/status bar)  │
└─────────────────────┬───────────────────────────────┘
                      │ uses
┌─────────────────────▼───────────────────────────────┐
│  Rendering Engine                                   │
│  - tkinterweb (pip install tkinterweb)              │
│    → Provides HTML5/CSS rendering                   │
└─────────────────────────────────────────────────────┘
```

---

## 📦 Installation

```bash
pip install tkinterweb
```

---

## 📋 Components

### WebBrowser (Core Control)

Lightweight browser control that can be embedded directly in any Form or Panel.

```python
from winformpy.ui_elements.web_browser import WebBrowser

# Add to a form
browser = WebBrowser(form, {'Dock': DockStyle.Fill})
browser.Navigate("https://www.python.org")
```

### WebBrowserPanel (Complete Panel)

Full-featured panel with navigation bar, status bar, and browser control.

```python
from winformpy.ui_elements.web_browser import WebBrowserPanel

# Add to a form
panel = WebBrowserPanel(form, {'Dock': DockStyle.Fill})
panel.Navigate("https://www.google.com")
```

---

## 📊 API Reference

### WebBrowser Properties

| Property          | Type                     | Description                              |
| ----------------- | ------------------------ | ---------------------------------------- |
| `Url`           | `str`                  | Gets or sets the current URL             |
| `DocumentTitle` | `str`                  | Gets the title of the current document   |
| `DocumentText`  | `str`                  | Gets or sets the HTML content            |
| `CanGoBack`     | `bool`                 | Returns `True` if can navigate back    |
| `CanGoForward`  | `bool`                 | Returns `True` if can navigate forward |
| `ReadyState`    | `WebBrowserReadyState` | Gets the loading state                   |
| `IsBusy`        | `bool`                 | Returns `True` if loading              |
| `HomeUrl`       | `str`                  | Gets or sets the home page URL           |

### WebBrowser Methods

| Method                       | Parameters                       | Description                   |
| ---------------------------- | -------------------------------- | ----------------------------- |
| `Navigate(url)`            | `url: str`                     | Navigate to the specified URL |
| `GoBack()`                 | —                               | Navigate to previous page     |
| `GoForward()`              | —                               | Navigate to next page         |
| `Refresh()`                | —                               | Reload current page           |
| `Stop()`                   | —                               | Stop loading                  |
| `GoHome()`                 | —                               | Navigate to home page         |
| `LoadHtml(html, base_url)` | `html: str`, `base_url: str` | Load HTML content directly    |
| `Focus()`                  | —                               | Set focus to the control      |
| `Dispose()`                | —                               | Release resources             |

### WebBrowser Events

| Event                    | EventArgs                                | Description                |
| ------------------------ | ---------------------------------------- | -------------------------- |
| `Navigating`           | `WebBrowserNavigatingEventArgs`        | Before navigation begins   |
| `Navigated`            | `WebBrowserNavigatedEventArgs`         | After navigation completes |
| `DocumentCompleted`    | `WebBrowserDocumentCompletedEventArgs` | Document fully loaded      |
| `DocumentTitleChanged` | `EventArgs`                            | Document title changed     |
| `ProgressChanged`      | `WebBrowserProgressChangedEventArgs`   | Loading progress changed   |

---

### WebBrowserPanel Properties

Includes all WebBrowser properties plus:

| Property                  | Type           | Default                    | Description                              |
| ------------------------- | -------------- | -------------------------- | ---------------------------------------- |
| `ShowNavigationBar`     | `bool`       | `True`                   | Show/hide the entire navigation bar      |
| `ShowStatusBar`         | `bool`       | `True`                   | Show/hide the status bar                 |
| `ShowNavigationButtons` | `bool`       | `True`                   | Show/hide back/forward buttons           |
| `ShowRefreshButton`     | `bool`       | `True`                   | Show/hide the refresh button             |
| `ShowHomeButton`        | `bool`       | `True`                   | Show/hide the home button                |
| `ShowAddressBar`        | `bool`       | `True`                   | Show/hide the URL bar and Go button      |
| `HomeUrl`               | `str`        | `https://www.google.com` | Home page URL                            |
| `Browser`               | `WebBrowser` | —                         | Access the underlying WebBrowser control |

### WebBrowserPanel Methods

Includes all WebBrowser methods plus:

| Method             | Parameters | Description                      |
| ------------------ | ---------- | -------------------------------- |
| `GoHome()`       | —         | Navigate to the home URL         |
| `Focus()`        | —         | Set focus to the URL bar         |
| `FocusBrowser()` | —         | Set focus to the browser control |

---

## 🔧 WebBrowserReadyState Enum

```python
class WebBrowserReadyState:
    Uninitialized = 0  # Control not initialized
    Loading = 1        # Loading document
    Loaded = 2         # Some data loaded
    Interactive = 3    # User can interact
    Complete = 4       # Fully loaded
```

---

## 💡 Usage Examples

### Basic Browser in a Form

```python
from winformpy.winformpy import Form, DockStyle
from winformpy.ui_elements.web_browser import WebBrowser

form = Form({'Text': 'Simple Browser', 'Width': 1024, 'Height': 768})
form.ApplyLayout()

browser = WebBrowser(form, {'Dock': DockStyle.Fill})
browser.Navigate("https://www.python.org")

form.Run()
```

### Full Browser Panel with Events

```python
from winformpy.winformpy import Form, DockStyle
from winformpy.ui_elements.web_browser import WebBrowserPanel

form = Form({'Text': 'Web Browser', 'Width': 1024, 'Height': 768})
form.ApplyLayout()

panel = WebBrowserPanel(form, {
    'Dock': DockStyle.Fill,
    'HomeUrl': 'https://www.github.com'
})

# Update window title when page title changes
def on_title_changed(sender, e):
    title = panel.DocumentTitle
    form.Text = f"Web Browser - {title}" if title else "Web Browser"

panel.DocumentTitleChanged = on_title_changed

# Navigate to home
panel.GoHome()

form.Run()
```

### Load HTML Content Directly

```python
from winformpy.ui_elements.web_browser import WebBrowser

browser = WebBrowser(form, {'Dock': DockStyle.Fill})

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Hello WinFormPy</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; padding: 20px; }
        h1 { color: #0066cc; }
    </style>
</head>
<body>
    <h1>Welcome to WinFormPy!</h1>
    <p>This HTML content was loaded directly.</p>
</body>
</html>
"""

browser.LoadHtml(html)
```

### Customizing Navigation Bar Visibility

```python
from winformpy.ui_elements.web_browser import WebBrowserPanel

# Create minimal browser (no navigation controls)
panel = WebBrowserPanel(form, {
    'Dock': DockStyle.Fill,
    'ShowNavigationButtons': False,
    'ShowRefreshButton': False,
    'ShowHomeButton': False,
    'ShowAddressBar': False,
    'ShowStatusBar': False
})

# Or toggle visibility dynamically
panel.ShowNavigationBar = True  # Show navigation bar
panel.ShowStatusBar = True      # Show status bar

# Selective controls
panel.ShowNavigationButtons = True  # Back/Forward
panel.ShowRefreshButton = True      # Refresh button
panel.ShowHomeButton = False        # Hide home button
panel.ShowAddressBar = True         # URL bar + Go button
```

### Handling Navigation Events

```python
def on_navigating(sender, e):
    print(f"Navigating to: {e.Url}")
    # Cancel navigation if needed:
    # e.Cancel = True

def on_navigated(sender, e):
    print(f"Navigated to: {e.Url}")

def on_document_completed(sender, e):
    print(f"Document loaded: {e.Url}")
    print(f"Title: {sender.DocumentTitle}")

panel.Navigating = on_navigating
panel.Navigated = on_navigated
panel.DocumentCompleted = on_document_completed
```

---

## 🖼️ Visual Layout

### WebBrowserPanel Structure

```
┌─────────────────────────────────────────────────────────────┐
│  Navigation Bar (ShowNavigationBar)                         │
│  ┌───┬───┬───┬───┬──────────────────────────────┬─────┐    │
│  │ ◀ │ ▶ │ ↻ │ 🏠│  https://example.com         │ Go  │    │
│  └───┴───┴───┴───┴──────────────────────────────┴─────┘    │
│   └─ ShowNavigationButtons   └── ShowAddressBar ──────┘    │
│            └── ShowRefreshButton                            │
│                 └── ShowHomeButton                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    WebBrowser                               │
│                  (Dock: Fill)                               │
│                                                             │
│                 [ Web Content ]                             │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  Status Bar (ShowStatusBar)                                 │
│  Ready                                              100%    │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚠️ Important Notes

1. **tkinterweb Required**: The module requires `tkinterweb` to be installed:

   ```bash
   pip install tkinterweb
   ```
2. **ApplyLayout() Required**: Always call `form.ApplyLayout()` before adding browser controls:

   ```python
   form = Form({'Width': 1024, 'Height': 768})
   form.ApplyLayout()  # MUST be called first!
   browser = WebBrowser(form, {'Dock': DockStyle.Fill})
   ```
3. **Dock Order Matters**: The WebBrowser should typically use `Dock: Fill` and be added after any `Top`, `Left`, `Right`, or `Bottom` docked controls.
4. **Events with Chained Handlers**: When setting events on `WebBrowserPanel`, the internal UI update handlers are automatically chained with your custom handlers.

---

## 📁 Module Files

| File                     | Description                          |
| ------------------------ | ------------------------------------ |
| `__init__.py`          | Module exports                       |
| `web_browser_ui.py`    | Re-exports WebBrowser from winformpy |
| `web_browser_panel.py` | WebBrowserPanel implementation       |
