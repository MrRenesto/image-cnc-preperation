"""CNC Image Preparation Tool - Entry Point.

Refactored architecture:
- processors/: Edge detection algorithms using Strategy pattern
- services/: Business logic layer
- ui/: User interface components
"""
import tkinter as tk
from ui import CNCImageApp


def main():
    """Application entry point."""
    root = tk.Tk()
    app = CNCImageApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
