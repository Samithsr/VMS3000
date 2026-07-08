"""
rack_area.py — VMS 3000  •  Professional Rack Canvas
Matches actual VMS-3000 hardware UI:
  • Three-section PSM column on the left
  • 12 slot cards with faceplate, grip texture, LED, connector pins
  • Selected slot glows amber
  • VMM-6M slots render a pixel-accurate replica of the reference image
  • When a VMM-6M slot is SELECTED (clicked) it flips to a dark/inverted display
"""

import tkinter as tk
import tkinter.font as tkfont
from theme import T
import sys
import os
import math
from PIL import Image, ImageTk

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from popups.configuration_settings import ConfigurationSettingsPopup
from popups.monitors import ModuleSelectionPopup
from popups.module_switch_confirmation import ModuleSwitchConfirmationPopup
from snapshot.racksnapshot import get_module_config, is_image_display_module

SLOT_COUNT = 12

# Modules that consume 2 slots and show the Measurement Module image
DIS_MODULE = "3000/12M/DIS"
VMM_MODULE = "VMM-6M"   # single-slot image (existing behaviour)
RLY_MODULE = "3000/RLY"  # single-slot Relay module image (fallback exact name)


def _is_relay_module(module: str) -> bool:
    """
    Flexible Relay-module check. Matches the exact RLY_MODULE string OR
    any module name containing 'RLY' / 'RELAY' (case-insensitive), so this
    keeps working even if the exact label in the module-selection list
    differs slightly from RLY_MODULE (e.g. 'Relay', '3000/12M/RLY', etc.).
    """
    if not module:
        return False
    if module == RLY_MODULE:
        return True
    upper = module.upper()
    return "RLY" in upper or "RELAY" in upper


