"""
menubar.py — VMS 3000
Dark-navy menu bar with fixed-width items and crisp separators.
"""

import tkinter as tk
from theme import T


def build_menubar(root, fonts, commands: dict):
    """
    Attach a dark-navy OS menu bar to *root*.

    Expected command keys:
        new, open, save, save_as, connect, disconnect,
        calibrate, diag, comm, about
    """
    mb = tk.Menu(
        root,
        bg=T["menu_bg"],
        fg=T["menu_fg"],
        activebackground=T["menu_active_bg"],
        activeforeground=T["menu_active_fg"],
        font=fonts["menu"],
        relief="flat",
        bd=0,
    )
    root.config(menu=mb)

    # ── helper ──────────────────────────────────────────────────────
    def _drop(label, items):
        m = tk.Menu(
            mb,
            tearoff=0,
            bg=T["menu_drop_bg"],
            fg=T["menu_fg"],
            activebackground=T["menu_active_bg"],
            activeforeground=T["menu_active_fg"],
            selectcolor=T["menu_active_bg"],
            font=fonts["menu"],
            relief="flat",
            bd=1,
            postcommand=None,
        )
        for item in items:
            if item is None:
                m.add_separator()
            else:
                lbl, cmd, *rest = item
                state    = rest[0] if rest else tk.NORMAL
                accel    = rest[1] if len(rest) > 1 else ""
                m.add_command(
                    label=f"  {lbl}",
                    accelerator=accel,
                    command=cmd or (lambda: None),
                    state=state,
                )
        mb.add_cascade(label=f"  {label}  ", menu=m)

    # ── File ────────────────────────────────────────────────────────
    _drop("File", [
        ("New",            commands.get("new"),      tk.NORMAL, "Ctrl+N"),
        ("Open…",          commands.get("open"),     tk.NORMAL, "Ctrl+O"),
        ("Save",           commands.get("save"),     tk.NORMAL, "Ctrl+S"),
        ("Save As…",       commands.get("save_as"),  tk.NORMAL, "Ctrl+Shift+S"),
        None,
        ("Print…",         None,                    tk.NORMAL, "Ctrl+P"),
        None,
        ("Exit",           root.destroy,            tk.NORMAL, "Alt+F4"),
    ])

    # ── Edit ────────────────────────────────────────────────────────
    _drop("Edit", [
        ("Undo",           None,  tk.DISABLED, "Ctrl+Z"),
        ("Redo",           None,  tk.DISABLED, "Ctrl+Y"),
        None,
        ("Cut",            None,  tk.NORMAL,  "Ctrl+X"),
        ("Copy",           None,  tk.NORMAL,  "Ctrl+C"),
        ("Paste",          None,  tk.NORMAL,  "Ctrl+V"),
        None,
        ("Select All",     None,  tk.NORMAL,  "Ctrl+A"),
    ])

    # ── Utilities ───────────────────────────────────────────────────
    _drop("Utilities", [
        ("Connect",            commands.get("connect"),     tk.NORMAL),
        ("Disconnect",         commands.get("disconnect"),  tk.NORMAL),
        None,
        ("Calibrate…",         commands.get("calibrate"),  tk.NORMAL),
        ("Diagnostics…",       commands.get("diag"),       tk.NORMAL),
        ("Firmware Update…",   None,                       tk.NORMAL),
    ])

    # ── Options ─────────────────────────────────────────────────────
    _drop("Options", [
        ("Preferences…",             None,                    tk.NORMAL),
        ("Communication Settings…",  commands.get("comm"),    tk.NORMAL),
        ("Rack Address…",            None,                    tk.NORMAL),
        None,
        ("Theme",                    None,                    tk.DISABLED),
    ])

    # ── View ────────────────────────────────────────────────────────
    _drop("View", [
        ("Zoom In",      None, tk.NORMAL, "Ctrl++"),
        ("Zoom Out",     None, tk.NORMAL, "Ctrl+-"),
        ("Reset Zoom",   None, tk.NORMAL, "Ctrl+0"),
        None,
        ("Full Screen",  None, tk.NORMAL, "F11"),
        ("Reset Layout", None, tk.NORMAL),
    ])

    # ── Help ────────────────────────────────────────────────────────
    _drop("Help", [
        ("Help Topics",      None,                    tk.NORMAL, "F1"),
        ("Quick Start Guide",None,                    tk.NORMAL),
        None,
        ("Check for Updates",None,                    tk.NORMAL),
        ("About VMS 3000",   commands.get("about"),  tk.NORMAL),
    ])