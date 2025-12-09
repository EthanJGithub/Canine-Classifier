#!/usr/bin/env python3
"""
Canine Classifier - Ultra-Modern GUI Application
A sleek, iOS-inspired dog breed identification tool with AI-powered recognition.
2025 Design Language
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
import sys
import threading
import math

# Import breed info
try:
    from breed_info import BREED_INFO, get_breed_info
    BREED_INFO_AVAILABLE = True
except ImportError:
    BREED_INFO_AVAILABLE = False
    BREED_INFO = {}
    def get_breed_info(breed): return None


class ModernTheme:
    """2025 iOS-inspired design system."""

    # Background colors - deep dark with subtle blue
    BG_PRIMARY = "#0a0a0f"
    BG_SECONDARY = "#12121a"
    BG_TERTIARY = "#1a1a24"
    BG_CARD = "#1e1e2a"
    BG_CARD_HOVER = "#252532"
    BG_INPUT = "#16161e"

    # Accent colors - vibrant gradients
    ACCENT_BLUE = "#0ea5e9"
    ACCENT_CYAN = "#22d3ee"
    ACCENT_PURPLE = "#a855f7"
    ACCENT_PINK = "#ec4899"
    ACCENT_GREEN = "#10b981"
    ACCENT_ORANGE = "#f59e0b"
    ACCENT_RED = "#ef4444"

    # Text colors
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#94a3b8"
    TEXT_MUTED = "#64748b"
    TEXT_ACCENT = "#38bdf8"

    # Border and effects
    BORDER_SUBTLE = "#2a2a3a"
    BORDER_ACCENT = "#3b82f6"
    GLOW_BLUE = "#0ea5e9"

    # Fonts - Clean modern sans-serif
    FONT_DISPLAY = ("Segoe UI", 32, "bold")
    FONT_TITLE = ("Segoe UI", 22, "bold")
    FONT_HEADING = ("Segoe UI", 16, "bold")
    FONT_SUBHEADING = ("Segoe UI", 14)
    FONT_BODY = ("Segoe UI", 12)
    FONT_CAPTION = ("Segoe UI", 10)
    FONT_SMALL = ("Segoe UI", 9)

    # Dimensions
    CORNER_RADIUS = 16
    CARD_PADDING = 24
    BUTTON_HEIGHT = 48
    INPUT_HEIGHT = 44


class RoundedFrame(tk.Canvas):
    """A frame with rounded corners."""

    def __init__(self, parent, bg_color, corner_radius=16, border_color=None, border_width=0, **kwargs):
        super().__init__(parent, highlightthickness=0, bg=parent.cget('bg'), **kwargs)
        self.bg_color = bg_color
        self.corner_radius = corner_radius
        self.border_color = border_color
        self.border_width = border_width
        self._frame = None

        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        self.delete("rounded_rect")
        self._draw_rounded_rect(event.width, event.height)

    def _draw_rounded_rect(self, width, height):
        r = self.corner_radius

        # Draw rounded rectangle
        self.create_polygon(
            r, 0,
            width - r, 0,
            width, 0,
            width, r,
            width, height - r,
            width, height,
            width - r, height,
            r, height,
            0, height,
            0, height - r,
            0, r,
            0, 0,
            r, 0,
            smooth=True,
            fill=self.bg_color,
            outline=self.border_color if self.border_color else "",
            width=self.border_width,
            tags="rounded_rect"
        )

    def get_inner_frame(self):
        if not self._frame:
            self._frame = tk.Frame(self, bg=self.bg_color)
            self.create_window(self.corner_radius, self.corner_radius,
                             window=self._frame, anchor="nw", tags="inner_frame")
        return self._frame


class GlowButton(tk.Canvas):
    """Modern button with glow effect on hover."""

    def __init__(self, parent, text, command, bg_color=ModernTheme.ACCENT_BLUE,
                 fg_color=ModernTheme.TEXT_PRIMARY, width=200, height=48, **kwargs):
        super().__init__(parent, width=width, height=height,
                        highlightthickness=0, bg=parent.cget('bg'), **kwargs)

        self.text = text
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.btn_width = width
        self.btn_height = height
        self.is_hovered = False

        self._draw_button()

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.config(cursor="hand2")

    def _draw_button(self):
        self.delete("all")

        r = 12  # Corner radius
        w, h = self.btn_width, self.btn_height

        # Glow effect when hovered
        if self.is_hovered:
            for i in range(3):
                offset = (3 - i) * 2
                alpha_color = self._blend_color(self.bg_color, ModernTheme.BG_PRIMARY, 0.3 + i * 0.2)
                self.create_oval(-offset, -offset, w + offset, h + offset,
                               fill="", outline=alpha_color, width=2)

        # Button background
        points = self._get_rounded_rect_points(0, 0, w, h, r)
        self.create_polygon(points, fill=self.bg_color, smooth=True, outline="")

        # Button text
        self.create_text(w // 2, h // 2, text=self.text,
                        font=ModernTheme.FONT_HEADING, fill=self.fg_color)

    def _get_rounded_rect_points(self, x1, y1, x2, y2, r):
        return [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1,
        ]

    def _blend_color(self, color1, color2, ratio):
        """Blend two colors."""
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        r = int(r1 * ratio + r2 * (1 - ratio))
        g = int(g1 * ratio + g2 * (1 - ratio))
        b = int(b1 * ratio + b2 * (1 - ratio))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _on_enter(self, event):
        self.is_hovered = True
        self._draw_button()

    def _on_leave(self, event):
        self.is_hovered = False
        self._draw_button()

    def _on_click(self, event):
        if self.command:
            self.command()


class ModernCard(tk.Frame):
    """Modern card component with subtle border and hover effect."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=ModernTheme.BG_CARD, **kwargs)
        self.default_bg = ModernTheme.BG_CARD
        self.hover_bg = ModernTheme.BG_CARD_HOVER

    def enable_hover(self):
        self.bind("<Enter>", lambda e: self.config(bg=self.hover_bg))
        self.bind("<Leave>", lambda e: self.config(bg=self.default_bg))
        self.config(cursor="hand2")


