"""
rack_Monitor_display.py — VMS 3000  •  PSM Front Panel Display
Exact design matching the reference image - Power Supply Module front panel
"""

import tkinter as tk
import tkinter.font as tkfont


# ══════════════════════════════════════════════════════════════════════════════
#  THEME  —  VMS 3000 Industrial SCADA colour palette
# ══════════════════════════════════════════════════════════════════════════════

T = {
    # ── Panel colours ───────────────────────────────────────────────────
    "panel_bg":        "#1a3a5c",   # Dark blue panel background
    "panel_dark":      "#0a2040",   # Darker blue for shadows
    "panel_light":     "#2a5080",   # Lighter blue for highlights
    
    # ── Metal/brushed steel ─────────────────────────────────────────────
    "metal_dark":      "#3a4a5a",
    "metal_light":     "#5a6a7a",
    "metal_mid":       "#4a5a6a",
    
    # ── LEDs ──────────────────────────────────────────────────────────
    "led_green":       "#22c55e",
    "led_green_glow":  "#16a34a",
    "led_amber":       "#f59e0b",
    "led_red":         "#ef4444",
    "led_blue":        "#3b82f6",
    "led_off":         "#1a2a3a",
    
    # ── Text ──────────────────────────────────────────────────────────
    "text_white":      "#ffffff",
    "text_dim":        "#8a9ab8",
    "text_label":      "#c8d8e8",
    
    # ── Button ────────────────────────────────────────────────────────
    "btn_face":        "#4a5a6a",
    "btn_hover":       "#5a6a7a",
    "btn_press":       "#3a4a5a",
    
    # ── Switch ────────────────────────────────────────────────────────
    "switch_bg":       "#2a3a4a",
    "switch_knob":     "#5a6a7a",
}


# ══════════════════════════════════════════════════════════════════════════════
#  PSM FRONT PANEL CLASS
# ══════════════════════════════════════════════════════════════════════════════

