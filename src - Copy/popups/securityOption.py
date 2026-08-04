"""
securityOption.py — VMS 3000  •  Security Options Popup
Exact design matching the reference image + themed to industrial SCADA palette.
Self-contained: theme T{} embedded, no external imports required.
"""

import tkinter as tk
import tkinter.font as tkfont


# ══════════════════════════════════════════════════════════════════════════════
#  THEME  —  VMS 3000 Industrial SCADA colour palette
# ══════════════════════════════════════════════════════════════════════════════

T = {
    # ── Window & chrome ───────────────────────────────────────────────────
    "win_bg":           "#f5f7fa",   # cool-grey workspace
    "titlebar":         "#1a3a5c",   # deep navy header

    # ── Toolbar / borders ─────────────────────────────────────────────────
    "toolbar_bg":       "#fafbfc",
    "toolbar_border":   "#b8c4d4",
    "toolbar_sep":      "#c8d4e4",

    # ── Menubar ───────────────────────────────────────────────────────────
    "menu_bg":          "#2a4a6e",
    "menu_fg":          "#e8f0ff",
    "menu_active_bg":   "#3a6a9e",
    "menu_active_fg":   "#ffffff",
    "menu_drop_bg":     "#2a5080",
    "menu_sep":         "#3a6090",

    # ── Sidebar ───────────────────────────────────────────────────────────
    "sidebar_bg":       "#e8ecf0",
    "sidebar_dark":     "#d0d8e0",
    "sidebar_rule":     "#b8c4d4",
    "sidebar_btn":      "#f5f7fa",
    "sidebar_btn_h":    "#e0e8f0",
    "sidebar_btn_p":    "#c8d4e4",
    "sidebar_text":     "#3a4a5a",
    "sidebar_text_hi":  "#1a2533",

    # ── Rack shell ────────────────────────────────────────────────────────
    "rack_shell_top":   "#b8c4d4",
    "rack_shell_bot":   "#a0b0c0",
    "rack_row":         "#d0d8e0",
    "rack_screw":       "#708090",

    # ── Slot cards ────────────────────────────────────────────────────────
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

    # ── PSM module ────────────────────────────────────────────────────────
    "psm_body":         "#d0d8e0",
    "psm_brand":        "#1a4fa0",
    "psm_brand2":       "#0d3080",
    "psm_label":        "#2a4a68",
    "psm_3000":         "#1a4fa0",
    "psm_plate":        "#c0d0e0",
    "psm_plate_text":   "#1a4fa0",

    # ── Buttons ───────────────────────────────────────────────────────────
    "btn_face":         "#e4e9f0",
    "btn_hover":        "#d0e4f8",
    "btn_press":        "#b0ccee",
    "btn_shadow":       "#8a9bb0",
    "btn_border":       "#b4bfcc",

    # ── Text ──────────────────────────────────────────────────────────────
    "text":             "#1a2533",
    "text_dim":         "#5a6a7a",
    "text_hint":        "#1a5ab8",
    "text_white":       "#ffffff",

    # ── Status bar ────────────────────────────────────────────────────────
    "status_bg":        "#dde3ec",
    "status_border":    "#b4bfcc",
    "status_section":   "#ccd4e0",

    # ── LEDs ──────────────────────────────────────────────────────────────
    "led_green":        "#22c55e",
    "led_green_glow":   "#16a34a",
    "led_amber":        "#f59e0b",
    "led_red":          "#ef4444",
    "led_blue":         "#3b82f6",
    "led_off":          "#334155",

    # ── Accent ────────────────────────────────────────────────────────────
    "accent":           "#1a4fa0",
    "accent_light":     "#3a6fcc",
    "accent_teal":      "#0891b2",
}


# ══════════════════════════════════════════════════════════════════════════════
#  POPUP CLASS
# ══════════════════════════════════════════════════════════════════════════════