class RackArea:

    def __init__(self, parent, fonts, hint_var: tk.StringVar):
        self._fonts    = fonts
        self._hint_var = hint_var
        self._selected = None
        self._slot_data: dict = {}

        right = tk.Frame(parent, bg=T["win_bg"])
        right.pack(side="left", fill="both", expand=True, padx=0, pady=10)

        self._canvas = tk.Canvas(
            right,
            bg=T["win_bg"],
            bd=0,
            highlightthickness=0,
        )
        self._canvas.pack(fill="both", expand=True)
        self._canvas.bind("<Configure>", lambda e: self.draw())

        hint_bar = tk.Frame(right, bg=T["win_bg"])
        hint_bar.pack(fill="x", pady=(6, 0))

        hint_icon = tk.Label(
            hint_bar,
            text="ℹ",
            font=tkfont.Font(family="Segoe UI", size=10),
            bg=T["win_bg"],
            fg=T["accent"],
        )
        hint_icon.pack(side="left", padx=(6, 4))

        tk.Label(
            hint_bar,
            textvariable=hint_var,
            font=tkfont.Font(family="Segoe UI", size=10),
            bg=T["win_bg"],
            fg=T["text_hint"],
            cursor="hand2",
        ).pack(side="left")

    # ── Public ──────────────────────────────────────────────────────

    def clear(self):
        self._slot_data.clear()
        self._selected = None
        self.draw()

    def get_slot_data(self) -> dict:
        return dict(self._slot_data)

    # ── Layout constants ────────────────────────────────────────────

    def _layout(self, W: int, H: int) -> dict:
        PSM_W   = 110
        PAD_X   = 14
        TOP_Y   = 32
        PAD_BOT = 10
        SHELL_H = H - TOP_Y - PAD_BOT

        slot_x0      = PAD_X + PSM_W + 8
        slot_w_total = W - PAD_X * 2 - PSM_W - 8 - PAD_X
        sw           = slot_w_total / SLOT_COUNT

        return dict(
            PAD_X=PAD_X, TOP_Y=TOP_Y, PAD_BOT=PAD_BOT,
            SHELL_H=SHELL_H, PSM_W=PSM_W,
            slot_x0=slot_x0, sw=sw,
            W=W, H=H,
        )

    # ── Main draw ───────────────────────────────────────────────────

    def draw(self):
        c = self._canvas
        c.delete("all")
        W = c.winfo_width()
        H = c.winfo_height()
        if W < 200 or H < 120:
            return

        L = self._layout(W, H)
        self._draw_rack_shell(c, L)
        self._draw_slot_headers(c, L)
        self._draw_psm_top(c, L)
        self._draw_psm_bottom(c, L)

        skip_next = False
        for slot in range(SLOT_COUNT):
            if skip_next:
                skip_next = False
                continue
            slot_num = slot + 1
            key      = f"0_{slot_num}"
            module   = self._slot_data.get(key)
            if module == DIS_MODULE:
                self._draw_dis_module(c, L, slot)
                skip_next = True   # slot+1 is absorbed into the merged card
            else:
                self._draw_slot(c, L, slot)

    # ── Rack shell ──────────────────────────────────────────────────

    def _draw_rack_shell(self, c: tk.Canvas, L: dict):
        x1 = L["PAD_X"]
        y1 = L["TOP_Y"] - 6
        x2 = L["W"] - L["PAD_X"]
        y2 = y1 + L["SHELL_H"]

        # Outer shell body — no border/shadow on any of the 4 sides
        # (top strip, left/right rails, and drop-shadow all removed).
        c.create_rectangle(x1, y1, x2, y2,
                            fill=T["rack_shell_bot"],
                            outline="",
                            width=0, tags="rack_bg")
        c.create_rectangle(x1+6, y1+6, x2-6, y2-6,
                            fill=T["rack_row"],
                            outline="#0a0f18",
                            width=1, tags="rack_bg")

    # ── Slot number headers ─────────────────────────────────────────

    def _draw_slot_headers(self, c: tk.Canvas, L: dict):
        """
        Draw slot numbers above each card.
        Rules:
          • Slot 1 header is always hidden (config slot, no number shown).
          • For a DIS double-slot at odd slot N:  show N centred over the
            merged pair, hide N+1 completely.
          • For VMM-6M single slots: normal single-slot number.
          • Selected slot number is dark (#cc2222), unselected is gray (#888888).
          • Display numbers start from 2 (slots 2-12 display as 2-12).
        """
        skip_next = False
        for i in range(1, SLOT_COUNT + 1):
            if skip_next:
                skip_next = False
                continue

            # Slot 1 is the PSM/config card — no header number
            if i == 1:
                continue

            key    = f"0_{i}"
            module = self._slot_data.get(key)
            is_selected = (self._selected == key)

            # Dark color for selected, gray for unselected
            fill_color = "#cc2222" if is_selected else "#888888"

            # Display number: shift by -1 to show 1-11 instead of 2-12
            display_num = i - 1

            if module == DIS_MODULE:
                # Centre the number over both slots i and i+1
                cx = L["slot_x0"] + (i - 1 + 1.0) * L["sw"]   # midpoint of pair
                c.create_text(cx, L["TOP_Y"] - 14,
                              text=str(display_num),
                              font=self._fonts["num"],
                              fill=fill_color,
                              anchor="center")
                skip_next = True   # hide i+1 header
            else:
                cx = L["slot_x0"] + (i - 1 + 0.5) * L["sw"]
                c.create_text(cx, L["TOP_Y"] - 14,
                              text=str(display_num),
                              font=self._fonts["num"],
                              fill=fill_color,
                              anchor="center")

    # ── Helper: draw one PSM panel ──────────────────────────────────

    def _draw_psm_panel(self, c: tk.Canvas, L: dict,
                        px1: int, py1: int, px2: int, py2: int,
                        label: str):
        mx = (px1 + px2) // 2

        c.create_rectangle(px1, py1, px2, py2,
                            fill=T["psm_body"],
                            outline=T["slot_edge_sh"],
                            width=2)
        c.create_line(px1, py1, px2, py1, fill="#2a4060", width=1)
        c.create_line(px1, py1, px1, py2, fill="#1e3050", width=1)

        logo_cx = mx
        logo_cy = py1 + 14
        logo_r  = 10
        c.create_oval(logo_cx - logo_r, logo_cy - logo_r,
                      logo_cx + logo_r, logo_cy + logo_r,
                      fill="#1a5fa0", outline="#4a9fd0", width=1)
        for ang in range(0, 180, 45):
            x0 = logo_cx + logo_r * math.cos(math.radians(ang))
            y0 = logo_cy + logo_r * math.sin(math.radians(ang))
            x1b = logo_cx - logo_r * math.cos(math.radians(ang))
            y1b = logo_cy - logo_r * math.sin(math.radians(ang))
            c.create_line(x0, y0, x1b, y1b, fill="#4ab0e0", width=1)
        c.create_oval(logo_cx - logo_r, logo_cy - 3,
                      logo_cx + logo_r, logo_cy + 3,
                      outline="#4ab0e0", width=1, fill="")

        strip_y = logo_cy + logo_r + 2
        c.create_rectangle(px1, strip_y, px2, strip_y + 14,
                            fill=T["psm_brand"], outline="")
        c.create_text(mx, strip_y + 7,
                      text="Sarayu",
                      font=tkfont.Font(family="Segoe UI", size=8, weight="bold",
                                       slant="italic"),
                      fill="#ffffff", anchor="center")

        vy = strip_y + 18
        for i, word in enumerate(["Vibration", "Monitoring", "System"]):
            c.create_text(mx, vy + i * 11,
                          text=word,
                          font=tkfont.Font(family="Segoe UI", size=6),
                          fill=T["psm_label"],
                          anchor="center")

        volts = ["+5V", "+12V", "-12V", "+24V", "-24V"]
        led_colors = [T["led_green"]] * 5
        vled_y0 = vy + 36
        lx = px1 + 6
        for i, (lbl, col) in enumerate(zip(volts, led_colors)):
            ly = vled_y0 + i * 12
            c.create_oval(lx-1, ly-1, lx+7, ly+7,
                          fill=col, outline="", stipple="gray50")
            c.create_oval(lx+1, ly+1, lx+5, ly+5,
                          fill=col, outline="#ffffff", width=1)
            c.create_text(lx + 10, ly + 3,
                          text=lbl,
                          font=tkfont.Font(family="Courier New", size=5),
                          fill="#8ab8d8",
                          anchor="w")

        num_y = vled_y0 + len(volts) * 12 + 6
        c.create_text(mx, num_y,
                      text="3000",
                      font=tkfont.Font(family="Segoe UI", size=14, weight="bold"),
                      fill=T["psm_3000"],
                      anchor="center")

        c.create_rectangle(px1+4, py2-20, px2-4, py2-4,
                            fill=T["psm_plate"],
                            outline="#1e3050")
        c.create_text(mx, py2-12,
                      text=label,
                      font=tkfont.Font(family="Segoe UI", size=6, weight="bold"),
                      fill=T["psm_plate_text"],
                      anchor="center")

        return num_y + 16

    # ── TOP PSM panel — Powersupply.jpg image, stretch-filled ───────

    def _draw_psm_top(self, c: tk.Canvas, L: dict):
        """
        Column 0 (PSM) top panel. Loads src/images/Powersupply.jpg and
        stretch-fills it into the panel's exact pixel bounds — the same
        STRETCH-FILL technique used for VMM-6M / Relay / DIS module cards
        (img.resize to (panel_w, panel_h), no aspect-ratio letterboxing,
        no cropping). Falls back to the original hand-drawn PSM panel
        graphic if the image file can't be found/loaded.
        Extended height to include middle strip area (45% -> 55%).
        """
        x1      = L["PAD_X"] + 14
        y1      = L["TOP_Y"] + 2
        x2      = x1 + L["PSM_W"] - 4
        top_end = L["TOP_Y"] + int(L["SHELL_H"] * 0.50)  # 50% to match bottom

        panel_w = max(1, x2 - x1)
        panel_h = max(1, top_end - y1)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(base_dir, 'src', 'images', 'Powersupply.jpg'),
            os.path.join(base_dir, 'images', 'Powersupply.jpg'),
            os.path.join(base_dir, 'Powersupply.jpg'),
            os.path.join(base_dir, 'src', 'Powersupply.jpg'),
        ]
        img_path = next((p for p in candidates if os.path.isfile(p)), None)

        if not hasattr(self, '_psm_top_photo'):
            self._psm_top_photo = None

        loaded = False
        if img_path:
            try:
                img = Image.open(img_path).convert("RGB")

                # STRETCH-FILL: resize directly to the panel's exact pixel
                # size, same treatment as VMM-6M / Relay / DIS module cards.
                img = img.resize((panel_w, panel_h), Image.Resampling.LANCZOS)

                photo = ImageTk.PhotoImage(img)
                c.create_rectangle(x1, y1, x2, top_end,
                                   fill="#0a0e14", outline="", tags="rack_bg")
                c.create_image(x1, y1, image=photo, anchor="nw")
                self._psm_top_photo = photo   # keep reference alive
                loaded = True
            except Exception:
                pass

        if not loaded:
            # Fallback: original hand-drawn panel
            self._draw_psm_panel(c, L, x1, y1, x2, top_end, "VMS-3000 PSM")

    # ── MIDDLE strip — Powersupply.jpg image, stretch-filled ─────────────

    def _draw_psm_middle(self, c: tk.Canvas, L: dict):
        """
        Column 0 (PSM) middle strip. Loads src/images/Powersupply.jpg and
        stretch-fills it into the strip's exact pixel bounds — the same
        STRETCH-FILL technique used for the top and bottom PSM panels.
        """
        x1      = L["PAD_X"] + 14
        x2      = x1 + L["PSM_W"] - 4
        top_end = L["TOP_Y"] + int(L["SHELL_H"] * 0.45)
        bot_st  = L["TOP_Y"] + int(L["SHELL_H"] * 0.55)
        if bot_st - top_end < 10:
            bot_st = top_end + 10

        panel_w = max(1, x2 - x1)
        panel_h = max(1, bot_st - top_end)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(base_dir, 'src', 'images', 'Powersupply.jpg'),
            os.path.join(base_dir, 'images', 'Powersupply.jpg'),
            os.path.join(base_dir, 'Powersupply.jpg'),
            os.path.join(base_dir, 'src', 'Powersupply.jpg'),
        ]
        img_path = next((p for p in candidates if os.path.isfile(p)), None)

        if not hasattr(self, '_psm_middle_photo'):
            self._psm_middle_photo = None

        loaded = False
        if img_path:
            try:
                img = Image.open(img_path).convert("RGB")

                # STRETCH-FILL: resize directly to the strip's exact pixel
                # size, same treatment as top and bottom PSM panels.
                img = img.resize((panel_w, panel_h), Image.Resampling.LANCZOS)

                photo = ImageTk.PhotoImage(img)
                c.create_rectangle(x1, top_end + 2, x2, bot_st - 2,
                                   fill="#0a0e14", outline="", tags="rack_bg")
                c.create_image(x1, top_end + 2, image=photo, anchor="nw")
                self._psm_middle_photo = photo   # keep reference alive
                loaded = True
            except Exception:
                pass

        if not loaded:
            # Fallback: dark background
            c.create_rectangle(x1, top_end + 2, x2, bot_st - 2,
                               fill="#0d1a28", outline="", tags="rack_bg")

    # ── BOTTOM PSM / CPU panel — Powersupply.jpg image, stretch-filled ───────

    def _draw_psm_bottom(self, c: tk.Canvas, L: dict):
        """
        Column 0 (PSM) bottom panel. Loads src/images/Powersupply.jpg and
        stretch-fills it into the panel's exact pixel bounds — the same
        STRETCH-FILL technique used for the top PSM panel and module cards.
        """
        x1    = L["PAD_X"] + 14
        x2    = x1 + L["PSM_W"] - 4
        bot_st = L["TOP_Y"] + int(L["SHELL_H"] * 0.50)  # 50% to match top
        y2     = L["TOP_Y"] + L["SHELL_H"] - 12

        panel_w = max(1, x2 - x1)
        panel_h = max(1, y2 - bot_st)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(base_dir, 'src', 'images', 'Powersupply.jpg'),
            os.path.join(base_dir, 'images', 'Powersupply.jpg'),
            os.path.join(base_dir, 'Powersupply.jpg'),
            os.path.join(base_dir, 'src', 'Powersupply.jpg'),
        ]
        img_path = next((p for p in candidates if os.path.isfile(p)), None)

        if not hasattr(self, '_psm_bottom_photo'):
            self._psm_bottom_photo = None

        loaded = False
        if img_path:
            try:
                img = Image.open(img_path).convert("RGB")

                # STRETCH-FILL: resize directly to the panel's exact pixel
                # size, same treatment as top PSM panel and module cards.
                img = img.resize((panel_w, panel_h), Image.Resampling.LANCZOS)

                photo = ImageTk.PhotoImage(img)
                c.create_rectangle(x1, bot_st, x2, y2,
                                   fill="#0a0e14", outline="", tags="rack_bg")
                c.create_image(x1, bot_st, image=photo, anchor="nw")
                self._psm_bottom_photo = photo   # keep reference alive
                loaded = True
            except Exception:
                pass

        if not loaded:
            # Fallback: original hand-drawn panel
            content_y = self._draw_psm_panel(c, L, x1, bot_st, x2, y2, "VMS-3000 CPU")

            box_x1 = x1 + 6
            box_x2 = x2 - 6
            box_y1 = content_y
            box_y2 = box_y1 + 30
            c.create_rectangle(box_x1, box_y1, box_x2, box_y2,
                               fill="#0a1520", outline="#1e3050")

            status_leds = [
                ("PSM",  T["led_green"],  0, 0),
                ("TuRn", T["led_amber"],  0, 1),
                ("TIS",  T["led_red"],    1, 0),
                ("CMFD", T["led_blue"],   1, 1),
            ]
            cell_w = (box_x2 - box_x1) // 2
            cell_h = (box_y2 - box_y1) // 2
            for lbl, col, row, col_i in status_leds:
                cx_led = box_x1 + col_i * cell_w + 5
                cy_led = box_y1 + row  * cell_h + 8
                c.create_oval(cx_led, cy_led, cx_led+6, cy_led+6,
                              fill=col, outline="#ffffff", width=1)
                c.create_text(cx_led + 9, cy_led + 3,
                              text=lbl,
                              font=tkfont.Font(family="Courier New", size=5),
                              fill="#8ab8d8",
                              anchor="w")

            run_y = box_y2 + 6
            c.create_oval(mx-10, run_y, mx+10, run_y+12,
                          fill="#183018", outline="#1e3050", width=2)
            c.create_oval(mx-6,  run_y+2, mx+6,  run_y+10,
                          fill=T["led_green"], outline="#ffffff", width=1)
            c.create_text(mx, run_y + 18,
                          text="RUN",
                          font=tkfont.Font(family="Courier New", size=5, weight="bold"),
                          fill="#4af04a",
                          anchor="center")

            db9_y = run_y + 26
            db9_x1 = mx - 14
            db9_x2 = mx + 14
            db9_h  = 18
            c.create_rectangle(db9_x1, db9_y, db9_x2, db9_y + db9_h,
                               fill="#1a2a3a", outline="#3a5a7a", width=1)
            pin_rows = [5, 4]
            pr_y = db9_y + 4
            for npins in pin_rows:
                spacing = (db9_x2 - db9_x1 - 6) / max(npins - 1, 1)
                for p in range(npins):
                    px = db9_x1 + 3 + int(p * spacing)
                    c.create_oval(px, pr_y, px+3, pr_y+3,
                                  fill="#000000", outline="#5a7a9a", width=1)
                pr_y += 7
            c.create_text(mx, db9_y + db9_h + 6,
                          text="PROG",
                          font=tkfont.Font(family="Courier New", size=5),
                          fill="#6a9aba",
                          anchor="center")

            bar_y = db9_y + db9_h + 14
            bar_x1 = mx - 12
            bar_x2 = mx + 12
            bar_h  = 22
            c.create_rectangle(bar_x1, bar_y, bar_x2, bar_y + bar_h,
                               fill="#1a0000", outline="#3a0000", width=1)
            seg_count = 8
            seg_h = (bar_h - 4) / seg_count
            for seg in range(seg_count):
                intensity = "#ff0000" if seg < 5 else "#660000"
                sy = bar_y + 2 + int(seg * seg_h)
                c.create_rectangle(bar_x1+3, sy,
                                   bar_x2-3, sy + max(1, int(seg_h)-1),
                                   fill=intensity, outline="")

    # ══════════════════════════════════════════════════════════════════
    #  3000/12M/DIS — double-wide Measurement Module card
    # ══════════════════════════════════════════════════════════════════

    def _draw_dis_module(self, c: tk.Canvas, L: dict, slot_idx: int):
        """
        Render a 3000/12M/DIS module that spans TWO slot columns.
        slot_idx  = the LEFT (primary) slot (0-based).
        slot_idx+1 = the hidden right slot.

        Behaviour:
          • The merged card occupies exactly 2× the normal slot width.
          • The Measurement_Module.jpg is loaded and scaled in COVER mode
            (fills the full card width and height, center-cropping any
            overflow) so there are no black margins on the sides.
          • Slot number label above shows only the primary slot number.
          • Clicking the card opens the same module-assignment dialog so the
            user can change or remove the module.
        """
        slot_num = slot_idx + 1
        key      = f"0_{slot_num}"
        tag      = f"s_{key}"
        is_sel   = (self._selected == key)

        sw   = L["sw"]
        # Double-wide: spans slot_idx and slot_idx+1
        sx1  = int(L["slot_x0"] + slot_idx * sw + 3)
        sx2  = int(L["slot_x0"] + (slot_idx + 2) * sw - 6)
        sy1  = L["TOP_Y"] + 2
        sy2  = L["TOP_Y"] + L["SHELL_H"] - 12

        card_w = max(1, sx2 - sx1)
        card_h = max(1, sy2 - sy1)

        # ── Locate Measurement_Module.jpg ────────────────────────────
        base_dir = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(base_dir, 'src', 'images', 'Measurement_Module.jpg'),
            os.path.join(base_dir, 'images', 'Measurement_Module.jpg'),
            os.path.join(base_dir, 'Measurement_Module.jpg'),
            os.path.join(base_dir, 'src', 'Measurement_Module.jpg'),
            # Also accept the uploaded filename variant
            os.path.join(base_dir, 'src', 'images', '1782708952514_Measurement_Module.jpg'),
            os.path.join(base_dir, 'images', '1782708952514_Measurement_Module.jpg'),
            os.path.join(base_dir, '1782708952514_Measurement_Module.jpg'),
        ]

        if not hasattr(self, '_module_images'):
            self._module_images = {}

        img_path = None
        for p in candidates:
            if os.path.isfile(p):
                img_path = p
                break

        loaded = False
        if img_path:
            try:
                img    = Image.open(img_path).convert("RGB")

                # STRETCH-FILL: resize directly to the card's exact pixel
                # size. The whole image stays fully visible (no cropping)
                # and there are no black margins (no letterboxing) — the
                # image is stretched/squashed non-uniformly to match the
                # card's aspect ratio exactly.
                img = img.resize((card_w, card_h), Image.Resampling.LANCZOS)

                ox = sx1
                oy = sy1

                photo = ImageTk.PhotoImage(img)
                # Dark background (only visible if image somehow doesn't
                # fully cover due to rounding — kept as a safety net).
                # No outline here — the border-less look is intentional.
                c.create_rectangle(sx1, sy1, sx2, sy2,
                                   fill="#0a0e14", outline="",
                                   width=0, tags=tag)
                c.create_image(ox, oy, image=photo, anchor="nw", tags=tag)
                self._module_images[key] = photo
                loaded = True
            except Exception:
                pass

        if not loaded:
            # Fallback
            c.create_rectangle(sx1, sy1, sx2, sy2,
                               fill="#1a4fa0", outline="",
                               width=0, tags=tag)
            mx = (sx1 + sx2) // 2
            my = (sy1 + sy2) // 2
            c.create_text(mx, my - 8,
                          text="VMS-3000",
                          fill="#ffffff",
                          font=tkfont.Font(family="Segoe UI", size=9, weight="bold"),
                          anchor="center", tags=tag)
            c.create_text(mx, my + 8,
                          text="3000/12M/DIS",
                          fill="#aaccff",
                          font=tkfont.Font(family="Segoe UI", size=7),
                          anchor="center", tags=tag)

        # ── Selection border only (amber) — no blue border in any state ──
        if is_sel:
            c.create_rectangle(sx1, sy1, sx2, sy2,
                               fill="", outline="#f0b040",
                               width=3, tags=tag)

        # ── Mouse bindings ────────────────────────────────────────────
        c.tag_bind(tag, "<Enter>",
                   lambda e, t=tag, k=key: self._hover(t, k, True))
        c.tag_bind(tag, "<Leave>",
                   lambda e, t=tag, k=key: self._hover(t, k, False))
        c.tag_bind(tag, "<Button-1>",
                   lambda e, k=key, s=slot_num: self._click(k, s))

    # ── Slot card ────────────────────────────────────────────────────

    def _draw_slot(self, c: tk.Canvas, L: dict, slot_idx: int):
        slot_num = slot_idx + 1
        key      = f"0_{slot_num}"
        tag      = f"s_{key}"
        is_sel   = (self._selected == key)
        module   = self._slot_data.get(key)

        # VMM-6M single-slot image card
        if module and is_image_display_module(module):
            self._draw_detailed_module(c, L, slot_idx, module, is_sel, tag)
            return

        # Relay single-slot image card
        if _is_relay_module(module):
            self._draw_relay_module(c, L, slot_idx, module, is_sel, tag)
            return

        sw  = L["sw"]
        sx1 = L["slot_x0"] + slot_idx * sw + 3
        sx2 = sx1 + sw - 6
        sy1 = L["TOP_Y"] + 2
        sy2 = L["TOP_Y"] + L["SHELL_H"] - 12
        mx  = (sx1 + sx2) // 2
        card_h = sy2 - sy1

        # Always show default appearance - removed disabled gray state
        if is_sel:
            face_col = T["slot_sel_face"]
            edge_col = T["slot_sel"]
        else:
            face_col = T["slot_face"]
            edge_col = T["slot_edge_sh"]

        # Outer card body
        c.create_rectangle(sx1, sy1, sx2, sy2,
                            fill=face_col,
                            outline=edge_col,
                            width=2,
                            tags=tag)

        # Small ejector-handle cap at the top, centred
        cap_w = 22
        cap_h = 8
        c.create_rectangle(mx - cap_w // 2, sy1 + 8,
                            mx + cap_w // 2, sy1 + 8 + cap_h,
                            fill=T["slot_cap"] if not is_sel else "#fde68a",
                            outline=edge_col,
                            width=1, tags=tag)

        # Plain bordered inner panel (no grip texture, no LED, no pins)
        panel_y1 = sy1 + 8 + cap_h + 8
        panel_y2 = sy2 - 10
        c.create_rectangle(sx1 + 6, panel_y1, sx2 - 6, panel_y2,
                            fill=face_col,
                            outline=edge_col,
                            width=1, tags=tag)

        if module:
            short = module.split()[0]
            c.create_text(mx, (panel_y1 + panel_y2) // 2,
                          text=short,
                          font=tkfont.Font(family="Courier New", size=7, weight="bold"),
                          fill=T["slot_mod_fg"],
                          anchor="center",
                          tags=tag)

        # Bottom thin bar
        c.create_rectangle(sx1 + 4, sy2 - 6, sx2 - 4, sy2 - 2,
                            fill="#0a1520",
                            outline="",
                            tags=tag)

        c.tag_bind(tag, "<Enter>",
                   lambda e, t=tag, k=key: self._hover(t, k, True))
        c.tag_bind(tag, "<Leave>",
                   lambda e, t=tag, k=key: self._hover(t, k, False))
        c.tag_bind(tag, "<Button-1>",
                   lambda e, k=key, s=slot_num: self._click(k, s))

    # ══════════════════════════════════════════════════════════════════
    #  VMM-6M detailed module — single-slot image card
    # ══════════════════════════════════════════════════════════════════

    def _draw_detailed_module(self, c: tk.Canvas, L: dict, slot_idx: int,
                              module: str, is_sel: bool, tag: str):
        """Single-slot VMM-6M image card.

        Uses COVER scaling: the image is scaled so it fully fills the
        card's width AND height, with any dimension overflow center-cropped
        away. This guarantees the rendered module image always spans the
        full card width — no black margins on the left/right.
        """
        slot_num = slot_idx + 1
        key      = f"0_{slot_num}"

        sw     = L["sw"]
        sx1    = int(L["slot_x0"] + slot_idx * sw + 3)
        sx2    = int(sx1 + sw - 6)
        sy1    = L["TOP_Y"] + 2
        sy2    = L["TOP_Y"] + L["SHELL_H"] - 12
        slot_w = max(1, sx2 - sx1)
        slot_h = max(1, sy2 - sy1)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(base_dir, 'src', 'images', 'VMM-6M.jpg'),
            os.path.join(base_dir, 'images', 'VMM-6M.jpg'),
            os.path.join(base_dir, 'VMM-6M.jpg'),
            os.path.join(base_dir, 'src', 'VMM-6M.jpg'),
        ]
        img_path = next((p for p in candidates if os.path.isfile(p)), None)

        if not hasattr(self, '_module_images'):
            self._module_images = {}

        loaded = False
        if img_path:
            try:
                img    = Image.open(img_path).convert("RGB")

                # STRETCH-FILL: resize directly to the card's exact pixel
                # size. The whole image stays fully visible (no cropping)
                # and there are no black margins (no letterboxing).
                img = img.resize((slot_w, slot_h), Image.Resampling.LANCZOS)

                ox = sx1
                oy = sy1

                photo = ImageTk.PhotoImage(img)
                # No outline — border-less card in all states.
                c.create_rectangle(sx1, sy1, sx2, sy2,
                                   fill="#0a0e14", outline="",
                                   width=0, tags=tag)
                c.create_image(ox, oy, image=photo, anchor="nw", tags=tag)
                self._module_images[key] = photo
                loaded = True
            except Exception:
                pass

        if not loaded:
            c.create_rectangle(sx1, sy1, sx2, sy2,
                               fill="#1a4fa0", outline="",
                               width=0, tags=tag)
            c.create_text((sx1 + sx2) // 2, (sy1 + sy2) // 2,
                          text="VMM-6M",
                          fill="#ffffff",
                          font=tkfont.Font(family="Segoe UI", size=8, weight="bold"),
                          anchor="center", tags=tag)

        # Selection border only (amber) — no blue border in any state
        if is_sel:
            c.create_rectangle(sx1, sy1, sx2, sy2,
                               fill="", outline="#f0b040",
                               width=3, tags=tag)

        c.tag_bind(tag, "<Enter>",
                   lambda e, t=tag, k=key: self._hover(t, k, True))
        c.tag_bind(tag, "<Leave>",
                   lambda e, t=tag, k=key: self._hover(t, k, False))
        c.tag_bind(tag, "<Button-1>",
                   lambda e, k=key, s=slot_num: self._click(k, s))

    # ══════════════════════════════════════════════════════════════════
    #  3000/RLY — single-slot Relay module image card
    # ══════════════════════════════════════════════════════════════════

    def _draw_relay_module(self, c: tk.Canvas, L: dict, slot_idx: int,
                            module: str, is_sel: bool, tag: str):
        """Single-slot Relay (3000/RLY) image card — same stretch-fill
        behaviour as the VMM-6M card, just a different source image."""
        slot_num = slot_idx + 1
        key      = f"0_{slot_num}"

        sw     = L["sw"]
        sx1    = int(L["slot_x0"] + slot_idx * sw + 3)
        sx2    = int(sx1 + sw - 6)
        sy1    = L["TOP_Y"] + 2
        sy2    = L["TOP_Y"] + L["SHELL_H"] - 12
        slot_w = max(1, sx2 - sx1)
        slot_h = max(1, sy2 - sy1)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(base_dir, 'src', 'images', 'Relay_Module.jpg'),
            os.path.join(base_dir, 'images', 'Relay_Module.jpg'),
            os.path.join(base_dir, 'Relay_Module.jpg'),
            os.path.join(base_dir, 'src', 'Relay_Module.jpg'),
        ]
        img_path = next((p for p in candidates if os.path.isfile(p)), None)

        if not hasattr(self, '_module_images'):
            self._module_images = {}

        loaded = False
        if img_path:
            try:
                img = Image.open(img_path).convert("RGB")

                # STRETCH-FILL: resize directly to the card's exact pixel
                # size, matching the same treatment as VMM-6M / DIS cards.
                img = img.resize((slot_w, slot_h), Image.Resampling.LANCZOS)

                ox = sx1
                oy = sy1

                photo = ImageTk.PhotoImage(img)
                # No outline — border-less card in all states.
                c.create_rectangle(sx1, sy1, sx2, sy2,
                                   fill="#0a0e14", outline="",
                                   width=0, tags=tag)
                c.create_image(ox, oy, image=photo, anchor="nw", tags=tag)
                self._module_images[key] = photo
                loaded = True
            except Exception:
                pass

        if not loaded:
            c.create_rectangle(sx1, sy1, sx2, sy2,
                               fill="#1a4fa0", outline="",
                               width=0, tags=tag)
            c.create_text((sx1 + sx2) // 2, (sy1 + sy2) // 2,
                          text="3000/RLY",
                          fill="#ffffff",
                          font=tkfont.Font(family="Segoe UI", size=8, weight="bold"),
                          anchor="center", tags=tag)

        # Selection border only (amber) — no blue border in any state
        if is_sel:
            c.create_rectangle(sx1, sy1, sx2, sy2,
                               fill="", outline="#f0b040",
                               width=3, tags=tag)

        c.tag_bind(tag, "<Enter>",
                   lambda e, t=tag, k=key: self._hover(t, k, True))
        c.tag_bind(tag, "<Leave>",
                   lambda e, t=tag, k=key: self._hover(t, k, False))
        c.tag_bind(tag, "<Button-1>",
                   lambda e, k=key, s=slot_num: self._click(k, s))

    # ── Interaction ─────────────────────────────────────────────────

    def _hover(self, tag: str, key: str, entering: bool):
        if self._selected == key:
            return
        slot_n   = key.split("_")[1]
        assigned = self._slot_data.get(key)
        # Removed color change logic - rack maintains default appearance
        if entering:
            self._hint_var.set(
                f"Slot {slot_n}  —  "
                + (f"Module: {assigned}" if assigned else "Empty — click to assign module")
            )
        else:
            self._hint_var.set("Click any slot to assign module")

    def _click(self, key: str, slot_num: int):
        self._selected = key
        self.draw()
        self._hint_var.set(f"Slot {slot_num} selected")

        if slot_num == 1:
            self._config_settings_dialog()
        else:
            self._module_dialog(key, slot_num)

    # ── Configuration Settings dialog (for slot 1) ──────────────────

    def _config_settings_dialog(self):
        popup = ConfigurationSettingsPopup(self._canvas, self._fonts)
        popup.show()
        self._selected = None
        self.draw()
        self._hint_var.set("Configuration Settings closed")

    # ── Module assignment dialog ─────────────────────────────────────

    def _module_dialog(self, key: str, slot_num: int):
        def on_selection(selection):
            current_module = self._slot_data.get(key)
            
            # If there's already a module and user is switching to a different module
            # (not "No Modules"), show confirmation popup
            if current_module and selection != "No Modules" and current_module != selection:
                def on_switch_confirmed(confirmed):
                    if confirmed:
                        if selection == "No Modules":
                            self._slot_data.pop(key, None)
                        else:
                            self._slot_data[key] = selection
                        self._selected = key
                        self.draw()
                        self._hint_var.set(
                            f"Slot {slot_num} → {self._slot_data.get(key, 'Empty')}"
                        )
                
                popup = ModuleSwitchConfirmationPopup(
                    self._canvas, self._fonts, current_module, selection, on_switch_confirmed
                )
                popup.show()
                return
            
            if selection == "No Modules":
                self._slot_data.pop(key, None)
            else:
                self._slot_data[key] = selection
            # Keep selection to show enabled color after module assignment
            self._selected = key
            self.draw()
            self._hint_var.set(
                f"Slot {slot_num} → {self._slot_data.get(key, 'Empty')}"
            )

        popup = ModuleSelectionPopup(self._canvas, self._fonts, slot_num, on_selection)
        popup.show()