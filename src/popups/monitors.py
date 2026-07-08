"""
monitors.py — VMS 3000  •  Cascading Menu System
Cascading menu for module selection: Monitors → Proximeter/Tachometer → Models
"""

import tkinter as tk
import tkinter.font as tkfont


# ══════════════════════════════════════════════════════════════════════════════
#  THEME  —  VMS 3000 Industrial SCADA colour palette
# ══════════════════════════════════════════════════════════════════════════════

T = {
    # ── Window & chrome ──────────────────────────────────────────────
    "win_bg":           "#f5f7fa",
    "titlebar":         "#1a3a5c",

    # ── Buttons ───────────────────────────────────────────────────────
    "btn_face":         "#e4e9f0",
    "btn_hover":        "#d0e4f8",
    "btn_border":       "#b4bfcc",

    # ── Text ──────────────────────────────────────────────────────────
    "text":             "#1a2533",
    "text_white":       "#ffffff",
    "text_dim":         "#6b7280",

    # ── Status bar ────────────────────────────────────────────────────
    "status_bg":        "#dde3ec",
    "status_border":    "#b4bfcc",

    # ── Accent ────────────────────────────────────────────────────────
    "accent":           "#1a4fa0",
    "accent_light":     "#3a6fcc",
    "accent_teal":      "#0891b2",
}


# ══════════════════════════════════════════════════════════════════════════════
#  CASCADING MENU CLASS
# ══════════════════════════════════════════════════════════════════════════════

class CascadingMenu:
    """
    Cascading menu system for module selection.
    
    Structure:
      Level 1: Monitors, Gateways, Relay, No Modules
      Level 2 (Monitors): Proximeter Monitor, Tachometer Monitor
      Level 3 (Proximeter): 3000/12M/DIS, 3000/6M
    """

    def __init__(self, parent, fonts, on_selection):
        """
        Initialize cascading menu.
        
        Args:
            parent: Parent widget
            fonts: Font dictionary
            on_selection: Callback function when a selection is made
        """
        self._parent = parent
        self._fonts = fonts
        self._on_selection = on_selection
        self._menus = {}  # Store menu references
        self._current_selection = None

    def _f(self, key, family="Segoe UI", size=9, weight="normal"):
        """Font helper."""
        return self._fonts.get(key, tkfont.Font(family=family, size=size, weight=weight))

    def show_menu(self, x, y):
        """Show the main menu at the given coordinates."""
        # Create main menu
        main_menu = tk.Menu(self._parent, tearoff=0, 
                           bg=T["win_bg"],
                           fg=T["text"],
                           activebackground=T["accent_light"],
                           activeforeground=T["text_white"],
                           font=self._f("sm", size=9))
        
        # Add menu items
        self._add_monitors_submenu(main_menu)
        main_menu.add_separator()
        main_menu.add_command(label="Gateways",
                             command=lambda: self._on_selection("Gateways"))
        main_menu.add_separator()
        main_menu.add_command(label="No Modules",
                             command=lambda: self._on_selection("No Modules"))
        
        # Show menu at position
        main_menu.tk_popup(x, y)

    def _add_monitors_submenu(self, parent_menu):
        """Add Monitors submenu with cascading options."""
        monitors_menu = tk.Menu(parent_menu, tearoff=0,
                               bg=T["win_bg"],
                               fg=T["text"],
                               activebackground=T["accent_light"],
                               activeforeground=T["text_white"],
                               font=self._f("sm", size=9))
        
        # Add Proximeter Monitor with its own submenu
        self._add_proximeter_submenu(monitors_menu)
        
        # Add Tachometer Monitor (could have its own submenu too)
        tachometer_menu = tk.Menu(monitors_menu, tearoff=0,
                                  bg=T["win_bg"],
                                  fg=T["text"],
                                  activebackground=T["accent_light"],
                                  activeforeground=T["text_white"],
                                  font=self._f("sm", size=9))
        
        tachometer_menu.add_command(label="3000/12M/TAC",
                                   command=lambda: self._on_selection("3000/12M/TAC"))
        tachometer_menu.add_command(label="3000/6M/TAC",
                                   command=lambda: self._on_selection("3000/6M/TAC"))
        
        monitors_menu.add_cascade(label="Tachometer Monitor", menu=tachometer_menu)
        
        parent_menu.add_cascade(label="Monitors", menu=monitors_menu)

    def _add_proximeter_submenu(self, parent_menu):
        """Add Proximeter Monitor submenu with model options."""
        proximeter_menu = tk.Menu(parent_menu, tearoff=0,
                                  bg=T["win_bg"],
                                  fg=T["text"],
                                  activebackground=T["accent_light"],
                                  activeforeground=T["text_white"],
                                  font=self._f("sm", size=9))
        
        proximeter_menu.add_command(label="3000/12M/DIS",
                                   command=lambda: self._on_selection("3000/12M/DIS"))
        proximeter_menu.add_command(label="3000/6M",
                                   command=lambda: self._on_selection("3000/6M"))
        
        parent_menu.add_cascade(label="Proximeter Monitor", menu=proximeter_menu)


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE SELECTION POPUP (Alternative implementation)
# ══════════════════════════════════════════════════════════════════════════════

