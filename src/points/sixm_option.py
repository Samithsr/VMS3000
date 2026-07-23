# """
# 6m-option.py — VMS 3000  •  3000/6M Options Dialog
# "3000/6M Options (Slot N)"

# Professional "card" UI matching the VMS 3000 design with configuration
# options for the 3000/6M module.
# """

# import tkinter as tk
# from tkinter import ttk
# import tkinter.font as tkfont


# # ══════════════════════════════════════════════════════════════════════════
# #  THEME
# # ══════════════════════════════════════════════════════════════════════════

# T = {
#     "win_bg":        "#eef1f6",
#     "group_border":  "#c9d3e0",
#     "titlebar":      "#1a3a5c",

#     "text":          "#1a2533",
#     "text_dim":      "#5a6a7a",

#     "card_bg":       "#ffffff",
#     "card_header":   "#0f6e7d",
#     "card_header_fg": "#ffffff",

#     "entry_bg":      "#ffffff",
#     "entry_border":  "#000000",

#     "btn_border":       "#b4bfcc",
#     "btn_primary":      "#1a4fa0",
#     "btn_primary_hov":  "#2a63bd",
#     "btn_primary_fg":   "#ffffff",
#     "btn_outline_fg":   "#1a3a5c",
#     "btn_outline_bd":   "#a9b7c8",
#     "btn_outline_hov":  "#e4edf9",

#     "accent_teal":   "#0891b2",
#     "vms_blue":      "#0d3fa0",
# }

# FONT_NAME = "Segoe UI"


# # ══════════════════════════════════════════════════════════════════════════
# #  Shared card / button helpers
# # ══════════════════════════════════════════════════════════════════════════

# def make_card(parent, title, header_font):
#     """White card panel with a teal accent header strip. Returns the body Frame."""
#     outer = tk.Frame(parent, bg=T["group_border"])
#     outer.pack(side="left", fill="both", expand=True, padx=6)

#     card = tk.Frame(outer, bg=T["card_bg"])
#     card.pack(fill="both", expand=True, padx=1, pady=1)

#     header = tk.Frame(card, bg=T["card_header"])
#     header.pack(fill="x")

#     spaced_title = " ".join(list(title.upper()))
#     tk.Label(
#         header, text=spaced_title, font=header_font,
#         bg=T["card_header"], fg=T["card_header_fg"],
#         anchor="w", padx=12, pady=6,
#     ).pack(fill="x")

#     body = tk.Frame(card, bg=T["card_bg"], padx=10, pady=10)
#     body.pack(fill="both", expand=True)
#     return body


# def make_pill_button(parent, text, command, font, kind="outline", enabled=True):
#     """Pill-style button: kind='primary' (solid navy) or 'outline' (bordered)."""
#     if kind == "primary":
#         bg, fg, hov, border = T["btn_primary"], T["btn_primary_fg"], T["btn_primary_hov"], T["btn_primary"]
#     else:
#         bg, fg, hov, border = T["card_bg"], T["btn_outline_fg"], T["btn_outline_hov"], T["btn_outline_bd"]

#     btn = tk.Button(
#         parent, text=text, command=command,
#         font=font, bg=bg, fg=fg,
#         activebackground=hov, activeforeground=fg,
#         relief="flat", bd=0, padx=16, pady=6,
#         cursor="hand2" if enabled else "arrow",
#         state="normal" if enabled else "disabled"
#     )
    
#     def on_enter(e):
#         if enabled:
#             btn.config(bg=hov)
    
#     def on_leave(e):
#         if enabled:
#             btn.config(bg=bg)
    
#     btn.bind("<Enter>", on_enter)
#     btn.bind("<Leave>", on_leave)
#     return btn


# # ══════════════════════════════════════════════════════════════════════════
# #  3000/6M Options Dialog
# # ══════════════════════════════════════════════════════════════════════════

# class SixMOptionsDialog:
#     """3000/6M Options Configuration dialog."""

