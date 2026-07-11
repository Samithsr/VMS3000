"""
print.py — VMS 3000  •  Print Confirmation Dialog
Simple confirmation dialog for print action.
"""

import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox
from theme import T


class PrintDialog:
    """Simple print confirmation dialog."""

    def __init__(self, parent, fonts):
        self._fonts = fonts
        self._parent = parent
        self._confirmed = False

    def show(self):
        result = messagebox.askyesno(
            "Print",
            "Do you want to print the configuration?",
            parent=self._parent
        )
        if result:
            messagebox.showinfo("Print", "Printing configuration...", parent=self._parent)
        return result
