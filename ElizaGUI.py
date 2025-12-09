#!/usr/bin/env python3
"""
Canine Classifier - Premium 2025 UI
Ultra-sleek dark glass morphism design.
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
    BG = "#050508"
    BG2 = "#0a0a12"
    CARD = "#12121c"
    CARD_HOVER = "#1a1a28"
    INPUT = "#0d0d18"
    BORDER = "#252538"

    PRIMARY = "#6366f1"
    PRIMARY_L = "#818cf8"
    PINK = "#ec4899"
    CYAN = "#22d3ee"
    GREEN = "#10b981"
    ORANGE = "#f97316"
    RED = "#ef4444"

    WHITE = "#ffffff"
    TEXT = "#e2e8f0"
    TEXT2 = "#94a3b8"
    MUTED = "#64748b"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Canine Classifier")

        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        self.w = min(int(sw * 0.85), 1350)
        self.h = min(int(sh * 0.85), 820)
        self.scale = min(self.w / 1350, self.h / 820)

        x, y = (sw - self.w) // 2, (sh - self.h) // 2
        root.geometry(f"{self.w}x{self.h}+{x}+{y}")
        root.configure(bg=Theme.BG)
        root.minsize(950, 600)

        b = max(int(11 * self.scale), 9)
        self.F = {
            'hero': ('Segoe UI', int(b*2.4), 'bold'),
            'h1': ('Segoe UI', int(b*1.7), 'bold'),
            'h2': ('Segoe UI', int(b*1.3), 'bold'),
            'body': ('Segoe UI', b),
            'sm': ('Segoe UI', int(b*0.9)),
            'xs': ('Segoe UI', int(b*0.8)),
        }

        self.frame = None
        self.classifier = None
        self.tree = self._tree()
        self.node = None
        self.qnum = 0

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', fieldbackground=Theme.INPUT, background=Theme.INPUT,
                       foreground=Theme.TEXT, borderwidth=0)

        self.home()

    def s(self, v): return max(int(v * self.scale), 1)

    def clear(self):
        if self.frame: self.frame.destroy()

    def card(self, p, **kw):
        return tk.Frame(p, bg=Theme.CARD, highlightbackground=Theme.BORDER, highlightthickness=1, **kw)

    def btn(self, p, txt, cmd, bg=None, **kw):
        bg = bg or Theme.PRIMARY
        f = tk.Frame(p, bg=bg, cursor='hand2')
        l = tk.Label(f, text=txt, font=self.F['body'], fg=Theme.WHITE, bg=bg, padx=22, pady=10)
        l.pack()
        f.bind('<Button-1>', lambda e: cmd())
        l.bind('<Button-1>', lambda e: cmd())
        return f

    def back(self, p):
        b = tk.Label(p, text="← Back", font=self.F['body'], fg=Theme.PRIMARY_L, bg=Theme.BG2, cursor='hand2')
        b.bind('<Button-1>', lambda e: self.home())
        return b

    # HOME
    def home(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG2)
        self.frame.pack(fill='both', expand=True)

        hdr = tk.Frame(self.frame, bg=Theme.BG2)
        hdr.pack(fill='x', padx=self.s(40), pady=(self.s(45), self.s(25)))
        tk.Label(hdr, text="Canine Classifier", font=self.F['hero'], fg=Theme.PRIMARY_L, bg=Theme.BG2).pack()
        tk.Label(hdr, text="AI-Powered Dog Breed Identification", font=self.F['body'], fg=Theme.TEXT2, bg=Theme.BG2).pack(pady=(5,0))

        g = tk.Frame(self.frame, bg=Theme.BG2)
        g.pack(fill='both', expand=True, padx=self.s(40), pady=self.s(10))
        g.grid_columnconfigure(0, weight=1, uniform='c')
        g.grid_columnconfigure(1, weight=1, uniform='c')
        g.grid_rowconfigure(0, weight=1, uniform='r')
        g.grid_rowconfigure(1, weight=1, uniform='r')

        items = [
            ("01", "AI Recognition", "Upload a photo for instant detection", Theme.PRIMARY, self.ai_page),
            ("02", "Questionnaire", "Answer questions about features", Theme.PINK, self.quest_page),
            ("03", "Dichotomous Key", "Scientific Yes/No method", Theme.CYAN, self.dkey_page),
            ("04", "Breed Database", "Explore 51+ breed details", Theme.ORANGE, self.db_page),
        ]

        for i, (n, t, d, c, cmd) in enumerate(items):
            r, col = divmod(i, 2)
            self._card(g, n, t, d, c, cmd, r, col)

        tk.Label(self.frame, text="v2.0 • 51 Breeds • AI Powered", font=self.F['xs'], fg=Theme.MUTED, bg=Theme.BG2).pack(side='bottom', pady=self.s(12))

    def _card(self, p, num, title, desc, color, cmd, row, col):
        c = self.card(p)
        c.grid(row=row, column=col, padx=self.s(8), pady=self.s(8), sticky='nsew')
        c.config(cursor='hand2')

        inner = tk.Frame(c, bg=Theme.CARD)
        inner.pack(fill='both', expand=True, padx=self.s(22), pady=self.s(22))

        n = tk.Label(inner, text=num, font=('Segoe UI', self.s(34), 'bold'), fg=color, bg=Theme.CARD)
        n.pack(anchor='w')
        t = tk.Label(inner, text=title, font=self.F['h2'], fg=Theme.WHITE, bg=Theme.CARD)
        t.pack(anchor='w', pady=(self.s(10), self.s(3)))
        d = tk.Label(inner, text=desc, font=self.F['sm'], fg=Theme.TEXT2, bg=Theme.CARD)
        d.pack(anchor='w')
        a = tk.Label(inner, text="→", font=('Segoe UI', self.s(18)), fg=color, bg=Theme.CARD)
        a.pack(anchor='e', side='bottom')

        ws = [c, inner, n, t, d, a]
        def enter(e):
            for w in ws: w.config(bg=Theme.CARD_HOVER)
            c.config(highlightbackground=color)
        def leave(e):
            for w in ws: w.config(bg=Theme.CARD)
            c.config(highlightbackground=Theme.BORDER)
        for w in ws:
            w.bind('<Enter>', enter)
            w.bind('<Leave>', leave)
            w.bind('<Button-1>', lambda e, cmd=cmd: cmd())

    # AI PAGE
    def ai_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG2)
        self.frame.pack(fill='both', expand=True)

        nav = tk.Frame(self.frame, bg=Theme.BG2)
        nav.pack(fill='x', padx=self.s(30), pady=(self.s(18), self.s(8)))
        self.back(nav).pack(side='left')

        tf = tk.Frame(self.frame, bg=Theme.BG2)
        tf.pack(fill='x', padx=self.s(30))
        tk.Label(tf, text="AI Recognition", font=self.F['h1'], fg=Theme.WHITE, bg=Theme.BG2).pack(anchor='w')
        tk.Label(tf, text="Upload a photo to identify your dog's breed", font=self.F['sm'], fg=Theme.TEXT2, bg=Theme.BG2).pack(anchor='w')

        content = tk.Frame(self.frame, bg=Theme.BG2)
        content.pack(fill='both', expand=True, padx=self.s(30), pady=self.s(12))

        # Left panel
        left = tk.Frame(content, bg=Theme.BG2)
        left.pack(side='left', fill='both', expand=True, padx=(0, self.s(10)))

        lc = self.card(left)
        lc.pack(fill='both', expand=True)
        li = tk.Frame(lc, bg=Theme.CARD)
        li.pack(fill='both', expand=True, padx=self.s(18), pady=self.s(18))

        tk.Label(li, text="Upload Image", font=self.F['h2'], fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w')

        # Preview
        pf = tk.Frame(li, bg=Theme.INPUT, highlightbackground=Theme.BORDER, highlightthickness=1)
        pf.pack(fill='both', expand=True, pady=(self.s(12), self.s(8)))

        self.prev_frame = tk.Frame(pf, bg=Theme.INPUT)
        self.prev_frame.pack(fill='both', expand=True, padx=3, pady=3)

        self.placeholder = tk.Frame(self.prev_frame, bg=Theme.INPUT)
        self.placeholder.place(relx=0.5, rely=0.5, anchor='center')
        tk.Label(self.placeholder, text="+", font=('Segoe UI', self.s(38)), fg=Theme.BORDER, bg=Theme.INPUT).pack()
        self.prev_txt = tk.Label(self.placeholder, text="Click Browse to select image", font=self.F['sm'], fg=Theme.MUTED, bg=Theme.INPUT)
        self.prev_txt.pack()

        self.prev_photo = None
        self.prev_lbl = None

        self.file_var = tk.StringVar(value="No file selected")
        tk.Label(li, textvariable=self.file_var, font=self.F['xs'], fg=Theme.MUTED, bg=Theme.CARD).pack(pady=(0, self.s(8)))

        bf = tk.Frame(li, bg=Theme.CARD)
        bf.pack(fill='x')
        self.btn(bf, "Browse Files", self.browse, bg=Theme.CARD_HOVER).pack(side='left', padx=(0, self.s(6)))
        self.btn(bf, "Analyze Image", self.analyze, bg=Theme.PRIMARY).pack(side='left')

        self.status = tk.StringVar()
        tk.Label(li, textvariable=self.status, font=self.F['sm'], fg=Theme.CYAN, bg=Theme.CARD).pack(pady=(self.s(8), 0))

        # Right panel
        right = tk.Frame(content, bg=Theme.BG2)
        right.pack(side='left', fill='both', expand=True, padx=(self.s(10), 0))

        rc = self.card(right)
        rc.pack(fill='both', expand=True)
        ri = tk.Frame(rc, bg=Theme.CARD)
        ri.pack(fill='both', expand=True, padx=self.s(18), pady=self.s(18))

        tk.Label(ri, text="Results", font=self.F['h2'], fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w')
        tk.Label(ri, text="AI predictions with database verification", font=self.F['xs'], fg=Theme.MUTED, bg=Theme.CARD).pack(anchor='w', pady=(0, self.s(8)))

        rf = tk.Frame(ri, bg=Theme.CARD)
        rf.pack(fill='both', expand=True)

        self.res_canvas = tk.Canvas(rf, bg=Theme.CARD, highlightthickness=0)
        sb = ttk.Scrollbar(rf, orient='vertical', command=self.res_canvas.yview)
        self.res_frame = tk.Frame(self.res_canvas, bg=Theme.CARD)

        self.res_canvas.create_window((0, 0), window=self.res_frame, anchor='nw')
        self.res_canvas.configure(yscrollcommand=sb.set)
        self.res_canvas.pack(side='left', fill='both', expand=True)
        sb.pack(side='right', fill='y')
        self.res_frame.bind('<Configure>', lambda e: self.res_canvas.configure(scrollregion=self.res_canvas.bbox('all')))

        tk.Label(self.res_frame, text="Select an image and click Analyze\nto identify the dog breed", font=self.F['body'], fg=Theme.MUTED, bg=Theme.CARD, justify='center').pack(pady=self.s(50))

        self.sel_img = None

    def browse(self):
        p = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.gif *.bmp *.webp")])
        if p:
            self.sel_img = p
            n = os.path.basename(p)
            self.file_var.set(n[:32] + "..." if len(n) > 35 else n)
            self._preview(p)

    def _preview(self, p):
        if not PIL_AVAILABLE: return
        try:
            img = Image.open(p)
            if img.mode != 'RGB': img = img.convert('RGB')
            self.prev_frame.update()
            mw, mh = max(self.prev_frame.winfo_width()-10, 150), max(self.prev_frame.winfo_height()-10, 100)
            r = min(mw/img.width, mh/img.height)
            img = img.resize((int(img.width*r), int(img.height*r)), Image.Resampling.LANCZOS)
            self.prev_photo = ImageTk.PhotoImage(img)
            self.placeholder.place_forget()
            if not self.prev_lbl:
                self.prev_lbl = tk.Label(self.prev_frame, bg=Theme.INPUT)
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
            self.root.after(0, lambda: self.status.set(f"Error: {str(e)[:35]}"))

    def _results(self, res):
        self.status.set("")
        for w in self.res_frame.winfo_children(): w.destroy()
        if not res:
            self.status.set("Could not classify")
            return

        colors = [Theme.PRIMARY, Theme.PINK, Theme.CYAN, Theme.ORANGE, Theme.GREEN]
        for i, r in enumerate(res[:5]):
            breed, conf, verified = r.get('breed','?'), r.get('confidence',0), r.get('verified',False)
            db_name = r.get('db_name', breed)

            row = tk.Frame(self.res_frame, bg=Theme.INPUT, cursor='hand2')
            row.pack(fill='x', pady=self.s(3))
            inner = tk.Frame(row, bg=Theme.INPUT)
            inner.pack(fill='x', padx=self.s(12), pady=self.s(10))

            lf = tk.Frame(inner, bg=Theme.INPUT)
            lf.pack(side='left', fill='x', expand=True)

            tk.Label(lf, text=f"#{i+1}", font=self.F['h2'], fg=colors[i], bg=Theme.INPUT).pack(side='left', padx=(0, self.s(10)))

            nf = tk.Frame(lf, bg=Theme.INPUT)
            nf.pack(side='left')
            name = db_name if verified else breed
            tk.Label(nf, text=name, font=self.F['body'], fg=Theme.WHITE, bg=Theme.INPUT).pack(anchor='w')
            st = "Verified in database" if verified else "AI prediction"
            sc = Theme.GREEN if verified else Theme.MUTED
            tk.Label(nf, text=st, font=self.F['xs'], fg=sc, bg=Theme.INPUT).pack(anchor='w')

            rf = tk.Frame(inner, bg=Theme.INPUT)
            rf.pack(side='right')

            bw = self.s(90)
            bb = tk.Frame(rf, bg=Theme.BG, width=bw, height=self.s(7))
            bb.pack(side='left', padx=(0, self.s(8)))
            bb.pack_propagate(False)
            fw = max(1, int(bw * conf / 100))
            tk.Frame(bb, bg=colors[i], width=fw).place(x=0, y=0, relheight=1)

            tk.Label(rf, text=f"{conf:.1f}%", font=self.F['body'], fg=colors[i], bg=Theme.INPUT, width=6).pack(side='left')

            row.bind('<Button-1>', lambda e, n=name: self.popup(n))
            inner.bind('<Button-1>', lambda e, n=name: self.popup(n))

        tk.Label(self.res_frame, text="Click result to view breed details", font=self.F['xs'], fg=Theme.MUTED, bg=Theme.CARD).pack(pady=(self.s(12), 0))

    # QUESTIONNAIRE
    def quest_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG2)
        self.frame.pack(fill='both', expand=True)

        nav = tk.Frame(self.frame, bg=Theme.BG2)
        nav.pack(fill='x', padx=self.s(30), pady=(self.s(18), self.s(8)))
        self.back(nav).pack(side='left')

        tf = tk.Frame(self.frame, bg=Theme.BG2)
        tf.pack(fill='x', padx=self.s(30))
        tk.Label(tf, text="Questionnaire", font=self.F['h1'], fg=Theme.WHITE, bg=Theme.BG2).pack(anchor='w')
        tk.Label(tf, text="Select your dog's physical characteristics", font=self.F['sm'], fg=Theme.TEXT2, bg=Theme.BG2).pack(anchor='w')

        content = tk.Frame(self.frame, bg=Theme.BG2)
        content.pack(fill='both', expand=True, padx=self.s(30), pady=self.s(12))

        fc = self.card(content)
        fc.pack(fill='x')
        fi = tk.Frame(fc, bg=Theme.CARD)
        fi.pack(fill='x', padx=self.s(22), pady=self.s(22))

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
                row = tk.Frame(fi, bg=Theme.CARD)
                row.pack(fill='x', pady=self.s(6))
            qf = tk.Frame(row, bg=Theme.CARD)
            qf.pack(side='left', fill='x', expand=True, padx=self.s(5))
            tk.Label(qf, text=l, font=self.F['sm'], fg=Theme.TEXT2, bg=Theme.CARD).pack(anchor='w')
            v = tk.StringVar(value=opts[0])
            self.qvars[k] = v
            ttk.Combobox(qf, textvariable=v, values=opts, state='readonly', font=self.F['sm'], width=self.s(20)).pack(anchor='w', pady=(2, 0))

        bf = tk.Frame(content, bg=Theme.BG2)
        bf.pack(pady=self.s(12))
        self.btn(bf, "  Find Matches  ", self.run_quest, bg=Theme.PINK).pack()

        self.qres = tk.Frame(content, bg=Theme.BG2)
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
            ri.pack(fill='x', padx=self.s(18), pady=self.s(18))
            tk.Label(ri, text="Matches", font=self.F['h2'], fg=Theme.WHITE, bg=Theme.CARD).pack(anchor='w', pady=(0, self.s(8)))

            cols = [Theme.GREEN, Theme.CYAN, Theme.ORANGE]
            for i, (breed, _, prob) in enumerate(res):
                row = tk.Frame(ri, bg=Theme.INPUT, cursor='hand2')
                row.pack(fill='x', pady=self.s(3))
                inner = tk.Frame(row, bg=Theme.INPUT)
                inner.pack(fill='x', padx=self.s(12), pady=self.s(10))
                tk.Label(inner, text=f"#{i+1}", font=self.F['h2'], fg=cols[i] if i<3 else Theme.MUTED, bg=Theme.INPUT).pack(side='left', padx=(0, self.s(10)))
                tk.Label(inner, text=breed, font=self.F['body'], fg=Theme.WHITE, bg=Theme.INPUT).pack(side='left')
                tk.Label(inner, text=f"{prob:.0f}%", font=self.F['body'], fg=Theme.TEXT2, bg=Theme.INPUT).pack(side='right')
                row.bind('<Button-1>', lambda e, b=breed: self.popup(b))
        else:
            tk.Label(self.qres, text="No matches found", font=self.F['body'], fg=Theme.MUTED, bg=Theme.BG2).pack(pady=self.s(25))

    # DICHOTOMOUS KEY
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
        self.frame = tk.Frame(self.root, bg=Theme.BG2)
        self.frame.pack(fill='both', expand=True)

        nav = tk.Frame(self.frame, bg=Theme.BG2)
        nav.pack(fill='x', padx=self.s(30), pady=(self.s(18), self.s(8)))
        self.back(nav).pack(side='left')

        tf = tk.Frame(self.frame, bg=Theme.BG2)
        tf.pack(fill='x', padx=self.s(30))
        tk.Label(tf, text="Dichotomous Key", font=self.F['h1'], fg=Theme.WHITE, bg=Theme.BG2).pack(anchor='w')
        tk.Label(tf, text="Answer Yes/No questions to identify your dog", font=self.F['sm'], fg=Theme.TEXT2, bg=Theme.BG2).pack(anchor='w')

        self.dkey_content = tk.Frame(self.frame, bg=Theme.BG2)
        self.dkey_content.pack(fill='both', expand=True, padx=self.s(30), pady=self.s(12))

        self.node = self.tree
        self.qnum = 0
        self._dkey_q()

    def _dkey_q(self):
        for w in self.dkey_content.winfo_children(): w.destroy()

        if "r" in self.node:
            self._dkey_res(self.node["r"])
            return

        self.qnum += 1
        tk.Label(self.dkey_content, text=f"Question {self.qnum}", font=self.F['sm'], fg=Theme.CYAN, bg=Theme.BG2).pack(anchor='w', pady=(0, self.s(12)))

        qc = self.card(self.dkey_content)
        qc.pack(fill='x')
        qi = tk.Frame(qc, bg=Theme.CARD)
        qi.pack(fill='x', padx=self.s(28), pady=self.s(32))
        tk.Label(qi, text=self.node["q"], font=self.F['h1'], fg=Theme.WHITE, bg=Theme.CARD, wraplength=self.s(480)).pack()

        bf = tk.Frame(self.dkey_content, bg=Theme.BG2)
        bf.pack(pady=self.s(20))
        self.btn(bf, "  Yes  ", lambda: self._dkey_ans(True), bg=Theme.GREEN).pack(side='left', padx=self.s(6))
        self.btn(bf, "  No  ", lambda: self._dkey_ans(False), bg=Theme.RED).pack(side='left', padx=self.s(6))

        rst = tk.Label(self.dkey_content, text="Start over", font=self.F['sm'], fg=Theme.MUTED, bg=Theme.BG2, cursor='hand2')
        rst.pack(pady=self.s(8))
        rst.bind('<Button-1>', lambda e: self._dkey_rst())

    def _dkey_ans(self, yes):
        self.node = self.node["y" if yes else "n"]
        self._dkey_q()

    def _dkey_res(self, breed):
        rc = self.card(self.dkey_content)
        rc.pack(fill='x')
        ri = tk.Frame(rc, bg=Theme.CARD)
        ri.pack(padx=self.s(35), pady=self.s(35))

        tk.Label(ri, text="✓", font=('Segoe UI', self.s(45)), fg=Theme.GREEN, bg=Theme.CARD).pack()
        tk.Label(ri, text="Identification Complete", font=self.F['body'], fg=Theme.TEXT2, bg=Theme.CARD).pack(pady=(self.s(4), 0))
        tk.Label(ri, text=breed, font=self.F['hero'], fg=Theme.PRIMARY_L, bg=Theme.CARD).pack(pady=self.s(12))
        tk.Label(ri, text=f"Identified in {self.qnum} questions", font=self.F['xs'], fg=Theme.MUTED, bg=Theme.CARD).pack()

        bf = tk.Frame(self.dkey_content, bg=Theme.BG2)
        bf.pack(pady=self.s(18))
        self.btn(bf, "View Breed Info", lambda: self.popup(breed), bg=Theme.PRIMARY).pack(side='left', padx=self.s(4))
        self.btn(bf, "Try Again", self._dkey_rst, bg=Theme.CARD_HOVER).pack(side='left', padx=self.s(4))

    def _dkey_rst(self):
        self.node = self.tree
        self.qnum = 0
        self._dkey_q()

    # DATABASE
    def db_page(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=Theme.BG2)
        self.frame.pack(fill='both', expand=True)

        nav = tk.Frame(self.frame, bg=Theme.BG2)
        nav.pack(fill='x', padx=self.s(30), pady=(self.s(18), self.s(8)))
        self.back(nav).pack(side='left')

        tf = tk.Frame(self.frame, bg=Theme.BG2)
        tf.pack(fill='x', padx=self.s(30))
        tk.Label(tf, text="Breed Database", font=self.F['h1'], fg=Theme.WHITE, bg=Theme.BG2).pack(anchor='w')
        tk.Label(tf, text=f"Explore {len(BREED_INFO)} breeds", font=self.F['sm'], fg=Theme.TEXT2, bg=Theme.BG2).pack(anchor='w')

        sf = tk.Frame(self.frame, bg=Theme.BG2)
        sf.pack(fill='x', padx=self.s(30), pady=(self.s(8), self.s(5)))
        breeds = sorted([i['name'] for i in BREED_INFO.values()]) if BREED_INFO else []
        self.search_var = tk.StringVar()
        ttk.Combobox(sf, textvariable=self.search_var, values=breeds, font=self.F['body'], width=self.s(32)).pack(side='left')
        self.btn(sf, "Search", lambda: self._db_detail(self.search_var.get()), bg=Theme.PRIMARY).pack(side='left', padx=(self.s(8), 0))

        content = tk.Frame(self.frame, bg=Theme.BG2)
        content.pack(fill='both', expand=True, padx=self.s(30), pady=self.s(8))

        canvas = tk.Canvas(content, bg=Theme.BG2, highlightthickness=0)
        sb = ttk.Scrollbar(content, orient='vertical', command=canvas.yview)
        self.db_frame = tk.Frame(canvas, bg=Theme.BG2)
        canvas.create_window((0, 0), window=self.db_frame, anchor='nw')
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side='left', fill='both', expand=True)
        sb.pack(side='right', fill='y')
        self.db_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        self._db_grid()

    def _db_grid(self):
        for w in self.db_frame.winfo_children(): w.destroy()
        if not BREED_INFO: return

        row = None
        for i, (k, info) in enumerate(sorted(BREED_INFO.items())):
            if i % 4 == 0:
                row = tk.Frame(self.db_frame, bg=Theme.BG2)
                row.pack(fill='x', pady=self.s(3))
            b = tk.Frame(row, bg=Theme.CARD, cursor='hand2', highlightbackground=Theme.BORDER, highlightthickness=1)
            b.pack(side='left', padx=self.s(3), fill='x', expand=True)
            l = tk.Label(b, text=info['name'], font=self.F['xs'], fg=Theme.TEXT, bg=Theme.CARD, padx=self.s(6), pady=self.s(8))
            l.pack()
            b.bind('<Button-1>', lambda e, n=info['name']: self._db_detail(n))
            l.bind('<Button-1>', lambda e, n=info['name']: self._db_detail(n))

    def _db_detail(self, name):
        info = get_breed_info(name)
        for w in self.db_frame.winfo_children(): w.destroy()

        if not info:
            tk.Label(self.db_frame, text=f"No info for '{name}'", font=self.F['body'], fg=Theme.MUTED, bg=Theme.BG2).pack(pady=self.s(18))
            bk = tk.Label(self.db_frame, text="← Back", font=self.F['body'], fg=Theme.PRIMARY_L, bg=Theme.BG2, cursor='hand2')
            bk.pack()
            bk.bind('<Button-1>', lambda e: self._db_grid())
            return

        bk = tk.Label(self.db_frame, text="← Back to list", font=self.F['sm'], fg=Theme.PRIMARY_L, bg=Theme.BG2, cursor='hand2')
        bk.pack(anchor='w', pady=(0, self.s(8)))
        bk.bind('<Button-1>', lambda e: self._db_grid())

        c = self.card(self.db_frame)
        c.pack(fill='x')
        inner = tk.Frame(c, bg=Theme.CARD)
        inner.pack(fill='x', padx=self.s(22), pady=self.s(22))

        tk.Label(inner, text=info['name'], font=self.F['h1'], fg=Theme.PRIMARY_L, bg=Theme.CARD).pack(anchor='w')
        tk.Label(inner, text=f"{info['group']} • {info['origin']} • {info['lifespan']}", font=self.F['sm'], fg=Theme.TEXT2, bg=Theme.CARD).pack(anchor='w', pady=(2, self.s(12)))

        for lbl, val in [("Size", info['size']['weight']), ("Temperament", ", ".join(info['temperament'][:3])), ("Exercise", info['exercise']), ("Grooming", info['grooming'])]:
            rf = tk.Frame(inner, bg=Theme.CARD)
            rf.pack(fill='x', pady=self.s(2))
            tk.Label(rf, text=lbl, font=self.F['sm'], fg=Theme.MUTED, bg=Theme.CARD, width=12, anchor='w').pack(side='left')
            tk.Label(rf, text=val, font=self.F['sm'], fg=Theme.TEXT, bg=Theme.CARD).pack(side='left')

    # POPUP
    def popup(self, name):
        info = get_breed_info(name)
        if not info:
            messagebox.showinfo("Info", f"No data for {name}")
            return

        p = tk.Toplevel(self.root)
        p.title(info['name'])
        pw, ph = min(self.s(460), self.w-80), min(self.s(500), self.h-80)
        px, py = self.root.winfo_x()+(self.w-pw)//2, self.root.winfo_y()+(self.h-ph)//2
        p.geometry(f"{pw}x{ph}+{px}+{py}")
        p.configure(bg=Theme.BG2)
        p.transient(self.root)
        p.grab_set()

        canvas = tk.Canvas(p, bg=Theme.BG2, highlightthickness=0)
        sb = ttk.Scrollbar(p, orient='vertical', command=canvas.yview)
        content = tk.Frame(canvas, bg=Theme.BG2)
        canvas.create_window((0, 0), window=content, anchor='nw')
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side='left', fill='both', expand=True, padx=self.s(18), pady=self.s(18))
        sb.pack(side='right', fill='y')
        content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        tk.Label(content, text=info['name'], font=self.F['h1'], fg=Theme.PRIMARY_L, bg=Theme.BG2).pack(anchor='w')
        tk.Label(content, text=f"{info['group']} • {info['origin']}", font=self.F['sm'], fg=Theme.TEXT2, bg=Theme.BG2).pack(anchor='w', pady=(2, self.s(12)))

        for lbl, val in [("Size", f"{info['size']['weight']}, {info['size']['height']}"), ("Lifespan", info['lifespan']), ("Temperament", ", ".join(info['temperament'])), ("Exercise", info['exercise']), ("Grooming", info['grooming']), ("Trainability", info['trainability'])]:
            rf = tk.Frame(content, bg=Theme.BG2)
            rf.pack(fill='x', pady=self.s(3))
            tk.Label(rf, text=lbl, font=self.F['sm'], fg=Theme.PRIMARY, bg=Theme.BG2, width=12, anchor='w').pack(side='left')
            tk.Label(rf, text=val, font=self.F['sm'], fg=Theme.TEXT, bg=Theme.BG2, wraplength=self.s(260)).pack(side='left', fill='x')

        fc = tk.Frame(content, bg=Theme.CARD)
        fc.pack(fill='x', pady=self.s(12))
        fi = tk.Frame(fc, bg=Theme.CARD)
        fi.pack(fill='x', padx=self.s(10), pady=self.s(10))
        tk.Label(fi, text="Fun Fact", font=self.F['sm'], fg=Theme.ORANGE, bg=Theme.CARD).pack(anchor='w')
        tk.Label(fi, text=info['fun_fact'], font=self.F['xs'], fg=Theme.TEXT, bg=Theme.CARD, wraplength=self.s(360), justify='left').pack(anchor='w', pady=(3, 0))

        bf = tk.Frame(content, bg=Theme.BG2)
        bf.pack(pady=self.s(12))
        self.btn(bf, "View Images", lambda: webbrowser.open(f"https://www.google.com/search?tbm=isch&q={info['name'].replace(' ', '+')}+dog"), bg=Theme.PINK).pack(side='left', padx=self.s(3))
        self.btn(bf, "Close", p.destroy, bg=Theme.CARD_HOVER).pack(side='left', padx=self.s(3))


class Database:
    def __init__(self):
        self.db = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dog_database.db'), check_same_thread=False)
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