#     def __init__(self, parent, slot_num):
#         self._parent = parent
#         self._slot_num = slot_num
#         self._dialog = None

#         # Configuration data
#         self.config_data = {
#             "channel_name": f"Channel {slot_num}",
#             "measurement_range": "0-10 mA",
#             "filter_setting": "50 Hz",
#             "alarm_enable": False,
#             "alarm_threshold": 5.0,
#             "units": "mA",
#         }

#     def show(self):
#         self._dialog = tk.Toplevel(self._parent)
#         self._dialog.title(f"3000/6M Options (Slot {self._slot_num})")
#         self._dialog.geometry("800x600")
#         self._dialog.configure(bg=T["win_bg"])
#         self._dialog.resizable(False, False)

#         # Fonts
#         self._f_title = tkfont.Font(family=FONT_NAME, size=12, weight="bold")
#         self._f_header = tkfont.Font(family=FONT_NAME, size=10, weight="bold")
#         self._f_body = tkfont.Font(family=FONT_NAME, size=9)
#         self._f_small = tkfont.Font(family=FONT_NAME, size=8)

#         # Main container
#         main = tk.Frame(self._dialog, bg=T["win_bg"])
#         main.pack(fill="both", expand=True, padx=16, pady=16)

#         # Title bar
#         title_frame = tk.Frame(main, bg=T["titlebar"], height=40)
#         title_frame.pack(fill="x", pady=(0, 12))
#         title_frame.pack_propagate(False)

#         tk.Label(
#             title_frame,
#             text=f"3000/6M OPTIONS - SLOT {self._slot_num}",
#             font=self._f_title,
#             bg=T["titlebar"],
#             fg="#ffffff",
#             anchor="w",
#             padx=16
#         ).pack(side="left", fill="y")

#         # Content area with cards
#         content = tk.Frame(main, bg=T["win_bg"])
#         content.pack(fill="both", expand=True)

#         # Row 1: Channel Configuration and Measurement Range
#         row1 = tk.Frame(content, bg=T["win_bg"])
#         row1.pack(fill="x", pady=(0, 8))

#         card1_body = make_card(row1, "Channel Configuration", self._f_header)
#         self._build_channel_config(card1_body)

#         card2_body = make_card(row1, "Measurement Range", self._f_header)
#         self._build_measurement_range(card2_body)

#         # Row 2: Alarm Settings and Filter Settings
#         row2 = tk.Frame(content, bg=T["win_bg"])
#         row2.pack(fill="x", pady=(0, 8))

#         card3_body = make_card(row2, "Alarm Settings", self._f_header)
#         self._build_alarm_settings(card3_body)

#         card4_body = make_card(row2, "Filter Settings", self._f_header)
#         self._build_filter_settings(card4_body)

#         # Row 3: Units and Display
#         row3 = tk.Frame(content, bg=T["win_bg"])
#         row3.pack(fill="x", pady=(0, 12))

#         card5_body = make_card(row3, "Units & Display", self._f_header)
#         self._build_units_display(card5_body)

#         # Bottom button bar
#         btn_frame = tk.Frame(main, bg=T["win_bg"])
#         btn_frame.pack(fill="x", pady=(8, 0))

#         make_pill_button(btn_frame, "OK", self._on_ok, self._f_body, kind="primary").pack(side="right", padx=4)
#         make_pill_button(btn_frame, "Cancel", self._on_cancel, self._f_body, kind="outline").pack(side="right", padx=4)
#         make_pill_button(btn_frame, "Defaults", self._on_defaults, self._f_body, kind="outline").pack(side="right", padx=4)
#         make_pill_button(btn_frame, "Apply", self._on_apply, self._f_body, kind="outline").pack(side="right", padx=4)