class SecurityOptionsPopup:
    """
    Security Options popup — VMS 3000 SCADA theme.

    Pixel-accurate to the reference image:
      ┌─ Security Options ─────────────────────────────────────────────────────┐
      │  ┌─ Configuration Module Security Options ─────────────────────────┐   │
      │  │  ☑  Change Setpoints in Program-Mode Only                       │   │
      │  │  ☐  Disable Front Communication Port                            │   │
      │  │  ☐  Drive Rack Not OK Relay If Rack Address is Changed…         │   │
      │  │  ☐  Drive Rack Not OK Relay if a Module is Removed…             │   │
      │  │  ☐  Drive Rack Not OK Relay If Key Switch is Changes…           │   │
      │  │  ☐  Disable VSM 3000 RCS Configuration Download…               │   │
      │  └─────────────────────────────────────────────────────────────────┘   │
      │  [ Ok ]  [ Cancel ]  [ Help ]  [ Select all ]          [VMS 3000]      │
      └────────────────────────────────────────────────────────────────────────┘
    """

    # ------------------------------------------------------------------ #
    #  Init                                                                #
    # ------------------------------------------------------------------ #

    def __init__(self, parent, fonts):
        self._fonts  = fonts
        self._parent = parent
        self._dialog = None
        self._vars   = {}          # key → tk.BooleanVar
        self._chk_widgets = []     # checkbox widget refs for select-all

        # Default states — first checkbox ticked, rest unchecked (matches image)
        self._defaults = {
            "change_setpoints":            True,
            "disable_front_comm":          False,
            "drive_relay_address_change":  False,
            "drive_relay_module_change":   False,
            "drive_relay_keyswitch_change":False,
            "disable_rcs_download":        False,
        }

        self._create_dialog()

    # ------------------------------------------------------------------ #
    #  Font helper                                                         #
    # ------------------------------------------------------------------ #

    def _f(self, key, family="Segoe UI", size=9, weight="normal"):
        return self._fonts.get(key, tkfont.Font(family=family, size=size, weight=weight))

    # ------------------------------------------------------------------ #
    #  Dialog shell                                                        #
    # ------------------------------------------------------------------ #

    def _create_dialog(self):
        self._dialog = tk.Toplevel(self._parent)
        self._dialog.title("Security Options")
        self._dialog.configure(bg=T["win_bg"])
        self._dialog.resizable(False, False)
        self._dialog.grab_set()

        # ── Navy titlebar ──────────────────────────────────────────────
        self._create_titlebar()

        # ── Teal accent rule ───────────────────────────────────────────
        tk.Frame(self._dialog, bg=T["accent_teal"], height=3).pack(fill="x")

        # ── Body ──────────────────────────────────────────────────────
        body = tk.Frame(self._dialog, bg=T["win_bg"], padx=16, pady=12)
        body.pack(fill="both", expand=True)

        self._create_security_group(body)

        # ── Status border + button strip ──────────────────────────────
        tk.Frame(self._dialog, bg=T["status_border"], height=1).pack(fill="x")
        self._create_buttons()

        # ── Size & centre ─────────────────────────────────────────────
        self._dialog.update_idletasks()
        w, h = 600, 370
        sw = self._dialog.winfo_screenwidth()
        sh = self._dialog.winfo_screenheight()
        self._dialog.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    # ------------------------------------------------------------------ #
    #  Titlebar  — navy + VMS 3000 badge (top-right)                      #
    # ------------------------------------------------------------------ #

    def _create_titlebar(self):
        bar = tk.Frame(self._dialog, bg=T["titlebar"], pady=10)
        bar.pack(fill="x")

        tk.Label(
            bar,
            text="  Security Options",
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

    # ------------------------------------------------------------------ #
    #  Security group box + checkboxes                                     #
    # ------------------------------------------------------------------ #

    def _create_security_group(self, parent):
        grp = tk.LabelFrame(
            parent,
            text="  Configuration Module Security Options  ",
            font=self._f("sm_b", size=9, weight="bold"),
            bg=T["win_bg"],
            fg=T["accent"],           # navy-blue group title
            bd=2,
            relief="groove",
            padx=14,
            pady=10,
        )
        grp.pack(fill="both", expand=True)

        checkboxes = [
            ("Change Setpoints in Program-Mode Only",
             "change_setpoints"),
            ("Disable Front Communication Port",
             "disable_front_comm"),
            ("Drive Rack Not OK Relay If Rack Address is Changed in Run Mode",
             "drive_relay_address_change"),
            ("Drive Rack Not OK Relay if a Module is Removed or Inserted into the Rack",
             "drive_relay_module_change"),
            ("Drive Rack Not OK Relay If Key Switch is Changes from Program to Run Mode",
             "drive_relay_keyswitch_change"),
            ("Disable VSM 3000 RCS Configuration Download in TCP/IP Communication Mode",
             "disable_rcs_download"),
        ]

        sm_b = self._f("sm_b", size=9, weight="bold")   # bold checkbox labels

        for label_text, key in checkboxes:
            var = tk.BooleanVar(value=self._defaults.get(key, False))
            self._vars[key] = var

            chk = tk.Checkbutton(
                grp,
                text=f"  {label_text}",
                variable=var,
                font=sm_b,                         # BOLD labels
                bg=T["win_bg"],
                fg=T["text"],                      # dark navy text
                selectcolor=T["accent_light"],     # blue fill when checked
                activebackground=T["win_bg"],
                activeforeground=T["accent"],
                anchor="w",
                padx=2,
                pady=3,
                cursor="hand2",
            )
            chk.pack(fill="x", pady=1)
            self._chk_widgets.append(chk)

            # Highlight row on hover
            def _enter(e, w=chk):
                w.config(bg=T["btn_hover"])
            def _leave(e, w=chk):
                w.config(bg=T["win_bg"])
            chk.bind("<Enter>", _enter)
            chk.bind("<Leave>", _leave)

    # ------------------------------------------------------------------ #
    #  Button strip  —  Ok | Cancel | Help | Select all  +  VMS 3000      #
    # ------------------------------------------------------------------ #

    def _create_buttons(self):
        strip = tk.Frame(self._dialog, bg=T["status_bg"], pady=12)
        strip.pack(fill="x")

        # Left cluster: Ok / Cancel / Help / Select all
        left = tk.Frame(strip, bg=T["status_bg"])
        left.pack(side="left", padx=16)

        ub = self._f("ui_b", size=9, weight="bold")

        def _btn(parent, text, cmd, style="normal"):
            if style == "primary":
                bg  = T["accent"];       fg  = T["text_white"]
                abg = T["accent_light"]; afg = T["text_white"]
            else:
                bg  = T["btn_face"];     fg  = T["text"]
                abg = T["btn_hover"];    afg = T["text"]

            b = tk.Button(
                parent,
                text=f"  {text}  ",
                command=cmd,
                font=ub,
                bg=bg, fg=fg,
                activebackground=abg, activeforeground=afg,
                relief="flat",
                bd=0,
                padx=12, pady=6,
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

        _btn(left, "Ok",         self._on_ok,         style="primary")
        _btn(left, "Cancel",     self._on_cancel)
        _btn(left, "Help",       self._on_help)
        _btn(left, "Select all", self._on_select_all)

        # Right: VMS 3000 badge — matches image bottom-right
        tk.Label(
            strip,
            text="  VMS 3000  ",
            font=self._f("ui_b", size=11, weight="bold"),
            bg=T["accent"],
            fg=T["text_white"],
            relief="flat",
            padx=10,
            pady=5,
        ).pack(side="right", padx=(0, 16))

    # ------------------------------------------------------------------ #
    #  Handlers                                                            #
    # ------------------------------------------------------------------ #

    def _on_ok(self):
        saved = {k: v.get() for k, v in self._vars.items()}
        print("Security Options saved:")
        for k, v in saved.items():
            print(f"  {k}: {'Enabled' if v else 'Disabled'}")
        self._dialog.destroy()

    def _on_cancel(self):
        self._dialog.destroy()

    def _on_select_all(self):
        for var in self._vars.values():
            var.set(True)

    def _on_help(self):
        dlg = self._subdialog("Security Options — Help", 500, 400)

        sm = self._f("sm",  size=9)
        ub = self._f("ui_b", size=9, weight="bold")

        body = tk.Frame(dlg, bg=T["win_bg"], padx=18, pady=14)
        body.pack(fill="both", expand=True)

        help_text = (
            "Change Setpoints in Program-Mode Only\n"
            "    Allows setpoint changes only when system is in Program mode.\n\n"
            "Disable Front Communication Port\n"
            "    Disables communication through the front panel port.\n\n"
            "Drive Rack Not OK Relay If Rack Address is Changed in Run Mode\n"
            "    Triggers the Not OK relay if rack address changes during Run mode.\n\n"
            "Drive Rack Not OK Relay if a Module is Removed or Inserted into the Rack\n"
            "    Triggers the Not OK relay when modules are added or removed.\n\n"
            "Drive Rack Not OK Relay If Key Switch is Changes from Program to Run Mode\n"
            "    Triggers the Not OK relay when key switch changes to Run mode.\n\n"
            "Disable VSM 3000 RCS Configuration Download in TCP/IP Communication Mode\n"
            "    Prevents RCS configuration downloads over TCP/IP.\n\n"
            "Refer to the VMS 3000 User Manual for full security configuration details."
        )

        tk.Label(
            body, text=help_text,
            font=sm, bg=T["win_bg"], fg=T["text"],
            justify="left", anchor="nw",
        ).pack(fill="both", expand=True)

        tk.Frame(body, bg=T["status_border"], height=1).pack(fill="x", pady=(10, 0))

        tk.Button(
            body, text="  Close  ", command=dlg.destroy,
            font=ub,
            bg=T["accent"], fg=T["text_white"],
            activebackground=T["accent_light"], activeforeground=T["text_white"],
            relief="flat", bd=0, padx=12, pady=5, cursor="hand2",
        ).pack(pady=(10, 0))

    # ------------------------------------------------------------------ #
    #  Sub-dialog factory                                                  #
    # ------------------------------------------------------------------ #

    def _subdialog(self, title, w, h):
        dlg = tk.Toplevel(self._dialog)
        dlg.title(title)
        dlg.configure(bg=T["win_bg"])
        dlg.resizable(False, False)
        dlg.grab_set()
        dlg.geometry(f"{w}x{h}")
        dlg.update_idletasks()
        dlg.geometry(
            f"+{self._dialog.winfo_x() + 40}+{self._dialog.winfo_y() + 50}"
        )

        ub = self._f("ui_b", size=10, weight="bold")

        hdr = tk.Frame(dlg, bg=T["titlebar"], pady=9)
        hdr.pack(fill="x")
        tk.Label(
            hdr, text=f"  {title}",
            font=ub, bg=T["titlebar"], fg=T["text_white"], anchor="w",
        ).pack(fill="x")

        tk.Frame(dlg, bg=T["accent_teal"], height=3).pack(fill="x")

        return dlg

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def show(self):
        """Display the dialog and block until it is closed."""
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

    popup = SecurityOptionsPopup(root, fonts)
    popup.show()
    root.destroy()