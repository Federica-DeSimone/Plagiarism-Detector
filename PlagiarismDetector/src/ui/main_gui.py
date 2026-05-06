'''
Created on 18 gen 2026

@author: admin
'''
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import sys
import os
from src.core.representations import MusicRepresentation
from src.core.comparator import PlagiarismComparator

# Aggiungi la directory src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class PlagiarismDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Plagiarism Detector - Sistema Multi-Rappresentazione")
        self.root.geometry("1400x1000")
        self.root.configure(bg="#f0f0f0")
        
        self.melody1_path = None
        self.melody2_path = None
        self.melody1_obj = None
        self.melody2_obj = None
        self.comparison_result = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Costruisce l'interfaccia utente"""
        
        # HEADER
        header = tk.Frame(self.root, bg="#2c3e50", height=80)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="🎵 PLAGIARISM DETECTOR", 
                        font=("Arial", 20, "bold"), fg="white", bg="#2c3e50")
        title.pack(pady=10)
        
        subtitle = tk.Label(header, text="Sistema Multi-Rappresentazione Musicale", 
                           font=("Arial", 11), fg="#ecf0f1", bg="#2c3e50")
        subtitle.pack()
        
        # MAIN CONTAINER
        main_container = tk.Frame(self.root, bg="#f0f0f0")
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # ROW 1: Caricamento file
        load_frame = tk.LabelFrame(main_container, text="📁 Carica Melodie", 
                                   font=("Arial", 12, "bold"), bg="#ffffff", padx=15, pady=15)
        load_frame.pack(fill=tk.X, pady=10)
        
        # Melodia 1
        btn1 = tk.Button(load_frame, text="Carica Melodia 1 (MIDI/MusicXML)", 
                        command=self.load_melody1, bg="#3498db", fg="white", 
                        font=("Arial", 10), padx=15, pady=8, relief=tk.FLAT, cursor="hand2")
        btn1.grid(row=0, column=0, padx=10, pady=5)
        
        self.label1 = tk.Label(load_frame, text="Nessun file caricato", 
                              font=("Arial", 9), fg="#7f8c8d", bg="#ffffff")
        self.label1.grid(row=0, column=1, sticky=tk.W, padx=10)
        
        # Melodia 2
        btn2 = tk.Button(load_frame, text="Carica Melodia 2 (MIDI/MusicXML)", 
                        command=self.load_melody2, bg="#3498db", fg="white", 
                        font=("Arial", 10), padx=15, pady=8, relief=tk.FLAT, cursor="hand2")
        btn2.grid(row=1, column=0, padx=10, pady=5)
        
        self.label2 = tk.Label(load_frame, text="Nessun file caricato", 
                              font=("Arial", 9), fg="#7f8c8d", bg="#ffffff")
        self.label2.grid(row=1, column=1, sticky=tk.W, padx=10)
        
        # ROW 2: Pulsante Analizza
        analyze_btn = tk.Button(main_container, text="▶️ ANALIZZA SIMILARITÀ", 
                               command=self.analyze, bg="#e74c3c", fg="white", 
                               font=("Arial", 12, "bold"), padx=20, pady=10, 
                               relief=tk.FLAT, cursor="hand2")
        analyze_btn.pack(pady=15)
        
        # ROW 3: Risultati (con scrollbar)
        result_frame = tk.LabelFrame(main_container, text="📊 Risultati Analisi", 
                                    font=("Arial", 12, "bold"), bg="#ffffff", padx=15, pady=15)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Crea un frame interno scrollabile
        summary_frame = tk.Frame(result_frame, bg="#ffffff")
        summary_frame.pack(fill=tk.X, pady=10)
        
        # Verdict
        self.verdict_label = tk.Label(summary_frame, text="", 
                                     font=("Arial", 14, "bold"), bg="#ffffff")
        self.verdict_label.pack(pady=10)
        
        # Score
        score_frame = tk.Frame(summary_frame, bg="#ffffff")
        score_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(score_frame, text="Similarità Complessiva:", 
                font=("Arial", 10), bg="#ffffff").pack(side=tk.LEFT, padx=5)
        
        self.score_label = tk.Label(score_frame, text="--", 
                                   font=("Arial", 12, "bold"), fg="#e74c3c", bg="#ffffff")
        self.score_label.pack(side=tk.LEFT, padx=5)
        
        # Confidence
        conf_frame = tk.Frame(summary_frame, bg="#ffffff")
        conf_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(conf_frame, text="Confidenza:", 
                font=("Arial", 10), bg="#ffffff").pack(side=tk.LEFT, padx=5)
        
        self.confidence_label = tk.Label(conf_frame, text="--", 
                                        font=("Arial", 12, "bold"), fg="#27ae60", bg="#ffffff")
        self.confidence_label.pack(side=tk.LEFT, padx=5)
        
        # Transposition
        transp_frame = tk.Frame(summary_frame, bg="#ffffff")
        transp_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(transp_frame, text="Trasposizione Rilevata:", 
                font=("Arial", 10), bg="#ffffff").pack(side=tk.LEFT, padx=5)
        
        self.transposition_label = tk.Label(transp_frame, text="--", 
                                           font=("Arial", 11, "bold"), fg="#9b59b6", bg="#ffffff")
        self.transposition_label.pack(side=tk.LEFT, padx=5)
        
        # Separatore
        ttk.Separator(result_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Tabella risultati per rappresentazione con scrollbar
        tk.Label(result_frame, text="Dettagli per Rappresentazione:", 
                font=("Arial", 11, "bold"), bg="#ffffff").pack(pady=(5, 10), anchor=tk.W)
        
        # Frame per la tabella e scrollbar
        table_frame = tk.Frame(result_frame, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbar verticale
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree = ttk.Treeview(table_frame, height=12, columns=('Similitudine', 'Distanza', 'Trasposizione', 'Forza'), 
                                 show='tree headings', yscrollcommand=scrollbar.set)
        
        # Configura scrollbar
        scrollbar.config(command=self.tree.yview)
        
        # Configura font più grande
        style = ttk.Style()
        style.configure('Treeview', font=('Arial', 11), rowheight=25)
        style.configure('Treeview.Heading', font=('Arial', 12, 'bold'))
        
        self.tree.column('#0', width=180, anchor=tk.W)
        self.tree.column('Similitudine', width=140, anchor=tk.CENTER)
        self.tree.column('Distanza', width=140, anchor=tk.CENTER)
        self.tree.column('Trasposizione', width=160, anchor=tk.CENTER)
        self.tree.column('Forza', width=200, anchor=tk.W)
        
        self.tree.heading('#0', text='Rappresentazione', anchor=tk.W)
        self.tree.heading('Similitudine', text='Similitudine %')
        self.tree.heading('Distanza', text='Distanza Norm.')
        self.tree.heading('Trasposizione', text='Trasposizione')
        self.tree.heading('Forza', text='Forza')
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # ROW 4: Footer con info
        footer = tk.Frame(self.root, bg="#34495e", height=40)
        footer.pack(fill=tk.X, padx=0, pady=0)
        footer.pack_propagate(False)
        
        info_text = tk.Label(footer, 
                            text="Capitolo 5 - Sistema Multi-Rappresentazione © 2024 | Python + Tkinter", 
                            font=("Arial", 9), fg="#bdc3c7", bg="#34495e")
        info_text.pack(pady=8)
    
    def load_melody1(self):
        file_path = filedialog.askopenfilename(
            title="Seleziona Melodia 1",
            filetypes=[("MIDI files", "*.mid *.midi"), ("MusicXML files", "*.xml *.musicxml"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.melody1_path = file_path
                self.melody1_obj = MusicRepresentation(file_path)
                filename = Path(file_path).name
                self.label1.config(text=f"✓ Caricato: {filename}", fg="#27ae60")
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile caricare il file:\n{str(e)}")
                self.label1.config(text="Errore nel caricamento", fg="#e74c3c")
    
    def load_melody2(self):
        file_path = filedialog.askopenfilename(
            title="Seleziona Melodia 2",
            filetypes=[("MIDI files", "*.mid *.midi"), ("MusicXML files", "*.xml *.musicxml"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.melody2_path = file_path
                self.melody2_obj = MusicRepresentation(file_path)
                filename = Path(file_path).name
                self.label2.config(text=f"✓ Caricato: {filename}", fg="#27ae60")
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile caricare il file:\n{str(e)}")
                self.label2.config(text="Errore nel caricamento", fg="#e74c3c")
    
    def analyze(self):
        if not self.melody1_obj or not self.melody2_obj:
            messagebox.showwarning("Avvertimento", "Carica entrambe le melodie prima di analizzare!")
            return
        
        try:
            # Ottieni le rappresentazioni
            repr1 = self.melody1_obj.get_all_representations()
            repr2 = self.melody2_obj.get_all_representations()

            
            # Crea comparator e analizza
            comparator = PlagiarismComparator(repr1, repr2)
            self.comparison_result = comparator.get_detailed_report()
            
            # Aggiorna UI
            self.update_results()
            messagebox.showinfo("Successo", "Analisi completata!")
        
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'analisi:\n{str(e)}")
    
    def update_results(self):
        if not self.comparison_result:
            return
        
        summary = self.comparison_result['summary']
        
        # Verdict
        self.verdict_label.config(text=summary['verdict'])
        
        # Score
        self.score_label.config(text=f"{summary['similarity_score']}%")
        
        # Confidence
        self.confidence_label.config(text=f"{summary['confidence']}%")
        
        # Transposition
        transp = summary['detected_transposition']
        transp_text = f"{transp} semitoni"
        self.transposition_label.config(text=transp_text)
        
        # Pulisci tabella
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Popola tabella
        for repr_type, data in self.comparison_result['by_representation'].items():
            self.tree.insert('', 'end', text=repr_type.upper(),
                           values=(
                               f"{data['similarity']:.1f}%",
                               f"{data['normalized_distance']:.3f}",
                               f"{data['best_transposition']} st",
                               data['strength']
                           ))


def main():
    root = tk.Tk()
    app = PlagiarismDetectorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
