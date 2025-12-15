# MaskedTextBox and MaskedTextProvider - Complete Implementation Guide

## Overview

The `MaskedTextBox` control provides a text box with input mask validation, similar to Windows Forms `MaskedTextBox`. It restricts user input to match a specific pattern defined by a mask string. The underlying `MaskedTextProvider` class handles the parsing, validation, and formatting of the masked text.

## MaskedTextProvider Class

The `MaskedTextProvider` is the core engine that manages mask parsing and text validation. It implements functionality equivalent to `System.ComponentModel.MaskedTextProvider` from .NET Framework.

### Mask Characters

The following mask characters are supported:

| Character                                               | Description                  | Required                | Example                  |
| ------------------------------------------------------- | ---------------------------- | ----------------------- | ------------------------ |
| `0`                                                   | Digit (0-9)                  | Yes                     | Phone:`(000) 000-0000` |
| `9`                                                   | Digit or space               | No                      | Optional code:`999`    |
| `#`                                                   | Digit, space, or sign (+/-)  | No                      | Signed number:`###`    |
| `L`                                                   | Letter (a-z, A-Z)            | Yes                     | Initials:`LL`          |
| `?`                                                   | Letter (a-z, A-Z)            | No                      | Optional middle:`?`    |
| `&`                                                   | Any printable character      | Yes                     | Code:`&&&&`            |
| `C`                                                   | Any printable character      | No                      | Optional char:`CCC`    |
| `A`                                                   | Alphanumeric (a-z, A-Z, 0-9) | Yes                     | Product code:`AAA-000` |
| `a`                                                   | Alphanumeric (a-z, A-Z, 0-9) | No                      | Optional code:`aaa`    |
| `.`                                                   | Decimal placeholder          | Literal                 | Price:`0.00`           |
| `,`                                                   | Thousands separator          | Literal                 | Number:`0,000`         |
| `:`                                                   | Time separator               | Literal                 | Time:`00:00`           |
| `/`                                                   | Date separator               | Literal                 | Date:`00/00/0000`      |
| `$` | Currency symbol | Literal | Currency: `$0.00` |                              |                         |                          |
| `<`                                                   | Convert to lowercase         | Modifier                | Email:`<LLLL`          |
| `>`                                                   | Convert to uppercase         | Modifier                | Code:`>aaaa`           |
| `                                                       | `                            | Disable case conversion | Modifier                 |
| `\`                                                   | Escape next character        | Escape                  | Literal 0:`\0`         |

### Constructor

```python
provider = MaskedTextProvider(
    mask="(000) 000-0000",
    culture=None,
    allow_prompt_as_input=True,
    prompt_char='_',
    password_char=None,
    restrict_to_ascii=False
)
```

**Parameters:**

- `mask`: The mask string defining the input format
- `culture`: Culture info (reserved for future implementation)
- `allow_prompt_as_input`: Whether prompt character can be entered as valid input
- `prompt_char`: Character displayed for empty required positions (default: `_`)
- `password_char`: Character to display instead of actual input (for passwords)
- `restrict_to_ascii`: Restrict input to ASCII characters only

### Properties

| Property               | Type | Description                                              |
| ---------------------- | ---- | -------------------------------------------------------- |
| `Mask`               | str  | Gets the input mask string                               |
| `Length`             | int  | Gets the total length of the mask                        |
| `PromptChar`         | str  | Gets the prompt character                                |
| `PasswordChar`       | str  | Gets the password character                              |
| `AllowPromptAsInput` | bool | Gets whether prompt char is allowed as input             |
| `MaskCompleted`      | bool | True if all required positions are filled                |
| `MaskFull`           | bool | True if all positions (required and optional) are filled |

### Methods

#### Text Manipulation

```python
# Add character at next available position
success = provider.Add('5')

# Insert character at specific position
success = provider.InsertAt('5', position=0)

# Remove character at position
success = provider.RemoveAt(position=3)

