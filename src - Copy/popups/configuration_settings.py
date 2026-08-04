"""
configuration_settings.py — VMS 3000  •  Configuration Settings Popup
Theme-matched to the industrial SCADA palette (navy/steel/amber/teal).
All colours, fonts, sizes and highlights come directly from T{}.
Single self-contained file — no external theme.py required.
"""

import tkinter as tk
import tkinter.font as tkfont
from .securityOption import SecurityOptionsPopup


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
#  POPUP CLASS
# ══════════════════════════════════════════════════════════════════════════════

class ConfigurationSettingsPopup:
    """
    Configuration Settings popup — VMS 3000 SCADA theme.

    Layout mirrors the reference image exactly:
      • Title row  : "Configuration Settings"  ·  [VMS 3000] badge
      • Password   : group-box  (Connect PW / Config PW)
      • Ethernet   : group-box  (Device Name / IP / Mask / GW / Port)
      • Buttons    : Ok  |  Security Opt  |  Cancel  |  Help
    """

    # ------------------------------------------------------------------ #
    #  Init                                                                #
    # ------------------------------------------------------------------ #

    def __init__(self, parent, fonts):
        self._fonts  = fonts
        self._parent = parent
        self._dialog = None
        self._vars   = {}          # field-key → tk.StringVar

        self._defaults = {
            "connect_password":    "",
            "config_password":     "",
            "network_device_name": "RACK0001",
            "rack_ip_address":     "192.168.1.255",
            "rack_subnet_mask":    "255.255.255.1",
            "gateway":             "192.168.1.1",
            "service_port_number": "502",
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
        self._dialog.title("Configuration Settings")
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

        self._create_password_group(body)
        self._create_ethernet_group(body)

        # ── Button strip ──────────────────────────────────────────────
        self._create_buttons()

        # ── Size & centre ─────────────────────────────────────────────
        self._dialog.update_idletasks()
        w, h = 500, 530
        sw = self._dialog.winfo_screenwidth()
        sh = self._dialog.winfo_screenheight()
        self._dialog.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    # ------------------------------------------------------------------ #
    #  Titlebar  — navy strip + VMS 3000 badge                            #
    # ------------------------------------------------------------------ #

    def _create_titlebar(self):
        bar = tk.Frame(self._dialog, bg=T["titlebar"], pady=10)
        bar.pack(fill="x")

        # Left: dialog title in white bold
        tk.Label(
            bar,
            text="  Configuration Settings",
            font=self._f("ui_b", size=11, weight="bold"),
            bg=T["titlebar"],
            fg=T["text_white"],
            anchor="w",
        ).pack(side="left", fill="x", expand=True)

        # Right: VMS 3000 badge — accent-blue bg, white text, rounded look
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

    # ------------------------------------------------------------------ #
    #  LabelFrame helper                                                   #
    # ------------------------------------------------------------------ #

    def _group(self, parent, title):
        """Styled LabelFrame matching the SCADA palette."""
        return tk.LabelFrame(
            parent,
            text=f"  {title}  ",
            font=self._f("sm_b", size=9, weight="bold"),
            bg=T["win_bg"],
            fg=T["accent"],           # navy-blue group-box label
            bd=2,
            relief="groove",
            padx=14,
            pady=10,
        )

    # ------------------------------------------------------------------ #
    #  Group boxes                                                         #
    # ------------------------------------------------------------------ #

    def _create_password_group(self, parent):
        grp = self._group(parent, "Password")
        grp.pack(fill="x", pady=(0, 10))

        self._field(grp, "Connect Password :",       "connect_password",    pw=True)
        self._field(grp, "Configuration Password :", "config_password",     pw=True)

    def _create_ethernet_group(self, parent):
        grp = self._group(parent, "Ethernet [TCP/IP]")
        grp.pack(fill="x", pady=(0, 10))

        self._field(grp, "Network Device Name :", "network_device_name", pw=False)
        self._field(grp, "Rack IP Address :",     "rack_ip_address",     pw=False)
        self._field(grp, "Rack Subnet Mask :",    "rack_subnet_mask",    pw=False)
        self._field(grp, "Gateway :",             "gateway",             pw=False)
        self._field(grp, "Service Port Number :", "service_port_number", pw=False)

    # ------------------------------------------------------------------ #
    #  Field row: bold label  +  highlighted entry                        #
    # ------------------------------------------------------------------ #

    def _field(self, parent, label_text, key, *, pw):
        """
        Two-column row:
          col 0 — bold dark label, right-aligned, fixed width
          col 1 — wide sunken entry with teal focus ring
        """
        row = tk.Frame(parent, bg=T["win_bg"])
        row.pack(fill="x", pady=4)

        # Bold label — navy text colour from theme
        lbl = tk.Label(
            row,
            text=label_text,
            font=self._f("sm_b", size=9, weight="bold"),   # BOLD
            bg=T["win_bg"],
            fg=T["text"],          # dark navy #1a2533
            anchor="e",
            width=26,              # fixed width → entries share left edge
        )
        lbl.pack(side="left")

        var = tk.StringVar(value=self._defaults.get(key, ""))
        self._vars[key] = var

        # Entry — white bg, navy text, teal highlight border on focus
        entry = tk.Entry(
            row,
            textvariable=var,
            font=self._f("mono", family="Consolas", size=10),
            bg="#ffffff",           # white field
            fg=T["text"],           # navy text
            insertbackground=T["accent_teal"],
            selectbackground=T["accent_light"],
            selectforeground=T["text_white"],
            relief="solid",
            bd=1,
            highlightthickness=2,
            highlightbackground=T["btn_border"],
            highlightcolor=T["accent_teal"],   # teal glow on focus
            width=22,              # wider than before
            show="*" if pw else "",
        )
        entry.pack(side="left", padx=(8, 0))

        # Hover colour effect
        def _on_enter(e):
            entry.config(highlightbackground=T["accent_light"])
        def _on_leave(e):
            entry.config(highlightbackground=T["btn_border"])

        entry.bind("<Enter>", _on_enter)
        entry.bind("<Leave>", _on_leave)

    # ------------------------------------------------------------------ #
    #  Button strip  —  Ok | Security Opt | Cancel | Help                 #
    # ------------------------------------------------------------------ #

    def _create_buttons(self):
        # Slightly recessed footer strip
        strip = tk.Frame(
            self._dialog,
            bg=T["status_bg"],
            pady=12,
            relief="flat",
            bd=0,
        )
        # Top border line
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
            elif style == "amber":
                bg  = T["led_amber"]
                fg  = "#1a1a00"
                abg = "#d48800"
                afg = "#1a1a00"
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

            # Hover effects
            def _e(ev): b.config(bg=abg, fg=afg)
            def _l(ev): b.config(bg=bg,  fg=fg)
            b.bind("<Enter>", _e)
            b.bind("<Leave>", _l)
            return b

        _btn("Ok",           self._on_ok,           style="primary")
        _btn("Security Opt", self._on_security_opt, style="amber")
        _btn("Cancel",       self._on_cancel,       style="normal")
        _btn("Help",         self._on_help,         style="normal")

    # ------------------------------------------------------------------ #
    #  Handlers                                                            #
    # ------------------------------------------------------------------ #

    def _on_ok(self):
        saved = {k: v.get() for k, v in self._vars.items()}
        print("Configuration saved:")
        for k, v in saved.items():
            if "password" not in k:
                print(f"  {k}: {v}")
        self._dialog.destroy()

    def _on_cancel(self):
        self._dialog.destroy()

    # ── Security Opt ──────────────────────────────────────────────────── #

    def _on_security_opt(self):
        """Open Security Options popup dialog."""
        popup = SecurityOptionsPopup(self._dialog, self._fonts)
        popup.show()

    # ── Help ──────────────────────────────────────────────────────────── #

    def _on_help(self):
        dlg = self._subdialog("Configuration Settings — Help", 480, 400)

        sm = self._f("sm",  size=9)
        ub = self._f("ui_b", size=9, weight="bold")

        body = tk.Frame(dlg, bg=T["win_bg"], padx=18, pady=14)
        body.pack(fill="both", expand=True)

        help_text = (
            "Connect Password\n"
            "    Password required to connect to the rack device.\n\n"
            "Configuration Password\n"
            "    Password required to access configuration settings.\n\n"
            "Network Device Name\n"
            "    Unique identifier for the rack on the network.\n\n"
            "Rack IP Address\n"
            "    Static IP address assigned to the rack unit.\n\n"
            "Rack Subnet Mask\n"
            "    Subnet mask for network segmentation.\n\n"
            "Gateway\n"
            "    Default gateway for outbound network routing.\n\n"
            "Service Port Number\n"
            "    TCP port used for Modbus / service communication (default 502).\n\n"
            "Security Options\n"
            "    SSL/TLS         — Enables encrypted transport layer.\n"
            "    Data Encryption — Encrypts payload data in transit.\n"
            "    Two-Factor Auth — Requires second authentication factor.\n\n"
            "Refer to the VMS 3000 User Manual for full details."
        )

        tk.Label(
            body, text=help_text,
            font=sm,
            bg=T["win_bg"],
            fg=T["text"],
            justify="left", anchor="nw",
        ).pack(fill="both", expand=True)

        tk.Frame(body, bg=T["status_border"], height=1).pack(fill="x", pady=(10, 0))

        tk.Button(
            body, text="  Close  ", command=dlg.destroy,
            font=ub,
            bg=T["accent"], fg=T["text_white"],
            activebackground=T["accent_light"],
            activeforeground=T["text_white"],
            relief="flat", bd=0,
            padx=12, pady=5,
            cursor="hand2",
        ).pack(pady=(10, 0))

    # ------------------------------------------------------------------ #
    #  Sub-dialog factory                                                  #
    # ------------------------------------------------------------------ #

    def _subdialog(self, title, w, h):
        """Create a themed child dialog with navy titlebar + teal rule."""
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

        # Navy titlebar
        hdr = tk.Frame(dlg, bg=T["titlebar"], pady=9)
        hdr.pack(fill="x")
        tk.Label(
            hdr, text=f"  {title}",
            font=ub, bg=T["titlebar"], fg=T["text_white"], anchor="w",
        ).pack(fill="x")

        # Teal rule
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

    popup = ConfigurationSettingsPopup(root, fonts)
    popup.show()
    root.destroy()