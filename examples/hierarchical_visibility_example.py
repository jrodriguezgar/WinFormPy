"""Hierarchical Visibility Example

Demonstrates how child control visibility depends on both:
1. Its own internal visibility property
2. The visibility of all parent containers in the hierarchy
"""

from winformpy import (
    Form, Panel, Button, Label, CheckBox, Application,
    Font, FontStyle, DockStyle
)


def main():
    # =========================================================================
    # Create main form
    # =========================================================================
    form = Form({
        'Text': 'Hierarchical Visibility Demo',
        'Width': 1000,
        'Height': 600,
        'StartPosition': 'CenterScreen'
    })
    form.ApplyLayout()

    # =========================================================================
    # Title Panel
    # =========================================================================
    title_panel = Panel(form, {
        'Height': 60,
        'BackColor': '#0078D4'
    })
    title_panel.Dock = DockStyle.Top
    
    Label(title_panel, {
        'Text': 'Parent-Child Visibility Hierarchy',
        'Left': 20,
        'Top': 15,
        'AutoSize': True,
        'Font': Font('Segoe UI', 16, FontStyle.Bold),
        'ForeColor': '#FFFFFF',
        'BackColor': '#0078D4'
    })

    # =========================================================================
    # Main Content Panel
    # =========================================================================
    main_panel = Panel(form, {
        'BackColor': '#F5F5F5'
    })
    main_panel.Dock = DockStyle.Fill

    # =========================================================================
    # Left Side - Target Container with Children
    # =========================================================================
    container = Panel(main_panel, {
        'Left': 20,
        'Top': 20,
        'Width': 300,
        'Height': 450,
        'BorderStyle': 'fixed_single',
        'BackColor': '#E3F2FD'
    })
    
    Label(container, {
        'Text': 'I am the Container',
        'Left': 10,
        'Top': 10,
        'AutoSize': True,
        'Font': Font('Segoe UI', 10, FontStyle.Bold),
        'BackColor': '#E3F2FD'
    })
    
    # Child 1: A Button
    btn_child = Button(container, {
        'Text': 'I am a Child Button',
        'Left': 50,
        'Top': 100,
        'Width': 180,
        'Height': 35,
        'Font': Font('Segoe UI', 9)
    })
    
    # Child 2: A Label
    lbl_child = Label(container, {
        'Text': 'I am a Child Label',
        'Left': 50,
        'Top': 200,
        'BackColor': '#FFFFFF',
        'AutoSize': True,
        'Font': Font('Segoe UI', 9),
        'BorderStyle': 'solid'
    })

    # =========================================================================
    # Right Side - Control Panel
    # =========================================================================
    ctrl_panel = Panel(main_panel, {
        'Left': 350,
        'Top': 20,
        'Width': 600,
        'Height': 450,
        'BackColor': '#FFFFFF',
        'BorderStyle': 'fixed_single'
    })
    
    # Header
    Label(ctrl_panel, {
        'Text': 'Control & Monitor',
        'Font': Font('Segoe UI', 14, FontStyle.Bold),
        'Left': 10,
        'Top': 10,
        'AutoSize': True,
        'ForeColor': '#0078D4'
    })
    
    # Actions Section
    Label(ctrl_panel, {
        'Text': 'Actions (Set Internal Visibility):',
        'Left': 10,
        'Top': 50,
        'Font': Font('Segoe UI', 10, FontStyle.Bold),
        'AutoSize': True
    })

    # Container Toggle
    chk_container = CheckBox(ctrl_panel, {
        'Text': 'Show Container (Parent)',
        'Left': 20,
        'Top': 80,
        'AutoSize': True,
        'Checked': True,
        'Font': Font('Segoe UI', 9)
    })
    
    # Child 1 Toggle
    chk_child1 = CheckBox(ctrl_panel, {
        'Text': 'Show Child Button',
        'Left': 40,
        'Top': 110,
        'AutoSize': True,
        'Checked': True,
        'Font': Font('Segoe UI', 9)
    })
    
    # Child 2 Toggle
    chk_child2 = CheckBox(ctrl_panel, {
        'Text': 'Show Child Label',
        'Left': 40,
        'Top': 140,
        'AutoSize': True,
        'Checked': True,
        'Font': Font('Segoe UI', 9)
    })
    
    # Monitor Section
    Label(ctrl_panel, {
        'Text': 'Effective Visibility (Real-time Status):',
        'Left': 10,
        'Top': 190,
        'Font': Font('Segoe UI', 10, FontStyle.Bold),
        'AutoSize': True
    })
    
    # Status Labels
    lbl_status_container = Label(ctrl_panel, {
        'Left': 20,
        'Top': 220,
        'AutoSize': True,
        'Font': Font('Consolas', 10)
    })
    
    lbl_status_child1 = Label(ctrl_panel, {
        'Left': 20,
        'Top': 250,
        'AutoSize': True,
        'Font': Font('Consolas', 10)
    })
    
    lbl_status_child2 = Label(ctrl_panel, {
        'Left': 20,
        'Top': 280,
        'AutoSize': True,
        'Font': Font('Consolas', 10)
    })
    
    # Explanation
    Label(ctrl_panel, {
        'Text': 'NOTE: A child control is only visible if BOTH:\n'
                '1. Its internal visibility is True (Checkbox checked)\n'
                '2. Its Parent Container is Visible',
        'Left': 10,
        'Top': 320,
        'Width': 580,
        'Height': 80,
        'BackColor': '#FFFFE0',
        'BorderStyle': 'fixed_single',
        'Font': Font('Segoe UI', 9)
    })

    # =========================================================================
    # Update Functions
    # =========================================================================
    def update_status_label(label_control, name, control, internal_chk):
        """Updates a status label with visibility information."""
        effective = control.Visible
        internal = internal_chk.Checked
        
        status = "VISIBLE" if effective else "HIDDEN "
        reason = ""
        
        if not effective:
            if not internal:
                reason = "(Self hidden)"
            elif not container.Visible and control != container:
                reason = "(Parent hidden)"
        
        color = "#008800" if effective else "#CC0000"
        label_control.Text = f"{name:<15}: {status} {reason}"
        label_control.ForeColor = color

    def update_state(sender=None, e=None):
        """Updates visibility based on checkbox states."""
        # Apply user intentions (Internal State)
        container.Visible = chk_container.Checked
        btn_child.Visible = chk_child1.Checked
        lbl_child.Visible = chk_child2.Checked
        
        # Update Monitor Labels
        update_status_label(lbl_status_container, "Container", container, chk_container)
        update_status_label(lbl_status_child1, "Child Button", btn_child, chk_child1)
        update_status_label(lbl_status_child2, "Child Label", lbl_child, chk_child2)

    # Bind events
    chk_container.CheckedChanged = update_state
    chk_child1.CheckedChanged = update_state
    chk_child2.CheckedChanged = update_state

    # =========================================================================
    # Initialize and run
    # =========================================================================
    update_state()
    Application.Run(form)


if __name__ == "__main__":
    main()