# Replace character at position
success = provider.Replace('7', position=3)

# Set entire text string
success = provider.Set("1234567890")

# Clear all input positions
provider.Clear()
```

#### Text Retrieval

```python
# Get formatted text with options
text = provider.ToString(include_prompt=True, include_literals=True)

# Get display text (with prompts and literals)
display_text = provider.ToDisplayString()
```

#### Validation and Navigation

```python
# Verify if string is valid for mask
is_valid = provider.VerifyString("(555) 123-4567")

# Find next/previous editable position
next_pos = provider.FindEditPositionFrom(position=5, forward=True)
prev_pos = provider.FindEditPositionFrom(position=5, forward=False)

# Check if position is editable
is_editable = provider.IsEditPosition(position=3)
```

## MaskedTextBox Control

The `MaskedTextBox` control extends `TextBox` with mask validation capabilities.

### Basic Usage

#### Option 1: Property Assignment

```python
from winformpy import Form, MaskedTextBox

form = Form()

# Phone number input
txt_phone = MaskedTextBox(form)
txt_phone.Mask = "(000) 000-0000"
txt_phone.Left = 20
txt_phone.Top = 20
txt_phone.Width = 200

form.Show()
```

#### Option 2: Dictionary Initialization

```python
txt_phone = MaskedTextBox(form, {
    'Mask': '(000) 000-0000',
    'Left': 20,
    'Top': 20,
    'Width': 200,
    'PromptChar': '_',
    'BeepOnError': True
})
```

### Common Mask Examples

#### Phone Number (US)

```python
txt_phone.Mask = "(000) 000-0000"
# Input: (555) 123-4567
```

#### Social Security Number

```python
txt_ssn.Mask = "000-00-0000"
txt_ssn.PasswordChar = '*'
# Input: ***-**-****
```

#### Date (MM/DD/YYYY)

```python
txt_date.Mask = "00/00/0000"
# Input: 12/09/2025
```

#### Time (HH:MM)

```python
txt_time.Mask = "00:00"
# Input: 14:30
```

#### ZIP Code

```python
txt_zip.Mask = "00000-9999"
# Input: 12345-6789 or 12345____
```

#### Credit Card

```python
txt_card.Mask = "0000-0000-0000-0000"
# Input: 1234-5678-9012-3456
```

#### Product Code (Mixed)

```python
txt_product.Mask = ">LLL-000"
# Input: ABC-123 (letters forced uppercase)
```

#### Email Prefix (Lowercase)

```python
txt_email.Mask = "<LLLLLLLL"
# Input: username (forced lowercase)
```

### Properties

| Property                      | Type | Default           | Description                                |
| ----------------------------- | ---- | ----------------- | ------------------------------------------ |
| `Mask`                      | str  | ""                | The input mask pattern                     |
| `Text`                      | str  | ""                | The actual text value                      |
| `PromptChar`                | str  | '_'               | Character shown for empty positions        |
| `PasswordChar`              | str  | None              | Character shown instead of input           |
| `UseSystemPasswordChar`     | bool | False             | Use system password character              |
| `BeepOnError`               | bool | False             | Beep when invalid character entered        |
| `AllowPromptAsInput`        | bool | False             | Allow prompt character as valid input      |
| `CutCopyMaskFormat`         | str  | 'IncludeLiterals' | Format for clipboard operations            |
| `TextMaskFormat`            | str  | 'IncludeLiterals' | Format for Text property output            |
| `InsertKeyMode`             | str  | 'Insert'          | Insert or overwrite mode                   |
| `AsciiOnly`                 | bool | False             | Restrict to ASCII characters only          |
| `ResetOnPrompt`             | bool | True              | Reset on prompt character entry            |
| `ResetOnSpace`              | bool | True              | Reset on space entry                       |
| `SkipLiterals`              | bool | True              | Auto-skip literal characters               |
| `ValidatingType`            | type | None              | Type for validation on blur                |
| `RejectInputOnFirstFailure` | bool | False             | Reject entire input on first error         |
| `MaskFull`                  | bool | Read-only         | All positions filled                       |
| `MaskCompleted`             | bool | Read-only         | All required positions filled              |

### Events

```python
# Fired when invalid input is rejected
txt_masked.MaskInputRejected = lambda sender, e: print("Invalid input!")