#         # Center the dialog on parent
#         self._dialog.update_idletasks()
#         x = self._parent.winfo_rootx() + (self._parent.winfo_width() - self._dialog.winfo_width()) // 2
#         y = self._parent.winfo_rooty() + (self._parent.winfo_height() - self._dialog.winfo_height()) // 2
#         self._dialog.geometry(f"+{x}+{y}")

#     def _build_channel_config(self, parent):
#         """Channel configuration card content."""
#         # Channel Name
#         tk.Label(parent, text="Channel Name:", font=self._f_body, bg=T["card_bg"], fg=T["text"]).grid(row=0, column=0, sticky="w", pady=4)
#         name_var = tk.StringVar(value=self.config_data["channel_name"])
#         tk.Entry(parent, textvariable=name_var, font=self._f_body, bg=T["entry_bg"], relief="solid", bd=1).grid(row=0, column=1, sticky="ew", padx=8, pady=4)

#         # Channel Number
#         tk.Label(parent, text="Channel Number:", font=self._f_body, bg=T["card_bg"], fg=T["text"]).grid(row=1, column=0, sticky="w", pady=4)
#         tk.Label(parent, text=str(self._slot_num), font=self._f_body, bg=T["card_bg"], fg=T["text_dim"]).grid(row=1, column=1, sticky="w", padx=8, pady=4)

#         parent.columnconfigure(1, weight=1)

#     def _build_measurement_range(self, parent):
#         """Measurement range card content."""
#         tk.Label(parent, text="Range:", font=self._f_body, bg=T["card_bg"], fg=T["text"]).grid(row=0, column=0, sticky="w", pady=4)
        
#         range_var = tk.StringVar(value=self.config_data["measurement_range"])
#         range_combo = ttk.Combobox(parent, textvariable=range_var, values=["0-10 mA", "4-20 mA", "0-5 V", "1-5 V"], font=self._f_body, state="readonly")
#         range_combo.grid(row=0, column=1, sticky="ew", padx=8, pady=4)

#         parent.columnconfigure(1, weight=1)

#     def _build_alarm_settings(self, parent):
#         """Alarm settings card content."""
#         # Alarm Enable checkbox
#         alarm_var = tk.BooleanVar(value=self.config_data["alarm_enable"])
#         tk.Checkbutton(parent, text="Enable Alarm", variable=alarm_var, font=self._f_body, bg=T["card_bg"], fg=T["text"], selectcolor=T["card_bg"]).grid(row=0, column=0, columnspan=2, sticky="w", pady=4)

#         # Alarm Threshold
#         tk.Label(parent, text="Alarm Threshold:", font=self._f_body, bg=T["card_bg"], fg=T["text"]).grid(row=1, column=0, sticky="w", pady=4)
#         threshold_var = tk.StringVar(value=str(self.config_data["alarm_threshold"]))
#         tk.Entry(parent, textvariable=threshold_var, font=self._f_body, bg=T["entry_bg"], relief="solid", bd=1, width=10).grid(row=1, column=1, sticky="w", padx=8, pady=4)

#         parent.columnconfigure(1, weight=1)

#     def _build_filter_settings(self, parent):
#         """Filter settings card content."""
#         tk.Label(parent, text="Filter Frequency:", font=self._f_body, bg=T["card_bg"], fg=T["text"]).grid(row=0, column=0, sticky="w", pady=4)
        
#         filter_var = tk.StringVar(value=self.config_data["filter_setting"])
#         filter_combo = ttk.Combobox(parent, textvariable=filter_var, values=["50 Hz", "60 Hz", "Off"], font=self._f_body, state="readonly")
#         filter_combo.grid(row=0, column=1, sticky="ew", padx=8, pady=4)

#         parent.columnconfigure(1, weight=1)

#     def _build_units_display(self, parent):
#         """Units and display card content."""
#         tk.Label(parent, text="Units:", font=self._f_body, bg=T["card_bg"], fg=T["text"]).grid(row=0, column=0, sticky="w", pady=4)
        