class ModuleSelectionPopup:
    """
    Module selection popup with cascading menu buttons.
    
    This provides an alternative to the context menu - a popup dialog
    with buttons that show sub-menus on hover/click.
    """

    def __init__(self, parent, fonts, slot_num, on_selection):
        """
        Initialize module selection popup.
        
        Args:
            parent: Parent widget
            fonts: Font dictionary
            slot_num: Slot number being configured
            on_selection: Callback function when a selection is made
        """
        self._fonts = fonts
        self._parent = parent
        self._slot_num = slot_num
        self._on_selection = on_selection
        self._dialog = None
        self._current_submenu = None

        self._create_dialog()

    def _f(self, key, family="Segoe UI", size=9, weight="normal"):
        """Font helper."""
        return self._fonts.get(key, tkfont.Font(family=family, size=size, weight=weight))

    def _create_dialog(self):
        """Create the module selection dialog."""
        self._dialog = tk.Toplevel(self._parent)
        self._dialog.title(f"Select Module — Slot {self._slot_num}")
        self._dialog.configure(bg=T["win_bg"])
        self._dialog.resizable(False, False)
        self._dialog.grab_set()

        # ── Titlebar strip (navy) ──────────────────────────────────────
        self._create_titlebar()

        # ── Teal accent rule under titlebar ───────────────────────────
        tk.Frame(self._dialog, bg=T["accent_teal"], height=3).pack(fill="x")

        # ── Body ──────────────────────────────────────────────────────
        body = tk.Frame(self._dialog, bg=T["win_bg"], padx=16, pady=12)
        body.pack(fill="both", expand=True)

        # Slot number indicator at top
        slot_indicator = tk.Frame(body, bg=T["accent"], pady=8)
        slot_indicator.pack(fill="x", pady=(0, 12))
        tk.Label(
            slot_indicator,
            text=f"Slot {self._slot_num}",
            font=self._f("ui_b", size=16, weight="bold"),
            bg=T["accent"],
            fg=T["text_white"],
        ).pack()

        self._create_category_buttons(body)
        self._create_submenu_area(body)

        # ── Size & centre ─────────────────────────────────────────────
        self._dialog.update_idletasks()
        w, h = 400, 350
        sw = self._dialog.winfo_screenwidth()
        sh = self._dialog.winfo_screenheight()
        self._dialog.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    def _create_titlebar(self):
        """Create titlebar."""
        bar = tk.Frame(self._dialog, bg=T["titlebar"], pady=10)
        bar.pack(fill="x")

        tk.Label(
            bar,
            text=f"  Select Module for Slot {self._slot_num}",
            font=self._f("ui_b", size=11, weight="bold"),
            bg=T["titlebar"],
            fg=T["text_white"],
            anchor="w",
        ).pack(side="left", fill="x", expand=True)

        tk.Label(
            bar,
            text="  VMS 3000  ",
            font=self._f("ui_b", size=10, weight="bold"),
            bg=T["accent_light"],
            fg=T["text_white"],
            relief="flat",
            padx=6,
            pady=4,
        ).pack(side="right", padx=(0, 12))

    def _create_category_buttons(self, parent):
        """Create main category buttons."""
        btn_frame = tk.Frame(parent, bg=T["win_bg"])
        btn_frame.pack(fill="x", pady=(0, 10))

        ub = self._f("ui_b", size=9, weight="bold")

        def _cat_btn(text, cmd):
            btn = tk.Button(
                btn_frame,
                text=f"  {text}  ",
                command=cmd,
                font=ub,
                bg=T["btn_face"],
                fg=T["text"],
                activebackground=T["btn_hover"],
                activeforeground=T["text"],
                relief="flat",
                bd=0,
                padx=12,
                pady=6,
                cursor="hand2",
                highlightthickness=1,
                highlightbackground=T["btn_border"],
            )
            btn.pack(side="left", padx=(0, 8))

            # Hover effects
            def _e(ev): btn.config(bg=T["btn_hover"])
            def _l(ev): btn.config(bg=T["btn_face"])
            btn.bind("<Enter>", _e)
            btn.bind("<Leave>", _l)
            return btn

        _cat_btn("Monitors", lambda: self._show_monitors_submenu())
        _cat_btn("Gateways", lambda: self._on_selection("Gateways"))
        _cat_btn("No Modules", lambda: self._on_selection("No Modules"))

    def _create_submenu_area(self, parent):
        """Create area for displaying submenus."""
        self._submenu_frame = tk.Frame(parent, bg=T["win_bg"], bd=2, relief="groove", padx=10, pady=10)
        self._submenu_frame.pack(fill="both", expand=True)

        # Initial message
        tk.Label(
            self._submenu_frame,
            text="Select a category to view options",
            font=self._f("sm", size=9),
            bg=T["win_bg"],
            fg=T["text_dim"],
        ).pack(anchor="center")

    def _show_monitors_submenu(self):
        """Show monitors submenu options."""
        # Clear current submenu
        for widget in self._submenu_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self._submenu_frame,
            text="Monitor Type:",
            font=self._f("sm_b", size=9, weight="bold"),
            bg=T["win_bg"],
            fg=T["accent"],
            anchor="w",
        ).pack(fill="x", pady=(0, 8))

        ub = self._f("ui_b", size=9, weight="bold")

        def _sub_btn(text, cmd):
            btn = tk.Button(
                self._submenu_frame,
                text=f"  {text}  ",
                command=cmd,
                font=ub,
                bg=T["btn_face"],
                fg=T["text"],
                activebackground=T["btn_hover"],
                activeforeground=T["text"],
                relief="flat",
                bd=0,
                padx=12,
                pady=6,
                cursor="hand2",
                highlightthickness=1,
                highlightbackground=T["btn_border"],
            )
            btn.pack(fill="x", pady=(0, 6))

            # Hover effects
            def _e(ev): btn.config(bg=T["btn_hover"])
            def _l(ev): btn.config(bg=T["btn_face"])
            btn.bind("<Enter>", _e)
            btn.bind("<Leave>", _l)
            return btn

        _sub_btn("Proximeter Monitor", lambda: self._show_proximeter_models())
        _sub_btn("Tachometer Monitor", lambda: self._show_tachometer_models())

    def _show_proximeter_models(self):
        """Show proximeter monitor models."""
        # Clear current submenu
        for widget in self._submenu_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self._submenu_frame,
            text="Proximeter Monitor Models:",
            font=self._f("sm_b", size=9, weight="bold"),
            bg=T["win_bg"],
            fg=T["accent"],
            anchor="w",
        ).pack(fill="x", pady=(0, 8))

        ub = self._f("ui_b", size=9, weight="bold")

        def _model_btn(text, cmd):
            btn = tk.Button(
                self._submenu_frame,
                text=f"  {text}  ",
                command=cmd,
                font=ub,
                bg=T["accent"],
                fg=T["text_white"],
                activebackground=T["accent_light"],
                activeforeground=T["text_white"],
                relief="flat",
                bd=0,
                padx=12,
                pady=6,
                cursor="hand2",
                highlightthickness=1,
                highlightbackground=T["btn_border"],
            )
            btn.pack(fill="x", pady=(0, 6))

            # Hover effects
            def _e(ev): btn.config(bg=T["accent_light"])
            def _l(ev): btn.config(bg=T["accent"])
            btn.bind("<Enter>", _e)
            btn.bind("<Leave>", _l)
            return btn

        _model_btn("3000/12M/DIS", lambda: self._on_selection("3000/12M/DIS"))
        _model_btn("3000/6M", lambda: self._on_selection("3000/6M"))
        _model_btn("Relay", lambda: self._on_selection("3000/RLY"))

        # Back button
        tk.Button(
            self._submenu_frame,
            text="  ← Back to Monitor Types  ",
            command=self._show_monitors_submenu,
            font=ub,
            bg=T["btn_face"],
            fg=T["text"],
            activebackground=T["btn_hover"],
            activeforeground=T["text"],
            relief="flat",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
        ).pack(fill="x", pady=(10, 0))

    def _show_tachometer_models(self):
        """Show tachometer monitor models."""
        # Clear current submenu
        for widget in self._submenu_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self._submenu_frame,
            text="Tachometer Monitor Models:",
            font=self._f("sm_b", size=9, weight="bold"),
            bg=T["win_bg"],
            fg=T["accent"],
            anchor="w",
        ).pack(fill="x", pady=(0, 8))

        ub = self._f("ui_b", size=9, weight="bold")

        def _model_btn(text, cmd):
            btn = tk.Button(
                self._submenu_frame,
                text=f"  {text}  ",
                command=cmd,
                font=ub,
                bg=T["accent"],
                fg=T["text_white"],
                activebackground=T["accent_light"],
                activeforeground=T["text_white"],
                relief="flat",
                bd=0,
                padx=12,
                pady=6,
                cursor="hand2",
                highlightthickness=1,
                highlightbackground=T["btn_border"],
            )
            btn.pack(fill="x", pady=(0, 6))

            # Hover effects
            def _e(ev): btn.config(bg=T["accent_light"])
            def _l(ev): btn.config(bg=T["accent"])
            btn.bind("<Enter>", _e)
            btn.bind("<Leave>", _l)
            return btn

        _model_btn("3000/12M/TAC", lambda: self._on_selection("3000/12M/TAC"))
        _model_btn("3000/6M/TAC", lambda: self._on_selection("3000/6M/TAC"))

        # Back button
        tk.Button(
            self._submenu_frame,
            text="  ← Back to Monitor Types  ",
            command=self._show_monitors_submenu,
            font=ub,
            bg=T["btn_face"],
            fg=T["text"],
            activebackground=T["btn_hover"],
            activeforeground=T["text"],
            relief="flat",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
        ).pack(fill="x", pady=(10, 0))

    def _on_selection(self, selection):
        """Handle selection and close dialog."""
        print(f"Slot {self._slot_num} → Selected: {selection}")
        if self._on_selection:
            self._on_selection(selection)
        self._dialog.destroy()

    def show(self):
        """Display the dialog."""
        self._dialog.wait_window()


# ══════════════════════════════════════════════════════════════════════════════
#  Standalone preview
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    fonts = {
        "ui_b": tkfont.Font(family="Segoe UI", size=10, weight="bold"),
        "sm":   tkfont.Font(family="Segoe UI", size=9),
        "sm_b": tkfont.Font(family="Segoe UI", size=9,  weight="bold"),
        "mono": tkfont.Font(family="Consolas", size=10),
    }

    def on_selection(selection):
        print(f"Selected: {selection}")

    # Test popup version
    popup = ModuleSelectionPopup(root, fonts, slot_num=5, on_selection=on_selection)
    popup.show()
    root.destroy()