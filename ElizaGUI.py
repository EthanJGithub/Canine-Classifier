#!/usr/bin/env python3
"""
Canine Classifier - Premium 2025 UI
Navy blue theme with cyan/teal gradients - Ultra sleek design.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
import threading
import webbrowser

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    from breed_info import BREED_INFO, get_breed_info
except ImportError:
    BREED_INFO = {}
    def get_breed_info(breed): return None


class Theme:
    """Navy blue theme with cyan/teal accents."""
    # Navy backgrounds
    BG_DARK = "#0f0f1a"
    BG = "#151528"
    BG2 = "#1a1a35"
    CARD = "#1e1e3f"
    CARD_HOVER = "#252550"
    INPUT = "#12122a"

    # Borders
    BORDER = "#2d2d5a"
    BORDER_LIGHT = "#3a3a70"

    # Accent colors - Cyan/Teal gradient feel
    CYAN = "#00d4aa"
    CYAN_LIGHT = "#00ffcc"
    TEAL = "#00b4d8"
    BLUE = "#0077b6"
    PURPLE = "#7b68ee"
    PINK = "#ff6b9d"
    ORANGE = "#ff9f43"
    GREEN = "#00d26a"
    RED = "#ff6b6b"

    # Text
    WHITE = "#ffffff"
    TEXT = "#e8e8f0"
    TEXT2 = "#a0a0c0"
    MUTED = "#6a6a90"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Canine Classifier")

        # Screen sizing
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        self.w = min(int(sw * 0.82), 1300)
        self.h = min(int(sh * 0.82), 780)
        self.scale = min(self.w / 1300, self.h / 780)

        x, y = (sw - self.w) // 2, (sh - self.h) // 2
        root.geometry(f"{self.w}x{self.h}+{x}+{y}")
        root.configure(bg=Theme.BG_DARK)
        root.minsize(900, 580)

        # Scaled fonts
        b = max(int(11 * self.scale), 9)
        self.F = {
            'hero': ('Segoe UI', int(b*2.2), 'bold'),
            'h1': ('Segoe UI', int(b*1.6), 'bold'),
            'h2': ('Segoe UI', int(b*1.25), 'bold'),
            'h3': ('Segoe UI', int(b*1.1), 'bold'),
            'body': ('Segoe UI', b),
            'sm': ('Segoe UI', int(b*0.9)),
            'xs': ('Segoe UI', int(b*0.8)),
        }

        self.frame = None
        self.classifier = None
        self.tree = self._tree()
        self.node = None
        self.qnum = 0

        # TTK styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox',
                       fieldbackground=Theme.INPUT,
                       background=Theme.CARD,
                       foreground=Theme.TEXT,
                       arrowcolor=Theme.CYAN,
                       borderwidth=0,
                       padding=8)
        style.map('TCombobox',
                 fieldbackground=[('readonly', Theme.INPUT)],
                 selectbackground=[('readonly', Theme.CYAN)])

        self.home()

    def s(self, v):
        return max(int(v * self.scale), 1)

    def clear(self):
        if self.frame:
            self.frame.destroy()

    def card(self, parent, highlight=False):
        """Create a sleek card with border."""
        border = Theme.CYAN if highlight else Theme.BORDER
        return tk.Frame(parent, bg=Theme.CARD,
                       highlightbackground=border,
                       highlightthickness=1)

    def btn(self, parent, text, cmd, style='primary'):
        """Create modern button."""
        colors = {
            'primary': (Theme.CYAN, Theme.BG_DARK),
            'secondary': (Theme.CARD_HOVER, Theme.TEXT),
            'success': (Theme.GREEN, Theme.BG_DARK),
            'danger': (Theme.RED, Theme.WHITE),
            'pink': (Theme.PINK, Theme.WHITE),
        }
        bg, fg = colors.get(style, colors['primary'])

        f = tk.Frame(parent, bg=bg, cursor='hand2')
        l = tk.Label(f, text=text, font=self.F['body'], fg=fg, bg=bg,
                    padx=self.s(20), pady=self.s(10))
        l.pack()

        def enter(e):
            f.config(bg=Theme.CYAN_LIGHT if style == 'primary' else Theme.BORDER_LIGHT)
            l.config(bg=Theme.CYAN_LIGHT if style == 'primary' else Theme.BORDER_LIGHT)
        def leave(e):
            f.config(bg=bg)
            l.config(bg=bg)

        f.bind('<Enter>', enter)
        f.bind('<Leave>', leave)
        f.bind('<Button-1>', lambda e: cmd())
        l.bind('<Button-1>', lambda e: cmd())
        return f

    def back_btn(self, parent):
        """Back navigation button."""
        f = tk.Frame(parent, bg=Theme.BG, cursor='hand2')
        l = tk.Label(f, text="←", font=('Segoe UI', self.s(16)),
                    fg=Theme.CYAN, bg=Theme.BG, padx=self.s(12), pady=self.s(6))
        l.pack()
        f.bind('<Button-1>', lambda e: self.home())
        l.bind('<Button-1>', lambda e: self.home())
        f.bind('<Enter>', lambda e: l.config(fg=Theme.CYAN_LIGHT))
        f.bind('<Leave>', lambda e: l.config(fg=Theme.CYAN))
        return f

    # ══════════════════════════════════════════════════════════════
    # HOME
    # ══════════════════════════════════════════════════════════════
    def home(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Header
        hdr = tk.Frame(self.frame, bg=Theme.BG)
        hdr.pack(fill='x', padx=self.s(50), pady=(self.s(40), self.s(20)))

        # Title with cyan accent
        tk.Label(hdr, text="Canine", font=self.F['hero'],
                fg=Theme.WHITE, bg=Theme.BG).pack(side='left')
        tk.Label(hdr, text="Classifier", font=self.F['hero'],
                fg=Theme.CYAN, bg=Theme.BG).pack(side='left', padx=(self.s(8), 0))

        # Subtitle
        sub = tk.Frame(self.frame, bg=Theme.BG)
        sub.pack(fill='x', padx=self.s(50))
        tk.Label(sub, text="AI-Powered Dog Breed Identification System",
                font=self.F['body'], fg=Theme.TEXT2, bg=Theme.BG).pack(anchor='w')

        # Cards grid
        grid = tk.Frame(self.frame, bg=Theme.BG)
        grid.pack(fill='both', expand=True, padx=self.s(50), pady=self.s(25))
        grid.grid_columnconfigure(0, weight=1, uniform='c')
        grid.grid_columnconfigure(1, weight=1, uniform='c')
        grid.grid_rowconfigure(0, weight=1, uniform='r')
        grid.grid_rowconfigure(1, weight=1, uniform='r')

        items = [
            ("01", "AI Recognition", "Upload a photo for instant breed detection",
             Theme.CYAN, "camera", self.ai_page),
            ("02", "Questionnaire", "Answer questions about your dog's features",
             Theme.PINK, "form", self.quest_page),
            ("03", "Dichotomous Key", "Scientific Yes/No identification method",
             Theme.TEAL, "tree", self.dkey_page),
            ("04", "Breed Database", "Explore detailed info on 51+ breeds",
             Theme.ORANGE, "book", self.db_page),
        ]

        for i, (num, title, desc, color, icon, cmd) in enumerate(items):
            r, c = divmod(i, 2)
            self._menu_card(grid, num, title, desc, color, cmd, r, c)

        # Footer
        foot = tk.Frame(self.frame, bg=Theme.BG)
        foot.pack(side='bottom', fill='x', pady=self.s(15))
        tk.Label(foot, text="v2.0", font=self.F['xs'], fg=Theme.MUTED, bg=Theme.BG).pack(side='left', padx=self.s(50))
        tk.Label(foot, text="51 Breeds  •  AI Powered", font=self.F['xs'], fg=Theme.MUTED, bg=Theme.BG).pack(side='right', padx=self.s(50))

    def _menu_card(self, parent, num, title, desc, color, cmd, row, col):
        """Create premium menu card."""
        c = self.card(parent)
        c.grid(row=row, column=col, padx=self.s(10), pady=self.s(10), sticky='nsew')
        c.config(cursor='hand2')

        inner = tk.Frame(c, bg=Theme.CARD)
        inner.pack(fill='both', expand=True, padx=self.s(25), pady=self.s(22))

        # Top row: number + icon indicator
        top = tk.Frame(inner, bg=Theme.CARD)
        top.pack(fill='x')

        # Number badge
        num_frame = tk.Frame(top, bg=color)
        num_frame.pack(side='left')
        tk.Label(num_frame, text=f" {num} ", font=self.F['h3'],
                fg=Theme.BG_DARK, bg=color, padx=self.s(8), pady=self.s(2)).pack()

        # Title
        tk.Label(inner, text=title, font=self.F['h2'],
                fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w', pady=(self.s(15), self.s(5)))

        # Description
        tk.Label(inner, text=desc, font=self.F['sm'],
                fg=Theme.TEXT2, bg=Theme.CARD).pack(anchor='w')

        # Bottom arrow
        bot = tk.Frame(inner, bg=Theme.CARD)
        bot.pack(side='bottom', fill='x')
        arrow = tk.Label(bot, text="→", font=('Segoe UI', self.s(20)),
                        fg=color, bg=Theme.CARD)
        arrow.pack(side='right')

        # Collect widgets for hover
        widgets = [c, inner, top, num_frame, bot, arrow]
        for w in inner.winfo_children():
            widgets.append(w)

        def enter(e):
            c.config(highlightbackground=color, bg=Theme.CARD_HOVER)
            for w in widgets:
                try: w.config(bg=Theme.CARD_HOVER)
                except: pass

        def leave(e):
            c.config(highlightbackground=Theme.BORDER, bg=Theme.CARD)
            for w in widgets:
                try: w.config(bg=Theme.CARD)
                except: pass
            num_frame.config(bg=color)
            for child in num_frame.winfo_children():
                child.config(bg=color)

        for w in widgets:
            w.bind('<Enter>', enter)
            w.bind('<Leave>', leave)
            w.bind('<Button-1>', lambda e, cmd=cmd: cmd())

    # ══════════════════════════════════════════════════════════════
    # AI RECOGNITION
    # ══════════════════════════════════════════════════════════════
    def ai_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Header
        hdr = tk.Frame(self.frame, bg=Theme.BG)
        hdr.pack(fill='x', padx=self.s(30), pady=(self.s(20), self.s(10)))

        self.back_btn(hdr).pack(side='left')

        title_frame = tk.Frame(hdr, bg=Theme.BG)
        title_frame.pack(side='left', padx=(self.s(15), 0))
        tk.Label(title_frame, text="AI Recognition", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(anchor='w')
        tk.Label(title_frame, text="Upload a photo to identify breed",
                font=self.F['xs'], fg=Theme.TEXT2, bg=Theme.BG).pack(anchor='w')

        # Main content
        content = tk.Frame(self.frame, bg=Theme.BG)
        content.pack(fill='both', expand=True, padx=self.s(30), pady=(0, self.s(20)))

        # Left panel - Upload
        left = tk.Frame(content, bg=Theme.BG)
        left.pack(side='left', fill='both', expand=True, padx=(0, self.s(10)))

        upload_card = self.card(left)
        upload_card.pack(fill='both', expand=True)

        uc_inner = tk.Frame(upload_card, bg=Theme.CARD)
        uc_inner.pack(fill='both', expand=True, padx=self.s(20), pady=self.s(20))

        # Upload title with icon
        uc_top = tk.Frame(uc_inner, bg=Theme.CARD)
        uc_top.pack(fill='x')
        tk.Label(uc_top, text="Upload Image", font=self.F['h3'],
                fg=Theme.WHITE, bg=Theme.CARD).pack(side='left')

        # Preview area
        preview_outer = tk.Frame(uc_inner, bg=Theme.BORDER,
                                highlightbackground=Theme.BORDER,
                                highlightthickness=1)
        preview_outer.pack(fill='both', expand=True, pady=(self.s(15), self.s(10)))

        self.preview_frame = tk.Frame(preview_outer, bg=Theme.INPUT)
        self.preview_frame.pack(fill='both', expand=True, padx=2, pady=2)

        # Placeholder
        self.placeholder = tk.Frame(self.preview_frame, bg=Theme.INPUT)
        self.placeholder.place(relx=0.5, rely=0.5, anchor='center')

        # Plus icon circle
        plus_circle = tk.Frame(self.placeholder, bg=Theme.BORDER, width=self.s(60), height=self.s(60))
        plus_circle.pack()
        plus_circle.pack_propagate(False)
        tk.Label(plus_circle, text="+", font=('Segoe UI', self.s(24)),
                fg=Theme.CYAN, bg=Theme.BORDER).place(relx=0.5, rely=0.5, anchor='center')

        self.prev_txt = tk.Label(self.placeholder, text="Drop image here or browse",
                                font=self.F['sm'], fg=Theme.MUTED, bg=Theme.INPUT)
        self.prev_txt.pack(pady=(self.s(10), 0))

        self.prev_photo = None
        self.prev_lbl = None

        # File name
        self.file_var = tk.StringVar(value="No file selected")
        tk.Label(uc_inner, textvariable=self.file_var, font=self.F['xs'],
                fg=Theme.MUTED, bg=Theme.CARD).pack(pady=(0, self.s(10)))

        # Buttons
        btn_frame = tk.Frame(uc_inner, bg=Theme.CARD)
        btn_frame.pack(fill='x')

        self.btn(btn_frame, "Browse Files", self.browse, 'secondary').pack(side='left', padx=(0, self.s(8)))
        self.btn(btn_frame, "Analyze", self.analyze, 'primary').pack(side='left')

        # Status
        self.status = tk.StringVar()
        tk.Label(uc_inner, textvariable=self.status, font=self.F['sm'],
                fg=Theme.CYAN, bg=Theme.CARD).pack(pady=(self.s(10), 0))

        # Right panel - Results
        right = tk.Frame(content, bg=Theme.BG)
        right.pack(side='left', fill='both', expand=True, padx=(self.s(10), 0))

        results_card = self.card(right)
        results_card.pack(fill='both', expand=True)

        rc_inner = tk.Frame(results_card, bg=Theme.CARD)
        rc_inner.pack(fill='both', expand=True, padx=self.s(20), pady=self.s(20))

        # Results header
        tk.Label(rc_inner, text="Results", font=self.F['h3'],
                fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w')
        tk.Label(rc_inner, text="AI predictions with database verification",
                font=self.F['xs'], fg=Theme.MUTED, bg=Theme.CARD).pack(anchor='w', pady=(0, self.s(10)))

        # Results scrollable area
        results_container = tk.Frame(rc_inner, bg=Theme.CARD)
        results_container.pack(fill='both', expand=True)

        self.res_canvas = tk.Canvas(results_container, bg=Theme.CARD, highlightthickness=0)
        self.res_frame = tk.Frame(self.res_canvas, bg=Theme.CARD)
        self.res_canvas.create_window((0, 0), window=self.res_frame, anchor='nw')
        self.res_canvas.pack(fill='both', expand=True)
        self.res_frame.bind('<Configure>',
            lambda e: self.res_canvas.configure(scrollregion=self.res_canvas.bbox('all')))

        # Initial placeholder
        tk.Label(self.res_frame, text="Upload an image to see results",
                font=self.F['body'], fg=Theme.MUTED, bg=Theme.CARD).pack(pady=self.s(50))

        self.sel_img = None

    def browse(self):
        p = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.gif *.bmp *.webp")])
        if p:
            self.sel_img = p
            n = os.path.basename(p)
            self.file_var.set(n[:30] + "..." if len(n) > 33 else n)
            self._preview(p)

    def _preview(self, p):
        if not PIL_AVAILABLE: return
        try:
            img = Image.open(p)
            if img.mode != 'RGB': img = img.convert('RGB')
            self.preview_frame.update()
            mw = max(self.preview_frame.winfo_width() - 10, 100)
            mh = max(self.preview_frame.winfo_height() - 10, 100)
            r = min(mw/img.width, mh/img.height)
            img = img.resize((int(img.width*r), int(img.height*r)), Image.Resampling.LANCZOS)
            self.prev_photo = ImageTk.PhotoImage(img)
            self.placeholder.place_forget()
            if not self.prev_lbl:
                self.prev_lbl = tk.Label(self.preview_frame, bg=Theme.INPUT)
            self.prev_lbl.config(image=self.prev_photo)
            self.prev_lbl.place(relx=0.5, rely=0.5, anchor='center')
        except: pass

    def analyze(self):
        if not self.sel_img:
            self.status.set("Please select an image first")
            return
        for w in self.res_frame.winfo_children(): w.destroy()
        self.status.set("Analyzing...")
        self.root.update()
        threading.Thread(target=self._classify).start()

    def _classify(self):
        try:
            from image_classifier import DogImageClassifier
            if not self.classifier: self.classifier = DogImageClassifier()
            res = self.classifier.classify_image(self.sel_img)
            self.root.after(0, lambda: self._results(res))
        except Exception as e:
            self.root.after(0, lambda: self.status.set(f"Error: {str(e)[:30]}"))

    def _results(self, res):
        self.status.set("")
        for w in self.res_frame.winfo_children(): w.destroy()

        if not res:
            self.status.set("Could not classify")
            return

        colors = [Theme.CYAN, Theme.TEAL, Theme.PINK, Theme.ORANGE, Theme.PURPLE]

        for i, r in enumerate(res[:5]):
            breed = r.get('breed', '?')
            conf = r.get('confidence', 0)
            verified = r.get('verified', False)
            db_name = r.get('db_name', breed)
            name = db_name if verified else breed

            # Result row
            row = tk.Frame(self.res_frame, bg=Theme.BG2, cursor='hand2')
            row.pack(fill='x', pady=self.s(4))

            inner = tk.Frame(row, bg=Theme.BG2)
            inner.pack(fill='x', padx=self.s(15), pady=self.s(12))

            # Left side
            left = tk.Frame(inner, bg=Theme.BG2)
            left.pack(side='left', fill='x', expand=True)

            # Rank badge
            rank_f = tk.Frame(left, bg=colors[i])
            rank_f.pack(side='left', padx=(0, self.s(12)))
            tk.Label(rank_f, text=f" {i+1} ", font=self.F['h3'],
                    fg=Theme.BG_DARK, bg=colors[i]).pack()

            # Name and status
            name_f = tk.Frame(left, bg=Theme.BG2)
            name_f.pack(side='left')
            tk.Label(name_f, text=name, font=self.F['body'],
                    fg=Theme.WHITE, bg=Theme.BG2).pack(anchor='w')

            st_text = "✓ Verified" if verified else "AI prediction"
            st_color = Theme.GREEN if verified else Theme.MUTED
            tk.Label(name_f, text=st_text, font=self.F['xs'],
                    fg=st_color, bg=Theme.BG2).pack(anchor='w')

            # Right side - progress bar
            right = tk.Frame(inner, bg=Theme.BG2)
            right.pack(side='right')

            bar_w = self.s(100)
            bar_bg = tk.Frame(right, bg=Theme.INPUT, width=bar_w, height=self.s(8))
            bar_bg.pack(side='left', padx=(0, self.s(10)))
            bar_bg.pack_propagate(False)

            fill_w = max(2, int(bar_w * conf / 100))
            tk.Frame(bar_bg, bg=colors[i], width=fill_w).place(x=0, y=0, relheight=1)

            tk.Label(right, text=f"{conf:.1f}%", font=self.F['body'],
                    fg=colors[i], bg=Theme.BG2, width=6).pack(side='left')

            # Click binding
            row.bind('<Button-1>', lambda e, n=name: self.popup(n))
            inner.bind('<Button-1>', lambda e, n=name: self.popup(n))

        tk.Label(self.res_frame, text="Click result for breed details",
                font=self.F['xs'], fg=Theme.MUTED, bg=Theme.CARD).pack(pady=(self.s(15), 0))

    # ══════════════════════════════════════════════════════════════
    # QUESTIONNAIRE
    # ══════════════════════════════════════════════════════════════
    def quest_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Header
        hdr = tk.Frame(self.frame, bg=Theme.BG)
        hdr.pack(fill='x', padx=self.s(30), pady=(self.s(20), self.s(10)))

        self.back_btn(hdr).pack(side='left')

        title_frame = tk.Frame(hdr, bg=Theme.BG)
        title_frame.pack(side='left', padx=(self.s(15), 0))
        tk.Label(title_frame, text="Questionnaire", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(anchor='w')
        tk.Label(title_frame, text="Select your dog's characteristics",
                font=self.F['xs'], fg=Theme.TEXT2, bg=Theme.BG).pack(anchor='w')

        # Content
        content = tk.Frame(self.frame, bg=Theme.BG)
        content.pack(fill='both', expand=True, padx=self.s(30), pady=(0, self.s(20)))

        # Form card
        form_card = self.card(content)
        form_card.pack(fill='x')

        form_inner = tk.Frame(form_card, bg=Theme.CARD)
        form_inner.pack(fill='x', padx=self.s(25), pady=self.s(25))

        # Questions
        self.qvars = {}
        qs = [
            ("color", "Color", ["Black", "White", "Brown", "Tan", "Brindle", "Merle", "Chocolate", "Yellow"]),
            ("ear", "Ear Type", ["Floppy", "Tall", "Triangular"]),
            ("tail", "Tail Type", ["Docked", "Long_and_curved", "Curled"]),
            ("size", "Size", ["Small", "Medium", "Large", "Giant"]),
            ("coat", "Coat Type", ["Short", "Medium", "Long", "Curly", "Double", "Smooth"]),
        ]

        row = None
        for i, (k, l, opts) in enumerate(qs):
            if i % 2 == 0:
                row = tk.Frame(form_inner, bg=Theme.CARD)
                row.pack(fill='x', pady=self.s(8))

            qf = tk.Frame(row, bg=Theme.CARD)
            qf.pack(side='left', fill='x', expand=True, padx=self.s(5))

            tk.Label(qf, text=l, font=self.F['sm'], fg=Theme.TEXT2, bg=Theme.CARD).pack(anchor='w')

            v = tk.StringVar(value=opts[0])
            self.qvars[k] = v

            combo = ttk.Combobox(qf, textvariable=v, values=opts, state='readonly',
                               font=self.F['sm'], width=self.s(22))
            combo.pack(anchor='w', pady=(self.s(4), 0))

        # Button
        btn_f = tk.Frame(content, bg=Theme.BG)
        btn_f.pack(pady=self.s(15))
        self.btn(btn_f, "  Find Matches  ", self.run_quest, 'pink').pack()

        # Results area
        self.qres = tk.Frame(content, bg=Theme.BG)
        self.qres.pack(fill='both', expand=True)

    def run_quest(self):
        for w in self.qres.winfo_children(): w.destroy()

        db = Database()
        res = db.fetch(self.qvars["color"].get(), self.qvars["ear"].get().lower(),
                      self.qvars["tail"].get().lower(), self.qvars["size"].get().lower(),
                      self.qvars["coat"].get().lower())
        db.close()

        if res:
            rc = self.card(self.qres)
            rc.pack(fill='x')
            ri = tk.Frame(rc, bg=Theme.CARD)
            ri.pack(fill='x', padx=self.s(20), pady=self.s(20))

            tk.Label(ri, text="Matches Found", font=self.F['h3'],
                    fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w', pady=(0, self.s(10)))

            colors = [Theme.GREEN, Theme.TEAL, Theme.ORANGE]
            for i, (breed, _, prob) in enumerate(res):
                row = tk.Frame(ri, bg=Theme.BG2, cursor='hand2')
                row.pack(fill='x', pady=self.s(3))
                inner = tk.Frame(row, bg=Theme.BG2)
                inner.pack(fill='x', padx=self.s(15), pady=self.s(10))

                rank_f = tk.Frame(inner, bg=colors[i] if i < 3 else Theme.MUTED)
                rank_f.pack(side='left', padx=(0, self.s(12)))
                tk.Label(rank_f, text=f" {i+1} ", font=self.F['h3'],
                        fg=Theme.BG_DARK, bg=colors[i] if i < 3 else Theme.MUTED).pack()

                tk.Label(inner, text=breed, font=self.F['body'],
                        fg=Theme.WHITE, bg=Theme.BG2).pack(side='left')
                tk.Label(inner, text=f"{prob:.0f}%", font=self.F['body'],
                        fg=Theme.TEXT2, bg=Theme.BG2).pack(side='right')

                row.bind('<Button-1>', lambda e, b=breed: self.popup(b))
        else:
            tk.Label(self.qres, text="No matches found", font=self.F['body'],
                    fg=Theme.MUTED, bg=Theme.BG).pack(pady=self.s(30))

    # ══════════════════════════════════════════════════════════════
    # DICHOTOMOUS KEY
    # ══════════════════════════════════════════════════════════════
    def _tree(self):
        return {
            "q": "Is your dog small (under 25 lbs)?",
            "y": {"q": "Does your dog have floppy ears?",
                  "y": {"q": "Long coat?", "y": {"r": "Shih Tzu"}, "n": {"r": "Cavalier King Charles Spaniel"}},
                  "n": {"q": "Long coat?", "y": {"r": "Pomeranian"}, "n": {"r": "Chihuahua"}}},
            "n": {"q": "Is your dog giant (over 100 lbs)?",
                  "y": {"q": "Short coat?", "y": {"r": "Great Dane"}, "n": {"r": "Saint Bernard"}},
                  "n": {"q": "Large (50-100 lbs)?",
                        "y": {"q": "Floppy ears?", "y": {"r": "Labrador Retriever"}, "n": {"r": "German Shepherd"}},
                        "n": {"q": "Curly coat?", "y": {"r": "Poodle"}, "n": {"r": "Beagle"}}}}
        }

    def dkey_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Header
        hdr = tk.Frame(self.frame, bg=Theme.BG)
        hdr.pack(fill='x', padx=self.s(30), pady=(self.s(20), self.s(10)))

        self.back_btn(hdr).pack(side='left')

        title_frame = tk.Frame(hdr, bg=Theme.BG)
        title_frame.pack(side='left', padx=(self.s(15), 0))
        tk.Label(title_frame, text="Dichotomous Key", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(anchor='w')
        tk.Label(title_frame, text="Answer Yes/No questions",
                font=self.F['xs'], fg=Theme.TEXT2, bg=Theme.BG).pack(anchor='w')

        self.dkey_content = tk.Frame(self.frame, bg=Theme.BG)
        self.dkey_content.pack(fill='both', expand=True, padx=self.s(30), pady=(0, self.s(20)))

        self.node = self.tree
        self.qnum = 0
        self._dkey_q()

    def _dkey_q(self):
        for w in self.dkey_content.winfo_children(): w.destroy()

        if "r" in self.node:
            self._dkey_res(self.node["r"])
            return

        self.qnum += 1

        # Progress indicator
        prog_f = tk.Frame(self.dkey_content, bg=Theme.BG)
        prog_f.pack(fill='x', pady=(0, self.s(15)))
        tk.Label(prog_f, text=f"Question {self.qnum}", font=self.F['sm'],
                fg=Theme.CYAN, bg=Theme.BG).pack(side='left')

        # Question card
        qc = self.card(self.dkey_content)
        qc.pack(fill='x')
        qi = tk.Frame(qc, bg=Theme.CARD)
        qi.pack(fill='x', padx=self.s(30), pady=self.s(35))

        tk.Label(qi, text=self.node["q"], font=self.F['h1'], fg=Theme.WHITE,
                bg=Theme.CARD, wraplength=self.s(500)).pack()

        # Buttons
        btn_f = tk.Frame(self.dkey_content, bg=Theme.BG)
        btn_f.pack(pady=self.s(25))

        self.btn(btn_f, "  Yes  ", lambda: self._dkey_ans(True), 'success').pack(side='left', padx=self.s(8))
        self.btn(btn_f, "  No  ", lambda: self._dkey_ans(False), 'danger').pack(side='left', padx=self.s(8))

        # Restart
        rst = tk.Label(self.dkey_content, text="Start over", font=self.F['sm'],
                      fg=Theme.MUTED, bg=Theme.BG, cursor='hand2')
        rst.pack(pady=self.s(10))
        rst.bind('<Button-1>', lambda e: self._dkey_rst())

    def _dkey_ans(self, yes):
        self.node = self.node["y" if yes else "n"]
        self._dkey_q()

    def _dkey_res(self, breed):
        rc = self.card(self.dkey_content, highlight=True)
        rc.pack(fill='x')
        ri = tk.Frame(rc, bg=Theme.CARD)
        ri.pack(padx=self.s(40), pady=self.s(40))

        # Success icon
        icon_f = tk.Frame(ri, bg=Theme.GREEN, width=self.s(60), height=self.s(60))
        icon_f.pack()
        icon_f.pack_propagate(False)
        tk.Label(icon_f, text="✓", font=('Segoe UI', self.s(28)),
                fg=Theme.BG_DARK, bg=Theme.GREEN).place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(ri, text="Identification Complete", font=self.F['body'],
                fg=Theme.TEXT2, bg=Theme.CARD).pack(pady=(self.s(10), 0))
        tk.Label(ri, text=breed, font=self.F['hero'],
                fg=Theme.CYAN, bg=Theme.CARD).pack(pady=self.s(10))
        tk.Label(ri, text=f"Identified in {self.qnum} questions",
                font=self.F['xs'], fg=Theme.MUTED, bg=Theme.CARD).pack()

        btn_f = tk.Frame(self.dkey_content, bg=Theme.BG)
        btn_f.pack(pady=self.s(20))
        self.btn(btn_f, "View Breed Info", lambda: self.popup(breed), 'primary').pack(side='left', padx=self.s(5))
        self.btn(btn_f, "Try Again", self._dkey_rst, 'secondary').pack(side='left', padx=self.s(5))

    def _dkey_rst(self):
        self.node = self.tree
        self.qnum = 0
        self._dkey_q()

    # ══════════════════════════════════════════════════════════════
    # DATABASE
    # ══════════════════════════════════════════════════════════════
    def db_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG)
        self.frame.pack(fill='both', expand=True)

        # Header
        hdr = tk.Frame(self.frame, bg=Theme.BG)
        hdr.pack(fill='x', padx=self.s(30), pady=(self.s(20), self.s(10)))

        self.back_btn(hdr).pack(side='left')

        title_frame = tk.Frame(hdr, bg=Theme.BG)
        title_frame.pack(side='left', padx=(self.s(15), 0))
        tk.Label(title_frame, text="Breed Database", font=self.F['h1'],
                fg=Theme.WHITE, bg=Theme.BG).pack(anchor='w')
        tk.Label(title_frame, text=f"Explore {len(BREED_INFO)} breeds",
                font=self.F['xs'], fg=Theme.TEXT2, bg=Theme.BG).pack(anchor='w')

        # Search
        search_f = tk.Frame(self.frame, bg=Theme.BG)
        search_f.pack(fill='x', padx=self.s(30), pady=(0, self.s(10)))

        breeds = sorted([i['name'] for i in BREED_INFO.values()]) if BREED_INFO else []
        self.search_var = tk.StringVar()
        combo = ttk.Combobox(search_f, textvariable=self.search_var, values=breeds,
                            font=self.F['body'], width=self.s(35))
        combo.pack(side='left')
        self.btn(search_f, "Search", lambda: self._db_detail(self.search_var.get()),
                'primary').pack(side='left', padx=(self.s(10), 0))

        # Content
        content = tk.Frame(self.frame, bg=Theme.BG)
        content.pack(fill='both', expand=True, padx=self.s(30), pady=(0, self.s(20)))

        canvas = tk.Canvas(content, bg=Theme.BG, highlightthickness=0)
        self.db_frame = tk.Frame(canvas, bg=Theme.BG)
        canvas.create_window((0, 0), window=self.db_frame, anchor='nw')
        canvas.pack(fill='both', expand=True)
        self.db_frame.bind('<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        self._db_grid()

    def _db_grid(self):
        for w in self.db_frame.winfo_children(): w.destroy()
        if not BREED_INFO: return

        row = None
        for i, (k, info) in enumerate(sorted(BREED_INFO.items())):
            if i % 4 == 0:
                row = tk.Frame(self.db_frame, bg=Theme.BG)
                row.pack(fill='x', pady=self.s(3))

            btn = tk.Frame(row, bg=Theme.CARD, cursor='hand2',
                          highlightbackground=Theme.BORDER, highlightthickness=1)
            btn.pack(side='left', padx=self.s(3), fill='x', expand=True)

            lbl = tk.Label(btn, text=info['name'], font=self.F['xs'], fg=Theme.TEXT,
                          bg=Theme.CARD, padx=self.s(8), pady=self.s(10))
            lbl.pack()

            btn.bind('<Button-1>', lambda e, n=info['name']: self._db_detail(n))
            lbl.bind('<Button-1>', lambda e, n=info['name']: self._db_detail(n))
            btn.bind('<Enter>', lambda e, b=btn: b.config(highlightbackground=Theme.CYAN))
            btn.bind('<Leave>', lambda e, b=btn: b.config(highlightbackground=Theme.BORDER))

    def _db_detail(self, name):
        info = get_breed_info(name)
        for w in self.db_frame.winfo_children(): w.destroy()

        if not info:
            tk.Label(self.db_frame, text=f"No info for '{name}'", font=self.F['body'],
                    fg=Theme.MUTED, bg=Theme.BG).pack(pady=self.s(20))
            back = tk.Label(self.db_frame, text="← Back to list", font=self.F['sm'],
                           fg=Theme.CYAN, bg=Theme.BG, cursor='hand2')
            back.pack()
            back.bind('<Button-1>', lambda e: self._db_grid())
            return

        # Back link
        back = tk.Label(self.db_frame, text="← Back to list", font=self.F['sm'],
                       fg=Theme.CYAN, bg=Theme.BG, cursor='hand2')
        back.pack(anchor='w', pady=(0, self.s(10)))
        back.bind('<Button-1>', lambda e: self._db_grid())

        # Info card
        c = self.card(self.db_frame)
        c.pack(fill='x')
        inner = tk.Frame(c, bg=Theme.CARD)
        inner.pack(fill='x', padx=self.s(25), pady=self.s(25))

        tk.Label(inner, text=info['name'], font=self.F['h1'],
                fg=Theme.CYAN, bg=Theme.CARD).pack(anchor='w')
        tk.Label(inner, text=f"{info['group']} • {info['origin']} • {info['lifespan']}",
                font=self.F['sm'], fg=Theme.TEXT2, bg=Theme.CARD).pack(anchor='w', pady=(self.s(3), self.s(15)))

        for lbl, val in [("Size", info['size']['weight']),
                        ("Temperament", ", ".join(info['temperament'][:3])),
                        ("Exercise", info['exercise']),
                        ("Grooming", info['grooming'])]:
            rf = tk.Frame(inner, bg=Theme.CARD)
            rf.pack(fill='x', pady=self.s(3))
            tk.Label(rf, text=lbl, font=self.F['sm'], fg=Theme.MUTED,
                    bg=Theme.CARD, width=12, anchor='w').pack(side='left')
            tk.Label(rf, text=val, font=self.F['sm'], fg=Theme.TEXT,
                    bg=Theme.CARD).pack(side='left')

    # ══════════════════════════════════════════════════════════════
    # POPUP
    # ══════════════════════════════════════════════════════════════
    def popup(self, name):
        info = get_breed_info(name)
        if not info:
            messagebox.showinfo("Info", f"No data for {name}")
            return

        p = tk.Toplevel(self.root)
        p.title(info['name'])

        pw, ph = min(self.s(450), self.w-80), min(self.s(480), self.h-80)
        px = self.root.winfo_x() + (self.w - pw) // 2
        py = self.root.winfo_y() + (self.h - ph) // 2
        p.geometry(f"{pw}x{ph}+{px}+{py}")
        p.configure(bg=Theme.BG)
        p.transient(self.root)
        p.grab_set()

        # Scrollable content
        canvas = tk.Canvas(p, bg=Theme.BG, highlightthickness=0)
        content = tk.Frame(canvas, bg=Theme.BG)
        canvas.create_window((0, 0), window=content, anchor='nw')
        canvas.pack(fill='both', expand=True, padx=self.s(20), pady=self.s(20))
        content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        # Header
        tk.Label(content, text=info['name'], font=self.F['h1'],
                fg=Theme.CYAN, bg=Theme.BG).pack(anchor='w')
        tk.Label(content, text=f"{info['group']} • {info['origin']}",
                font=self.F['sm'], fg=Theme.TEXT2, bg=Theme.BG).pack(anchor='w', pady=(self.s(3), self.s(15)))

        # Info items
        for lbl, val in [("Size", f"{info['size']['weight']}, {info['size']['height']}"),
                        ("Lifespan", info['lifespan']),
                        ("Temperament", ", ".join(info['temperament'])),
                        ("Exercise", info['exercise']),
                        ("Grooming", info['grooming']),
                        ("Trainability", info['trainability'])]:
            rf = tk.Frame(content, bg=Theme.BG)
            rf.pack(fill='x', pady=self.s(4))
            tk.Label(rf, text=lbl, font=self.F['sm'], fg=Theme.CYAN,
                    bg=Theme.BG, width=12, anchor='w').pack(side='left')
            tk.Label(rf, text=val, font=self.F['sm'], fg=Theme.TEXT,
                    bg=Theme.BG, wraplength=self.s(250)).pack(side='left', fill='x')

        # Fun fact card
        fc = tk.Frame(content, bg=Theme.CARD)
        fc.pack(fill='x', pady=self.s(15))
        fi = tk.Frame(fc, bg=Theme.CARD)
        fi.pack(fill='x', padx=self.s(12), pady=self.s(12))
        tk.Label(fi, text="Fun Fact", font=self.F['sm'], fg=Theme.ORANGE, bg=Theme.CARD).pack(anchor='w')
        tk.Label(fi, text=info['fun_fact'], font=self.F['xs'], fg=Theme.TEXT,
                bg=Theme.CARD, wraplength=self.s(350), justify='left').pack(anchor='w', pady=(self.s(4), 0))

        # Buttons
        bf = tk.Frame(content, bg=Theme.BG)
        bf.pack(pady=self.s(15))
        self.btn(bf, "View Images",
                lambda: webbrowser.open(f"https://www.google.com/search?tbm=isch&q={info['name'].replace(' ', '+')}+dog"),
                'pink').pack(side='left', padx=self.s(4))
        self.btn(bf, "Close", p.destroy, 'secondary').pack(side='left', padx=self.s(4))


class Database:
    def __init__(self):
        self.db = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                              'dog_database.db'), check_same_thread=False)
        self.cur = self.db.cursor()

    def fetch(self, color, ear, tail, size, coat):
        try:
            self.cur.execute("""
                SELECT DogBreeds.BreedName,
                       SUM(CASE WHEN DogColors.ColorName = ? THEN 1 ELSE 0 END +
                           CASE WHEN DogBreeds.CoatType = ? THEN 1 ELSE 0 END +
                           CASE WHEN DogBreeds.EarType = ? THEN 1 ELSE 0 END +
                           CASE WHEN DogBreeds.TailType = ? THEN 1 ELSE 0 END +
                           CASE WHEN DogBreeds.Size = ? THEN 1 ELSE 0 END) AS M,
                       ROUND((SUM(CASE WHEN DogColors.ColorName = ? THEN 1 ELSE 0 END +
                                  CASE WHEN DogBreeds.CoatType = ? THEN 1 ELSE 0 END +
                                  CASE WHEN DogBreeds.EarType = ? THEN 1 ELSE 0 END +
                                  CASE WHEN DogBreeds.TailType = ? THEN 1 ELSE 0 END +
                                  CASE WHEN DogBreeds.Size = ? THEN 1 ELSE 0 END) / 5.0) * 100, 2) AS P
                FROM DogBreeds
                LEFT JOIN BreedColors ON DogBreeds.BreedID = BreedColors.BreedID
                LEFT JOIN DogColors ON BreedColors.ColorID = DogColors.ColorID
                WHERE DogColors.ColorName = ? OR DogColors.ColorName IS NULL
                GROUP BY DogBreeds.BreedName ORDER BY M DESC LIMIT 3
            """, (color, coat, ear, tail, size, color, coat, ear, tail, size, color))
            return self.cur.fetchall()
        except: return []

    def close(self):
        self.cur.close()
        self.db.close()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
