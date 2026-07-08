"""
tooltip.py — lightweight hover tooltip for VMS 3000
"""
import tkinter as tk


class ToolTip:
    def __init__(self, widget, text):
        self.w = widget
        self.t = text
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, _=None):
        x = self.w.winfo_rootx() + 4
        y = self.w.winfo_rooty() + self.w.winfo_height() + 4
        self.tip = tk.Toplevel(self.w)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        f = tk.Frame(self.tip, bg="#1a3a6b", padx=1, pady=1)
        f.pack()
        tk.Label(f, text=self.t, font=("Segoe UI", 8),
                 bg="#fffde0", fg="#1a2433", padx=6, pady=3).pack()

    def hide(self, _=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None


# Alias for compatibility
Tooltip = ToolTip