class PSMFrontPanel:
    """
    PSM (Power Supply Module) Front Panel Display.
    
    Exact design matching the reference image:
      • Top screw/latch
      • LED indicators: PWR, TX/RX, TM, CNFG
      • RST button
      • RUN/PROG rotary switch
      • Configuration Port slot
      • Monitor icon with VMS-3000 CNFG label
      • Bottom screw
    """

    def __init__(self, parent, width=120, height=400):
        """
        Initialize PSM front panel.
        
        Args:
            parent: Parent widget
            width: Panel width (default 120)
            height: Panel height (default 400)
        """
        self._parent = parent
        self._width = width
        self._height = height
        
        self._canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            bg=T["panel_bg"],
            highlightthickness=0,
        )
        self._canvas.pack()
        
        self._draw_panel()

    def _draw_panel(self):
        """Draw the complete PSM front panel."""
        c = self._canvas
        w = self._width
        h = self._height
        
        # ── Panel body with gradient effect ─────────────────────────────
        self._draw_panel_body(c, w, h)
        
        # ── Top screw/latch ────────────────────────────────────────────
        self._draw_screw(c, w // 2, 15)
        
        # ── LED indicators section ───────────────────────────────────────
        led_y = 50
        led_spacing = 25
        self._draw_led(c, w // 2, led_y, "PWR", T["led_green"])
        self._draw_led(c, w // 2, led_y + led_spacing, "TX/RX", T["led_amber"])
        self._draw_led(c, w // 2, led_y + led_spacing * 2, "TM", T["led_blue"])
        self._draw_led(c, w // 2, led_y + led_spacing * 3, "CNFG", T["led_off"])
        
        # ── RST button ──────────────────────────────────────────────────
        self._draw_rst_button(c, w // 2, led_y + led_spacing * 4 + 15)
        
        # ── RUN/PROG rotary switch ───────────────────────────────────────
        switch_y = led_y + led_spacing * 4 + 50
        self._draw_rotary_switch(c, w // 2, switch_y)
        
        # ── Configuration Port slot ─────────────────────────────────────
        port_y = switch_y + 60
        self._draw_config_port(c, w // 2, port_y)
        
        # ── Monitor icon and label ───────────────────────────────────────
        icon_y = port_y + 50
        self._draw_monitor_icon(c, w // 2, icon_y)
        
        # ── Bottom screw ────────────────────────────────────────────────
        self._draw_screw(c, w // 2, h - 15)

    def _draw_panel_body(self, c, w, h):
        """Draw the main panel body with brushed metal effect."""
        # Main panel background
        c.create_rectangle(0, 0, w, h, fill=T["panel_bg"], outline="")
        
        # Top highlight
        c.create_rectangle(0, 0, w, 3, fill=T["panel_light"], outline="")
        
        # Bottom shadow
        c.create_rectangle(0, h - 3, w, h, fill=T["panel_dark"], outline="")
        
        # Vertical highlights for brushed metal effect
        for x in range(0, w, 4):
            c.create_line(x, 0, x, h, fill=T["panel_light"], width=1, stipple="gray25")

    def _draw_screw(self, c, x, y):
        """Draw a screw/latch at the given position."""
        r = 6
        # Screw head
        c.create_oval(x - r, y - r, x + r, y + r,
                      fill=T["metal_dark"],
                      outline=T["metal_light"],
                      width=1)
        # Crosshead
        c.create_line(x - 3, y, x + 3, y, fill=T["metal_light"], width=1)
        c.create_line(x, y - 3, x, y + 3, fill=T["metal_light"], width=1)

    def _draw_led(self, c, x, y, label, color):
        """Draw an LED indicator with label."""
        # LED body
        r = 8
        # Glow effect
        c.create_oval(x - r - 2, y - r - 2, x + r + 2, y + r + 2,
                      fill=color if color != T["led_off"] else "",
                      outline="",
                      stipple="gray50" if color != T["led_off"] else "")
        # LED
        c.create_oval(x - r, y - r, x + r, y + r,
                      fill=color,
                      outline=T["metal_light"],
                      width=1)
        # Label
        c.create_text(x + r + 15, y,
                      text=label,
                      fill=T["text_label"],
                      font=tkfont.Font(family="Arial", size=7, weight="bold"),
                      anchor="w")

    def _draw_rst_button(self, c, x, y):
        """Draw the RST (Reset) button."""
        btn_w = 40
        btn_h = 20
        # Button body
        c.create_rectangle(x - btn_w // 2, y - btn_h // 2,
                          x + btn_w // 2, y + btn_h // 2,
                          fill=T["btn_face"],
                          outline=T["metal_light"],
                          width=1)
        # Button text
        c.create_text(x, y,
                      text="RST",
                      fill=T["text_white"],
                      font=tkfont.Font(family="Arial", size=8, weight="bold"),
                      anchor="center")

    def _draw_rotary_switch(self, c, x, y):
        """Draw the RUN/PROG rotary switch."""
        # Switch background
        r = 25
        c.create_oval(x - r, y - r, x + r, y + r,
                      fill=T["switch_bg"],
                      outline=T["metal_light"],
                      width=2)
        
        # Switch knob
        knob_r = 18
        c.create_oval(x - knob_r, y - knob_r, x + knob_r, y + knob_r,
                      fill=T["switch_knob"],
                      outline=T["metal_dark"],
                      width=1)
        
        # Knob indicator line (pointing to RUN)
        c.create_line(x, y - knob_r + 5, x, y - knob_r + 12,
                      fill=T["text_white"],
                      width=2)
        
        # RUN label (top - selected)
        c.create_text(x, y - r - 8,
                      text="RUN",
                      fill=T["led_green"],
                      font=tkfont.Font(family="Arial", size=8, weight="bold"),
                      anchor="center")
        
        # PROG label (bottom)
        c.create_text(x, y + r + 8,
                      text="PROG",
                      fill=T["text_dim"],
                      font=tkfont.Font(family="Arial", size=8, weight="bold"),
                      anchor="center")

    def _draw_config_port(self, c, x, y):
        """Draw the Configuration Port slot."""
        slot_w = 50
        slot_h = 30
        # Slot body
        c.create_rectangle(x - slot_w // 2, y - slot_h // 2,
                          x + slot_w // 2, y + slot_h // 2,
                          fill=T["panel_dark"],
                          outline=T["metal_light"],
                          width=1)
        # Slot inner
        c.create_rectangle(x - slot_w // 2 + 3, y - slot_h // 2 + 3,
                          x + slot_w // 2 - 3, y + slot_h // 2 - 3,
                          fill="#0a1020",
                          outline="")
        # Label
        c.create_text(x, y + slot_h // 2 + 12,
                      text="CONFIGURATION",
                      fill=T["text_dim"],
                      font=tkfont.Font(family="Arial", size=6),
                      anchor="center")
        c.create_text(x, y + slot_h // 2 + 20,
                      text="PORT",
                      fill=T["text_dim"],
                      font=tkfont.Font(family="Arial", size=6),
                      anchor="center")

    def _draw_monitor_icon(self, c, x, y):
        """Draw the monitor icon with VMS-3000 label."""
        # Icon background (hand cursor pointing to document)
        icon_w = 30
        icon_h = 30
        icon_x = x - icon_w // 2
        icon_y = y - icon_h // 2
        
        # Document rectangle
        c.create_rectangle(icon_x + 5, icon_y + 5,
                          icon_x + icon_w - 5, icon_y + icon_h - 5,
                          fill="#ffffff",
                          outline=T["metal_light"],
                          width=1)
        # Document lines
        for i in range(3):
            line_y = icon_y + 10 + i * 6
            c.create_line(icon_x + 10, line_y,
                          icon_x + icon_w - 10, line_y,
                          fill=T["text_dim"],
                          width=1)
        
        # Hand cursor (simplified)
        hand_x = icon_x + icon_w - 8
        hand_y = icon_y + icon_h - 8
        c.create_polygon(hand_x, hand_y,
                          hand_x + 6, hand_y - 4,
                          hand_x + 8, hand_y - 2,
                          hand_x + 8, hand_y + 4,
                          hand_x + 4, hand_y + 8,
                          hand_x, hand_y + 6,
                          fill=T["led_amber"],
                          outline=T["metal_light"],
                          width=1)
        
        # VMS-3000 label
        c.create_text(x, y + icon_h // 2 + 15,
                      text="VMS-3000",
                      fill=T["text_white"],
                      font=tkfont.Font(family="Arial", size=9, weight="bold"),
                      anchor="center")
        
        # CNFG label
        c.create_text(x, y + icon_h // 2 + 25,
                      text="CNFG",
                      fill=T["text_dim"],
                      font=tkfont.Font(family="Arial", size=7),
                      anchor="center")

    def get_canvas(self):
        """Return the canvas widget."""
        return self._canvas


# ══════════════════════════════════════════════════════════════════════════════
#  VMM-6M MODULE DISPLAY CLASS
# ══════════════════════════════════════════════════════════════════════════════

class VMM6MModule:
    """
    VMM-6M Module Display.
    
    Exact design matching the reference image:
      • Top white tab with screw
      • Blue oval logo
      • LED indicators: PWR, Tx/Rx, OK
      • ALARM section: OK, ALT, DAN, BYP
      • 4 BNC connectors
      • VMM-6M label
      • Bottom white tab with screw
    """

    def __init__(self, parent, width=100, height=350):
        """
        Initialize VMM-6M module display.
        
        Args:
            parent: Parent widget
            width: Module width (default 100)
            height: Module height (default 350)
        """
        self._parent = parent
        self._width = width
        self._height = height
        
        self._canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            bg="#1a4fa0",
            highlightthickness=0,
        )
        self._canvas.pack()
        
        self._draw_module()

    def _draw_module(self):
        """Draw the complete VMM-6M module."""
        c = self._canvas
        w = self._width
        h = self._height
        
        mx = w // 2
        
        # ── Module body (blue faceplate) ─────────────────────────────
        c.create_rectangle(0, 0, w, h,
                          fill="#1a4fa0",
                          outline="#0a2f60",
                          width=2)
        
        # ── Top white tab with screw ─────────────────────────────────
        tab_h = 12
        c.create_rectangle(2, 2, w-2, tab_h,
                          fill="#e8e8e8",
                          outline="#c0c0c0",
                          width=1)
        # Screw
        screw_cx = mx
        screw_cy = tab_h // 2
        c.create_oval(screw_cx-4, screw_cy-4, screw_cx+4, screw_cy+4,
                      fill="#a0a0a0",
                      outline="#808080",
                      width=1)
        c.create_line(screw_cx-2, screw_cy, screw_cx+2, screw_cy,
                      fill="#606060", width=1)
        c.create_line(screw_cx, screw_cy-2, screw_cx, screw_cy+2,
                      fill="#606060", width=1)
        
        # ── Blue oval logo ───────────────────────────────────────────
        logo_y = tab_h + 8
        logo_w = min(30, w - 10)
        c.create_oval(mx - logo_w//2, logo_y,
                      mx + logo_w//2, logo_y + logo_w,
                      fill="#2a6fc0",
                      outline="#4a9fe0",
                      width=1)
        
        # ── Top indicators (PWR, Tx/Rx, OK) ─────────────────────────
        ind_y = logo_y + logo_w + 8
        indicators = ["PWR", "Tx/Rx", "OK"]
        ind_spacing = (w - 20) // len(indicators)
        for i, lbl in enumerate(indicators):
            ix = 10 + i * ind_spacing + ind_spacing // 2
            # Grey circle
            c.create_oval(ix-6, ind_y, ix+6, ind_y+12,
                          fill="#888888",
                          outline="#a0a0a0",
                          width=1)
            # Label
            c.create_text(ix, ind_y + 20,
                          text=lbl,
                          font=tkfont.Font(family="Segoe UI", size=5),
                          fill="#ffffff",
                          anchor="center")
        
        # ── ALARM section with 4 indicators ─────────────────────────
        alarm_y = ind_y + 28
        alarm_box_h = 40
        c.create_rectangle(4, alarm_y, w-4, alarm_y + alarm_box_h,
                          fill="#0a2040",
                          outline="#1a4070",
                          width=1)
        c.create_text(mx, alarm_y + 6,
                      text="ALARM",
                      font=tkfont.Font(family="Segoe UI", size=5, weight="bold"),
                      fill="#ffffff",
                      anchor="center")
        
        alarm_indicators = ["OK", "ALT", "DAN", "BYP"]
        alarm_ind_spacing = (w - 12) // len(alarm_indicators)
        for i, lbl in enumerate(alarm_indicators):
            aix = 6 + i * alarm_ind_spacing + alarm_ind_spacing // 2
            aiy = alarm_y + 18
            # Grey circle
            c.create_oval(aix-5, aiy, aix+5, aiy+10,
                          fill="#888888",
                          outline="#a0a0a0",
                          width=1)
            # Label
            c.create_text(aix, aiy + 14,
                          text=lbl,
                          font=tkfont.Font(family="Segoe UI", size=4),
                          fill="#ffffff",
                          anchor="center")
        
        # ── BNC connectors (4 vertical) ─────────────────────────────
        conn_start_y = alarm_y + alarm_box_h + 8
        conn_spacing = (h - 12 - conn_start_y) // 4
        for i in range(4):
            cy = conn_start_y + i * conn_spacing + conn_spacing // 2
            cx = mx
            # Outer ring
            c.create_oval(cx-7, cy-7, cx+7, cy+7,
                          fill="#c0c0c0",
                          outline="#808080",
                          width=1)
            # Inner circle
            c.create_oval(cx-4, cy-4, cx+4, cy+4,
                          fill="#404040",
                          outline="#606060",
                          width=1)
        
        # ── Bottom white tab with screw ─────────────────────────────
        bot_tab_y = h - 12
        c.create_rectangle(2, bot_tab_y, w-2, h-2,
                          fill="#e8e8e8",
                          outline="#c0c0c0",
                          width=1)
        # Screw
        bot_screw_cx = mx
        bot_screw_cy = bot_tab_y + 5
        c.create_oval(bot_screw_cx-4, bot_screw_cy-4, bot_screw_cx+4, bot_screw_cy+4,
                      fill="#a0a0a0",
                      outline="#808080",
                      width=1)
        c.create_line(bot_screw_cx-2, bot_screw_cy, bot_screw_cx+2, bot_screw_cy,
                      fill="#606060", width=1)
        c.create_line(bot_screw_cx, bot_screw_cy-2, bot_screw_cx, bot_screw_cy+2,
                      fill="#606060", width=1)
        
        # ── VMM-6M label ────────────────────────────────────────────
        label_y = bot_tab_y - 8
        c.create_text(mx, label_y,
                      text="VMM-6M",
                      font=tkfont.Font(family="Segoe UI", size=6, weight="bold"),
                      fill="#ffffff",
                      anchor="center")

    def get_canvas(self):
        """Return the canvas widget."""
        return self._canvas


# ══════════════════════════════════════════════════════════════════════════════
#  Standalone preview
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    root.title("PSM Front Panel Display")
    root.configure(bg="#1a1a1a")
    root.resizable(False, False)
    
    # Center the window
    panel = PSMFrontPanel(root, width=120, height=400)
    canvas = panel.get_canvas()
    
    root.update_idletasks()
    w = 120
    h = 400
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")
    
    root.mainloop()
