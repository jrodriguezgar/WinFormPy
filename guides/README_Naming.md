NAMING CONVENTIONS FOR WINFORMS (BASED ON .NET/C#)

1. CONTROLS (UI)
    - Convention: Three-letter lowercase prefix + Camel Case name.
    - Rule: The prefix identifies the control type (e.g., btn, txt, lbl).
    - Examples: `btnSave`, `txtUser`, `lblMessage`, `frmMain`.

2. CLASSES, INTERFACES, AND NAMESPACES
    - Convention: Pascal Case.
    - Rule: First letter of each word capitalized. Interfaces start with "I".
    - Examples: `MainForm`, `IController`, `System.Utilities`.

3. PROPERTIES AND METHODS/PROCEDURES
    - Convention: Pascal Case.
    - Properties: Describe a characteristic. Example: `FullName`, `IsValid`.
    - Methods: Verbs or verb phrases. Example: `CalculateTotal()`, `ValidateData()`.

4. LOCAL VARIABLES AND PARAMETERS
    - Convention: Camel Case.
    - Rule: Starts with lowercase. Used within a method or as method arguments.
    - Examples: `currentIndex`, `selectedClient`, `invoiceTotal`.

5. PRIVATE CLASS FIELDS
    - Convention: Camel Case with Underscore.
    - Rule: Prefix with an underscore (`_`) to distinguish from local variables.
    - Examples: `_userName`, `_maxAttempts`, `_accountBalance`.

6. CONSTANTS
    - Convention: Pascal Case.
    - Examples: `MaxElements`, `VATRate`.

---
COMMON PREFIX EXAMPLES FOR CONTROLS:
- Button: `btn`
- Text Box: `txt`
- Label: `lbl`
- Form: `frm`
- Combo Box: `cmb`
- Check Box: `chk`

---
EXAMPLES OF EVENT HANDLER NAMING CONVENTIONS:
- The general pattern is: **on_[control_name]_[event]** (using snake_case)
- Save Button: `def on_btn_save_click(self, event):`
- Text Box: `def on_txt_address_text_changed(self, event):`
- Combo Box: `def on_cmb_products_selected_index_changed(self, event):`
- Form on Load: `def on_frm_main_load(self, event):`
- Cancel Button: `def on_btn_cancel_click(self, event):`