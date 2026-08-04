"""
tooltip.py — Simple tooltip widget for Tkinter
"""

import tkinter as tk


class ToolTip:
    def __init__(self, widget, text):
        self.w = widget
        self.t = text
        self.tip_window = None

    def show_tip(self, event=None):
        """Display the tooltip."""
        if self.tip_window or not self.t:
            return

        x, y, cx, cy = self.w.bbox("insert")
        x = x + self.w.winfo_rootx() + 25
        y = y + self.w.winfo_rooty() + 25

        self.tip_window = tw = tk.Toplevel(self.w)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            tw,
            text=self.t,
            justify=tk.LEFT,
            background="#ffffe0",
            relief=tk.SOLID,
            borderwidth=1,
            font=("tahoma", "8", "normal"),
        )
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        """Hide the tooltip."""
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

    def __call__(self, event=None):
        """Enable tooltip on hover."""
        self.w.bind("<Enter>", self.show_tip)
        self.w.bind("<Leave>", self.hide_tip)
