import sys
import os
sys.path.append(os.getcwd())

from winformpy.winformpy import Form, Button, Panel, Label, Application

def main():
    form = Form()
    form.Text = "Test Dock"
    form.Size = (800, 600)
    
    # Top panel
    top = Panel(form)
    top.Dock = "Top"
    top.Height = 100
    top.BackColor = "blue"
    
    # Bottom panel
    bottom = Panel(form)
    bottom.Dock = "Bottom"
    bottom.Height = 100
    bottom.BackColor = "red"
    
    # Left panel
    left = Panel(form)
    left.Dock = "Left"
    left.Width = 150
    left.BackColor = "green"
    
    # Main panel
    main = Panel(form)
    main.Dock = "Fill"
    main.BackColor = "white"
    
    print("Panels created:")
    print(f"Top: {top}")
    print(f"Bottom: {bottom}")
    print(f"Left: {left}")
    print(f"Main: {main}")
    
    Application.Run(form)

if __name__ == "__main__":
    main()
