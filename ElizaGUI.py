#!/usr/bin/env python3
"""
Canine Classifier - Ultra Premium iOS-Style UI
Clean, minimal, and polished design with hidden scrollbars.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
import threading
import webbrowser

try:
    from PIL import Image, ImageTk, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    from breed_info import BREED_INFO, get_breed_info
except ImportError:
    BREED_INFO = {}
    def get_breed_info(breed): return None


class Theme:
    """Ultra-modern dark theme with vibrant accents."""
    # Backgrounds - deeper, richer navy
    BG_DARK = "#080810"
    BG = "#0c0c18"
    BG2 = "#101020"
    CARD = "#16162a"
    CARD2 = "#1a1a32"
    CARD_HOVER = "#1e1e3a"
    INPUT = "#0e0e1c"

    # Glass effect colors
    GLASS = "#1c1c38"
    GLASS_BORDER = "#2a2a50"

    # Vibrant accents
    CYAN = "#00e5c0"
    CYAN2 = "#00d4aa"
    CYAN_GLOW = "#00ffdd"
    TEAL = "#00c4d8"
    BLUE = "#0099ff"
    PURPLE = "#8b5cf6"
    PINK = "#ec4899"
    ORANGE = "#f97316"
    GREEN = "#22c55e"
    RED = "#ef4444"
    YELLOW = "#eab308"

    # Text
    WHITE = "#ffffff"
    TEXT = "#f0f0f8"
    TEXT2 = "#b0b0c8"
    MUTED = "#6b6b88"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Canine Classifier")

        # Screen sizing - fill more of the screen
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        self.w = min(int(sw * 0.88), 1400)
        self.h = min(int(sh * 0.88), 850)
        self.scale = min(self.w / 1400, self.h / 850)

        x, y = (sw - self.w) // 2, (sh - self.h) // 2
        root.geometry(f"{self.w}x{self.h}+{x}+{y}")
        root.configure(bg=Theme.BG_DARK)
        root.minsize(1000, 650)

        # Premium fonts
        base = max(int(12 * self.scale), 10)
        self.F = {
            'hero': ('Segoe UI Semibold', int(base * 2.4)),
            'h1': ('Segoe UI Semibold', int(base * 1.7)),
            'h2': ('Segoe UI Semibold', int(base * 1.3)),
            'h3': ('Segoe UI Semibold', int(base * 1.1)),
            'body': ('Segoe UI', base),
            'sm': ('Segoe UI', int(base * 0.92)),
            'xs': ('Segoe UI', int(base * 0.83)),
            'mono': ('Consolas', int(base * 0.9)),
        }

        self.frame = None
        self.classifier = None
        self.tree = self._build_tree()
        self.node = None
        self.qnum = 0

        # Style ttk widgets
        self._setup_styles()
        self.home()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox',
            fieldbackground=Theme.INPUT,
            background=Theme.CARD,
            foreground=Theme.TEXT,
            arrowcolor=Theme.CYAN,
            borderwidth=0,
            padding=10)
        style.map('TCombobox',
            fieldbackground=[('readonly', Theme.INPUT)],
            selectbackground=[('readonly', Theme.CYAN)])

    def s(self, v):
        """Scale a value based on window size."""
        return max(int(v * self.scale), 1)

    def clear(self):
        if self.frame:
            self.frame.destroy()

    # ══════════════════════════════════════════════════════════════════
    # UI COMPONENTS
    # ══════════════════════════════════════════════════════════════════

    def glass_card(self, parent, glow_color=None):
        """Create a premium glass-morphism card."""
        border_color = glow_color if glow_color else Theme.GLASS_BORDER
        card = tk.Frame(parent, bg=Theme.CARD,
                       highlightbackground=border_color,
                       highlightthickness=1)
        return card

    def pill_btn(self, parent, text, cmd, color=None, size='normal'):
        """Create an iOS-style pill button."""
        bg = color if color else Theme.CYAN
        fg = Theme.BG_DARK if bg in [Theme.CYAN, Theme.GREEN, Theme.YELLOW] else Theme.WHITE

        pad_x = self.s(28) if size == 'normal' else self.s(20)
        pad_y = self.s(12) if size == 'normal' else self.s(8)
        font = self.F['body'] if size == 'normal' else self.F['sm']

        frame = tk.Frame(parent, bg=bg, cursor='hand2')
        label = tk.Label(frame, text=text, font=font, fg=fg, bg=bg,
                        padx=pad_x, pady=pad_y)
        label.pack()

        def on_enter(e):
            lighter = Theme.CYAN_GLOW if bg == Theme.CYAN else Theme.CARD_HOVER
            frame.config(bg=lighter)
            label.config(bg=lighter)

        def on_leave(e):
            frame.config(bg=bg)
            label.config(bg=bg)

        frame.bind('<Enter>', on_enter)
        frame.bind('<Leave>', on_leave)
        frame.bind('<Button-1>', lambda e: cmd())
        label.bind('<Button-1>', lambda e: cmd())

        return frame

    def ghost_btn(self, parent, text, cmd):
        """Create a subtle ghost/outline button."""
        frame = tk.Frame(parent, bg=Theme.CARD, cursor='hand2',
                        highlightbackground=Theme.GLASS_BORDER,
                        highlightthickness=1)
        label = tk.Label(frame, text=text, font=self.F['body'],
                        fg=Theme.TEXT2, bg=Theme.CARD,
                        padx=self.s(24), pady=self.s(10))
        label.pack()

        def on_enter(e):
            frame.config(bg=Theme.CARD_HOVER, highlightbackground=Theme.CYAN)
            label.config(bg=Theme.CARD_HOVER, fg=Theme.WHITE)

        def on_leave(e):
            frame.config(bg=Theme.CARD, highlightbackground=Theme.GLASS_BORDER)
            label.config(bg=Theme.CARD, fg=Theme.TEXT2)

        frame.bind('<Enter>', on_enter)
        frame.bind('<Leave>', on_leave)
        frame.bind('<Button-1>', lambda e: cmd())
        label.bind('<Button-1>', lambda e: cmd())

        return frame

    def back_arrow(self, parent):
        """Create a sleek back navigation."""
        frame = tk.Frame(parent, bg=Theme.BG, cursor='hand2')
        label = tk.Label(frame, text="← Back", font=self.F['sm'],
                        fg=Theme.TEXT2, bg=Theme.BG,
                        padx=self.s(8), pady=self.s(6))
        label.pack()

        def on_enter(e):
            label.config(fg=Theme.CYAN)
        def on_leave(e):
            label.config(fg=Theme.TEXT2)

        frame.bind('<Enter>', on_enter)
        frame.bind('<Leave>', on_leave)
        frame.bind('<Button-1>', lambda e: self.home())
        label.bind('<Button-1>', lambda e: self.home())

        return frame

    def scrollable_frame(self, parent):
        """Create a scrollable container without visible scrollbar."""
        container = tk.Frame(parent, bg=Theme.BG)
        canvas = tk.Canvas(container, bg=Theme.BG, highlightthickness=0)
        inner = tk.Frame(canvas, bg=Theme.BG)

        canvas.create_window((0, 0), window=inner, anchor='nw')
        canvas.pack(fill='both', expand=True)

        def on_configure(e):
            canvas.configure(scrollregion=canvas.bbox('all'))
            # Make inner frame fill width
            canvas.itemconfig(canvas.find_all()[0], width=canvas.winfo_width())

        inner.bind('<Configure>', on_configure)
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(
            canvas.find_all()[0], width=e.width))

        # Mouse wheel scrolling
        def on_mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), 'units')

        canvas.bind_all('<MouseWheel>', on_mousewheel)

        return container, inner

    # ══════════════════════════════════════════════════════════════════
    # HOME PAGE
    # ══════════════════════════════════════════════════════════════════

    def home(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Header section
        header = tk.Frame(self.frame, bg=Theme.BG)
        header.pack(fill='x', padx=self.s(60), pady=(self.s(50), self.s(30)))

        # Title with gradient effect (simulated)
        title_frame = tk.Frame(header, bg=Theme.BG)
        title_frame.pack(anchor='w')

        tk.Label(title_frame, text="Canine", font=self.F['hero'],
                fg=Theme.WHITE, bg=Theme.BG).pack(side='left')
        tk.Label(title_frame, text="Classifier", font=self.F['hero'],
                fg=Theme.CYAN, bg=Theme.BG).pack(side='left', padx=(self.s(12), 0))

        # Subtitle
        tk.Label(header, text="AI-Powered Dog Breed Identification",
                font=self.F['h3'], fg=Theme.TEXT2, bg=Theme.BG).pack(anchor='w', pady=(self.s(8), 0))

        # Cards grid
        grid = tk.Frame(self.frame, bg=Theme.BG)
        grid.pack(fill='both', expand=True, padx=self.s(60), pady=self.s(20))

        grid.grid_columnconfigure(0, weight=1, uniform='col')
        grid.grid_columnconfigure(1, weight=1, uniform='col')
        grid.grid_rowconfigure(0, weight=1, uniform='row')
        grid.grid_rowconfigure(1, weight=1, uniform='row')

        cards = [
            ("01", "AI Recognition", "Upload a photo for instant breed detection using machine learning",
             Theme.CYAN, self.ai_page),
            ("02", "Questionnaire", "Answer questions about your dog's physical features",
             Theme.PINK, self.quest_page),
            ("03", "Dichotomous Key", "Scientific Yes/No identification method",
             Theme.TEAL, self.dkey_page),
            ("04", "Breed Database", "Explore detailed information on 51+ dog breeds",
             Theme.ORANGE, self.db_page),
        ]

        for i, (num, title, desc, color, cmd) in enumerate(cards):
            row, col = divmod(i, 2)
            self._create_home_card(grid, num, title, desc, color, cmd, row, col)

        # Footer
        footer = tk.Frame(self.frame, bg=Theme.BG)
        footer.pack(fill='x', pady=self.s(20))

        tk.Label(footer, text="v2.0  •  51 Breeds  •  AI Powered",
                font=self.F['xs'], fg=Theme.MUTED, bg=Theme.BG).pack()

    def _create_home_card(self, parent, num, title, desc, accent, cmd, row, col):
        """Create a premium home page card."""
        card = self.glass_card(parent)
        card.grid(row=row, column=col, padx=self.s(12), pady=self.s(12), sticky='nsew')
        card.config(cursor='hand2')

        inner = tk.Frame(card, bg=Theme.CARD)
        inner.pack(fill='both', expand=True, padx=self.s(28), pady=self.s(28))

        # Number badge with accent color
        badge = tk.Frame(inner, bg=accent)
        badge.pack(anchor='w')
        tk.Label(badge, text=f"  {num}  ", font=self.F['h3'],
                fg=Theme.BG_DARK, bg=accent).pack(padx=self.s(2), pady=self.s(2))

        # Title
        tk.Label(inner, text=title, font=self.F['h2'],
                fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w', pady=(self.s(18), self.s(6)))

        # Description
        tk.Label(inner, text=desc, font=self.F['sm'],
                fg=Theme.TEXT2, bg=Theme.CARD,
                wraplength=self.s(280), justify='left').pack(anchor='w')

        # Arrow indicator
        arrow_frame = tk.Frame(inner, bg=Theme.CARD)
        arrow_frame.pack(side='bottom', fill='x')
        arrow = tk.Label(arrow_frame, text="→", font=('Segoe UI', self.s(24)),
                        fg=accent, bg=Theme.CARD)
        arrow.pack(side='right')

        # Hover effects
        all_widgets = [card, inner, badge, arrow_frame, arrow]
        for w in inner.winfo_children():
            all_widgets.append(w)

        def enter(e):
            card.config(highlightbackground=accent, bg=Theme.CARD_HOVER)
            for w in all_widgets:
                try:
                    if w != badge and not w.master == badge:
                        w.config(bg=Theme.CARD_HOVER)
                except: pass

        def leave(e):
            card.config(highlightbackground=Theme.GLASS_BORDER, bg=Theme.CARD)
            for w in all_widgets:
                try:
                    if w != badge and not w.master == badge:
                        w.config(bg=Theme.CARD)
                except: pass

        for w in all_widgets:
            w.bind('<Enter>', enter)
            w.bind('<Leave>', leave)
            w.bind('<Button-1>', lambda e, c=cmd: c())

    # ══════════════════════════════════════════════════════════════════
    # AI RECOGNITION PAGE
    # ══════════════════════════════════════════════════════════════════

    def ai_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Header
        header = tk.Frame(self.frame, bg=Theme.BG)
        header.pack(fill='x', padx=self.s(40), pady=(self.s(25), self.s(15)))

        self.back_arrow(header).pack(side='left')

        title_area = tk.Frame(header, bg=Theme.BG)
        title_area.pack(side='left', padx=(self.s(20), 0))
        tk.Label(title_area, text="AI Recognition", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(anchor='w')
        tk.Label(title_area, text="Upload a photo to identify the breed",
                font=self.F['sm'], fg=Theme.TEXT2, bg=Theme.BG).pack(anchor='w')

        # Main content - two columns
        content = tk.Frame(self.frame, bg=Theme.BG)
        content.pack(fill='both', expand=True, padx=self.s(40), pady=(0, self.s(30)))

        # === LEFT COLUMN - Upload ===
        left = tk.Frame(content, bg=Theme.BG)
        left.pack(side='left', fill='both', expand=True, padx=(0, self.s(15)))

        upload_card = self.glass_card(left, Theme.GLASS_BORDER)
        upload_card.pack(fill='both', expand=True)

        upload_inner = tk.Frame(upload_card, bg=Theme.CARD)
        upload_inner.pack(fill='both', expand=True, padx=self.s(25), pady=self.s(25))

        # Upload header
        tk.Label(upload_inner, text="Upload Image", font=self.F['h3'],
                fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w')
        tk.Label(upload_inner, text="Supports JPG, PNG, WebP",
                font=self.F['xs'], fg=Theme.MUTED, bg=Theme.CARD).pack(anchor='w')

        # Preview area with dashed border effect
        preview_container = tk.Frame(upload_inner, bg=Theme.INPUT,
                                    highlightbackground=Theme.GLASS_BORDER,
                                    highlightthickness=2)
        preview_container.pack(fill='both', expand=True, pady=(self.s(18), self.s(15)))

        self.preview_frame = tk.Frame(preview_container, bg=Theme.INPUT)
        self.preview_frame.pack(fill='both', expand=True, padx=3, pady=3)

        # Placeholder content
        self.placeholder = tk.Frame(self.preview_frame, bg=Theme.INPUT)
        self.placeholder.place(relx=0.5, rely=0.5, anchor='center')

        # Upload icon (circle with plus)
        icon_size = self.s(70)
        icon_frame = tk.Frame(self.placeholder, bg=Theme.GLASS,
                             width=icon_size, height=icon_size)
        icon_frame.pack()
        icon_frame.pack_propagate(False)
        tk.Label(icon_frame, text="+", font=('Segoe UI Light', self.s(32)),
                fg=Theme.CYAN, bg=Theme.GLASS).place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(self.placeholder, text="Click to browse or drag image here",
                font=self.F['sm'], fg=Theme.MUTED, bg=Theme.INPUT).pack(pady=(self.s(15), 0))
        tk.Label(self.placeholder, text="Maximum 10MB",
                font=self.F['xs'], fg=Theme.MUTED, bg=Theme.INPUT).pack(pady=(self.s(5), 0))

        self.preview_photo = None
        self.preview_label = None

        # File info
        self.file_var = tk.StringVar(value="No file selected")
        tk.Label(upload_inner, textvariable=self.file_var, font=self.F['xs'],
                fg=Theme.TEXT2, bg=Theme.CARD).pack(anchor='w', pady=(0, self.s(12)))

        # Buttons
        btn_row = tk.Frame(upload_inner, bg=Theme.CARD)
        btn_row.pack(fill='x')

        self.ghost_btn(btn_row, "Browse Files", self._browse_image).pack(side='left', padx=(0, self.s(10)))
        self.pill_btn(btn_row, "Analyze Image", self._analyze_image).pack(side='left')

        # Status
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(upload_inner, textvariable=self.status_var,
                                    font=self.F['sm'], fg=Theme.CYAN, bg=Theme.CARD)
        self.status_label.pack(pady=(self.s(15), 0))

        # === RIGHT COLUMN - Results ===
        right = tk.Frame(content, bg=Theme.BG)
        right.pack(side='left', fill='both', expand=True, padx=(self.s(15), 0))

        results_card = self.glass_card(right, Theme.GLASS_BORDER)
        results_card.pack(fill='both', expand=True)

        results_inner = tk.Frame(results_card, bg=Theme.CARD)
        results_inner.pack(fill='both', expand=True, padx=self.s(25), pady=self.s(25))

        # Results header
        tk.Label(results_inner, text="Analysis Results", font=self.F['h3'],
                fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w')
        tk.Label(results_inner, text="Top predictions with confidence scores",
                font=self.F['xs'], fg=Theme.MUTED, bg=Theme.CARD).pack(anchor='w', pady=(0, self.s(15)))

        # Results container (no scrollbar needed - 5 results fit easily)
        self.results_frame = tk.Frame(results_inner, bg=Theme.CARD)
        self.results_frame.pack(fill='both', expand=True)

        # Initial state
        self._show_empty_results()

        self.selected_image = None

    def _show_empty_results(self):
        """Show placeholder when no results."""
        for w in self.results_frame.winfo_children():
            w.destroy()

        placeholder = tk.Frame(self.results_frame, bg=Theme.CARD)
        placeholder.pack(expand=True)

        # Empty state icon
        icon = tk.Label(placeholder, text="◎", font=('Segoe UI', self.s(48)),
                       fg=Theme.MUTED, bg=Theme.CARD)
        icon.pack()

        tk.Label(placeholder, text="No analysis yet",
                font=self.F['body'], fg=Theme.TEXT2, bg=Theme.CARD).pack(pady=(self.s(10), 0))
        tk.Label(placeholder, text="Upload an image to identify the breed",
                font=self.F['xs'], fg=Theme.MUTED, bg=Theme.CARD).pack(pady=(self.s(5), 0))

    def _browse_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.webp")])
        if path:
            self.selected_image = path
            name = os.path.basename(path)
            self.file_var.set(name[:35] + "..." if len(name) > 38 else name)
            self._show_preview(path)

    def _show_preview(self, path):
        if not PIL_AVAILABLE:
            return
        try:
            img = Image.open(path)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            self.preview_frame.update()
            max_w = max(self.preview_frame.winfo_width() - 20, 100)
            max_h = max(self.preview_frame.winfo_height() - 20, 100)

            ratio = min(max_w / img.width, max_h / img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

            self.preview_photo = ImageTk.PhotoImage(img)
            self.placeholder.place_forget()

            if not self.preview_label:
                self.preview_label = tk.Label(self.preview_frame, bg=Theme.INPUT)
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

        # Loading state
        loading = tk.Frame(self.results_frame, bg=Theme.CARD)
        loading.pack(expand=True)
        tk.Label(loading, text="⟳", font=('Segoe UI', self.s(36)),
                fg=Theme.CYAN, bg=Theme.CARD).pack()
        tk.Label(loading, text="Analyzing...",
                font=self.F['body'], fg=Theme.TEXT2, bg=Theme.CARD).pack(pady=(self.s(10), 0))

        self.status_var.set("Processing image...")
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
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)[:40]}"))

    def _display_results(self, results):
        self.status_var.set("")

        for w in self.results_frame.winfo_children():
            w.destroy()

        if not results:
            self.status_var.set("Could not classify image")
            self._show_empty_results()
            return

        # Color palette for rankings
        colors = [Theme.CYAN, Theme.TEAL, Theme.PINK, Theme.ORANGE, Theme.PURPLE]

        for i, result in enumerate(results[:5]):
            breed = result.get('breed', 'Unknown')
            confidence = result.get('confidence', 0)
            verified = result.get('verified', False)
            db_name = result.get('db_name', breed)
            display_name = db_name if verified else breed

            # Result card
            card = tk.Frame(self.results_frame, bg=Theme.BG2, cursor='hand2')
            card.pack(fill='x', pady=self.s(5))

            inner = tk.Frame(card, bg=Theme.BG2)
            inner.pack(fill='x', padx=self.s(18), pady=self.s(14))

            # Left section
            left = tk.Frame(inner, bg=Theme.BG2)
            left.pack(side='left', fill='both', expand=True)

            # Rank badge
            rank_color = colors[i] if i < len(colors) else Theme.MUTED
            rank_badge = tk.Frame(left, bg=rank_color)
            rank_badge.pack(side='left', padx=(0, self.s(15)))
            tk.Label(rank_badge, text=f"  #{i+1}  ", font=self.F['h3'],
                    fg=Theme.BG_DARK, bg=rank_color).pack(pady=self.s(2))

            # Name and verification status
            info_frame = tk.Frame(left, bg=Theme.BG2)
            info_frame.pack(side='left', fill='both', expand=True)

            tk.Label(info_frame, text=display_name, font=self.F['body'],
                    fg=Theme.WHITE, bg=Theme.BG2).pack(anchor='w')

            status_text = "✓ Verified in database" if verified else "AI prediction"
            status_color = Theme.GREEN if verified else Theme.MUTED
            tk.Label(info_frame, text=status_text, font=self.F['xs'],
                    fg=status_color, bg=Theme.BG2).pack(anchor='w')

            # Right section - Progress bar and percentage
            right = tk.Frame(inner, bg=Theme.BG2)
            right.pack(side='right')

            # Larger progress bar
            bar_width = self.s(140)
            bar_height = self.s(12)

            bar_bg = tk.Frame(right, bg=Theme.INPUT, width=bar_width, height=bar_height)
            bar_bg.pack(side='left', padx=(0, self.s(12)))
            bar_bg.pack_propagate(False)

            fill_width = max(3, int(bar_width * confidence / 100))
            bar_fill = tk.Frame(bar_bg, bg=rank_color, width=fill_width, height=bar_height)
            bar_fill.place(x=0, y=0)

            # Percentage
            tk.Label(right, text=f"{confidence:.1f}%", font=self.F['body'],
                    fg=rank_color, bg=Theme.BG2, width=7, anchor='e').pack(side='left')

            # Click to view details
            def make_click_handler(name):
                return lambda e: self._show_breed_popup(name)

            for widget in [card, inner, left, info_frame, right]:
                widget.bind('<Button-1>', make_click_handler(display_name))

            # Hover effect
            def make_enter(c, clr):
                return lambda e: c.config(highlightbackground=clr, highlightthickness=1)
            def make_leave(c):
                return lambda e: c.config(highlightthickness=0)

            card.bind('<Enter>', make_enter(card, rank_color))
            card.bind('<Leave>', make_leave(card))

        # Footer hint
        tk.Label(self.results_frame, text="Click any result to view breed details",
                font=self.F['xs'], fg=Theme.MUTED, bg=Theme.CARD).pack(pady=(self.s(18), 0))

    # ══════════════════════════════════════════════════════════════════
    # QUESTIONNAIRE PAGE
    # ══════════════════════════════════════════════════════════════════

    def quest_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Header
        header = tk.Frame(self.frame, bg=Theme.BG)
        header.pack(fill='x', padx=self.s(40), pady=(self.s(25), self.s(15)))

        self.back_arrow(header).pack(side='left')

        title_area = tk.Frame(header, bg=Theme.BG)
        title_area.pack(side='left', padx=(self.s(20), 0))
        tk.Label(title_area, text="Questionnaire", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(anchor='w')
        tk.Label(title_area, text="Select your dog's characteristics",
                font=self.F['sm'], fg=Theme.TEXT2, bg=Theme.BG).pack(anchor='w')

        # Content
        content = tk.Frame(self.frame, bg=Theme.BG)
        content.pack(fill='both', expand=True, padx=self.s(40), pady=(0, self.s(30)))

        # Form card
        form_card = self.glass_card(content)
        form_card.pack(fill='x')

        form_inner = tk.Frame(form_card, bg=Theme.CARD)
        form_inner.pack(fill='x', padx=self.s(30), pady=self.s(30))

        # Questions grid
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
                row_frame.pack(fill='x', pady=self.s(10))

            q_frame = tk.Frame(row_frame, bg=Theme.CARD)
            q_frame.pack(side='left', fill='x', expand=True, padx=self.s(8))

            tk.Label(q_frame, text=label, font=self.F['sm'],
                    fg=Theme.TEXT2, bg=Theme.CARD).pack(anchor='w')

            var = tk.StringVar(value=options[0])
            self.quest_vars[key] = var

            combo = ttk.Combobox(q_frame, textvariable=var, values=options,
                               state='readonly', font=self.F['body'], width=self.s(20))
            combo.pack(anchor='w', pady=(self.s(5), 0))

        # Submit button
        btn_frame = tk.Frame(content, bg=Theme.BG)
        btn_frame.pack(pady=self.s(20))
        self.pill_btn(btn_frame, "Find Matching Breeds", self._run_questionnaire,
                     color=Theme.PINK).pack()

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
            card = self.glass_card(self.quest_results)
            card.pack(fill='x')

            inner = tk.Frame(card, bg=Theme.CARD)
            inner.pack(fill='x', padx=self.s(25), pady=self.s(25))

            tk.Label(inner, text="Matching Breeds", font=self.F['h3'],
                    fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w', pady=(0, self.s(12)))

            colors = [Theme.GREEN, Theme.TEAL, Theme.ORANGE]

            for i, (breed, _, prob) in enumerate(results):
                row = tk.Frame(inner, bg=Theme.BG2, cursor='hand2')
                row.pack(fill='x', pady=self.s(4))

                row_inner = tk.Frame(row, bg=Theme.BG2)
                row_inner.pack(fill='x', padx=self.s(15), pady=self.s(12))

                color = colors[i] if i < len(colors) else Theme.MUTED

                badge = tk.Frame(row_inner, bg=color)
                badge.pack(side='left', padx=(0, self.s(12)))
                tk.Label(badge, text=f"  #{i+1}  ", font=self.F['h3'],
                        fg=Theme.BG_DARK, bg=color).pack()

                tk.Label(row_inner, text=breed, font=self.F['body'],
                        fg=Theme.WHITE, bg=Theme.BG2).pack(side='left')
                tk.Label(row_inner, text=f"{prob:.0f}% match", font=self.F['sm'],
                        fg=color, bg=Theme.BG2).pack(side='right')

                row.bind('<Button-1>', lambda e, b=breed: self._show_breed_popup(b))
        else:
            tk.Label(self.quest_results, text="No matching breeds found",
                    font=self.F['body'], fg=Theme.MUTED, bg=Theme.BG).pack(pady=self.s(40))

    # ══════════════════════════════════════════════════════════════════
    # DICHOTOMOUS KEY PAGE
    # ══════════════════════════════════════════════════════════════════

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
        header.pack(fill='x', padx=self.s(40), pady=(self.s(25), self.s(15)))

        self.back_arrow(header).pack(side='left')

        title_area = tk.Frame(header, bg=Theme.BG)
        title_area.pack(side='left', padx=(self.s(20), 0))
        tk.Label(title_area, text="Dichotomous Key", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(anchor='w')
        tk.Label(title_area, text="Answer Yes or No to identify the breed",
                font=self.F['sm'], fg=Theme.TEXT2, bg=Theme.BG).pack(anchor='w')

        # Content
        self.dkey_content = tk.Frame(self.frame, bg=Theme.BG)
        self.dkey_content.pack(fill='both', expand=True, padx=self.s(40), pady=(0, self.s(30)))

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

        # Progress
        progress = tk.Frame(self.dkey_content, bg=Theme.BG)
        progress.pack(fill='x', pady=(0, self.s(20)))

        tk.Label(progress, text=f"Question {self.qnum}", font=self.F['sm'],
                fg=Theme.CYAN, bg=Theme.BG).pack(side='left')

        # Question card
        card = self.glass_card(self.dkey_content)
        card.pack(fill='x')

        inner = tk.Frame(card, bg=Theme.CARD)
        inner.pack(padx=self.s(40), pady=self.s(45))

        tk.Label(inner, text=self.node["q"], font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.CARD,
                wraplength=self.s(550)).pack()

        # Buttons
        btn_frame = tk.Frame(self.dkey_content, bg=Theme.BG)
        btn_frame.pack(pady=self.s(30))

        self.pill_btn(btn_frame, "   Yes   ",
                     lambda: self._answer_dkey(True), Theme.GREEN).pack(side='left', padx=self.s(10))
        self.pill_btn(btn_frame, "   No   ",
                     lambda: self._answer_dkey(False), Theme.RED).pack(side='left', padx=self.s(10))

        # Restart link
        restart = tk.Label(self.dkey_content, text="Start over", font=self.F['sm'],
                          fg=Theme.MUTED, bg=Theme.BG, cursor='hand2')
        restart.pack(pady=self.s(15))
        restart.bind('<Button-1>', lambda e: self._reset_dkey())
        restart.bind('<Enter>', lambda e: restart.config(fg=Theme.CYAN))
        restart.bind('<Leave>', lambda e: restart.config(fg=Theme.MUTED))

    def _answer_dkey(self, yes):
        self.node = self.node["y" if yes else "n"]
        self._show_dkey_question()

    def _show_dkey_result(self, breed):
        card = self.glass_card(self.dkey_content, Theme.CYAN)
        card.pack(fill='x')

        inner = tk.Frame(card, bg=Theme.CARD)
        inner.pack(padx=self.s(50), pady=self.s(50))

        # Success icon
        icon_size = self.s(70)
        icon = tk.Frame(inner, bg=Theme.GREEN, width=icon_size, height=icon_size)
        icon.pack()
        icon.pack_propagate(False)
        tk.Label(icon, text="✓", font=('Segoe UI', self.s(32)),
                fg=Theme.BG_DARK, bg=Theme.GREEN).place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(inner, text="Identification Complete", font=self.F['body'],
                fg=Theme.TEXT2, bg=Theme.CARD).pack(pady=(self.s(15), 0))

        tk.Label(inner, text=breed, font=self.F['hero'],
                fg=Theme.CYAN, bg=Theme.CARD).pack(pady=self.s(12))

        tk.Label(inner, text=f"Identified in {self.qnum} questions",
                font=self.F['xs'], fg=Theme.MUTED, bg=Theme.CARD).pack()

        # Buttons
        btn_frame = tk.Frame(self.dkey_content, bg=Theme.BG)
        btn_frame.pack(pady=self.s(25))

        self.pill_btn(btn_frame, "View Breed Info",
                     lambda: self._show_breed_popup(breed)).pack(side='left', padx=self.s(8))
        self.ghost_btn(btn_frame, "Try Again", self._reset_dkey).pack(side='left', padx=self.s(8))

    def _reset_dkey(self):
        self.node = self.tree
        self.qnum = 0
        self._show_dkey_question()

    # ══════════════════════════════════════════════════════════════════
    # DATABASE PAGE
    # ══════════════════════════════════════════════════════════════════

    def db_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Header
        header = tk.Frame(self.frame, bg=Theme.BG)
        header.pack(fill='x', padx=self.s(40), pady=(self.s(25), self.s(15)))

        self.back_arrow(header).pack(side='left')

        title_area = tk.Frame(header, bg=Theme.BG)
        title_area.pack(side='left', padx=(self.s(20), 0))
        tk.Label(title_area, text="Breed Database", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(anchor='w')

        count = len(BREED_INFO) if BREED_INFO else 0
        tk.Label(title_area, text=f"Explore detailed info on {count} breeds",
                font=self.F['sm'], fg=Theme.TEXT2, bg=Theme.BG).pack(anchor='w')

        # Search bar
        search_frame = tk.Frame(self.frame, bg=Theme.BG)
        search_frame.pack(fill='x', padx=self.s(40), pady=(0, self.s(15)))

        breeds = sorted([info['name'] for info in BREED_INFO.values()]) if BREED_INFO else []
        self.search_var = tk.StringVar()

        search_combo = ttk.Combobox(search_frame, textvariable=self.search_var,
                                   values=breeds, font=self.F['body'], width=self.s(35))
        search_combo.pack(side='left')

        self.pill_btn(search_frame, "Search",
                     lambda: self._show_db_detail(self.search_var.get()),
                     size='small').pack(side='left', padx=(self.s(12), 0))

        # Grid content
        content = tk.Frame(self.frame, bg=Theme.BG)
        content.pack(fill='both', expand=True, padx=self.s(40), pady=(0, self.s(30)))

        container, self.db_inner = self.scrollable_frame(content)
        container.pack(fill='both', expand=True)

        self._show_db_grid()

    def _show_db_grid(self):
        for w in self.db_inner.winfo_children():
            w.destroy()

        if not BREED_INFO:
            tk.Label(self.db_inner, text="No breed data available",
                    font=self.F['body'], fg=Theme.MUTED, bg=Theme.BG).pack(pady=self.s(40))
            return

        row_frame = None
        cols = 4

        for i, (key, info) in enumerate(sorted(BREED_INFO.items())):
            if i % cols == 0:
                row_frame = tk.Frame(self.db_inner, bg=Theme.BG)
                row_frame.pack(fill='x', pady=self.s(4))

            btn = tk.Frame(row_frame, bg=Theme.CARD, cursor='hand2',
                          highlightbackground=Theme.GLASS_BORDER,
                          highlightthickness=1)
            btn.pack(side='left', fill='x', expand=True, padx=self.s(4))

            label = tk.Label(btn, text=info['name'], font=self.F['xs'],
                           fg=Theme.TEXT, bg=Theme.CARD,
                           padx=self.s(10), pady=self.s(12))
            label.pack()

            def make_click(name):
                return lambda e: self._show_db_detail(name)

            btn.bind('<Button-1>', make_click(info['name']))
            label.bind('<Button-1>', make_click(info['name']))

            def make_enter(b):
                return lambda e: b.config(highlightbackground=Theme.CYAN, bg=Theme.CARD_HOVER)
            def make_leave(b):
                return lambda e: b.config(highlightbackground=Theme.GLASS_BORDER, bg=Theme.CARD)

            btn.bind('<Enter>', make_enter(btn))
            btn.bind('<Leave>', make_leave(btn))

    def _show_db_detail(self, name):
        info = get_breed_info(name)

        for w in self.db_inner.winfo_children():
            w.destroy()

        if not info:
            tk.Label(self.db_inner, text=f"No information found for '{name}'",
                    font=self.F['body'], fg=Theme.MUTED, bg=Theme.BG).pack(pady=self.s(20))

            back = tk.Label(self.db_inner, text="← Back to all breeds",
                           font=self.F['sm'], fg=Theme.CYAN, bg=Theme.BG, cursor='hand2')
            back.pack()
            back.bind('<Button-1>', lambda e: self._show_db_grid())
            return

        # Back link
        back = tk.Label(self.db_inner, text="← Back to all breeds",
                       font=self.F['sm'], fg=Theme.CYAN, bg=Theme.BG, cursor='hand2')
        back.pack(anchor='w', pady=(0, self.s(15)))
        back.bind('<Button-1>', lambda e: self._show_db_grid())

        # Info card
        card = self.glass_card(self.db_inner)
        card.pack(fill='x')

        inner = tk.Frame(card, bg=Theme.CARD)
        inner.pack(fill='x', padx=self.s(30), pady=self.s(30))

        tk.Label(inner, text=info['name'], font=self.F['h1'],
                fg=Theme.CYAN, bg=Theme.CARD).pack(anchor='w')

        subtitle = f"{info['group']}  •  {info['origin']}  •  {info['lifespan']}"
        tk.Label(inner, text=subtitle, font=self.F['sm'],
                fg=Theme.TEXT2, bg=Theme.CARD).pack(anchor='w', pady=(self.s(5), self.s(20)))

        details = [
            ("Size", info['size']['weight']),
            ("Temperament", ", ".join(info['temperament'][:3])),
            ("Exercise Needs", info['exercise']),
            ("Grooming", info['grooming']),
        ]

        for label, value in details:
            row = tk.Frame(inner, bg=Theme.CARD)
            row.pack(fill='x', pady=self.s(4))

            tk.Label(row, text=label, font=self.F['sm'], fg=Theme.MUTED,
                    bg=Theme.CARD, width=16, anchor='w').pack(side='left')
            tk.Label(row, text=value, font=self.F['sm'], fg=Theme.TEXT,
                    bg=Theme.CARD).pack(side='left')

    # ══════════════════════════════════════════════════════════════════
    # BREED POPUP
    # ══════════════════════════════════════════════════════════════════

    def _show_breed_popup(self, name):
        info = get_breed_info(name)
        if not info:
            messagebox.showinfo("Info", f"No detailed information for {name}")
            return

        popup = tk.Toplevel(self.root)
        popup.title(info['name'])

        pw, ph = min(self.s(480), self.w - 100), min(self.s(520), self.h - 100)
        px = self.root.winfo_x() + (self.w - pw) // 2
        py = self.root.winfo_y() + (self.h - ph) // 2
        popup.geometry(f"{pw}x{ph}+{px}+{py}")
        popup.configure(bg=Theme.BG)
        popup.transient(self.root)
        popup.grab_set()

        # Content
        content = tk.Frame(popup, bg=Theme.BG)
        content.pack(fill='both', expand=True, padx=self.s(25), pady=self.s(25))

        # Header
        tk.Label(content, text=info['name'], font=self.F['h1'],
                fg=Theme.CYAN, bg=Theme.BG).pack(anchor='w')

        subtitle = f"{info['group']}  •  {info['origin']}"
        tk.Label(content, text=subtitle, font=self.F['sm'],
                fg=Theme.TEXT2, bg=Theme.BG).pack(anchor='w', pady=(self.s(5), self.s(20)))

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
            row.pack(fill='x', pady=self.s(5))

            tk.Label(row, text=label, font=self.F['sm'], fg=Theme.CYAN,
                    bg=Theme.BG, width=14, anchor='w').pack(side='left')
            tk.Label(row, text=value, font=self.F['sm'], fg=Theme.TEXT,
                    bg=Theme.BG, wraplength=self.s(280)).pack(side='left', fill='x')

        # Fun fact card
        fact_card = tk.Frame(content, bg=Theme.CARD)
        fact_card.pack(fill='x', pady=self.s(20))

        fact_inner = tk.Frame(fact_card, bg=Theme.CARD)
        fact_inner.pack(fill='x', padx=self.s(15), pady=self.s(15))

        tk.Label(fact_inner, text="Fun Fact", font=self.F['sm'],
                fg=Theme.ORANGE, bg=Theme.CARD).pack(anchor='w')
        tk.Label(fact_inner, text=info['fun_fact'], font=self.F['xs'],
                fg=Theme.TEXT, bg=Theme.CARD,
                wraplength=self.s(380), justify='left').pack(anchor='w', pady=(self.s(5), 0))

        # Buttons
        btn_frame = tk.Frame(content, bg=Theme.BG)
        btn_frame.pack(pady=self.s(15))

        search_url = f"https://www.google.com/search?tbm=isch&q={info['name'].replace(' ', '+')}+dog"

        self.pill_btn(btn_frame, "View Images",
                     lambda: webbrowser.open(search_url), Theme.PINK).pack(side='left', padx=self.s(5))
        self.ghost_btn(btn_frame, "Close", popup.destroy).pack(side='left', padx=self.s(5))


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