# Fired when type validation completes
txt_masked.TypeValidationCompleted = lambda sender, e: print("Validated!")

# Fired when mask changes
txt_masked.MaskChanged = lambda sender, e: print("Mask changed!")

# Fired when overwrite mode changes
txt_masked.IsOverwriteModeChanged = lambda sender, e: print("Mode changed!")
```

### Advanced Examples

#### Custom Validation with Events

```python
from winformpy import Form, MaskedTextBox, Label, Button

form = Form()
form.Text = "Phone Number Entry"
form.Width = 350
form.Height = 200

# Label
lbl = Label(form, {
    'Text': 'Enter your phone number:',
    'Left': 20,
    'Top': 20,
    'Width': 300
})

# MaskedTextBox
txt_phone = MaskedTextBox(form, {
    'Mask': '(000) 000-0000',
    'Left': 20,
    'Top': 50,
    'Width': 200,
    'PromptChar': '_',
    'BeepOnError': True
})

# Result label
lbl_result = Label(form, {
    'Text': '',
    'Left': 20,
    'Top': 80,
    'Width': 300,
    'ForeColor': 'green'
})

# Validation on input rejected
def on_input_rejected(sender, e):
    lbl_result.Text = "Invalid character entered!"
    lbl_result.ForeColor = 'red'

txt_phone.MaskInputRejected = on_input_rejected

# Button to validate
def on_validate_click(sender, e):
    if txt_phone.MaskCompleted:
        lbl_result.Text = f"Valid phone: {txt_phone.Text}"
        lbl_result.ForeColor = 'green'
    else:
        lbl_result.Text = "Please complete the phone number"
        lbl_result.ForeColor = 'orange'

btn_validate = Button(form, {
    'Text': 'Validate',
    'Left': 20,
    'Top': 110,
    'Width': 100,
    'Height': 30
})
btn_validate.Click = on_validate_click

form.Show()
```

#### Multiple Mask Formats

```python
from winformpy import Form, MaskedTextBox, Label, ComboBox

form = Form()
form.Text = "Mask Format Demo"
form.Width = 400
form.Height = 300

masks = {
    'Phone (US)': '(000) 000-0000',
    'SSN': '000-00-0000',
    'Date (US)': '00/00/0000',
    'Date (ISO)': '0000-00-00',
    'Time (24h)': '00:00:00',
    'ZIP+4': '00000-9999',
    'Credit Card': '0000-0000-0000-0000',
    'Product Code': '>LLL-000',
}

# ComboBox to select mask
combo = ComboBox(form, {
    'Left': 20,
    'Top': 20,
    'Width': 200,
    'Items': list(masks.keys())
})
combo.SelectedIndex = 0

# MaskedTextBox
txt_masked = MaskedTextBox(form, {
    'Mask': masks['Phone (US)'],
    'Left': 20,
    'Top': 60,
    'Width': 250,
    'Font': ('Courier New', 12)
})

# Info label
lbl_info = Label(form, {
    'Text': 'Mask: (000) 000-0000',
    'Left': 20,
    'Top': 100,
    'Width': 350,
    'Font': ('Consolas', 10),
    'ForeColor': 'blue'
})

# Status label
lbl_status = Label(form, {
    'Text': 'Status: Empty',
    'Left': 20,
    'Top': 130,
    'Width': 350
})

def on_mask_changed(sender, e):
    selected = combo.SelectedItem
    if selected and selected in masks:
        txt_masked.Mask = masks[selected]
        lbl_info.Text = f"Mask: {masks[selected]}"
        lbl_status.Text = 'Status: Empty'

