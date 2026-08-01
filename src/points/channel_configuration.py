"""
channel_configuration.py — VMS 3000  •  Channel-N Configuration Dialog
Exact visual match to the reference screenshots:
  - "Channel-N Configuration" titlebar (navy, white text) with red close box
  - CHANNEL / 'ACTIVE' / SLOT / RACK TYPE identity strip
  - Two-tab strip: "Transducer setup" (active) | "Variables + Alarms"
  - "Transducer Setup" group containing:
        "Transducer Selection"  -> Type: 3000- 8mm Proximeter (dropdown)
        "Transducer Direction"  -> Towards Probe / Away From Probe (radio, disabled)
  - Bottom button row: Ok, Set defaults, Cancel | Print, Help | VMS 3000 logo
"""

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont


# ══════════════════════════════════════════════════════════════════════════
#  PALETTE — colours matched from the reference screenshots
# ══════════════════════════════════════════════════════════════════════════

C = {
    "win_bg":          "#f0f0f0",   # pale grey dialog background
    "titlebar":        "#1a3a5c",   # navy titlebar
    "titlebar_text":   "#ffffff",
    "close_bg":        "#c0392b",

    "field_bg":        "#eef1f5",   # SLOT / RACK TYPE display box
    "field_border":    "#6b7280",

    "group_bg":        "#f0f0f0",
    "group_border":    "#8a8f98",
    "group_label":     "#000000",

    "tab_bg":          "#e6e9ee",
    "tab_active_bg":   "#f0f0f0",
    "tab_border":      "#8a8f98",
    "tab_text":        "#000000",

    "combo_bg":        "#ffffff",
    "combo_fg":        "#1a3a8c",

    "btn_face":        "#e7e9ec",
    "btn_hover":       "#f2f4f6",
    "btn_press":       "#cfd4da",
    "btn_border":      "#5a5a5a",
    "btn_disabled_fg": "#8895a6",

    "text":            "#000000",
    "text_dim":        "#4a5568",
    "text_disabled":   "#8a93a0",

    "vms_logo":        "#17408a",
}

FONT_NAME = "Segoe UI"


