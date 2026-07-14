"""
exit.py — VMS 3000  •  Exit Confirmation Dialog
Theme-matched to the industrial SCADA palette (navy/steel/amber/teal).
Shows confirmation before exiting the application.
"""

import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox


# ══════════════════════════════════════════════════════════════════════════════
#  THEME  —  VMS 3000 Industrial SCADA colour palette
# ══════════════════════════════════════════════════════════════════════════════

T = {
    # ── Window & chrome ──────────────────────────────────────────────
    "win_bg":           "#f5f7fa",
    "titlebar":         "#1a3a5c",

    # ── Toolbar ──────────────────────────────────────────────────────
    "toolbar_bg":       "#fafbfc",
    "toolbar_border":   "#b8c4d4",
    "toolbar_sep":      "#c8d4e4",

    # ── Menubar ───────────────────────────────────────────────────────
    "menu_bg":          "#2a4a6e",
    "menu_fg":          "#e8f0ff",
    "menu_active_bg":   "#3a6a9e",
    "menu_active_fg":   "#ffffff",
    "menu_drop_bg":     "#2a5080",
    "menu_sep":         "#3a6090",

    # ── Sidebar ───────────────────────────────────────────────────────
    "sidebar_bg":       "#e8ecf0",
    "sidebar_dark":     "#d0d8e0",
    "sidebar_rule":     "#b8c4d4",
    "sidebar_btn":      "#f5f7fa",
    "sidebar_btn_h":    "#e0e8f0",
    "sidebar_btn_p":    "#c8d4e4",
    "sidebar_text":     "#3a4a5a",
    "sidebar_text_hi":  "#1a2533",

    # ── Rack shell ────────────────────────────────────────────────────
    "rack_shell_top":   "#b8c4d4",
    "rack_shell_bot":   "#a0b0c0",
    "rack_row":         "#d0d8e0",
    "rack_screw":       "#708090",

    # ── Slot cards ────────────────────────────────────────────────────
    "slot_bg":          "#d0d8e0",
    "slot_face":        "#c8d4e0",
    "slot_edge_hi":     "#e0e8f0",
    "slot_edge_sh":     "#a8b8c8",
    "slot_cap":         "#f5f7fa",
    "slot_grip":        "#c0d0e0",
    "slot_sel":         "#3a6fcc",
    "slot_sel_face":    "#4a8ae0",
    "slot_num_fg":      "#4a6a98",
    "slot_mod_fg":      "#1a2533",

    # ── PSM module ────────────────────────────────────────────────────
    "psm_body":         "#d0d8e0",
    "psm_brand":        "#1a4fa0",
    "psm_brand2":       "#0d3080",
    "psm_label":        "#2a4a68",
    "psm_3000":         "#1a4fa0",
    "psm_plate":        "#c0d0e0",
    "psm_plate_text":   "#1a4fa0",

    # ── Buttons ───────────────────────────────────────────────────────
    "btn_face":         "#e4e9f0",
    "btn_hover":        "#d0e4f8",
    "btn_press":        "#b0ccee",
    "btn_shadow":       "#8a9bb0",
    "btn_border":       "#b4bfcc",

    # ── Text ──────────────────────────────────────────────────────────
    "text":             "#1a2533",
    "text_dim":         "#5a6a7a",
    "text_hint":        "#1a5ab8",
    "text_white":       "#ffffff",

    # ── Status bar ────────────────────────────────────────────────────
    "status_bg":        "#dde3ec",
    "status_border":    "#b4bfcc",
    "status_section":   "#ccd4e0",

    # ── LEDs ──────────────────────────────────────────────────────────
    "led_green":        "#22c55e",
    "led_green_glow":   "#16a34a",
    "led_amber":        "#f59e0b",
    "led_red":          "#ef4444",
    "led_blue":         "#3b82f6",
    "led_off":          "#334155",

    # ── Accent ────────────────────────────────────────────────────────
    "accent":           "#1a4fa0",
    "accent_light":     "#3a6fcc",
    "accent_teal":      "#0891b2",
}


# ══════════════════════════════════════════════════════════════════════════════
#  EXIT CONFIRMATION DIALOG
# ══════════════════════════════════════════════════════════════════════════════