combo.SelectedIndexChanged = on_mask_changed

def on_text_changed(sender, e):
    if txt_masked.MaskFull:
        status = "Status: Complete (all positions filled)"
        color = 'green'
    elif txt_masked.MaskCompleted:
        status = "Status: Valid (required positions filled)"
        color = 'darkgreen'
    else:
        status = "Status: Incomplete"
        color = 'orange'
  
    lbl_status.Text = status
    lbl_status.ForeColor = color

txt_masked.TextChanged = on_text_changed

form.Show()
```

#### Password Entry with Mask

```python
txt_password = MaskedTextBox(form, {
    'Mask': '&&&&&&&&',  # 8 required characters
    'Left': 20,
    'Top': 20,
    'Width': 200,
    'UseSystemPasswordChar': True,
    'BeepOnError': True
})
```

## Implementation Details

### Internal Architecture

1. **Mask Parsing**: The mask string is parsed into a list of structured elements, each containing:

   - `type`: 'input' or 'literal'
   - `validator`: validation function name (for input elements)
   - `required`: whether the position must be filled
   - `case`: case conversion mode ('upper', 'lower', None)
   - `char`: literal character (for literal elements)
2. **Character Buffer**: An internal buffer maintains the current state of each position, storing either:

   - User input (validated)
   - Prompt character (for empty input positions)
   - Literal character (for mask literals)
3. **Event Handling**: The control binds to keyboard events to:

   - Validate input characters before acceptance
   - Auto-skip literal positions
   - Handle backspace/delete with mask awareness
   - Manage focus in/out behavior
4. **Display Management**: Text display respects:

   - Password character masking
   - Prompt character visibility
   - Literal inclusion/exclusion
   - Case conversion

### Case Conversion

Case conversion modifiers affect all subsequent input positions until changed:

```python
# Force uppercase
mask = ">LLLL"  # Input: "test" → Display: "TEST"

# Force lowercase  
mask = "<LLLL"  # Input: "TEST" → Display: "test"

# Mixed case
mask = ">LL|ll"  # Input: "TeSt" → Display: "TEst"
```

### Literal Characters

Any character not recognized as a mask placeholder is treated as a literal:

```python
mask = "(000) 000-0000"
# Literals: '(', ')', ' ', ' ', '-'
# These are auto-filled and cannot be edited
```

To use a mask character as a literal, escape it:

```python
mask = "\\0\\0\\0"  # Three literal '0' characters
```

## Best Practices

1. **Choose Appropriate Masks**: Use required (`0`, `L`, `&`, `A`) for mandatory fields, optional (`9`, `?`, `C`, `a`) for flexible inputs
2. **Provide Visual Feedback**: Use `BeepOnError` and/or `MaskInputRejected` event to inform users of invalid input
3. **Validate on Submit**: Check `MaskCompleted` before accepting form data
4. **Use Appropriate Prompt Characters**: Choose prompt chars that won't confuse users (avoid characters that might be valid input)
5. **Consider Accessibility**: Password fields should use `PasswordChar` or `UseSystemPasswordChar`
6. **Test Edge Cases**: Test with incomplete data, rapid typing, paste operations

## Limitations and Considerations

- Clipboard operations (copy/paste) are simplified compared to .NET implementation
- Culture-specific formatting (decimal/thousands separators) is not fully implemented
- Some advanced .NET features like `ValidatingType` parsing are placeholders
- Performance may vary with very long masks or rapid input

## Compatibility

The implementation aims for API compatibility with:

- `System.Windows.Forms.MaskedTextBox` (.NET Framework)
- `System.ComponentModel.MaskedTextProvider` (.NET Framework)

Most common use cases are fully supported, with some advanced features reserved for future enhancement.

## See Also

- [TextBox Documentation](README_TextBox.md) (if exists)
- [WinFormPy Tools](README_winformpy_tools.md)
- [Form Controls Guide](../README.md)
