"""
6m-option.py — VMS 3000  •  3000/6M Options Dialog
"3000/6M Options (Slot N)"

Professional "card" UI matching the VMS 3000 design with configuration
options for the 3000/6M module.
"""

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont


# ══════════════════════════════════════════════════════════════════════════
#  THEME
# ══════════════════════════════════════════════════════════════════════════

T = {
    "win_bg":        "#eef1f6",
    "group_border":  "#c9d3e0",
    "titlebar":      "#1a3a5c",

    "text":          "#1a2533",
    "text_dim":      "#5a6a7a",

    "card_bg":       "#ffffff",
    "card_header":   "#0f6e7d",
    "card_header_fg": "#ffffff",

    "entry_bg":      "#ffffff",
    "entry_border":  "#000000",

    "btn_border":       "#b4bfcc",
    "btn_primary":      "#1a4fa0",
    "btn_primary_hov":  "#2a63bd",
    "btn_primary_fg":   "#ffffff",
    "btn_outline_fg":   "#1a3a5c",
    "btn_outline_bd":   "#a9b7c8",
    "btn_outline_hov":  "#e4edf9",

    "accent_teal":   "#0891b2",
    "vms_blue":      "#0d3fa0",
}

FONT_NAME = "Segoe UI"


# ══════════════════════════════════════════════════════════════════════════
#  Shared card / button helpers
# ══════════════════════════════════════════════════════════════════════════

def make_card(parent, title, header_font):
    """White card panel with a teal accent header strip. Returns the body Frame."""
    outer = tk.Frame(parent, bg=T["group_border"])
    outer.pack(side="left", fill="both", expand=True, padx=6)

    card = tk.Frame(outer, bg=T["card_bg"])
    card.pack(fill="both", expand=True, padx=1, pady=1)

    header = tk.Frame(card, bg=T["card_header"])
    header.pack(fill="x")

    spaced_title = " ".join(list(title.upper()))
    tk.Label(
        header, text=spaced_title, font=header_font,
        bg=T["card_header"], fg=T["card_header_fg"],
        anchor="w", padx=12, pady=6,
    ).pack(fill="x")

    body = tk.Frame(card, bg=T["card_bg"], padx=10, pady=10)
    body.pack(fill="both", expand=True)
    return body


def make_pill_button(parent, text, command, font, kind="outline", enabled=True):
    """Pill-style button: kind='primary' (solid navy) or 'outline' (bordered)."""
    if kind == "primary":
        bg, fg, hov, border = T["btn_primary"], T["btn_primary_fg"], T["btn_primary_hov"], T["btn_primary"]
    else:
        bg, fg, hov, border = T["card_bg"], T["btn_outline_fg"], T["btn_outline_hov"], T["btn_outline_bd"]

    btn = tk.Button(
        parent, text=text, command=command,
        font=font, bg=bg, fg=fg,
        activebackground=hov, activeforeground=fg,
        relief="flat", bd=0, padx=16, pady=6,
        cursor="hand2" if enabled else "arrow",
        state="normal" if enabled else "disabled"
    )
    
    def on_enter(e):
        if enabled:
            btn.config(bg=hov)
    
    def on_leave(e):
        if enabled:
            btn.config(bg=bg)
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


# ══════════════════════════════════════════════════════════════════════════
#  3000/6M Options Dialog
# ══════════════════════════════════════════════════════════════════════════

