'''
Plagiarism Detector GUI — Tema scuro + Poppins
Fix v2: stelle Unicode gialle, colonna Forza allineata inline,
        no pallini macOS, header monocromatico
'''
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.representations import MusicRepresentation
from src.core.comparator import PlagiarismComparator


# ──────────────────────────────────────────────
#  PALETTE
# ──────────────────────────────────────────────
BG_DARK    = "#1e1e2e"
BG_SURFACE = "#f0f2f5"
BG_CARD    = "#ffffff"
BG_ROW_ALT = "#f7f8fa"

ACCENT_BLUE   = "#5c7cfa"
ACCENT_RED    = "#e64553"
ACCENT_GREEN  = "#40c057"
ACCENT_PURPLE = "#8839ef"
ACCENT_YELLOW = "#ffd43b"

TEXT_LIGHT = "#cdd6f4"
TEXT_MUTED = "#6c7086"
TEXT_DARK  = "#4c4f69"
TEXT_FOOTER = "#45475a"

BORDER = "#dde1e7"

FONT_FAMILY = "Poppins"


def ff(size: int, weight: str = "normal") -> tuple:
    return (FONT_FAMILY, size, weight)



def _forza_str(similarity: float) -> str:
    if similarity > 80:
        label, n = "MOLTO FORTE", 5
    elif similarity > 60:
        label, n = "FORTE", 4
    elif similarity > 40:
        label, n = "MODERATO", 3
    elif similarity > 20:
        label, n = "DEBOLE", 2
    else:
        label, n = "MOLTO DEBOLE", 1

    stars = "★" * n + "☆" * (5 - n)

    # padding uniforme
    return f"{label:<14} {stars}"


class PlagiarismDetectorGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Plagiarism Detector — Sistema Multi-Rappresentazione")
        self.root.geometry("900x720")
        self.root.minsize(780, 600)
        self.root.configure(bg=BG_SURFACE)

        self.melody1_obj = None
        self.melody2_obj = None
        self.comparison_result = None

        self._build_ui()

    # ──────────────────────────────────────────
    #  BUILD UI
    # ──────────────────────────────────────────
    def _build_ui(self):
        self._build_header()
        self._build_body()
        self._build_footer()

    def _build_header(self):
        """Header monocromatico — nessun pallino macOS."""
        hdr = tk.Frame(self.root, bg=BG_DARK)
        hdr.pack(fill=tk.X)

        title_area = tk.Frame(hdr, bg=BG_DARK, pady=22)
        title_area.pack(fill=tk.X)

        tk.Label(title_area, text="Plagiarism Detector",
                 font=ff(20, "bold"), fg=TEXT_LIGHT, bg=BG_DARK).pack()
        tk.Label(title_area, text="Sistema Multi-Rappresentazione Musicale",
                 font=ff(10), fg=TEXT_MUTED, bg=BG_DARK).pack(pady=(2, 0))

    def _build_body(self):
        canvas = tk.Canvas(self.root, bg=BG_SURFACE, highlightthickness=0)
        scroll = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)

        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.body = tk.Frame(canvas, bg=BG_SURFACE)
        win_id = canvas.create_window((0, 0), window=self.body, anchor="nw")

        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
        self.body.bind("<Configure>",
                       lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        outer = tk.Frame(self.body, bg=BG_SURFACE)
        outer.pack(fill=tk.BOTH, expand=True, padx=20, pady=18)

        self._build_load_section(outer)
        self._build_analyze_btn(outer)
        self._build_metrics(outer)
        self._build_verdict(outer)
        self._build_table(outer)

    def _card(self, parent, title: str) -> tk.Frame:
        wrapper = tk.Frame(parent, bg=BORDER, bd=0)
        wrapper.pack(fill=tk.X, pady=(0, 14))

        inner = tk.Frame(wrapper, bg=BG_CARD)
        inner.pack(fill=tk.X, padx=1, pady=1)

        title_bar = tk.Frame(inner, bg=BG_ROW_ALT, pady=7)
        title_bar.pack(fill=tk.X)
        tk.Frame(title_bar, bg=BORDER, height=1).pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(title_bar, text=title.upper(),
                 font=ff(9, "bold"), fg=TEXT_DARK, bg=BG_ROW_ALT,
                 padx=14).pack(side=tk.LEFT)

        body = tk.Frame(inner, bg=BG_CARD, padx=14, pady=12)
        body.pack(fill=tk.X)
        return body

    def _build_load_section(self, parent):
        body = self._card(parent, "Carica melodie")
        self.lbl1 = self._file_row(body, "Carica melodia 1  (MIDI / MusicXML)", self.load_melody1)
        self.lbl2 = self._file_row(body, "Carica melodia 2  (MIDI / MusicXML)", self.load_melody2)

    def _file_row(self, parent, text, cmd) -> tk.Label:
        row = tk.Frame(parent, bg=BG_CARD)
        row.pack(fill=tk.X, pady=4)

        tk.Button(row, text=text, command=cmd,
                  bg=ACCENT_BLUE, fg="white", activebackground="#4c6ef5",
                  activeforeground="white", relief=tk.FLAT,
                  font=ff(9, "bold"), padx=14, pady=6, cursor="hand2", bd=0
                  ).pack(side=tk.LEFT)

        lbl = tk.Label(row, text="Nessun file caricato",
                       font=ff(9), fg="#9ca3af", bg=BG_CARD)
        lbl.pack(side=tk.LEFT, padx=12)
        return lbl

    def _build_analyze_btn(self, parent):
        frame = tk.Frame(parent, bg=BG_SURFACE)
        frame.pack(fill=tk.X, pady=(0, 14))

        tk.Button(frame, text="▶  Analizza similarità",
                  command=self.analyze,
                  bg=ACCENT_RED, fg="white", activebackground="#c9374a",
                  activeforeground="white", relief=tk.FLAT,
                  font=ff(12, "bold"), pady=11, cursor="hand2", bd=0
                  ).pack(fill=tk.X)

    def _build_metrics(self, parent):
        row = tk.Frame(parent, bg=BG_SURFACE)
        row.pack(fill=tk.X, pady=(0, 14))

        for i, (label, val, color, key) in enumerate([
            ("Similarità complessiva", "--", ACCENT_RED,    "score"),
            ("Confidenza",             "--", ACCENT_GREEN,  "conf"),
            ("Trasposizione rilevata", "--", ACCENT_PURPLE, "transp"),
        ]):
            card = tk.Frame(row, bg=BG_ROW_ALT,
                            highlightbackground=BORDER, highlightthickness=1)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True,
                      padx=(0 if i == 0 else 10, 0))

            tk.Label(card, text=label, font=ff(8, "bold"),
                     fg=TEXT_MUTED, bg=BG_ROW_ALT).pack(anchor="w", padx=14, pady=(10, 2))

            lbl = tk.Label(card, text=val, font=ff(22, "bold"), fg=color, bg=BG_ROW_ALT)
            lbl.pack(anchor="w", padx=14, pady=(0, 10))
            setattr(self, f"lbl_{key}", lbl)

    def _build_verdict(self, parent):
        self.verdict_frame = tk.Frame(parent, bg="#fff8e1",
                                      highlightbackground=ACCENT_YELLOW,
                                      highlightthickness=1)
        self.verdict_frame.pack(fill=tk.X, pady=(0, 14))

        self.verdict_lbl = tk.Label(self.verdict_frame, text="",
                                    font=ff(10, "bold"), fg="#854f0b",
                                    bg="#fff8e1", padx=14, pady=10,
                                    anchor="w", justify=tk.LEFT)
        self.verdict_lbl.pack(fill=tk.X)

    def _build_table(self, parent):
        body = self._card(parent, "Dettagli per rappresentazione")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("PD.Treeview",
                font=(FONT_FAMILY, 9),
                rowheight=34,
                padding=(0, 2),
                background=BG_CARD,
                fieldbackground=BG_CARD,
                foreground=TEXT_DARK,
                borderwidth=0)
        style.configure("PD.Treeview.Heading",
                        font=(FONT_FAMILY, 9, "bold"),
                        background=BG_ROW_ALT,
                        foreground=TEXT_DARK,
                        relief="flat",
                        borderwidth=0)
        style.map("PD.Treeview",
                  background=[("selected", "#e0e7ff")],
                  foreground=[("selected", TEXT_DARK)])
        style.layout("PD.Treeview", [("PD.Treeview.treearea", {"sticky": "nswe"})])

        cols = ("sim", "dist", "transp", "forza")

        tree_frame = tk.Frame(body, bg=BORDER, bd=0)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(tree_frame,
                                 columns=cols,
                                 show="tree headings",
                                 style="PD.Treeview",
                                 yscrollcommand=vsb.set,
                                 height=7)
        vsb.config(command=self.tree.yview)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.column("#0",     width=130, anchor="w",      stretch=False)
        self.tree.column("sim",    width=110, anchor="center", stretch=False)
        self.tree.column("dist",   width=110, anchor="center", stretch=False)
        self.tree.column("transp", width=130, anchor="center", stretch=False)
        self.tree.column("forza", width=260, anchor="center", stretch=True)

        self.tree.heading("#0",     text="Rappresentazione")
        self.tree.heading("sim",    text="Similarità %")
        self.tree.heading("dist",   text="Distanza norm.")
        self.tree.heading("transp", text="Trasposizione")
        self.tree.heading("forza",  text="Forza")

        # Tag righe alternate
        self.tree.tag_configure("odd",  background=BG_CARD)
        self.tree.tag_configure("even", background=BG_ROW_ALT)

       
        

    def _build_footer(self):
        footer = tk.Frame(self.root, bg=BG_DARK, height=34)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)

        tk.Label(footer,
                 text="Capitolo 5 — Sistema Multi-Rappresentazione  ©  2024  |  Python + Tkinter + Poppins",
                 font=ff(8), fg=TEXT_FOOTER, bg=BG_DARK).pack(pady=8)

    # ──────────────────────────────────────────
    #  LOGIC
    # ──────────────────────────────────────────
    def load_melody1(self):
        self._load_file(1)

    def load_melody2(self):
        self._load_file(2)

    def _load_file(self, n: int):
        path = filedialog.askopenfilename(
            title=f"Seleziona melodia {n}",
            filetypes=[
                ("MIDI files",     "*.mid *.midi"),
                ("MusicXML files", "*.xml *.musicxml"),
                ("All files",      "*.*"),
            ]
        )
        if not path:
            return
        try:
            obj = MusicRepresentation(path)
            if n == 1:
                self.melody1_obj = obj
                self.lbl1.config(text=f"✓  {Path(path).name}", fg=ACCENT_GREEN)
            else:
                self.melody2_obj = obj
                self.lbl2.config(text=f"✓  {Path(path).name}", fg=ACCENT_GREEN)
        except Exception as e:
            lbl = self.lbl1 if n == 1 else self.lbl2
            lbl.config(text="Errore nel caricamento", fg=ACCENT_RED)
            messagebox.showerror("Errore", f"Impossibile caricare il file:\n{e}")

    def analyze(self):
        if not self.melody1_obj or not self.melody2_obj:
            messagebox.showwarning("Attenzione", "Carica entrambe le melodie prima di analizzare.")
            return
        try:
            repr1 = self.melody1_obj.get_all_representations()
            repr2 = self.melody2_obj.get_all_representations()
            comparator = PlagiarismComparator(repr1, repr2)
            self.comparison_result = comparator.get_detailed_report()
            self._update_results()
            messagebox.showinfo("Completato", "Analisi completata con successo!")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'analisi:\n{e}")

    def _update_results(self):
        if not self.comparison_result:
            return

        s = self.comparison_result["summary"]

        self.lbl_score.config(text=f"{s['similarity_score']}%")
        self.lbl_conf.config(text=f"{s['confidence']}%")

        transp = s["detected_transposition"]
        self.lbl_transp.config(text=f"{'+' if transp > 0 else ''}{transp} st")

        score = s["similarity_score"]
        if score > 75:
            bg, border, fg = "#ffe3e3", "#f09595", "#c92a2a"
        elif score > 45:
            bg, border, fg = "#fff8e1", ACCENT_YELLOW, "#854f0b"
        else:
            bg, border, fg = "#d3f9d8", "#8ce99a", "#2f9e44"

        self.verdict_frame.config(bg=bg, highlightbackground=border)
        self.verdict_lbl.config(text=f"Verdetto:   {s['verdict']}", fg=fg, bg=bg)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, (repr_type, data) in enumerate(
                self.comparison_result["by_representation"].items()):
            sim = data["similarity"]
            tag = "even" if i % 2 == 0 else "odd"

            self.tree.insert(
                "", "end",
                text=repr_type.upper(),
                values=(
                    f"{sim:.1f}%",
                    f"{data['normalized_distance']:.3f}",
                    f"{'+' if data['best_transposition'] > 0 else ''}{data['best_transposition']} st",
                    _forza_str(sim),
                ),
                tags=(tag,),
            )


# ──────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────
def main():
    root = tk.Tk()
    PlagiarismDetectorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