#         units_var = tk.StringVar(value=self.config_data["units"])
#         units_combo = ttk.Combobox(parent, textvariable=units_var, values=["mA", "V", "psi", "bar"], font=self._f_body, state="readonly")
#         units_combo.grid(row=0, column=1, sticky="ew", padx=8, pady=4)

#         # Display format
#         tk.Label(parent, text="Decimal Places:", font=self._f_body, bg=T["card_bg"], fg=T["text"]).grid(row=1, column=0, sticky="w", pady=4)
        
#         decimal_var = tk.StringVar(value="2")
#         decimal_combo = ttk.Combobox(parent, textvariable=decimal_var, values=["0", "1", "2", "3"], font=self._f_body, state="readonly", width=5)
#         decimal_combo.grid(row=1, column=1, sticky="w", padx=8, pady=4)

#         parent.columnconfigure(1, weight=1)

#     def _on_ok(self):
#         """OK button handler - save and close."""
#         print(f"OK clicked - Saving 3000/6M options for slot {self._slot_num}")
#         self._dialog.destroy()

#     def _on_cancel(self):
#         """Cancel button handler - close without saving."""
#         print(f"Cancel clicked - Discarding changes for slot {self._slot_num}")
#         self._dialog.destroy()

#     def _on_defaults(self):
#         """Defaults button handler - reset to default values."""
#         print(f"Defaults clicked - Resetting to defaults for slot {self._slot_num}")
#         self.config_data = {
#             "channel_name": f"Channel {self._slot_num}",
#             "measurement_range": "0-10 mA",
#             "filter_setting": "50 Hz",
#             "alarm_enable": False,
#             "alarm_threshold": 5.0,
#             "units": "mA",
#         }
#         self._dialog.destroy()
#         self.show()

#     def _on_apply(self):
#         """Apply button handler - save without closing."""
#         print(f"Apply clicked - Saving 3000/6M options for slot {self._slot_num}")


# # ══════════════════════════════════════════════════════════════════════════
# #  Standalone demo (for testing)
# # ══════════════════════════════════════════════════════════════════════════

# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("3000/6M Options Dialog Demo")
#     root.geometry("900x700")
    
#     demo_btn = tk.Button(root, text="Show 3000/6M Options Dialog", 
#                         command=lambda: SixMOptionsDialog(root, 3).show(),
#                         font=("Segoe UI", 12), padx=20, pady=10)
#     demo_btn.pack(expand=True)
    
#     root.mainloop()
/





























"""
sixm_option.py — VMS 3000  •  3000/6M Options Dialog
Clarity-first redesign of the 3000/6M Options Configuration Dialog.

Design goals for this version:
  - Big, legible text. No tiny labels, no tiny icons.
  - Plain English labels instead of abbreviations/all-caps jargon.
  - One clear primary action (OK), everything else visually secondary.
  - Simple top-to-bottom flow — read top, fill in, act at the bottom.
  - High contrast: dark text on white/light backgrounds, one accent color.
  - Generous spacing so nothing feels cramped or cluttered.
  - Still resizable / responsive, but simplicity comes first.
"""

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont


# ══════════════════════════════════════════════════════════════════════════
#  PALETTE — simple, high-contrast, one accent color
# ══════════════════════════════════════════════════════════════════════════

C = {
    "bg":            "#ffffff",   # everything sits on plain white
    "section_bg":    "#f7f8fa",   # light gray for grouped sections
    "border":        "#d7dbe0",

    "text":          "#111111",   # near-black, high contrast
    "text_dim":      "#5a6270",

    "accent":        "#1a56db",
    "accent_hover":  "#1544ad",
    "accent_text":   "#ffffff",

    "danger":        "#b3261e",

    "btn_bg":        "#ffffff",
    "btn_hover":     "#eef1f5",
    "btn_border":    "#c7ccd4",

    "field_bg":      "#ffffff",
    "field_border":  "#b9bfc8",

    "on_color":      "#1a7f37",
    "off_color":     "#9aa1ab",
}