class Database:
    """Database handler for dog breeds."""
    def __init__(self):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dog_database.db')
        self.db = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.db.cursor()

    def fetch_dog_breeds(self, color, ear_type, tail_type, size, coat_type):
        query = """
        SELECT DogBreeds.BreedName,
               SUM(CASE WHEN DogColors.ColorName = ? THEN 1 ELSE 0 END +
                   CASE WHEN DogBreeds.CoatType = ? THEN 1 ELSE 0 END +
                   CASE WHEN DogBreeds.EarType = ? THEN 1 ELSE 0 END +
                   CASE WHEN DogBreeds.TailType = ? THEN 1 ELSE 0 END +
                   CASE WHEN DogBreeds.Size = ? THEN 1 ELSE 0 END) AS MatchedAttributes,
               ROUND((SUM(CASE WHEN DogColors.ColorName = ? THEN 1 ELSE 0 END +
                          CASE WHEN DogBreeds.CoatType = ? THEN 1 ELSE 0 END +
                          CASE WHEN DogBreeds.EarType = ? THEN 1 ELSE 0 END +
                          CASE WHEN DogBreeds.TailType = ? THEN 1 ELSE 0 END +
                          CASE WHEN DogBreeds.Size = ? THEN 1 ELSE 0 END) / 5.0) * 100, 2) AS Probability
        FROM DogBreeds
        LEFT JOIN BreedColors ON DogBreeds.BreedID = BreedColors.BreedID
        LEFT JOIN DogColors ON BreedColors.ColorID = DogColors.ColorID
        WHERE DogColors.ColorName = ? OR DogColors.ColorName IS NULL
        GROUP BY DogBreeds.BreedName
        ORDER BY MatchedAttributes DESC, DogBreeds.BreedName
        LIMIT 3;
        """
        try:
            self.cursor.execute(query, (color, coat_type, ear_type, tail_type, size,
                                       color, coat_type, ear_type, tail_type, size, color))
            return self.cursor.fetchall()
        except sqlite3.Error as err:
            print(f"Database error: {err}")
            return []

    def close(self):
        self.cursor.close()
        self.db.close()


