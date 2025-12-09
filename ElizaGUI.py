#!/usr/bin/env python3
"""
Canine Classifier - Ultra-Modern Professional GUI
A sleek, glass-morphism inspired dog breed identification tool.
2025 Premium Design Language
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
import sys
import threading
import webbrowser

# Try to import PIL for image display
try:
    from PIL import Image, ImageTk, ImageDraw, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Import breed info
try:
    from breed_info import BREED_INFO, get_breed_info
    BREED_INFO_AVAILABLE = True
except ImportError:
    BREED_INFO_AVAILABLE = False
    BREED_INFO = {}
    def get_breed_info(breed): return None


class ModernTheme:
    """2025 Premium Dark Theme with Glass Morphism."""

    # Deep dark backgrounds
    BG_DARK = "#08080c"
    BG_PRIMARY = "#0d0d14"
    BG_SECONDARY = "#13131c"
    BG_TERTIARY = "#1a1a26"

    # Glass card backgrounds (with transparency simulation)
    GLASS_BG = "#16161f"
    GLASS_BORDER = "#2a2a3d"
    GLASS_HIGHLIGHT = "#3d3d5c"

    # Gradient accent colors
    ACCENT_PURPLE = "#8b5cf6"
    ACCENT_VIOLET = "#a78bfa"
    ACCENT_PINK = "#ec4899"
    ACCENT_MAGENTA = "#f472b6"
    ACCENT_CYAN = "#06b6d4"
    ACCENT_TEAL = "#14b8a6"
    ACCENT_BLUE = "#3b82f6"
    ACCENT_GREEN = "#10b981"
    ACCENT_ORANGE = "#f59e0b"
    ACCENT_RED = "#ef4444"

    # Text colors
    TEXT_PRIMARY = "#f8fafc"
    TEXT_SECONDARY = "#94a3b8"
    TEXT_MUTED = "#64748b"
    TEXT_ACCENT = "#c4b5fd"

    # Borders and effects
    BORDER_SUBTLE = "#1e1e2e"
    BORDER_GLOW = "#8b5cf680"

    # Status colors
    SUCCESS = "#10b981"
    WARNING = "#f59e0b"
    ERROR = "#ef4444"
    INFO = "#3b82f6"


class ResponsiveApp:
    """Handles responsive sizing based on screen dimensions."""

    def __init__(self, root):
        self.root = root
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        # Calculate optimal window size (80% of screen, max 1400x900)
        self.window_width = min(int(self.screen_width * 0.8), 1400)
        self.window_height = min(int(self.screen_height * 0.85), 900)

        # Scaling factor based on screen size
        self.scale = min(self.window_width / 1400, self.window_height / 900)

    def scaled(self, value):
        """Return scaled value based on screen size."""
        return max(int(value * self.scale), 1)

    def get_font_size(self, base_size):
        """Get responsive font size."""
        return max(int(base_size * self.scale), 8)


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
    """Ultra-Modern Professional GUI for Canine Classifier."""

    def __init__(self, root):
        self.root = root
        self.root.title("Canine Classifier")

        # Initialize responsive handler
        self.responsive = ResponsiveApp(root)

        # Set window size and position
        w, h = self.responsive.window_width, self.responsive.window_height
        x = (self.responsive.screen_width - w) // 2
        y = (self.responsive.screen_height - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.minsize(900, 600)
        self.root.configure(bg=ModernTheme.BG_DARK)

        # Configure fonts based on scale
        self.fonts = {
            'display': ("Segoe UI", self.responsive.get_font_size(28), "bold"),
            'title': ("Segoe UI", self.responsive.get_font_size(20), "bold"),
            'heading': ("Segoe UI", self.responsive.get_font_size(14), "bold"),
            'body': ("Segoe UI", self.responsive.get_font_size(11)),
            'caption': ("Segoe UI", self.responsive.get_font_size(9)),
            'small': ("Segoe UI", self.responsive.get_font_size(8)),
        }

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

    def configure_styles(self):
        """Configure ttk styles for modern look."""
        style = ttk.Style()
        style.theme_use('clam')

        # Combobox style
        style.configure('Modern.TCombobox',
                       fieldbackground=ModernTheme.GLASS_BG,
                       background=ModernTheme.GLASS_BG,
                       foreground=ModernTheme.TEXT_PRIMARY,
                       arrowcolor=ModernTheme.TEXT_SECONDARY,
                       borderwidth=1,
                       padding=10)

        style.map('Modern.TCombobox',
                 fieldbackground=[('readonly', ModernTheme.GLASS_BG)],
                 selectbackground=[('readonly', ModernTheme.ACCENT_PURPLE)],
                 selectforeground=[('readonly', ModernTheme.TEXT_PRIMARY)])

        # Scrollbar style
        style.configure('Modern.Vertical.TScrollbar',
                       background=ModernTheme.BG_TERTIARY,
                       troughcolor=ModernTheme.BG_SECONDARY,
                       borderwidth=0,
                       arrowsize=0,
                       width=8)

    def clear_frame(self):
        """Clear the current frame."""
        if self.current_frame:
            self.current_frame.destroy()

    def create_glass_card(self, parent, **kwargs):
        """Create a glass morphism style card."""
        card = tk.Frame(parent,
                       bg=ModernTheme.GLASS_BG,
                       highlightbackground=ModernTheme.GLASS_BORDER,
                       highlightthickness=1,
                       **kwargs)
        return card

    def create_gradient_button(self, parent, text, command, accent_color=ModernTheme.ACCENT_PURPLE, width=None):
        """Create a modern gradient-style button."""
        btn_frame = tk.Frame(parent, bg=accent_color, cursor="hand2")

        padx = width // 4 if width else 20
        btn_label = tk.Label(btn_frame, text=text,
                            font=self.fonts['body'],
                            fg=ModernTheme.TEXT_PRIMARY,
                            bg=accent_color,
                            padx=padx, pady=10)
        btn_label.pack()

        # Hover effects
        def on_enter(e):
            btn_frame.config(bg=ModernTheme.GLASS_HIGHLIGHT)
            btn_label.config(bg=ModernTheme.GLASS_HIGHLIGHT)

        def on_leave(e):
            btn_frame.config(bg=accent_color)
            btn_label.config(bg=accent_color)

        btn_frame.bind("<Enter>", on_enter)
        btn_frame.bind("<Leave>", on_leave)
        btn_frame.bind("<Button-1>", lambda e: command())
        btn_label.bind("<Button-1>", lambda e: command())

        return btn_frame

    def create_nav_header(self, parent):
        """Create navigation header with back button."""
        nav = tk.Frame(parent, bg=ModernTheme.BG_PRIMARY, height=self.responsive.scaled(50))
        nav.pack(fill=tk.X, padx=self.responsive.scaled(20), pady=(self.responsive.scaled(15), 0))
        nav.pack_propagate(False)

        back_btn = tk.Label(nav, text="←  Back",
                           font=self.fonts['body'],
                           fg=ModernTheme.ACCENT_VIOLET,
                           bg=ModernTheme.BG_PRIMARY,
                           cursor="hand2")
        back_btn.pack(side=tk.LEFT, pady=self.responsive.scaled(12))
        back_btn.bind("<Button-1>", lambda e: self.show_main_menu())
        back_btn.bind("<Enter>", lambda e: back_btn.config(fg=ModernTheme.TEXT_PRIMARY))
        back_btn.bind("<Leave>", lambda e: back_btn.config(fg=ModernTheme.ACCENT_VIOLET))

        return nav

    def create_page_title(self, parent, title, subtitle=""):
        """Create page title section."""
        title_frame = tk.Frame(parent, bg=ModernTheme.BG_PRIMARY)
        title_frame.pack(fill=tk.X, padx=self.responsive.scaled(20), pady=(self.responsive.scaled(5), self.responsive.scaled(15)))

        title_label = tk.Label(title_frame, text=title,
                              font=self.fonts['title'],
                              fg=ModernTheme.TEXT_PRIMARY,
                              bg=ModernTheme.BG_PRIMARY)
        title_label.pack(anchor="w")

        if subtitle:
            sub_label = tk.Label(title_frame, text=subtitle,
                                font=self.fonts['caption'],
                                fg=ModernTheme.TEXT_SECONDARY,
                                bg=ModernTheme.BG_PRIMARY)
            sub_label.pack(anchor="w", pady=(2, 0))

        return title_frame

    # ==================== MAIN MENU ====================

    def show_main_menu(self):
        """Display the ultra-modern main menu."""
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=ModernTheme.BG_PRIMARY)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        # Header section
        header = tk.Frame(self.current_frame, bg=ModernTheme.BG_PRIMARY)
        header.pack(fill=tk.X, padx=self.responsive.scaled(30), pady=(self.responsive.scaled(40), self.responsive.scaled(25)))

        # App title with accent color
        title_label = tk.Label(header, text="Canine Classifier",
                              font=self.fonts['display'],
                              fg=ModernTheme.ACCENT_VIOLET,
                              bg=ModernTheme.BG_PRIMARY)
        title_label.pack()

        subtitle_label = tk.Label(header, text="AI-Powered Dog Breed Identification",
                                 font=self.fonts['body'],
                                 fg=ModernTheme.TEXT_SECONDARY,
                                 bg=ModernTheme.BG_PRIMARY)
        subtitle_label.pack(pady=(5, 0))

        # Menu cards container - scrollable if needed
        container = tk.Frame(self.current_frame, bg=ModernTheme.BG_PRIMARY)
        container.pack(fill=tk.BOTH, expand=True, padx=self.responsive.scaled(30), pady=self.responsive.scaled(10))

        # Configure 2x2 grid
        container.grid_columnconfigure(0, weight=1, uniform="col")
        container.grid_columnconfigure(1, weight=1, uniform="col")
        container.grid_rowconfigure(0, weight=1, uniform="row")
        container.grid_rowconfigure(1, weight=1, uniform="row")

        # Menu items with gradient accents
        menu_items = [
            ("AI Recognition", "Upload a photo for instant breed detection",
             ModernTheme.ACCENT_PURPLE, ModernTheme.ACCENT_VIOLET, self.show_image_recognition, "01"),
            ("Questionnaire", "Answer questions about your dog's features",
             ModernTheme.ACCENT_PINK, ModernTheme.ACCENT_MAGENTA, self.show_questionnaire, "02"),
            ("Dichotomous Key", "Scientific Yes/No identification method",
             ModernTheme.ACCENT_CYAN, ModernTheme.ACCENT_TEAL, self.show_dichotomous_key, "03"),
            ("Breed Database", "Explore detailed info on 51+ breeds",
             ModernTheme.ACCENT_ORANGE, ModernTheme.ACCENT_GREEN, self.show_breed_lookup, "04"),
        ]

        for idx, (title, desc, color1, color2, command, num) in enumerate(menu_items):
            row, col = divmod(idx, 2)
            self._create_menu_card(container, title, desc, color1, color2, command, num, row, col)

        # Footer
        footer = tk.Label(self.current_frame,
                         text="v2.0  •  51 Breeds  •  AI Powered",
                         font=self.fonts['small'],
                         fg=ModernTheme.TEXT_MUTED,
                         bg=ModernTheme.BG_PRIMARY)
        footer.pack(side=tk.BOTTOM, pady=self.responsive.scaled(15))

    def _create_menu_card(self, parent, title, desc, accent1, accent2, command, num, row, col):
        """Create a modern glass-morphism menu card."""
        # Card container with glass effect
        card = tk.Frame(parent,
                       bg=ModernTheme.GLASS_BG,
                       highlightbackground=ModernTheme.GLASS_BORDER,
                       highlightthickness=1,
                       cursor="hand2")
        card.grid(row=row, column=col, padx=self.responsive.scaled(8),
                 pady=self.responsive.scaled(8), sticky="nsew")

        # Inner content
        inner = tk.Frame(card, bg=ModernTheme.GLASS_BG)
        inner.pack(fill=tk.BOTH, expand=True, padx=self.responsive.scaled(20),
                  pady=self.responsive.scaled(20))

        # Number with accent gradient
        num_label = tk.Label(inner, text=num,
                            font=("Segoe UI", self.responsive.get_font_size(32), "bold"),
                            fg=accent1,
                            bg=ModernTheme.GLASS_BG)
        num_label.pack(anchor="w")

        # Title
        title_label = tk.Label(inner, text=title,
                              font=self.fonts['heading'],
                              fg=ModernTheme.TEXT_PRIMARY,
                              bg=ModernTheme.GLASS_BG)
        title_label.pack(anchor="w", pady=(self.responsive.scaled(10), self.responsive.scaled(3)))

        # Description
        desc_label = tk.Label(inner, text=desc,
                             font=self.fonts['caption'],
                             fg=ModernTheme.TEXT_SECONDARY,
                             bg=ModernTheme.GLASS_BG)
        desc_label.pack(anchor="w")

        # Arrow with gradient color
        arrow_frame = tk.Frame(inner, bg=ModernTheme.GLASS_BG)
        arrow_frame.pack(anchor="e", side=tk.BOTTOM)

        arrow_label = tk.Label(arrow_frame, text="→",
                              font=("Segoe UI", self.responsive.get_font_size(18)),
                              fg=accent2,
                              bg=ModernTheme.GLASS_BG)
        arrow_label.pack()

        # Hover effects
        def on_enter(e):
            card.config(bg=ModernTheme.BG_TERTIARY, highlightbackground=accent1)
            inner.config(bg=ModernTheme.BG_TERTIARY)
            for w in [num_label, title_label, desc_label, arrow_frame, arrow_label]:
                w.config(bg=ModernTheme.BG_TERTIARY)

        def on_leave(e):
            card.config(bg=ModernTheme.GLASS_BG, highlightbackground=ModernTheme.GLASS_BORDER)
            inner.config(bg=ModernTheme.GLASS_BG)
            for w in [num_label, title_label, desc_label, arrow_frame, arrow_label]:
                w.config(bg=ModernTheme.GLASS_BG)

        # Bind events
        for widget in [card, inner, num_label, title_label, desc_label, arrow_frame, arrow_label]:
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

        # Main content - horizontal split
        content = tk.Frame(self.current_frame, bg=ModernTheme.BG_PRIMARY)
        content.pack(fill=tk.BOTH, expand=True, padx=self.responsive.scaled(20),
                    pady=(0, self.responsive.scaled(15)))

        # Left panel - Upload (40% width)
        left_panel = tk.Frame(content, bg=ModernTheme.BG_PRIMARY)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, self.responsive.scaled(10)))
        left_panel.configure(width=self.responsive.scaled(380))
        left_panel.pack_propagate(False)

        # Upload card
        upload_card = self.create_glass_card(left_panel)
        upload_card.pack(fill=tk.BOTH, expand=True)

        upload_inner = tk.Frame(upload_card, bg=ModernTheme.GLASS_BG)
        upload_inner.pack(fill=tk.BOTH, expand=True, padx=self.responsive.scaled(15),
                         pady=self.responsive.scaled(15))

        # Section title
        section_title = tk.Label(upload_inner, text="Upload Image",
                                font=self.fonts['heading'],
                                fg=ModernTheme.TEXT_PRIMARY,
                                bg=ModernTheme.GLASS_BG)
        section_title.pack(anchor="w", pady=(0, self.responsive.scaled(10)))

        # Image preview area
        preview_height = self.responsive.scaled(220)
        self.preview_frame = tk.Frame(upload_inner, bg=ModernTheme.BG_TERTIARY,
                                     height=preview_height,
                                     highlightbackground=ModernTheme.GLASS_BORDER,
                                     highlightthickness=1)
        self.preview_frame.pack(fill=tk.X, pady=(0, self.responsive.scaled(10)))
        self.preview_frame.pack_propagate(False)

        # Placeholder
        self.placeholder_frame = tk.Frame(self.preview_frame, bg=ModernTheme.BG_TERTIARY)
        self.placeholder_frame.place(relx=0.5, rely=0.5, anchor="center")

        plus_icon = tk.Label(self.placeholder_frame, text="+",
                            font=("Segoe UI", self.responsive.get_font_size(36)),
                            fg=ModernTheme.GLASS_BORDER,
                            bg=ModernTheme.BG_TERTIARY)
        plus_icon.pack()

        self.preview_label = tk.Label(self.placeholder_frame,
                                     text="Click Browse to select image",
                                     font=self.fonts['caption'],
                                     fg=ModernTheme.TEXT_MUTED,
                                     bg=ModernTheme.BG_TERTIARY)
        self.preview_label.pack()

        self.preview_photo = None
        self.image_display_label = None

        # File info
        self.image_path_var = tk.StringVar(value="No file selected")
        path_label = tk.Label(upload_inner, textvariable=self.image_path_var,
                             font=self.fonts['small'],
                             fg=ModernTheme.TEXT_MUTED,
                             bg=ModernTheme.GLASS_BG)
        path_label.pack(pady=(0, self.responsive.scaled(10)))

        # Buttons
        btn_frame = tk.Frame(upload_inner, bg=ModernTheme.GLASS_BG)
        btn_frame.pack(fill=tk.X)

        browse_btn = self.create_gradient_button(btn_frame, "Browse",
                                                 self.browse_image,
                                                 ModernTheme.BG_TERTIARY)
        browse_btn.pack(side=tk.LEFT, padx=(0, self.responsive.scaled(8)))

        analyze_btn = self.create_gradient_button(btn_frame, "Analyze",
                                                  self.classify_image,
                                                  ModernTheme.ACCENT_PURPLE)
        analyze_btn.pack(side=tk.LEFT)

        # Status
        self.ai_status_var = tk.StringVar(value="")
        self.ai_status_label = tk.Label(upload_inner, textvariable=self.ai_status_var,
                                       font=self.fonts['caption'],
                                       fg=ModernTheme.ACCENT_CYAN,
                                       bg=ModernTheme.GLASS_BG)
        self.ai_status_label.pack(pady=(self.responsive.scaled(10), 0))

        # Right panel - Results (60% width)
        right_panel = tk.Frame(content, bg=ModernTheme.BG_PRIMARY)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Results card
        results_card = self.create_glass_card(right_panel)
        results_card.pack(fill=tk.BOTH, expand=True)

        results_inner = tk.Frame(results_card, bg=ModernTheme.GLASS_BG)
        results_inner.pack(fill=tk.BOTH, expand=True, padx=self.responsive.scaled(15),
                          pady=self.responsive.scaled(15))

        # Results header
        results_title = tk.Label(results_inner, text="Results",
                                font=self.fonts['heading'],
                                fg=ModernTheme.TEXT_PRIMARY,
                                bg=ModernTheme.GLASS_BG)
        results_title.pack(anchor="w")

        results_sub = tk.Label(results_inner, text="AI predictions with database verification",
                              font=self.fonts['small'],
                              fg=ModernTheme.TEXT_MUTED,
                              bg=ModernTheme.GLASS_BG)
        results_sub.pack(anchor="w", pady=(2, self.responsive.scaled(10)))

        # Scrollable results
        results_container = tk.Frame(results_inner, bg=ModernTheme.GLASS_BG)
        results_container.pack(fill=tk.BOTH, expand=True)

        self.ai_canvas = tk.Canvas(results_container, bg=ModernTheme.GLASS_BG,
                                  highlightthickness=0)
        scrollbar = ttk.Scrollbar(results_container, orient="vertical",
                                 command=self.ai_canvas.yview,
                                 style='Modern.Vertical.TScrollbar')

        self.ai_results_frame = tk.Frame(self.ai_canvas, bg=ModernTheme.GLASS_BG)

        self.ai_canvas.create_window((0, 0), window=self.ai_results_frame, anchor="nw")
        self.ai_canvas.configure(yscrollcommand=scrollbar.set)

        self.ai_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.ai_results_frame.bind("<Configure>",
            lambda e: self.ai_canvas.configure(scrollregion=self.ai_canvas.bbox("all")))

        # Placeholder
        placeholder = tk.Label(self.ai_results_frame,
                              text="Select an image and click Analyze\nto identify the dog breed",
                              font=self.fonts['body'],
                              fg=ModernTheme.TEXT_MUTED,
                              bg=ModernTheme.GLASS_BG,
                              justify=tk.CENTER)
        placeholder.pack(pady=self.responsive.scaled(60))

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
            if len(filename) > 30:
                filename = filename[:27] + "..."
            self.image_path_var.set(filename)
            self._show_image_preview(filepath)

    def _show_image_preview(self, filepath):
        """Display the selected image in the preview area."""
        if not PIL_AVAILABLE:
            self.preview_label.config(text="PIL not installed")
            return

        try:
            img = Image.open(filepath)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Fit to preview area
            max_w = self.responsive.scaled(340)
            max_h = self.responsive.scaled(200)
            ratio = min(max_w / img.width, max_h / img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

            self.preview_photo = ImageTk.PhotoImage(img)

            if hasattr(self, 'placeholder_frame'):
                self.placeholder_frame.place_forget()

            if not self.image_display_label:
                self.image_display_label = tk.Label(self.preview_frame, bg=ModernTheme.BG_TERTIARY)

            self.image_display_label.config(image=self.preview_photo)
            self.image_display_label.place(relx=0.5, rely=0.5, anchor="center")

        except Exception as e:
            self.preview_label.config(text=f"Error: {type(e).__name__}")

    def classify_image(self):
        """Classify the selected image using AI."""
        if not self.selected_image_path:
            self.ai_status_var.set("Please select an image first")
            return

        for widget in self.ai_results_frame.winfo_children():
            widget.destroy()

        self.ai_status_var.set("Analyzing...")
        self.root.update()

        thread = threading.Thread(target=self._run_classification)
        thread.start()

    def _run_classification(self):
        """Run classification in background thread."""
        try:
            from image_classifier import DogImageClassifier

            if not self.classifier:
                self.classifier = DogImageClassifier()

            results = self.classifier.classify_image(self.selected_image_path)
            self.root.after(0, lambda: self._display_ai_results(results))

        except ImportError:
            self.root.after(0, lambda: self.ai_status_var.set("AI module not available"))
        except Exception as e:
            self.root.after(0, lambda: self.ai_status_var.set(f"Error: {str(e)[:50]}"))

    def _display_ai_results(self, results):
        """Display AI classification results."""
        self.ai_status_var.set("")

        for widget in self.ai_results_frame.winfo_children():
            widget.destroy()

        if not results:
            self.ai_status_var.set("Could not classify image")
            return

        colors = [ModernTheme.ACCENT_PURPLE, ModernTheme.ACCENT_PINK,
                 ModernTheme.ACCENT_CYAN, ModernTheme.ACCENT_ORANGE, ModernTheme.ACCENT_GREEN]

        for i, result in enumerate(results[:5]):
            breed = result.get('breed', 'Unknown')
            confidence = result.get('confidence', 0)
            verified = result.get('verified', False)
            db_name = result.get('db_name', breed)

            # Result row
            row = tk.Frame(self.ai_results_frame, bg=ModernTheme.BG_TERTIARY, cursor="hand2")
            row.pack(fill=tk.X, pady=self.responsive.scaled(3))

            inner = tk.Frame(row, bg=ModernTheme.BG_TERTIARY)
            inner.pack(fill=tk.X, padx=self.responsive.scaled(12), pady=self.responsive.scaled(10))

            # Left: verification + name
            left = tk.Frame(inner, bg=ModernTheme.BG_TERTIARY)
            left.pack(side=tk.LEFT, fill=tk.X, expand=True)

            indicator = tk.Label(left, text="●" if verified else "○",
                               font=self.fonts['small'],
                               fg=ModernTheme.SUCCESS if verified else ModernTheme.TEXT_MUTED,
                               bg=ModernTheme.BG_TERTIARY)
            indicator.pack(side=tk.LEFT, padx=(0, self.responsive.scaled(8)))

            display_name = db_name if verified else breed
            name = tk.Label(left, text=display_name,
                           font=self.fonts['body'],
                           fg=ModernTheme.TEXT_PRIMARY,
                           bg=ModernTheme.BG_TERTIARY)
            name.pack(side=tk.LEFT)

            # Right: bar + percentage
            right = tk.Frame(inner, bg=ModernTheme.BG_TERTIARY)
            right.pack(side=tk.RIGHT)

            bar_w = self.responsive.scaled(80)
            bar_bg = tk.Frame(right, bg=ModernTheme.BG_PRIMARY, width=bar_w, height=self.responsive.scaled(6))
            bar_bg.pack(side=tk.LEFT, padx=(0, self.responsive.scaled(8)))
            bar_bg.pack_propagate(False)

            fill_w = max(1, int(bar_w * confidence / 100))
            bar_fill = tk.Frame(bar_bg, bg=colors[i], width=fill_w)
            bar_fill.place(x=0, y=0, relheight=1)

            pct = tk.Label(right, text=f"{confidence:.1f}%",
                          font=self.fonts['caption'],
                          fg=colors[i],
                          bg=ModernTheme.BG_TERTIARY,
                          width=6)
            pct.pack(side=tk.LEFT)

            # Click binding
            def on_click(e, b=display_name):
                self.show_breed_info_popup(b)

            for w in [row, inner, left, right, indicator, name, pct]:
                w.bind("<Button-1>", on_click)

    # ==================== QUESTIONNAIRE ====================

    def show_questionnaire(self):
        """Display the questionnaire page."""
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=ModernTheme.BG_PRIMARY)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        self.create_nav_header(self.current_frame)
        self.create_page_title(self.current_frame, "Questionnaire",
                              "Select your dog's physical characteristics")

        # Content
        content = tk.Frame(self.current_frame, bg=ModernTheme.BG_PRIMARY)
        content.pack(fill=tk.BOTH, expand=True, padx=self.responsive.scaled(20),
                    pady=(0, self.responsive.scaled(15)))

        # Form card
        form_card = self.create_glass_card(content)
        form_card.pack(fill=tk.X)

        form_inner = tk.Frame(form_card, bg=ModernTheme.GLASS_BG)
        form_inner.pack(fill=tk.X, padx=self.responsive.scaled(20), pady=self.responsive.scaled(20))

        # Questions in 2 columns
        self.q_vars = {}
        questions = [
            ("color", "Color", ["Black", "White", "Brown", "Tan", "Brindle", "Merle", "Chocolate", "Yellow"]),
            ("ear_type", "Ear Type", ["Floppy", "Tall", "Triangular"]),
            ("tail_type", "Tail Type", ["Docked", "Long_and_curved", "Curled"]),
            ("size", "Size", ["Small", "Medium", "Large", "Giant"]),
            ("coat_type", "Coat Type", ["Short", "Medium", "Long", "Curly", "Double", "Smooth", "Dense", "Silky"]),
        ]

        # Create 2-column layout
        row_frame = None
        for idx, (key, label, options) in enumerate(questions):
            if idx % 2 == 0:
                row_frame = tk.Frame(form_inner, bg=ModernTheme.GLASS_BG)
                row_frame.pack(fill=tk.X, pady=self.responsive.scaled(5))

            q_frame = tk.Frame(row_frame, bg=ModernTheme.GLASS_BG)
            q_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=self.responsive.scaled(5))

            lbl = tk.Label(q_frame, text=label,
                          font=self.fonts['caption'],
                          fg=ModernTheme.TEXT_SECONDARY,
                          bg=ModernTheme.GLASS_BG)
            lbl.pack(anchor="w")

            var = tk.StringVar(value=options[0])
            self.q_vars[key] = var

            combo = ttk.Combobox(q_frame, textvariable=var, values=options,
                                state="readonly", font=self.fonts['caption'],
                                width=self.responsive.scaled(20))
            combo.pack(anchor="w", pady=(2, 0))

        # Submit button
        btn_frame = tk.Frame(content, bg=ModernTheme.BG_PRIMARY)
        btn_frame.pack(pady=self.responsive.scaled(15))

        submit_btn = self.create_gradient_button(btn_frame, "  Find Matches  ",
                                                 self.process_questionnaire,
                                                 ModernTheme.ACCENT_PINK)
        submit_btn.pack()

        # Results area
        self.q_results_frame = tk.Frame(content, bg=ModernTheme.BG_PRIMARY)
        self.q_results_frame.pack(fill=tk.BOTH, expand=True)

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
            results_card = self.create_glass_card(self.q_results_frame)
            results_card.pack(fill=tk.X)

            results_inner = tk.Frame(results_card, bg=ModernTheme.GLASS_BG)
            results_inner.pack(fill=tk.X, padx=self.responsive.scaled(15),
                              pady=self.responsive.scaled(15))

            header = tk.Label(results_inner, text="Matches",
                            font=self.fonts['heading'],
                            fg=ModernTheme.TEXT_PRIMARY,
                            bg=ModernTheme.GLASS_BG)
            header.pack(anchor="w", pady=(0, self.responsive.scaled(10)))

            colors = [ModernTheme.ACCENT_GREEN, ModernTheme.ACCENT_CYAN, ModernTheme.ACCENT_ORANGE]

            for i, (breed, matched, probability) in enumerate(results):
                row = tk.Frame(results_inner, bg=ModernTheme.BG_TERTIARY, cursor="hand2")
                row.pack(fill=tk.X, pady=self.responsive.scaled(3))

                inner = tk.Frame(row, bg=ModernTheme.BG_TERTIARY)
                inner.pack(fill=tk.X, padx=self.responsive.scaled(12), pady=self.responsive.scaled(10))

                rank = tk.Label(inner, text=f"#{i+1}",
                               font=self.fonts['body'],
                               fg=colors[i] if i < 3 else ModernTheme.TEXT_MUTED,
                               bg=ModernTheme.BG_TERTIARY)
                rank.pack(side=tk.LEFT, padx=(0, self.responsive.scaled(10)))

                name = tk.Label(inner, text=breed,
                               font=self.fonts['body'],
                               fg=ModernTheme.TEXT_PRIMARY,
                               bg=ModernTheme.BG_TERTIARY)
                name.pack(side=tk.LEFT)

                score = tk.Label(inner, text=f"{probability:.0f}%",
                                font=self.fonts['caption'],
                                fg=ModernTheme.TEXT_SECONDARY,
                                bg=ModernTheme.BG_TERTIARY)
                score.pack(side=tk.RIGHT)

                for w in [row, inner, rank, name, score]:
                    w.bind("<Button-1>", lambda e, b=breed: self.show_breed_info_popup(b))
        else:
            no_results = tk.Label(self.q_results_frame,
                                text="No matching breeds found",
                                font=self.fonts['body'],
                                fg=ModernTheme.TEXT_MUTED,
                                bg=ModernTheme.BG_PRIMARY)
            no_results.pack(pady=self.responsive.scaled(20))

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

        self.dkey_content = tk.Frame(self.current_frame, bg=ModernTheme.BG_PRIMARY)
        self.dkey_content.pack(fill=tk.BOTH, expand=True, padx=self.responsive.scaled(20),
                              pady=(0, self.responsive.scaled(15)))

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

        # Progress
        progress = tk.Label(self.dkey_content,
                           text=f"Question {self.dkey_question_count}",
                           font=self.fonts['caption'],
                           fg=ModernTheme.ACCENT_CYAN,
                           bg=ModernTheme.BG_PRIMARY)
        progress.pack(anchor="w", pady=(0, self.responsive.scaled(15)))

        # Question card
        q_card = self.create_glass_card(self.dkey_content)
        q_card.pack(fill=tk.X)

        q_inner = tk.Frame(q_card, bg=ModernTheme.GLASS_BG)
        q_inner.pack(fill=tk.X, padx=self.responsive.scaled(25), pady=self.responsive.scaled(30))

        q_label = tk.Label(q_inner, text=node["question"],
                          font=self.fonts['title'],
                          fg=ModernTheme.TEXT_PRIMARY,
                          bg=ModernTheme.GLASS_BG,
                          wraplength=self.responsive.scaled(500))
        q_label.pack()

        # Buttons
        btn_frame = tk.Frame(self.dkey_content, bg=ModernTheme.BG_PRIMARY)
        btn_frame.pack(pady=self.responsive.scaled(20))

        yes_btn = self.create_gradient_button(btn_frame, "  Yes  ",
                                             lambda: self._dkey_answer(True),
                                             ModernTheme.ACCENT_GREEN)
        yes_btn.pack(side=tk.LEFT, padx=self.responsive.scaled(10))

        no_btn = self.create_gradient_button(btn_frame, "  No  ",
                                            lambda: self._dkey_answer(False),
                                            ModernTheme.ACCENT_RED)
        no_btn.pack(side=tk.LEFT, padx=self.responsive.scaled(10))

        # Restart
        restart = tk.Label(self.dkey_content, text="Start over",
                          font=self.fonts['caption'],
                          fg=ModernTheme.TEXT_MUTED,
                          bg=ModernTheme.BG_PRIMARY,
                          cursor="hand2")
        restart.pack(pady=self.responsive.scaled(15))
        restart.bind("<Button-1>", lambda e: self._restart_dkey())

    def _dkey_answer(self, is_yes):
        """Handle answer."""
        self.dkey_current_node = self.dkey_current_node["yes" if is_yes else "no"]
        self._show_dkey_question()

    def _show_dkey_result(self, breed):
        """Show identification result."""
        result_card = self.create_glass_card(self.dkey_content)
        result_card.pack(fill=tk.X)

        result_inner = tk.Frame(result_card, bg=ModernTheme.GLASS_BG)
        result_inner.pack(padx=self.responsive.scaled(30), pady=self.responsive.scaled(30))

        check = tk.Label(result_inner, text="✓",
                        font=("Segoe UI", self.responsive.get_font_size(40)),
                        fg=ModernTheme.ACCENT_GREEN,
                        bg=ModernTheme.GLASS_BG)
        check.pack()

        complete = tk.Label(result_inner, text="Identification Complete",
                           font=self.fonts['body'],
                           fg=ModernTheme.TEXT_SECONDARY,
                           bg=ModernTheme.GLASS_BG)
        complete.pack(pady=(self.responsive.scaled(5), 0))

        breed_label = tk.Label(result_inner, text=breed,
                              font=self.fonts['display'],
                              fg=ModernTheme.ACCENT_VIOLET,
                              bg=ModernTheme.GLASS_BG)
        breed_label.pack(pady=self.responsive.scaled(10))

        questions_text = tk.Label(result_inner,
                                 text=f"Identified in {self.dkey_question_count} questions",
                                 font=self.fonts['small'],
                                 fg=ModernTheme.TEXT_MUTED,
                                 bg=ModernTheme.GLASS_BG)
        questions_text.pack()

        # Action buttons
        btn_frame = tk.Frame(self.dkey_content, bg=ModernTheme.BG_PRIMARY)
        btn_frame.pack(pady=self.responsive.scaled(15))

        info_btn = self.create_gradient_button(btn_frame, "View Breed Info",
                                              lambda: self.show_breed_info_popup(breed),
                                              ModernTheme.ACCENT_PURPLE)
        info_btn.pack(side=tk.LEFT, padx=self.responsive.scaled(5))

        again_btn = self.create_gradient_button(btn_frame, "Try Again",
                                               self._restart_dkey,
                                               ModernTheme.BG_TERTIARY)
        again_btn.pack(side=tk.LEFT, padx=self.responsive.scaled(5))

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

        # Search
        search_frame = tk.Frame(self.current_frame, bg=ModernTheme.BG_PRIMARY)
        search_frame.pack(fill=tk.X, padx=self.responsive.scaled(20), pady=(0, self.responsive.scaled(10)))

        breed_names = sorted([info['name'] for info in BREED_INFO.values()]) if BREED_INFO else []

        self.breed_search_var = tk.StringVar()
        search_combo = ttk.Combobox(search_frame, textvariable=self.breed_search_var,
                                   values=breed_names, font=self.fonts['body'],
                                   width=self.responsive.scaled(30))
        search_combo.pack(side=tk.LEFT)
        search_combo.bind("<<ComboboxSelected>>", lambda e: self._lookup_breed())

        search_btn = self.create_gradient_button(search_frame, "Search",
                                                self._lookup_breed,
                                                ModernTheme.ACCENT_PURPLE)
        search_btn.pack(side=tk.LEFT, padx=(self.responsive.scaled(10), 0))

        # Results with scroll
        results_container = tk.Frame(self.current_frame, bg=ModernTheme.BG_PRIMARY)
        results_container.pack(fill=tk.BOTH, expand=True, padx=self.responsive.scaled(20),
                              pady=(0, self.responsive.scaled(15)))

        self.breed_canvas = tk.Canvas(results_container, bg=ModernTheme.BG_PRIMARY,
                                     highlightthickness=0)
        scrollbar = ttk.Scrollbar(results_container, orient="vertical",
                                 command=self.breed_canvas.yview,
                                 style='Modern.Vertical.TScrollbar')

        self.breed_results_frame = tk.Frame(self.breed_canvas, bg=ModernTheme.BG_PRIMARY)

        self.breed_canvas.create_window((0, 0), window=self.breed_results_frame, anchor="nw")
        self.breed_canvas.configure(yscrollcommand=scrollbar.set)

        self.breed_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.breed_results_frame.bind("<Configure>",
            lambda e: self.breed_canvas.configure(scrollregion=self.breed_canvas.bbox("all")))

        self._show_breed_grid()

    def _show_breed_grid(self):
        """Show grid of all breeds."""
        for widget in self.breed_results_frame.winfo_children():
            widget.destroy()

        if not BREED_INFO:
            return

        cols = 4
        current_row = None

        for i, (key, info) in enumerate(sorted(BREED_INFO.items())):
            if i % cols == 0:
                current_row = tk.Frame(self.breed_results_frame, bg=ModernTheme.BG_PRIMARY)
                current_row.pack(fill=tk.X, pady=self.responsive.scaled(2))

            btn = tk.Frame(current_row, bg=ModernTheme.GLASS_BG, cursor="hand2",
                          highlightbackground=ModernTheme.GLASS_BORDER, highlightthickness=1)
            btn.pack(side=tk.LEFT, padx=self.responsive.scaled(2), fill=tk.X, expand=True)

            label = tk.Label(btn, text=info['name'],
                            font=self.fonts['small'],
                            fg=ModernTheme.TEXT_PRIMARY,
                            bg=ModernTheme.GLASS_BG,
                            padx=self.responsive.scaled(8), pady=self.responsive.scaled(8))
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
                              font=self.fonts['body'],
                              fg=ModernTheme.TEXT_MUTED,
                              bg=ModernTheme.BG_PRIMARY)
            no_info.pack(pady=self.responsive.scaled(20))

            back = tk.Label(self.breed_results_frame, text="← Back to list",
                           font=self.fonts['body'],
                           fg=ModernTheme.ACCENT_VIOLET,
                           bg=ModernTheme.BG_PRIMARY,
                           cursor="hand2")
            back.pack()
            back.bind("<Button-1>", lambda e: self._show_breed_grid())
            return

        # Back link
        back = tk.Label(self.breed_results_frame, text="← Back to list",
                       font=self.fonts['caption'],
                       fg=ModernTheme.ACCENT_VIOLET,
                       bg=ModernTheme.BG_PRIMARY,
                       cursor="hand2")
        back.pack(anchor="w", pady=(0, self.responsive.scaled(10)))
        back.bind("<Button-1>", lambda e: self._show_breed_grid())

        # Info card
        card = self.create_glass_card(self.breed_results_frame)
        card.pack(fill=tk.X)

        inner = tk.Frame(card, bg=ModernTheme.GLASS_BG)
        inner.pack(fill=tk.X, padx=self.responsive.scaled(20), pady=self.responsive.scaled(20))

        # Header
        name = tk.Label(inner, text=info['name'],
                       font=self.fonts['title'],
                       fg=ModernTheme.ACCENT_VIOLET,
                       bg=ModernTheme.GLASS_BG)
        name.pack(anchor="w")

        meta = tk.Label(inner, text=f"{info['group']}  •  {info['origin']}  •  {info['lifespan']}",
                       font=self.fonts['small'],
                       fg=ModernTheme.TEXT_SECONDARY,
                       bg=ModernTheme.GLASS_BG)
        meta.pack(anchor="w", pady=(2, self.responsive.scaled(15)))

        # Stats in 2 columns
        stats_frame = tk.Frame(inner, bg=ModernTheme.GLASS_BG)
        stats_frame.pack(fill=tk.X)

        stats = [
            ("Size", f"{info['size']['weight']}"),
            ("Temperament", ", ".join(info['temperament'][:3])),
            ("Exercise", info['exercise']),
            ("Grooming", info['grooming']),
        ]

        for i, (label, value) in enumerate(stats):
            col = i % 2
            row_f = stats_frame if col == 0 else stats_frame

            stat_row = tk.Frame(inner, bg=ModernTheme.GLASS_BG)
            stat_row.pack(fill=tk.X, pady=self.responsive.scaled(2))

            lbl = tk.Label(stat_row, text=label,
                          font=self.fonts['caption'],
                          fg=ModernTheme.TEXT_MUTED,
                          bg=ModernTheme.GLASS_BG,
                          width=12, anchor="w")
            lbl.pack(side=tk.LEFT)

            val = tk.Label(stat_row, text=value,
                          font=self.fonts['caption'],
                          fg=ModernTheme.TEXT_PRIMARY,
                          bg=ModernTheme.GLASS_BG)
            val.pack(side=tk.LEFT)

    def show_breed_info_popup(self, breed_name):
        """Show breed info in popup."""
        info = get_breed_info(breed_name)

        if not info:
            messagebox.showinfo("Breed Info", f"No info available for {breed_name}")
            return

        # Popup window
        popup = tk.Toplevel(self.root)
        popup.title(info['name'])

        # Size popup responsively
        pw = min(self.responsive.scaled(500), self.responsive.window_width - 100)
        ph = min(self.responsive.scaled(550), self.responsive.window_height - 100)
        px = self.root.winfo_x() + (self.responsive.window_width - pw) // 2
        py = self.root.winfo_y() + (self.responsive.window_height - ph) // 2
        popup.geometry(f"{pw}x{ph}+{px}+{py}")
        popup.configure(bg=ModernTheme.BG_PRIMARY)
        popup.transient(self.root)
        popup.grab_set()

        # Scrollable content
        canvas = tk.Canvas(popup, bg=ModernTheme.BG_PRIMARY, highlightthickness=0)
        scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=ModernTheme.BG_PRIMARY)

        canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=self.responsive.scaled(20),
                   pady=self.responsive.scaled(20))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Header
        name = tk.Label(content, text=info['name'],
                       font=self.fonts['title'],
                       fg=ModernTheme.ACCENT_VIOLET,
                       bg=ModernTheme.BG_PRIMARY)
        name.pack(anchor="w")

        meta = tk.Label(content, text=f"{info['group']}  •  {info['origin']}",
                       font=self.fonts['caption'],
                       fg=ModernTheme.TEXT_SECONDARY,
                       bg=ModernTheme.BG_PRIMARY)
        meta.pack(anchor="w", pady=(2, self.responsive.scaled(15)))

        # Info items
        items = [
            ("Size", f"{info['size']['weight']}, {info['size']['height']}"),
            ("Lifespan", info['lifespan']),
            ("Temperament", ", ".join(info['temperament'])),
            ("Exercise", info['exercise']),
            ("Grooming", info['grooming']),
            ("Trainability", info['trainability']),
        ]

        for label, value in items:
            row = tk.Frame(content, bg=ModernTheme.BG_PRIMARY)
            row.pack(fill=tk.X, pady=self.responsive.scaled(4))

            lbl = tk.Label(row, text=label,
                          font=self.fonts['caption'],
                          fg=ModernTheme.ACCENT_PURPLE,
                          bg=ModernTheme.BG_PRIMARY,
                          width=12, anchor="w")
            lbl.pack(side=tk.LEFT)

            val = tk.Label(row, text=value,
                          font=self.fonts['caption'],
                          fg=ModernTheme.TEXT_PRIMARY,
                          bg=ModernTheme.BG_PRIMARY,
                          wraplength=self.responsive.scaled(300), justify=tk.LEFT)
            val.pack(side=tk.LEFT, fill=tk.X)

        # Fun fact
        fact_card = tk.Frame(content, bg=ModernTheme.GLASS_BG)
        fact_card.pack(fill=tk.X, pady=self.responsive.scaled(10))

        fact_inner = tk.Frame(fact_card, bg=ModernTheme.GLASS_BG)
        fact_inner.pack(fill=tk.X, padx=self.responsive.scaled(12), pady=self.responsive.scaled(12))

        fact_title = tk.Label(fact_inner, text="Fun Fact",
                             font=self.fonts['caption'],
                             fg=ModernTheme.ACCENT_ORANGE,
                             bg=ModernTheme.GLASS_BG)
        fact_title.pack(anchor="w")

        fact_text = tk.Label(fact_inner, text=info['fun_fact'],
                            font=self.fonts['small'],
                            fg=ModernTheme.TEXT_PRIMARY,
                            bg=ModernTheme.GLASS_BG,
                            wraplength=self.responsive.scaled(400), justify=tk.LEFT)
        fact_text.pack(anchor="w", pady=(4, 0))

        # Buttons
        btn_row = tk.Frame(content, bg=ModernTheme.BG_PRIMARY)
        btn_row.pack(pady=self.responsive.scaled(15))

        def open_images():
            url = f"https://www.google.com/search?tbm=isch&q={info['name'].replace(' ', '+')}+dog+breed"
            webbrowser.open(url)

        img_btn = self.create_gradient_button(btn_row, "View Images",
                                             open_images, ModernTheme.ACCENT_PINK)
        img_btn.pack(side=tk.LEFT, padx=self.responsive.scaled(4))

        close_btn = self.create_gradient_button(btn_row, "Close",
                                               popup.destroy, ModernTheme.BG_TERTIARY)
        close_btn.pack(side=tk.LEFT, padx=self.responsive.scaled(4))


def main():
    """Main entry point."""
    root = tk.Tk()
    app = CanineClassifierApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