FONT_NAME = "Segoe UI"


class SixMOptionsDialog:
    """Configuration dialog for 3000/6M Module (VMS 3000) — clarity-first UI."""

    def __init__(self, parent, slot_num=6, fonts=None,
                 rack_type="VMM/12T/DISP", config_id=""):
        self._parent    = parent
        self._slot_num  = slot_num
        self._fonts     = fonts if isinstance(fonts, dict) else {}
        self._rack_type = rack_type
        self._config_id = config_id
        self._dialog    = None

    def _f(self, key, family=FONT_NAME, size=11, weight="normal", slant="roman"):
        if not isinstance(self._fonts, dict):
            self._fonts = {}
        font = self._fonts.get(key)
        if font is None:
            font = tkfont.Font(family=family, size=size, weight=weight, slant=slant)
            self._fonts[key] = font
        return font

    # ── build ────────────────────────────────────────────────────────────
    def show(self):
        self._dialog = tk.Toplevel(self._parent)
        self._dialog.title("3000/6M Options Configuration")
        self._dialog.configure(bg=C["bg"])
        self._dialog.minsize(600, 500)
        self._dialog.transient(self._parent)
        self._dialog.grab_set()

        self._style_ttk()
        self._create_header()

        body = tk.Frame(self._dialog, bg=C["bg"], padx=24, pady=20)
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=1)

        row = 0
        self._create_identity_section(body).grid(row=row, column=0, sticky="ew")
        row += 1

        self._create_module_type_section(body).grid(row=row, column=0, sticky="ew", pady=(20, 0))
        row += 1

        tk.Label(
            body, text="Channels",
            font=self._f("section_heading", size=13, weight="bold"),
            bg=C["bg"], fg=C["text"], anchor="w",
        ).grid(row=row, column=0, sticky="w", pady=(24, 8))
        row += 1

        self._build_channel_section(body, "Channel 1").grid(row=row, column=0, sticky="ew", pady=(0, 12))
        row += 1
        self._build_channel_section(body, "Channel 2").grid(row=row, column=0, sticky="ew")
        row += 1

        body.rowconfigure(row, weight=1)
        spacer = tk.Frame(body, bg=C["bg"])
        spacer.grid(row=row, column=0, sticky="nsew")
        row += 1

        self._create_buttons(body).grid(row=row, column=0, sticky="ew", pady=(20, 0))

        self._dialog.update_idletasks()
        w, h = 680, 700
        sw = self._dialog.winfo_screenwidth()
        sh = self._dialog.winfo_screenheight()
        self._dialog.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    # ── ttk theming ──────────────────────────────────────────────────────
    def _style_ttk(self):
        style = ttk.Style(self._dialog)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Clear.TCombobox",
            fieldbackground=C["field_bg"],
            background=C["btn_bg"],
            foreground=C["text"],
            arrowcolor=C["text_dim"],
            bordercolor=C["field_border"],
            lightcolor=C["field_bg"],
            darkcolor=C["field_bg"],
            padding=8,
            relief="flat",
        )
        style.map(
            "Clear.TCombobox",
            fieldbackground=[("readonly", C["field_bg"])],
            foreground=[("readonly", C["text"])],
            bordercolor=[("focus", C["accent"])],
        )
        self._dialog.option_add("*TCombobox*Listbox.font", self._f("field", size=11))

    # ── header ───────────────────────────────────────────────────────────
    def _create_header(self):
        bar = tk.Frame(self._dialog, bg=C["bg"])
        bar.pack(fill="x", padx=24, pady=(20, 0))

        tk.Label(
            bar, text="3000/6M Options Configuration",
            font=self._f("title", size=17, weight="bold"),
            bg=C["bg"], fg=C["text"], anchor="w",
        ).pack(side="left")

        close_label = tk.Label(
            bar, text="Close",
            font=self._f("close_link", size=10, weight="bold"),
            bg=C["bg"], fg=C["accent"], cursor="hand2",
        )
        close_label.pack(side="right")
        close_label.bind("<Button-1>", lambda e: self._on_cancel())

        underline = tk.Frame(self._dialog, bg=C["border"], height=1)
        underline.pack(fill="x", padx=24, pady=(14, 0))

    # ── plain section box ────────────────────────────────────────────────
    def _section(self, parent, label=None):
        outer = tk.Frame(parent, bg=C["section_bg"], highlightthickness=1,
                          highlightbackground=C["border"])
        inner = tk.Frame(outer, bg=C["section_bg"], padx=16, pady=14)
        inner.pack(fill="both", expand=True)
        if label:
            tk.Label(
                inner, text=label, font=self._f("field_label", size=10, weight="bold"),
                bg=C["section_bg"], fg=C["text_dim"], anchor="w",
            ).pack(anchor="w", pady=(0, 6))
        outer.body = inner
        return outer

    # ── identity section ─────────────────────────────────────────────────
    def _create_identity_section(self, parent):
        wrap = self._section(parent, "Slot Information")
        grid = tk.Frame(wrap.body, bg=C["section_bg"])
        grid.pack(fill="x")
        grid.columnconfigure(0, weight=1, uniform="id")
        grid.columnconfigure(1, weight=1, uniform="id")
        grid.columnconfigure(2, weight=1, uniform="id")

        self._info_pair(grid, "Slot number", str(self._slot_num), col=0)
        self._info_pair(grid, "Rack type", self._rack_type, col=1)
        self._info_pair(grid, "Configuration ID", self._config_id or "Not set", col=2)

        return wrap

    def _info_pair(self, parent, label, value, col):
        cell = tk.Frame(parent, bg=C["section_bg"])
        cell.grid(row=0, column=col, sticky="w", padx=(0 if col == 0 else 16, 0))

        tk.Label(
            cell, text=label, bg=C["section_bg"], fg=C["text_dim"],
            font=self._f("small_label", size=9),
        ).pack(anchor="w")

        tk.Label(
            cell, text=value, bg=C["section_bg"], fg=C["text"],
            font=self._f("value", size=13, weight="bold"),
        ).pack(anchor="w", pady=(2, 0))

    # ── module type section ──────────────────────────────────────────────
    def _create_module_type_section(self, parent):
        wrap = self._section(parent, "Module Type")
        tk.Label(
            wrap.body, text="What kind of module is installed in this slot.",
            font=self._f("hint", size=9), bg=C["section_bg"], fg=C["text_dim"],
        ).pack(anchor="w", pady=(0, 8))

        combo = ttk.Combobox(
            wrap.body, values=["3000/6M Module"],
            font=self._f("field", size=11), state="readonly",
            style="Clear.TCombobox",
        )
        combo.set("3000/6M Module")
        combo.pack(fill="x")
        return wrap

    # ── channel sections ─────────────────────────────────────────────────
    def _build_channel_section(self, parent, ch_name):
        wrap = self._section(parent)
        row = tk.Frame(wrap.body, bg=C["section_bg"])
        row.pack(fill="x")
        row.columnconfigure(0, weight=1)

        left = tk.Frame(row, bg=C["section_bg"])
        left.grid(row=0, column=0, sticky="w")

        tk.Label(
            left, text=ch_name, font=self._f("channel_title", size=13, weight="bold"),
            bg=C["section_bg"], fg=C["text"],
        ).pack(anchor="w")

        self._status_toggle(left, ch_name)

        self._button(
            row, "Configure", lambda: self._on_options(ch_name),
            variant="secondary", width=12,
        ).grid(row=0, column=1, sticky="e")

        return wrap

    def _status_toggle(self, parent, ch_name):
        """Simple, clearly labeled on/off control — plain text, no icon guessing."""
        state = {"on": True}
        row = tk.Frame(parent, bg=C["section_bg"])
        row.pack(anchor="w", pady=(4, 0))

        dot = tk.Label(row, text="●", font=self._f("dot", size=11),
                        bg=C["section_bg"], fg=C["on_color"])
        dot.pack(side="left")

        status_label = tk.Label(
            row, text="Active — this channel is turned on", bg=C["section_bg"],
            fg=C["text_dim"], font=self._f("status_text", size=10), cursor="hand2",
        )
        status_label.pack(side="left", padx=(6, 0))

        hint = tk.Label(row, text="(click to change)", bg=C["section_bg"], fg=C["text_dim"],
                         font=self._f("tiny_hint", size=8))
        hint.pack(side="left", padx=(6, 0))

        def refresh():
            if state["on"]:
                dot.config(fg=C["on_color"])
                status_label.config(text="Active — this channel is turned on")
            else:
                dot.config(fg=C["off_color"])
                status_label.config(text="Inactive — this channel is turned off")

        def toggle(_e=None):
            state["on"] = not state["on"]
            refresh()
            print(f"{ch_name} Active = {state['on']}")

        status_label.bind("<Button-1>", toggle)
        dot.bind("<Button-1>", toggle)
        return state

    # ── buttons ──────────────────────────────────────────────────────────
    def _button(self, parent, text, cmd, width=None, variant="secondary"):
        palette = {
            "primary":   dict(bg=C["accent"], hover=C["accent_hover"], fg=C["accent_text"], border=C["accent"]),
            "secondary": dict(bg=C["btn_bg"], hover=C["btn_hover"], fg=C["text"], border=C["btn_border"]),
            "danger":    dict(bg=C["btn_bg"], hover=C["btn_hover"], fg=C["danger"], border=C["danger"]),
        }[variant]

        b = tk.Label(
            parent, text=text,
            font=self._f("btn", size=11, weight="bold" if variant == "primary" else "normal"),
            bg=palette["bg"], fg=palette["fg"],
            padx=18, pady=10, width=width, cursor="hand2",
            highlightthickness=1, highlightbackground=palette["border"],
        )

        def on_enter(_e):
            b.config(bg=palette["hover"])

        def on_leave(_e):
            b.config(bg=palette["bg"])

        def on_click(_e):
            cmd()

        b.bind("<Enter>", on_enter)
        b.bind("<Leave>", on_leave)
        b.bind("<Button-1>", on_click)
        return b

    def _create_buttons(self, parent):
        bar = tk.Frame(parent, bg=C["bg"])
        bar.columnconfigure(0, weight=1)

        left = tk.Frame(bar, bg=C["bg"])
        left.grid(row=0, column=0, sticky="w")
        self._button(left, "OK", self._on_ok, variant="primary", width=10).pack(side="left")
        self._button(left, "Cancel", self._on_cancel, variant="secondary", width=10).pack(side="left", padx=(10, 0))

        right = tk.Frame(bar, bg=C["bg"])
        right.grid(row=0, column=1, sticky="e")
        self._button(right, "Set Defaults", self._on_set_defaults, variant="secondary").pack(side="left")
        self._button(right, "Print", self._on_print, variant="secondary").pack(side="left", padx=(10, 0))
        self._button(right, "Help", self._on_help, variant="secondary").pack(side="left", padx=(10, 0))

        return bar

    # ── callbacks ────────────────────────────────────────────────────────
    def _on_options(self, channel_name):
        print(f"Open options for {channel_name}")

    def _on_ok(self):
        print("OK pressed")
        self._dialog.destroy()

    def _on_set_defaults(self):
        print("Set defaults pressed")

    def _on_cancel(self):
        self._dialog.destroy()

    def _on_print(self):
        print("Print pressed")

    def _on_help(self):
        print("Help pressed")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    dlg = SixMOptionsDialog(root, 6)
    dlg.show()
    root.mainloop()