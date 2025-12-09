#!/usr/bin/env python3
"""
Canine Classifier - GUI Version
A graphical interface for dog breed identification.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import font as tkfont
import os
import sys

# Import our modules
try:
    from breed_info import get_breed_info, BREED_INFO
    BREED_INFO_AVAILABLE = True
except ImportError:
    BREED_INFO_AVAILABLE = False
    BREED_INFO = {}

try:
    from image_classifier import DogImageClassifier
    IMAGE_CLASSIFIER_AVAILABLE = True
except ImportError:
    IMAGE_CLASSIFIER_AVAILABLE = False


class CanineClassifierGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🐕 Canine Classifier - Dog Breed Identification")
        self.root.geometry("900x700")
        self.root.configure(bg="#1a1a2e")

        # Try to set icon
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        # Colors
        self.colors = {
            "bg": "#1a1a2e",
            "card": "#16213e",
            "accent": "#0f3460",
            "highlight": "#e94560",
            "text": "#ffffff",
            "text_dim": "#a0a0a0",
            "success": "#4ecca3",
            "warning": "#ffc107"
        }

        # Fonts
        self.title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.heading_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
        self.normal_font = tkfont.Font(family="Helvetica", size=11)
        self.small_font = tkfont.Font(family="Helvetica", size=9)

        # Image classifier
        self.classifier = None

        # Build UI
        self.create_widgets()

    def create_widgets(self):
        """Create the main UI layout."""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        title_frame.pack(fill=tk.X, pady=(0, 20))

        title_label = tk.Label(
            title_frame,
            text="🐕 Canine Classifier",
            font=self.title_font,
            fg=self.colors["text"],
            bg=self.colors["bg"]
        )
        title_label.pack()

        subtitle_label = tk.Label(
            title_frame,
            text="Identify Your Dog's Breed with AI & Science",
            font=self.normal_font,
            fg=self.colors["text_dim"],
            bg=self.colors["bg"]
        )
        subtitle_label.pack()

        # Notebook (tabs)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.colors["bg"], borderwidth=0)
        style.configure('TNotebook.Tab',
                       background=self.colors["card"],
                       foreground=self.colors["text"],
                       padding=[20, 10],
                       font=('Helvetica', 11, 'bold'))
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors["highlight"])],
                 foreground=[('selected', self.colors["text"])])

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.create_image_tab()
        self.create_breed_info_tab()
        self.create_breed_list_tab()

    def create_image_tab(self):
        """Create the AI Image Recognition tab."""
        tab = tk.Frame(self.notebook, bg=self.colors["card"])
        self.notebook.add(tab, text="🤖 AI Image Recognition")

        # Instructions
        instr_label = tk.Label(
            tab,
            text="Upload a photo of your dog to identify its breed using AI",
            font=self.normal_font,
            fg=self.colors["text_dim"],
            bg=self.colors["card"]
        )
        instr_label.pack(pady=20)

        # Image selection frame
        select_frame = tk.Frame(tab, bg=self.colors["card"])
        select_frame.pack(pady=10)

        self.image_path_var = tk.StringVar()
        self.image_path_entry = tk.Entry(
            select_frame,
            textvariable=self.image_path_var,
            width=50,
            font=self.normal_font,
            bg=self.colors["accent"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"]
        )
        self.image_path_entry.pack(side=tk.LEFT, padx=(0, 10))

        browse_btn = tk.Button(
            select_frame,
            text="📁 Browse",
            font=self.normal_font,
            bg=self.colors["highlight"],
            fg=self.colors["text"],
            activebackground="#ff6b6b",
            activeforeground=self.colors["text"],
            border=0,
            padx=20,
            pady=5,
            command=self.browse_image
        )
        browse_btn.pack(side=tk.LEFT)

        # Analyze button
        analyze_btn = tk.Button(
            tab,
            text="🔍 Analyze Image",
            font=self.heading_font,
            bg=self.colors["success"],
            fg=self.colors["bg"],
            activebackground="#6deca3",
            activeforeground=self.colors["bg"],
            border=0,
            padx=30,
            pady=10,
            command=self.analyze_image
        )
        analyze_btn.pack(pady=20)

        # Results frame
        results_frame = tk.Frame(tab, bg=self.colors["accent"], padx=20, pady=20)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        results_title = tk.Label(
            results_frame,
            text="Results",
            font=self.heading_font,
            fg=self.colors["text"],
            bg=self.colors["accent"]
        )
        results_title.pack(anchor=tk.W)

        # Results text
        self.results_text = tk.Text(
            results_frame,
            height=15,
            font=self.normal_font,
            bg=self.colors["bg"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=10)
        self.results_text.insert(tk.END, "Results will appear here after analysis...")
        self.results_text.config(state=tk.DISABLED)

    def create_breed_info_tab(self):
        """Create the Breed Information tab."""
        tab = tk.Frame(self.notebook, bg=self.colors["card"])
        self.notebook.add(tab, text="📖 Breed Information")

        # Search frame
        search_frame = tk.Frame(tab, bg=self.colors["card"])
        search_frame.pack(pady=20)

        search_label = tk.Label(
            search_frame,
            text="Search for a breed:",
            font=self.normal_font,
            fg=self.colors["text"],
            bg=self.colors["card"]
        )
        search_label.pack(side=tk.LEFT, padx=(0, 10))

        self.breed_search_var = tk.StringVar()
        breed_combo = ttk.Combobox(
            search_frame,
            textvariable=self.breed_search_var,
            values=sorted([info['name'] for info in BREED_INFO.values()]),
            width=30,
            font=self.normal_font
        )
        breed_combo.pack(side=tk.LEFT, padx=(0, 10))
        breed_combo.bind('<<ComboboxSelected>>', self.show_breed_info)
        breed_combo.bind('<Return>', self.show_breed_info)

        search_btn = tk.Button(
            search_frame,
            text="🔍 Search",
            font=self.normal_font,
            bg=self.colors["highlight"],
            fg=self.colors["text"],
            border=0,
            padx=15,
            pady=5,
            command=self.show_breed_info
        )
        search_btn.pack(side=tk.LEFT)

        # Info display frame
        info_frame = tk.Frame(tab, bg=self.colors["accent"], padx=20, pady=20)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        self.breed_info_text = tk.Text(
            info_frame,
            height=20,
            font=self.normal_font,
            bg=self.colors["bg"],
            fg=self.colors["text"],
            wrap=tk.WORD,
            padx=15,
            pady=15
        )
        self.breed_info_text.pack(fill=tk.BOTH, expand=True)

        # Configure tags for formatting
        self.breed_info_text.tag_configure("title", font=('Helvetica', 16, 'bold'), foreground=self.colors["highlight"])
        self.breed_info_text.tag_configure("heading", font=('Helvetica', 12, 'bold'), foreground=self.colors["success"])
        self.breed_info_text.tag_configure("label", font=('Helvetica', 11, 'bold'), foreground=self.colors["warning"])
        self.breed_info_text.tag_configure("value", font=('Helvetica', 11), foreground=self.colors["text"])
        self.breed_info_text.tag_configure("good", foreground="#4ecca3")
        self.breed_info_text.tag_configure("bad", foreground="#e94560")

        self.breed_info_text.insert(tk.END, "Select a breed to view detailed information...")
        self.breed_info_text.config(state=tk.DISABLED)

    def create_breed_list_tab(self):
        """Create the Breed List tab."""
        tab = tk.Frame(self.notebook, bg=self.colors["card"])
        self.notebook.add(tab, text="📋 All Breeds")

        # Header
        header_label = tk.Label(
            tab,
            text=f"Available Breeds ({len(BREED_INFO)} total)",
            font=self.heading_font,
            fg=self.colors["text"],
            bg=self.colors["card"]
        )
        header_label.pack(pady=20)

        # Create treeview for breed list
        columns = ("Breed", "Group", "Origin", "Size")

        style = ttk.Style()
        style.configure("Treeview",
                       background=self.colors["bg"],
                       foreground=self.colors["text"],
                       fieldbackground=self.colors["bg"],
                       font=('Helvetica', 10))
        style.configure("Treeview.Heading",
                       background=self.colors["accent"],
                       foreground=self.colors["text"],
                       font=('Helvetica', 11, 'bold'))

        tree_frame = tk.Frame(tab, bg=self.colors["card"])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)

        # Define headings
        tree.heading("Breed", text="Breed")
        tree.heading("Group", text="Group")
        tree.heading("Origin", text="Origin")
        tree.heading("Size", text="Size")

        # Define column widths
        tree.column("Breed", width=200)
        tree.column("Group", width=120)
        tree.column("Origin", width=150)
        tree.column("Size", width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Populate tree
        for breed_key in sorted(BREED_INFO.keys()):
            info = BREED_INFO[breed_key]
            tree.insert("", tk.END, values=(
                info['name'],
                info['group'],
                info['origin'],
                info['size']['weight']
            ))

        # Double-click to view breed info
        def on_double_click(event):
            item = tree.selection()
            if item:
                breed_name = tree.item(item[0])['values'][0]
                self.breed_search_var.set(breed_name)
                self.notebook.select(1)  # Switch to breed info tab
                self.show_breed_info()

        tree.bind('<Double-1>', on_double_click)

    def browse_image(self):
        """Open file dialog to select an image."""
        filetypes = [
            ('Image files', '*.jpg *.jpeg *.png *.gif *.bmp'),
            ('All files', '*.*')
        ]
        filename = filedialog.askopenfilename(
            title='Select a dog image',
            filetypes=filetypes
        )
        if filename:
            self.image_path_var.set(filename)

    def analyze_image(self):
        """Analyze the selected image using AI."""
        image_path = self.image_path_var.get().strip()

        if not image_path:
            messagebox.showwarning("No Image", "Please select an image first.")
            return

        if not os.path.exists(image_path):
            messagebox.showerror("Error", f"File not found: {image_path}")
            return

        # Update results to show loading
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "🔄 Loading AI model and analyzing image...\n\n")
        self.results_text.insert(tk.END, "This may take a moment on first run.\n")
        self.results_text.config(state=tk.DISABLED)
        self.root.update()

        try:
            # Load classifier if not already loaded
            if self.classifier is None:
                if not IMAGE_CLASSIFIER_AVAILABLE:
                    raise ImportError("Image classifier not available. Install: pip install transformers torch torchvision Pillow")
                self.classifier = DogImageClassifier()

            # Classify image
            results = self.classifier.classify_image(image_path)

            # Display results
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)

            if results:
                self.results_text.insert(tk.END, "🎉 AI PREDICTION RESULTS\n", "title")
                self.results_text.insert(tk.END, "═" * 50 + "\n\n")

                self.results_text.insert(tk.END, "● = In database (verified)    ○ = AI only\n\n")

                medals = ["🥇", "🥈", "🥉", "  ", "  "]
                for i, result in enumerate(results[:5]):
                    breed = result.get('breed', 'Unknown')
                    confidence = result.get('confidence', 0)
                    verified = result.get('verified', False)
                    db_info = result.get('db_info', {})

                    icon = "●" if verified else "○"
                    medal = medals[i] if i < len(medals) else "  "

                    # Confidence bar
                    bar_filled = int(confidence / 5)
                    bar_empty = 20 - bar_filled
                    bar = "█" * bar_filled + "░" * bar_empty

                    self.results_text.insert(tk.END, f"{medal} {icon} {breed:30} [{bar}] {confidence:5.1f}%\n")

                    if verified and db_info:
                        size = db_info.get('Size', '')
                        coat = db_info.get('Coat', '')
                        ears = db_info.get('Ears', '')
                        self.results_text.insert(tk.END, f"      Database: Size: {size}, Coat: {coat}, Ears: {ears}\n")

                    self.results_text.insert(tk.END, "\n")

                # Count verified
                verified_count = sum(1 for r in results[:5] if r.get('verified', False))
                self.results_text.insert(tk.END, f"ℹ {verified_count} of {min(5, len(results))} predictions found in local database\n")
                self.results_text.insert(tk.END, "ℹ AI Model: Google Vision Transformer (ViT)\n")
            else:
                self.results_text.insert(tk.END, "❌ Could not classify the image.\n")
                self.results_text.insert(tk.END, "Please try a different image.")

        except Exception as e:
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"❌ Error: {str(e)}\n\n")
            self.results_text.insert(tk.END, "Make sure you have installed the required packages:\n")
            self.results_text.insert(tk.END, "pip install transformers torch torchvision Pillow")

        self.results_text.config(state=tk.DISABLED)

    def show_breed_info(self, event=None):
        """Display information about the selected breed."""
        breed_name = self.breed_search_var.get().strip()

        if not breed_name:
            return

        info = get_breed_info(breed_name)

        self.breed_info_text.config(state=tk.NORMAL)
        self.breed_info_text.delete(1.0, tk.END)

        if not info:
            self.breed_info_text.insert(tk.END, f"No information found for '{breed_name}'.\n\n")
            self.breed_info_text.insert(tk.END, "Try searching for one of these breeds:\n")
            for breed_key in sorted(list(BREED_INFO.keys())[:10]):
                self.breed_info_text.insert(tk.END, f"  • {BREED_INFO[breed_key]['name']}\n")
            self.breed_info_text.config(state=tk.DISABLED)
            return

        # Display breed info
        self.breed_info_text.insert(tk.END, f"🐕 {info['name'].upper()}\n", "title")
        self.breed_info_text.insert(tk.END, "═" * 50 + "\n\n")

        # Basic info
        self.breed_info_text.insert(tk.END, "BASIC INFO\n", "heading")
        self.breed_info_text.insert(tk.END, f"Group: ", "label")
        self.breed_info_text.insert(tk.END, f"{info['group']}\n", "value")
        self.breed_info_text.insert(tk.END, f"Origin: ", "label")
        self.breed_info_text.insert(tk.END, f"{info['origin']}\n", "value")
        self.breed_info_text.insert(tk.END, f"Size: ", "label")
        self.breed_info_text.insert(tk.END, f"{info['size']['weight']} ({info['size']['height']})\n", "value")
        self.breed_info_text.insert(tk.END, f"Lifespan: ", "label")
        self.breed_info_text.insert(tk.END, f"{info['lifespan']}\n\n", "value")

        # Temperament
        self.breed_info_text.insert(tk.END, "TEMPERAMENT\n", "heading")
        self.breed_info_text.insert(tk.END, f"{', '.join(info['temperament'])}\n\n", "value")

        # Care needs
        self.breed_info_text.insert(tk.END, "CARE NEEDS\n", "heading")
        self.breed_info_text.insert(tk.END, f"Exercise: ", "label")
        self.breed_info_text.insert(tk.END, f"{info['exercise']}\n", "value")
        self.breed_info_text.insert(tk.END, f"Grooming: ", "label")
        self.breed_info_text.insert(tk.END, f"{info['grooming']}\n", "value")
        self.breed_info_text.insert(tk.END, f"Trainability: ", "label")
        self.breed_info_text.insert(tk.END, f"{info['trainability']}\n", "value")
        self.breed_info_text.insert(tk.END, f"Barking: ", "label")
        self.breed_info_text.insert(tk.END, f"{info['barking']}\n", "value")
        self.breed_info_text.insert(tk.END, f"Shedding: ", "label")
        self.breed_info_text.insert(tk.END, f"{info['shedding']}\n\n", "value")

        # Good with
        self.breed_info_text.insert(tk.END, "GOOD WITH\n", "heading")
        gw = info['good_with']
        for category, good in [("Kids", gw['kids']), ("Dogs", gw['dogs']), ("Cats", gw['cats']), ("Strangers", gw['strangers'])]:
            self.breed_info_text.insert(tk.END, f"{category}: ", "label")
            if good:
                self.breed_info_text.insert(tk.END, "✓ Yes\n", "good")
            else:
                self.breed_info_text.insert(tk.END, "✗ No\n", "bad")
        self.breed_info_text.insert(tk.END, "\n")

        # Health issues
        self.breed_info_text.insert(tk.END, "HEALTH WATCH\n", "heading")
        self.breed_info_text.insert(tk.END, f"{', '.join(info['health_issues'])}\n\n", "value")

        # Fun fact
        self.breed_info_text.insert(tk.END, "💡 FUN FACT\n", "heading")
        self.breed_info_text.insert(tk.END, f"{info['fun_fact']}\n\n", "value")

        # Similar breeds
        self.breed_info_text.insert(tk.END, "SIMILAR BREEDS\n", "heading")
        self.breed_info_text.insert(tk.END, f"{', '.join(info['similar_breeds'])}\n", "value")

        self.breed_info_text.config(state=tk.DISABLED)


def main():
    """Launch the GUI application."""
    root = tk.Tk()
    app = CanineClassifierGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