class SixMOptionsDialog:
    """3000/6M Options Configuration dialog."""

    def __init__(self, parent, slot_num):
        self._parent = parent
        self._slot_num = slot_num
        self._dialog = None

        # Configuration data
        self.config_data = {
            "channel_name": f"Channel {slot_num}",
            "measurement_range": "0-10 mA",
            "filter_setting": "50 Hz",
            "alarm_enable": False,
            "alarm_threshold": 5.0,
            "units": "mA",
        }

    def show(self):
        self._dialog = tk.Toplevel(self._parent)
        self._dialog.title(f"3000/6M Options (Slot {self._slot_num})")
        self._dialog.geometry("800x600")
        self._dialog.configure(bg=T["win_bg"])
        self._dialog.resizable(False, False)

        # Fonts
        self._f_title = tkfont.Font(family=FONT_NAME, size=12, weight="bold")
        self._f_header = tkfont.Font(family=FONT_NAME, size=10, weight="bold")
        self._f_body = tkfont.Font(family=FONT_NAME, size=9)
        self._f_small = tkfont.Font(family=FONT_NAME, size=8)

        # Main container
        main = tk.Frame(self._dialog, bg=T["win_bg"])
        main.pack(fill="both", expand=True, padx=16, pady=16)

        # Title bar
        title_frame = tk.Frame(main, bg=T["titlebar"], height=40)
        title_frame.pack(fill="x", pady=(0, 12))
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text=f"3000/6M OPTIONS - SLOT {self._slot_num}",
            font=self._f_title,
            bg=T["titlebar"],
            fg="#ffffff",
            anchor="w",
            padx=16
        ).pack(side="left", fill="y")

        # Content area with cards
        content = tk.Frame(main, bg=T["win_bg"])
        content.pack(fill="both", expand=True)

        # Row 1: Channel Configuration and Measurement Range
        row1 = tk.Frame(content, bg=T["win_bg"])
        row1.pack(fill="x", pady=(0, 8))

        card1_body = make_card(row1, "Channel Configuration", self._f_header)
        self._build_channel_config(card1_body)

        card2_body = make_card(row1, "Measurement Range", self._f_header)
        self._build_measurement_range(card2_body)

        # Row 2: Alarm Settings and Filter Settings
        row2 = tk.Frame(content, bg=T["win_bg"])
        row2.pack(fill="x", pady=(0, 8))

        card3_body = make_card(row2, "Alarm Settings", self._f_header)
        self._build_alarm_settings(card3_body)

        card4_body = make_card(row2, "Filter Settings", self._f_header)
        self._build_filter_settings(card4_body)

        # Row 3: Units and Display
        row3 = tk.Frame(content, bg=T["win_bg"])
        row3.pack(fill="x", pady=(0, 12))

        card5_body = make_card(row3, "Units & Display", self._f_header)
        self._build_units_display(card5_body)

        # Bottom button bar
        btn_frame = tk.Frame(main, bg=T["win_bg"])
        btn_frame.pack(fill="x", pady=(8, 0))

        make_pill_button(btn_frame, "OK", self._on_ok, self._f_body, kind="primary").pack(side="right", padx=4)
        make_pill_button(btn_frame, "Cancel", self._on_cancel, self._f_body, kind="outline").pack(side="right", padx=4)
        make_pill_button(btn_frame, "Defaults", self._on_defaults, self._f_body, kind="outline").pack(side="right", padx=4)
        make_pill_button(btn_frame, "Apply", self._on_apply, self._f_body, kind="outline").pack(side="right", padx=4)

        # Center the dialog on parent
        self._dialog.update_idletasks()
        x = self._parent.winfo_rootx() + (self._parent.winfo_width() - self._dialog.winfo_width()) // 2
        y = self._parent.winfo_rooty() + (self._parent.winfo_height() - self._dialog.winfo_height()) // 2
        self._dialog.geometry(f"+{x}+{y}")

    def _build_channel_config(self, parent):
        """Channel configuration card content."""
        # Channel Name
        tk.Label(parent, text="Channel Name:", font=self._f_body, bg=T["card_bg"], fg=T["text"]).grid(row=0, column=0, sticky="w", pady=4)
        name_var = tk.StringVar(value=self.config_data["channel_name"])
        tk.Entry(parent, textvariable=name_var, font=self._f_body, bg=T["entry_bg"], relief="solid", bd=1).grid(row=0, column=1, sticky="ew", padx=8, pady=4)

        # Channel Number
        tk.Label(parent, text="Channel Number:", font=self._f_body, bg=T["card_bg"], fg=T["text"]).grid(row=1, column=0, sticky="w", pady=4)
        tk.Label(parent, text=str(self._slot_num), font=self._f_body, bg=T["card_bg"], fg=T["text_dim"]).grid(row=1, column=1, sticky="w", padx=8, pady=4)

        parent.columnconfigure(1, weight=1)

    def _build_measurement_range(self, parent):
        """Measurement range card content."""
        tk.Label(parent, text="Range:", font=self._f_body, bg=T["card_bg"], fg=T["text"]).grid(row=0, column=0, sticky="w", pady=4)
        
        range_var = tk.StringVar(value=self.config_data["measurement_range"])
        range_combo = ttk.Combobox(parent, textvariable=range_var, values=["0-10 mA", "4-20 mA", "0-5 V", "1-5 V"], font=self._f_body, state="readonly")
        range_combo.grid(row=0, column=1, sticky="ew", padx=8, pady=4)

        parent.columnconfigure(1, weight=1)

    def _build_alarm_settings(self, parent):
        """Alarm settings card content."""
        # Alarm Enable checkbox
        alarm_var = tk.BooleanVar(value=self.config_data["alarm_enable"])
        tk.Checkbutton(parent, text="Enable Alarm", variable=alarm_var, font=self._f_body, bg=T["card_bg"], fg=T["text"], selectcolor=T["card_bg"]).grid(row=0, column=0, columnspan=2, sticky="w", pady=4)

        # Alarm Threshold
        tk.Label(parent, text="Alarm Threshold:", font=self._f_body, bg=T["card_bg"], fg=T["text"]).grid(row=1, column=0, sticky="w", pady=4)
        threshold_var = tk.StringVar(value=str(self.config_data["alarm_threshold"]))
        tk.Entry(parent, textvariable=threshold_var, font=self._f_body, bg=T["entry_bg"], relief="solid", bd=1, width=10).grid(row=1, column=1, sticky="w", padx=8, pady=4)

        parent.columnconfigure(1, weight=1)

    def _build_filter_settings(self, parent):
        """Filter settings card content."""
        tk.Label(parent, text="Filter Frequency:", font=self._f_body, bg=T["card_bg"], fg=T["text"]).grid(row=0, column=0, sticky="w", pady=4)
        
        filter_var = tk.StringVar(value=self.config_data["filter_setting"])
        filter_combo = ttk.Combobox(parent, textvariable=filter_var, values=["50 Hz", "60 Hz", "Off"], font=self._f_body, state="readonly")
        filter_combo.grid(row=0, column=1, sticky="ew", padx=8, pady=4)

        parent.columnconfigure(1, weight=1)

    def _build_units_display(self, parent):
        """Units and display card content."""
        tk.Label(parent, text="Units:", font=self._f_body, bg=T["card_bg"], fg=T["text"]).grid(row=0, column=0, sticky="w", pady=4)
        
        units_var = tk.StringVar(value=self.config_data["units"])
        units_combo = ttk.Combobox(parent, textvariable=units_var, values=["mA", "V", "psi", "bar"], font=self._f_body, state="readonly")
        units_combo.grid(row=0, column=1, sticky="ew", padx=8, pady=4)

        # Display format
        tk.Label(parent, text="Decimal Places:", font=self._f_body, bg=T["card_bg"], fg=T["text"]).grid(row=1, column=0, sticky="w", pady=4)
        
        decimal_var = tk.StringVar(value="2")
        decimal_combo = ttk.Combobox(parent, textvariable=decimal_var, values=["0", "1", "2", "3"], font=self._f_body, state="readonly", width=5)
        decimal_combo.grid(row=1, column=1, sticky="w", padx=8, pady=4)

        parent.columnconfigure(1, weight=1)

    def _on_ok(self):
        """OK button handler - save and close."""
        print(f"OK clicked - Saving 3000/6M options for slot {self._slot_num}")
        self._dialog.destroy()

    def _on_cancel(self):
        """Cancel button handler - close without saving."""
        print(f"Cancel clicked - Discarding changes for slot {self._slot_num}")
        self._dialog.destroy()

    def _on_defaults(self):
        """Defaults button handler - reset to default values."""
        print(f"Defaults clicked - Resetting to defaults for slot {self._slot_num}")
        self.config_data = {
            "channel_name": f"Channel {self._slot_num}",
            "measurement_range": "0-10 mA",
            "filter_setting": "50 Hz",
            "alarm_enable": False,
            "alarm_threshold": 5.0,
            "units": "mA",
        }
        self._dialog.destroy()
        self.show()

    def _on_apply(self):
        """Apply button handler - save without closing."""
        print(f"Apply clicked - Saving 3000/6M options for slot {self._slot_num}")


# ══════════════════════════════════════════════════════════════════════════
#  Standalone demo (for testing)
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    root.title("3000/6M Options Dialog Demo")
    root.geometry("900x700")
    
    demo_btn = tk.Button(root, text="Show 3000/6M Options Dialog", 
                        command=lambda: SixMOptionsDialog(root, 3).show(),
                        font=("Segoe UI", 12), padx=20, pady=10)
    demo_btn.pack(expand=True)
    
    root.mainloop()
