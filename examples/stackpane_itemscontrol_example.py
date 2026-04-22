"""
StackPane & ItemsControl Example

Demonstrates the two new container layout controls:

1. StackPane  - Stacks child controls vertically or horizontally with optional spacing.
2. ItemsControl - Generates child controls from a data source via a template function.

FEATURES DEMONSTRATED:
- StackPane with Vertical and Horizontal orientation
- StackPane.Spacing for gaps between children
- ItemsControl.ItemsSource data-binding
- ItemsControl.ItemTemplate for custom item rendering
- Dynamic add / remove items at runtime
"""

from winformpy.winformpy import (
    Application, Form, StackPane, ItemsControl,
    Button, Label, Panel, TextBox, CheckBox,
    DockStyle, BorderStyle, Font, FontStyle, Color
)


def main():
    # ── Main Form ───────────────────────────────────────────────
    form = Form({
        'Text': 'StackPane & ItemsControl Demo',
        'Width': 800,
        'Height': 520,
        'BackColor': '#F5F5F5'
    })

    # ── Left side: StackPane demo ──────────────────────────────
    left_panel = Panel(form, {
        'Left': 10, 'Top': 10, 'Width': 370, 'Height': 460,
        'BorderStyle': BorderStyle.FixedSingle,
        'BackColor': '#FFFFFF'
    })

    Label(left_panel, {
        'Text': 'StackPane Demo',
        'Left': 10, 'Top': 8, 'AutoSize': True,
        'Font': Font('Segoe UI', 11, FontStyle.Bold),
        'ForeColor': '#0078D4', 'BackColor': '#FFFFFF'
    })

    # Vertical StackPane
    Label(left_panel, {
        'Text': 'Vertical (Spacing=8):',
        'Left': 10, 'Top': 40, 'AutoSize': True,
        'BackColor': '#FFFFFF'
    })

    v_stack = StackPane(left_panel, {
        'Left': 10, 'Top': 62, 'Width': 160, 'Height': 200,
        'Orientation': 'Vertical',
        'Spacing': 8,
        'AutoScroll': True,
        'BorderStyle': BorderStyle.FixedSingle,
        'BackColor': '#FAFAFA'
    })

    for i in range(1, 4):
        Button(v_stack, {
            'Text': f'Item {i}', 'Width': 130, 'Height': 30
        })

    # Horizontal StackPane
    Label(left_panel, {
        'Text': 'Horizontal (Spacing=6):',
        'Left': 190, 'Top': 40, 'AutoSize': True,
        'BackColor': '#FFFFFF'
    })

    h_stack = StackPane(left_panel, {
        'Left': 10, 'Top': 280, 'Width': 340, 'Height': 50,
        'Orientation': 'Horizontal',
        'Spacing': 6,
        'BorderStyle': BorderStyle.FixedSingle,
        'BackColor': '#FAFAFA'
    })

    for color, text in [('#0078D4', 'Home'), ('#107C10', 'Files'), ('#5C2D91', 'Settings')]:
        Button(h_stack, {
            'Text': text, 'Width': 80, 'Height': 32, 'BackColor': color, 'ForeColor': '#FFFFFF'
        })

    # Dynamic add button
    def add_to_stack(sender, e):
        n = len(v_stack.Controls) + 1
        Button(v_stack, {'Text': f'Item {n}', 'Width': 130, 'Height': 30})

    btn_add = Button(left_panel, {
        'Text': '+ Add to Vertical Stack',
        'Left': 10, 'Top': 350, 'Width': 160, 'Height': 30
    })
    btn_add.Click = add_to_stack

    # ── Right side: ItemsControl demo ──────────────────────────
    right_panel = Panel(form, {
        'Left': 400, 'Top': 10, 'Width': 370, 'Height': 460,
        'BorderStyle': BorderStyle.FixedSingle,
        'BackColor': '#FFFFFF'
    })

    Label(right_panel, {
        'Text': 'ItemsControl Demo',
        'Left': 10, 'Top': 8, 'AutoSize': True,
        'Font': Font('Segoe UI', 11, FontStyle.Bold),
        'ForeColor': '#0078D4', 'BackColor': '#FFFFFF'
    })

    # --- Template function: each item is rendered as a styled label ---
    def fruit_template(parent, item):
        lbl = Label(parent, {
            'Text': f'  {item}',
            'Width': 310, 'Height': 32,
            'BackColor': '#F0F8FF',
            'ForeColor': '#1A1A1A',
            'Font': Font('Segoe UI', 10),
            'BorderStyle': BorderStyle.FixedSingle
        })
        return lbl

    fruits = ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry', 'Fig']

    ic = ItemsControl(right_panel, {
        'Left': 10, 'Top': 40, 'Width': 340, 'Height': 280,
        'ItemsSource': fruits,
        'ItemTemplate': fruit_template,
        'Spacing': 4,
        'AutoScroll': True,
        'BackColor': '#FFFFFF'
    })

    # Controls for dynamic changes
    new_fruits = iter(['Guava', 'Grape', 'Kiwi', 'Lemon', 'Mango', 'Papaya', 'Peach'])

    txt_new = TextBox(right_panel, {
        'Left': 10, 'Top': 335, 'Width': 200, 'Height': 28
    })
    txt_new.Text = next(new_fruits)

    def add_fruit(sender, e):
        name = txt_new.Text.strip()
        if name:
            fruits.append(name)
            ic.ItemsSource = list(fruits)
            txt_new.Text = next(new_fruits, f'Fruit {len(fruits) + 1}')

    def remove_last(sender, e):
        if fruits:
            fruits.pop()
            ic.ItemsSource = list(fruits)

    btn_add_fruit = Button(right_panel, {
        'Text': 'Add Item',
        'Left': 220, 'Top': 335, 'Width': 120, 'Height': 28
    })
    btn_add_fruit.Click = add_fruit

    btn_remove = Button(right_panel, {
        'Text': 'Remove Last',
        'Left': 220, 'Top': 370, 'Width': 120, 'Height': 28
    })
    btn_remove.Click = remove_last

    lbl_count = Label(right_panel, {
        'Text': f'Items: {ic.ItemCount}',
        'Left': 10, 'Top': 375, 'AutoSize': True,
        'BackColor': '#FFFFFF'
    })

    def on_items_changed(sender, e):
        lbl_count.Text = f'Items: {ic.ItemCount}'

    ic.ItemsChanged = on_items_changed

    # ── Run ─────────────────────────────────────────────────────
    Application.Run(form)


if __name__ == '__main__':
    main()