class ChannelConfigurationDialog:
    """
    Channel-N Configuration dialog for a single channel of a
    Proximeter I/O Module (DIS_MODULE) — exact match to the reference
    screenshots for Channel-1 .. Channel-4.
    """

    def __init__(self, parent, channel_num, slot_num=1, fonts=None,
                 rack_type="VMM/12T/DISP", active=True,
                 transducer_type="3000- 8mm Proximeter",
                 direction="Towards Probe"):
        """
        Args:
            parent: Parent widget
            channel_num: Channel number (1, 2, 3, or 4)
            slot_num: Slot number housing this channel's module
            fonts: Optional shared font dictionary
            rack_type: Rack type text shown in the identity strip
            active: Whether the channel is marked 'ACTIVE'
            transducer_type: Preselected transducer type
            direction: Preselected transducer direction
        """
        self._parent          = parent
        self._channel_num     = channel_num
        self._slot_num        = slot_num
        self._fonts           = fonts if isinstance(fonts, dict) else {}
        self._rack_type       = rack_type
        self._active          = active
        self._transducer_type = transducer_type
        self._direction       = tk.StringVar(value=direction)
        self._dialog           = None

    def _f(self, key, family=FONT_NAME, size=9, weight="normal", slant="roman"):
        if not isinstance(self._fonts, dict):
            self._fonts = {}
        font = self._fonts.get(key)
        if font is None:
            font = tkfont.Font(family=family, size=size, weight=weight, slant=slant)
            self._fonts[key] = font
        return font

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def show(self):
        self._dialog = tk.Toplevel(self._parent)
        self._dialog.title(f"Channel-{self._channel_num} Configuration")
        self._dialog.configure(bg=C["win_bg"])
        self._dialog.resizable(False, False)
        self._dialog.transient(self._parent)
        self._dialog.grab_set()

        self._style_ttk()

        self._create_titlebar()

        body = tk.Frame(self._dialog, bg=C["win_bg"], padx=14, pady=10)
        body.pack(fill="both", expand=True)

        self._create_identity_row(body)

        self._create_tabs(body)

        self._create_buttons(body)

        self._dialog.update_idletasks()
        w, h = 620, 460
        sw = self._dialog.winfo_screenwidth()
        sh = self._dialog.winfo_screenheight()
        self._dialog.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

        return self._dialog

    # ------------------------------------------------------------------ #
    #  ttk styling                                                         #
    # ------------------------------------------------------------------ #

    def _style_ttk(self):
        style = ttk.Style(self._dialog)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Channel.TCombobox",
            fieldbackground=C["combo_bg"],
            background=C["btn_face"],
            foreground=C["combo_fg"],
            arrowcolor=C["text"],
            bordercolor=C["field_border"],
            lightcolor=C["combo_bg"],
            darkcolor=C["field_border"],
            padding=3,
        )
        style.map("Channel.TCombobox",
                  fieldbackground=[("readonly", C["combo_bg"])],
                  foreground=[("readonly", C["combo_fg"])])

    # ------------------------------------------------------------------ #
    #  Titlebar                                                            #
    # ------------------------------------------------------------------ #

    def _create_titlebar(self):
        bar = tk.Frame(self._dialog, bg=C["titlebar"], height=26)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        tk.Label(
            bar, text=f"  Channel-{self._channel_num} Configuration",
            font=self._f("title", size=10, weight="bold"),
            bg=C["titlebar"], fg=C["titlebar_text"], anchor="w",
        ).pack(side="left", fill="both", expand=True)

        tk.Button(
            bar, text="\u2715", font=self._f("close", size=8),
            bg=C["close_bg"], fg="#ffffff", bd=1, relief="raised",
            width=3, command=self._on_cancel,
        ).pack(side="right", padx=4, pady=3)

    # ------------------------------------------------------------------ #
    #  Identity row  —  CHANNEL / 'ACTIVE' / SLOT / RACK TYPE               #
    # ------------------------------------------------------------------ #

    def _create_identity_row(self, parent):
        row = tk.Frame(parent, bg=C["win_bg"])
        row.pack(fill="x", pady=(0, 10))

        left = tk.Frame(row, bg=C["win_bg"])
        left.pack(side="left", anchor="w")

        # CHANNEL label + number box
        tk.Label(
            left, text="CHANNEL", bg=C["win_bg"], fg=C["text"],
            font=self._f("label_b", size=9, weight="bold"),
        ).pack(side="left")

        tk.Label(
            left, text=str(self._channel_num), bg=C["field_bg"], fg=C["text"],
            font=self._f("field", size=9, weight="bold"),
            width=3, anchor="center", relief="sunken", bd=2,
            highlightthickness=1, highlightbackground=C["field_border"],
        ).pack(side="left", padx=(6, 14))

        # 'ACTIVE' status box
        status_text = "'ACTIVE'" if self._active else "'INACTIVE'"
        tk.Label(
            left, text=status_text, bg=C["win_bg"], fg=C["text"],
            font=self._f("field_b", size=9, weight="bold"),
            relief="groove", bd=2, padx=8, pady=2,
        ).pack(side="left", padx=(0, 24))

        # SLOT label + number box
        tk.Label(
            left, text="SLOT", bg=C["win_bg"], fg=C["text"],
            font=self._f("label_b", size=9, weight="bold"),
        ).pack(side="left")

        tk.Label(
            left, text=str(self._slot_num), bg=C["field_bg"], fg=C["text"],
            font=self._f("field", size=9, weight="bold"),
            width=3, anchor="center", relief="sunken", bd=2,
            highlightthickness=1, highlightbackground=C["field_border"],
        ).pack(side="left", padx=(6, 0))

        # RACK TYPE label + value box (right aligned)
        right = tk.Frame(row, bg=C["win_bg"])
        right.pack(side="right", anchor="e")

        tk.Label(
            right, text="RACK TYPE", bg=C["win_bg"], fg=C["text"],
            font=self._f("label_b", size=9, weight="bold"),
        ).pack(side="left")

        tk.Label(
            right, text=self._rack_type, bg=C["field_bg"], fg=C["text"],
            font=self._f("field", size=9, weight="bold"),
            width=14, anchor="center", relief="sunken", bd=2,
            highlightthickness=1, highlightbackground=C["field_border"],
        ).pack(side="left", padx=(6, 0))

    # ------------------------------------------------------------------ #
    #  Tabs  —  "Transducer setup" | "Variables + Alarms"                   #
    # ------------------------------------------------------------------ #

    def _create_tabs(self, parent):
        container = tk.Frame(parent, bg=C["win_bg"])
        container.pack(fill="both", expand=True)

        # ── Tab strip ────────────────────────────────────────────────
        strip = tk.Frame(container, bg=C["win_bg"])
        strip.pack(fill="x")

        self._tab_buttons = {}
        self._active_tab = tk.StringVar(value="transducer")

        self._add_tab(strip, "Transducer setup", "transducer")
        self._add_tab(strip, "Variables + Alarms", "variables")

        # ── Panel frame (bordered, sits under the tab strip) ───────────
        panel_frame = tk.Frame(
            container, bg=C["win_bg"], bd=1, relief="solid",
            highlightbackground=C["tab_border"], highlightthickness=1,
        )
        panel_frame.pack(fill="both", expand=True)

        self._transducer_panel = self._build_transducer_panel(panel_frame)
        self._variables_panel = self._build_variables_panel(panel_frame)

        self._show_tab("transducer")

    def _add_tab(self, strip, label, key):
        btn = tk.Label(
            strip, text=f"  {label}  ",
            font=self._f("tab", size=9),
            bg=C["tab_active_bg"] if key == "transducer" else C["tab_bg"],
            fg=C["tab_text"],
            relief="solid", bd=1,
            highlightbackground=C["tab_border"],
            padx=6, pady=4, cursor="hand2",
        )
        btn.pack(side="left", padx=(0, 2), anchor="s")
        btn.bind("<Button-1>", lambda e, k=key: self._show_tab(k))
        self._tab_buttons[key] = btn

    def _show_tab(self, key):
        self._active_tab.set(key)
        for k, btn in self._tab_buttons.items():
            btn.configure(bg=C["tab_active_bg"] if k == key else C["tab_bg"])

        self._transducer_panel.pack_forget()
        self._variables_panel.pack_forget()

        if key == "transducer":
            self._transducer_panel.pack(fill="both", expand=True, padx=10, pady=10)
        else:
            self._variables_panel.pack(fill="both", expand=True, padx=10, pady=10)

    # ------------------------------------------------------------------ #
    #  Group-box helper                                                    #
    # ------------------------------------------------------------------ #

    def _group(self, parent, title):
        return tk.LabelFrame(
            parent, text=f" {title} ",
            font=self._f("group", size=9, weight="bold"),
            bg=C["group_bg"], fg=C["group_label"],
            bd=1, relief="groove",
            highlightbackground=C["group_border"],
            padx=12, pady=10,
        )

    # ------------------------------------------------------------------ #
    #  "Transducer setup" tab panel                                        #
    # ------------------------------------------------------------------ #

    def _build_transducer_panel(self, parent):
        outer = self._group(parent, "Transducer Setup")

        # Transducer Selection group
        sel_group = self._group(outer, "Transducer Selection")
        sel_group.pack(fill="x", pady=(0, 12))

        type_row = tk.Frame(sel_group, bg=C["win_bg"])
        type_row.pack(fill="x")

        tk.Label(
            type_row, text="Type", bg=C["win_bg"], fg=C["text"],
            font=self._f("label_b", size=9, weight="bold"),
        ).pack(side="left", padx=(0, 8))

        combo = ttk.Combobox(
            type_row, values=[self._transducer_type],
            font=self._f("field", size=9), state="readonly",
            style="Channel.TCombobox", width=28,
        )
        combo.set(self._transducer_type)
        combo.pack(side="left")

        # Transducer Direction group (disabled — single transducer type)
        dir_group = self._group(outer, "Transducer Direction")
        dir_group.pack(fill="x")

        tk.Radiobutton(
            dir_group, text="Towards Probe",
            variable=self._direction, value="Towards Probe",
            bg=C["win_bg"], fg=C["text_disabled"],
            activebackground=C["win_bg"], activeforeground=C["text_disabled"],
            selectcolor="#ffffff",
            font=self._f("field", size=9),
            state="disabled",
        ).pack(anchor="w", pady=(0, 4))

        tk.Radiobutton(
            dir_group, text="Away From Probe",
            variable=self._direction, value="Away From Probe",
            bg=C["win_bg"], fg=C["text_disabled"],
            activebackground=C["win_bg"], activeforeground=C["text_disabled"],
            selectcolor="#ffffff",
            font=self._f("field", size=9),
            state="disabled",
        ).pack(anchor="w")

        return outer

    # ------------------------------------------------------------------ #
    #  "Variables + Alarms" tab panel (placeholder, same shell)            #
    # ------------------------------------------------------------------ #

    def _build_variables_panel(self, parent):
        outer = self._group(parent, "Variables + Alarms")

        tk.Label(
            outer,
            text="Variables + Alarms settings for this channel.",
            font=self._f("field", size=9),
            bg=C["win_bg"], fg=C["text_dim"],
        ).pack(anchor="w", pady=(4, 0))

        return outer

    # ------------------------------------------------------------------ #
    #  Classic raised, beveled button                                      #
    # ------------------------------------------------------------------ #

    def _raised_btn(self, parent, text, cmd, width=None, enabled=True):
        b = tk.Button(
            parent, text=text, command=cmd,
            font=self._f("field", size=9),
            bg=C["btn_face"], fg=C["text"],
            activebackground=C["btn_press"], activeforeground=C["text"],
            disabledforeground=C["btn_disabled_fg"],
            relief="raised", bd=2,
            highlightthickness=1, highlightbackground=C["btn_border"],
            width=width, state="normal" if enabled else "disabled",
            cursor="hand2" if enabled else "arrow",
        )
        if enabled:
            b.bind("<Enter>", lambda e: b.config(bg=C["btn_hover"]))
            b.bind("<Leave>", lambda e: b.config(bg=C["btn_face"]))
        return b

    # ------------------------------------------------------------------ #
    #  Bottom button bar                                                   #
    # ------------------------------------------------------------------ #

    def _create_buttons(self, parent):
        bar = tk.Frame(parent, bg=C["win_bg"])
        bar.pack(fill="x", pady=(12, 0))

        left = tk.Frame(bar, bg=C["win_bg"])
        left.pack(side="left")
        self._raised_btn(left, "Ok", self._on_ok, width=10).pack(side="left")
        self._raised_btn(left, "Set defaults", self._on_set_defaults, width=12).pack(side="left", padx=(8, 0))
        self._raised_btn(left, "Cancel", self._on_cancel, width=10).pack(side="left", padx=(8, 0))

        mid = tk.Frame(bar, bg=C["win_bg"])
        mid.pack(side="left", padx=(60, 0))
        self._raised_btn(mid, "Print", self._on_print, width=10).pack(side="left")
        self._raised_btn(mid, "Help", self._on_help, width=10).pack(side="left", padx=(8, 0))

        tk.Label(
            bar, text="VMS 3000",
            font=self._f("logo", family="Segoe UI", size=15, weight="bold", slant="italic"),
            bg=C["win_bg"], fg=C["vms_logo"],
        ).pack(side="right")

    # ------------------------------------------------------------------ #
    #  Handlers                                                            #
    # ------------------------------------------------------------------ #

    def _on_ok(self):
        print(f"Channel-{self._channel_num} OK pressed")
        self._dialog.destroy()

    def _on_set_defaults(self):
        print(f"Channel-{self._channel_num} Set defaults pressed")

    def _on_cancel(self):
        self._dialog.destroy()

    def _on_print(self):
        print(f"Channel-{self._channel_num} Print pressed")

    def _on_help(self):
        print(f"Channel-{self._channel_num} Help pressed")


# ══════════════════════════════════════════════════════════════════════
#  Standalone preview
# ══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    dlg = ChannelConfigurationDialog(root, 1, slot_num=1)   # (parent, channel_num, slot_num)
    dlg.show()
    root.mainloop()