class CanineClassifierApp:
    """Ultra-modern GUI Application for Canine Classifier."""

    def __init__(self, root):
        self.root = root
        self.root.title("Canine Classifier")
        self.root.geometry("1100x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg=ModernTheme.BG_PRIMARY)

        # Remove window decorations for cleaner look (optional)
        # self.root.overrideredirect(True)

        # Center window
        self.center_window()

        # Current frame reference
        self.current_frame = None

        # Dichotomous key state
        self.dkey_tree = self._build_dichotomous_tree()
        self.dkey_current_node = None
        self.dkey_question_count = 0

        # AI classifier (lazy loaded)
        self.classifier = None

        # Configure styles
        self.configure_styles()

        # Show main menu
        self.show_main_menu()

    def center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        width = 1100
        height = 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def configure_styles(self):
        """Configure ttk styles for modern look."""
        style = ttk.Style()
        style.theme_use('clam')

        # Combobox style
        style.configure('Modern.TCombobox',
                       fieldbackground=ModernTheme.BG_INPUT,
                       background=ModernTheme.BG_INPUT,
                       foreground=ModernTheme.TEXT_PRIMARY,
                       arrowcolor=ModernTheme.TEXT_SECONDARY,
                       borderwidth=0,
                       padding=12)

        style.map('Modern.TCombobox',
                 fieldbackground=[('readonly', ModernTheme.BG_INPUT)],
                 selectbackground=[('readonly', ModernTheme.ACCENT_BLUE)],
                 selectforeground=[('readonly', ModernTheme.TEXT_PRIMARY)])

        # Scrollbar style
        style.configure('Modern.Vertical.TScrollbar',
                       background=ModernTheme.BG_TERTIARY,
                       troughcolor=ModernTheme.BG_SECONDARY,
                       borderwidth=0,
                       arrowsize=0)

    def clear_frame(self):
        """Clear the current frame."""
        if self.current_frame:
            self.current_frame.destroy()

    def create_nav_header(self, parent, show_back=True):
        """Create navigation header."""
        nav = tk.Frame(parent, bg=ModernTheme.BG_PRIMARY, height=60)
        nav.pack(fill=tk.X, padx=30, pady=(20, 0))
        nav.pack_propagate(False)

        if show_back:
            back_btn = tk.Label(nav, text="<  Back", font=ModernTheme.FONT_BODY,
                               fg=ModernTheme.ACCENT_BLUE, bg=ModernTheme.BG_PRIMARY,
                               cursor="hand2")
            back_btn.pack(side=tk.LEFT, pady=15)
            back_btn.bind("<Button-1>", lambda e: self.show_main_menu())
            back_btn.bind("<Enter>", lambda e: back_btn.config(fg=ModernTheme.ACCENT_CYAN))
            back_btn.bind("<Leave>", lambda e: back_btn.config(fg=ModernTheme.ACCENT_BLUE))

        return nav

    def create_page_title(self, parent, title, subtitle=""):
        """Create page title section."""
        title_frame = tk.Frame(parent, bg=ModernTheme.BG_PRIMARY)
        title_frame.pack(fill=tk.X, padx=30, pady=(10, 20))

        title_label = tk.Label(title_frame, text=title,
                              font=ModernTheme.FONT_TITLE,
                              fg=ModernTheme.TEXT_PRIMARY,
                              bg=ModernTheme.BG_PRIMARY)
        title_label.pack(anchor="w")

        if subtitle:
            sub_label = tk.Label(title_frame, text=subtitle,
                                font=ModernTheme.FONT_BODY,
                                fg=ModernTheme.TEXT_SECONDARY,
                                bg=ModernTheme.BG_PRIMARY)
            sub_label.pack(anchor="w", pady=(5, 0))

        return title_frame

    # ==================== MAIN MENU ====================

    def show_main_menu(self):
        """Display the ultra-modern main menu."""
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=ModernTheme.BG_PRIMARY)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        # Header section
        header = tk.Frame(self.current_frame, bg=ModernTheme.BG_PRIMARY)
        header.pack(fill=tk.X, padx=50, pady=(60, 40))

        # App title with gradient effect (simulated)
        title_label = tk.Label(header, text="Canine Classifier",
                              font=ModernTheme.FONT_DISPLAY,
                              fg=ModernTheme.ACCENT_CYAN,
                              bg=ModernTheme.BG_PRIMARY)
        title_label.pack()

        subtitle_label = tk.Label(header, text="AI-Powered Dog Breed Identification",
                                 font=ModernTheme.FONT_SUBHEADING,
                                 fg=ModernTheme.TEXT_SECONDARY,
                                 bg=ModernTheme.BG_PRIMARY)
        subtitle_label.pack(pady=(8, 0))

        # Menu cards container
        cards_frame = tk.Frame(self.current_frame, bg=ModernTheme.BG_PRIMARY)
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)

        # Configure grid
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        cards_frame.grid_rowconfigure(0, weight=1)
        cards_frame.grid_rowconfigure(1, weight=1)

        # Menu items
        menu_items = [
            ("AI Recognition", "Upload a photo for instant breed detection",
             ModernTheme.ACCENT_BLUE, self.show_image_recognition, "01"),
            ("Questionnaire", "Answer questions about your dog's features",
             ModernTheme.ACCENT_PURPLE, self.show_questionnaire, "02"),
            ("Dichotomous Key", "Scientific Yes/No identification method",
             ModernTheme.ACCENT_GREEN, self.show_dichotomous_key, "03"),
            ("Breed Database", "Explore detailed info on 51+ breeds",
             ModernTheme.ACCENT_ORANGE, self.show_breed_lookup, "04"),
        ]

        for idx, (title, desc, color, command, num) in enumerate(menu_items):
            row, col = divmod(idx, 2)
            self._create_menu_card(cards_frame, title, desc, color, command, num, row, col)

        # Footer
        footer = tk.Label(self.current_frame,
                         text="v2.0  |  51 Breeds  |  AI Powered",
                         font=ModernTheme.FONT_CAPTION,
                         fg=ModernTheme.TEXT_MUTED,
                         bg=ModernTheme.BG_PRIMARY)
        footer.pack(side=tk.BOTTOM, pady=20)

    def _create_menu_card(self, parent, title, desc, accent_color, command, num, row, col):
        """Create a modern menu card."""
        # Card container
        card = tk.Frame(parent, bg=ModernTheme.BG_CARD, cursor="hand2")
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Inner content with padding
        inner = tk.Frame(card, bg=ModernTheme.BG_CARD)
        inner.pack(fill=tk.BOTH, expand=True, padx=28, pady=28)

        # Number indicator
        num_label = tk.Label(inner, text=num,
                            font=("Segoe UI", 36, "bold"),
                            fg=accent_color,
                            bg=ModernTheme.BG_CARD)
        num_label.pack(anchor="w")

        # Title
        title_label = tk.Label(inner, text=title,
                              font=ModernTheme.FONT_HEADING,
                              fg=ModernTheme.TEXT_PRIMARY,
                              bg=ModernTheme.BG_CARD)
        title_label.pack(anchor="w", pady=(15, 5))

        # Description
        desc_label = tk.Label(inner, text=desc,
                             font=ModernTheme.FONT_BODY,
                             fg=ModernTheme.TEXT_SECONDARY,
                             bg=ModernTheme.BG_CARD)
        desc_label.pack(anchor="w")

        # Arrow indicator
        arrow_label = tk.Label(inner, text="→",
                              font=("Segoe UI", 20),
                              fg=accent_color,
                              bg=ModernTheme.BG_CARD)
        arrow_label.pack(anchor="e", side=tk.BOTTOM)

        # Hover effects
        def on_enter(e):
            card.config(bg=ModernTheme.BG_CARD_HOVER)
            inner.config(bg=ModernTheme.BG_CARD_HOVER)
            for widget in inner.winfo_children():
                widget.config(bg=ModernTheme.BG_CARD_HOVER)

        def on_leave(e):
            card.config(bg=ModernTheme.BG_CARD)
            inner.config(bg=ModernTheme.BG_CARD)
            for widget in inner.winfo_children():
                widget.config(bg=ModernTheme.BG_CARD)

        # Bind events to all widgets
        for widget in [card, inner, num_label, title_label, desc_label, arrow_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", lambda e, cmd=command: cmd())

    # ==================== AI IMAGE RECOGNITION ====================

    def show_image_recognition(self):
        """Display the AI image recognition page."""
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=ModernTheme.BG_PRIMARY)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        self.create_nav_header(self.current_frame)
        self.create_page_title(self.current_frame, "AI Recognition",
                              "Upload a photo to identify your dog's breed")

        # Content area
        content = tk.Frame(self.current_frame, bg=ModernTheme.BG_PRIMARY)
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        # Upload card
        upload_card = tk.Frame(content, bg=ModernTheme.BG_CARD)
        upload_card.pack(fill=tk.X, pady=10)

        upload_inner = tk.Frame(upload_card, bg=ModernTheme.BG_CARD)
        upload_inner.pack(fill=tk.X, padx=30, pady=30)

        # Upload icon
        icon_frame = tk.Frame(upload_inner, bg=ModernTheme.BG_TERTIARY, width=80, height=80)
        icon_frame.pack(pady=(0, 15))
        icon_frame.pack_propagate(False)

        icon_label = tk.Label(icon_frame, text="+",
                             font=("Segoe UI", 32),
                             fg=ModernTheme.ACCENT_BLUE,
                             bg=ModernTheme.BG_TERTIARY)
        icon_label.place(relx=0.5, rely=0.5, anchor="center")

        # File path display
        self.image_path_var = tk.StringVar(value="No file selected")
        path_label = tk.Label(upload_inner, textvariable=self.image_path_var,
                             font=ModernTheme.FONT_BODY,
                             fg=ModernTheme.TEXT_SECONDARY,
                             bg=ModernTheme.BG_CARD)
        path_label.pack(pady=5)

        # Browse button
        browse_btn = tk.Frame(upload_inner, bg=ModernTheme.BG_TERTIARY, cursor="hand2")
        browse_btn.pack(pady=15)

        browse_label = tk.Label(browse_btn, text="  Browse Files  ",
                               font=ModernTheme.FONT_BODY,
                               fg=ModernTheme.TEXT_PRIMARY,
                               bg=ModernTheme.BG_TERTIARY,
                               padx=20, pady=10)
        browse_label.pack()

        browse_btn.bind("<Button-1>", lambda e: self.browse_image())
        browse_label.bind("<Button-1>", lambda e: self.browse_image())

        # Classify button
        self.classify_btn_frame = tk.Frame(content, bg=ModernTheme.ACCENT_BLUE, cursor="hand2")
        self.classify_btn_frame.pack(pady=20)

        self.classify_label = tk.Label(self.classify_btn_frame, text="  Analyze Image  ",
                                      font=ModernTheme.FONT_HEADING,
                                      fg=ModernTheme.TEXT_PRIMARY,
                                      bg=ModernTheme.ACCENT_BLUE,
                                      padx=30, pady=12)
        self.classify_label.pack()

        self.classify_btn_frame.bind("<Button-1>", lambda e: self.classify_image())
        self.classify_label.bind("<Button-1>", lambda e: self.classify_image())

        # Status
        self.ai_status_var = tk.StringVar(value="")
        self.ai_status_label = tk.Label(content, textvariable=self.ai_status_var,
                                       font=ModernTheme.FONT_BODY,
                                       fg=ModernTheme.ACCENT_CYAN,
                                       bg=ModernTheme.BG_PRIMARY)
        self.ai_status_label.pack(pady=5)

        # Results area with scrolling
        results_container = tk.Frame(content, bg=ModernTheme.BG_PRIMARY)
        results_container.pack(fill=tk.BOTH, expand=True, pady=10)

        self.ai_canvas = tk.Canvas(results_container, bg=ModernTheme.BG_PRIMARY,
                                  highlightthickness=0)
        scrollbar = ttk.Scrollbar(results_container, orient="vertical",
                                 command=self.ai_canvas.yview)

        self.ai_results_frame = tk.Frame(self.ai_canvas, bg=ModernTheme.BG_PRIMARY)

        self.ai_canvas.create_window((0, 0), window=self.ai_results_frame, anchor="nw")
        self.ai_canvas.configure(yscrollcommand=scrollbar.set)

        self.ai_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.ai_results_frame.bind("<Configure>",
            lambda e: self.ai_canvas.configure(scrollregion=self.ai_canvas.bbox("all")))

        # Store image path
        self.selected_image_path = None

    def browse_image(self):
        """Open file dialog to select an image."""
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.webp"),
            ("All files", "*.*")
        ]
        filepath = filedialog.askopenfilename(title="Select Dog Image", filetypes=filetypes)

        if filepath:
            self.selected_image_path = filepath
            filename = os.path.basename(filepath)
            if len(filename) > 40:
                filename = filename[:37] + "..."
            self.image_path_var.set(filename)

    def classify_image(self):
        """Classify the selected image using AI."""
        if not self.selected_image_path:
            self.ai_status_var.set("Please select an image first")
            return

        # Clear previous results
        for widget in self.ai_results_frame.winfo_children():
            widget.destroy()

        self.ai_status_var.set("Analyzing image...")
        self.root.update()

        # Run classification in thread
        thread = threading.Thread(target=self._run_classification)
        thread.start()

    def _run_classification(self):
        """Run the classification in a background thread."""
        try:
            from image_classifier import DogImageClassifier

            if not self.classifier:
                self.classifier = DogImageClassifier()

            results = self.classifier.classify_image(self.selected_image_path)
            self.root.after(0, lambda: self._display_ai_results(results))

        except ImportError as e:
            error_msg = "AI module not available. Install: pip install transformers torch torchvision Pillow"
            self.root.after(0, lambda: self.ai_status_var.set(error_msg))
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self.ai_status_var.set(error_msg))

    def _display_ai_results(self, results):
        """Display AI classification results."""
        self.ai_status_var.set("")

        for widget in self.ai_results_frame.winfo_children():
            widget.destroy()

        if not results:
            self.ai_status_var.set("Could not classify the image")
            return

        # Results header
        header = tk.Label(self.ai_results_frame, text="Results",
                        font=ModernTheme.FONT_HEADING,
                        fg=ModernTheme.TEXT_PRIMARY,
                        bg=ModernTheme.BG_PRIMARY)
        header.pack(anchor="w", pady=(0, 15))

        colors = [ModernTheme.ACCENT_BLUE, ModernTheme.ACCENT_CYAN,
                 ModernTheme.ACCENT_GREEN, ModernTheme.ACCENT_ORANGE, ModernTheme.ACCENT_PURPLE]

        for i, result in enumerate(results[:5]):
            breed = result.get('breed', 'Unknown')
            confidence = result.get('confidence', 0)
            verified = result.get('verified', False)
            db_name = result.get('db_name', breed)

            # Result card
            card = tk.Frame(self.ai_results_frame, bg=ModernTheme.BG_CARD, cursor="hand2")
            card.pack(fill=tk.X, pady=5)

            inner = tk.Frame(card, bg=ModernTheme.BG_CARD)
            inner.pack(fill=tk.X, padx=20, pady=15)

            # Left side - rank and name
            left = tk.Frame(inner, bg=ModernTheme.BG_CARD)
            left.pack(side=tk.LEFT, fill=tk.X, expand=True)

            # Rank number
            rank_label = tk.Label(left, text=f"#{i+1}",
                                 font=ModernTheme.FONT_HEADING,
                                 fg=colors[i],
                                 bg=ModernTheme.BG_CARD)
            rank_label.pack(side=tk.LEFT, padx=(0, 15))

            # Breed name and status
            name_frame = tk.Frame(left, bg=ModernTheme.BG_CARD)
            name_frame.pack(side=tk.LEFT)

            display_name = db_name if verified else breed
            name_label = tk.Label(name_frame, text=display_name,
                                 font=ModernTheme.FONT_BODY,
                                 fg=ModernTheme.TEXT_PRIMARY,
                                 bg=ModernTheme.BG_CARD)
            name_label.pack(anchor="w")

            status_text = "Verified in database" if verified else "AI prediction"
            status_color = ModernTheme.ACCENT_GREEN if verified else ModernTheme.TEXT_MUTED
            status_label = tk.Label(name_frame, text=status_text,
                                   font=ModernTheme.FONT_CAPTION,
                                   fg=status_color,
                                   bg=ModernTheme.BG_CARD)
            status_label.pack(anchor="w")

            # Right side - confidence
            right = tk.Frame(inner, bg=ModernTheme.BG_CARD)
            right.pack(side=tk.RIGHT)

            # Confidence bar
            bar_bg = tk.Frame(right, bg=ModernTheme.BG_TERTIARY, width=120, height=8)
            bar_bg.pack(side=tk.LEFT, padx=(0, 10))
            bar_bg.pack_propagate(False)

            bar_width = int(120 * confidence / 100)
            bar_fill = tk.Frame(bar_bg, bg=colors[i], width=bar_width, height=8)
            bar_fill.place(x=0, y=0)

            conf_label = tk.Label(right, text=f"{confidence:.0f}%",
                                 font=ModernTheme.FONT_BODY,
                                 fg=ModernTheme.TEXT_PRIMARY,
                                 bg=ModernTheme.BG_CARD,
                                 width=5)
            conf_label.pack(side=tk.LEFT)

            # Click handler
            def on_click(e, b=display_name):
                self.show_breed_info_popup(b)

            for widget in [card, inner, left, right, rank_label, name_frame,
                          name_label, status_label, conf_label]:
                widget.bind("<Button-1>", on_click)

    # ==================== QUESTIONNAIRE ====================

    def show_questionnaire(self):
        """Display the questionnaire page."""
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=ModernTheme.BG_PRIMARY)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        self.create_nav_header(self.current_frame)
        self.create_page_title(self.current_frame, "Questionnaire",
                              "Select your dog's physical characteristics")

        # Content with scroll
        content = tk.Frame(self.current_frame, bg=ModernTheme.BG_PRIMARY)
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        # Questions card
        form_card = tk.Frame(content, bg=ModernTheme.BG_CARD)
        form_card.pack(fill=tk.X, pady=10)

        form_inner = tk.Frame(form_card, bg=ModernTheme.BG_CARD)
        form_inner.pack(fill=tk.X, padx=30, pady=25)

        # Question data
        self.q_vars = {}
        questions = [
            ("color", "Color", ["Black", "White", "Brown", "Tan", "Brindle", "Merle", "Chocolate", "Yellow"]),
            ("ear_type", "Ear Type", ["Floppy", "Tall", "Triangular"]),
            ("tail_type", "Tail Type", ["Docked", "Long_and_curved", "Curled"]),
            ("size", "Size", ["Small", "Medium", "Large", "Giant"]),
            ("coat_type", "Coat Type", ["Short", "Medium", "Long", "Curly", "Double", "Smooth", "Dense", "Silky"]),
        ]

        for key, label, options in questions:
            q_frame = tk.Frame(form_inner, bg=ModernTheme.BG_CARD)
            q_frame.pack(fill=tk.X, pady=10)

            label_widget = tk.Label(q_frame, text=label,
                                   font=ModernTheme.FONT_BODY,
                                   fg=ModernTheme.TEXT_SECONDARY,
                                   bg=ModernTheme.BG_CARD)
            label_widget.pack(anchor="w", pady=(0, 5))

            var = tk.StringVar(value=options[0])
            self.q_vars[key] = var

            combo = ttk.Combobox(q_frame, textvariable=var, values=options,
                                state="readonly", font=ModernTheme.FONT_BODY, width=35)
            combo.pack(anchor="w")

        # Submit button
        submit_frame = tk.Frame(content, bg=ModernTheme.ACCENT_PURPLE, cursor="hand2")
        submit_frame.pack(pady=20)

        submit_label = tk.Label(submit_frame, text="  Find Matches  ",
                               font=ModernTheme.FONT_HEADING,
                               fg=ModernTheme.TEXT_PRIMARY,
                               bg=ModernTheme.ACCENT_PURPLE,
                               padx=30, pady=12)
        submit_label.pack()

        submit_frame.bind("<Button-1>", lambda e: self.process_questionnaire())
        submit_label.bind("<Button-1>", lambda e: self.process_questionnaire())

        # Results area
        self.q_results_frame = tk.Frame(content, bg=ModernTheme.BG_PRIMARY)
        self.q_results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    def process_questionnaire(self):
        """Process questionnaire and show results."""
        for widget in self.q_results_frame.winfo_children():
            widget.destroy()

        color = self.q_vars["color"].get()
        ear_type = self.q_vars["ear_type"].get().lower()
        tail_type = self.q_vars["tail_type"].get().lower()
        size = self.q_vars["size"].get().lower()
        coat_type = self.q_vars["coat_type"].get().lower()

        db = Database()
        results = db.fetch_dog_breeds(color, ear_type, tail_type, size, coat_type)
        db.close()

        if results:
            header = tk.Label(self.q_results_frame, text="Matches",
                            font=ModernTheme.FONT_HEADING,
                            fg=ModernTheme.TEXT_PRIMARY,
                            bg=ModernTheme.BG_PRIMARY)
            header.pack(anchor="w", pady=(10, 15))

            colors = [ModernTheme.ACCENT_GREEN, ModernTheme.ACCENT_CYAN, ModernTheme.ACCENT_ORANGE]

            for i, (breed, matched, probability) in enumerate(results):
                card = tk.Frame(self.q_results_frame, bg=ModernTheme.BG_CARD, cursor="hand2")
                card.pack(fill=tk.X, pady=5)

                inner = tk.Frame(card, bg=ModernTheme.BG_CARD)
                inner.pack(fill=tk.X, padx=20, pady=15)

                # Rank
                rank = tk.Label(inner, text=f"#{i+1}",
                               font=ModernTheme.FONT_HEADING,
                               fg=colors[i] if i < 3 else ModernTheme.TEXT_MUTED,
                               bg=ModernTheme.BG_CARD)
                rank.pack(side=tk.LEFT, padx=(0, 15))

                # Name
                name = tk.Label(inner, text=breed,
                               font=ModernTheme.FONT_BODY,
                               fg=ModernTheme.TEXT_PRIMARY,
                               bg=ModernTheme.BG_CARD)
                name.pack(side=tk.LEFT)

                # Score
                score = tk.Label(inner, text=f"{probability:.0f}%  ({int(matched)}/5)",
                                font=ModernTheme.FONT_BODY,
                                fg=ModernTheme.TEXT_SECONDARY,
                                bg=ModernTheme.BG_CARD)
                score.pack(side=tk.RIGHT)

                for w in [card, inner, rank, name, score]:
                    w.bind("<Button-1>", lambda e, b=breed: self.show_breed_info_popup(b))
        else:
            no_results = tk.Label(self.q_results_frame,
                                text="No matching breeds found",
                                font=ModernTheme.FONT_BODY,
                                fg=ModernTheme.TEXT_MUTED,
                                bg=ModernTheme.BG_PRIMARY)
            no_results.pack(pady=20)

    # ==================== DICHOTOMOUS KEY ====================

    def _build_dichotomous_tree(self):
        """Build the dichotomous key decision tree."""
        return {
            "question": "Is your dog small (under 25 lbs)?",
            "yes": {
                "question": "Does your dog have floppy ears?",
                "yes": {
                    "question": "Does your dog have a long coat?",
                    "yes": {"result": "Shih Tzu"},
                    "no": {"result": "Cavalier King Charles Spaniel"}
                },
                "no": {
                    "question": "Does your dog have a long coat?",
                    "yes": {"result": "Pomeranian"},
                    "no": {"result": "Chihuahua"}
                }
            },
            "no": {
                "question": "Is your dog giant sized (over 100 lbs)?",
                "yes": {
                    "question": "Does your dog have a short coat?",
                    "yes": {"result": "Great Dane"},
                    "no": {"result": "Saint Bernard"}
                },
                "no": {
                    "question": "Is your dog large (50-100 lbs)?",
                    "yes": {
                        "question": "Does your dog have floppy ears?",
                        "yes": {"result": "Labrador Retriever"},
                        "no": {"result": "German Shepherd"}
                    },
                    "no": {
                        "question": "Does your dog have a curly coat?",
                        "yes": {"result": "Poodle"},
                        "no": {"result": "Beagle"}
                    }
                }
            }
        }

    def show_dichotomous_key(self):
        """Display the dichotomous key page."""
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=ModernTheme.BG_PRIMARY)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        self.create_nav_header(self.current_frame)
        self.create_page_title(self.current_frame, "Dichotomous Key",
                              "Answer Yes/No questions to identify your dog")

        # Content area
        self.dkey_content = tk.Frame(self.current_frame, bg=ModernTheme.BG_PRIMARY)
        self.dkey_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        # Initialize
        self.dkey_current_node = self.dkey_tree
        self.dkey_question_count = 0

        self._show_dkey_question()

    def _show_dkey_question(self):
        """Show current question or result."""
        for widget in self.dkey_content.winfo_children():
            widget.destroy()

        node = self.dkey_current_node

        if "result" in node:
            self._show_dkey_result(node["result"])
            return

        self.dkey_question_count += 1

        # Progress indicator
        progress = tk.Label(self.dkey_content,
                           text=f"Question {self.dkey_question_count}",
                           font=ModernTheme.FONT_CAPTION,
                           fg=ModernTheme.ACCENT_GREEN,
                           bg=ModernTheme.BG_PRIMARY)
        progress.pack(anchor="w", pady=(0, 20))

        # Question card
        q_card = tk.Frame(self.dkey_content, bg=ModernTheme.BG_CARD)
        q_card.pack(fill=tk.X, pady=10)

        q_inner = tk.Frame(q_card, bg=ModernTheme.BG_CARD)
        q_inner.pack(fill=tk.X, padx=30, pady=40)

        q_label = tk.Label(q_inner, text=node["question"],
                          font=ModernTheme.FONT_TITLE,
                          fg=ModernTheme.TEXT_PRIMARY,
                          bg=ModernTheme.BG_CARD,
                          wraplength=600)
        q_label.pack()

        # Buttons
        btn_frame = tk.Frame(self.dkey_content, bg=ModernTheme.BG_PRIMARY)
        btn_frame.pack(pady=30)

        # Yes button
        yes_btn = tk.Frame(btn_frame, bg=ModernTheme.ACCENT_GREEN, cursor="hand2")
        yes_btn.pack(side=tk.LEFT, padx=15)

        yes_label = tk.Label(yes_btn, text="  Yes  ",
                            font=ModernTheme.FONT_HEADING,
                            fg=ModernTheme.TEXT_PRIMARY,
                            bg=ModernTheme.ACCENT_GREEN,
                            padx=40, pady=15)
        yes_label.pack()

        yes_btn.bind("<Button-1>", lambda e: self._dkey_answer(True))
        yes_label.bind("<Button-1>", lambda e: self._dkey_answer(True))

        # No button
        no_btn = tk.Frame(btn_frame, bg=ModernTheme.ACCENT_RED, cursor="hand2")
        no_btn.pack(side=tk.LEFT, padx=15)

        no_label = tk.Label(no_btn, text="  No  ",
                           font=ModernTheme.FONT_HEADING,
                           fg=ModernTheme.TEXT_PRIMARY,
                           bg=ModernTheme.ACCENT_RED,
                           padx=40, pady=15)
        no_label.pack()

        no_btn.bind("<Button-1>", lambda e: self._dkey_answer(False))
        no_label.bind("<Button-1>", lambda e: self._dkey_answer(False))

        # Restart link
        restart = tk.Label(self.dkey_content, text="Start over",
                          font=ModernTheme.FONT_BODY,
                          fg=ModernTheme.TEXT_MUTED,
                          bg=ModernTheme.BG_PRIMARY,
                          cursor="hand2")
        restart.pack(pady=20)
        restart.bind("<Button-1>", lambda e: self._restart_dkey())

    def _dkey_answer(self, is_yes):
        """Handle answer."""
        self.dkey_current_node = self.dkey_current_node["yes" if is_yes else "no"]
        self._show_dkey_question()

    def _show_dkey_result(self, breed):
        """Show identification result."""
        # Result card
        result_card = tk.Frame(self.dkey_content, bg=ModernTheme.BG_CARD)
        result_card.pack(fill=tk.X, pady=20)

        result_inner = tk.Frame(result_card, bg=ModernTheme.BG_CARD)
        result_inner.pack(padx=40, pady=40)

        # Success indicator
        check = tk.Label(result_inner, text="✓",
                        font=("Segoe UI", 48),
                        fg=ModernTheme.ACCENT_GREEN,
                        bg=ModernTheme.BG_CARD)
        check.pack()

        complete = tk.Label(result_inner, text="Identification Complete",
                           font=ModernTheme.FONT_HEADING,
                           fg=ModernTheme.TEXT_SECONDARY,
                           bg=ModernTheme.BG_CARD)
        complete.pack(pady=(10, 5))

        breed_label = tk.Label(result_inner, text=breed,
                              font=ModernTheme.FONT_DISPLAY,
                              fg=ModernTheme.ACCENT_CYAN,
                              bg=ModernTheme.BG_CARD)
        breed_label.pack(pady=10)

        questions_text = tk.Label(result_inner,
                                 text=f"Identified in {self.dkey_question_count} questions",
                                 font=ModernTheme.FONT_CAPTION,
                                 fg=ModernTheme.TEXT_MUTED,
                                 bg=ModernTheme.BG_CARD)
        questions_text.pack()

        # Action buttons
        btn_frame = tk.Frame(self.dkey_content, bg=ModernTheme.BG_PRIMARY)
        btn_frame.pack(pady=20)

        # View info button
        info_btn = tk.Frame(btn_frame, bg=ModernTheme.ACCENT_BLUE, cursor="hand2")
        info_btn.pack(side=tk.LEFT, padx=10)

        info_label = tk.Label(info_btn, text="  View Breed Info  ",
                             font=ModernTheme.FONT_BODY,
                             fg=ModernTheme.TEXT_PRIMARY,
                             bg=ModernTheme.ACCENT_BLUE,
                             padx=20, pady=10)
        info_label.pack()

        info_btn.bind("<Button-1>", lambda e: self.show_breed_info_popup(breed))
        info_label.bind("<Button-1>", lambda e: self.show_breed_info_popup(breed))

        # Try again button
        again_btn = tk.Frame(btn_frame, bg=ModernTheme.BG_TERTIARY, cursor="hand2")
        again_btn.pack(side=tk.LEFT, padx=10)

        again_label = tk.Label(again_btn, text="  Try Again  ",
                              font=ModernTheme.FONT_BODY,
                              fg=ModernTheme.TEXT_PRIMARY,
                              bg=ModernTheme.BG_TERTIARY,
                              padx=20, pady=10)
        again_label.pack()

        again_btn.bind("<Button-1>", lambda e: self._restart_dkey())
        again_label.bind("<Button-1>", lambda e: self._restart_dkey())

    def _restart_dkey(self):
        """Restart the key."""
        self.dkey_current_node = self.dkey_tree
        self.dkey_question_count = 0
        self._show_dkey_question()

    # ==================== BREED DATABASE ====================

    def show_breed_lookup(self):
        """Display the breed database page."""
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=ModernTheme.BG_PRIMARY)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        self.create_nav_header(self.current_frame)
        self.create_page_title(self.current_frame, "Breed Database",
                              f"Explore detailed information on {len(BREED_INFO)} breeds")

        # Search bar
        search_frame = tk.Frame(self.current_frame, bg=ModernTheme.BG_PRIMARY)
        search_frame.pack(fill=tk.X, padx=30, pady=10)

        breed_names = sorted([info['name'] for info in BREED_INFO.values()]) if BREED_INFO else []

        self.breed_search_var = tk.StringVar()
        search_combo = ttk.Combobox(search_frame, textvariable=self.breed_search_var,
                                   values=breed_names, font=ModernTheme.FONT_BODY, width=40)
        search_combo.pack(side=tk.LEFT)
        search_combo.bind("<<ComboboxSelected>>", lambda e: self._lookup_breed())
        search_combo.bind("<Return>", lambda e: self._lookup_breed())

        search_btn = tk.Frame(search_frame, bg=ModernTheme.ACCENT_BLUE, cursor="hand2")
        search_btn.pack(side=tk.LEFT, padx=15)

        search_label = tk.Label(search_btn, text="  Search  ",
                               font=ModernTheme.FONT_BODY,
                               fg=ModernTheme.TEXT_PRIMARY,
                               bg=ModernTheme.ACCENT_BLUE,
                               padx=15, pady=8)
        search_label.pack()

        search_btn.bind("<Button-1>", lambda e: self._lookup_breed())
        search_label.bind("<Button-1>", lambda e: self._lookup_breed())

        # Results area with scroll
        results_container = tk.Frame(self.current_frame, bg=ModernTheme.BG_PRIMARY)
        results_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        self.breed_canvas = tk.Canvas(results_container, bg=ModernTheme.BG_PRIMARY,
                                     highlightthickness=0)
        scrollbar = ttk.Scrollbar(results_container, orient="vertical",
                                 command=self.breed_canvas.yview)

        self.breed_results_frame = tk.Frame(self.breed_canvas, bg=ModernTheme.BG_PRIMARY)

        self.breed_canvas.create_window((0, 0), window=self.breed_results_frame, anchor="nw")
        self.breed_canvas.configure(yscrollcommand=scrollbar.set)

        self.breed_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.breed_results_frame.bind("<Configure>",
            lambda e: self.breed_canvas.configure(scrollregion=self.breed_canvas.bbox("all")))

        # Show breed grid
        self._show_breed_grid()

    def _show_breed_grid(self):
        """Show grid of all breeds."""
        for widget in self.breed_results_frame.winfo_children():
            widget.destroy()

        if not BREED_INFO:
            return

        # Create grid
        cols = 4
        current_row = None

        for i, (key, info) in enumerate(sorted(BREED_INFO.items())):
            if i % cols == 0:
                current_row = tk.Frame(self.breed_results_frame, bg=ModernTheme.BG_PRIMARY)
                current_row.pack(fill=tk.X, pady=3)

            btn = tk.Frame(current_row, bg=ModernTheme.BG_CARD, cursor="hand2")
            btn.pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)

            label = tk.Label(btn, text=info['name'],
                            font=ModernTheme.FONT_CAPTION,
                            fg=ModernTheme.TEXT_PRIMARY,
                            bg=ModernTheme.BG_CARD,
                            padx=10, pady=12)
            label.pack()

            def on_click(e, b=info['name']):
                self._display_breed_info(b)

            btn.bind("<Button-1>", on_click)
            label.bind("<Button-1>", on_click)

    def _lookup_breed(self):
        """Look up searched breed."""
        breed = self.breed_search_var.get().strip()
        if breed:
            self._display_breed_info(breed)

    def _display_breed_info(self, breed_name):
        """Display breed info inline."""
        info = get_breed_info(breed_name)

        for widget in self.breed_results_frame.winfo_children():
            widget.destroy()

        if not info:
            no_info = tk.Label(self.breed_results_frame,
                              text=f"No info found for '{breed_name}'",
                              font=ModernTheme.FONT_BODY,
                              fg=ModernTheme.TEXT_MUTED,
                              bg=ModernTheme.BG_PRIMARY)
            no_info.pack(pady=20)

            back = tk.Label(self.breed_results_frame, text="← Back to list",
                           font=ModernTheme.FONT_BODY,
                           fg=ModernTheme.ACCENT_BLUE,
                           bg=ModernTheme.BG_PRIMARY,
                           cursor="hand2")
            back.pack()
            back.bind("<Button-1>", lambda e: self._show_breed_grid())
            return

        # Back link
        back = tk.Label(self.breed_results_frame, text="← Back to list",
                       font=ModernTheme.FONT_BODY,
                       fg=ModernTheme.ACCENT_BLUE,
                       bg=ModernTheme.BG_PRIMARY,
                       cursor="hand2")
        back.pack(anchor="w", pady=(0, 15))
        back.bind("<Button-1>", lambda e: self._show_breed_grid())

        # Info card
        card = tk.Frame(self.breed_results_frame, bg=ModernTheme.BG_CARD)
        card.pack(fill=tk.X)

        inner = tk.Frame(card, bg=ModernTheme.BG_CARD)
        inner.pack(fill=tk.X, padx=30, pady=25)

        # Header
        name = tk.Label(inner, text=info['name'],
                       font=ModernTheme.FONT_TITLE,
                       fg=ModernTheme.ACCENT_CYAN,
                       bg=ModernTheme.BG_CARD)
        name.pack(anchor="w")

        meta = tk.Label(inner, text=f"{info['group']}  •  {info['origin']}  •  {info['lifespan']}",
                       font=ModernTheme.FONT_CAPTION,
                       fg=ModernTheme.TEXT_SECONDARY,
                       bg=ModernTheme.BG_CARD)
        meta.pack(anchor="w", pady=(5, 20))

        # Stats
        stats = [
            ("Size", f"{info['size']['weight']}"),
            ("Temperament", ", ".join(info['temperament'][:3])),
            ("Exercise", info['exercise']),
            ("Grooming", info['grooming']),
            ("Trainability", info['trainability']),
            ("Barking", info['barking']),
            ("Shedding", info['shedding']),
        ]

        for label, value in stats:
            row = tk.Frame(inner, bg=ModernTheme.BG_CARD)
            row.pack(fill=tk.X, pady=4)

            lbl = tk.Label(row, text=label,
                          font=ModernTheme.FONT_BODY,
                          fg=ModernTheme.TEXT_MUTED,
                          bg=ModernTheme.BG_CARD,
                          width=12, anchor="w")
            lbl.pack(side=tk.LEFT)

            val = tk.Label(row, text=value,
                          font=ModernTheme.FONT_BODY,
                          fg=ModernTheme.TEXT_PRIMARY,
                          bg=ModernTheme.BG_CARD)
            val.pack(side=tk.LEFT)

        # Good with
        gw = info['good_with']
        gw_frame = tk.Frame(inner, bg=ModernTheme.BG_CARD)
        gw_frame.pack(fill=tk.X, pady=(15, 10))

        for item, val in [("Kids", gw['kids']), ("Dogs", gw['dogs']),
                         ("Cats", gw['cats']), ("Strangers", gw['strangers'])]:
            color = ModernTheme.ACCENT_GREEN if val else ModernTheme.ACCENT_RED
            badge = tk.Label(gw_frame, text=f" {item} {'✓' if val else '✗'} ",
                            font=ModernTheme.FONT_CAPTION,
                            fg=color,
                            bg=ModernTheme.BG_TERTIARY)
            badge.pack(side=tk.LEFT, padx=3)

        # Fun fact
        fact_card = tk.Frame(inner, bg=ModernTheme.BG_TERTIARY)
        fact_card.pack(fill=tk.X, pady=(15, 0))

        fact_inner = tk.Frame(fact_card, bg=ModernTheme.BG_TERTIARY)
        fact_inner.pack(fill=tk.X, padx=15, pady=15)

        fact_title = tk.Label(fact_inner, text="Fun Fact",
                             font=ModernTheme.FONT_CAPTION,
                             fg=ModernTheme.ACCENT_ORANGE,
                             bg=ModernTheme.BG_TERTIARY)
        fact_title.pack(anchor="w")

        fact_text = tk.Label(fact_inner, text=info['fun_fact'],
                            font=ModernTheme.FONT_BODY,
                            fg=ModernTheme.TEXT_PRIMARY,
                            bg=ModernTheme.BG_TERTIARY,
                            wraplength=600, justify=tk.LEFT)
        fact_text.pack(anchor="w", pady=(5, 0))

    def show_breed_info_popup(self, breed_name):
        """Show breed info in popup."""
        info = get_breed_info(breed_name)

        if not info:
            messagebox.showinfo("Breed Info", f"No info available for {breed_name}")
            return

        # Popup window
        popup = tk.Toplevel(self.root)
        popup.title(info['name'])
        popup.geometry("550x650")
        popup.configure(bg=ModernTheme.BG_PRIMARY)
        popup.transient(self.root)
        popup.grab_set()

        # Scrollable content
        canvas = tk.Canvas(popup, bg=ModernTheme.BG_PRIMARY, highlightthickness=0)
        scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=ModernTheme.BG_PRIMARY)

        canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=25, pady=25)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Header
        name = tk.Label(content, text=info['name'],
                       font=ModernTheme.FONT_TITLE,
                       fg=ModernTheme.ACCENT_CYAN,
                       bg=ModernTheme.BG_PRIMARY)
        name.pack(anchor="w")

        meta = tk.Label(content, text=f"{info['group']}  •  {info['origin']}",
                       font=ModernTheme.FONT_BODY,
                       fg=ModernTheme.TEXT_SECONDARY,
                       bg=ModernTheme.BG_PRIMARY)
        meta.pack(anchor="w", pady=(5, 20))

        # All info
        items = [
            ("Size", f"{info['size']['weight']}, {info['size']['height']}"),
            ("Lifespan", info['lifespan']),
            ("Temperament", ", ".join(info['temperament'])),
            ("Exercise", info['exercise']),
            ("Grooming", info['grooming']),
            ("Trainability", info['trainability']),
            ("Barking", info['barking']),
            ("Shedding", info['shedding']),
            ("Health Watch", ", ".join(info['health_issues'][:3])),
        ]

        for label, value in items:
            row = tk.Frame(content, bg=ModernTheme.BG_PRIMARY)
            row.pack(fill=tk.X, pady=6)

            lbl = tk.Label(row, text=label,
                          font=ModernTheme.FONT_BODY,
                          fg=ModernTheme.ACCENT_BLUE,
                          bg=ModernTheme.BG_PRIMARY,
                          width=14, anchor="w")
            lbl.pack(side=tk.LEFT)

            val = tk.Label(row, text=value,
                          font=ModernTheme.FONT_BODY,
                          fg=ModernTheme.TEXT_PRIMARY,
                          bg=ModernTheme.BG_PRIMARY,
                          wraplength=350, justify=tk.LEFT)
            val.pack(side=tk.LEFT, fill=tk.X)

        # Good with
        gw = info['good_with']
        gw_frame = tk.Frame(content, bg=ModernTheme.BG_PRIMARY)
        gw_frame.pack(fill=tk.X, pady=15)

        gw_label = tk.Label(gw_frame, text="Good with",
                           font=ModernTheme.FONT_BODY,
                           fg=ModernTheme.ACCENT_BLUE,
                           bg=ModernTheme.BG_PRIMARY,
                           width=14, anchor="w")
        gw_label.pack(side=tk.LEFT)

        gw_vals = tk.Frame(gw_frame, bg=ModernTheme.BG_PRIMARY)
        gw_vals.pack(side=tk.LEFT)

        for item, val in [("Kids", gw['kids']), ("Dogs", gw['dogs']),
                         ("Cats", gw['cats']), ("Strangers", gw['strangers'])]:
            color = ModernTheme.ACCENT_GREEN if val else ModernTheme.ACCENT_RED
            badge = tk.Label(gw_vals, text=f" {item} {'✓' if val else '✗'} ",
                            font=ModernTheme.FONT_CAPTION,
                            fg=color,
                            bg=ModernTheme.BG_TERTIARY)
            badge.pack(side=tk.LEFT, padx=2)

        # Fun fact
        fact_card = tk.Frame(content, bg=ModernTheme.BG_CARD)
        fact_card.pack(fill=tk.X, pady=15)

        fact_inner = tk.Frame(fact_card, bg=ModernTheme.BG_CARD)
        fact_inner.pack(fill=tk.X, padx=20, pady=15)

        fact_title = tk.Label(fact_inner, text="Fun Fact",
                             font=ModernTheme.FONT_BODY,
                             fg=ModernTheme.ACCENT_ORANGE,
                             bg=ModernTheme.BG_CARD)
        fact_title.pack(anchor="w")

        fact_text = tk.Label(fact_inner, text=info['fun_fact'],
                            font=ModernTheme.FONT_BODY,
                            fg=ModernTheme.TEXT_PRIMARY,
                            bg=ModernTheme.BG_CARD,
                            wraplength=450, justify=tk.LEFT)
        fact_text.pack(anchor="w", pady=(8, 0))

        # Similar breeds
        similar = tk.Label(content, text=f"Similar: {', '.join(info['similar_breeds'])}",
                          font=ModernTheme.FONT_CAPTION,
                          fg=ModernTheme.TEXT_MUTED,
                          bg=ModernTheme.BG_PRIMARY)
        similar.pack(anchor="w", pady=(10, 0))

        # Close button
        close_btn = tk.Frame(content, bg=ModernTheme.BG_TERTIARY, cursor="hand2")
        close_btn.pack(pady=20)

        close_label = tk.Label(close_btn, text="  Close  ",
                              font=ModernTheme.FONT_BODY,
                              fg=ModernTheme.TEXT_PRIMARY,
                              bg=ModernTheme.BG_TERTIARY,
                              padx=25, pady=10)
        close_label.pack()

        close_btn.bind("<Button-1>", lambda e: popup.destroy())
        close_label.bind("<Button-1>", lambda e: popup.destroy())


def main():
    """Main entry point."""
    root = tk.Tk()
    app = CanineClassifierApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