class ExitDialog:
    """
    Exit confirmation dialog — VMS 3000 SCADA theme.
    
    Shows confirmation before exiting the application.
    """

    def __init__(self, parent, fonts):
        self._fonts  = fonts
        self._parent = parent
        self._dialog = None
        self._confirmed = False

        self._create_dialog()

    def _f(self, key, family="Segoe UI", size=9, weight="normal"):
        return self._fonts.get(key, tkfont.Font(family=family, size=size, weight=weight))

    def _create_dialog(self):
        self._dialog = tk.Toplevel(self._parent)
        self._dialog.title("Exit")
        self._dialog.configure(bg=T["win_bg"])
        self._dialog.resizable(False, False)
        self._dialog.grab_set()

        # Titlebar strip (navy)
        self._create_titlebar()

        # Teal accent rule under titlebar
        tk.Frame(self._dialog, bg=T["accent_teal"], height=3).pack(fill="x")

        # Body
        body = tk.Frame(self._dialog, bg=T["win_bg"], padx=16, pady=12)
        body.pack(fill="both", expand=True)

        self._create_message(body)

        # Button strip
        self._create_buttons()

        # Size & centre
        self._dialog.update_idletasks()
        w, h = 400, 200
        sw = self._dialog.winfo_screenwidth()
        sh = self._dialog.winfo_screenheight()
        self._dialog.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    def _create_titlebar(self):
        bar = tk.Frame(self._dialog, bg=T["titlebar"], pady=10)
        bar.pack(fill="x")

        tk.Label(
            bar,
            text="  Exit",
            font=self._f("ui_b", size=11, weight="bold"),
            bg=T["titlebar"],
            fg=T["text_white"],
            anchor="w",
        ).pack(side="left", fill="x", expand=True)

        badge = tk.Label(
            bar,
            text="  VMS 3000  ",
            font=self._f("ui_b", size=10, weight="bold"),
            bg=T["accent_light"],
            fg=T["text_white"],
            relief="flat",
            padx=6,
            pady=4,
        )
        badge.pack(side="right", padx=(0, 12))

    def _create_message(self, parent):
        # Message text
        message = (
            "Are you sure you want to exit?\n\n"
            "Any unsaved changes will be lost."
        )

        tk.Label(
            parent,
            text=message,
            font=self._f("sm", size=10),
            bg=T["win_bg"],
            fg=T["text"],
            justify="center",
        ).pack(pady=(20, 16))

    def _create_buttons(self):
        strip = tk.Frame(
            self._dialog,
            bg=T["status_bg"],
            pady=12,
            relief="flat",
            bd=0,
        )
        tk.Frame(self._dialog, bg=T["status_border"], height=1).pack(fill="x")
        strip.pack(fill="x", padx=0)

        inner = tk.Frame(strip, bg=T["status_bg"])
        inner.pack(padx=16)

        ub = self._f("ui_b", size=9, weight="bold")

        def _btn(text, cmd, style="normal"):
            if style == "primary":
                bg  = T["accent"]
                fg  = T["text_white"]
                abg = T["accent_light"]
                afg = T["text_white"]
            elif style == "danger":
                bg  = T["led_red"]
                fg  = T["text_white"]
                abg = "#dc2626"
                afg = T["text_white"]
            else:
                bg  = T["btn_face"]
                fg  = T["text"]
                abg = T["btn_hover"]
                afg = T["text"]

            b = tk.Button(
                inner,
                text=f"  {text}  ",
                command=cmd,
                font=ub,
                bg=bg,
                fg=fg,
                activebackground=abg,
                activeforeground=afg,
                relief="flat",
                bd=0,
                padx=12,
                pady=6,
                cursor="hand2",
                highlightthickness=1,
                highlightbackground=T["btn_border"],
            )
            b.pack(side="left", padx=(0, 8))

            def _e(ev): b.config(bg=abg, fg=afg)
            def _l(ev): b.config(bg=bg,  fg=fg)
            b.bind("<Enter>", _e)
            b.bind("<Leave>", _l)
            return b

        _btn("Yes", self._on_confirm, style="danger")
        _btn("No", self._on_cancel, style="normal")

    def _on_confirm(self):
        self._confirmed = True
        self._dialog.destroy()

    def _on_cancel(self):
        self._confirmed = False
        self._dialog.destroy()

    def show(self):
        self._dialog.wait_window()
        return self._confirmed


# ══════════════════════════════════════════════════════════════════════════════
#  Standalone preview
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    root.title("VMS 3000 - Exit Test")
    root.geometry("400x300")
    root.configure(bg=T["win_bg"])

    fonts = {
        "ui_b": tkfont.Font(family="Segoe UI", size=10, weight="bold"),
        "sm":   tkfont.Font(family="Segoe UI", size=9),
        "sm_b": tkfont.Font(family="Segoe UI", size=9,  weight="bold"),
        "mono": tkfont.Font(family="Consolas", size=10),
    }

    def on_exit():
        dialog = ExitDialog(root, fonts)
        if dialog.show():
            print("Exit confirmed")
            root.destroy()
        else:
            print("Exit cancelled")

    # Test button
    btn_frame = tk.Frame(root, bg=T["win_bg"])
    btn_frame.pack(pady=100)

    tk.Button(
        btn_frame,
        text="Exit",
        command=on_exit,
        font=fonts["ui_b"],
        bg=T["accent"],
        fg=T["text_white"],
        activebackground=T["accent_light"],
        activeforeground=T["text_white"],
        relief="flat",
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2",
    ).pack()

    root.mainloop()
