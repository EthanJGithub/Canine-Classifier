#!/usr/bin/env python3
"""
Canine Classifier - Ultimate 2025 Premium UI
The most beautiful dog breed identification interface ever created.
Features: Animated gradients, particle effects, smooth transitions, glass morphism,
pulsing glows, animated spinners, gradient buttons, and premium micro-interactions.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
import threading
import webbrowser
import time
import math
import random
import colorsys
import datetime

try:
    from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    from breed_info import BREED_INFO, get_breed_info
except ImportError:
    BREED_INFO = {}
    def get_breed_info(breed): return None

# PDF generation
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import black, gray, white, HexColor
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


class Theme:
    """Ultimate 2025 Premium Theme - Cosmic elegance with aurora accents."""

    # Deep space backgrounds with purple undertones
    BG_DARK = "#030308"
    BG = "#06060c"
    BG2 = "#0a0a14"
    BG3 = "#0e0e1a"
    BG4 = "#121220"

    # Premium card surfaces
    CARD = "#0f0f1a"
    CARD2 = "#141422"
    CARD_HOVER = "#1a1a2e"
    CARD_ACTIVE = "#1e1e38"
    CARD_GLOW = "#252545"

    # Glass morphism with depth
    GLASS = "#12122480"
    GLASS_LIGHT = "#1e1e3060"
    GLASS_BORDER = "#2828fifty"
    GLASS_BORDER_LIGHT = "#3a3a65"
    GLASS_GLOW = "#4040708"

    # Gradient accent colors - Aurora palette
    AURORA_1 = "#00f5d4"  # Cyan
    AURORA_2 = "#00bbf9"  # Blue
    AURORA_3 = "#9b5de5"  # Purple
    AURORA_4 = "#f15bb5"  # Pink
    AURORA_5 = "#fee440"  # Yellow

    # Primary gradient endpoints
    PRIMARY = "#00f5d4"
    PRIMARY_LIGHT = "#00ffde"
    PRIMARY_DARK = "#00d4b8"
    PRIMARY_GLOW = "#00ffd0"

    # Secondary accents - Vibrant neons
    CYAN = "#00e5ff"
    TEAL = "#00d4aa"
    BLUE = "#4d9fff"
    INDIGO = "#6366f1"
    PURPLE = "#a855f7"
    VIOLET = "#c084fc"
    MAGENTA = "#e879f9"
    PINK = "#f472b6"
    ROSE = "#fb7185"
    CORAL = "#ff7f7f"
    ORANGE = "#ff9f43"
    AMBER = "#ffc107"
    GOLD = "#ffd700"
    LIME = "#84cc16"
    GREEN = "#22c55e"
    EMERALD = "#10b981"
    RED = "#ff4757"
    CRIMSON = "#dc2626"

    # Text with perfect contrast
    WHITE = "#ffffff"
    TEXT = "#f8f8fc"
    TEXT2 = "#c8c8e0"
    TEXT3 = "#9898b8"
    MUTED = "#6868a8"
    SUBTLE = "#484878"
    DIM = "#383860"

    # Status colors with glow
    SUCCESS = "#00ff88"
    SUCCESS_GLOW = "#00ff8840"
    WARNING = "#ffcc00"
    WARNING_GLOW = "#ffcc0040"
    ERROR = "#ff4466"
    ERROR_GLOW = "#ff446640"
    INFO = "#00ccff"
    INFO_GLOW = "#00ccff40"

    # Scrollbar
    SCROLL_BG = "#08080f"
    SCROLL_THUMB = "#28284a"
    SCROLL_THUMB_HOVER = "#3a3a68"
    SCROLL_THUMB_ACTIVE = "#4a4a88"

    # Border colors
    BORDER = "#2a2a4a"
    BORDER_LIGHT = "#3a3a5a"
    BORDER_FOCUS = "#00f5d4"

    # Gradient presets for buttons
    GRAD_PRIMARY = ["#00f5d4", "#00bbf9"]
    GRAD_SECONDARY = ["#9b5de5", "#f15bb5"]
    GRAD_SUCCESS = ["#00ff88", "#00d4aa"]
    GRAD_DANGER = ["#ff4466", "#ff6b9d"]
    GRAD_GOLD = ["#ffd700", "#ff9f43"]


class ParticleSystem:
    """Animated particle background for premium feel."""

    def __init__(self, canvas, count=50):
        self.canvas = canvas
        self.particles = []
        self.running = False

        for _ in range(count):
            self.particles.append({
                'x': random.randint(0, 2000),
                'y': random.randint(0, 1200),
                'vx': random.uniform(-0.3, 0.3),
                'vy': random.uniform(-0.2, 0.2),
                'size': random.uniform(1, 3),
                'alpha': random.uniform(0.1, 0.4),
                'color': random.choice([Theme.AURORA_1, Theme.AURORA_2, Theme.AURORA_3, Theme.AURORA_4]),
                'id': None
            })

    def start(self):
        self.running = True
        self._animate()

    def stop(self):
        self.running = False

    def _animate(self):
        if not self.running:
            return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        for p in self.particles:
            # Update position
            p['x'] += p['vx']
            p['y'] += p['vy']

            # Wrap around
            if p['x'] < 0: p['x'] = w
            if p['x'] > w: p['x'] = 0
            if p['y'] < 0: p['y'] = h
            if p['y'] > h: p['y'] = 0

            # Remove old and create new
            if p['id']:
                self.canvas.delete(p['id'])

            # Create glowing particle
            size = int(p['size'])
            p['id'] = self.canvas.create_oval(
                p['x'] - size, p['y'] - size,
                p['x'] + size, p['y'] + size,
                fill=p['color'], outline='', tags='particle'
            )

        self.canvas.after(50, self._animate)


class AnimatedGradient:
    """Smooth animated gradient background."""

    def __init__(self, canvas):
        self.canvas = canvas
        self.phase = 0
        self.running = False

    def start(self):
        self.running = True
        self._animate()

    def stop(self):
        self.running = False

    def _animate(self):
        if not self.running:
            return

        self.phase += 0.02
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        if w > 1 and h > 1:
            # Create subtle moving gradient effect
            self.canvas.delete('gradient')

            # Draw gradient bands
            bands = 20
            for i in range(bands):
                y1 = i * h // bands
                y2 = (i + 1) * h // bands

                # Oscillating color
                hue = (0.55 + math.sin(self.phase + i * 0.1) * 0.05) % 1.0
                r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.08 + i * 0.002)
                color = f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

                self.canvas.create_rectangle(
                    0, y1, w, y2,
                    fill=color, outline='', tags='gradient'
                )

            self.canvas.tag_lower('gradient')

        self.canvas.after(60, self._animate)


class PulsingGlow:
    """Creates a pulsing glow effect around widgets."""

    def __init__(self, widget, color, intensity=1.0):
        self.widget = widget
        self.base_color = color
        self.intensity = intensity
        self.phase = 0
        self.running = False

    def start(self):
        self.running = True
        self._pulse()

    def stop(self):
        self.running = False

    def _pulse(self):
        if not self.running:
            return

        self.phase += 0.1
        glow = 0.5 + 0.5 * math.sin(self.phase)

        # Interpolate border color
        try:
            if hasattr(self.widget, 'set_glow_intensity'):
                self.widget.set_glow_intensity(glow * self.intensity)
        except:
            pass

        self.widget.after(50, self._pulse)


class AnimatedSpinner(tk.Canvas):
    """Beautiful animated loading spinner with gradient."""

    def __init__(self, parent, size=60, **kwargs):
        super().__init__(parent, **kwargs)

        self.size = size
        self.configure(
            width=size, height=size,
            bg=Theme.CARD, highlightthickness=0
        )

        self.angle = 0
        self.running = False
        self.colors = [Theme.AURORA_1, Theme.AURORA_2, Theme.AURORA_3, Theme.AURORA_4]

    def start(self):
        self.running = True
        self._animate()

    def stop(self):
        self.running = False
        self.delete('all')

    def _animate(self):
        if not self.running:
            return

        self.delete('all')
        cx, cy = self.size // 2, self.size // 2
        r = self.size // 2 - 8

        # Draw arc segments with gradient colors
        segments = 12
        for i in range(segments):
            start_angle = self.angle + i * (360 / segments)
            extent = 360 / segments - 5

            # Fade effect
            alpha = (i / segments)
            color_idx = int(i / segments * len(self.colors)) % len(self.colors)
            color = self.colors[color_idx]

            self.create_arc(
                cx - r, cy - r, cx + r, cy + r,
                start=start_angle, extent=extent,
                style='arc', outline=color, width=3
            )

        # Center dot
        dot_r = 4
        self.create_oval(
            cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r,
            fill=Theme.PRIMARY, outline=''
        )

        self.angle = (self.angle + 8) % 360
        self.after(30, self._animate)


class GradientButton(tk.Frame):
    """Clean, simple button with solid colors - no artifacts."""

    def __init__(self, parent, text="", command=None, colors=None, icon="", width=None, height=48, **kwargs):
        # Get parent background
        try:
            parent_bg = parent.cget('bg')
        except:
            parent_bg = Theme.BG

        super().__init__(parent, bg=parent_bg, **kwargs)

        self.text = text
        self.icon = icon
        self.command = command
        self.colors = colors or Theme.GRAD_PRIMARY
        self._height = height
        self._width = width or 180

        self._hovering = False
        self._pressed = False

        # Main button frame with rounded corners simulation using padding
        self.btn_frame = tk.Frame(self, bg=self.colors[0], cursor="hand2")
        self.btn_frame.pack(padx=2, pady=2)

        # Inner content
        display = f"{icon}  {text}" if icon else text

        # Determine text color based on button color
        main_color = self.colors[0]
        bright_colors = [Theme.PRIMARY, Theme.AURORA_1, Theme.SUCCESS, Theme.WARNING,
                        Theme.GOLD, Theme.LIME, Theme.CYAN, Theme.TEAL, Theme.EMERALD,
                        '#00f5d4', '#00d4aa', '#00ff88', '#ffd700', '#00e5ff']
        fg = Theme.BG_DARK if main_color in bright_colors else Theme.WHITE

        self.label = tk.Label(
            self.btn_frame,
            text=display,
            font=("Segoe UI Semibold", 11),
            fg=fg,
            bg=self.colors[0],
            cursor="hand2",
            padx=self._width // 6 if self._width else 30,
            pady=(self._height - 24) // 2 if self._height else 12
        )
        self.label.pack()

        # Bind events to all widgets
        for widget in [self, self.btn_frame, self.label]:
            widget.bind('<Enter>', self._on_enter)
            widget.bind('<Leave>', self._on_leave)
            widget.bind('<Button-1>', self._on_press)
            widget.bind('<ButtonRelease-1>', self._on_release)

    def _update_colors(self):
        """Update button colors based on state."""
        if self._pressed:
            color = self._darken_color(self.colors[0], 0.7)
        elif self._hovering:
            color = self.colors[1] if len(self.colors) > 1 else self._lighten_color(self.colors[0], 1.1)
        else:
            color = self.colors[0]

        self.btn_frame.config(bg=color)
        self.label.config(bg=color)

    def _darken_color(self, hex_color, factor):
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r, g, b = max(0, int(r * factor)), max(0, int(g * factor)), max(0, int(b * factor))
        return f'#{r:02x}{g:02x}{b:02x}'

    def _lighten_color(self, hex_color, factor):
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r, g, b = min(255, int(r * factor)), min(255, int(g * factor)), min(255, int(b * factor))
        return f'#{r:02x}{g:02x}{b:02x}'

    def _on_enter(self, event):
        self._hovering = True
        self._update_colors()

    def _on_leave(self, event):
        self._hovering = False
        self._pressed = False
        self._update_colors()

    def _on_press(self, event):
        self._pressed = True
        self._update_colors()

    def _on_release(self, event):
        was_pressed = self._pressed
        self._pressed = False
        self._update_colors()
        if was_pressed and self._hovering and self.command:
            self.command()


class GlassCard(tk.Frame):
    """Simple card with solid background - no Canvas artifacts."""

    def __init__(self, parent, glow_color=None, animated=False, **kwargs):
        # Remove Canvas-specific kwargs
        kwargs.pop('highlightthickness', None)

        super().__init__(parent, bg=Theme.CARD, **kwargs)

        self.glow_color = glow_color or Theme.BORDER
        self._content_frame = None

        # Add a subtle border effect using nested frames
        self.configure(highlightbackground=self.glow_color, highlightthickness=1)

    def get_content_frame(self):
        """Get the content frame for adding widgets."""
        if not self._content_frame:
            self._content_frame = tk.Frame(self, bg=Theme.CARD)
            self._content_frame.pack(fill='both', expand=True, padx=4, pady=4)
        return self._content_frame

    def set_glow(self, color):
        self.glow_color = color
        self.configure(highlightbackground=color)


class ModernScrollbar(tk.Frame):
    """Simple scrollbar using ttk for reliability."""

    def __init__(self, parent, command=None, **kwargs):
        super().__init__(parent, bg=Theme.BG, **kwargs)

        self.command = command

        # Use ttk scrollbar with dark styling
        style = ttk.Style()
        style.configure("Dark.Vertical.TScrollbar",
                       background=Theme.SCROLL_THUMB,
                       troughcolor=Theme.BG,
                       borderwidth=0,
                       arrowsize=0)

        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=command,
                                        style="Dark.Vertical.TScrollbar")
        self.scrollbar.pack(fill='y', expand=True)

    def set(self, first, last):
        self.scrollbar.set(first, last)


class ModernDropdown(tk.Frame):
    """Premium styled dropdown with modern appearance."""

    def __init__(self, parent, values=None, textvariable=None, width=200, **kwargs):
        super().__init__(parent, bg=Theme.CARD, **kwargs)

        self.values = values or []
        self.var = textvariable or tk.StringVar()
        self._is_open = False
        self._dropdown_window = None
        self._selected_idx = 0
        self.width = width

        # Main button container
        self.btn_frame = tk.Frame(self, bg=Theme.BG4, highlightbackground=Theme.BORDER,
                                  highlightthickness=1, highlightcolor=Theme.CYAN)
        self.btn_frame.pack(fill='x')

        # Inner padding frame
        self.inner = tk.Frame(self.btn_frame, bg=Theme.BG4)
        self.inner.pack(fill='x', padx=14, pady=10)

        # Selected text
        self.label = tk.Label(self.inner, textvariable=self.var, font=('Segoe UI', 11),
                             fg=Theme.WHITE, bg=Theme.BG4, anchor='w')
        self.label.pack(side='left', fill='x', expand=True)

        # Arrow icon
        self.arrow = tk.Label(self.inner, text="▼", font=('Segoe UI', 8),
                             fg=Theme.CYAN, bg=Theme.BG4)
        self.arrow.pack(side='right', padx=(8, 0))

        # Bind events
        for widget in [self.btn_frame, self.inner, self.label, self.arrow]:
            widget.bind('<Button-1>', self._toggle)
            widget.bind('<Enter>', self._on_enter)
            widget.bind('<Leave>', self._on_leave)
            widget.configure(cursor='hand2')

        # Set initial value
        if self.values and not self.var.get():
            self.var.set(self.values[0])

    def _on_enter(self, event=None):
        self.btn_frame.configure(highlightbackground=Theme.CYAN)
        self.inner.configure(bg=Theme.BG3)
        self.label.configure(bg=Theme.BG3)
        self.arrow.configure(bg=Theme.BG3, fg=Theme.PRIMARY)

    def _on_leave(self, event=None):
        if not self._is_open:
            self.btn_frame.configure(highlightbackground=Theme.BORDER)
            self.inner.configure(bg=Theme.BG4)
            self.label.configure(bg=Theme.BG4)
            self.arrow.configure(bg=Theme.BG4, fg=Theme.CYAN)

    def _toggle(self, event=None):
        if self._is_open:
            self._close()
        else:
            self._open()

    def _open(self):
        if self._dropdown_window:
            self._close()
            return

        self._is_open = True
        self.arrow.configure(text="▲")

        # Create dropdown window
        self._dropdown_window = tk.Toplevel(self)
        self._dropdown_window.wm_overrideredirect(True)
        self._dropdown_window.configure(bg=Theme.BORDER)

        # Position below the button
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self._dropdown_window.geometry(f"+{x}+{y}")

        # Inner frame
        inner_frame = tk.Frame(self._dropdown_window, bg=Theme.BG3)
        inner_frame.pack(fill='both', expand=True, padx=1, pady=1)

        # Create scrollable list if many items
        if len(self.values) > 8:
            canvas = tk.Canvas(inner_frame, bg=Theme.BG3, highlightthickness=0,
                              width=self.width, height=280)
            scrollbar = tk.Scrollbar(inner_frame, orient='vertical', command=canvas.yview)
            list_frame = tk.Frame(canvas, bg=Theme.BG3)

            canvas.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side='right', fill='y')
            canvas.pack(side='left', fill='both', expand=True)
            canvas.create_window((0, 0), window=list_frame, anchor='nw')

            list_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
            canvas.bind('<Enter>', lambda e: canvas.bind_all('<MouseWheel>',
                       lambda ev: canvas.yview_scroll(int(-1*(ev.delta/120)), 'units')))
            canvas.bind('<Leave>', lambda e: canvas.unbind_all('<MouseWheel>'))
        else:
            list_frame = inner_frame

        # Populate items
        for i, value in enumerate(self.values):
            is_placeholder = value.startswith('--')
            item = tk.Frame(list_frame, bg=Theme.BG3, cursor='hand2')
            item.pack(fill='x')

            item_label = tk.Label(item, text=value, font=('Segoe UI', 11),
                                 fg=Theme.DIM if is_placeholder else Theme.WHITE,
                                 bg=Theme.BG3, anchor='w', padx=14, pady=8)
            item_label.pack(fill='x')

            if not is_placeholder:
                item.bind('<Enter>', lambda e, f=item, l=item_label: self._item_hover(f, l, True))
                item.bind('<Leave>', lambda e, f=item, l=item_label: self._item_hover(f, l, False))
                item.bind('<Button-1>', lambda e, v=value: self._select(v))
                item_label.bind('<Button-1>', lambda e, v=value: self._select(v))

        # Handle clicks outside
        self._dropdown_window.bind('<FocusOut>', lambda e: self.after(100, self._close))
        self.winfo_toplevel().bind('<Button-1>', self._check_click_outside, '+')

    def _item_hover(self, frame, label, entering):
        if entering:
            frame.configure(bg=Theme.PRIMARY)
            label.configure(bg=Theme.PRIMARY, fg=Theme.BG_DARK)
        else:
            frame.configure(bg=Theme.BG3)
            label.configure(bg=Theme.BG3, fg=Theme.WHITE)

    def _select(self, value):
        self.var.set(value)
        self._close()

    def _check_click_outside(self, event):
        if self._dropdown_window:
            # Check if click is outside dropdown
            try:
                # event.widget might be a string if widget was destroyed
                if isinstance(event.widget, str):
                    self._close()
                    return
                widget = event.widget.winfo_toplevel()
                if widget != self._dropdown_window:
                    self._close()
            except:
                self._close()

    def _close(self):
        self._is_open = False
        try:
            if self.arrow.winfo_exists():
                self.arrow.configure(text="▼")
            self._on_leave()
        except:
            pass
        if self._dropdown_window:
            try:
                self._dropdown_window.destroy()
            except:
                pass
            self._dropdown_window = None
        try:
            self.winfo_toplevel().unbind('<Button-1>')
        except:
            pass

    def get(self):
        return self.var.get()

    def set(self, value):
        self.var.set(value)


class ProgressRing(tk.Canvas):
    """Animated circular progress indicator."""

    def __init__(self, parent, size=120, thickness=8, **kwargs):
        super().__init__(parent, **kwargs)

        self.size = size
        self.thickness = thickness
        self._progress = 0
        self._target_progress = 0

        self.configure(
            width=size, height=size,
            bg=Theme.CARD, highlightthickness=0
        )

        self._animate()

    def set_progress(self, value):
        self._target_progress = max(0, min(100, value))

    def _animate(self):
        # Smooth animation to target
        diff = self._target_progress - self._progress
        if abs(diff) > 0.5:
            self._progress += diff * 0.1
            self._draw()

        self.after(20, self._animate)

    def _draw(self):
        self.delete('all')

        cx, cy = self.size // 2, self.size // 2
        r = self.size // 2 - self.thickness - 4

        # Background ring
        self.create_arc(
            cx - r, cy - r, cx + r, cy + r,
            start=90, extent=-360,
            style='arc', outline=Theme.BG3, width=self.thickness
        )

        # Progress arc with gradient effect
        extent = -360 * (self._progress / 100)
        if abs(extent) > 1:
            # Draw multiple arcs for gradient effect
            segments = max(1, int(abs(extent) / 10))
            for i in range(segments):
                seg_start = 90 - (i * extent / segments)
                seg_extent = extent / segments

                # Color gradient
                t = i / segments
                color = self._interpolate_color(Theme.AURORA_1, Theme.AURORA_3, t)

                self.create_arc(
                    cx - r, cy - r, cx + r, cy + r,
                    start=seg_start, extent=seg_extent,
                    style='arc', outline=color, width=self.thickness
                )

        # Center text
        self.create_text(
            cx, cy,
            text=f"{int(self._progress)}%",
            fill=Theme.TEXT,
            font=("Segoe UI Semibold", int(self.size / 5))
        )

    def _interpolate_color(self, c1, c2, t):
        c1 = c1.lstrip('#')
        c2 = c2.lstrip('#')
        r1, g1, b1 = int(c1[:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)
        r2, g2, b2 = int(c2[:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return f'#{r:02x}{g:02x}{b:02x}'


class App:
    """Ultimate 2025 Premium Canine Classifier Application."""

    def __init__(self, root):
        self.root = root
        self.root.title("Canine Classifier")

        # DPI awareness
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(2)
        except:
            pass

        # Screen detection and responsive sizing
        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()

        # Optimal window size (90% of screen)
        self.w = min(int(self.screen_w * 0.9), 1600)
        self.h = min(int(self.screen_h * 0.9), 960)

        # Responsive scale
        self.scale = min(self.w / 1400, self.h / 900)

        # Center window
        x = (self.screen_w - self.w) // 2
        y = (self.screen_h - self.h) // 2

        root.geometry(f"{self.w}x{self.h}+{x}+{y}")
        root.configure(bg=Theme.BG_DARK)
        root.minsize(1100, 700)

        # Premium fonts
        base = max(int(12 * self.scale), 10)
        self.F = {
            'display': ('Segoe UI Light', int(base * 3.2)),
            'hero': ('Segoe UI Light', int(base * 2.8)),
            'hero_bold': ('Segoe UI Semibold', int(base * 2.8)),
            'h1': ('Segoe UI Semibold', int(base * 2)),
            'h2': ('Segoe UI Semibold', int(base * 1.5)),
            'h3': ('Segoe UI Semibold', int(base * 1.2)),
            'body': ('Segoe UI', base),
            'body_bold': ('Segoe UI Semibold', base),
            'sm': ('Segoe UI', int(base * 0.92)),
            'xs': ('Segoe UI', int(base * 0.83)),
            'xxs': ('Segoe UI', int(base * 0.75)),
            'mono': ('Cascadia Code', int(base * 0.9)),
        }

        # State
        self.frame = None
        self.classifier = None
        self.tree = self._build_tree()
        self.node = None
        self.qnum = 0

        # Active animations
        self.animations = []

        self._setup_styles()
        self.home()

    def _setup_styles(self):
        """Configure premium ttk styles with modern appearance."""
        style = ttk.Style()
        style.theme_use('clam')

        # Modern Combobox styling
        style.configure('Modern.TCombobox',
            fieldbackground=Theme.BG4,
            background=Theme.CARD,
            foreground=Theme.WHITE,
            arrowcolor=Theme.CYAN,
            borderwidth=2,
            padding=(16, 12),
            relief='flat',
            arrowsize=18
        )
        style.map('Modern.TCombobox',
            fieldbackground=[
                ('readonly', Theme.BG4),
                ('readonly', 'focus', Theme.BG3),
                ('readonly', 'hover', Theme.BG3)
            ],
            background=[
                ('readonly', Theme.CARD),
                ('readonly', 'focus', Theme.CARD_HOVER)
            ],
            foreground=[
                ('readonly', Theme.WHITE),
                ('disabled', Theme.DIM)
            ],
            arrowcolor=[
                ('readonly', Theme.CYAN),
                ('readonly', 'focus', Theme.PRIMARY),
                ('readonly', 'hover', Theme.PRIMARY)
            ],
            bordercolor=[
                ('readonly', Theme.BORDER),
                ('readonly', 'focus', Theme.CYAN),
                ('readonly', 'hover', Theme.PRIMARY)
            ]
        )

        # Style the dropdown listbox
        self.root.option_add('*TCombobox*Listbox.background', Theme.BG3)
        self.root.option_add('*TCombobox*Listbox.foreground', Theme.WHITE)
        self.root.option_add('*TCombobox*Listbox.selectBackground', Theme.PRIMARY)
        self.root.option_add('*TCombobox*Listbox.selectForeground', Theme.BG_DARK)
        self.root.option_add('*TCombobox*Listbox.font', ('Segoe UI', 11))

    def s(self, val):
        """Scale value for responsiveness."""
        return max(int(val * self.scale), 1)

    def clear(self):
        """Clear current frame and stop animations."""
        for anim in self.animations:
            try:
                anim.stop()
            except:
                pass
        self.animations = []

        if self.frame:
            self.frame.destroy()

    # ══════════════════════════════════════════════════════════════════════════
    # PREMIUM UI COMPONENTS
    # ══════════════════════════════════════════════════════════════════════════

    def gradient_btn(self, parent, text, cmd, colors=None, icon="", width=None, height=None):
        """Create premium gradient button."""
        h = height or self.s(48)
        btn = GradientButton(parent, text=text, command=cmd, colors=colors or Theme.GRAD_PRIMARY, icon=icon, width=width, height=h)
        return btn

    def glass_card(self, parent, glow=None, animated=False):
        """Create premium glass card."""
        return GlassCard(parent, glow_color=glow, animated=animated)

    def back_nav(self, parent):
        """Premium back navigation with hover effects."""
        frame = tk.Frame(parent, bg=Theme.BG, cursor="hand2")

        # Animated arrow
        arrow = tk.Label(frame, text="←", font=("Segoe UI Light", self.s(22)),
                        fg=Theme.MUTED, bg=Theme.BG, cursor="hand2")
        arrow.pack(side='left')

        label = tk.Label(frame, text="Back", font=self.F['body'],
                        fg=Theme.MUTED, bg=Theme.BG, cursor="hand2",
                        padx=self.s(8))
        label.pack(side='left')

        def enter(e):
            arrow.config(fg=Theme.PRIMARY)
            label.config(fg=Theme.PRIMARY)

        def leave(e):
            arrow.config(fg=Theme.MUTED)
            label.config(fg=Theme.MUTED)

        for w in [frame, arrow, label]:
            w.bind('<Enter>', enter)
            w.bind('<Leave>', leave)
            w.bind('<Button-1>', lambda e: self.home())

        return frame

    def scrollable(self, parent):
        """Create premium scrollable container with smooth scrolling."""
        container = tk.Frame(parent, bg=Theme.BG)
        canvas = tk.Canvas(container, bg=Theme.BG, highlightthickness=0)
        scrollbar = ModernScrollbar(container, command=canvas.yview)

        inner = tk.Frame(canvas, bg=Theme.BG)
        window = canvas.create_window((0, 0), window=inner, anchor='nw')

        def on_configure(e):
            canvas.configure(scrollregion=canvas.bbox('all'))
            canvas.itemconfig(window, width=canvas.winfo_width())

        inner.bind('<Configure>', on_configure)
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(window, width=e.width))

        # Smoother scrolling - increased scroll amount for faster navigation
        def on_wheel(e):
            # Scroll 3 units at a time for smoother feel
            canvas.yview_scroll(int(-1 * (e.delta / 40)), 'units')

        # Bind mousewheel to the canvas and all its children
        def bind_wheel(widget):
            widget.bind('<MouseWheel>', on_wheel)
            widget.bind('<Enter>', lambda e: canvas.bind_all('<MouseWheel>', on_wheel))
            widget.bind('<Leave>', lambda e: canvas.unbind_all('<MouseWheel>'))

        bind_wheel(canvas)
        bind_wheel(inner)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y', padx=(self.s(6), 0))

        canvas.configure(yscrollcommand=scrollbar.set)

        # Store reference for child binding
        inner._scroll_canvas = canvas
        inner._on_wheel = on_wheel

        return container, inner

    def spinner(self, parent, size=None):
        """Create animated loading spinner."""
        return AnimatedSpinner(parent, size=size or self.s(60))

    # ══════════════════════════════════════════════════════════════════════════
    # HOME PAGE - PREMIUM EXPERIENCE
    # ══════════════════════════════════════════════════════════════════════════

    def home(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Compact header
        header = tk.Frame(self.frame, bg=Theme.BG)
        header.pack(fill='x', padx=self.s(40), pady=(self.s(25), self.s(15)))

        # Title row
        title_row = tk.Frame(header, bg=Theme.BG)
        title_row.pack(fill='x')

        tk.Label(title_row, text="🐕 Canine Classifier", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(side='left')

        tk.Label(title_row, text=f"{len(BREED_INFO)} Breeds • AI Powered",
                font=self.F['sm'], fg=Theme.MUTED, bg=Theme.BG).pack(side='right', pady=(self.s(8), 0))

        # Cards grid - directly in frame, no canvas needed for simpler layout
        grid = tk.Frame(self.frame, bg=Theme.BG)
        grid.pack(fill='both', expand=True, padx=self.s(40), pady=(self.s(10), self.s(20)))

        # Configure 2 columns
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)

        # Card data
        cards = [
            ("AI Recognition", "Upload a photo for instant breed detection",
             Theme.CYAN, "🤖", self.ai_page),
            ("Questionnaire", "Answer questions about your dog's features",
             Theme.MAGENTA, "📋", self.quest_page),
            ("Dichotomous Key", "Yes/No identification method",
             Theme.BLUE, "🔬", self.dkey_page),
            ("Breed Database", f"Explore {len(BREED_INFO)} breeds",
             Theme.GOLD, "📚", self.db_page),
            ("Mixed Breed Detection", "AI breed composition analysis",
             Theme.EMERALD, "🧬", self.mixed_breed_page),
            ("Health Risk Score", "Breed-based health assessment",
             Theme.CORAL, "🏥", self.health_risk_page),
            ("Intake Forms", "Auto-generate professional forms",
             Theme.INDIGO, "📄", self.intake_form_page),
        ]

        for i, (title, desc, accent, icon, cmd) in enumerate(cards):
            row, col = divmod(i, 2)
            self._simple_card(grid, title, desc, accent, icon, cmd, row, col)

    def _simple_card(self, parent, title, desc, accent, icon, cmd, row, col):
        """Create premium, polished card with subtle depth and glow effects."""
        # Outer glow frame for depth
        outer = tk.Frame(parent, bg=Theme.BG)
        outer.grid(row=row, column=col, padx=self.s(10), pady=self.s(10), sticky='nsew')

        # Card frame with refined border
        card = tk.Frame(outer, bg=Theme.CARD, highlightbackground=Theme.BORDER_LIGHT,
                       highlightthickness=1, cursor="hand2")
        card.pack(fill='both', expand=True)

        # Inner padding with generous spacing
        inner = tk.Frame(card, bg=Theme.CARD, cursor="hand2")
        inner.pack(fill='both', expand=True, padx=self.s(24), pady=self.s(22))

        # Top row: Icon with accent background
        top = tk.Frame(inner, bg=Theme.CARD)
        top.pack(fill='x', pady=(0, self.s(14)))

        # Icon container with accent background
        icon_bg = tk.Frame(top, bg=accent, width=self.s(48), height=self.s(48))
        icon_bg.pack(side='left', padx=(0, self.s(14)))
        icon_bg.pack_propagate(False)

        # Center the icon
        tk.Label(icon_bg, text=icon, font=("Segoe UI Emoji", self.s(20)),
                bg=accent, fg=Theme.BG_DARK).place(relx=0.5, rely=0.5, anchor='center')

        # Title with accent color
        title_label = tk.Label(inner, text=title, font=self.F['h3'],
                fg=Theme.WHITE, bg=Theme.CARD, anchor='w')
        title_label.pack(fill='x', pady=(0, self.s(8)))

        # Description with better readability
        desc_label = tk.Label(inner, text=desc, font=self.F['body'],
                fg=Theme.TEXT2, bg=Theme.CARD, anchor='w',
                wraplength=self.s(300), justify='left')
        desc_label.pack(fill='x')

        # Subtle arrow indicator
        arrow = tk.Label(inner, text="→", font=self.F['h3'],
                        fg=Theme.SUBTLE, bg=Theme.CARD)
        arrow.pack(side='right', anchor='se', pady=(self.s(8), 0))

        # Click action - collect all clickable widgets
        all_widgets = [outer, card, inner, top, icon_bg, title_label, desc_label, arrow]

        def on_enter(e):
            card.configure(highlightbackground=accent, bg=Theme.CARD_HOVER)
            inner.configure(bg=Theme.CARD_HOVER)
            top.configure(bg=Theme.CARD_HOVER)
            title_label.configure(bg=Theme.CARD_HOVER, fg=accent)
            desc_label.configure(bg=Theme.CARD_HOVER)
            arrow.configure(bg=Theme.CARD_HOVER, fg=accent)

        def on_leave(e):
            card.configure(highlightbackground=Theme.BORDER_LIGHT, bg=Theme.CARD)
            inner.configure(bg=Theme.CARD)
            top.configure(bg=Theme.CARD)
            title_label.configure(bg=Theme.CARD, fg=Theme.WHITE)
            desc_label.configure(bg=Theme.CARD)
            arrow.configure(bg=Theme.CARD, fg=Theme.SUBTLE)

        for w in all_widgets:
            try:
                w.bind('<Enter>', on_enter)
                w.bind('<Leave>', on_leave)
                w.bind('<Button-1>', lambda e, c=cmd: c())
            except:
                pass

    def _premium_card(self, parent, label, title, desc, accent, grad, icon, cmd, row, col):
        """Create ultra-premium home card."""
        # Card container
        card_canvas = GlassCard(parent, glow_color=Theme.GLASS_BORDER_LIGHT, animated=True)
        card_canvas.grid(row=row, column=col, padx=self.s(12), pady=self.s(12), sticky='nsew')

        content = card_canvas.get_content_frame()
        content.configure(cursor="hand2")

        inner = tk.Frame(content, bg=Theme.CARD)
        inner.pack(fill='both', expand=True, padx=self.s(28), pady=self.s(28))

        # Top row: Badge and icon
        top = tk.Frame(inner, bg=Theme.CARD)
        top.pack(fill='x')

        # Label badge with gradient background (simulated)
        badge_frame = tk.Frame(top, bg=accent)
        badge_frame.pack(side='left')
        tk.Label(badge_frame, text=f"  {label.upper()}  ", font=self.F['xxs'],
                fg=Theme.BG_DARK, bg=accent).pack(padx=1, pady=1)

        # Icon
        tk.Label(top, text=icon, font=("Segoe UI Emoji", self.s(28)),
                bg=Theme.CARD).pack(side='right')

        # Title
        tk.Label(inner, text=title, font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w', pady=(self.s(24), self.s(10)))

        # Description
        tk.Label(inner, text=desc, font=self.F['sm'],
                fg=Theme.TEXT3, bg=Theme.CARD,
                wraplength=self.s(320), justify='left').pack(anchor='w')

        # Bottom: CTA button simulation
        bottom = tk.Frame(inner, bg=Theme.CARD)
        bottom.pack(side='bottom', fill='x', pady=(self.s(20), 0))

        cta = tk.Label(bottom, text="Get Started →", font=self.F['body_bold'],
                      fg=accent, bg=Theme.CARD, cursor="hand2")
        cta.pack(side='left')

        # Hover effects
        all_widgets = [card_canvas, content, inner, top, bottom, cta] + list(inner.winfo_children()) + list(top.winfo_children())

        def enter(e):
            card_canvas.set_glow(accent)
            for w in all_widgets:
                try:
                    if not isinstance(w, tk.Frame) or w.cget('bg') != accent:
                        if hasattr(w, 'configure') and w != badge_frame:
                            parent_bg = w.master.cget('bg') if hasattr(w.master, 'cget') else Theme.CARD
                            if parent_bg == Theme.CARD:
                                w.configure(bg=Theme.CARD_HOVER)
                except:
                    pass

        def leave(e):
            card_canvas.set_glow(Theme.GLASS_BORDER_LIGHT)
            for w in all_widgets:
                try:
                    if not isinstance(w, tk.Frame) or w.cget('bg') != accent:
                        if hasattr(w, 'configure') and w != badge_frame:
                            parent_bg = w.master.cget('bg') if hasattr(w.master, 'cget') else Theme.CARD
                            if parent_bg in [Theme.CARD, Theme.CARD_HOVER]:
                                w.configure(bg=Theme.CARD)
                except:
                    pass

        for w in all_widgets:
            try:
                w.bind('<Enter>', enter)
                w.bind('<Leave>', leave)
                w.bind('<Button-1>', lambda e, c=cmd: c())
            except:
                pass

    # ══════════════════════════════════════════════════════════════════════════
    # AI RECOGNITION PAGE
    # ══════════════════════════════════════════════════════════════════════════

    def ai_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Header
        header = tk.Frame(self.frame, bg=Theme.BG)
        header.pack(fill='x', padx=self.s(40), pady=(self.s(25), self.s(15)))

        self.back_nav(header).pack(side='left')

        tk.Label(header, text="AI Recognition", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(side='left', padx=(self.s(20), 0))

        tk.Label(header, text="● AI Ready", font=self.F['sm'],
                fg=Theme.SUCCESS, bg=Theme.BG).pack(side='right')

        # Content - two columns
        content = tk.Frame(self.frame, bg=Theme.BG)
        content.pack(fill='both', expand=True, padx=self.s(40), pady=(0, self.s(25)))

        # Left - Upload
        left = tk.Frame(content, bg=Theme.BG)
        left.pack(side='left', fill='both', expand=True, padx=(0, self.s(10)))

        # Simple card frame
        upload_card = tk.Frame(left, bg=Theme.CARD, highlightbackground=Theme.BORDER, highlightthickness=1)
        upload_card.pack(fill='both', expand=True)

        upload_inner = tk.Frame(upload_card, bg=Theme.CARD)
        upload_inner.pack(fill='both', expand=True, padx=self.s(20), pady=self.s(20))

        # Upload header
        tk.Label(upload_inner, text="Upload Image", font=self.F['h3'],
                fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w')
        tk.Label(upload_inner, text="Supports JPG, PNG, WebP, GIF formats",
                font=self.F['xs'], fg=Theme.MUTED, bg=Theme.CARD).pack(anchor='w')

        # Preview area - clickable to browse
        preview_outer = tk.Frame(upload_inner, bg=Theme.BG3,
                                highlightbackground=Theme.GLASS_BORDER_LIGHT,
                                highlightthickness=2, cursor="hand2")
        preview_outer.pack(fill='both', expand=True, pady=(self.s(22), self.s(20)))

        self.preview_frame = tk.Frame(preview_outer, bg=Theme.BG3, cursor="hand2")
        self.preview_frame.pack(fill='both', expand=True, padx=4, pady=4)

        # Placeholder
        self.placeholder = tk.Frame(self.preview_frame, bg=Theme.BG3, cursor="hand2")
        self.placeholder.place(relx=0.5, rely=0.5, anchor='center')

        # Upload icon
        icon_size = self.s(90)
        icon_frame = tk.Frame(self.placeholder, bg=Theme.CARD2, width=icon_size, height=icon_size, cursor="hand2")
        icon_frame.pack()
        icon_frame.pack_propagate(False)

        icon_label = tk.Label(icon_frame, text="📷", font=("Segoe UI Emoji", self.s(32)), bg=Theme.CARD2, cursor="hand2")
        icon_label.place(relx=0.5, rely=0.5, anchor='center')

        browse_hint = tk.Label(self.placeholder, text="Drop image here or click to browse",
                font=self.F['body'], fg=Theme.TEXT3, bg=Theme.BG3, cursor="hand2")
        browse_hint.pack(pady=(self.s(20), 0))
        size_hint = tk.Label(self.placeholder, text="Maximum file size: 10MB",
                font=self.F['xs'], fg=Theme.MUTED, bg=Theme.BG3, cursor="hand2")
        size_hint.pack(pady=(self.s(8), 0))

        # Bind click-to-browse on all preview area elements
        for widget in [preview_outer, self.preview_frame, self.placeholder, icon_frame, icon_label, browse_hint, size_hint]:
            widget.bind('<Button-1>', lambda e: self._browse())

        self.preview_photo = None
        self.preview_label = None

        # File info
        self.file_var = tk.StringVar(value="No file selected")
        tk.Label(upload_inner, textvariable=self.file_var, font=self.F['xs'],
                fg=Theme.TEXT3, bg=Theme.CARD).pack(anchor='w', pady=(0, self.s(18)))

        # Buttons
        btn_row = tk.Frame(upload_inner, bg=Theme.CARD)
        btn_row.pack(fill='x')

        browse = self.gradient_btn(btn_row, "Browse Files", self._browse, colors=[Theme.CARD_GLOW, Theme.CARD_HOVER])
        browse.pack(side='left', fill='x', expand=True, padx=(0, self.s(12)))

        analyze = self.gradient_btn(btn_row, "Analyze Image", self._analyze, colors=Theme.GRAD_PRIMARY)
        analyze.pack(side='left', fill='x', expand=True)

        # Status
        self.status_var = tk.StringVar()
        self.status_lbl = tk.Label(upload_inner, textvariable=self.status_var,
                                  font=self.F['sm'], fg=Theme.PRIMARY, bg=Theme.CARD)
        self.status_lbl.pack(pady=(self.s(20), 0))

        # Right - Results
        right = tk.Frame(content, bg=Theme.BG)
        right.pack(side='left', fill='both', expand=True, padx=(self.s(10), 0))

        # Simple card frame
        results_card = tk.Frame(right, bg=Theme.CARD, highlightbackground=Theme.BORDER, highlightthickness=1)
        results_card.pack(fill='both', expand=True)

        results_inner = tk.Frame(results_card, bg=Theme.CARD)
        results_inner.pack(fill='both', expand=True, padx=self.s(20), pady=self.s(20))

        tk.Label(results_inner, text="Analysis Results", font=self.F['h3'],
                fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w')
        tk.Label(results_inner, text="Top predictions with confidence scores",
                font=self.F['sm'], fg=Theme.MUTED, bg=Theme.CARD).pack(anchor='w', pady=(0, self.s(15)))

        self.results_frame = tk.Frame(results_inner, bg=Theme.CARD)
        self.results_frame.pack(fill='both', expand=True)

        self._empty_results()
        self.selected_image = None

    def _empty_results(self):
        """Premium empty state."""
        for w in self.results_frame.winfo_children():
            w.destroy()

        ph = tk.Frame(self.results_frame, bg=Theme.CARD)
        ph.pack(expand=True)

        # Animated icon
        tk.Label(ph, text="🔍", font=("Segoe UI Emoji", self.s(48)),
                bg=Theme.CARD).pack()

        tk.Label(ph, text="Ready to Analyze", font=self.F['h3'],
                fg=Theme.TEXT2, bg=Theme.CARD).pack(pady=(self.s(16), 0))
        tk.Label(ph, text="Upload an image to identify the breed",
                font=self.F['sm'], fg=Theme.MUTED, bg=Theme.CARD).pack(pady=(self.s(8), 0))

    def _browse(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.webp")])
        if path:
            self.selected_image = path
            name = os.path.basename(path)
            self.file_var.set(name[:45] + "..." if len(name) > 48 else name)
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
                self.preview_label = tk.Label(self.preview_frame, bg=Theme.BG3)
            self.preview_label.configure(image=self.preview_photo)
            self.preview_label.place(relx=0.5, rely=0.5, anchor='center')
        except Exception:
            pass

    def _analyze(self):
        if not self.selected_image:
            self.status_var.set("⚠ Please select an image first")
            return

        for w in self.results_frame.winfo_children():
            w.destroy()

        # Premium loading state
        loading = tk.Frame(self.results_frame, bg=Theme.CARD)
        loading.pack(expand=True)

        spinner = self.spinner(loading)
        spinner.pack()
        spinner.start()
        self.animations.append(spinner)

        tk.Label(loading, text="Analyzing Image", font=self.F['h3'],
                fg=Theme.TEXT, bg=Theme.CARD).pack(pady=(self.s(20), 0))
        tk.Label(loading, text="Processing with neural network...",
                font=self.F['xs'], fg=Theme.MUTED, bg=Theme.CARD).pack(pady=(self.s(8), 0))

        self.status_var.set("🔄 Processing...")
        self.root.update()

        threading.Thread(target=self._run_ai, daemon=True).start()

    def _run_ai(self):
        try:
            from image_classifier import DogImageClassifier
            if not self.classifier:
                self.classifier = DogImageClassifier()
            results = self.classifier.classify_image(self.selected_image)
            self.root.after(0, lambda: self._show_results(results))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"❌ Error: {str(e)[:40]}"))

    def _show_results(self, results):
        self.status_var.set("")

        for w in self.results_frame.winfo_children():
            w.destroy()

        if not results:
            self.status_var.set("❌ Could not classify image")
            self._empty_results()
            return

        colors = [Theme.AURORA_1, Theme.AURORA_2, Theme.AURORA_4, Theme.AURORA_5, Theme.AURORA_3]
        medals = ["🥇", "🥈", "🥉", "4", "5"]

        for i, r in enumerate(results[:5]):
            breed = r.get('breed', 'Unknown')
            conf = r.get('confidence', 0)
            verified = r.get('verified', False)
            db_name = r.get('db_name', breed)
            display = db_name if verified else breed

            # Result row with premium styling
            row = tk.Frame(self.results_frame, bg=Theme.BG3, cursor="hand2")
            row.pack(fill='x', pady=self.s(6))

            inner = tk.Frame(row, bg=Theme.BG3)
            inner.pack(fill='x', padx=self.s(20), pady=self.s(16))

            # Medal/Rank
            clr = colors[i] if i < len(colors) else Theme.MUTED
            medal = medals[i] if i < 3 else str(i + 1)

            rank_frame = tk.Frame(inner, bg=clr, width=self.s(44), height=self.s(44))
            rank_frame.pack(side='left', padx=(0, self.s(18)))
            rank_frame.pack_propagate(False)

            if i < 3:
                tk.Label(rank_frame, text=medal, font=("Segoe UI Emoji", self.s(18)),
                        bg=clr).place(relx=0.5, rely=0.5, anchor='center')
            else:
                tk.Label(rank_frame, text=f"#{i+1}", font=self.F['body_bold'],
                        fg=Theme.BG_DARK, bg=clr).place(relx=0.5, rely=0.5, anchor='center')

            # Info
            info = tk.Frame(inner, bg=Theme.BG3)
            info.pack(side='left', fill='both', expand=True)

            tk.Label(info, text=display, font=self.F['body_bold'],
                    fg=Theme.WHITE, bg=Theme.BG3).pack(anchor='w')

            status_text = "✓ Verified in database" if verified else "AI prediction"
            status_clr = Theme.SUCCESS if verified else Theme.MUTED
            tk.Label(info, text=status_text, font=self.F['xs'],
                    fg=status_clr, bg=Theme.BG3).pack(anchor='w')

            # Progress bar
            right = tk.Frame(inner, bg=Theme.BG3)
            right.pack(side='right')

            bar_w = self.s(160)
            bar_h = self.s(12)

            bar_bg = tk.Canvas(right, width=bar_w, height=bar_h, bg=Theme.BG, highlightthickness=0)
            bar_bg.pack(side='left', padx=(0, self.s(16)))

            # Rounded bar background
            bar_bg.create_rectangle(0, 0, bar_w, bar_h, fill=Theme.BG, outline='')

            # Filled portion with gradient effect
            fill_w = max(4, int(bar_w * conf / 100))
            bar_bg.create_rectangle(0, 0, fill_w, bar_h, fill=clr, outline='')

            tk.Label(right, text=f"{conf:.1f}%", font=self.F['body_bold'],
                    fg=clr, bg=Theme.BG3, width=7, anchor='e').pack(side='left')

            # Click handler
            def make_click(name):
                return lambda e: self._breed_popup(name)

            for widget in [row, inner, info, right]:
                widget.bind('<Button-1>', make_click(display))

            # Hover
            def make_enter(r, c):
                return lambda e: r.configure(highlightbackground=c, highlightthickness=2)
            def make_leave(r):
                return lambda e: r.configure(highlightthickness=0)

            row.bind('<Enter>', make_enter(row, clr))
            row.bind('<Leave>', make_leave(row))

        # Hint
        tk.Label(self.results_frame, text="Click any result to view detailed breed information",
                font=self.F['xs'], fg=Theme.DIM, bg=Theme.CARD).pack(pady=(self.s(24), 0))

    # ══════════════════════════════════════════════════════════════════════════
    # QUESTIONNAIRE PAGE
    # ══════════════════════════════════════════════════════════════════════════

    def quest_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Header
        header = tk.Frame(self.frame, bg=Theme.BG)
        header.pack(fill='x', padx=self.s(40), pady=(self.s(25), self.s(15)))

        self.back_nav(header).pack(side='left')

        tk.Label(header, text="Feature Questionnaire", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(side='left', padx=(self.s(20), 0))

        # Content
        content = tk.Frame(self.frame, bg=Theme.BG)
        content.pack(fill='both', expand=True, padx=self.s(40), pady=(0, self.s(25)))

        # Form card - simple frame
        form_card = tk.Frame(content, bg=Theme.CARD, highlightbackground=Theme.BORDER, highlightthickness=1)
        form_card.pack(fill='x')

        form_inner = tk.Frame(form_card, bg=Theme.CARD)
        form_inner.pack(fill='x', padx=self.s(25), pady=self.s(25))

        # Questions with comprehensive options for 150+ breeds
        # Each question has: key, label, options, and help text
        self.quest_vars = {}
        questions = [
            ("color", "Primary Color", [
                "-- Select Color --", "Black", "White", "Brown", "Tan", "Golden", "Yellow",
                "Red", "Cream", "Gray", "Blue", "Liver", "Chocolate", "Brindle",
                "Merle", "Sable", "Tricolor", "Bicolor", "Spotted"
            ], "The main/dominant color of the coat. Brindle=tiger stripes, Merle=mottled patches, Tricolor=3 distinct colors"),
            ("ear", "Ear Type", [
                "-- Select Ear Type --", "Floppy", "Erect", "Semi-erect", "Button",
                "Rose", "V-shaped", "Bat", "Folded"
            ], "Floppy=hang down (Beagle), Erect=stand up (German Shepherd), Button=fold forward (Fox Terrier), Rose=fold back (Greyhound), Bat=large & rounded (French Bulldog)"),
            ("tail", "Tail Type", [
                "-- Select Tail Type --", "Long_and_curved", "Curled", "Docked",
                "Straight", "Sickle", "Plume", "Whip", "Natural bob"
            ], "Curled=curves over back (Pug, Husky), Docked=surgically shortened, Plume=feathered & flowing, Sickle=curves upward like a crescent"),
            ("size", "Size", [
                "-- Select Size --", "Toy (under 10 lbs)", "Small (10-25 lbs)",
                "Medium (25-50 lbs)", "Large (50-100 lbs)", "Giant (over 100 lbs)"
            ], "Estimate adult weight. Toy: Chihuahua, Small: Beagle, Medium: Border Collie, Large: Labrador, Giant: Great Dane"),
            ("coat", "Coat Type", [
                "-- Select Coat Type --", "Short", "Medium", "Long", "Curly",
                "Wavy", "Wire/Rough", "Double", "Smooth", "Silky", "Corded", "Hairless"
            ], "Short=sleek & close (Lab), Double=thick undercoat (Husky), Wire=bristly texture (Terriers), Curly=tight curls (Poodle), Silky=soft & flowing (Setter)"),
        ]

        # Create a centered grid for questions
        grid_frame = tk.Frame(form_inner, bg=Theme.CARD)
        grid_frame.pack(fill='x', expand=True)

        for i, (key, label, opts, help_text) in enumerate(questions):
            row_idx = i // 2
            col_idx = i % 2

            q_frame = tk.Frame(grid_frame, bg=Theme.CARD)
            q_frame.grid(row=row_idx, column=col_idx, padx=self.s(20), pady=self.s(14), sticky='ew')

            tk.Label(q_frame, text=label, font=self.F['body_bold'],
                    fg=Theme.TEXT2, bg=Theme.CARD).pack(anchor='w')

            var = tk.StringVar(value=opts[0])
            self.quest_vars[key] = var

            # Use custom modern dropdown
            dropdown = ModernDropdown(q_frame, values=opts, textvariable=var, width=self.s(200))
            dropdown.pack(anchor='w', pady=(self.s(8), 0), fill='x')

            # Help text below dropdown
            tk.Label(q_frame, text=help_text, font=self.F['xs'],
                    fg=Theme.TEXT3, bg=Theme.CARD, wraplength=self.s(280),
                    justify='left').pack(anchor='w', pady=(self.s(6), 0))

        # Configure grid columns to be equal width
        grid_frame.grid_columnconfigure(0, weight=1, uniform='quest')
        grid_frame.grid_columnconfigure(1, weight=1, uniform='quest')

        # Submit
        btn_frame = tk.Frame(content, bg=Theme.BG)
        btn_frame.pack(pady=self.s(30))

        submit = self.gradient_btn(btn_frame, "Find Matching Breeds", self._run_quest, colors=Theme.GRAD_SECONDARY)
        submit.pack()

        # Results
        self.quest_results = tk.Frame(content, bg=Theme.BG)
        self.quest_results.pack(fill='both', expand=True)

    def _run_quest(self):
        for w in self.quest_results.winfo_children():
            w.destroy()

        # Clean up values (handle placeholders and extract size category)
        def clean_val(val):
            if val.startswith('--'):
                return ''
            return val

        color = clean_val(self.quest_vars["color"].get())
        ear = clean_val(self.quest_vars["ear"].get()).lower()
        tail = clean_val(self.quest_vars["tail"].get()).lower()
        coat = clean_val(self.quest_vars["coat"].get()).lower()

        # Extract size category from dropdown option
        size_val = clean_val(self.quest_vars["size"].get()).lower()
        # Map detailed sizes to database values
        size_map = {
            'toy (under 10 lbs)': 'small',
            'small (10-25 lbs)': 'small',
            'medium (25-50 lbs)': 'medium',
            'large (50-100 lbs)': 'large',
            'giant (over 100 lbs)': 'giant'
        }
        size = size_map.get(size_val, size_val)

        # Handle coat type mappings
        coat_map = {
            'wire/rough': 'wiry',
            'silky': 'long',
            'wavy': 'medium'
        }
        coat = coat_map.get(coat, coat)

        db = Database()
        results = db.query(color, ear, tail, size, coat)
        db.close()

        if results:
            card = self.glass_card(self.quest_results, animated=True)
            card.pack(fill='x')

            card_content = card.get_content_frame()
            inner = tk.Frame(card_content, bg=Theme.CARD)
            inner.pack(fill='x', padx=self.s(30), pady=self.s(30))

            tk.Label(inner, text="Matching Breeds", font=self.F['h3'],
                    fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w', pady=(0, self.s(18)))

            colors = [Theme.SUCCESS, Theme.CYAN, Theme.ORANGE]

            for i, (breed, _, prob) in enumerate(results):
                row = tk.Frame(inner, bg=Theme.BG3, cursor="hand2")
                row.pack(fill='x', pady=self.s(6))

                row_inner = tk.Frame(row, bg=Theme.BG3)
                row_inner.pack(fill='x', padx=self.s(20), pady=self.s(16))

                clr = colors[i] if i < len(colors) else Theme.MUTED

                badge = tk.Frame(row_inner, bg=clr)
                badge.pack(side='left', padx=(0, self.s(16)))
                tk.Label(badge, text=f"  #{i+1}  ", font=self.F['body_bold'],
                        fg=Theme.BG_DARK, bg=clr).pack(pady=2)

                tk.Label(row_inner, text=breed, font=self.F['body_bold'],
                        fg=Theme.WHITE, bg=Theme.BG3).pack(side='left')
                tk.Label(row_inner, text=f"{prob:.0f}% match", font=self.F['body_bold'],
                        fg=clr, bg=Theme.BG3).pack(side='right')

                row.bind('<Button-1>', lambda e, b=breed: self._breed_popup(b))
        else:
            tk.Label(self.quest_results, text="No matching breeds found",
                    font=self.F['body'], fg=Theme.MUTED, bg=Theme.BG).pack(pady=self.s(60))

    # ══════════════════════════════════════════════════════════════════════════
    # DICHOTOMOUS KEY PAGE
    # ══════════════════════════════════════════════════════════════════════════

    def _build_tree(self):
        """Build comprehensive dichotomous key for 150+ breeds."""
        # Each node has: q=question, d=description (help text), y=yes branch, n=no branch, r=result
        return {
            "q": "Is your dog small (under 25 lbs)?",
            "d": "Small dogs can be held comfortably in your arms. Think Chihuahua, Pug, or Yorkshire Terrier size.",
            "y": {
                # SMALL DOGS
                "q": "Does your dog have floppy ears?",
                "d": "Floppy ears hang down past the jawline and swing when the dog moves. Examples: Beagle, Cocker Spaniel, Dachshund.",
                "y": {
                    # Small + Floppy ears
                    "q": "Does your dog have a long, silky coat?",
                    "d": "Long silky coats flow past the body and feel smooth like human hair. Requires regular brushing. Examples: Maltese, Shih Tzu, Yorkshire Terrier.",
                    "y": {
                        "q": "Is the coat white or predominantly white?",
                        "d": "More than 50% of the coat is white or cream colored.",
                        "y": {
                            "q": "Does it have a slightly pushed-in face?",
                            "d": "The snout is short and flat rather than pointed. The face looks 'smooshed' with large round eyes.",
                            "y": {"r": "Shih Tzu"},
                            "n": {"r": "Maltese"}
                        },
                        "n": {
                            "q": "Does it have a golden/tan and white coat?",
                            "d": "Coat has patches of golden, chestnut, or tan color mixed with white.",
                            "y": {"r": "Cavalier King Charles Spaniel"},
                            "n": {"r": "Yorkshire Terrier"}
                        }
                    },
                    "n": {
                        "q": "Does it have a short, smooth coat?",
                        "d": "Short coats lie flat against the body, feel sleek to touch, and don't require much brushing. Examples: Beagle, Dachshund.",
                        "y": {
                            "q": "Is it primarily black and tan?",
                            "d": "Main body is black with tan/rust markings above eyes, on muzzle, chest, and legs.",
                            "y": {"r": "Dachshund"},
                            "n": {
                                "q": "Does it have a spotted or tricolor pattern?",
                                "d": "Tricolor means three distinct colors (usually black, tan, and white). Spotted means irregular patches of color.",
                                "y": {"r": "Beagle"},
                                "n": {"r": "Miniature Pinscher"}
                            }
                        },
                        "n": {
                            "q": "Does it have a wiry/rough coat?",
                            "d": "Wiry coats feel coarse and bristly, like a scrub brush. Hair stands away from body. Examples: Schnauzer, many terriers.",
                            "y": {"r": "Miniature Schnauzer"},
                            "n": {"r": "Cocker Spaniel"}
                        }
                    }
                },
                "n": {
                    # Small + Erect ears
                    "q": "Does your dog have erect/pointed ears?",
                    "d": "Erect ears stand straight up like triangles on top of the head. Examples: Chihuahua, Pomeranian, French Bulldog.",
                    "y": {
                        "q": "Does it have a fluffy, double coat?",
                        "d": "Double coats have a soft dense undercoat plus longer outer fur. Dog looks puffy/fluffy. Sheds heavily.",
                        "y": {
                            "q": "Is the coat predominantly white?",
                            "d": "More than 50% of the coat is white or cream colored.",
                            "y": {"r": "American Eskimo Dog"},
                            "n": {"r": "Pomeranian"}
                        },
                        "n": {
                            "q": "Does it have a smooth, short coat?",
                            "d": "Short coats lie flat against the body, feel sleek to touch. Minimal grooming needed.",
                            "y": {
                                "q": "Is it apple-headed with large eyes?",
                                "d": "Apple head means a rounded dome-shaped skull. Eyes are prominent and bulging slightly.",
                                "y": {"r": "Chihuahua"},
                                "n": {"r": "Toy Fox Terrier"}
                            },
                            "n": {
                                "q": "Does it have a wiry coat?",
                                "d": "Wiry coats feel coarse and bristly, like a scrub brush. Hair stands away from body.",
                                "y": {"r": "Norwich Terrier"},
                                "n": {"r": "Papillon"}
                            }
                        }
                    },
                    "n": {
                        # Small + Button/rose ears
                        "q": "Does it have a flat, pushed-in face?",
                        "d": "Also called brachycephalic. The snout is very short, face looks flat or 'smooshed'. Often snores. Examples: Pug, French Bulldog, Boston Terrier.",
                        "y": {
                            "q": "Does it have wrinkly skin and a curled tail?",
                            "d": "Wrinkles are folds of loose skin on face/forehead. Curled tail curves tightly up and over the back like a cinnamon roll.",
                            "y": {"r": "Pug"},
                            "n": {
                                "q": "Does it have bat-like ears that stand up?",
                                "d": "Bat ears are large, broad at base, rounded at tips, and stand erect. Much larger than typical pointed ears.",
                                "y": {"r": "French Bulldog"},
                                "n": {"r": "Boston Terrier"}
                            }
                        },
                        "n": {
                            "q": "Does it have a fluffy white coat?",
                            "d": "Coat is predominantly white and puffy/cotton-like in texture. Dog looks like a little cloud.",
                            "y": {"r": "Bichon Frise"},
                            "n": {
                                "q": "Does it have large butterfly-like ears with fringe?",
                                "d": "Ears are large and feathered with long silky hair, spread out like butterfly wings when alert.",
                                "y": {"r": "Papillon"},
                                "n": {"r": "Havanese"}
                            }
                        }
                    }
                }
            },
            "n": {
                # MEDIUM TO GIANT DOGS
                "q": "Is your dog giant sized (over 100 lbs)?",
                "d": "Giant breeds are very large and heavy. Examples: Great Dane, Mastiff, Saint Bernard, Newfoundland.",
                "y": {
                    # GIANT DOGS
                    "q": "Does your dog have a thick, fluffy coat?",
                    "d": "Thick fluffy coats stand away from body, feel plush and dense. Dog looks bigger due to all the fur.",
                    "y": {
                        "q": "Is the coat primarily white?",
                        "d": "More than 50% of the coat is white or cream colored.",
                        "y": {
                            "q": "Does it have a massive head with loose skin?",
                            "d": "Head is very large in proportion to body. Skin hangs loose around face and jowls.",
                            "y": {"r": "Great Pyrenees"},
                            "n": {"r": "Samoyed"}
                        },
                        "n": {
                            "q": "Is it black, white, and rust tricolor?",
                            "d": "Three distinct colors: black as main color, white on chest/blaze/paws, rust/tan on cheeks and legs.",
                            "y": {"r": "Bernese Mountain Dog"},
                            "n": {
                                "q": "Does it have corded (dreadlock-like) fur?",
                                "d": "Coat forms long rope-like cords that hang down, similar to dreadlocks or a mop.",
                                "y": {"r": "Komondor"},
                                "n": {"r": "Newfoundland"}
                            }
                        }
                    },
                    "n": {
                        "q": "Does it have a short, smooth coat?",
                        "d": "Short coats lie flat against the body, feel sleek to touch. You can see the muscle definition underneath.",
                        "y": {
                            "q": "Is it black and tan with a muscular build?",
                            "d": "Main body is black with tan/rust markings above eyes, on muzzle, chest, and legs. Body is thick and powerful.",
                            "y": {"r": "Rottweiler"},
                            "n": {
                                "q": "Is it very tall and lean?",
                                "d": "Dog is exceptionally tall (over 28 inches) with a slender, athletic build. Long legs.",
                                "y": {"r": "Great Dane"},
                                "n": {
                                    "q": "Does it have a wrinkly, droopy face?",
                                    "d": "Face has heavy wrinkles and loose skin. Jowls hang down. Expression looks serious or sad.",
                                    "y": {"r": "Mastiff"},
                                    "n": {"r": "Cane Corso"}
                                }
                            }
                        },
                        "n": {
                            "q": "Does it have a medium-length coat with feathering?",
                            "d": "Feathering means longer hair on ears, chest, belly, legs, and tail. Creates a flowing, elegant look.",
                            "y": {
                                "q": "Is it red/brown and white?",
                                "d": "Coat has large patches of reddish-brown or mahogany color with white markings.",
                                "y": {"r": "Saint Bernard"},
                                "n": {"r": "Leonberger"}
                            },
                            "n": {"r": "Irish Wolfhound"}
                        }
                    }
                },
                "n": {
                    # MEDIUM TO LARGE DOGS (25-100 lbs)
                    "q": "Is your dog large (50-100 lbs)?",
                    "d": "Large dogs are substantial but not giant. Examples: Labrador, Golden Retriever, German Shepherd, Boxer.",
                    "y": {
                        # LARGE DOGS
                        "q": "Does your dog have floppy ears?",
                        "d": "Floppy ears hang down past the jawline and swing when the dog moves. Examples: Labrador, Golden Retriever, Beagle.",
                        "y": {
                            "q": "Does it have a golden/yellow coat?",
                            "d": "Coat color ranges from cream to deep gold/yellow. Solid color without major markings.",
                            "y": {
                                "q": "Is the coat long and wavy?",
                                "d": "Coat is several inches long with gentle waves or slight curl. Feathering on chest, legs, and tail.",
                                "y": {"r": "Golden Retriever"},
                                "n": {"r": "Labrador Retriever"}
                            },
                            "n": {
                                "q": "Is it black and tan or tricolor?",
                                "d": "Black and tan: black body with tan markings. Tricolor: black, tan, and white in distinct areas.",
                                "y": {
                                    "q": "Does it have a long, silky coat?",
                                    "d": "Coat is long and flows smoothly, feels like silk. Requires regular grooming.",
                                    "y": {"r": "Gordon Setter"},
                                    "n": {"r": "Rottweiler"}
                                },
                                "n": {
                                    "q": "Does it have a spotted or liver/white coat?",
                                    "d": "Spotted: distinct spots or ticking. Liver: brown/chocolate color. Often with white base.",
                                    "y": {
                                        "q": "Is it white with black spots?",
                                        "d": "Base coat is white with distinct black spots scattered across body, like a dalmatian pattern.",
                                        "y": {"r": "Dalmatian"},
                                        "n": {"r": "German Shorthaired Pointer"}
                                    },
                                    "n": {
                                        "q": "Is it red/mahogany with a silky coat?",
                                        "d": "Rich reddish-brown color like polished wood. Coat is long, silky, and flowing.",
                                        "y": {"r": "Irish Setter"},
                                        "n": {"r": "Weimaraner"}
                                    }
                                }
                            }
                        },
                        "n": {
                            # Large + Erect ears
                            "q": "Does it have erect, pointed ears?",
                            "d": "Erect ears stand straight up like triangles on top of the head. Alert and forward-facing.",
                            "y": {
                                "q": "Is it black and tan with a sloped back?",
                                "d": "Classic police dog look: black saddle on back, tan legs/chest/face. Back slopes down toward tail.",
                                "y": {"r": "German Shepherd"},
                                "n": {
                                    "q": "Is it sleek and black/rust with cropped ears?",
                                    "d": "Very sleek, muscular body. Black or dark brown with rust markings. Ears may be cropped to stand tall.",
                                    "y": {"r": "Doberman Pinscher"},
                                    "n": {
                                        "q": "Does it have a thick double coat?",
                                        "d": "Double coats have soft dense undercoat plus longer outer fur. Dog looks fluffy. Sheds heavily.",
                                        "y": {
                                            "q": "Is it gray/white with blue eyes?",
                                            "d": "Coat is gray and white (or black and white). Eyes are striking blue or multi-colored.",
                                            "y": {"r": "Siberian Husky"},
                                            "n": {"r": "Alaskan Malamute"}
                                        },
                                        "n": {"r": "Belgian Malinois"}
                                    }
                                }
                            },
                            "n": {
                                "q": "Is it muscular with a square head?",
                                "d": "Body is athletic and muscular. Head is boxy/square shaped with a short muzzle. Strong jaw.",
                                "y": {"r": "Boxer"},
                                "n": {"r": "Rhodesian Ridgeback"}
                            }
                        }
                    },
                    "n": {
                        # MEDIUM DOGS (25-50 lbs)
                        "q": "Does your dog have floppy ears?",
                        "d": "Floppy ears hang down past the jawline and swing when the dog moves. Examples: Beagle, Cocker Spaniel, Basset Hound.",
                        "y": {
                            "q": "Does it have a curly or wavy coat?",
                            "d": "Coat forms curls or waves rather than lying flat. May look like wool or have loose ringlets.",
                            "y": {
                                "q": "Is the coat very curly and dense?",
                                "d": "Tight curls all over body, like lamb's wool. Very dense and doesn't shed much.",
                                "y": {"r": "Poodle"},
                                "n": {"r": "Portuguese Water Dog"}
                            },
                            "n": {
                                "q": "Does it have a medium-length coat with feathering?",
                                "d": "Feathering means longer hair on ears, chest, belly, legs, and tail. Creates flowing look.",
                                "y": {
                                    "q": "Is it primarily black and white?",
                                    "d": "Main colors are black and white in large patches or with ticking pattern.",
                                    "y": {"r": "Border Collie"},
                                    "n": {
                                        "q": "Does it have a merle pattern?",
                                        "d": "Merle is a mottled pattern with patches of darker color on lighter background. Often blue-gray or red.",
                                        "y": {"r": "Australian Shepherd"},
                                        "n": {"r": "English Springer Spaniel"}
                                    }
                                },
                                "n": {
                                    "q": "Does it have short legs and a long body?",
                                    "d": "Legs are notably short compared to body length. Dog is low to the ground with elongated torso.",
                                    "y": {"r": "Basset Hound"},
                                    "n": {
                                        "q": "Is it tricolor (black, tan, white)?",
                                        "d": "Three distinct colors in defined areas: black back, tan markings, white chest/legs/tail tip.",
                                        "y": {"r": "Beagle"},
                                        "n": {"r": "Brittany"}
                                    }
                                }
                            }
                        },
                        "n": {
                            # Medium + Erect ears
                            "q": "Does it have erect, pointed ears?",
                            "d": "Erect ears stand straight up like triangles on top of the head. Alert and forward-facing.",
                            "y": {
                                "q": "Does it have a fox-like appearance?",
                                "d": "Face resembles a fox: pointed muzzle, alert expression, triangular head shape, bushy tail.",
                                "y": {
                                    "q": "Is it red/sesame colored?",
                                    "d": "Coat is reddish-orange (like a fox) or sesame (red with black-tipped hairs).",
                                    "y": {"r": "Shiba Inu"},
                                    "n": {"r": "Finnish Spitz"}
                                },
                                "n": {
                                    "q": "Does it have a very fluffy coat?",
                                    "d": "Coat is thick, plush, and stands away from body. Dog looks like a fluffy ball.",
                                    "y": {"r": "Keeshond"},
                                    "n": {"r": "Basenji"}
                                }
                            },
                            "n": {
                                "q": "Does it have short legs with a long body?",
                                "d": "Legs are notably short compared to body length. Dog is low to the ground with elongated torso.",
                                "y": {"r": "Pembroke Welsh Corgi"},
                                "n": {
                                    "q": "Does it have a wiry coat?",
                                    "d": "Wiry coats feel coarse and bristly, like a scrub brush. Hair stands away from body.",
                                    "y": {"r": "Airedale Terrier"},
                                    "n": {"r": "Whippet"}
                                }
                            }
                        }
                    }
                }
            }
        }

    def dkey_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Header
        header = tk.Frame(self.frame, bg=Theme.BG)
        header.pack(fill='x', padx=self.s(40), pady=(self.s(25), self.s(15)))

        self.back_nav(header).pack(side='left')

        tk.Label(header, text="Dichotomous Key", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(side='left', padx=(self.s(20), 0))

        # Content
        self.dkey_content = tk.Frame(self.frame, bg=Theme.BG)
        self.dkey_content.pack(fill='both', expand=True, padx=self.s(40), pady=(0, self.s(25)))

        self.node = self.tree
        self.qnum = 0
        self._show_question()

    def _show_question(self):
        for w in self.dkey_content.winfo_children():
            w.destroy()

        if "r" in self.node:
            self._show_dkey_result(self.node["r"])
            return

        self.qnum += 1

        # Progress
        progress = tk.Frame(self.dkey_content, bg=Theme.BG)
        progress.pack(fill='x', pady=(0, self.s(30)))

        tk.Label(progress, text=f"Question {self.qnum}", font=self.F['body_bold'],
                fg=Theme.CYAN, bg=Theme.BG).pack(side='left')

        # Question card - use Frame for reliable sizing
        card = tk.Frame(self.dkey_content, bg=Theme.CARD, highlightbackground=Theme.CYAN, highlightthickness=2)
        card.pack(fill='x')

        inner = tk.Frame(card, bg=Theme.CARD)
        inner.pack(fill='x', padx=self.s(60), pady=self.s(50))

        tk.Label(inner, text="🤔", font=("Segoe UI Emoji", self.s(36)),
                bg=Theme.CARD).pack()

        tk.Label(inner, text=self.node["q"], font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.CARD,
                wraplength=self.s(650)).pack(pady=(self.s(20), 0))

        # Description/help text
        if "d" in self.node:
            desc_frame = tk.Frame(inner, bg=Theme.BG3)
            desc_frame.pack(fill='x', pady=(self.s(20), 0), padx=self.s(20))

            tk.Label(desc_frame, text="💡", font=self.F['body'],
                    bg=Theme.BG3).pack(side='left', padx=(self.s(12), self.s(8)), pady=self.s(12))

            tk.Label(desc_frame, text=self.node["d"], font=self.F['body'],
                    fg=Theme.TEXT2, bg=Theme.BG3,
                    wraplength=self.s(550), justify='left').pack(side='left', fill='x', expand=True, pady=self.s(12), padx=(0, self.s(12)))

        # Buttons
        btn_frame = tk.Frame(self.dkey_content, bg=Theme.BG)
        btn_frame.pack(pady=self.s(40))

        yes_btn = self.gradient_btn(btn_frame, "    Yes    ", lambda: self._answer(True), colors=Theme.GRAD_SUCCESS)
        yes_btn.pack(side='left', padx=self.s(15))

        no_btn = self.gradient_btn(btn_frame, "    No    ", lambda: self._answer(False), colors=Theme.GRAD_DANGER)
        no_btn.pack(side='left', padx=self.s(15))

        # Restart
        restart = tk.Label(self.dkey_content, text="Start over", font=self.F['body'],
                          fg=Theme.MUTED, bg=Theme.BG, cursor="hand2")
        restart.pack(pady=self.s(20))
        restart.bind('<Button-1>', lambda e: self._reset_dkey())
        restart.bind('<Enter>', lambda e: restart.config(fg=Theme.PRIMARY))
        restart.bind('<Leave>', lambda e: restart.config(fg=Theme.MUTED))

    def _answer(self, yes):
        self.node = self.node["y" if yes else "n"]
        self._show_question()

    def _show_dkey_result(self, breed):
        # Result card - use Frame for reliable sizing
        card = tk.Frame(self.dkey_content, bg=Theme.CARD, highlightbackground=Theme.SUCCESS, highlightthickness=2)
        card.pack(fill='x')

        inner = tk.Frame(card, bg=Theme.CARD)
        inner.pack(fill='x', padx=self.s(70), pady=self.s(50))

        # Success animation
        tk.Label(inner, text="🎉", font=("Segoe UI Emoji", self.s(48)),
                bg=Theme.CARD).pack()

        tk.Label(inner, text="Identification Complete!", font=self.F['h3'],
                fg=Theme.TEXT2, bg=Theme.CARD).pack(pady=(self.s(16), 0))

        tk.Label(inner, text=breed, font=self.F['hero_bold'],
                fg=Theme.PRIMARY, bg=Theme.CARD).pack(pady=self.s(20))

        tk.Label(inner, text=f"Identified in {self.qnum} questions",
                font=self.F['xs'], fg=Theme.MUTED, bg=Theme.CARD).pack()

        # Buttons
        btn_frame = tk.Frame(self.dkey_content, bg=Theme.BG)
        btn_frame.pack(pady=self.s(35))

        view_btn = self.gradient_btn(btn_frame, "View Breed Info", lambda: self._breed_popup(breed), colors=Theme.GRAD_PRIMARY)
        view_btn.pack(side='left', padx=self.s(12))

        retry_btn = self.gradient_btn(btn_frame, "Try Again", self._reset_dkey, colors=[Theme.CARD_GLOW, Theme.CARD_HOVER])
        retry_btn.pack(side='left', padx=self.s(12))

    def _reset_dkey(self):
        self.node = self.tree
        self.qnum = 0
        self._show_question()

    # ══════════════════════════════════════════════════════════════════════════
    # DATABASE PAGE
    # ══════════════════════════════════════════════════════════════════════════

    def db_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Header
        header = tk.Frame(self.frame, bg=Theme.BG)
        header.pack(fill='x', padx=self.s(40), pady=(self.s(25), self.s(15)))

        self.back_nav(header).pack(side='left')

        tk.Label(header, text="Breed Database", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(side='left', padx=(self.s(20), 0))

        count = len(BREED_INFO) if BREED_INFO else 0
        tk.Label(header, text=f"{count} breeds", font=self.F['sm'],
                fg=Theme.MUTED, bg=Theme.BG).pack(side='right')

        # Search - clean text entry field
        search_frame = tk.Frame(self.frame, bg=Theme.BG)
        search_frame.pack(fill='x', padx=self.s(40), pady=(0, self.s(15)))

        # Search input container with border
        search_container = tk.Frame(search_frame, bg=Theme.BG3,
                                   highlightbackground=Theme.BORDER_LIGHT, highlightthickness=1)
        search_container.pack(side='left', fill='x', expand=True)

        # Search icon label
        tk.Label(search_container, text="🔍", font=self.F['body'],
                fg=Theme.MUTED, bg=Theme.BG3, padx=self.s(12)).pack(side='left')

        # Text entry field
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_container, textvariable=self.search_var,
                               font=self.F['body'], bg=Theme.BG3, fg=Theme.WHITE,
                               insertbackground=Theme.WHITE, relief='flat',
                               highlightthickness=0)
        search_entry.pack(side='left', fill='x', expand=True, pady=self.s(12), padx=(0, self.s(12)))
        search_entry.insert(0, "")

        # Placeholder behavior
        def on_focus_in(e):
            search_container.configure(highlightbackground=Theme.PRIMARY)
        def on_focus_out(e):
            search_container.configure(highlightbackground=Theme.BORDER_LIGHT)
        search_entry.bind('<FocusIn>', on_focus_in)
        search_entry.bind('<FocusOut>', on_focus_out)

        # Live search as user types
        def on_search_change(*args):
            query = self.search_var.get().strip().lower()
            if query:
                self._filter_grid(query)
            else:
                self._show_grid()

        self.search_var.trace('w', on_search_change)

        # Enter key to jump to first match detail
        def on_enter(e):
            query = self.search_var.get().strip().lower()
            if query:
                for key, info in BREED_INFO.items():
                    if query in info['name'].lower():
                        self._show_detail(info['name'])
                        break
        search_entry.bind('<Return>', on_enter)

        # Clear button
        clear_btn = tk.Label(search_frame, text="✕", font=self.F['body'],
                            fg=Theme.MUTED, bg=Theme.BG, cursor="hand2", padx=self.s(12))
        clear_btn.pack(side='left')
        clear_btn.bind('<Button-1>', lambda e: (self.search_var.set(''), search_entry.focus()))
        clear_btn.bind('<Enter>', lambda e: clear_btn.configure(fg=Theme.WHITE))
        clear_btn.bind('<Leave>', lambda e: clear_btn.configure(fg=Theme.MUTED))

        # Content
        content = tk.Frame(self.frame, bg=Theme.BG)
        content.pack(fill='both', expand=True, padx=self.s(40), pady=(0, self.s(25)))

        container, self.db_inner = self.scrollable(content)
        container.pack(fill='both', expand=True)

        self._show_grid()

    def _filter_grid(self, query):
        """Filter breed grid based on search query."""
        for w in self.db_inner.winfo_children():
            w.destroy()

        # Filter breeds matching query
        matches = [(key, info) for key, info in BREED_INFO.items()
                   if query in info['name'].lower() or query in info.get('group', '').lower()]

        if not matches:
            tk.Label(self.db_inner, text=f"No breeds found matching '{query}'",
                    font=self.F['body'], fg=Theme.MUTED, bg=Theme.BG).pack(pady=self.s(40))
            return

        # Show match count
        tk.Label(self.db_inner, text=f"{len(matches)} breed{'s' if len(matches) != 1 else ''} found",
                font=self.F['sm'], fg=Theme.TEXT3, bg=Theme.BG).pack(anchor='w', pady=(0, self.s(10)))

        self._render_breed_cards(sorted(matches))

    def _show_grid(self):
        for w in self.db_inner.winfo_children():
            w.destroy()

        if not BREED_INFO:
            tk.Label(self.db_inner, text="No breed data available",
                    font=self.F['body'], fg=Theme.MUTED, bg=Theme.BG).pack(pady=self.s(60))
            return

        self._render_breed_cards(sorted(BREED_INFO.items()))

    def _render_breed_cards(self, breed_items):
        """Render breed cards in a grid layout."""
        # Show breeds in a clean 3-column grid with larger, more readable cards
        row_frame = None
        cols = 3  # Reduced from 4 for better readability

        for i, (key, info) in enumerate(breed_items):
            if i % cols == 0:
                row_frame = tk.Frame(self.db_inner, bg=Theme.BG)
                row_frame.pack(fill='x', pady=self.s(6))

            # Card with better visibility
            btn = tk.Frame(row_frame, bg=Theme.CARD, cursor="hand2",
                          highlightbackground=Theme.BORDER_LIGHT,
                          highlightthickness=1)
            btn.pack(side='left', fill='x', expand=True, padx=self.s(6))

            # Inner frame for padding
            inner = tk.Frame(btn, bg=Theme.CARD, cursor="hand2")
            inner.pack(fill='both', expand=True, padx=self.s(12), pady=self.s(14))

            # Breed name - larger font
            label = tk.Label(inner, text=info['name'], font=self.F['body'],
                           fg=Theme.WHITE, bg=Theme.CARD,
                           cursor="hand2", anchor='w')
            label.pack(fill='x')

            # Breed group subtitle
            group_label = tk.Label(inner, text=info.get('group', ''), font=self.F['xs'],
                                  fg=Theme.MUTED, bg=Theme.CARD,
                                  cursor="hand2", anchor='w')
            group_label.pack(fill='x', pady=(self.s(2), 0))

            def make_click(name):
                return lambda e: self._show_detail(name)

            for widget in [btn, inner, label, group_label]:
                widget.bind('<Button-1>', make_click(info['name']))

            def make_enter(b, inn, l, g):
                def handler(e):
                    b.configure(highlightbackground=Theme.PRIMARY, bg=Theme.CARD_HOVER)
                    inn.configure(bg=Theme.CARD_HOVER)
                    l.configure(bg=Theme.CARD_HOVER, fg=Theme.PRIMARY)
                    g.configure(bg=Theme.CARD_HOVER)
                return handler
            def make_leave(b, inn, l, g):
                def handler(e):
                    b.configure(highlightbackground=Theme.BORDER_LIGHT, bg=Theme.CARD)
                    inn.configure(bg=Theme.CARD)
                    l.configure(bg=Theme.CARD, fg=Theme.WHITE)
                    g.configure(bg=Theme.CARD)
                return handler

            for widget in [btn, inner, label, group_label]:
                widget.bind('<Enter>', make_enter(btn, inner, label, group_label))
                widget.bind('<Leave>', make_leave(btn, inner, label, group_label))

    def _show_detail(self, name):
        info = get_breed_info(name)

        for w in self.db_inner.winfo_children():
            w.destroy()

        if not info:
            tk.Label(self.db_inner, text=f"No information found for '{name}'",
                    font=self.F['body'], fg=Theme.MUTED, bg=Theme.BG).pack(pady=self.s(30))

            back = tk.Label(self.db_inner, text="← Back to all breeds",
                           font=self.F['body'], fg=Theme.PRIMARY, bg=Theme.BG, cursor="hand2")
            back.pack()
            back.bind('<Button-1>', lambda e: self._show_grid())
            return

        # Back
        back = tk.Label(self.db_inner, text="← Back to all breeds",
                       font=self.F['body'], fg=Theme.PRIMARY, bg=Theme.BG, cursor="hand2")
        back.pack(anchor='w', pady=(0, self.s(20)))
        back.bind('<Button-1>', lambda e: self._show_grid())

        # Detail card - use Frame instead of GlassCard to avoid sizing issues
        card = tk.Frame(self.db_inner, bg=Theme.CARD, highlightbackground=Theme.GLASS_BORDER_LIGHT, highlightthickness=1)
        card.pack(fill='x', pady=(0, self.s(20)))

        inner = tk.Frame(card, bg=Theme.CARD)
        inner.pack(fill='x', padx=self.s(40), pady=self.s(40))

        tk.Label(inner, text=info['name'], font=self.F['h1'],
                fg=Theme.PRIMARY, bg=Theme.CARD).pack(anchor='w')

        subtitle = f"{info['group']}  •  {info['origin']}  •  {info['lifespan']}"
        tk.Label(inner, text=subtitle, font=self.F['body'],
                fg=Theme.TEXT3, bg=Theme.CARD).pack(anchor='w', pady=(self.s(8), self.s(20)))

        details = [
            ("Size", f"{info['size']['weight']}, {info['size']['height']}"),
            ("Temperament", ", ".join(info['temperament'])),
            ("Exercise Needs", info['exercise']),
            ("Grooming", info['grooming']),
            ("Trainability", info['trainability']),
            ("Barking", info['barking']),
            ("Shedding", info['shedding']),
        ]

        for label, value in details:
            row = tk.Frame(inner, bg=Theme.CARD)
            row.pack(fill='x', pady=self.s(5))

            tk.Label(row, text=label, font=self.F['body_bold'], fg=Theme.AURORA_1,
                    bg=Theme.CARD, width=18, anchor='w').pack(side='left')
            tk.Label(row, text=value, font=self.F['body'], fg=Theme.TEXT,
                    bg=Theme.CARD, wraplength=self.s(500), anchor='w', justify='left').pack(side='left', fill='x')

        # Good with section
        gw = info['good_with']
        gw_frame = tk.Frame(inner, bg=Theme.CARD)
        gw_frame.pack(fill='x', pady=(self.s(15), self.s(5)))

        tk.Label(gw_frame, text="Good With", font=self.F['body_bold'], fg=Theme.AURORA_1,
                bg=Theme.CARD, width=18, anchor='w').pack(side='left')

        gw_items = []
        if gw['kids']: gw_items.append("✓ Kids")
        else: gw_items.append("✗ Kids")
        if gw['dogs']: gw_items.append("✓ Dogs")
        else: gw_items.append("✗ Dogs")
        if gw['cats']: gw_items.append("✓ Cats")
        else: gw_items.append("✗ Cats")
        if gw['strangers']: gw_items.append("✓ Strangers")
        else: gw_items.append("✗ Strangers")

        tk.Label(gw_frame, text="   ".join(gw_items), font=self.F['body'], fg=Theme.TEXT,
                bg=Theme.CARD).pack(side='left')

        # Health issues
        health_frame = tk.Frame(inner, bg=Theme.CARD)
        health_frame.pack(fill='x', pady=self.s(5))

        tk.Label(health_frame, text="Health Watch", font=self.F['body_bold'], fg=Theme.AURORA_4,
                bg=Theme.CARD, width=18, anchor='w').pack(side='left')
        tk.Label(health_frame, text=", ".join(info['health_issues'][:4]), font=self.F['body'],
                fg=Theme.TEXT, bg=Theme.CARD, wraplength=self.s(500)).pack(side='left')

        # Fun fact
        fact_frame = tk.Frame(inner, bg=Theme.BG3)
        fact_frame.pack(fill='x', pady=(self.s(20), 0))

        fact_inner = tk.Frame(fact_frame, bg=Theme.BG3)
        fact_inner.pack(fill='x', padx=self.s(15), pady=self.s(15))

        tk.Label(fact_inner, text="💡 Fun Fact", font=self.F['body_bold'],
                fg=Theme.GOLD, bg=Theme.BG3).pack(anchor='w')
        tk.Label(fact_inner, text=info['fun_fact'], font=self.F['sm'],
                fg=Theme.TEXT, bg=Theme.BG3, wraplength=self.s(600), justify='left').pack(anchor='w', pady=(self.s(5), 0))

        # Similar breeds
        similar_frame = tk.Frame(inner, bg=Theme.CARD)
        similar_frame.pack(fill='x', pady=(self.s(15), 0))

        tk.Label(similar_frame, text="Similar Breeds:", font=self.F['sm'], fg=Theme.MUTED,
                bg=Theme.CARD).pack(side='left')
        tk.Label(similar_frame, text="  " + ", ".join(info['similar_breeds']), font=self.F['sm'],
                fg=Theme.TEXT3, bg=Theme.CARD).pack(side='left')

    # ══════════════════════════════════════════════════════════════════════════
    # BREED POPUP
    # ══════════════════════════════════════════════════════════════════════════

    def _breed_popup(self, name):
        info = get_breed_info(name)
        if not info:
            messagebox.showinfo("Info", f"No detailed information for {name}")
            return

        popup = tk.Toplevel(self.root)
        popup.title(info['name'])

        pw, ph = min(self.s(580), self.w - 100), min(self.s(650), self.h - 100)
        px = self.root.winfo_x() + (self.w - pw) // 2
        py = self.root.winfo_y() + (self.h - ph) // 2

        popup.geometry(f"{pw}x{ph}+{px}+{py}")
        popup.configure(bg=Theme.BG)
        popup.transient(self.root)
        popup.grab_set()

        # Content
        content = tk.Frame(popup, bg=Theme.BG)
        content.pack(fill='both', expand=True, padx=self.s(35), pady=self.s(35))

        # Header
        tk.Label(content, text=info['name'], font=self.F['h1'],
                fg=Theme.PRIMARY, bg=Theme.BG).pack(anchor='w')

        subtitle = f"{info['group']}  •  {info['origin']}"
        tk.Label(content, text=subtitle, font=self.F['body'],
                fg=Theme.TEXT3, bg=Theme.BG).pack(anchor='w', pady=(self.s(8), self.s(30)))

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
            row.pack(fill='x', pady=self.s(7))

            tk.Label(row, text=label, font=self.F['body_bold'], fg=Theme.AURORA_1,
                    bg=Theme.BG, width=15, anchor='w').pack(side='left')
            tk.Label(row, text=value, font=self.F['body'], fg=Theme.TEXT,
                    bg=Theme.BG, wraplength=self.s(360)).pack(side='left', fill='x')

        # Fun fact
        fact_card = tk.Frame(content, bg=Theme.CARD)
        fact_card.pack(fill='x', pady=self.s(28))

        fact_inner = tk.Frame(fact_card, bg=Theme.CARD)
        fact_inner.pack(fill='x', padx=self.s(20), pady=self.s(20))

        tk.Label(fact_inner, text="💡 Fun Fact", font=self.F['body_bold'],
                fg=Theme.GOLD, bg=Theme.CARD).pack(anchor='w')
        tk.Label(fact_inner, text=info['fun_fact'], font=self.F['sm'],
                fg=Theme.TEXT, bg=Theme.CARD,
                wraplength=self.s(480), justify='left').pack(anchor='w', pady=(self.s(8), 0))

        # Buttons
        btn_frame = tk.Frame(content, bg=Theme.BG)
        btn_frame.pack(pady=self.s(25))

        search_url = f"https://www.google.com/search?tbm=isch&q={info['name'].replace(' ', '+')}+dog"

        images_btn = self.gradient_btn(btn_frame, "View Images",
                                       lambda: webbrowser.open(search_url), colors=Theme.GRAD_SECONDARY,
                                       width=self.s(160))
        images_btn.pack(side='left', padx=self.s(10))

        close_btn = self.gradient_btn(btn_frame, "Close", popup.destroy, colors=[Theme.CARD_GLOW, Theme.CARD_HOVER],
                                      width=self.s(120))
        close_btn.pack(side='left', padx=self.s(10))

    # ══════════════════════════════════════════════════════════════════════════
    # MIXED BREED DETECTION PAGE (Business Feature)
    # ══════════════════════════════════════════════════════════════════════════

    def mixed_breed_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Create scrollable container for the whole page
        scroll_container, scroll_inner = self.scrollable(self.frame)
        scroll_container.pack(fill='both', expand=True)

        # Header
        header = tk.Frame(scroll_inner, bg=Theme.BG)
        header.pack(fill='x', padx=self.s(50), pady=(self.s(30), self.s(20)))

        # Back button row
        back_row = tk.Frame(header, bg=Theme.BG)
        back_row.pack(fill='x', pady=(0, self.s(15)))
        self.back_nav(back_row).pack(side='left')

        # Pro badge
        badge = tk.Frame(back_row, bg=Theme.EMERALD)
        badge.pack(side='right')
        tk.Label(badge, text=" PRO ", font=self.F['xxs'],
                fg=Theme.BG_DARK, bg=Theme.EMERALD).pack(padx=self.s(8), pady=self.s(3))

        # Title
        tk.Label(header, text="Mixed Breed Detection", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(anchor='w')
        tk.Label(header, text="Visual breed estimation based on physical characteristics",
                font=self.F['body'], fg=Theme.TEXT3, bg=Theme.BG).pack(anchor='w', pady=(self.s(5), 0))

        # Important disclaimer banner
        disclaimer_frame = tk.Frame(header, bg=Theme.BG2, highlightbackground=Theme.ORANGE, highlightthickness=1)
        disclaimer_frame.pack(fill='x', pady=(self.s(15), 0))
        disclaimer_inner = tk.Frame(disclaimer_frame, bg=Theme.BG2)
        disclaimer_inner.pack(fill='x', padx=self.s(15), pady=self.s(12))
        tk.Label(disclaimer_inner, text="⚠️ IMPORTANT:", font=self.F['body_bold'],
                fg=Theme.ORANGE, bg=Theme.BG2).pack(anchor='w')
        tk.Label(disclaimer_inner, text="This is a VISUAL ESTIMATION only. The AI identifies breeds based on appearance,\nnot genetics. For accurate breed composition, DNA testing (Embark, Wisdom Panel) is required.",
                font=self.F['sm'], fg=Theme.TEXT3, bg=Theme.BG2, justify='left').pack(anchor='w', pady=(self.s(3), 0))

        # Main content area - two column layout
        content = tk.Frame(scroll_inner, bg=Theme.BG)
        content.pack(fill='both', expand=True, padx=self.s(50), pady=(self.s(10), self.s(40)))

        # Left side - Upload area
        left_col = tk.Frame(content, bg=Theme.BG)
        left_col.pack(side='left', fill='both', expand=True, padx=(0, self.s(15)))

        upload_card = tk.Frame(left_col, bg=Theme.CARD, padx=self.s(25), pady=self.s(25))
        upload_card.pack(fill='both', expand=True)

        tk.Label(upload_card, text="Upload Photo", font=self.F['h3'],
                fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w')
        tk.Label(upload_card, text="Select an image of your dog",
                font=self.F['sm'], fg=Theme.MUTED, bg=Theme.CARD).pack(anchor='w', pady=(self.s(5), self.s(20)))

        # Preview area - larger and more prominent
        self.mix_preview = tk.Frame(upload_card, bg=Theme.BG2, width=self.s(320), height=self.s(240))
        self.mix_preview.pack(pady=self.s(10))
        self.mix_preview.pack_propagate(False)

        preview_inner = tk.Frame(self.mix_preview, bg=Theme.BG2)
        preview_inner.pack(expand=True, fill='both', padx=self.s(3), pady=self.s(3))

        self.mix_preview_label = tk.Label(preview_inner, text="📷\n\nClick here or use\n'Browse' button below",
                                         font=self.F['body'], fg=Theme.MUTED, bg=Theme.BG2, cursor="hand2")
        self.mix_preview_label.pack(expand=True, fill='both')
        self.mix_preview_label.bind('<Button-1>', lambda e: self._mix_browse())
        self.mix_preview.bind('<Button-1>', lambda e: self._mix_browse())

        # Buttons - stacked vertically for better visibility
        btn_frame = tk.Frame(upload_card, bg=Theme.CARD)
        btn_frame.pack(fill='x', pady=(self.s(20), self.s(10)))

        browse_btn = self.gradient_btn(btn_frame, "Browse Files", self._mix_browse,
                                       colors=[Theme.TEAL, Theme.EMERALD], width=self.s(200), height=self.s(44))
        browse_btn.pack(pady=self.s(5))

        self.mix_analyze_btn = self.gradient_btn(btn_frame, "Analyze Breed Mix", self._analyze_mix,
                                                colors=Theme.GRAD_PRIMARY, width=self.s(200), height=self.s(44))
        self.mix_analyze_btn.pack(pady=self.s(5))

        # Right side - Results area
        right_col = tk.Frame(content, bg=Theme.BG)
        right_col.pack(side='right', fill='both', expand=True, padx=(self.s(15), 0))

        results_header = tk.Frame(right_col, bg=Theme.BG)
        results_header.pack(fill='x', pady=(0, self.s(10)))
        tk.Label(results_header, text="Analysis Results", font=self.F['h3'],
                fg=Theme.WHITE, bg=Theme.BG).pack(anchor='w')

        self.mix_results = tk.Frame(right_col, bg=Theme.CARD, padx=self.s(20), pady=self.s(20))
        self.mix_results.pack(fill='both', expand=True)

        # Initial placeholder
        tk.Label(self.mix_results, text="Results will appear here\nafter analysis",
                font=self.F['body'], fg=Theme.MUTED, bg=Theme.CARD, justify='center').pack(expand=True)

        self.mix_image_path = None

    def _mix_browse(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp *.gif")]
        )
        if path:
            self.mix_image_path = path
            try:
                img = Image.open(path)
                img.thumbnail((self.s(280), self.s(180)))
                photo = ImageTk.PhotoImage(img)
                self.mix_preview_label.config(image=photo, text="")
                self.mix_preview_label.image = photo
            except Exception as e:
                self.mix_preview_label.config(text=f"Error: {e}")

    def _analyze_mix(self):
        if not self.mix_image_path:
            messagebox.showwarning("Warning", "Please select an image first")
            return

        for w in self.mix_results.winfo_children():
            w.destroy()

        # Show loading
        loading = tk.Label(self.mix_results, text="🔍 Analyzing breed composition...",
                          font=self.F['body'], fg=Theme.CYAN, bg=Theme.BG)
        loading.pack(pady=self.s(30))
        self.root.update()

        # Run AI analysis
        if not self.classifier:
            from image_classifier import DogImageClassifier
            self.classifier = DogImageClassifier()

        results = self.classifier.classify_image(self.mix_image_path, top_k=5)
        loading.destroy()

        if results:
            self._show_mix_results(results)
        else:
            tk.Label(self.mix_results, text="No breeds detected. Try a clearer photo.",
                    font=self.F['body'], fg=Theme.MUTED, bg=Theme.BG).pack(pady=self.s(40))

    def _detect_mixed_breed(self, results):
        """
        Advanced mixed breed detection algorithm.

        Analyzes multiple signals to detect potential mixed breeds:
        1. Confidence distribution patterns
        2. Known breed family relationships
        3. Common mix combinations
        4. Secondary breed presence

        Returns: (is_mixed, confidence_score, detected_breeds)
        """
        if not results or len(results) < 2:
            return False, 0, []

        # Get top predictions
        top_conf = results[0]['confidence']
        top_breed = results[0]['breed'].lower()

        # All secondary breeds with any confidence
        secondary_breeds = []
        for r in results[1:]:
            secondary_breeds.append({
                'breed': r['breed'],
                'confidence': r['confidence']
            })

        # Define breed families for relationship checking
        large_breeds = {'golden retriever', 'labrador retriever', 'german shepherd',
                       'rottweiler', 'doberman', 'boxer', 'husky', 'siberian husky',
                       'australian shepherd', 'border collie', 'great dane', 'mastiff',
                       'bernese mountain dog', 'saint bernard', 'akita', 'malamute',
                       'alaskan malamute', 'newfoundland', 'great pyrenees', 'collie',
                       'kuvasz', 'leonberger', 'irish wolfhound', 'scottish deerhound',
                       'weimaraner', 'vizsla', 'rhodesian ridgeback', 'bloodhound',
                       'english setter', 'gordon setter', 'irish setter', 'pointer'}

        medium_breeds = {'beagle', 'basset hound', 'cocker spaniel', 'bulldog',
                        'english bulldog', 'french bulldog', 'poodle', 'standard poodle',
                        'shiba inu', 'chow chow', 'shetland sheepdog', 'corgi',
                        'pembroke welsh corgi', 'brittany', 'springer spaniel',
                        'american eskimo', 'keeshond', 'samoyed', 'finnish spitz'}

        small_breeds = {'chihuahua', 'pomeranian', 'yorkshire terrier', 'shih tzu',
                       'maltese', 'pug', 'boston terrier', 'dachshund', 'miniature pinscher',
                       'cavalier king charles spaniel', 'papillon', 'havanese', 'bichon frise',
                       'toy poodle', 'miniature poodle', 'lhasa apso', 'pekingese'}

        all_dog_breeds = large_breeds | medium_breeds | small_breeds

        # Common mixed breed combinations (parent breeds that often mix)
        common_mixes = {
            'golden retriever': ['labrador retriever', 'german shepherd', 'poodle', 'collie'],
            'labrador retriever': ['golden retriever', 'german shepherd', 'poodle', 'boxer'],
            'german shepherd': ['golden retriever', 'labrador retriever', 'husky', 'rottweiler', 'collie'],
            'poodle': ['golden retriever', 'labrador retriever', 'cocker spaniel', 'bernese mountain dog'],
            'husky': ['german shepherd', 'malamute', 'labrador retriever', 'australian shepherd'],
            'boxer': ['labrador retriever', 'bulldog', 'pit bull', 'german shepherd'],
            'beagle': ['labrador retriever', 'basset hound', 'dachshund', 'pug'],
            'bulldog': ['boxer', 'pug', 'french bulldog', 'boston terrier'],
        }

        # Check if breed name matches (partial matching for ImageNet labels)
        def matches_breed(name, breed_set):
            name_lower = name.lower()
            for b in breed_set:
                if b in name_lower or name_lower in b:
                    return True
                # Handle common variations
                if 'retriever' in name_lower and 'retriever' in b:
                    if 'golden' in name_lower and 'golden' in b:
                        return True
                    if 'labrador' in name_lower and 'labrador' in b:
                        return True
            return False

        def get_breed_key(name):
            """Get the standardized breed key for common_mixes lookup."""
            name_lower = name.lower()
            for key in common_mixes.keys():
                if key in name_lower or name_lower in key:
                    return key
            return None

        # DETECTION RULES:
        mix_score = 0
        detected = [results[0]['breed']]
        mix_reasons = []

        # Rule 1: Low top confidence = likely mixed
        if top_conf < 60:
            mix_score += 50
            mix_reasons.append("Low confidence indicates mixed features")
        elif top_conf < 75:
            mix_score += 35
            mix_reasons.append("Moderate confidence suggests possible mix")
        elif top_conf < 85:
            mix_score += 20
            mix_reasons.append("Some uncertainty in classification")

        # Rule 2: Check if secondary breeds are known dog breeds
        real_secondary = []
        for sb in secondary_breeds:
            if matches_breed(sb['breed'], all_dog_breeds):
                real_secondary.append(sb)

        # Rule 3: Secondary breed presence with meaningful confidence
        if real_secondary:
            best_secondary = real_secondary[0]
            if best_secondary['confidence'] > 5:
                mix_score += 40
                detected.append(best_secondary['breed'])
                mix_reasons.append(f"Strong secondary breed signal: {best_secondary['breed']}")
            elif best_secondary['confidence'] > 2:
                mix_score += 25
                detected.append(best_secondary['breed'])
                mix_reasons.append(f"Secondary breed detected: {best_secondary['breed']}")
            elif best_secondary['confidence'] > 1:
                mix_score += 15
                detected.append(best_secondary['breed'])

        # Rule 4: Check for known common mix combinations
        top_key = get_breed_key(top_breed)
        if top_key and top_key in common_mixes:
            known_partners = common_mixes[top_key]
            for sb in secondary_breeds[:5]:
                sb_lower = sb['breed'].lower()
                for partner in known_partners:
                    if partner in sb_lower or sb_lower in partner:
                        mix_score += 30
                        if sb['breed'] not in detected:
                            detected.append(sb['breed'])
                        mix_reasons.append(f"Common mix pair: {top_breed} × {partner}")
                        break

        # Rule 5: Multiple dog breeds in top results = likely mix
        dog_breed_count = sum(1 for r in results[:4] if matches_breed(r['breed'], all_dog_breeds))
        if dog_breed_count >= 3:
            mix_score += 20
            mix_reasons.append("Multiple dog breeds in predictions")

        # Rule 6: Spread confidence distribution
        if len(results) >= 3:
            conf_2_3 = results[1]['confidence'] + results[2]['confidence']
            if conf_2_3 > 10:
                mix_score += 15
                mix_reasons.append("Confidence spread across breeds")

        # Rule 7: Very high confidence with clean prediction = likely purebred
        if top_conf > 92:
            if len(real_secondary) == 0 or real_secondary[0]['confidence'] < 2:
                mix_score = max(0, mix_score - 40)
            elif real_secondary[0]['confidence'] < 5:
                mix_score = max(0, mix_score - 20)

        # Normalize score to 0-100
        mix_score = min(100, max(0, mix_score))

        # Determine if mixed (threshold: 30%)
        is_mixed = mix_score >= 30

        return is_mixed, mix_score, detected

    def _show_mix_results(self, results):
        # Results display directly in the results frame (already a card)
        inner = self.mix_results

        # Advanced mixed breed detection algorithm
        is_mixed, mix_confidence, detected_breeds = self._detect_mixed_breed(results)

        # Status indicator
        if is_mixed:
            status_frame = tk.Frame(inner, bg=Theme.BG3)
            status_frame.pack(fill='x', pady=(0, self.s(10)))

            tk.Label(status_frame, text="🔀 POSSIBLE MIX DETECTED", font=self.F['body_bold'],
                    fg=Theme.ORANGE, bg=Theme.BG3, padx=self.s(12), pady=self.s(8)).pack(side='left')

            # Show detected mix prominently
            if len(detected_breeds) >= 2:
                mix_text = " × ".join(detected_breeds[:2]) + " Mix"
                mix_frame = tk.Frame(inner, bg=Theme.BG2)
                mix_frame.pack(fill='x', pady=(0, self.s(10)))
                tk.Label(mix_frame, text="🐕", font=self.F['h3'],
                        fg=Theme.WHITE, bg=Theme.BG2, padx=self.s(10), pady=self.s(10)).pack(side='left')
                tk.Label(mix_frame, text=f"Resembles: {mix_text}", font=self.F['h3'],
                        fg=Theme.GOLD, bg=Theme.BG2, pady=self.s(10)).pack(side='left')
        else:
            status_frame = tk.Frame(inner, bg=Theme.BG3)
            status_frame.pack(fill='x', pady=(0, self.s(10)))
            tk.Label(status_frame, text="✓ APPEARS PUREBRED", font=self.F['body_bold'],
                    fg=Theme.SUCCESS, bg=Theme.BG3, padx=self.s(12), pady=self.s(8)).pack(side='left')

        # Explanation note
        note_frame = tk.Frame(inner, bg=Theme.CARD)
        note_frame.pack(fill='x', pady=(0, self.s(10)))
        tk.Label(note_frame, text="Visual similarity scores (not genetic percentages):",
                font=self.F['xs'], fg=Theme.MUTED, bg=Theme.CARD).pack(anchor='w')

        # Breed breakdown header
        tk.Label(inner, text="Breeds This Dog Resembles", font=self.F['body_bold'],
                fg=Theme.TEXT2, bg=Theme.CARD).pack(anchor='w', pady=(self.s(5), self.s(10)))

        colors = [Theme.EMERALD, Theme.TEAL, Theme.CYAN, Theme.BLUE, Theme.PURPLE]
        total_conf = sum(r['confidence'] for r in results)

        for i, result in enumerate(results):
            breed = result['breed']
            conf = result['confidence']
            pct = (conf / total_conf * 100) if total_conf > 0 else 0

            row = tk.Frame(inner, bg=Theme.CARD)
            row.pack(fill='x', pady=self.s(4))

            clr = colors[i % len(colors)]

            # Percentage first
            tk.Label(row, text=f"{pct:.0f}%", font=self.F['body_bold'],
                    fg=clr, bg=Theme.CARD, width=5, anchor='e').pack(side='left')

            # Progress bar
            bar_frame = tk.Frame(row, bg=Theme.BG2, height=self.s(16), width=self.s(100))
            bar_frame.pack(side='left', padx=self.s(10))
            bar_frame.pack_propagate(False)

            fill = tk.Frame(bar_frame, bg=clr)
            fill.place(x=0, y=0, relwidth=pct/100, relheight=1)

            # Breed name
            tk.Label(row, text=breed, font=self.F['sm'],
                    fg=Theme.WHITE, bg=Theme.CARD, anchor='w').pack(side='left', padx=(self.s(5), 0))

        # DNA testing recommendation
        dna_frame = tk.Frame(inner, bg=Theme.BG3, highlightbackground=Theme.CYAN, highlightthickness=1)
        dna_frame.pack(fill='x', pady=(self.s(15), 0))
        dna_inner = tk.Frame(dna_frame, bg=Theme.BG3)
        dna_inner.pack(fill='x', padx=self.s(12), pady=self.s(10))
        tk.Label(dna_inner, text="💡 Want accurate results?", font=self.F['sm'],
                fg=Theme.CYAN, bg=Theme.BG3).pack(anchor='w')
        tk.Label(dna_inner, text="DNA tests like Embark or Wisdom Panel can\nreveal your dog's true genetic makeup.",
                font=self.F['xs'], fg=Theme.TEXT3, bg=Theme.BG3, justify='left').pack(anchor='w', pady=(self.s(2), 0))

        # Generate report button
        btn_frame = tk.Frame(inner, bg=Theme.CARD)
        btn_frame.pack(fill='x', pady=(self.s(15), 0))

        report_btn = self.gradient_btn(btn_frame, "Save Report",
                                       lambda: self._generate_mix_report(results, is_mixed, detected_breeds),
                                       colors=[Theme.TEAL, Theme.EMERALD], width=self.s(160), height=self.s(40))
        report_btn.pack()

    def _generate_mix_report(self, results, is_mixed, detected_breeds=None):
        # Generate report content
        total_conf = sum(r['confidence'] for r in results)
        report = []
        report.append("=" * 60)
        report.append("CANINE VISUAL BREED ESTIMATION REPORT")
        report.append("=" * 60)
        report.append(f"\nDate: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append(f"Visual Assessment: {'POSSIBLE MIX' if is_mixed else 'APPEARS PUREBRED'}")

        # Show detected mix prominently
        if is_mixed and detected_breeds and len(detected_breeds) >= 2:
            mix_text = " × ".join(detected_breeds[:2])
            report.append(f"Resembles: {mix_text} Mix")

        report.append(f"\n{'─' * 40}")
        report.append("VISUAL SIMILARITY SCORES:")
        report.append("(Based on physical appearance, NOT genetics)")
        report.append(f"{'─' * 40}\n")

        for result in results:
            pct = (result['confidence'] / total_conf * 100) if total_conf > 0 else 0
            report.append(f"  • {result['breed']}: {pct:.1f}% visual similarity")

        report.append(f"\n{'─' * 40}")
        report.append("IMPORTANT DISCLAIMER:")
        report.append(f"{'─' * 40}")
        report.append("This report is based on AI visual analysis only.")
        report.append("For accurate genetic breed composition, DNA testing")
        report.append("(Embark, Wisdom Panel, etc.) is recommended.")

        report.append(f"\n{'─' * 40}")
        report.append("NOTES FOR SHELTER/RESCUE:")
        report.append(f"{'─' * 40}")

        if is_mixed:
            if detected_breeds and len(detected_breeds) >= 2:
                report.append(f"  • This dog appears to be a {detected_breeds[0]} × {detected_breeds[1]} mix")
            else:
                report.append("  • This dog appears to be a mixed breed")
            report.append("  • Behavioral traits may vary from parent breeds")
            report.append("  • Consider temperament testing for adoption matching")
            report.append("  • Size and appearance may differ from purebred standards")
        else:
            top_breed = results[0]['breed'] if results else "Unknown"
            report.append(f"  • This dog appears to be a purebred {top_breed}")
            report.append("  • Refer to breed-specific characteristics for care")

        report.append(f"\n{'=' * 60}")
        report.append("Generated by Canine Classifier Pro")
        report.append("=" * 60)

        # Save to file
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"breed_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        if filepath:
            with open(filepath, 'w') as f:
                f.write('\n'.join(report))
            messagebox.showinfo("Success", f"Report saved to:\n{filepath}")

    # ══════════════════════════════════════════════════════════════════════════
    # HEALTH RISK SCORING PAGE (Business Feature)
    # ══════════════════════════════════════════════════════════════════════════

    def health_risk_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Header
        header = tk.Frame(self.frame, bg=Theme.BG)
        header.pack(fill='x', padx=self.s(40), pady=(self.s(25), self.s(15)))

        self.back_nav(header).pack(side='left')

        tk.Label(header, text="Health Risk Scoring", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(side='left', padx=(self.s(20), 0))

        # Pro badge
        badge = tk.Frame(header, bg=Theme.CORAL)
        badge.pack(side='right')
        tk.Label(badge, text=" PRO ", font=self.F['xxs'],
                fg=Theme.BG_DARK, bg=Theme.CORAL).pack(padx=self.s(8), pady=self.s(3))

        # Content
        content = tk.Frame(self.frame, bg=Theme.BG)
        content.pack(fill='both', expand=True, padx=self.s(40), pady=(0, self.s(25)))

        # Breed selection - simple card
        select_card = tk.Frame(content, bg=Theme.CARD, highlightbackground=Theme.BORDER, highlightthickness=1)
        select_card.pack(fill='x')

        select_frame = tk.Frame(select_card, bg=Theme.CARD)
        select_frame.pack(fill='x', padx=self.s(20), pady=self.s(20))

        tk.Label(select_frame, text="🏥 Select Breed for Health Assessment",
                font=self.F['h3'], fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w')
        tk.Label(select_frame, text="Get detailed health risk scores and insurance considerations",
                font=self.F['sm'], fg=Theme.TEXT3, bg=Theme.CARD).pack(anchor='w', pady=(self.s(8), self.s(20)))

        # Breed search field
        search_frame = tk.Frame(select_frame, bg=Theme.CARD)
        search_frame.pack(fill='x', pady=self.s(10))

        # Search input container
        search_container = tk.Frame(search_frame, bg=Theme.BG3,
                                   highlightbackground=Theme.BORDER_LIGHT, highlightthickness=1)
        search_container.pack(side='left', fill='x', expand=True)

        tk.Label(search_container, text="🔍", font=self.F['body'],
                fg=Theme.MUTED, bg=Theme.BG3, padx=self.s(12)).pack(side='left')

        self.health_breed_var = tk.StringVar()
        self.health_search_entry = tk.Entry(search_container, textvariable=self.health_breed_var,
                               font=self.F['body'], bg=Theme.BG3, fg=Theme.WHITE,
                               insertbackground=Theme.WHITE, relief='flat',
                               highlightthickness=0, width=30)
        self.health_search_entry.pack(side='left', fill='x', expand=True, pady=self.s(12), padx=(0, self.s(12)))

        # Focus styling
        def on_focus_in(e):
            search_container.configure(highlightbackground=Theme.CORAL)
        def on_focus_out(e):
            search_container.configure(highlightbackground=Theme.BORDER_LIGHT)
        self.health_search_entry.bind('<FocusIn>', on_focus_in)
        self.health_search_entry.bind('<FocusOut>', on_focus_out)

        # Autocomplete dropdown
        self.health_suggestions = tk.Listbox(select_frame, bg=Theme.BG3, fg=Theme.WHITE,
                                             font=self.F['body'], height=5, relief='flat',
                                             highlightbackground=Theme.BORDER_LIGHT, highlightthickness=1,
                                             selectbackground=Theme.CORAL, selectforeground=Theme.WHITE)

        breeds = sorted([info['name'] for info in BREED_INFO.values()]) if BREED_INFO else []

        def update_suggestions(*args):
            query = self.health_breed_var.get().strip().lower()
            self.health_suggestions.delete(0, tk.END)
            if query:
                matches = [b for b in breeds if query in b.lower()][:8]
                if matches:
                    for match in matches:
                        self.health_suggestions.insert(tk.END, match)
                    self.health_suggestions.pack(fill='x', pady=(self.s(5), 0))
                else:
                    self.health_suggestions.pack_forget()
            else:
                self.health_suggestions.pack_forget()

        self.health_breed_var.trace('w', update_suggestions)

        def select_suggestion(e):
            if self.health_suggestions.curselection():
                selected = self.health_suggestions.get(self.health_suggestions.curselection())
                self.health_breed_var.set(selected)
                self.health_suggestions.pack_forget()
                self._assess_health()

        self.health_suggestions.bind('<ButtonRelease-1>', select_suggestion)
        self.health_search_entry.bind('<Return>', lambda e: self._assess_health())

        assess_btn = self.gradient_btn(search_frame, "Assess Health Risks", self._assess_health,
                                       colors=[Theme.CORAL, Theme.ROSE])
        assess_btn.pack(side='left', padx=(self.s(20), 0))

        # Results area
        self.health_results = tk.Frame(content, bg=Theme.BG)
        self.health_results.pack(fill='both', expand=True, pady=(self.s(20), 0))

    def _assess_health(self):
        breed_name = self.health_breed_var.get().strip()
        if not breed_name:
            messagebox.showwarning("Warning", "Please enter a breed name")
            return

        # Hide suggestions
        try:
            self.health_suggestions.pack_forget()
        except:
            pass

        info = get_breed_info(breed_name)
        if not info:
            messagebox.showerror("Error", f"No data for '{breed_name}'. Try typing a few letters to see suggestions.")
            return

        for w in self.health_results.winfo_children():
            w.destroy()

        # Create scrollable results
        container, inner = self.scrollable(self.health_results)
        container.pack(fill='both', expand=True)

        # Overall Risk Score Card
        score_card = self.glass_card(inner, animated=True)
        score_card.pack(fill='x', pady=(0, self.s(15)))

        score_inner = score_card.get_content_frame()
        score_frame = tk.Frame(score_inner, bg=Theme.CARD)
        score_frame.pack(fill='x', padx=self.s(30), pady=self.s(30))

        # Calculate risk score based on health issues and lifespan
        health_issues = info.get('health_issues', [])
        lifespan = info.get('lifespan', '10-12 years')

        # Parse lifespan for scoring
        try:
            lifespan_low = int(lifespan.split('-')[0].split()[0])
        except:
            lifespan_low = 10

        # Risk calculation
        issue_risk = min(len(health_issues) * 12, 60)  # Up to 60 points for issues
        lifespan_risk = max(0, (12 - lifespan_low) * 8)  # Short lifespan adds risk
        total_risk = min(issue_risk + lifespan_risk, 100)

        # Risk level
        if total_risk < 30:
            risk_level = "LOW"
            risk_color = Theme.SUCCESS
        elif total_risk < 60:
            risk_level = "MODERATE"
            risk_color = Theme.ORANGE
        else:
            risk_level = "HIGH"
            risk_color = Theme.RED

        # Display score
        tk.Label(score_frame, text=f"Overall Health Risk Score: {info['name']}",
                font=self.F['h3'], fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w')

        score_display = tk.Frame(score_frame, bg=Theme.CARD)
        score_display.pack(fill='x', pady=self.s(20))

        # Big score number
        tk.Label(score_display, text=f"{total_risk}", font=('Segoe UI', 48, 'bold'),
                fg=risk_color, bg=Theme.CARD).pack(side='left')

        tk.Label(score_display, text=f"/100\n{risk_level} RISK", font=self.F['body_bold'],
                fg=risk_color, bg=Theme.CARD).pack(side='left', padx=self.s(10))

        # Risk bar
        bar_frame = tk.Frame(score_frame, bg=Theme.BG3, height=self.s(20))
        bar_frame.pack(fill='x', pady=self.s(10))
        bar_frame.pack_propagate(False)

        fill = tk.Frame(bar_frame, bg=risk_color)
        fill.place(x=0, y=0, relwidth=total_risk/100, relheight=1)

        # Insurance implications
        tk.Label(score_frame, text="📋 Insurance Implications:", font=self.F['body_bold'],
                fg=Theme.TEXT2, bg=Theme.CARD).pack(anchor='w', pady=(self.s(15), self.s(8)))

        if total_risk < 30:
            insurance_text = "• Standard rates likely applicable\n• No breed-specific exclusions expected\n• May qualify for wellness discounts"
        elif total_risk < 60:
            insurance_text = "• Moderate premium adjustments possible\n• Some conditions may have waiting periods\n• Pre-existing condition review recommended"
        else:
            insurance_text = "• Higher premiums likely\n• Breed-specific exclusions may apply\n• Comprehensive coverage strongly recommended"

        tk.Label(score_frame, text=insurance_text, font=self.F['sm'],
                fg=Theme.TEXT3, bg=Theme.CARD, justify='left').pack(anchor='w')

        # Health Issues Card
        issues_card = self.glass_card(inner, animated=True)
        issues_card.pack(fill='x', pady=self.s(15))

        issues_inner = issues_card.get_content_frame()
        issues_frame = tk.Frame(issues_inner, bg=Theme.CARD)
        issues_frame.pack(fill='x', padx=self.s(30), pady=self.s(30))

        tk.Label(issues_frame, text="⚠️ Known Health Concerns", font=self.F['h3'],
                fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w', pady=(0, self.s(15)))

        if health_issues:
            for issue in health_issues:
                row = tk.Frame(issues_frame, bg=Theme.BG3)
                row.pack(fill='x', pady=self.s(4))

                tk.Label(row, text=f"  •  {issue}", font=self.F['body'],
                        fg=Theme.TEXT, bg=Theme.BG3, anchor='w').pack(fill='x', padx=self.s(10), pady=self.s(8))
        else:
            tk.Label(issues_frame, text="No known breed-specific health issues",
                    font=self.F['body'], fg=Theme.SUCCESS, bg=Theme.CARD).pack(anchor='w')

        # Care Recommendations Card
        care_card = self.glass_card(inner, animated=True)
        care_card.pack(fill='x', pady=self.s(15))

        care_inner = care_card.get_content_frame()
        care_frame = tk.Frame(care_inner, bg=Theme.CARD)
        care_frame.pack(fill='x', padx=self.s(30), pady=self.s(30))

        tk.Label(care_frame, text="💊 Veterinary Care Recommendations", font=self.F['h3'],
                fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w', pady=(0, self.s(15)))

        recommendations = [
            f"Expected Lifespan: {info['lifespan']}",
            f"Exercise Needs: {info.get('exercise', 'Moderate')}",
            f"Grooming Level: {info.get('grooming', 'Moderate')}",
        ]

        for rec in recommendations:
            tk.Label(care_frame, text=f"  •  {rec}", font=self.F['body'],
                    fg=Theme.TEXT, bg=Theme.CARD, anchor='w').pack(fill='x')

        # Generate report button
        btn_frame = tk.Frame(inner, bg=Theme.BG)
        btn_frame.pack(pady=self.s(20))

        report_btn = self.gradient_btn(btn_frame, "Generate Health Report",
                                       lambda: self._generate_health_report(info, total_risk, risk_level),
                                       colors=[Theme.CORAL, Theme.ROSE])
        report_btn.pack()

    def _generate_health_report(self, info, risk_score, risk_level):
        """Generate health report - PDF if available, otherwise text."""
        if PDF_AVAILABLE:
            self._generate_health_pdf(info, risk_score, risk_level)
        else:
            self._generate_health_txt(info, risk_score, risk_level)

    def _generate_health_pdf(self, info, risk_score, risk_level):
        """Generate professional PDF health report using reportlab."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=f"health_report_{info['name'].replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d')}.pdf"
        )

        if not filepath:
            return

        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.lib import colors

        doc = SimpleDocTemplate(filepath, pagesize=letter,
                               rightMargin=0.75*inch, leftMargin=0.75*inch,
                               topMargin=0.75*inch, bottomMargin=0.75*inch)

        styles = getSampleStyleSheet()
        story = []

        # Custom styles
        title_style = ParagraphStyle('Title', parent=styles['Heading1'],
                                     fontSize=20, alignment=1, spaceAfter=6,
                                     fontName='Helvetica-Bold')
        subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'],
                                        fontSize=10, alignment=1, textColor=colors.gray)
        section_style = ParagraphStyle('Section', parent=styles['Heading2'],
                                       fontSize=14, fontName='Helvetica-Bold',
                                       spaceBefore=16, spaceAfter=8,
                                       backColor=colors.Color(0.94, 0.94, 0.94))
        label_style = ParagraphStyle('Label', parent=styles['Normal'],
                                     fontSize=10, fontName='Helvetica-Bold')
        value_style = ParagraphStyle('Value', parent=styles['Normal'], fontSize=10)
        alert_style = ParagraphStyle('Alert', parent=styles['Normal'],
                                     fontSize=9, fontStyle='italic', textColor=colors.gray)

        # Header
        story.append(Paragraph("CANINE HEALTH RISK ASSESSMENT", title_style))
        story.append(Paragraph("Professional Veterinary & Insurance Report", subtitle_style))
        story.append(Spacer(1, 8))

        # Report info
        report_id = f"HR-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        report_date = datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p')
        info_data = [
            ['Report ID:', report_id, 'Date:', report_date]
        ]
        info_table = Table(info_data, colWidths=[1*inch, 2*inch, 0.8*inch, 2.5*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.gray),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 6))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
        story.append(Spacer(1, 12))

        # Breed Information Section
        story.append(Paragraph("BREED INFORMATION", section_style))
        breed_data = [
            ['Breed:', info['name']],
            ['Group:', info.get('group', 'N/A')],
            ['Origin:', info.get('origin', 'N/A')],
            ['Size:', f"{info.get('size', {}).get('weight', 'N/A')} / {info.get('size', {}).get('height', 'N/A')}"],
            ['Expected Lifespan:', info.get('lifespan', 'N/A')],
        ]
        breed_table = Table(breed_data, colWidths=[1.8*inch, 5*inch])
        breed_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BACKGROUND', (0, 0), (0, -1), colors.Color(0.97, 0.97, 0.97)),
        ]))
        story.append(breed_table)
        story.append(Spacer(1, 16))

        # Risk Assessment Section
        story.append(Paragraph("OVERALL RISK ASSESSMENT", section_style))

        # Determine risk color
        if risk_score < 30:
            risk_color = colors.green
        elif risk_score < 60:
            risk_color = colors.orange
        else:
            risk_color = colors.red

        risk_data = [
            ['Risk Score:', f'{risk_score}/100', 'Risk Level:', risk_level]
        ]
        risk_table = Table(risk_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
        risk_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('FONTSIZE', (1, 0), (1, 0), 16),
            ('FONTSIZE', (3, 0), (3, 0), 14),
            ('TEXTCOLOR', (1, 0), (1, 0), risk_color),
            ('TEXTCOLOR', (3, 0), (3, 0), risk_color),
            ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (3, 0), (3, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(risk_table)
        story.append(Spacer(1, 16))

        # Health Concerns Section
        story.append(Paragraph("KNOWN HEALTH CONCERNS", section_style))
        health_issues = info.get('health_issues', [])
        if health_issues:
            for issue in health_issues:
                story.append(Paragraph(f"&bull; {issue}", value_style))
                story.append(Spacer(1, 4))
        else:
            story.append(Paragraph("No known breed-specific health issues documented.", value_style))
        story.append(Spacer(1, 12))

        # Care Requirements Section
        story.append(Paragraph("CARE REQUIREMENTS", section_style))
        care_data = [
            ['Exercise Needs:', info.get('exercise', 'N/A')],
            ['Grooming Level:', info.get('grooming', 'N/A')],
            ['Shedding:', info.get('shedding', 'N/A')],
            ['Trainability:', info.get('trainability', 'N/A')],
        ]
        care_table = Table(care_data, colWidths=[1.8*inch, 5*inch])
        care_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BACKGROUND', (0, 0), (0, -1), colors.Color(0.97, 0.97, 0.97)),
        ]))
        story.append(care_table)
        story.append(Spacer(1, 16))

        # Insurance Considerations Section
        story.append(Paragraph("INSURANCE CONSIDERATIONS", section_style))
        if risk_score < 30:
            insurance_points = [
                "Standard insurance rates likely applicable",
                "No breed-specific exclusions expected",
                "May qualify for wellness program discounts",
                "Low likelihood of claim denials based on breed"
            ]
        elif risk_score < 60:
            insurance_points = [
                "Moderate premium adjustments possible",
                "Some conditions may have waiting periods",
                "Pre-existing condition review recommended",
                "Consider comprehensive coverage options"
            ]
        else:
            insurance_points = [
                "Higher premiums likely due to breed risk factors",
                "Breed-specific exclusions may apply",
                "Comprehensive coverage strongly recommended",
                "Consider breed-specific policy options",
                "Early enrollment recommended to establish coverage"
            ]

        for point in insurance_points:
            story.append(Paragraph(f"&bull; {point}", value_style))
            story.append(Spacer(1, 4))
        story.append(Spacer(1, 16))

        # Footer
        story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
        story.append(Spacer(1, 8))
        story.append(Paragraph("Generated by Canine Classifier Pro - Health Assessment Module", alert_style))
        story.append(Paragraph("For veterinary and insurance professional use. This report is based on breed-typical characteristics and should be used as a reference only. Individual dogs may vary.", alert_style))

        doc.build(story)
        messagebox.showinfo("Success", f"Health report PDF saved to:\n{filepath}")

    def _generate_health_txt(self, info, risk_score, risk_level):
        """Generate text health report as fallback."""
        report = []
        report.append("=" * 60)
        report.append("CANINE HEALTH RISK ASSESSMENT REPORT")
        report.append("=" * 60)
        report.append(f"\nDate: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append(f"Breed: {info['name']}")
        report.append(f"Group: {info['group']}")
        report.append(f"\n{'─' * 40}")
        report.append("OVERALL RISK ASSESSMENT:")
        report.append(f"{'─' * 40}")
        report.append(f"\n  Risk Score: {risk_score}/100")
        report.append(f"  Risk Level: {risk_level}")
        report.append(f"  Expected Lifespan: {info['lifespan']}")
        report.append(f"\n{'─' * 40}")
        report.append("KNOWN HEALTH CONCERNS:")
        report.append(f"{'─' * 40}\n")

        for issue in info.get('health_issues', ['None documented']):
            report.append(f"  * {issue}")

        report.append(f"\n{'─' * 40}")
        report.append("CARE REQUIREMENTS:")
        report.append(f"{'─' * 40}")
        report.append(f"\n  Exercise: {info.get('exercise', 'N/A')}")
        report.append(f"  Grooming: {info.get('grooming', 'N/A')}")

        report.append(f"\n{'─' * 40}")
        report.append("INSURANCE CONSIDERATIONS:")
        report.append(f"{'─' * 40}")

        if risk_score < 30:
            report.append("\n  * Low risk - Standard rates expected")
            report.append("  * Minimal breed-specific exclusions")
        elif risk_score < 60:
            report.append("\n  * Moderate risk - Some premium adjustment possible")
            report.append("  * Review for condition-specific waiting periods")
        else:
            report.append("\n  * High risk - Increased premiums likely")
            report.append("  * Comprehensive coverage recommended")
            report.append("  * Consider breed-specific policy options")

        report.append(f"\n{'=' * 60}")
        report.append("Generated by Canine Classifier Pro - Health Module")
        report.append("For veterinary and insurance professional use")
        report.append("=" * 60)

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"health_report_{info['name'].replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d')}.txt"
        )

        if filepath:
            with open(filepath, 'w') as f:
                f.write('\n'.join(report))
            messagebox.showinfo("Success", f"Health report saved to:\n{filepath}")

    # ══════════════════════════════════════════════════════════════════════════
    # INTAKE FORM GENERATOR PAGE (Business Feature)
    # ══════════════════════════════════════════════════════════════════════════

    def intake_form_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Header
        header = tk.Frame(self.frame, bg=Theme.BG)
        header.pack(fill='x', padx=self.s(40), pady=(self.s(25), self.s(15)))

        self.back_nav(header).pack(side='left')

        tk.Label(header, text="Intake Forms", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(side='left', padx=(self.s(20), 0))

        # Pro badge
        badge = tk.Frame(header, bg=Theme.BLUE)
        badge.pack(side='right')
        tk.Label(badge, text=" PRO ", font=self.F['xxs'],
                fg=Theme.WHITE, bg=Theme.BLUE).pack(padx=self.s(8), pady=self.s(3))

        # Content - scrollable
        content = tk.Frame(self.frame, bg=Theme.BG)
        content.pack(fill='both', expand=True, padx=self.s(40), pady=(0, self.s(25)))

        container, inner = self.scrollable(content)
        container.pack(fill='both', expand=True)

        # Form Type Selection - simple card
        type_card = tk.Frame(inner, bg=Theme.CARD, highlightbackground=Theme.BORDER, highlightthickness=1)
        type_card.pack(fill='x', pady=(0, self.s(10)))

        type_frame = tk.Frame(type_card, bg=Theme.CARD)
        type_frame.pack(fill='x', padx=self.s(20), pady=self.s(20))

        tk.Label(type_frame, text="📄 Select Form Type", font=self.F['h3'],
                fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w', pady=(0, self.s(15)))

        self.form_type_var = tk.StringVar(value="shelter")

        form_types = [
            ("shelter", "🏠 Shelter/Rescue Intake", "Complete intake form for animal shelters and rescues"),
            ("groomer", "✂️ Grooming Intake", "Professional grooming salon intake form"),
            ("vet", "🏥 Veterinary Intake", "New patient intake for veterinary clinics"),
            ("boarding", "🏨 Boarding/Daycare", "Pet boarding and daycare intake form"),
        ]

        for value, title, desc in form_types:
            radio_frame = tk.Frame(type_frame, bg=Theme.BG3, cursor="hand2")
            radio_frame.pack(fill='x', pady=self.s(5))

            rb = tk.Radiobutton(radio_frame, text=title, variable=self.form_type_var, value=value,
                               font=self.F['body_bold'], fg=Theme.WHITE, bg=Theme.BG3,
                               selectcolor=Theme.BG4, activebackground=Theme.BG3,
                               activeforeground=Theme.PRIMARY, cursor="hand2")
            rb.pack(side='left', padx=self.s(15), pady=self.s(12))

            tk.Label(radio_frame, text=desc, font=self.F['xs'],
                    fg=Theme.TEXT3, bg=Theme.BG3).pack(side='left')

        # Dog Information - simple card
        info_card = tk.Frame(inner, bg=Theme.CARD, highlightbackground=Theme.BORDER, highlightthickness=1)
        info_card.pack(fill='x', pady=self.s(10))

        info_frame = tk.Frame(info_card, bg=Theme.CARD)
        info_frame.pack(fill='x', padx=self.s(20), pady=self.s(20))

        tk.Label(info_frame, text="🐕 Dog Information", font=self.F['h3'],
                fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w', pady=(0, self.s(15)))

        # Form fields
        self.intake_fields = {}
        fields = [
            ("dog_name", "Dog's Name"),
            ("breed", "Breed (or select below)"),
            ("age", "Age"),
            ("weight", "Weight (lbs)"),
            ("color", "Color/Markings"),
            ("sex", "Sex (M/F/Neutered/Spayed)"),
        ]

        for key, label in fields:
            row = tk.Frame(info_frame, bg=Theme.CARD)
            row.pack(fill='x', pady=self.s(6))

            tk.Label(row, text=label, font=self.F['body'],
                    fg=Theme.TEXT2, bg=Theme.CARD, width=20, anchor='w').pack(side='left')

            entry = tk.Entry(row, font=self.F['body'], bg=Theme.BG4, fg=Theme.WHITE,
                           insertbackground=Theme.WHITE, relief='flat', width=30)
            entry.pack(side='left', padx=self.s(10), ipady=self.s(8))
            self.intake_fields[key] = entry

        # Breed selector
        breed_row = tk.Frame(info_frame, bg=Theme.CARD)
        breed_row.pack(fill='x', pady=self.s(10))

        tk.Label(breed_row, text="Or select from database:", font=self.F['body'],
                fg=Theme.TEXT3, bg=Theme.CARD).pack(side='left')

        breeds = sorted([info['name'] for info in BREED_INFO.values()]) if BREED_INFO else []
        self.intake_breed_var = tk.StringVar(value="-- Select Breed --")
        breed_dropdown = ModernDropdown(breed_row, values=["-- Select Breed --"] + breeds,
                                        textvariable=self.intake_breed_var, width=self.s(250))
        breed_dropdown.pack(side='left', padx=self.s(15))

        # Owner Information
        owner_card = self.glass_card(inner, animated=True)
        owner_card.pack(fill='x', pady=self.s(15))

        owner_inner = owner_card.get_content_frame()
        owner_frame = tk.Frame(owner_inner, bg=Theme.CARD)
        owner_frame.pack(fill='x', padx=self.s(30), pady=self.s(30))

        tk.Label(owner_frame, text="👤 Owner/Contact Information", font=self.F['h3'],
                fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w', pady=(0, self.s(15)))

        owner_fields = [
            ("owner_name", "Owner Name"),
            ("phone", "Phone Number"),
            ("email", "Email Address"),
            ("address", "Address"),
            ("emergency_contact", "Emergency Contact"),
        ]

        for key, label in owner_fields:
            row = tk.Frame(owner_frame, bg=Theme.CARD)
            row.pack(fill='x', pady=self.s(6))

            tk.Label(row, text=label, font=self.F['body'],
                    fg=Theme.TEXT2, bg=Theme.CARD, width=20, anchor='w').pack(side='left')

            entry = tk.Entry(row, font=self.F['body'], bg=Theme.BG4, fg=Theme.WHITE,
                           insertbackground=Theme.WHITE, relief='flat', width=30)
            entry.pack(side='left', padx=self.s(10), ipady=self.s(8))
            self.intake_fields[key] = entry

        # Generate button
        btn_frame = tk.Frame(inner, bg=Theme.BG)
        btn_frame.pack(pady=self.s(25))

        generate_btn = self.gradient_btn(btn_frame, "Generate Intake Form", self._generate_intake_form,
                                        colors=[Theme.BLUE, Theme.INDIGO], width=self.s(250))
        generate_btn.pack()

    def _generate_intake_form(self):
        form_type = self.form_type_var.get()

        # Get field values
        data = {}
        for key, entry in self.intake_fields.items():
            data[key] = entry.get().strip() or ""

        # Check if breed selected from dropdown
        selected_breed = self.intake_breed_var.get()
        if not selected_breed.startswith('--') and not data['breed']:
            data['breed'] = selected_breed

        # Get breed info if available
        breed_info = get_breed_info(data['breed']) if data['breed'] else None

        date = datetime.datetime.now().strftime('%Y-%m-%d')

        # Save form as PDF
        type_names = {"shelter": "Shelter_Intake", "groomer": "Grooming_Intake",
                     "vet": "Veterinary_Intake", "boarding": "Boarding_Intake"}
        type_titles = {"shelter": "ANIMAL SHELTER INTAKE FORM",
                      "groomer": "PROFESSIONAL GROOMING INTAKE FORM",
                      "vet": "VETERINARY PATIENT INTAKE FORM",
                      "boarding": "PET BOARDING/DAYCARE INTAKE FORM"}

        if PDF_AVAILABLE:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile=f"{type_names[form_type]}_{date}.pdf"
            )
            if filepath:
                self._generate_pdf_form(filepath, form_type, type_titles[form_type], data, breed_info, date)
                messagebox.showinfo("Success", f"Professional PDF form saved to:\n{filepath}")
        else:
            # Fallback to text if reportlab not available
            form = []
            if form_type == "shelter":
                form = self._shelter_form(data, breed_info, date)
            elif form_type == "groomer":
                form = self._groomer_form(data, breed_info, date)
            elif form_type == "vet":
                form = self._vet_form(data, breed_info, date)
            elif form_type == "boarding":
                form = self._boarding_form(data, breed_info, date)

            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=f"{type_names[form_type]}_{date}.txt"
            )
            if filepath:
                with open(filepath, 'w') as f:
                    f.write('\n'.join(form))
                messagebox.showinfo("Success", f"Intake form saved to:\n{filepath}")

    def _generate_pdf_form(self, filepath, form_type, title, data, breed_info, date):
        """Generate a professional black and white PDF intake form."""
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                               topMargin=0.5*inch, bottomMargin=0.5*inch,
                               leftMargin=0.75*inch, rightMargin=0.75*inch)

        # Define styles
        styles = getSampleStyleSheet()

        # Custom styles for professional look
        title_style = ParagraphStyle('Title', parent=styles['Heading1'],
                                     fontSize=18, alignment=TA_CENTER,
                                     spaceAfter=6, textColor=black,
                                     fontName='Helvetica-Bold')

        subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'],
                                        fontSize=10, alignment=TA_CENTER,
                                        spaceAfter=20, textColor=gray)

        section_style = ParagraphStyle('Section', parent=styles['Heading2'],
                                       fontSize=12, spaceBefore=15, spaceAfter=8,
                                       textColor=black, fontName='Helvetica-Bold',
                                       borderWidth=1, borderColor=black,
                                       borderPadding=5, backColor=HexColor('#f0f0f0'))

        label_style = ParagraphStyle('Label', parent=styles['Normal'],
                                     fontSize=10, textColor=black,
                                     fontName='Helvetica-Bold')

        value_style = ParagraphStyle('Value', parent=styles['Normal'],
                                     fontSize=10, textColor=black)

        small_style = ParagraphStyle('Small', parent=styles['Normal'],
                                     fontSize=9, textColor=gray)

        alert_style = ParagraphStyle('Alert', parent=styles['Normal'],
                                     fontSize=9, textColor=black,
                                     fontName='Helvetica-Oblique',
                                     leftIndent=20)

        # Build content
        content = []

        # Header
        content.append(Paragraph(title, title_style))
        form_id = f"{form_type.upper()[:3]}-{datetime.datetime.now().strftime('%Y%m%d%H%M')}"
        content.append(Paragraph(f"Form ID: {form_id}  |  Date: {date}", subtitle_style))
        content.append(HRFlowable(width="100%", thickness=2, color=black, spaceAfter=15))

        # Helper to create form field rows
        def field_row(label, value, width1=2*inch, width2=4.5*inch):
            return [Paragraph(f"<b>{label}:</b>", label_style),
                    Paragraph(value if value else "_" * 40, value_style)]

        def make_table(rows, col_widths=[2*inch, 4.5*inch]):
            t = Table(rows, colWidths=col_widths)
            t.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
            ]))
            return t

        def checkbox(text, checked=False):
            box = "[X]" if checked else "[  ]"
            return f"{box} {text}"

        # Form-specific content
        if form_type == "shelter":
            # Owner/Previous Owner Section
            content.append(Paragraph("PREVIOUS OWNER INFORMATION", section_style))
            rows = [
                field_row("Owner Name", data.get('owner_name', '')),
                field_row("Phone", data.get('phone', '')),
                field_row("Address", data.get('address', '')),
            ]
            content.append(make_table(rows))

            # Animal Information
            content.append(Paragraph("ANIMAL INFORMATION", section_style))
            rows = [
                field_row("Animal Name", data.get('dog_name', '')),
                field_row("Species", "Canine"),
                field_row("Breed", data.get('breed', '')),
                field_row("Age", data.get('age', '')),
                field_row("Weight", f"{data.get('weight', '')} lbs" if data.get('weight') else ''),
                field_row("Sex", data.get('sex', '')),
                field_row("Color/Markings", data.get('color', '')),
            ]
            content.append(make_table(rows))

            if breed_info:
                content.append(Paragraph("BREED DATABASE INFORMATION", section_style))
                rows = [
                    field_row("Breed Group", breed_info.get('group', '')),
                    field_row("Expected Size", breed_info.get('size', {}).get('weight', '')),
                    field_row("Typical Temperament", ', '.join(breed_info.get('temperament', [])[:3])),
                    field_row("Expected Lifespan", breed_info.get('lifespan', '')),
                ]
                content.append(make_table(rows))

                if breed_info.get('health_issues'):
                    content.append(Paragraph("<b>Breed Health Alerts:</b>", label_style))
                    for issue in breed_info['health_issues'][:4]:
                        content.append(Paragraph(f"- {issue}", alert_style))
                    content.append(Spacer(1, 10))

            # Intake Circumstances
            content.append(Paragraph("INTAKE CIRCUMSTANCES", section_style))
            content.append(Paragraph(f"{checkbox('Stray')}    {checkbox('Surrender')}    {checkbox('Transfer')}    {checkbox('Other')}", value_style))
            content.append(Spacer(1, 8))
            content.append(make_table([field_row("Location Found", ""), field_row("Surrender Reason", "")]))

            # Assessment
            content.append(Paragraph("INITIAL ASSESSMENT", section_style))
            content.append(Paragraph(f"Body Condition Score (1-9): _____", value_style))
            content.append(Spacer(1, 6))
            content.append(Paragraph(f"Temperament: {checkbox('Friendly')}  {checkbox('Shy')}  {checkbox('Fearful')}  {checkbox('Aggressive')}", value_style))
            content.append(Spacer(1, 6))
            content.append(Paragraph(f"Vaccinations: {checkbox('Unknown')}  {checkbox('Up to Date')}  {checkbox('Needed')}", value_style))
            content.append(Spacer(1, 6))
            content.append(Paragraph(f"Spay/Neuter: {checkbox('Yes')}  {checkbox('No')}  {checkbox('Unknown')}", value_style))
            content.append(Spacer(1, 6))
            content.append(Paragraph(f"Microchip: {checkbox('Yes')} #____________  {checkbox('No')}  {checkbox('Check Needed')}", value_style))

        elif form_type == "groomer":
            # Client Information
            content.append(Paragraph("CLIENT INFORMATION", section_style))
            rows = [
                field_row("Client Name", data.get('owner_name', '')),
                field_row("Phone", data.get('phone', '')),
                field_row("Email", data.get('email', '')),
                field_row("Address", data.get('address', '')),
                field_row("Emergency Contact", data.get('emergency_contact', '')),
            ]
            content.append(make_table(rows))

            # Pet Information
            content.append(Paragraph("PET INFORMATION", section_style))
            rows = [
                field_row("Pet Name", data.get('dog_name', '')),
                field_row("Breed", data.get('breed', '')),
                field_row("Age", data.get('age', '')),
                field_row("Weight", f"{data.get('weight', '')} lbs" if data.get('weight') else ''),
                field_row("Color", data.get('color', '')),
            ]
            content.append(make_table(rows))

            if breed_info:
                content.append(Paragraph("BREED-SPECIFIC GROOMING NOTES", section_style))
                rows = [
                    field_row("Grooming Needs", breed_info.get('grooming', '')),
                    field_row("Shedding Level", breed_info.get('shedding', '')),
                    field_row("Coat Type", breed_info.get('size', {}).get('weight', 'Standard')),
                ]
                content.append(make_table(rows))

            # Services
            content.append(Paragraph("SERVICES REQUESTED", section_style))
            content.append(Paragraph(f"{checkbox('Full Groom')}    {checkbox('Bath & Brush')}    {checkbox('Nail Trim')}    {checkbox('Ear Clean')}", value_style))
            content.append(Spacer(1, 6))
            content.append(Paragraph(f"{checkbox('Teeth Brushing')}    {checkbox('De-shedding')}    {checkbox('Breed Cut')}    {checkbox('Puppy Cut')}", value_style))
            content.append(Spacer(1, 8))
            content.append(make_table([field_row("Special Requests", "")]))

            # Health
            content.append(Paragraph("HEALTH & BEHAVIOR", section_style))
            content.append(Paragraph(f"Vaccinations Current: {checkbox('Yes')}  {checkbox('No')} (Required for service)", value_style))
            content.append(Spacer(1, 6))
            content.append(make_table([
                field_row("Allergies/Sensitivities", ""),
                field_row("Skin Conditions", ""),
            ]))
            content.append(Paragraph(f"Behavior: {checkbox('Good')}  {checkbox('Nervous')}  {checkbox('Needs Muzzle')}", value_style))

        elif form_type == "vet":
            # Owner Information
            content.append(Paragraph("OWNER INFORMATION", section_style))
            rows = [
                field_row("Owner Name", data.get('owner_name', '')),
                field_row("Phone", data.get('phone', '')),
                field_row("Email", data.get('email', '')),
                field_row("Address", data.get('address', '')),
                field_row("Emergency Contact", data.get('emergency_contact', '')),
            ]
            content.append(make_table(rows))

            # Patient Information
            content.append(Paragraph("PATIENT INFORMATION", section_style))
            rows = [
                field_row("Patient Name", data.get('dog_name', '')),
                field_row("Species", "Canine"),
                field_row("Breed", data.get('breed', '')),
                field_row("Age", data.get('age', '')),
                field_row("Weight", f"{data.get('weight', '')} lbs" if data.get('weight') else ''),
                field_row("Sex", data.get('sex', '')),
                field_row("Color/Markings", data.get('color', '')),
            ]
            content.append(make_table(rows))

            if breed_info:
                content.append(Paragraph("BREED-SPECIFIC MEDICAL CONSIDERATIONS", section_style))
                rows = [
                    field_row("Breed Group", breed_info.get('group', '')),
                    field_row("Expected Lifespan", breed_info.get('lifespan', '')),
                ]
                content.append(make_table(rows))

                if breed_info.get('health_issues'):
                    content.append(Paragraph("<b>Known Breed Health Concerns:</b>", label_style))
                    for issue in breed_info['health_issues']:
                        content.append(Paragraph(f"- {issue}", alert_style))
                    content.append(Spacer(1, 10))

            # Medical History
            content.append(Paragraph("MEDICAL HISTORY", section_style))
            content.append(Paragraph(f"Spayed/Neutered: {checkbox('Yes')}  {checkbox('No')}  Date: __________", value_style))
            content.append(Spacer(1, 6))
            content.append(make_table([
                field_row("Previous Veterinarian", ""),
                field_row("Current Medications", ""),
                field_row("Known Allergies", ""),
                field_row("Previous Surgeries", ""),
            ]))

            # Vaccinations
            content.append(Paragraph("VACCINATION RECORD", section_style))
            content.append(Paragraph(f"Rabies: {checkbox('Current')} Date: ________ {checkbox('Needed')}", value_style))
            content.append(Spacer(1, 4))
            content.append(Paragraph(f"DHPP: {checkbox('Current')} Date: ________ {checkbox('Needed')}", value_style))
            content.append(Spacer(1, 4))
            content.append(Paragraph(f"Bordetella: {checkbox('Current')} Date: ________ {checkbox('Needed')}", value_style))
            content.append(Spacer(1, 4))
            content.append(Paragraph(f"Heartworm Test: {checkbox('Current')} Date: ________ {checkbox('Needed')}", value_style))

            # Reason for Visit
            content.append(Paragraph("REASON FOR VISIT", section_style))
            content.append(Paragraph(f"{checkbox('Wellness Exam')}  {checkbox('Sick Visit')}  {checkbox('Vaccination')}  {checkbox('Injury')}  {checkbox('Follow-up')}  {checkbox('Emergency')}", value_style))
            content.append(Spacer(1, 8))
            content.append(Paragraph("<b>Description of Concern:</b>", label_style))
            content.append(Paragraph("_" * 80, value_style))
            content.append(Paragraph("_" * 80, value_style))

        elif form_type == "boarding":
            # Owner Information
            content.append(Paragraph("OWNER INFORMATION", section_style))
            rows = [
                field_row("Owner Name", data.get('owner_name', '')),
                field_row("Phone", data.get('phone', '')),
                field_row("Email", data.get('email', '')),
                field_row("Address", data.get('address', '')),
                field_row("Emergency Contact", data.get('emergency_contact', '')),
            ]
            content.append(make_table(rows))

            # Pet Information
            content.append(Paragraph("PET INFORMATION", section_style))
            rows = [
                field_row("Pet Name", data.get('dog_name', '')),
                field_row("Breed", data.get('breed', '')),
                field_row("Age", data.get('age', '')),
                field_row("Weight", f"{data.get('weight', '')} lbs" if data.get('weight') else ''),
                field_row("Sex", data.get('sex', '')),
                field_row("Color", data.get('color', '')),
            ]
            content.append(make_table(rows))

            if breed_info:
                content.append(Paragraph("BREED-SPECIFIC CARE NOTES", section_style))
                rows = [
                    field_row("Exercise Needs", breed_info.get('exercise', '')),
                    field_row("Good with Dogs", 'Yes' if breed_info.get('good_with', {}).get('dogs') else 'Monitor closely'),
                    field_row("Temperament", ', '.join(breed_info.get('temperament', [])[:2])),
                ]
                content.append(make_table(rows))

            # Stay Details
            content.append(Paragraph("STAY DETAILS", section_style))
            content.append(make_table([
                field_row("Check-in Date/Time", ""),
                field_row("Check-out Date/Time", ""),
            ]))
            content.append(Paragraph(f"Service Type: {checkbox('Boarding')}  {checkbox('Daycare')}  {checkbox('Both')}", value_style))

            # Feeding
            content.append(Paragraph("FEEDING INSTRUCTIONS", section_style))
            content.append(make_table([
                field_row("Food Brand", ""),
                field_row("Amount per Meal", ""),
                field_row("Special Diet Notes", ""),
            ]))
            content.append(Paragraph(f"Schedule: {checkbox('AM Only')}  {checkbox('PM Only')}  {checkbox('AM & PM')}  {checkbox('Free Feed')}", value_style))
            content.append(Spacer(1, 6))
            content.append(Paragraph(f"Treats OK: {checkbox('Yes')}  {checkbox('No')}  {checkbox('Bring Own')}", value_style))

            # Health & Behavior
            content.append(Paragraph("HEALTH & BEHAVIOR", section_style))
            content.append(Paragraph(f"Vaccinations Current: {checkbox('Yes')}  {checkbox('No')} (REQUIRED)", value_style))
            content.append(Spacer(1, 6))
            content.append(make_table([
                field_row("Medications", ""),
                field_row("Medication Schedule", ""),
                field_row("Allergies", ""),
            ]))
            content.append(Paragraph(f"With other dogs: {checkbox('Great')}  {checkbox('OK')}  {checkbox('Prefers Alone')}", value_style))
            content.append(Spacer(1, 4))
            content.append(Paragraph(f"With people: {checkbox('Friendly')}  {checkbox('Shy')}  {checkbox('Caution')}", value_style))

        # Footer - Authorization
        content.append(Spacer(1, 20))
        content.append(HRFlowable(width="100%", thickness=1, color=black, spaceAfter=10))
        content.append(Paragraph("AUTHORIZATION & CONSENT", section_style))

        auth_text = {
            "shelter": "I certify that the information provided is accurate. I understand the shelter will provide appropriate care.",
            "groomer": "I authorize grooming services and agree to pay for services rendered. I confirm vaccinations are current.",
            "vet": "I authorize examination and treatment of my pet and agree to pay for all services rendered.",
            "boarding": "I authorize boarding services and emergency veterinary care if needed. I agree to pay all associated costs."
        }
        content.append(Paragraph(auth_text[form_type], small_style))
        content.append(Spacer(1, 20))

        # Signature line
        sig_table = Table([
            [Paragraph("<b>Signature:</b>", label_style), "_" * 40,
             Paragraph("<b>Date:</b>", label_style), "_" * 20]
        ], colWidths=[1*inch, 2.5*inch, 0.6*inch, 1.5*inch])
        sig_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ]))
        content.append(sig_table)

        # Footer
        content.append(Spacer(1, 30))
        content.append(HRFlowable(width="100%", thickness=0.5, color=gray))
        content.append(Paragraph("Generated by Canine Classifier Pro | www.canineclassifier.com",
                                ParagraphStyle('Footer', parent=styles['Normal'],
                                              fontSize=8, alignment=TA_CENTER, textColor=gray)))

        # Build PDF
        doc.build(content)

    def _shelter_form(self, data, breed_info, date):
        form = []
        form.append("╔" + "═" * 58 + "╗")
        form.append("║" + "ANIMAL SHELTER INTAKE FORM".center(58) + "║")
        form.append("╚" + "═" * 58 + "╝")
        form.append(f"\nIntake Date: {date}")
        form.append(f"Intake ID: SH-{datetime.datetime.now().strftime('%Y%m%d%H%M')}")
        form.append("\n" + "─" * 60)
        form.append("ANIMAL INFORMATION")
        form.append("─" * 60)
        form.append(f"\nName: {data['dog_name']}")
        form.append(f"Species: Canine")
        form.append(f"Breed: {data['breed']}")
        form.append(f"Age: {data['age']}")
        form.append(f"Weight: {data['weight']} lbs")
        form.append(f"Sex: {data['sex']}")
        form.append(f"Color/Markings: {data['color']}")

        if breed_info:
            form.append(f"\n[AUTO-FILLED FROM DATABASE]")
            form.append(f"Breed Group: {breed_info['group']}")
            form.append(f"Expected Size: {breed_info['size']['weight']}")
            form.append(f"Typical Temperament: {', '.join(breed_info['temperament'][:3])}")

        form.append("\n" + "─" * 60)
        form.append("INTAKE CIRCUMSTANCES")
        form.append("─" * 60)
        form.append("\nIntake Type: [ ] Stray  [ ] Surrender  [ ] Transfer  [ ] Other")
        form.append("Location Found: ________________")
        form.append("Surrender Reason: ________________")

        form.append("\n" + "─" * 60)
        form.append("PREVIOUS OWNER (if known)")
        form.append("─" * 60)
        form.append(f"\nName: {data['owner_name']}")
        form.append(f"Phone: {data['phone']}")
        form.append(f"Address: {data['address']}")

        form.append("\n" + "─" * 60)
        form.append("INITIAL ASSESSMENT")
        form.append("─" * 60)
        form.append("\nBody Condition Score (1-9): ____")
        form.append("Temperament: [ ] Friendly  [ ] Shy  [ ] Fearful  [ ] Aggressive")
        form.append("Vaccinations: [ ] Unknown  [ ] UTD  [ ] Needed")
        form.append("Spay/Neuter: [ ] Yes  [ ] No  [ ] Unknown")
        form.append("Microchip: [ ] Yes #____________  [ ] No  [ ] Check needed")

        if breed_info and breed_info.get('health_issues'):
            form.append(f"\n[BREED-SPECIFIC HEALTH ALERTS]")
            for issue in breed_info['health_issues'][:3]:
                form.append(f"  ⚠ Watch for: {issue}")

        form.append("\n" + "─" * 60)
        form.append("STAFF USE ONLY")
        form.append("─" * 60)
        form.append("\nIntake Staff: ________________")
        form.append("Kennel Assignment: ________________")
        form.append("Vet Exam Scheduled: ________________")
        form.append("\n\nStaff Signature: ________________  Date: ________")

        form.append("\n" + "═" * 60)
        form.append("Generated by Canine Classifier Pro")
        return form

    def _groomer_form(self, data, breed_info, date):
        form = []
        form.append("╔" + "═" * 58 + "╗")
        form.append("║" + "PROFESSIONAL GROOMING INTAKE FORM".center(58) + "║")
        form.append("╚" + "═" * 58 + "╝")
        form.append(f"\nDate: {date}")
        form.append(f"Appointment #: GR-{datetime.datetime.now().strftime('%Y%m%d%H%M')}")

        form.append("\n" + "─" * 60)
        form.append("CLIENT INFORMATION")
        form.append("─" * 60)
        form.append(f"\nOwner Name: {data['owner_name']}")
        form.append(f"Phone: {data['phone']}")
        form.append(f"Email: {data['email']}")
        form.append(f"Address: {data['address']}")

        form.append("\n" + "─" * 60)
        form.append("PET INFORMATION")
        form.append("─" * 60)
        form.append(f"\nPet Name: {data['dog_name']}")
        form.append(f"Breed: {data['breed']}")
        form.append(f"Age: {data['age']}")
        form.append(f"Weight: {data['weight']} lbs")
        form.append(f"Color: {data['color']}")

        if breed_info:
            form.append(f"\n[BREED-SPECIFIC GROOMING INFO]")
            form.append(f"Coat Type: {breed_info.get('grooming', 'Standard')}")
            form.append(f"Shedding Level: {breed_info.get('shedding', 'Moderate')}")

        form.append("\n" + "─" * 60)
        form.append("SERVICE REQUEST")
        form.append("─" * 60)
        form.append("\n[ ] Full Groom  [ ] Bath & Brush  [ ] Nail Trim  [ ] Ear Clean")
        form.append("[ ] Teeth Brushing  [ ] De-shedding  [ ] Breed Cut  [ ] Puppy Cut")
        form.append("\nSpecial Requests: ________________")
        form.append("Preferred Cologne: [ ] None  [ ] Light  [ ] Fresh  [ ] ________")

        form.append("\n" + "─" * 60)
        form.append("HEALTH & BEHAVIOR")
        form.append("─" * 60)
        form.append("\nVaccinations Current: [ ] Yes  [ ] No  (Required for service)")
        form.append("Allergies/Sensitivities: ________________")
        form.append("Skin Conditions: ________________")
        form.append("Behavioral Notes: [ ] Good  [ ] Nervous  [ ] Needs muzzle")
        form.append("Problem Areas: ________________")

        form.append("\n" + "─" * 60)
        form.append("AUTHORIZATION")
        form.append("─" * 60)
        form.append("\nI authorize grooming services and agree to pay for services")
        form.append("rendered. I understand my pet must be current on vaccinations.")
        form.append("\n\nSignature: ________________  Date: ________")
        form.append("Emergency Contact: " + data['emergency_contact'])

        form.append("\n" + "═" * 60)
        form.append("Generated by Canine Classifier Pro")
        return form

    def _vet_form(self, data, breed_info, date):
        form = []
        form.append("╔" + "═" * 58 + "╗")
        form.append("║" + "NEW PATIENT VETERINARY INTAKE FORM".center(58) + "║")
        form.append("╚" + "═" * 58 + "╝")
        form.append(f"\nDate: {date}")
        form.append(f"Patient ID: VET-{datetime.datetime.now().strftime('%Y%m%d%H%M')}")

        form.append("\n" + "─" * 60)
        form.append("OWNER INFORMATION")
        form.append("─" * 60)
        form.append(f"\nName: {data['owner_name']}")
        form.append(f"Phone: {data['phone']}")
        form.append(f"Email: {data['email']}")
        form.append(f"Address: {data['address']}")
        form.append(f"Emergency Contact: {data['emergency_contact']}")

        form.append("\n" + "─" * 60)
        form.append("PATIENT INFORMATION")
        form.append("─" * 60)
        form.append(f"\nPatient Name: {data['dog_name']}")
        form.append(f"Species: Canine")
        form.append(f"Breed: {data['breed']}")
        form.append(f"Age: {data['age']}")
        form.append(f"Weight: {data['weight']} lbs")
        form.append(f"Sex: {data['sex']}")
        form.append(f"Color/Markings: {data['color']}")

        if breed_info:
            form.append(f"\n[BREED-SPECIFIC MEDICAL CONSIDERATIONS]")
            form.append(f"Breed Group: {breed_info['group']}")
            form.append(f"Expected Lifespan: {breed_info['lifespan']}")
            form.append(f"\nKnown Breed Health Concerns:")
            for issue in breed_info.get('health_issues', []):
                form.append(f"  ⚠ {issue}")

        form.append("\n" + "─" * 60)
        form.append("MEDICAL HISTORY")
        form.append("─" * 60)
        form.append("\nSpayed/Neutered: [ ] Yes  [ ] No  Date: ________")
        form.append("Previous Vet: ________________")
        form.append("Current Medications: ________________")
        form.append("Known Allergies: ________________")
        form.append("Previous Surgeries: ________________")

        form.append("\n" + "─" * 60)
        form.append("VACCINATION RECORD")
        form.append("─" * 60)
        form.append("\nRabies: [ ] Current  Date: ________ [ ] Needed")
        form.append("DHPP: [ ] Current  Date: ________ [ ] Needed")
        form.append("Bordetella: [ ] Current  Date: ________ [ ] Needed")
        form.append("Heartworm Test: [ ] Current  Date: ________ [ ] Needed")

        form.append("\n" + "─" * 60)
        form.append("REASON FOR VISIT")
        form.append("─" * 60)
        form.append("\n[ ] Wellness Exam  [ ] Sick Visit  [ ] Vaccination")
        form.append("[ ] Injury  [ ] Follow-up  [ ] Emergency")
        form.append("\nDescription of Concern:")
        form.append("________________________________________________")
        form.append("________________________________________________")

        form.append("\n" + "─" * 60)
        form.append("CONSENT")
        form.append("─" * 60)
        form.append("\nI authorize examination and treatment of my pet.")
        form.append("\n\nSignature: ________________  Date: ________")

        form.append("\n" + "═" * 60)
        form.append("Generated by Canine Classifier Pro - Veterinary Module")
        return form

    def _boarding_form(self, data, breed_info, date):
        form = []
        form.append("╔" + "═" * 58 + "╗")
        form.append("║" + "PET BOARDING/DAYCARE INTAKE FORM".center(58) + "║")
        form.append("╚" + "═" * 58 + "╝")
        form.append(f"\nDate: {date}")
        form.append(f"Reservation #: BD-{datetime.datetime.now().strftime('%Y%m%d%H%M')}")

        form.append("\n" + "─" * 60)
        form.append("OWNER INFORMATION")
        form.append("─" * 60)
        form.append(f"\nName: {data['owner_name']}")
        form.append(f"Phone: {data['phone']}")
        form.append(f"Email: {data['email']}")
        form.append(f"Address: {data['address']}")
        form.append(f"Emergency Contact: {data['emergency_contact']}")

        form.append("\n" + "─" * 60)
        form.append("PET INFORMATION")
        form.append("─" * 60)
        form.append(f"\nPet Name: {data['dog_name']}")
        form.append(f"Breed: {data['breed']}")
        form.append(f"Age: {data['age']}")
        form.append(f"Weight: {data['weight']} lbs")
        form.append(f"Color: {data['color']}")
        form.append(f"Sex: {data['sex']}")

        if breed_info:
            form.append(f"\n[BREED-SPECIFIC CARE NOTES]")
            form.append(f"Exercise Needs: {breed_info.get('exercise', 'Moderate')}")
            form.append(f"Good with other dogs: {'Yes' if breed_info.get('good_with', {}).get('dogs') else 'Monitor'}")
            form.append(f"Temperament: {', '.join(breed_info.get('temperament', [])[:2])}")

        form.append("\n" + "─" * 60)
        form.append("STAY DETAILS")
        form.append("─" * 60)
        form.append("\nCheck-in Date: ________  Time: ________")
        form.append("Check-out Date: ________  Time: ________")
        form.append("Service Type: [ ] Boarding  [ ] Daycare  [ ] Both")

        form.append("\n" + "─" * 60)
        form.append("FEEDING INSTRUCTIONS")
        form.append("─" * 60)
        form.append("\nFood Brand: ________________")
        form.append("Amount per meal: ________________")
        form.append("Feeding Schedule: [ ] AM only  [ ] PM only  [ ] AM & PM  [ ] Free feed")
        form.append("Special Diet: ________________")
        form.append("Treats OK: [ ] Yes  [ ] No  [ ] Bring own")

        form.append("\n" + "─" * 60)
        form.append("HEALTH & BEHAVIOR")
        form.append("─" * 60)
        form.append("\nVaccinations Current: [ ] Yes  [ ] No (REQUIRED)")
        form.append("Medications: ________________")
        form.append("Medication Schedule: ________________")
        form.append("Allergies: ________________")
        form.append("\nBehavior with other dogs: [ ] Great  [ ] OK  [ ] Prefers alone")
        form.append("Behavior with people: [ ] Friendly  [ ] Shy  [ ] Caution")

        form.append("\n" + "─" * 60)
        form.append("ADDITIONAL SERVICES")
        form.append("─" * 60)
        form.append("\n[ ] Bath before pickup  [ ] Nail trim  [ ] Playtime upgrade")
        form.append("[ ] One-on-one attention  [ ] Webcam access  [ ] Report card")

        form.append("\n" + "─" * 60)
        form.append("AUTHORIZATION & AGREEMENT")
        form.append("─" * 60)
        form.append("\nI authorize boarding services and emergency veterinary care")
        form.append("if needed. I agree to pay all associated costs.")
        form.append("\n\nSignature: ________________  Date: ________")

        form.append("\n" + "═" * 60)
        form.append("Generated by Canine Classifier Pro")
        return form


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


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
