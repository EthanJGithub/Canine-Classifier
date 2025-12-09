#!/usr/bin/env python3
"""
Canine Classifier - Beautiful GUI Application
A modern, feature-rich dog breed identification tool with AI-powered recognition.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
import sys
import threading

# Import breed info
try:
    from breed_info import BREED_INFO, get_breed_info
    BREED_INFO_AVAILABLE = True
except ImportError:
    BREED_INFO_AVAILABLE = False
    BREED_INFO = {}
    def get_breed_info(breed): return None


class ModernStyle:
    """Modern color scheme and styling constants."""
    # Colors
    BG_DARK = "#1a1a2e"
    BG_MEDIUM = "#16213e"
    BG_LIGHT = "#0f3460"
    BG_CARD = "#1f4068"

    ACCENT_PRIMARY = "#e94560"
    ACCENT_SECONDARY = "#00d9ff"
    ACCENT_SUCCESS = "#00ff88"
    ACCENT_WARNING = "#ffaa00"
    ACCENT_ERROR = "#ff4444"

    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#b0b0b0"
    TEXT_DIM = "#707070"

    # Fonts
    FONT_TITLE = ("Segoe UI", 24, "bold")
    FONT_HEADER = ("Segoe UI", 16, "bold")
    FONT_SUBHEADER = ("Segoe UI", 14, "bold")
    FONT_BODY = ("Segoe UI", 11)
    FONT_SMALL = ("Segoe UI", 10)
    FONT_BUTTON = ("Segoe UI", 12, "bold")


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
    """Main GUI Application for Canine Classifier."""

    def __init__(self, root):
        self.root = root
        self.root.title("Canine Classifier - Dog Breed Identification")
        self.root.geometry("1000x750")
        self.root.minsize(900, 650)
        self.root.configure(bg=ModernStyle.BG_DARK)

        # Center window
        self.center_window()

        # Current frame reference
        self.current_frame = None

        # Dichotomous key state
        self.dkey_tree = self._build_dichotomous_tree()
        self.dkey_current_node = None
        self.dkey_question_count = 0

        # Configure styles
        self.configure_styles()

        # Show main menu
        self.show_main_menu()

    def center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def configure_styles(self):
        """Configure ttk styles for modern look."""
        style = ttk.Style()
        style.theme_use('clam')

        # Main button style
        style.configure('Modern.TButton',
                       font=ModernStyle.FONT_BUTTON,
                       padding=(20, 12),
                       background=ModernStyle.ACCENT_PRIMARY,
                       foreground=ModernStyle.TEXT_PRIMARY)

        # Secondary button
        style.configure('Secondary.TButton',
                       font=ModernStyle.FONT_BODY,
                       padding=(15, 8),
                       background=ModernStyle.BG_LIGHT,
                       foreground=ModernStyle.TEXT_PRIMARY)

        # Combobox style
        style.configure('Modern.TCombobox',
                       font=ModernStyle.FONT_BODY,
                       padding=8,
                       fieldbackground=ModernStyle.BG_CARD,
                       background=ModernStyle.BG_CARD,
                       foreground=ModernStyle.TEXT_PRIMARY)

        # Entry style
        style.configure('Modern.TEntry',
                       font=ModernStyle.FONT_BODY,
                       padding=8,
                       fieldbackground=ModernStyle.BG_CARD)

    def clear_frame(self):
        """Clear the current frame."""
        if self.current_frame:
            self.current_frame.destroy()

    def create_header(self, parent, title, subtitle=""):
        """Create a styled header."""
        header_frame = tk.Frame(parent, bg=ModernStyle.BG_DARK)
        header_frame.pack(fill=tk.X, pady=(20, 10))

        # Title
        title_label = tk.Label(header_frame,
                              text=title,
                              font=ModernStyle.FONT_TITLE,
                              fg=ModernStyle.ACCENT_SECONDARY,
                              bg=ModernStyle.BG_DARK)
        title_label.pack()

        # Subtitle
        if subtitle:
            subtitle_label = tk.Label(header_frame,
                                     text=subtitle,
                                     font=ModernStyle.FONT_BODY,
                                     fg=ModernStyle.TEXT_SECONDARY,
                                     bg=ModernStyle.BG_DARK)
            subtitle_label.pack(pady=(5, 0))

        return header_frame

    def create_menu_button(self, parent, text, icon, color, command):
        """Create a styled menu button."""
        btn_frame = tk.Frame(parent, bg=color, cursor="hand2")
        btn_frame.pack(fill=tk.X, pady=8, padx=50)

        # Content frame
        content = tk.Frame(btn_frame, bg=color)
        content.pack(fill=tk.X, padx=20, pady=15)

        # Icon and text
        icon_label = tk.Label(content, text=icon, font=("Segoe UI", 20),
                             fg=ModernStyle.TEXT_PRIMARY, bg=color)
        icon_label.pack(side=tk.LEFT, padx=(0, 15))

        text_label = tk.Label(content, text=text, font=ModernStyle.FONT_SUBHEADER,
                             fg=ModernStyle.TEXT_PRIMARY, bg=color)
        text_label.pack(side=tk.LEFT)

        # Bind click events
        for widget in [btn_frame, content, icon_label, text_label]:
            widget.bind("<Button-1>", lambda e, cmd=command: cmd())
            widget.bind("<Enter>", lambda e, f=btn_frame: f.configure(bg=ModernStyle.ACCENT_PRIMARY))
            widget.bind("<Leave>", lambda e, f=btn_frame, c=color: f.configure(bg=c))

        return btn_frame

    def show_main_menu(self):
        """Display the main menu."""
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=ModernStyle.BG_DARK)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        self.create_header(self.current_frame,
                          "CANINE CLASSIFIER",
                          "Identify your dog's breed using AI, questionnaire, or dichotomous key")

        # Separator
        sep = tk.Frame(self.current_frame, height=2, bg=ModernStyle.BG_LIGHT)
        sep.pack(fill=tk.X, padx=100, pady=20)

        # Menu buttons container
        menu_container = tk.Frame(self.current_frame, bg=ModernStyle.BG_DARK)
        menu_container.pack(fill=tk.BOTH, expand=True, pady=20)

        # Menu options
        menu_items = [
            ("Questionnaire", "[?]", ModernStyle.BG_LIGHT, self.show_questionnaire,
             "Answer questions about your dog's appearance"),
            ("AI Image Recognition", "[AI]", ModernStyle.BG_MEDIUM, self.show_image_recognition,
             "Upload a photo for instant AI analysis"),
            ("Dichotomous Key", "[Y/N]", ModernStyle.BG_CARD, self.show_dichotomous_key,
             "Yes/No branching questions (scientific method)"),
            ("Breed Information", "[i]", ModernStyle.BG_LIGHT, self.show_breed_lookup,
             "Look up detailed info about any breed"),
        ]

        for text, icon, color, command, desc in menu_items:
            btn_frame = tk.Frame(menu_container, bg=color, cursor="hand2")
            btn_frame.pack(fill=tk.X, pady=6, padx=80)

            content = tk.Frame(btn_frame, bg=color)
            content.pack(fill=tk.X, padx=25, pady=18)

            icon_label = tk.Label(content, text=icon, font=("Consolas", 16, "bold"),
                                 fg=ModernStyle.ACCENT_SECONDARY, bg=color)
            icon_label.pack(side=tk.LEFT, padx=(0, 20))

            text_frame = tk.Frame(content, bg=color)
            text_frame.pack(side=tk.LEFT, fill=tk.X)

            text_label = tk.Label(text_frame, text=text, font=ModernStyle.FONT_SUBHEADER,
                                 fg=ModernStyle.TEXT_PRIMARY, bg=color, anchor="w")
            text_label.pack(anchor="w")

            desc_label = tk.Label(text_frame, text=desc, font=ModernStyle.FONT_SMALL,
                                 fg=ModernStyle.TEXT_SECONDARY, bg=color, anchor="w")
            desc_label.pack(anchor="w")

            # Hover effects and click binding
            def on_enter(e, f=btn_frame, c=content, tf=text_frame, il=icon_label, tl=text_label, dl=desc_label):
                for w in [f, c, tf, il, tl, dl]:
                    w.configure(bg=ModernStyle.ACCENT_PRIMARY)

            def on_leave(e, f=btn_frame, c=content, tf=text_frame, il=icon_label, tl=text_label, dl=desc_label, orig=color):
                for w in [f, c, tf, tl, dl]:
                    w.configure(bg=orig)
                il.configure(bg=orig)

            for widget in [btn_frame, content, text_frame, icon_label, text_label, desc_label]:
                widget.bind("<Button-1>", lambda e, cmd=command: cmd())
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)

        # Exit button
        exit_btn = tk.Button(menu_container, text="Exit", font=ModernStyle.FONT_BODY,
                            bg=ModernStyle.ACCENT_ERROR, fg=ModernStyle.TEXT_PRIMARY,
                            relief=tk.FLAT, padx=30, pady=8, cursor="hand2",
                            command=self.root.quit)
        exit_btn.pack(pady=30)

        # Footer
        footer = tk.Label(self.current_frame,
                         text="Canine Classifier v2.0 - AI-Powered Dog Breed Identification",
                         font=ModernStyle.FONT_SMALL,
                         fg=ModernStyle.TEXT_DIM,
                         bg=ModernStyle.BG_DARK)
        footer.pack(side=tk.BOTTOM, pady=15)

    def create_back_button(self, parent):
        """Create a back button."""
        back_btn = tk.Button(parent, text="< Back to Menu", font=ModernStyle.FONT_BODY,
                            bg=ModernStyle.BG_LIGHT, fg=ModernStyle.TEXT_PRIMARY,
                            relief=tk.FLAT, padx=15, pady=5, cursor="hand2",
                            command=self.show_main_menu)
        back_btn.pack(anchor="nw", padx=20, pady=10)
        return back_btn

    # ==================== QUESTIONNAIRE MODE ====================

    def show_questionnaire(self):
        """Display the questionnaire mode."""
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=ModernStyle.BG_DARK)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        self.create_back_button(self.current_frame)
        self.create_header(self.current_frame, "QUESTIONNAIRE MODE",
                          "Answer questions about your dog's physical characteristics")

        # Form container
        form_frame = tk.Frame(self.current_frame, bg=ModernStyle.BG_MEDIUM, padx=40, pady=30)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=60, pady=20)

        # Question options
        self.q_vars = {}
        questions = [
            ("color", "What is the COLOR of your dog?",
             ["Black", "White", "Brown", "Tan", "Brindle", "Merle", "Chocolate", "Yellow"]),
            ("ear_type", "What is the EAR TYPE of your dog?",
             ["Floppy", "Tall", "Triangular"]),
            ("tail_type", "What is the TAIL TYPE of your dog?",
             ["Docked", "Long_and_curved", "Curled"]),
            ("size", "What is the SIZE of your dog?",
             ["Small", "Medium", "Large", "Giant"]),
            ("coat_type", "What is the COAT TYPE of your dog?",
             ["Short", "Medium", "Long", "Curly", "Double", "Smooth", "Dense", "Silky"]),
        ]

        for i, (key, question, options) in enumerate(questions):
            q_frame = tk.Frame(form_frame, bg=ModernStyle.BG_MEDIUM)
            q_frame.pack(fill=tk.X, pady=10)

            label = tk.Label(q_frame, text=question, font=ModernStyle.FONT_BODY,
                           fg=ModernStyle.TEXT_PRIMARY, bg=ModernStyle.BG_MEDIUM)
            label.pack(anchor="w")

            var = tk.StringVar(value=options[0])
            self.q_vars[key] = var

            combo = ttk.Combobox(q_frame, textvariable=var, values=options,
                                state="readonly", font=ModernStyle.FONT_BODY, width=30)
            combo.pack(anchor="w", pady=5)

        # Submit button
        submit_btn = tk.Button(form_frame, text="Find Matching Breeds",
                              font=ModernStyle.FONT_BUTTON,
                              bg=ModernStyle.ACCENT_PRIMARY, fg=ModernStyle.TEXT_PRIMARY,
                              relief=tk.FLAT, padx=30, pady=12, cursor="hand2",
                              command=self.process_questionnaire)
        submit_btn.pack(pady=30)

        # Results area
        self.q_results_frame = tk.Frame(form_frame, bg=ModernStyle.BG_MEDIUM)
        self.q_results_frame.pack(fill=tk.BOTH, expand=True)

    def process_questionnaire(self):
        """Process questionnaire answers and show results."""
        # Clear previous results
        for widget in self.q_results_frame.winfo_children():
            widget.destroy()

        # Get values
        color = self.q_vars["color"].get()
        ear_type = self.q_vars["ear_type"].get().lower()
        tail_type = self.q_vars["tail_type"].get().lower()
        size = self.q_vars["size"].get().lower()
        coat_type = self.q_vars["coat_type"].get().lower()

        # Query database
        db = Database()
        results = db.fetch_dog_breeds(color, ear_type, tail_type, size, coat_type)
        db.close()

        if results:
            # Results header
            header = tk.Label(self.q_results_frame, text="BREED MATCHES",
                            font=ModernStyle.FONT_HEADER,
                            fg=ModernStyle.ACCENT_SUCCESS, bg=ModernStyle.BG_MEDIUM)
            header.pack(pady=(10, 15))

            medals = ["[1st]", "[2nd]", "[3rd]"]
            colors = [ModernStyle.ACCENT_SUCCESS, ModernStyle.ACCENT_SECONDARY, ModernStyle.ACCENT_WARNING]

            for i, (breed, matched, probability) in enumerate(results):
                result_frame = tk.Frame(self.q_results_frame, bg=ModernStyle.BG_CARD, padx=15, pady=10)
                result_frame.pack(fill=tk.X, pady=5)

                # Medal and breed name
                medal_label = tk.Label(result_frame, text=medals[i] if i < 3 else f"[{i+1}]",
                                      font=("Consolas", 12, "bold"),
                                      fg=colors[i] if i < 3 else ModernStyle.TEXT_SECONDARY,
                                      bg=ModernStyle.BG_CARD)
                medal_label.pack(side=tk.LEFT, padx=(0, 10))

                breed_label = tk.Label(result_frame, text=breed,
                                      font=ModernStyle.FONT_SUBHEADER,
                                      fg=ModernStyle.TEXT_PRIMARY, bg=ModernStyle.BG_CARD)
                breed_label.pack(side=tk.LEFT)

                # Probability
                prob_text = f"{probability:.1f}% ({int(matched)}/5 attributes)"
                prob_label = tk.Label(result_frame, text=prob_text,
                                     font=ModernStyle.FONT_BODY,
                                     fg=ModernStyle.TEXT_SECONDARY, bg=ModernStyle.BG_CARD)
                prob_label.pack(side=tk.RIGHT)

                # Make clickable for breed info
                for widget in [result_frame, medal_label, breed_label, prob_label]:
                    widget.bind("<Button-1>", lambda e, b=breed: self.show_breed_info_popup(b))
                    widget.configure(cursor="hand2")

            # Info text
            info_label = tk.Label(self.q_results_frame,
                                text="Click on a breed to see detailed information",
                                font=ModernStyle.FONT_SMALL,
                                fg=ModernStyle.TEXT_DIM, bg=ModernStyle.BG_MEDIUM)
            info_label.pack(pady=(15, 0))
        else:
            no_results = tk.Label(self.q_results_frame,
                                text="No matching breeds found.\nTry different attribute combinations.",
                                font=ModernStyle.FONT_BODY,
                                fg=ModernStyle.ACCENT_WARNING, bg=ModernStyle.BG_MEDIUM)
            no_results.pack(pady=20)

    # ==================== AI IMAGE RECOGNITION ====================

    def show_image_recognition(self):
        """Display the AI image recognition mode."""
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=ModernStyle.BG_DARK)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        self.create_back_button(self.current_frame)
        self.create_header(self.current_frame, "AI IMAGE RECOGNITION",
                          "Upload a photo to identify your dog's breed using AI")

        # Main container
        main_frame = tk.Frame(self.current_frame, bg=ModernStyle.BG_MEDIUM, padx=40, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=60, pady=20)

        # Upload section
        upload_frame = tk.Frame(main_frame, bg=ModernStyle.BG_CARD, padx=30, pady=30)
        upload_frame.pack(fill=tk.X, pady=10)

        upload_icon = tk.Label(upload_frame, text="[IMAGE]", font=("Consolas", 24),
                              fg=ModernStyle.ACCENT_SECONDARY, bg=ModernStyle.BG_CARD)
        upload_icon.pack()

        upload_text = tk.Label(upload_frame, text="Click to select an image of your dog",
                              font=ModernStyle.FONT_BODY,
                              fg=ModernStyle.TEXT_SECONDARY, bg=ModernStyle.BG_CARD)
        upload_text.pack(pady=10)

        # File path display
        self.image_path_var = tk.StringVar(value="No file selected")
        path_label = tk.Label(upload_frame, textvariable=self.image_path_var,
                             font=ModernStyle.FONT_SMALL,
                             fg=ModernStyle.TEXT_DIM, bg=ModernStyle.BG_CARD)
        path_label.pack()

        # Browse button
        browse_btn = tk.Button(upload_frame, text="Browse...", font=ModernStyle.FONT_BODY,
                              bg=ModernStyle.BG_LIGHT, fg=ModernStyle.TEXT_PRIMARY,
                              relief=tk.FLAT, padx=20, pady=8, cursor="hand2",
                              command=self.browse_image)
        browse_btn.pack(pady=15)

        # Classify button
        self.classify_btn = tk.Button(main_frame, text="Classify Image",
                                     font=ModernStyle.FONT_BUTTON,
                                     bg=ModernStyle.ACCENT_PRIMARY, fg=ModernStyle.TEXT_PRIMARY,
                                     relief=tk.FLAT, padx=30, pady=12, cursor="hand2",
                                     command=self.classify_image, state=tk.DISABLED)
        self.classify_btn.pack(pady=20)

        # Status label
        self.ai_status_var = tk.StringVar(value="")
        self.ai_status_label = tk.Label(main_frame, textvariable=self.ai_status_var,
                                       font=ModernStyle.FONT_BODY,
                                       fg=ModernStyle.ACCENT_SECONDARY, bg=ModernStyle.BG_MEDIUM)
        self.ai_status_label.pack()

        # Results area
        self.ai_results_frame = tk.Frame(main_frame, bg=ModernStyle.BG_MEDIUM)
        self.ai_results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Store image path
        self.selected_image_path = None

    def browse_image(self):
        """Open file dialog to select an image."""
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("All files", "*.*")
        ]
        filepath = filedialog.askopenfilename(title="Select Dog Image", filetypes=filetypes)

        if filepath:
            self.selected_image_path = filepath
            # Truncate long paths
            display_path = filepath if len(filepath) < 50 else "..." + filepath[-47:]
            self.image_path_var.set(display_path)
            self.classify_btn.config(state=tk.NORMAL)

    def classify_image(self):
        """Classify the selected image using AI."""
        if not self.selected_image_path:
            return

        # Clear previous results
        for widget in self.ai_results_frame.winfo_children():
            widget.destroy()

        self.ai_status_var.set("Loading AI model... This may take a moment.")
        self.classify_btn.config(state=tk.DISABLED)
        self.root.update()

        # Run classification in thread to prevent GUI freeze
        thread = threading.Thread(target=self._run_classification)
        thread.start()

    def _run_classification(self):
        """Run the classification in a background thread."""
        try:
            from image_classifier import DogImageClassifier
            classifier = DogImageClassifier()

            self.root.after(0, lambda: self.ai_status_var.set("Analyzing image..."))

            results = classifier.classify_image(self.selected_image_path)

            # Update UI in main thread
            self.root.after(0, lambda: self._display_ai_results(results))

        except ImportError as e:
            error_msg = "AI module not available.\nInstall: pip install transformers torch torchvision Pillow"
            self.root.after(0, lambda: self._show_ai_error(error_msg))
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self._show_ai_error(error_msg))

    def _display_ai_results(self, results):
        """Display AI classification results."""
        self.ai_status_var.set("")
        self.classify_btn.config(state=tk.NORMAL)

        # Clear previous results
        for widget in self.ai_results_frame.winfo_children():
            widget.destroy()

        if not results:
            self._show_ai_error("Could not classify the image.")
            return

        # Results header
        header = tk.Label(self.ai_results_frame, text="AI PREDICTION RESULTS",
                        font=ModernStyle.FONT_HEADER,
                        fg=ModernStyle.ACCENT_SUCCESS, bg=ModernStyle.BG_MEDIUM)
        header.pack(pady=(10, 5))

        # Legend
        legend = tk.Label(self.ai_results_frame,
                        text="[DB] = Verified in database    [AI] = AI prediction only",
                        font=ModernStyle.FONT_SMALL,
                        fg=ModernStyle.TEXT_DIM, bg=ModernStyle.BG_MEDIUM)
        legend.pack(pady=(0, 15))

        medals = ["[1st]", "[2nd]", "[3rd]", "[4th]", "[5th]"]

        for i, result in enumerate(results[:5]):
            breed = result.get('breed', 'Unknown')
            confidence = result.get('confidence', 0)
            verified = result.get('verified', False)
            db_name = result.get('db_name', breed)

            result_frame = tk.Frame(self.ai_results_frame, bg=ModernStyle.BG_CARD, padx=15, pady=10)
            result_frame.pack(fill=tk.X, pady=4)

            # Medal
            medal_colors = [ModernStyle.ACCENT_SUCCESS, ModernStyle.ACCENT_SECONDARY,
                          ModernStyle.ACCENT_WARNING, ModernStyle.TEXT_SECONDARY, ModernStyle.TEXT_DIM]
            medal_label = tk.Label(result_frame, text=medals[i],
                                  font=("Consolas", 11, "bold"),
                                  fg=medal_colors[i], bg=ModernStyle.BG_CARD)
            medal_label.pack(side=tk.LEFT, padx=(0, 10))

            # Verification status
            status_text = "[DB]" if verified else "[AI]"
            status_color = ModernStyle.ACCENT_SUCCESS if verified else ModernStyle.TEXT_DIM
            status_label = tk.Label(result_frame, text=status_text,
                                   font=("Consolas", 10),
                                   fg=status_color, bg=ModernStyle.BG_CARD)
            status_label.pack(side=tk.LEFT, padx=(0, 10))

            # Breed name
            display_name = db_name if verified else breed
            breed_label = tk.Label(result_frame, text=display_name,
                                  font=ModernStyle.FONT_BODY,
                                  fg=ModernStyle.TEXT_PRIMARY, bg=ModernStyle.BG_CARD)
            breed_label.pack(side=tk.LEFT)

            # Confidence bar
            bar_frame = tk.Frame(result_frame, bg=ModernStyle.BG_DARK, width=100, height=12)
            bar_frame.pack(side=tk.RIGHT, padx=10)
            bar_frame.pack_propagate(False)

            bar_color = ModernStyle.ACCENT_SUCCESS if confidence >= 70 else (
                ModernStyle.ACCENT_WARNING if confidence >= 40 else ModernStyle.ACCENT_ERROR)
            fill_width = int(confidence)
            bar_fill = tk.Frame(bar_frame, bg=bar_color, width=fill_width, height=12)
            bar_fill.place(x=0, y=0)

            # Confidence percentage
            conf_label = tk.Label(result_frame, text=f"{confidence:.1f}%",
                                 font=ModernStyle.FONT_SMALL,
                                 fg=ModernStyle.TEXT_SECONDARY, bg=ModernStyle.BG_CARD)
            conf_label.pack(side=tk.RIGHT)

            # Make clickable
            if verified or BREED_INFO_AVAILABLE:
                for widget in [result_frame, medal_label, status_label, breed_label, conf_label]:
                    widget.bind("<Button-1>", lambda e, b=display_name: self.show_breed_info_popup(b))
                    widget.configure(cursor="hand2")

        # Info text
        info_label = tk.Label(self.ai_results_frame,
                            text="Click on a breed to see detailed information",
                            font=ModernStyle.FONT_SMALL,
                            fg=ModernStyle.TEXT_DIM, bg=ModernStyle.BG_MEDIUM)
        info_label.pack(pady=(15, 0))

    def _show_ai_error(self, message):
        """Show an AI error message."""
        self.ai_status_var.set("")
        self.classify_btn.config(state=tk.NORMAL)

        for widget in self.ai_results_frame.winfo_children():
            widget.destroy()

        error_label = tk.Label(self.ai_results_frame, text=message,
                              font=ModernStyle.FONT_BODY,
                              fg=ModernStyle.ACCENT_ERROR, bg=ModernStyle.BG_MEDIUM)
        error_label.pack(pady=20)

    # ==================== DICHOTOMOUS KEY ====================

    def _build_dichotomous_tree(self):
        """Build the dichotomous key decision tree."""
        return {
            "question": "Is your dog SMALL (under 25 lbs)?",
            "yes": {
                "question": "Does your dog have FLOPPY ears (hanging down)?",
                "yes": {
                    "question": "Does your dog have a LONG coat?",
                    "yes": {
                        "question": "Does your dog have a CURLED tail?",
                        "yes": {"result": "Shih Tzu"},
                        "no": {"result": "Shetland Sheepdog"}
                    },
                    "no": {
                        "question": "Does your dog have a SILKY coat?",
                        "yes": {"result": "Cavalier King Charles Spaniel"},
                        "no": {"result": "Dachshund"}
                    }
                },
                "no": {
                    "question": "Does your dog have TRIANGULAR (pointed/erect) ears?",
                    "yes": {
                        "question": "Does your dog have a LONG coat?",
                        "yes": {"result": "Pomeranian"},
                        "no": {
                            "question": "Does your dog have a SMOOTH coat?",
                            "yes": {"result": "Pug"},
                            "no": {"result": "Chihuahua"}
                        }
                    },
                    "no": {"result": "Small mixed breed"}
                }
            },
            "no": {
                "question": "Is your dog GIANT sized (over 100 lbs)?",
                "yes": {
                    "question": "Does your dog have a SHORT coat?",
                    "yes": {"result": "Great Dane"},
                    "no": {"result": "Saint Bernard"}
                },
                "no": {
                    "question": "Is your dog LARGE (50-100 lbs)?",
                    "yes": {
                        "question": "Does your dog have FLOPPY ears?",
                        "yes": {
                            "question": "Does your dog have a LONG coat?",
                            "yes": {"result": "Bernese Mountain Dog"},
                            "no": {
                                "question": "Does your dog have a DOUBLE coat?",
                                "yes": {"result": "Siberian Husky"},
                                "no": {"result": "Labrador Retriever"}
                            }
                        },
                        "no": {
                            "question": "Does your dog have a DOCKED tail?",
                            "yes": {"result": "Doberman Pinscher"},
                            "no": {"result": "German Shepherd"}
                        }
                    },
                    "no": {
                        "question": "Does your dog have FLOPPY ears?",
                        "yes": {
                            "question": "Does your dog have a CURLY coat?",
                            "yes": {"result": "Poodle"},
                            "no": {
                                "question": "Does your dog have a MEDIUM length coat?",
                                "yes": {"result": "Border Collie"},
                                "no": {"result": "Beagle"}
                            }
                        },
                        "no": {
                            "question": "Does your dog have a DOUBLE coat?",
                            "yes": {"result": "Shiba Inu"},
                            "no": {"result": "Medium mixed breed"}
                        }
                    }
                }
            }
        }

    def show_dichotomous_key(self):
        """Display the dichotomous key mode."""
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=ModernStyle.BG_DARK)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        self.create_back_button(self.current_frame)
        self.create_header(self.current_frame, "DICHOTOMOUS KEY",
                          "Answer Yes/No questions to identify your dog's breed")

        # Main container
        self.dkey_main_frame = tk.Frame(self.current_frame, bg=ModernStyle.BG_MEDIUM, padx=40, pady=30)
        self.dkey_main_frame.pack(fill=tk.BOTH, expand=True, padx=60, pady=20)

        # Initialize key
        self.dkey_current_node = self.dkey_tree
        self.dkey_question_count = 0

        # Show first question
        self._show_dkey_question()

    def _show_dkey_question(self):
        """Show the current dichotomous key question or result."""
        # Clear frame
        for widget in self.dkey_main_frame.winfo_children():
            widget.destroy()

        node = self.dkey_current_node

        if "result" in node:
            # Show result
            self._show_dkey_result(node["result"])
            return

        # Question counter
        self.dkey_question_count += 1
        counter_label = tk.Label(self.dkey_main_frame,
                                text=f"Question {self.dkey_question_count}",
                                font=ModernStyle.FONT_SMALL,
                                fg=ModernStyle.ACCENT_SECONDARY, bg=ModernStyle.BG_MEDIUM)
        counter_label.pack(pady=(0, 20))

        # Question frame
        q_frame = tk.Frame(self.dkey_main_frame, bg=ModernStyle.BG_CARD, padx=30, pady=30)
        q_frame.pack(fill=tk.X)

        question_label = tk.Label(q_frame, text=node["question"],
                                 font=ModernStyle.FONT_HEADER,
                                 fg=ModernStyle.TEXT_PRIMARY, bg=ModernStyle.BG_CARD,
                                 wraplength=600)
        question_label.pack(pady=20)

        # Buttons frame
        btn_frame = tk.Frame(q_frame, bg=ModernStyle.BG_CARD)
        btn_frame.pack(pady=20)

        yes_btn = tk.Button(btn_frame, text="YES", font=ModernStyle.FONT_BUTTON,
                           bg=ModernStyle.ACCENT_SUCCESS, fg=ModernStyle.TEXT_PRIMARY,
                           relief=tk.FLAT, padx=40, pady=12, cursor="hand2",
                           command=lambda: self._dkey_answer(True))
        yes_btn.pack(side=tk.LEFT, padx=20)

        no_btn = tk.Button(btn_frame, text="NO", font=ModernStyle.FONT_BUTTON,
                          bg=ModernStyle.ACCENT_ERROR, fg=ModernStyle.TEXT_PRIMARY,
                          relief=tk.FLAT, padx=40, pady=12, cursor="hand2",
                          command=lambda: self._dkey_answer(False))
        no_btn.pack(side=tk.LEFT, padx=20)

        # Restart button
        restart_btn = tk.Button(self.dkey_main_frame, text="Start Over",
                               font=ModernStyle.FONT_BODY,
                               bg=ModernStyle.BG_LIGHT, fg=ModernStyle.TEXT_PRIMARY,
                               relief=tk.FLAT, padx=20, pady=8, cursor="hand2",
                               command=self._restart_dkey)
        restart_btn.pack(pady=30)

    def _dkey_answer(self, is_yes):
        """Handle yes/no answer in dichotomous key."""
        self.dkey_current_node = self.dkey_current_node["yes" if is_yes else "no"]
        self._show_dkey_question()

    def _show_dkey_result(self, breed):
        """Show the dichotomous key result."""
        # Result frame
        result_frame = tk.Frame(self.dkey_main_frame, bg=ModernStyle.BG_CARD, padx=30, pady=30)
        result_frame.pack(fill=tk.X, pady=20)

        # Success icon
        icon_label = tk.Label(result_frame, text="[OK]", font=("Consolas", 36),
                             fg=ModernStyle.ACCENT_SUCCESS, bg=ModernStyle.BG_CARD)
        icon_label.pack(pady=10)

        # Result header
        header_label = tk.Label(result_frame, text="IDENTIFICATION COMPLETE!",
                               font=ModernStyle.FONT_HEADER,
                               fg=ModernStyle.ACCENT_SUCCESS, bg=ModernStyle.BG_CARD)
        header_label.pack()

        # Question count
        count_label = tk.Label(result_frame,
                              text=f"Based on {self.dkey_question_count} questions:",
                              font=ModernStyle.FONT_BODY,
                              fg=ModernStyle.TEXT_SECONDARY, bg=ModernStyle.BG_CARD)
        count_label.pack(pady=(10, 20))

        # Breed result
        breed_label = tk.Label(result_frame, text=breed,
                              font=("Segoe UI", 28, "bold"),
                              fg=ModernStyle.ACCENT_SECONDARY, bg=ModernStyle.BG_CARD)
        breed_label.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(self.dkey_main_frame, bg=ModernStyle.BG_MEDIUM)
        btn_frame.pack(pady=20)

        info_btn = tk.Button(btn_frame, text="View Breed Info",
                            font=ModernStyle.FONT_BODY,
                            bg=ModernStyle.ACCENT_PRIMARY, fg=ModernStyle.TEXT_PRIMARY,
                            relief=tk.FLAT, padx=20, pady=10, cursor="hand2",
                            command=lambda: self.show_breed_info_popup(breed))
        info_btn.pack(side=tk.LEFT, padx=10)

        restart_btn = tk.Button(btn_frame, text="Start Over",
                               font=ModernStyle.FONT_BODY,
                               bg=ModernStyle.BG_LIGHT, fg=ModernStyle.TEXT_PRIMARY,
                               relief=tk.FLAT, padx=20, pady=10, cursor="hand2",
                               command=self._restart_dkey)
        restart_btn.pack(side=tk.LEFT, padx=10)

    def _restart_dkey(self):
        """Restart the dichotomous key."""
        self.dkey_current_node = self.dkey_tree
        self.dkey_question_count = 0
        self._show_dkey_question()

    # ==================== BREED INFORMATION ====================

    def show_breed_lookup(self):
        """Display the breed information lookup mode."""
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=ModernStyle.BG_DARK)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        self.create_back_button(self.current_frame)
        self.create_header(self.current_frame, "BREED INFORMATION",
                          "Look up detailed information about any dog breed")

        # Main container
        main_frame = tk.Frame(self.current_frame, bg=ModernStyle.BG_MEDIUM, padx=40, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=60, pady=20)

        # Search frame
        search_frame = tk.Frame(main_frame, bg=ModernStyle.BG_MEDIUM)
        search_frame.pack(fill=tk.X, pady=10)

        search_label = tk.Label(search_frame, text="Search for a breed:",
                               font=ModernStyle.FONT_BODY,
                               fg=ModernStyle.TEXT_PRIMARY, bg=ModernStyle.BG_MEDIUM)
        search_label.pack(anchor="w")

        # Get all breed names
        breed_names = sorted([info['name'] for info in BREED_INFO.values()]) if BREED_INFO else []

        self.breed_search_var = tk.StringVar()
        search_combo = ttk.Combobox(search_frame, textvariable=self.breed_search_var,
                                   values=breed_names, font=ModernStyle.FONT_BODY, width=40)
        search_combo.pack(anchor="w", pady=10)
        search_combo.bind("<<ComboboxSelected>>", lambda e: self._lookup_breed())
        search_combo.bind("<Return>", lambda e: self._lookup_breed())

        search_btn = tk.Button(search_frame, text="Look Up", font=ModernStyle.FONT_BODY,
                              bg=ModernStyle.ACCENT_PRIMARY, fg=ModernStyle.TEXT_PRIMARY,
                              relief=tk.FLAT, padx=20, pady=8, cursor="hand2",
                              command=self._lookup_breed)
        search_btn.pack(anchor="w", pady=5)

        # Results area with scrollbar
        results_container = tk.Frame(main_frame, bg=ModernStyle.BG_MEDIUM)
        results_container.pack(fill=tk.BOTH, expand=True, pady=20)

        # Canvas for scrolling
        self.breed_canvas = tk.Canvas(results_container, bg=ModernStyle.BG_MEDIUM,
                                     highlightthickness=0)
        scrollbar = ttk.Scrollbar(results_container, orient="vertical",
                                 command=self.breed_canvas.yview)

        self.breed_results_frame = tk.Frame(self.breed_canvas, bg=ModernStyle.BG_MEDIUM)

        self.breed_canvas.create_window((0, 0), window=self.breed_results_frame, anchor="nw")
        self.breed_canvas.configure(yscrollcommand=scrollbar.set)

        self.breed_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Update scroll region when frame changes
        self.breed_results_frame.bind("<Configure>",
            lambda e: self.breed_canvas.configure(scrollregion=self.breed_canvas.bbox("all")))

        # Show breed list initially
        self._show_breed_list()

    def _show_breed_list(self):
        """Show a list of all available breeds."""
        for widget in self.breed_results_frame.winfo_children():
            widget.destroy()

        if not BREED_INFO:
            no_info = tk.Label(self.breed_results_frame,
                              text="Breed information not available.",
                              font=ModernStyle.FONT_BODY,
                              fg=ModernStyle.ACCENT_WARNING, bg=ModernStyle.BG_MEDIUM)
            no_info.pack(pady=20)
            return

        header = tk.Label(self.breed_results_frame,
                        text=f"Available Breeds ({len(BREED_INFO)} total)",
                        font=ModernStyle.FONT_SUBHEADER,
                        fg=ModernStyle.ACCENT_SECONDARY, bg=ModernStyle.BG_MEDIUM)
        header.pack(pady=(0, 15))

        # Create grid of breeds
        breeds_per_row = 3
        current_row = None

        for i, (key, info) in enumerate(sorted(BREED_INFO.items())):
            if i % breeds_per_row == 0:
                current_row = tk.Frame(self.breed_results_frame, bg=ModernStyle.BG_MEDIUM)
                current_row.pack(fill=tk.X, pady=2)

            breed_btn = tk.Button(current_row, text=info['name'],
                                 font=ModernStyle.FONT_SMALL,
                                 bg=ModernStyle.BG_CARD, fg=ModernStyle.TEXT_PRIMARY,
                                 relief=tk.FLAT, padx=10, pady=5, cursor="hand2",
                                 width=25, anchor="w",
                                 command=lambda b=info['name']: self._display_breed_info(b))
            breed_btn.pack(side=tk.LEFT, padx=5, pady=2)

    def _lookup_breed(self):
        """Look up the selected breed."""
        breed_name = self.breed_search_var.get().strip()
        if breed_name:
            self._display_breed_info(breed_name)

    def _display_breed_info(self, breed_name):
        """Display detailed breed information."""
        info = get_breed_info(breed_name)

        for widget in self.breed_results_frame.winfo_children():
            widget.destroy()

        if not info:
            no_info = tk.Label(self.breed_results_frame,
                              text=f"No information found for '{breed_name}'",
                              font=ModernStyle.FONT_BODY,
                              fg=ModernStyle.ACCENT_WARNING, bg=ModernStyle.BG_MEDIUM)
            no_info.pack(pady=20)

            back_btn = tk.Button(self.breed_results_frame, text="Back to List",
                                font=ModernStyle.FONT_BODY,
                                bg=ModernStyle.BG_LIGHT, fg=ModernStyle.TEXT_PRIMARY,
                                relief=tk.FLAT, padx=15, pady=5, cursor="hand2",
                                command=self._show_breed_list)
            back_btn.pack()
            return

        # Back button
        back_btn = tk.Button(self.breed_results_frame, text="< Back to List",
                            font=ModernStyle.FONT_SMALL,
                            bg=ModernStyle.BG_LIGHT, fg=ModernStyle.TEXT_PRIMARY,
                            relief=tk.FLAT, padx=10, pady=3, cursor="hand2",
                            command=self._show_breed_list)
        back_btn.pack(anchor="w", pady=(0, 10))

        # Info card
        card = tk.Frame(self.breed_results_frame, bg=ModernStyle.BG_CARD, padx=25, pady=20)
        card.pack(fill=tk.X)

        # Header
        name_label = tk.Label(card, text=info['name'].upper(),
                             font=ModernStyle.FONT_TITLE,
                             fg=ModernStyle.ACCENT_SECONDARY, bg=ModernStyle.BG_CARD)
        name_label.pack(anchor="w")

        # Basic info
        basic_text = f"{info['group']} | {info['origin']} | Lifespan: {info['lifespan']}"
        basic_label = tk.Label(card, text=basic_text,
                              font=ModernStyle.FONT_BODY,
                              fg=ModernStyle.TEXT_SECONDARY, bg=ModernStyle.BG_CARD)
        basic_label.pack(anchor="w", pady=(5, 15))

        # Size
        size_text = f"Size: {info['size']['weight']}, {info['size']['height']}"
        size_label = tk.Label(card, text=size_text,
                             font=ModernStyle.FONT_BODY,
                             fg=ModernStyle.TEXT_PRIMARY, bg=ModernStyle.BG_CARD)
        size_label.pack(anchor="w")

        # Temperament
        temp_text = f"Temperament: {', '.join(info['temperament'])}"
        temp_label = tk.Label(card, text=temp_text,
                             font=ModernStyle.FONT_BODY,
                             fg=ModernStyle.TEXT_PRIMARY, bg=ModernStyle.BG_CARD)
        temp_label.pack(anchor="w", pady=(10, 0))

        # Exercise
        exercise_label = tk.Label(card, text=f"Exercise: {info['exercise']}",
                                 font=ModernStyle.FONT_BODY,
                                 fg=ModernStyle.TEXT_PRIMARY, bg=ModernStyle.BG_CARD)
        exercise_label.pack(anchor="w", pady=(5, 0))

        # Grooming
        grooming_label = tk.Label(card, text=f"Grooming: {info['grooming']}",
                                 font=ModernStyle.FONT_BODY,
                                 fg=ModernStyle.TEXT_PRIMARY, bg=ModernStyle.BG_CARD)
        grooming_label.pack(anchor="w", pady=(5, 0))

        # Trainability
        train_label = tk.Label(card, text=f"Trainability: {info['trainability']}",
                              font=ModernStyle.FONT_BODY,
                              fg=ModernStyle.TEXT_PRIMARY, bg=ModernStyle.BG_CARD)
        train_label.pack(anchor="w", pady=(5, 0))

        # Good with section
        gw = info['good_with']
        gw_frame = tk.Frame(card, bg=ModernStyle.BG_CARD)
        gw_frame.pack(anchor="w", pady=(15, 0))

        gw_title = tk.Label(gw_frame, text="Good with: ",
                           font=ModernStyle.FONT_BODY,
                           fg=ModernStyle.TEXT_SECONDARY, bg=ModernStyle.BG_CARD)
        gw_title.pack(side=tk.LEFT)

        for item, value in [("Kids", gw['kids']), ("Dogs", gw['dogs']),
                           ("Cats", gw['cats']), ("Strangers", gw['strangers'])]:
            color = ModernStyle.ACCENT_SUCCESS if value else ModernStyle.ACCENT_ERROR
            symbol = "[Y]" if value else "[N]"
            item_label = tk.Label(gw_frame, text=f"{item} {symbol}  ",
                                 font=ModernStyle.FONT_SMALL,
                                 fg=color, bg=ModernStyle.BG_CARD)
            item_label.pack(side=tk.LEFT)

        # Barking and Shedding
        bs_text = f"Barking: {info['barking']} | Shedding: {info['shedding']}"
        bs_label = tk.Label(card, text=bs_text,
                           font=ModernStyle.FONT_BODY,
                           fg=ModernStyle.TEXT_PRIMARY, bg=ModernStyle.BG_CARD)
        bs_label.pack(anchor="w", pady=(10, 0))

        # Health issues
        health_text = f"Health Watch: {', '.join(info['health_issues'][:4])}"
        health_label = tk.Label(card, text=health_text,
                               font=ModernStyle.FONT_BODY,
                               fg=ModernStyle.ACCENT_WARNING, bg=ModernStyle.BG_CARD)
        health_label.pack(anchor="w", pady=(10, 0))

        # Fun fact
        fact_frame = tk.Frame(card, bg=ModernStyle.BG_LIGHT, padx=15, pady=10)
        fact_frame.pack(fill=tk.X, pady=(15, 0))

        fact_title = tk.Label(fact_frame, text="Fun Fact:",
                             font=ModernStyle.FONT_SUBHEADER,
                             fg=ModernStyle.ACCENT_SECONDARY, bg=ModernStyle.BG_LIGHT)
        fact_title.pack(anchor="w")

        fact_text = tk.Label(fact_frame, text=info['fun_fact'],
                            font=ModernStyle.FONT_BODY,
                            fg=ModernStyle.TEXT_PRIMARY, bg=ModernStyle.BG_LIGHT,
                            wraplength=500, justify=tk.LEFT)
        fact_text.pack(anchor="w", pady=(5, 0))

        # Similar breeds
        similar_text = f"Similar breeds: {', '.join(info['similar_breeds'])}"
        similar_label = tk.Label(card, text=similar_text,
                                font=ModernStyle.FONT_SMALL,
                                fg=ModernStyle.TEXT_DIM, bg=ModernStyle.BG_CARD)
        similar_label.pack(anchor="w", pady=(15, 0))

    def show_breed_info_popup(self, breed_name):
        """Show breed info in a popup window."""
        info = get_breed_info(breed_name)

        if not info:
            messagebox.showinfo("Breed Info", f"No detailed information available for {breed_name}")
            return

        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title(f"{info['name']} - Breed Information")
        popup.geometry("600x700")
        popup.configure(bg=ModernStyle.BG_DARK)
        popup.transient(self.root)
        popup.grab_set()

        # Scrollable content
        canvas = tk.Canvas(popup, bg=ModernStyle.BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        content_frame = tk.Frame(canvas, bg=ModernStyle.BG_DARK)

        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        content_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Header
        name_label = tk.Label(content_frame, text=info['name'].upper(),
                             font=ModernStyle.FONT_TITLE,
                             fg=ModernStyle.ACCENT_SECONDARY, bg=ModernStyle.BG_DARK)
        name_label.pack(anchor="w", pady=(0, 10))

        # Basic info
        basic_text = f"{info['group']} | {info['origin']}"
        basic_label = tk.Label(content_frame, text=basic_text,
                              font=ModernStyle.FONT_BODY,
                              fg=ModernStyle.TEXT_SECONDARY, bg=ModernStyle.BG_DARK)
        basic_label.pack(anchor="w")

        # Create info sections
        sections = [
            ("Size", f"{info['size']['weight']}, {info['size']['height']}"),
            ("Lifespan", info['lifespan']),
            ("Temperament", ", ".join(info['temperament'])),
            ("Exercise", info['exercise']),
            ("Grooming", info['grooming']),
            ("Trainability", info['trainability']),
            ("Barking", info['barking']),
            ("Shedding", info['shedding']),
        ]

        for title, value in sections:
            section_frame = tk.Frame(content_frame, bg=ModernStyle.BG_DARK)
            section_frame.pack(fill=tk.X, pady=5)

            title_label = tk.Label(section_frame, text=f"{title}:",
                                  font=ModernStyle.FONT_BODY,
                                  fg=ModernStyle.ACCENT_SECONDARY, bg=ModernStyle.BG_DARK,
                                  width=12, anchor="w")
            title_label.pack(side=tk.LEFT)

            value_label = tk.Label(section_frame, text=value,
                                  font=ModernStyle.FONT_BODY,
                                  fg=ModernStyle.TEXT_PRIMARY, bg=ModernStyle.BG_DARK,
                                  wraplength=400, justify=tk.LEFT)
            value_label.pack(side=tk.LEFT, fill=tk.X)

        # Good with
        gw = info['good_with']
        gw_frame = tk.Frame(content_frame, bg=ModernStyle.BG_DARK)
        gw_frame.pack(fill=tk.X, pady=10)

        gw_title = tk.Label(gw_frame, text="Good with:",
                           font=ModernStyle.FONT_BODY,
                           fg=ModernStyle.ACCENT_SECONDARY, bg=ModernStyle.BG_DARK,
                           width=12, anchor="w")
        gw_title.pack(side=tk.LEFT)

        gw_values = tk.Frame(gw_frame, bg=ModernStyle.BG_DARK)
        gw_values.pack(side=tk.LEFT)

        for item, value in [("Kids", gw['kids']), ("Dogs", gw['dogs']),
                           ("Cats", gw['cats']), ("Strangers", gw['strangers'])]:
            color = ModernStyle.ACCENT_SUCCESS if value else ModernStyle.ACCENT_ERROR
            symbol = "[Y]" if value else "[N]"
            item_label = tk.Label(gw_values, text=f"{item} {symbol}  ",
                                 font=ModernStyle.FONT_SMALL,
                                 fg=color, bg=ModernStyle.BG_DARK)
            item_label.pack(side=tk.LEFT)

        # Health issues
        health_frame = tk.Frame(content_frame, bg=ModernStyle.BG_DARK)
        health_frame.pack(fill=tk.X, pady=5)

        health_title = tk.Label(health_frame, text="Health Watch:",
                               font=ModernStyle.FONT_BODY,
                               fg=ModernStyle.ACCENT_WARNING, bg=ModernStyle.BG_DARK,
                               width=12, anchor="w")
        health_title.pack(side=tk.LEFT, anchor="n")

        health_value = tk.Label(health_frame, text=", ".join(info['health_issues']),
                               font=ModernStyle.FONT_BODY,
                               fg=ModernStyle.TEXT_PRIMARY, bg=ModernStyle.BG_DARK,
                               wraplength=400, justify=tk.LEFT)
        health_value.pack(side=tk.LEFT)

        # Fun fact
        fact_card = tk.Frame(content_frame, bg=ModernStyle.BG_CARD, padx=15, pady=15)
        fact_card.pack(fill=tk.X, pady=15)

        fact_title = tk.Label(fact_card, text="Fun Fact:",
                             font=ModernStyle.FONT_SUBHEADER,
                             fg=ModernStyle.ACCENT_SECONDARY, bg=ModernStyle.BG_CARD)
        fact_title.pack(anchor="w")

        fact_text = tk.Label(fact_card, text=info['fun_fact'],
                            font=ModernStyle.FONT_BODY,
                            fg=ModernStyle.TEXT_PRIMARY, bg=ModernStyle.BG_CARD,
                            wraplength=500, justify=tk.LEFT)
        fact_text.pack(anchor="w", pady=(5, 0))

        # Similar breeds
        similar_label = tk.Label(content_frame,
                                text=f"Similar breeds: {', '.join(info['similar_breeds'])}",
                                font=ModernStyle.FONT_SMALL,
                                fg=ModernStyle.TEXT_DIM, bg=ModernStyle.BG_DARK)
        similar_label.pack(anchor="w", pady=(10, 0))

        # Close button
        close_btn = tk.Button(content_frame, text="Close", font=ModernStyle.FONT_BODY,
                             bg=ModernStyle.BG_LIGHT, fg=ModernStyle.TEXT_PRIMARY,
                             relief=tk.FLAT, padx=30, pady=8, cursor="hand2",
                             command=popup.destroy)
        close_btn.pack(pady=20)


def main():
    """Main entry point."""
    root = tk.Tk()

    # Set window icon if available
    try:
        # Try to set icon (won't fail if not available)
        pass
    except:
        pass

    app = CanineClassifierApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
