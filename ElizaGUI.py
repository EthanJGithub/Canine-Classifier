#!/usr/bin/env python3
"""
Canine Classifier - Ultra Premium 2025 UI
Inspired by modern streaming apps and premium dashboards.
Glass morphism, gradients, and sleek rounded components.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
import threading
import webbrowser
import math

try:
    from PIL import Image, ImageTk, ImageDraw, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    from breed_info import BREED_INFO, get_breed_info
except ImportError:
    BREED_INFO = {}
    def get_breed_info(breed): return None


# ═══════════════════════════════════════════════════════════════════════════════
# PREMIUM THEME
# ═══════════════════════════════════════════════════════════════════════════════

class Theme:
    """Ultra-premium dark theme inspired by streaming apps."""

    # Deep backgrounds
    BG_DARKEST = "#05050a"
    BG_DARK = "#080812"
    BG = "#0d0d1a"
    BG_LIGHT = "#12122a"

    # Card surfaces
    CARD_DARK = "#14142b"
    CARD = "#1a1a3a"
    CARD_LIGHT = "#22224a"
    CARD_HOVER = "#2a2a5a"

    # Glass effect
    GLASS = "#1e1e4a"
    GLASS_LIGHT = "#28285a"
    GLASS_BORDER = "#3a3a7a"

    # Vibrant gradients
    CYAN_START = "#00e5ff"
    CYAN_END = "#00b4d8"
    TEAL_START = "#00ffc8"
    TEAL_END = "#00d4aa"
    PINK_START = "#ff6b9d"
    PINK_END = "#c44569"
    PURPLE_START = "#a855f7"
    PURPLE_END = "#7c3aed"
    ORANGE_START = "#ff9f43"
    ORANGE_END = "#ee5a24"

    # Solid accents
    CYAN = "#00e5ff"
    TEAL = "#00e5c0"
    PINK = "#ff6b9d"
    PURPLE = "#a855f7"
    ORANGE = "#ff9f43"
    GREEN = "#22c55e"
    RED = "#ef4444"
    BLUE = "#3b82f6"

    # Text
    WHITE = "#ffffff"
    TEXT_PRIMARY = "#f8f8ff"
    TEXT_SECONDARY = "#a8a8d8"
    TEXT_MUTED = "#6868a8"
    TEXT_DISABLED = "#484878"

    # Borders and lines
    BORDER = "#2a2a5a"
    BORDER_LIGHT = "#3a3a6a"
    DIVIDER = "#1e1e3e"


# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM CANVAS WIDGETS
# ═══════════════════════════════════════════════════════════════════════════════

class RoundedFrame(tk.Canvas):
    """A frame with rounded corners using canvas."""

    def __init__(self, parent, width=200, height=100, radius=20,
                 bg_color=Theme.CARD, border_color=None, border_width=0, **kwargs):
        super().__init__(parent, width=width, height=height,
                        bg=parent.cget('bg'), highlightthickness=0, **kwargs)
        self.bg_color = bg_color
        self.border_color = border_color or bg_color
        self.border_width = border_width
        self.radius = radius
        self._width = width
        self._height = height

        self.bind('<Configure>', self._redraw)
        self._draw()

    def _draw(self):
        self.delete('all')
        w, h, r = self._width, self._height, self.radius

        # Draw rounded rectangle
        self.create_rounded_rect(0, 0, w, h, r,
                                fill=self.bg_color,
                                outline=self.border_color,
                                width=self.border_width)

    def _redraw(self, event=None):
        if event:
            self._width = event.width
            self._height = event.height
        self._draw()

    def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1+r, y1,
            x2-r, y1,
            x2, y1,
            x2, y1+r,
            x2, y2-r,
            x2, y2,
            x2-r, y2,
            x1+r, y2,
            x1, y2,
            x1, y2-r,
            x1, y1+r,
            x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def set_hover(self, color):
        self.bg_color = color
        self._draw()


class GradientBar(tk.Canvas):
    """A progress bar with gradient fill."""

    def __init__(self, parent, width=150, height=10, progress=0,
                 start_color=Theme.CYAN_START, end_color=Theme.CYAN_END,
                 bg_color=Theme.BG_DARK, **kwargs):
        super().__init__(parent, width=width, height=height,
                        bg=parent.cget('bg'), highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.progress = progress
        self.start_color = start_color
        self.end_color = end_color
        self.bg_color = bg_color
        self._draw()

    def _draw(self):
        self.delete('all')
        r = self.height // 2

        # Background track
        self._rounded_rect(0, 0, self.width, self.height, r, self.bg_color)

        # Progress fill with gradient simulation
        if self.progress > 0:
            fill_width = max(self.height, int(self.width * self.progress / 100))
            # Draw gradient by drawing multiple thin lines
            steps = max(1, fill_width - self.height)
            for i in range(steps + self.height):
                x = i
                if x > fill_width:
                    break
                # Interpolate color
                t = i / max(1, fill_width)
                color = self._interpolate_color(self.start_color, self.end_color, t)
                self.create_line(x, 1, x, self.height-1, fill=color)

            # Round the ends
            self.create_oval(0, 0, self.height, self.height,
                           fill=self.start_color, outline='')
            if fill_width > self.height:
                self.create_oval(fill_width-self.height, 0, fill_width, self.height,
                               fill=self._interpolate_color(self.start_color, self.end_color, 1),
                               outline='')

    def _rounded_rect(self, x1, y1, x2, y2, r, color):
        self.create_oval(x1, y1, x1+2*r, y1+2*r, fill=color, outline='')
        self.create_oval(x2-2*r, y1, x2, y1+2*r, fill=color, outline='')
        self.create_oval(x1, y2-2*r, x1+2*r, y2, fill=color, outline='')
        self.create_oval(x2-2*r, y2-2*r, x2, y2, fill=color, outline='')
        self.create_rectangle(x1+r, y1, x2-r, y2, fill=color, outline='')
        self.create_rectangle(x1, y1+r, x2, y2-r, fill=color, outline='')

    def _interpolate_color(self, c1, c2, t):
        """Interpolate between two hex colors."""
        r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
        r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return f'#{r:02x}{g:02x}{b:02x}'

    def set_progress(self, value):
        self.progress = max(0, min(100, value))
        self._draw()


class CircleBadge(tk.Canvas):
    """A circular badge with number or icon."""

    def __init__(self, parent, size=40, text="1",
                 bg_color=Theme.CYAN, fg_color=Theme.BG_DARK,
                 font_size=14, **kwargs):
        super().__init__(parent, width=size, height=size,
                        bg=parent.cget('bg'), highlightthickness=0, **kwargs)
        self.size = size
        self.text = text
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.font_size = font_size
        self._draw()

    def _draw(self):
        self.delete('all')
        # Circle
        self.create_oval(0, 0, self.size, self.size,
                        fill=self.bg_color, outline='')
        # Text
        self.create_text(self.size//2, self.size//2, text=self.text,
                        fill=self.fg_color, font=('Segoe UI Semibold', self.font_size))


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Canine Classifier")

        # Screen sizing - generous sizing
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        self.w = min(int(sw * 0.9), 1500)
        self.h = min(int(sh * 0.9), 900)
        self.scale = min(self.w / 1500, self.h / 900)

        x, y = (sw - self.w) // 2, (sh - self.h) // 2
        root.geometry(f"{self.w}x{self.h}+{x}+{y}")
        root.configure(bg=Theme.BG_DARK)
        root.minsize(1100, 700)

        # Premium fonts
        base = max(int(13 * self.scale), 11)
        self.F = {
            'hero': ('Segoe UI', int(base * 2.6), 'bold'),
            'h1': ('Segoe UI Semibold', int(base * 1.8)),
            'h2': ('Segoe UI Semibold', int(base * 1.4)),
            'h3': ('Segoe UI Semibold', int(base * 1.15)),
            'body': ('Segoe UI', base),
            'body_medium': ('Segoe UI Semibold', base),
            'sm': ('Segoe UI', int(base * 0.9)),
            'xs': ('Segoe UI', int(base * 0.8)),
            'icon': ('Segoe UI Symbol', int(base * 1.2)),
        }

        self.frame = None
        self.classifier = None
        self.tree = self._build_tree()
        self.node = None
        self.qnum = 0

        self._setup_styles()
        self.home()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Premium combobox
        style.configure('Premium.TCombobox',
            fieldbackground=Theme.CARD_DARK,
            background=Theme.CARD,
            foreground=Theme.TEXT_PRIMARY,
            arrowcolor=Theme.CYAN,
            borderwidth=0,
            padding=12,
            relief='flat')
        style.map('Premium.TCombobox',
            fieldbackground=[('readonly', Theme.CARD_DARK), ('focus', Theme.CARD)],
            selectbackground=[('readonly', Theme.CYAN)],
            bordercolor=[('focus', Theme.CYAN)])

    def s(self, v):
        """Scale value based on window size."""
        return max(int(v * self.scale), 1)

    def clear(self):
        if self.frame:
            self.frame.destroy()

    # ═══════════════════════════════════════════════════════════════════════════
    # PREMIUM UI COMPONENTS
    # ═══════════════════════════════════════════════════════════════════════════

    def create_glass_card(self, parent, padx=0, pady=0):
        """Create a premium glass-morphism card."""
        outer = tk.Frame(parent, bg=Theme.BG)
        outer.pack(fill='both', expand=True, padx=padx, pady=pady)

        # Card with subtle border
        card = tk.Frame(outer, bg=Theme.CARD,
                       highlightbackground=Theme.GLASS_BORDER,
                       highlightthickness=1)
        card.pack(fill='both', expand=True)

        return card

    def gradient_button(self, parent, text, command,
                       color_start=None, color_end=None,
                       width=None, size='normal'):
        """Create a button with gradient-like appearance."""
        color_start = color_start or Theme.CYAN_START
        color_end = color_end or Theme.CYAN_END

        # Use the brighter color
        bg = color_start
        fg = Theme.BG_DARK if self._is_light_color(color_start) else Theme.WHITE

        pad_x = self.s(32) if size == 'normal' else self.s(20)
        pad_y = self.s(14) if size == 'normal' else self.s(10)
        font = self.F['body_medium'] if size == 'normal' else self.F['sm']

        frame = tk.Frame(parent, bg=bg, cursor='hand2')
        label = tk.Label(frame, text=text, font=font, fg=fg, bg=bg,
                        padx=pad_x, pady=pad_y)
        label.pack()

        # Hover effects
        hover_color = self._lighten_color(color_start, 0.15)

        def on_enter(e):
            frame.config(bg=hover_color)
            label.config(bg=hover_color)

        def on_leave(e):
            frame.config(bg=bg)
            label.config(bg=bg)

        frame.bind('<Enter>', on_enter)
        frame.bind('<Leave>', on_leave)
        frame.bind('<Button-1>', lambda e: command())
        label.bind('<Button-1>', lambda e: command())

        return frame

    def ghost_button(self, parent, text, command, color=None, size='normal'):
        """Create a subtle outline button."""
        color = color or Theme.TEXT_SECONDARY

        pad_x = self.s(28) if size == 'normal' else self.s(18)
        pad_y = self.s(12) if size == 'normal' else self.s(8)
        font = self.F['body'] if size == 'normal' else self.F['sm']

        frame = tk.Frame(parent, bg=Theme.CARD_DARK, cursor='hand2',
                        highlightbackground=Theme.BORDER,
                        highlightthickness=1)
        label = tk.Label(frame, text=text, font=font,
                        fg=color, bg=Theme.CARD_DARK,
                        padx=pad_x, pady=pad_y)
        label.pack()

        def on_enter(e):
            frame.config(bg=Theme.CARD_HOVER, highlightbackground=Theme.CYAN)
            label.config(bg=Theme.CARD_HOVER, fg=Theme.WHITE)

        def on_leave(e):
            frame.config(bg=Theme.CARD_DARK, highlightbackground=Theme.BORDER)
            label.config(bg=Theme.CARD_DARK, fg=color)

        frame.bind('<Enter>', on_enter)
        frame.bind('<Leave>', on_leave)
        frame.bind('<Button-1>', lambda e: command())
        label.bind('<Button-1>', lambda e: command())

        return frame

    def icon_button(self, parent, icon, command, color=None, size=40):
        """Create a circular icon button."""
        color = color or Theme.CYAN
        bg = Theme.CARD_DARK

        canvas = tk.Canvas(parent, width=size, height=size,
                          bg=parent.cget('bg'), highlightthickness=0,
                          cursor='hand2')

        # Draw circle
        canvas.create_oval(2, 2, size-2, size-2, fill=bg, outline=Theme.BORDER)
        canvas.create_text(size//2, size//2, text=icon,
                          fill=color, font=self.F['icon'])

        def on_enter(e):
            canvas.delete('all')
            canvas.create_oval(2, 2, size-2, size-2, fill=Theme.CARD_HOVER, outline=color)
            canvas.create_text(size//2, size//2, text=icon, fill=color, font=self.F['icon'])

        def on_leave(e):
            canvas.delete('all')
            canvas.create_oval(2, 2, size-2, size-2, fill=bg, outline=Theme.BORDER)
            canvas.create_text(size//2, size//2, text=icon, fill=color, font=self.F['icon'])

        canvas.bind('<Enter>', on_enter)
        canvas.bind('<Leave>', on_leave)
        canvas.bind('<Button-1>', lambda e: command())

        return canvas

    def section_header(self, parent, title, subtitle=None, color=None):
        """Create a section header with optional subtitle."""
        frame = tk.Frame(parent, bg=parent.cget('bg'))

        title_label = tk.Label(frame, text=title, font=self.F['h2'],
                              fg=color or Theme.TEXT_PRIMARY,
                              bg=parent.cget('bg'))
        title_label.pack(anchor='w')

        if subtitle:
            sub_label = tk.Label(frame, text=subtitle, font=self.F['sm'],
                               fg=Theme.TEXT_MUTED, bg=parent.cget('bg'))
            sub_label.pack(anchor='w', pady=(self.s(2), 0))

        return frame

    def back_navigation(self, parent):
        """Create a sleek back navigation."""
        frame = tk.Frame(parent, bg=parent.cget('bg'), cursor='hand2')

        # Arrow icon
        arrow = tk.Label(frame, text="←", font=('Segoe UI', self.s(18)),
                        fg=Theme.TEXT_SECONDARY, bg=parent.cget('bg'))
        arrow.pack(side='left')

        # Text
        text = tk.Label(frame, text="Back", font=self.F['sm'],
                       fg=Theme.TEXT_SECONDARY, bg=parent.cget('bg'))
        text.pack(side='left', padx=(self.s(6), 0))

        def on_enter(e):
            arrow.config(fg=Theme.CYAN)
            text.config(fg=Theme.CYAN)

        def on_leave(e):
            arrow.config(fg=Theme.TEXT_SECONDARY)
            text.config(fg=Theme.TEXT_SECONDARY)

        for widget in [frame, arrow, text]:
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
            widget.bind('<Button-1>', lambda e: self.home())

        return frame

    def _is_light_color(self, hex_color):
        """Check if a color is light (for text contrast)."""
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return luminance > 0.5

    def _lighten_color(self, hex_color, factor):
        """Lighten a hex color by a factor."""
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        return f'#{r:02x}{g:02x}{b:02x}'

    # ═══════════════════════════════════════════════════════════════════════════
    # HOME PAGE
    # ═══════════════════════════════════════════════════════════════════════════

    def home(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # === HEADER ===
        header = tk.Frame(self.frame, bg=Theme.BG)
        header.pack(fill='x', padx=self.s(70), pady=(self.s(50), self.s(35)))

        # Logo/Title area
        title_area = tk.Frame(header, bg=Theme.BG)
        title_area.pack(anchor='w')

        # Main title with gradient feel
        title_row = tk.Frame(title_area, bg=Theme.BG)
        title_row.pack(anchor='w')

        tk.Label(title_row, text="Canine", font=self.F['hero'],
                fg=Theme.WHITE, bg=Theme.BG).pack(side='left')
        tk.Label(title_row, text="Classifier", font=self.F['hero'],
                fg=Theme.CYAN, bg=Theme.BG).pack(side='left', padx=(self.s(15), 0))

        # Subtitle
        tk.Label(title_area, text="AI-Powered Dog Breed Identification System",
                font=self.F['h3'], fg=Theme.TEXT_SECONDARY,
                bg=Theme.BG).pack(anchor='w', pady=(self.s(10), 0))

        # === MAIN CARDS GRID ===
        grid = tk.Frame(self.frame, bg=Theme.BG)
        grid.pack(fill='both', expand=True, padx=self.s(70), pady=self.s(10))

        grid.grid_columnconfigure(0, weight=1, uniform='col')
        grid.grid_columnconfigure(1, weight=1, uniform='col')
        grid.grid_rowconfigure(0, weight=1, uniform='row')
        grid.grid_rowconfigure(1, weight=1, uniform='row')

        cards = [
            ("01", "AI Recognition", "Upload a photo for instant breed detection using deep learning",
             Theme.CYAN, Theme.CYAN_END, "🔍", self.ai_page),
            ("02", "Questionnaire", "Answer questions about your dog's physical characteristics",
             Theme.PINK, Theme.PINK_END, "📝", self.quest_page),
            ("03", "Dichotomous Key", "Scientific Yes/No identification method",
             Theme.TEAL, Theme.TEAL_END, "🌳", self.dkey_page),
            ("04", "Breed Database", "Explore detailed information on 51+ dog breeds",
             Theme.ORANGE, Theme.ORANGE_END, "📚", self.db_page),
        ]

        for i, (num, title, desc, color, color2, icon, cmd) in enumerate(cards):
            row, col = divmod(i, 2)
            self._create_premium_card(grid, num, title, desc, color, color2, icon, cmd, row, col)

        # === FOOTER ===
        footer = tk.Frame(self.frame, bg=Theme.BG)
        footer.pack(fill='x', pady=self.s(25))

        footer_text = tk.Label(footer,
                              text="Version 2.0  •  51 Breeds  •  Powered by AI",
                              font=self.F['xs'], fg=Theme.TEXT_DISABLED, bg=Theme.BG)
        footer_text.pack()

    def _create_premium_card(self, parent, num, title, desc, color, color2, icon, cmd, row, col):
        """Create a premium animated card."""
        # Outer container
        container = tk.Frame(parent, bg=Theme.BG)
        container.grid(row=row, column=col, padx=self.s(12), pady=self.s(12), sticky='nsew')

        # Card with border
        card = tk.Frame(container, bg=Theme.CARD,
                       highlightbackground=Theme.BORDER,
                       highlightthickness=1,
                       cursor='hand2')
        card.pack(fill='both', expand=True)

        inner = tk.Frame(card, bg=Theme.CARD)
        inner.pack(fill='both', expand=True, padx=self.s(30), pady=self.s(28))

        # Top row: Badge and icon
        top = tk.Frame(inner, bg=Theme.CARD)
        top.pack(fill='x')

        # Number badge with accent color
        badge_frame = tk.Frame(top, bg=color)
        badge_frame.pack(side='left')
        badge_label = tk.Label(badge_frame, text=f"  {num}  ", font=self.F['h3'],
                              fg=Theme.BG_DARK, bg=color)
        badge_label.pack(padx=self.s(2), pady=self.s(2))

        # Icon on right
        icon_label = tk.Label(top, text=icon, font=('Segoe UI', self.s(24)),
                             fg=color, bg=Theme.CARD)
        icon_label.pack(side='right')

        # Title
        title_label = tk.Label(inner, text=title, font=self.F['h2'],
                              fg=Theme.WHITE, bg=Theme.CARD)
        title_label.pack(anchor='w', pady=(self.s(20), self.s(8)))

        # Description
        desc_label = tk.Label(inner, text=desc, font=self.F['sm'],
                             fg=Theme.TEXT_SECONDARY, bg=Theme.CARD,
                             wraplength=self.s(300), justify='left')
        desc_label.pack(anchor='w')

        # Bottom arrow
        bottom = tk.Frame(inner, bg=Theme.CARD)
        bottom.pack(side='bottom', fill='x')

        arrow = tk.Label(bottom, text="→", font=('Segoe UI', self.s(26)),
                        fg=color, bg=Theme.CARD)
        arrow.pack(side='right')

        # Hover animation
        all_widgets = [card, inner, top, bottom, title_label, desc_label, icon_label, arrow]

        def on_enter(e):
            card.config(highlightbackground=color, bg=Theme.CARD_HOVER)
            for w in all_widgets:
                try:
                    if w not in [badge_frame, badge_label]:
                        w.config(bg=Theme.CARD_HOVER)
                except: pass

        def on_leave(e):
            card.config(highlightbackground=Theme.BORDER, bg=Theme.CARD)
            for w in all_widgets:
                try:
                    if w not in [badge_frame, badge_label]:
                        w.config(bg=Theme.CARD)
                except: pass

        for w in all_widgets + [badge_frame, badge_label]:
            w.bind('<Enter>', on_enter)
            w.bind('<Leave>', on_leave)
            w.bind('<Button-1>', lambda e, c=cmd: c())

    # ═══════════════════════════════════════════════════════════════════════════
    # AI RECOGNITION PAGE
    # ═══════════════════════════════════════════════════════════════════════════

    def ai_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Header
        header = tk.Frame(self.frame, bg=Theme.BG)
        header.pack(fill='x', padx=self.s(50), pady=(self.s(30), self.s(20)))

        self.back_navigation(header).pack(side='left')

        title_area = tk.Frame(header, bg=Theme.BG)
        title_area.pack(side='left', padx=(self.s(25), 0))

        tk.Label(title_area, text="AI Recognition", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(anchor='w')
        tk.Label(title_area, text="Upload a photo to identify the breed instantly",
                font=self.F['sm'], fg=Theme.TEXT_SECONDARY, bg=Theme.BG).pack(anchor='w')

        # Main content - two columns
        content = tk.Frame(self.frame, bg=Theme.BG)
        content.pack(fill='both', expand=True, padx=self.s(50), pady=(0, self.s(35)))

        # === LEFT: Upload Panel ===
        left = tk.Frame(content, bg=Theme.BG)
        left.pack(side='left', fill='both', expand=True, padx=(0, self.s(15)))

        upload_card = tk.Frame(left, bg=Theme.CARD,
                              highlightbackground=Theme.GLASS_BORDER,
                              highlightthickness=1)
        upload_card.pack(fill='both', expand=True)

        upload_inner = tk.Frame(upload_card, bg=Theme.CARD)
        upload_inner.pack(fill='both', expand=True, padx=self.s(28), pady=self.s(28))

        # Upload header
        upload_header = self.section_header(upload_inner, "Upload Image",
                                           "Supports JPG, PNG, WebP, GIF")
        upload_header.pack(anchor='w')

        # Preview area
        preview_container = tk.Frame(upload_inner, bg=Theme.CARD_DARK,
                                    highlightbackground=Theme.BORDER,
                                    highlightthickness=2)
        preview_container.pack(fill='both', expand=True, pady=(self.s(20), self.s(18)))

        self.preview_frame = tk.Frame(preview_container, bg=Theme.CARD_DARK)
        self.preview_frame.pack(fill='both', expand=True, padx=3, pady=3)

        # Placeholder
        self.placeholder = tk.Frame(self.preview_frame, bg=Theme.CARD_DARK)
        self.placeholder.place(relx=0.5, rely=0.5, anchor='center')

        # Upload icon circle
        icon_size = self.s(80)
        icon_canvas = tk.Canvas(self.placeholder, width=icon_size, height=icon_size,
                               bg=Theme.CARD_DARK, highlightthickness=0)
        icon_canvas.pack()
        icon_canvas.create_oval(2, 2, icon_size-2, icon_size-2,
                               fill=Theme.GLASS, outline=Theme.GLASS_BORDER, width=2)
        icon_canvas.create_text(icon_size//2, icon_size//2, text="+",
                               fill=Theme.CYAN, font=('Segoe UI Light', self.s(36)))

        tk.Label(self.placeholder, text="Click browse or drag image here",
                font=self.F['body'], fg=Theme.TEXT_SECONDARY,
                bg=Theme.CARD_DARK).pack(pady=(self.s(15), 0))
        tk.Label(self.placeholder, text="Maximum file size: 10MB",
                font=self.F['xs'], fg=Theme.TEXT_MUTED,
                bg=Theme.CARD_DARK).pack(pady=(self.s(5), 0))

        self.preview_photo = None
        self.preview_label = None

        # File info
        self.file_var = tk.StringVar(value="No file selected")
        tk.Label(upload_inner, textvariable=self.file_var, font=self.F['xs'],
                fg=Theme.TEXT_MUTED, bg=Theme.CARD).pack(anchor='w', pady=(0, self.s(15)))

        # Buttons row
        btn_row = tk.Frame(upload_inner, bg=Theme.CARD)
        btn_row.pack(fill='x')

        self.ghost_button(btn_row, "Browse Files", self._browse_image).pack(side='left', padx=(0, self.s(12)))
        self.gradient_button(btn_row, "Analyze Image", self._analyze_image).pack(side='left')

        # Status
        self.status_var = tk.StringVar()
        tk.Label(upload_inner, textvariable=self.status_var, font=self.F['sm'],
                fg=Theme.CYAN, bg=Theme.CARD).pack(pady=(self.s(18), 0))

        # === RIGHT: Results Panel ===
        right = tk.Frame(content, bg=Theme.BG)
        right.pack(side='left', fill='both', expand=True, padx=(self.s(15), 0))

        results_card = tk.Frame(right, bg=Theme.CARD,
                               highlightbackground=Theme.GLASS_BORDER,
                               highlightthickness=1)
        results_card.pack(fill='both', expand=True)

        results_inner = tk.Frame(results_card, bg=Theme.CARD)
        results_inner.pack(fill='both', expand=True, padx=self.s(28), pady=self.s(28))

        # Results header
        results_header = self.section_header(results_inner, "Analysis Results",
                                            "Top predictions with confidence scores")
        results_header.pack(anchor='w')

        # Results container
        self.results_frame = tk.Frame(results_inner, bg=Theme.CARD)
        self.results_frame.pack(fill='both', expand=True, pady=(self.s(18), 0))

        self._show_empty_results()
        self.selected_image = None

    def _show_empty_results(self):
        """Show placeholder when no results."""
        for w in self.results_frame.winfo_children():
            w.destroy()

        placeholder = tk.Frame(self.results_frame, bg=Theme.CARD)
        placeholder.pack(expand=True)

        # Empty state icon
        icon_canvas = tk.Canvas(placeholder, width=self.s(70), height=self.s(70),
                               bg=Theme.CARD, highlightthickness=0)
        icon_canvas.pack()
        icon_canvas.create_oval(5, 5, self.s(65), self.s(65),
                               outline=Theme.BORDER, width=2)
        icon_canvas.create_text(self.s(35), self.s(35), text="?",
                               fill=Theme.TEXT_MUTED, font=('Segoe UI', self.s(28)))

        tk.Label(placeholder, text="No analysis yet", font=self.F['body_medium'],
                fg=Theme.TEXT_SECONDARY, bg=Theme.CARD).pack(pady=(self.s(15), 0))
        tk.Label(placeholder, text="Upload an image to identify the breed",
                font=self.F['sm'], fg=Theme.TEXT_MUTED,
                bg=Theme.CARD).pack(pady=(self.s(5), 0))

    def _browse_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.webp")])
        if path:
            self.selected_image = path
            name = os.path.basename(path)
            self.file_var.set(name[:40] + "..." if len(name) > 43 else name)
            self._show_preview(path)

    def _show_preview(self, path):
        if not PIL_AVAILABLE:
            return
        try:
            img = Image.open(path)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            self.preview_frame.update()
            max_w = max(self.preview_frame.winfo_width() - 30, 100)
            max_h = max(self.preview_frame.winfo_height() - 30, 100)

            ratio = min(max_w / img.width, max_h / img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

            self.preview_photo = ImageTk.PhotoImage(img)
            self.placeholder.place_forget()

            if not self.preview_label:
                self.preview_label = tk.Label(self.preview_frame, bg=Theme.CARD_DARK)
            self.preview_label.config(image=self.preview_photo)
            self.preview_label.place(relx=0.5, rely=0.5, anchor='center')
        except Exception:
            pass

    def _analyze_image(self):
        if not self.selected_image:
            self.status_var.set("Please select an image first")
            return

        for w in self.results_frame.winfo_children():
            w.destroy()

        # Loading animation
        loading = tk.Frame(self.results_frame, bg=Theme.CARD)
        loading.pack(expand=True)

        # Spinning indicator (static for now)
        load_canvas = tk.Canvas(loading, width=self.s(50), height=self.s(50),
                               bg=Theme.CARD, highlightthickness=0)
        load_canvas.pack()
        load_canvas.create_arc(5, 5, self.s(45), self.s(45), start=0, extent=300,
                              outline=Theme.CYAN, width=3, style='arc')

        tk.Label(loading, text="Analyzing image...", font=self.F['body'],
                fg=Theme.TEXT_SECONDARY, bg=Theme.CARD).pack(pady=(self.s(12), 0))

        self.status_var.set("Processing...")
        self.root.update()

        threading.Thread(target=self._run_classification, daemon=True).start()

    def _run_classification(self):
        try:
            from image_classifier import DogImageClassifier
            if not self.classifier:
                self.classifier = DogImageClassifier()
            results = self.classifier.classify_image(self.selected_image)
            self.root.after(0, lambda: self._display_results(results))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)[:50]}"))

    def _display_results(self, results):
        self.status_var.set("")

        for w in self.results_frame.winfo_children():
            w.destroy()

        if not results:
            self.status_var.set("Could not classify image")
            self._show_empty_results()
            return

        # Color pairs for gradient bars
        color_pairs = [
            (Theme.CYAN_START, Theme.CYAN_END),
            (Theme.TEAL_START, Theme.TEAL_END),
            (Theme.PINK_START, Theme.PINK_END),
            (Theme.ORANGE_START, Theme.ORANGE_END),
            (Theme.PURPLE_START, Theme.PURPLE_END),
        ]

        for i, result in enumerate(results[:5]):
            breed = result.get('breed', 'Unknown')
            confidence = result.get('confidence', 0)
            verified = result.get('verified', False)
            db_name = result.get('db_name', breed)
            display_name = db_name if verified else breed

            colors = color_pairs[i] if i < len(color_pairs) else color_pairs[-1]

            # Result card
            card = tk.Frame(self.results_frame, bg=Theme.CARD_LIGHT, cursor='hand2')
            card.pack(fill='x', pady=self.s(6))

            inner = tk.Frame(card, bg=Theme.CARD_LIGHT)
            inner.pack(fill='x', padx=self.s(18), pady=self.s(16))

            # Left section
            left = tk.Frame(inner, bg=Theme.CARD_LIGHT)
            left.pack(side='left', fill='both', expand=True)

            # Rank badge using CircleBadge-like approach
            rank_row = tk.Frame(left, bg=Theme.CARD_LIGHT)
            rank_row.pack(anchor='w')

            rank_badge = CircleBadge(rank_row, size=self.s(36), text=str(i+1),
                                    bg_color=colors[0], fg_color=Theme.BG_DARK,
                                    font_size=self.s(13))
            rank_badge.pack(side='left')

            # Name and status
            info_col = tk.Frame(rank_row, bg=Theme.CARD_LIGHT)
            info_col.pack(side='left', padx=(self.s(14), 0))

            tk.Label(info_col, text=display_name, font=self.F['body_medium'],
                    fg=Theme.WHITE, bg=Theme.CARD_LIGHT).pack(anchor='w')

            status_text = "✓ Verified in database" if verified else "AI prediction"
            status_color = Theme.GREEN if verified else Theme.TEXT_MUTED
            tk.Label(info_col, text=status_text, font=self.F['xs'],
                    fg=status_color, bg=Theme.CARD_LIGHT).pack(anchor='w')

            # Right section - Progress bar and percentage
            right = tk.Frame(inner, bg=Theme.CARD_LIGHT)
            right.pack(side='right')

            # Gradient progress bar
            bar = GradientBar(right, width=self.s(160), height=self.s(14),
                            progress=confidence,
                            start_color=colors[0], end_color=colors[1],
                            bg_color=Theme.BG_LIGHT)
            bar.pack(side='left', padx=(0, self.s(15)))

            # Percentage
            tk.Label(right, text=f"{confidence:.1f}%", font=self.F['body_medium'],
                    fg=colors[0], bg=Theme.CARD_LIGHT, width=7, anchor='e').pack(side='left')

            # Click handlers
            def make_click(name):
                return lambda e: self._show_breed_popup(name)

            for widget in [card, inner, left, rank_row, info_col, right]:
                widget.bind('<Button-1>', make_click(display_name))

            # Hover effect
            def make_enter(c, clr):
                return lambda e: c.config(highlightbackground=clr, highlightthickness=2)
            def make_leave(c):
                return lambda e: c.config(highlightthickness=0)

            card.bind('<Enter>', make_enter(card, colors[0]))
            card.bind('<Leave>', make_leave(card))

        # Footer
        tk.Label(self.results_frame, text="Click any result to view breed details",
                font=self.F['xs'], fg=Theme.TEXT_MUTED, bg=Theme.CARD).pack(pady=(self.s(20), 0))

    # ═══════════════════════════════════════════════════════════════════════════
    # QUESTIONNAIRE PAGE
    # ═══════════════════════════════════════════════════════════════════════════

    def quest_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Header
        header = tk.Frame(self.frame, bg=Theme.BG)
        header.pack(fill='x', padx=self.s(50), pady=(self.s(30), self.s(20)))

        self.back_navigation(header).pack(side='left')

        title_area = tk.Frame(header, bg=Theme.BG)
        title_area.pack(side='left', padx=(self.s(25), 0))

        tk.Label(title_area, text="Questionnaire", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(anchor='w')
        tk.Label(title_area, text="Select your dog's characteristics",
                font=self.F['sm'], fg=Theme.TEXT_SECONDARY, bg=Theme.BG).pack(anchor='w')

        # Content
        content = tk.Frame(self.frame, bg=Theme.BG)
        content.pack(fill='both', expand=True, padx=self.s(50), pady=(0, self.s(35)))

        # Form card
        form_card = tk.Frame(content, bg=Theme.CARD,
                            highlightbackground=Theme.GLASS_BORDER,
                            highlightthickness=1)
        form_card.pack(fill='x')

        form_inner = tk.Frame(form_card, bg=Theme.CARD)
        form_inner.pack(fill='x', padx=self.s(35), pady=self.s(35))

        # Questions
        self.quest_vars = {}
        questions = [
            ("color", "Primary Color", ["Black", "White", "Brown", "Tan", "Brindle", "Merle", "Chocolate", "Yellow"]),
            ("ear", "Ear Type", ["Floppy", "Tall", "Triangular"]),
            ("tail", "Tail Type", ["Docked", "Long_and_curved", "Curled"]),
            ("size", "Size", ["Small", "Medium", "Large", "Giant"]),
            ("coat", "Coat Type", ["Short", "Medium", "Long", "Curly", "Double", "Smooth"]),
        ]

        row_frame = None
        for i, (key, label, options) in enumerate(questions):
            if i % 2 == 0:
                row_frame = tk.Frame(form_inner, bg=Theme.CARD)
                row_frame.pack(fill='x', pady=self.s(12))

            q_frame = tk.Frame(row_frame, bg=Theme.CARD)
            q_frame.pack(side='left', fill='x', expand=True, padx=self.s(10))

            tk.Label(q_frame, text=label, font=self.F['sm'],
                    fg=Theme.TEXT_SECONDARY, bg=Theme.CARD).pack(anchor='w')

            var = tk.StringVar(value=options[0])
            self.quest_vars[key] = var

            combo = ttk.Combobox(q_frame, textvariable=var, values=options,
                               state='readonly', font=self.F['body'],
                               style='Premium.TCombobox', width=self.s(22))
            combo.pack(anchor='w', pady=(self.s(6), 0))

        # Submit button
        btn_frame = tk.Frame(content, bg=Theme.BG)
        btn_frame.pack(pady=self.s(25))

        self.gradient_button(btn_frame, "Find Matching Breeds", self._run_questionnaire,
                            color_start=Theme.PINK, color_end=Theme.PINK_END).pack()

        # Results area
        self.quest_results = tk.Frame(content, bg=Theme.BG)
        self.quest_results.pack(fill='both', expand=True)

    def _run_questionnaire(self):
        for w in self.quest_results.winfo_children():
            w.destroy()

        db = Database()
        results = db.query(
            self.quest_vars["color"].get(),
            self.quest_vars["ear"].get().lower(),
            self.quest_vars["tail"].get().lower(),
            self.quest_vars["size"].get().lower(),
            self.quest_vars["coat"].get().lower()
        )
        db.close()

        if results:
            card = tk.Frame(self.quest_results, bg=Theme.CARD,
                           highlightbackground=Theme.GLASS_BORDER,
                           highlightthickness=1)
            card.pack(fill='x')

            inner = tk.Frame(card, bg=Theme.CARD)
            inner.pack(fill='x', padx=self.s(30), pady=self.s(30))

            self.section_header(inner, "Matching Breeds", "Based on your selections").pack(anchor='w', pady=(0, self.s(15)))

            colors = [(Theme.GREEN, Theme.GREEN), (Theme.TEAL, Theme.TEAL_END), (Theme.ORANGE, Theme.ORANGE_END)]

            for i, (breed, _, prob) in enumerate(results):
                row = tk.Frame(inner, bg=Theme.CARD_LIGHT, cursor='hand2')
                row.pack(fill='x', pady=self.s(5))

                row_inner = tk.Frame(row, bg=Theme.CARD_LIGHT)
                row_inner.pack(fill='x', padx=self.s(18), pady=self.s(14))

                color = colors[i][0] if i < len(colors) else Theme.TEXT_MUTED

                badge = CircleBadge(row_inner, size=self.s(32), text=str(i+1),
                                   bg_color=color, fg_color=Theme.BG_DARK,
                                   font_size=self.s(12))
                badge.pack(side='left')

                tk.Label(row_inner, text=breed, font=self.F['body_medium'],
                        fg=Theme.WHITE, bg=Theme.CARD_LIGHT).pack(side='left', padx=(self.s(14), 0))

                tk.Label(row_inner, text=f"{prob:.0f}% match", font=self.F['sm'],
                        fg=color, bg=Theme.CARD_LIGHT).pack(side='right')

                row.bind('<Button-1>', lambda e, b=breed: self._show_breed_popup(b))
        else:
            tk.Label(self.quest_results, text="No matching breeds found",
                    font=self.F['body'], fg=Theme.TEXT_MUTED, bg=Theme.BG).pack(pady=self.s(50))

    # ═══════════════════════════════════════════════════════════════════════════
    # DICHOTOMOUS KEY PAGE
    # ═══════════════════════════════════════════════════════════════════════════

    def _build_tree(self):
        return {
            "q": "Is your dog small (under 25 lbs)?",
            "y": {
                "q": "Does your dog have floppy ears?",
                "y": {"q": "Does it have a long coat?", "y": {"r": "Shih Tzu"}, "n": {"r": "Cavalier King Charles Spaniel"}},
                "n": {"q": "Does it have a long coat?", "y": {"r": "Pomeranian"}, "n": {"r": "Chihuahua"}}
            },
            "n": {
                "q": "Is your dog giant sized (over 100 lbs)?",
                "y": {"q": "Does it have a short coat?", "y": {"r": "Great Dane"}, "n": {"r": "Saint Bernard"}},
                "n": {
                    "q": "Is your dog large (50-100 lbs)?",
                    "y": {"q": "Does it have floppy ears?", "y": {"r": "Labrador Retriever"}, "n": {"r": "German Shepherd"}},
                    "n": {"q": "Does it have a curly coat?", "y": {"r": "Poodle"}, "n": {"r": "Beagle"}}
                }
            }
        }

    def dkey_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Header
        header = tk.Frame(self.frame, bg=Theme.BG)
        header.pack(fill='x', padx=self.s(50), pady=(self.s(30), self.s(20)))

        self.back_navigation(header).pack(side='left')

        title_area = tk.Frame(header, bg=Theme.BG)
        title_area.pack(side='left', padx=(self.s(25), 0))

        tk.Label(title_area, text="Dichotomous Key", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(anchor='w')
        tk.Label(title_area, text="Answer Yes or No to identify the breed",
                font=self.F['sm'], fg=Theme.TEXT_SECONDARY, bg=Theme.BG).pack(anchor='w')

        # Content
        self.dkey_content = tk.Frame(self.frame, bg=Theme.BG)
        self.dkey_content.pack(fill='both', expand=True, padx=self.s(50), pady=(0, self.s(35)))

        self.node = self.tree
        self.qnum = 0
        self._show_dkey_question()

    def _show_dkey_question(self):
        for w in self.dkey_content.winfo_children():
            w.destroy()

        if "r" in self.node:
            self._show_dkey_result(self.node["r"])
            return

        self.qnum += 1

        # Progress indicator
        progress = tk.Frame(self.dkey_content, bg=Theme.BG)
        progress.pack(fill='x', pady=(0, self.s(25)))

        tk.Label(progress, text=f"Question {self.qnum}", font=self.F['sm'],
                fg=Theme.CYAN, bg=Theme.BG).pack(side='left')

        # Question card
        card = tk.Frame(self.dkey_content, bg=Theme.CARD,
                       highlightbackground=Theme.GLASS_BORDER,
                       highlightthickness=1)
        card.pack(fill='x')

        inner = tk.Frame(card, bg=Theme.CARD)
        inner.pack(padx=self.s(50), pady=self.s(55))

        tk.Label(inner, text=self.node["q"], font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.CARD,
                wraplength=self.s(600)).pack()

        # Buttons
        btn_frame = tk.Frame(self.dkey_content, bg=Theme.BG)
        btn_frame.pack(pady=self.s(35))

        self.gradient_button(btn_frame, "    Yes    ",
                            lambda: self._answer_dkey(True),
                            color_start=Theme.GREEN).pack(side='left', padx=self.s(12))
        self.gradient_button(btn_frame, "    No    ",
                            lambda: self._answer_dkey(False),
                            color_start=Theme.RED).pack(side='left', padx=self.s(12))

        # Restart link
        restart = tk.Label(self.dkey_content, text="Start over", font=self.F['sm'],
                          fg=Theme.TEXT_MUTED, bg=Theme.BG, cursor='hand2')
        restart.pack(pady=self.s(18))
        restart.bind('<Button-1>', lambda e: self._reset_dkey())
        restart.bind('<Enter>', lambda e: restart.config(fg=Theme.CYAN))
        restart.bind('<Leave>', lambda e: restart.config(fg=Theme.TEXT_MUTED))

    def _answer_dkey(self, yes):
        self.node = self.node["y" if yes else "n"]
        self._show_dkey_question()

    def _show_dkey_result(self, breed):
        card = tk.Frame(self.dkey_content, bg=Theme.CARD,
                       highlightbackground=Theme.CYAN,
                       highlightthickness=2)
        card.pack(fill='x')

        inner = tk.Frame(card, bg=Theme.CARD)
        inner.pack(padx=self.s(60), pady=self.s(60))

        # Success icon
        icon_size = self.s(80)
        icon_canvas = tk.Canvas(inner, width=icon_size, height=icon_size,
                               bg=Theme.CARD, highlightthickness=0)
        icon_canvas.pack()
        icon_canvas.create_oval(2, 2, icon_size-2, icon_size-2,
                               fill=Theme.GREEN, outline='')
        icon_canvas.create_text(icon_size//2, icon_size//2, text="✓",
                               fill=Theme.BG_DARK, font=('Segoe UI', self.s(36)))

        tk.Label(inner, text="Identification Complete", font=self.F['body'],
                fg=Theme.TEXT_SECONDARY, bg=Theme.CARD).pack(pady=(self.s(18), 0))

        tk.Label(inner, text=breed, font=self.F['hero'],
                fg=Theme.CYAN, bg=Theme.CARD).pack(pady=self.s(15))

        tk.Label(inner, text=f"Identified in {self.qnum} questions",
                font=self.F['xs'], fg=Theme.TEXT_MUTED, bg=Theme.CARD).pack()

        # Buttons
        btn_frame = tk.Frame(self.dkey_content, bg=Theme.BG)
        btn_frame.pack(pady=self.s(30))

        self.gradient_button(btn_frame, "View Breed Info",
                            lambda: self._show_breed_popup(breed)).pack(side='left', padx=self.s(8))
        self.ghost_button(btn_frame, "Try Again", self._reset_dkey).pack(side='left', padx=self.s(8))

    def _reset_dkey(self):
        self.node = self.tree
        self.qnum = 0
        self._show_dkey_question()

    # ═══════════════════════════════════════════════════════════════════════════
    # DATABASE PAGE
    # ═══════════════════════════════════════════════════════════════════════════

    def db_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Header
        header = tk.Frame(self.frame, bg=Theme.BG)
        header.pack(fill='x', padx=self.s(50), pady=(self.s(30), self.s(20)))

        self.back_navigation(header).pack(side='left')

        title_area = tk.Frame(header, bg=Theme.BG)
        title_area.pack(side='left', padx=(self.s(25), 0))

        count = len(BREED_INFO) if BREED_INFO else 0
        tk.Label(title_area, text="Breed Database", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(anchor='w')
        tk.Label(title_area, text=f"Explore detailed info on {count} breeds",
                font=self.F['sm'], fg=Theme.TEXT_SECONDARY, bg=Theme.BG).pack(anchor='w')

        # Search bar
        search_frame = tk.Frame(self.frame, bg=Theme.BG)
        search_frame.pack(fill='x', padx=self.s(50), pady=(0, self.s(18)))

        breeds = sorted([info['name'] for info in BREED_INFO.values()]) if BREED_INFO else []
        self.search_var = tk.StringVar()

        search_combo = ttk.Combobox(search_frame, textvariable=self.search_var,
                                   values=breeds, font=self.F['body'],
                                   style='Premium.TCombobox', width=self.s(38))
        search_combo.pack(side='left')

        self.gradient_button(search_frame, "Search",
                            lambda: self._show_db_detail(self.search_var.get()),
                            size='small').pack(side='left', padx=(self.s(15), 0))

        # Grid content with scrollable frame
        content = tk.Frame(self.frame, bg=Theme.BG)
        content.pack(fill='both', expand=True, padx=self.s(50), pady=(0, self.s(35)))

        # Canvas for scrolling without scrollbar
        canvas = tk.Canvas(content, bg=Theme.BG, highlightthickness=0)
        self.db_inner = tk.Frame(canvas, bg=Theme.BG)

        canvas.create_window((0, 0), window=self.db_inner, anchor='nw')
        canvas.pack(fill='both', expand=True)

        def configure_scroll(e):
            canvas.configure(scrollregion=canvas.bbox('all'))
            canvas.itemconfig(canvas.find_all()[0], width=canvas.winfo_width())

        self.db_inner.bind('<Configure>', configure_scroll)
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas.find_all()[0], width=e.width))

        # Mouse wheel scrolling
        def on_mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), 'units')
        canvas.bind_all('<MouseWheel>', on_mousewheel)

        self._show_db_grid()

    def _show_db_grid(self):
        for w in self.db_inner.winfo_children():
            w.destroy()

        if not BREED_INFO:
            tk.Label(self.db_inner, text="No breed data available",
                    font=self.F['body'], fg=Theme.TEXT_MUTED, bg=Theme.BG).pack(pady=self.s(50))
            return

        row_frame = None
        cols = 4

        for i, (key, info) in enumerate(sorted(BREED_INFO.items())):
            if i % cols == 0:
                row_frame = tk.Frame(self.db_inner, bg=Theme.BG)
                row_frame.pack(fill='x', pady=self.s(5))

            btn = tk.Frame(row_frame, bg=Theme.CARD, cursor='hand2',
                          highlightbackground=Theme.BORDER,
                          highlightthickness=1)
            btn.pack(side='left', fill='x', expand=True, padx=self.s(5))

            label = tk.Label(btn, text=info['name'], font=self.F['sm'],
                           fg=Theme.TEXT_PRIMARY, bg=Theme.CARD,
                           padx=self.s(12), pady=self.s(14))
            label.pack()

            def make_click(name):
                return lambda e: self._show_db_detail(name)

            btn.bind('<Button-1>', make_click(info['name']))
            label.bind('<Button-1>', make_click(info['name']))

            def make_enter(b, l):
                return lambda e: (b.config(highlightbackground=Theme.CYAN, bg=Theme.CARD_HOVER),
                                 l.config(bg=Theme.CARD_HOVER))
            def make_leave(b, l):
                return lambda e: (b.config(highlightbackground=Theme.BORDER, bg=Theme.CARD),
                                 l.config(bg=Theme.CARD))

            btn.bind('<Enter>', make_enter(btn, label))
            btn.bind('<Leave>', make_leave(btn, label))

    def _show_db_detail(self, name):
        info = get_breed_info(name)

        for w in self.db_inner.winfo_children():
            w.destroy()

        if not info:
            tk.Label(self.db_inner, text=f"No information found for '{name}'",
                    font=self.F['body'], fg=Theme.TEXT_MUTED, bg=Theme.BG).pack(pady=self.s(25))

            back = tk.Label(self.db_inner, text="← Back to all breeds",
                           font=self.F['sm'], fg=Theme.CYAN, bg=Theme.BG, cursor='hand2')
            back.pack()
            back.bind('<Button-1>', lambda e: self._show_db_grid())
            return

        # Back link
        back = tk.Label(self.db_inner, text="← Back to all breeds",
                       font=self.F['sm'], fg=Theme.CYAN, bg=Theme.BG, cursor='hand2')
        back.pack(anchor='w', pady=(0, self.s(18)))
        back.bind('<Button-1>', lambda e: self._show_db_grid())

        # Info card
        card = tk.Frame(self.db_inner, bg=Theme.CARD,
                       highlightbackground=Theme.GLASS_BORDER,
                       highlightthickness=1)
        card.pack(fill='x')

        inner = tk.Frame(card, bg=Theme.CARD)
        inner.pack(fill='x', padx=self.s(35), pady=self.s(35))

        tk.Label(inner, text=info['name'], font=self.F['h1'],
                fg=Theme.CYAN, bg=Theme.CARD).pack(anchor='w')

        subtitle = f"{info['group']}  •  {info['origin']}  •  {info['lifespan']}"
        tk.Label(inner, text=subtitle, font=self.F['sm'],
                fg=Theme.TEXT_SECONDARY, bg=Theme.CARD).pack(anchor='w', pady=(self.s(6), self.s(25)))

        details = [
            ("Size", info['size']['weight']),
            ("Temperament", ", ".join(info['temperament'][:3])),
            ("Exercise", info['exercise']),
            ("Grooming", info['grooming']),
        ]

        for label, value in details:
            row = tk.Frame(inner, bg=Theme.CARD)
            row.pack(fill='x', pady=self.s(5))

            tk.Label(row, text=label, font=self.F['sm'], fg=Theme.TEXT_MUTED,
                    bg=Theme.CARD, width=16, anchor='w').pack(side='left')
            tk.Label(row, text=value, font=self.F['sm'], fg=Theme.TEXT_PRIMARY,
                    bg=Theme.CARD).pack(side='left')

    # ═══════════════════════════════════════════════════════════════════════════
    # BREED POPUP
    # ═══════════════════════════════════════════════════════════════════════════

    def _show_breed_popup(self, name):
        info = get_breed_info(name)
        if not info:
            messagebox.showinfo("Info", f"No detailed information for {name}")
            return

        popup = tk.Toplevel(self.root)
        popup.title(info['name'])

        pw, ph = min(self.s(520), self.w - 100), min(self.s(580), self.h - 100)
        px = self.root.winfo_x() + (self.w - pw) // 2
        py = self.root.winfo_y() + (self.h - ph) // 2
        popup.geometry(f"{pw}x{ph}+{px}+{py}")
        popup.configure(bg=Theme.BG)
        popup.transient(self.root)
        popup.grab_set()

        # Content
        content = tk.Frame(popup, bg=Theme.BG)
        content.pack(fill='both', expand=True, padx=self.s(30), pady=self.s(30))

        # Header
        tk.Label(content, text=info['name'], font=self.F['h1'],
                fg=Theme.CYAN, bg=Theme.BG).pack(anchor='w')

        subtitle = f"{info['group']}  •  {info['origin']}"
        tk.Label(content, text=subtitle, font=self.F['sm'],
                fg=Theme.TEXT_SECONDARY, bg=Theme.BG).pack(anchor='w', pady=(self.s(6), self.s(22)))

        # Details
        details = [
            ("Size", f"{info['size']['weight']}, {info['size']['height']}"),
            ("Lifespan", info['lifespan']),
            ("Temperament", ", ".join(info['temperament'])),
            ("Exercise", info['exercise']),
            ("Grooming", info['grooming']),
            ("Trainability", info['trainability']),
        ]

        for label, value in details:
            row = tk.Frame(content, bg=Theme.BG)
            row.pack(fill='x', pady=self.s(6))

            tk.Label(row, text=label, font=self.F['sm'], fg=Theme.CYAN,
                    bg=Theme.BG, width=14, anchor='w').pack(side='left')
            tk.Label(row, text=value, font=self.F['sm'], fg=Theme.TEXT_PRIMARY,
                    bg=Theme.BG, wraplength=self.s(320)).pack(side='left', fill='x')

        # Fun fact card
        fact_card = tk.Frame(content, bg=Theme.CARD)
        fact_card.pack(fill='x', pady=self.s(22))

        fact_inner = tk.Frame(fact_card, bg=Theme.CARD)
        fact_inner.pack(fill='x', padx=self.s(18), pady=self.s(18))

        tk.Label(fact_inner, text="Fun Fact", font=self.F['sm'],
                fg=Theme.ORANGE, bg=Theme.CARD).pack(anchor='w')
        tk.Label(fact_inner, text=info['fun_fact'], font=self.F['xs'],
                fg=Theme.TEXT_PRIMARY, bg=Theme.CARD,
                wraplength=self.s(420), justify='left').pack(anchor='w', pady=(self.s(6), 0))

        # Buttons
        btn_frame = tk.Frame(content, bg=Theme.BG)
        btn_frame.pack(pady=self.s(18))

        search_url = f"https://www.google.com/search?tbm=isch&q={info['name'].replace(' ', '+')}+dog"

        self.gradient_button(btn_frame, "View Images",
                            lambda: webbrowser.open(search_url),
                            color_start=Theme.PINK).pack(side='left', padx=self.s(6))
        self.ghost_button(btn_frame, "Close", popup.destroy).pack(side='left', padx=self.s(6))


# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════════════════════════════════════════

class Database:
    """SQLite database handler."""

    def __init__(self):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dog_database.db')
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def query(self, color, ear, tail, size, coat):
        try:
            self.cursor.execute("""
                SELECT DogBreeds.BreedName,
                       SUM(CASE WHEN DogColors.ColorName = ? THEN 1 ELSE 0 END +
                           CASE WHEN DogBreeds.CoatType = ? THEN 1 ELSE 0 END +
                           CASE WHEN DogBreeds.EarType = ? THEN 1 ELSE 0 END +
                           CASE WHEN DogBreeds.TailType = ? THEN 1 ELSE 0 END +
                           CASE WHEN DogBreeds.Size = ? THEN 1 ELSE 0 END) AS Match,
                       ROUND((SUM(CASE WHEN DogColors.ColorName = ? THEN 1 ELSE 0 END +
                                  CASE WHEN DogBreeds.CoatType = ? THEN 1 ELSE 0 END +
                                  CASE WHEN DogBreeds.EarType = ? THEN 1 ELSE 0 END +
                                  CASE WHEN DogBreeds.TailType = ? THEN 1 ELSE 0 END +
                                  CASE WHEN DogBreeds.Size = ? THEN 1 ELSE 0 END) / 5.0) * 100, 2) AS Prob
                FROM DogBreeds
                LEFT JOIN BreedColors ON DogBreeds.BreedID = BreedColors.BreedID
                LEFT JOIN DogColors ON BreedColors.ColorID = DogColors.ColorID
                WHERE DogColors.ColorName = ? OR DogColors.ColorName IS NULL
                GROUP BY DogBreeds.BreedName ORDER BY Match DESC LIMIT 3
            """, (color, coat, ear, tail, size, color, coat, ear, tail, size, color))
            return self.cursor.fetchall()
        except Exception:
            return []

    def close(self):
        self.cursor.close()
        self.conn.close()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
