import matplotlib
matplotlib.use('TkAgg')
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import shapiro
import re, os, csv
from datetime import datetime

def linear_theory(x, m, c): return m * x + c
def polynomial_theory(x, a, b, c): return a * (x**2) + b * x + c

class EnterpriseValidatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Matrix Platform - Master Ledger Edition")
        self.root.geometry("620x720")
        
        # --- UI DESIGN PALETTES MATRIX ---
        self.themes = {
            "Cyberpunk Matrix": {"bg": "#121212", "card": "#1e1e1e", "text": "#ffffff", "accent": "#00ff66", "secondary": "#00bcff"},
            "High-Contrast Slate": {"bg": "#1a202c", "card": "#2d3748", "text": "#f7fafc", "accent": "#edf2f7", "secondary": "#63b3ed"},
            "Amethyst Purple":  {"bg": "#1a1625", "card": "#2d2438", "text": "#f7fafc", "accent": "#d6bcfa", "secondary": "#9f7aea"},
            "Midnight Blue":   {"bg": "#0f172a", "card": "#1e293b", "text": "#f8fafc", "accent": "#38bdf8", "secondary": "#3b82f6"}
        }
        self.current_theme = "Cyberpunk Matrix"
        self.percentages, self.current_statement, self.data_x, self.data_y = {}, "", None, None
        
        # Main Layout Tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)
        self.tab1 = tk.Frame(self.notebook)
        self.tab2 = tk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Empirical Math Studio")
        self.notebook.add(self.tab2, text="Textual Configuration Matrix")
        
        self.setup_math_studio()
        self.setup_text_matrix()
        self.setup_theme_selector()
        self.apply_theme_profile()
    def setup_theme_selector(self):
        self.theme_frame = tk.Frame(self.root)
        self.theme_frame.pack(fill="x", side="bottom", padx=15, pady=5)
        self.theme_lbl = tk.Label(self.theme_frame, text="🎨 DYNAMIC UI DESIGN SELECTOR:")
        self.theme_lbl.pack(side="left", padx=5)
        self.theme_var = tk.StringVar(value=self.current_theme)
        self.theme_dropdown = ttk.Combobox(self.theme_frame, textvariable=self.theme_var, values=list(self.themes.keys()), state="readonly", width=18)
        self.theme_dropdown.pack(side="left", padx=5)
        self.theme_dropdown.bind("<<ComboboxSelected>>", self.on_theme_changed)

    def apply_theme_profile(self):
        t = self.themes[self.current_theme]
        self.root.configure(bg=t["bg"])
        self.tab1.configure(bg=t["bg"])
        self.tab2.configure(bg=t["bg"])
        self.theme_frame.configure(bg=t["bg"])
        self.theme_lbl.configure(bg=t["bg"], fg=t["text"], font=("Helvetica", 9, "bold"))
        self.math_title.configure(bg=t["bg"], fg=t["accent"])
        self.status_lbl.configure(bg=t["bg"], fg=t["text"])
        self.text_title.configure(bg=t["bg"], fg=t["secondary"])
        self.prompt_lbl.configure(bg=t["bg"], fg=t["text"])
        self.report_frame.configure(bg=t["bg"], fg=t["accent"], background=t["bg"])
        self.text_box.configure(bg=t["card"], fg=t["text"], highlightbackground=t["card"])
        
        for lbl in self.form_labels: lbl.configure(bg=t["bg"], fg=t["text"])
        for ent in self.entries.values(): ent.configure(bg=t["card"], fg=t["text"], highlightbackground=t["card"])
        self.upload_btn.configure(bg=t["card"], fg=t["text"], font=("Helvetica", 10, "bold"), bd=0)
        self.math_btn.configure(bg=t["accent"], fg=t["bg"], font=("Helvetica", 11, "bold"), bd=0)
        self.eval_btn.configure(bg=t["secondary"], fg=t["bg"], font=("Helvetica", 11, "bold"), bd=0)
        self.report_btn.configure(bg=t["accent"], fg=t["bg"], font=("Helvetica", 10, "bold"), bd=0)

    def on_theme_changed(self, event):
        self.current_theme = self.theme_var.get()
        self.apply_theme_profile()

    def setup_math_studio(self):
        self.math_title = tk.Label(self.tab1, text="MATHEMATICAL CURVE ANALYSIS MATRIX", font=("Helvetica", 12, "bold"))
        self.math_title.pack(pady=20)
        self.upload_btn = tk.Button(self.tab1, text="📂 BROWSE NUMERIC DATASET (.CSV)", command=self.browse_csv)
        self.upload_btn.pack(pady=15)
        self.status_lbl = tk.Label(self.tab1, text="No dataset currently injected.", font=("Helvetica", 10, "italic"))
        self.status_lbl.pack(pady=5)
        self.math_btn = tk.Button(self.tab1, text="⚡ RUN COMPUTATIONAL CURVE OVERLAY", command=self.compute_math, state="disabled")
        self.math_btn.pack(pady=25)

    def setup_text_matrix(self):
        self.text_title = tk.Label(self.tab2, text="CONTEXTUAL ANALYSIS SPECTRAL CORE", font=("Helvetica", 12, "bold"))
        self.text_title.pack(pady=15)
        self.prompt_lbl = tk.Label(self.tab2, text="Input Proposition Context Target Below:", font=("Helvetica", 10))
        self.prompt_lbl.pack(anchor="w", padx=25, pady=5)
        self.text_box = tk.Text(self.tab2, height=5, width=60, bd=0, highlightthickness=1)
        self.text_box.pack(padx=25, pady=5)
        self.text_box.insert(tk.END, "Life possesses no objective value or intrinsic meaning. The universe is cold and indifferent. Therefore, one must cultivate absolute emotional control, enduring hardship with unshakeable stoic calm.")
        self.eval_btn = tk.Button(self.tab2, text="🔬 EXECUTE CONFIGURATION EVALUATION", command=self.compute_text)
        self.eval_btn.pack(pady=15)
        
        self.report_frame = tk.LabelFrame(self.tab2, text=" Document Report Compiler Gateway ", font=("Helvetica", 9, "bold"))
        self.report_frame.pack(fill="x", padx=25, pady=5)
        
        fields = [("Custom Document Title:", "Matrix Spectral Output Report"), ("Target Auditor Initials:", "LD")]
        self.entries, self.form_labels = {}, []
        for label_text, default_val in fields:
            row = tk.Frame(self.report_frame, bg="#121212")
            row.pack(fill="x", padx=10, pady=3)
            lbl = tk.Label(row, text=label_text, width=20, anchor="w", font=("Helvetica", 9))
            lbl.pack(side="left")
            self.form_labels.append(lbl)
            ent = tk.Entry(row, bd=0, highlightthickness=1, font=("Helvetica", 9))
            ent.pack(side="right", expand=True, fill="x")
            ent.insert(0, default_val)
            self.entries[label_text] = ent
        self.report_btn = tk.Button(self.report_frame, text="📄 COMPILE MASTER DISCOVERY REPORT", command=self.compile_local_report, state="disabled")
        self.report_btn.pack(pady=10)
    def browse_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path: return
        try:
            raw_data = np.loadtxt(file_path, delimiter=",")
            self.data_x, self.data_y = raw_data[:, 0], raw_data[:, 1]
            self.status_lbl.configure(text=f"Injected successfully: {os.path.basename(file_path)}", fg="#00ff66")
            self.math_btn.configure(state="normal")
        except Exception as e: messagebox.showerror("Ingestion Error", str(e))

    def compute_math(self):
        stat, p_val = shapiro(self.data_y)
        ss_tot = np.sum((self.data_y - np.mean(self.data_y))**2)
        popt_lin, _ = curve_fit(linear_theory, self.data_x, self.data_y)
        r2_lin = 1 - (np.sum((self.data_y - linear_theory(self.data_x, *popt_lin))**2) / ss_tot)
        messagebox.showinfo("Matrix Computations Complete", f"Gaussian Metric Profile: {p_val:.4f}\nLinear Matrix Score: R² = {r2_lin:.4f}")
        
        plt.figure(figsize=(8, 4))
        plt.scatter(self.data_x, self.data_y, color='white', edgecolors='#00ff66', label='Injected Points')
        x_smooth = np.linspace(min(self.data_x), max(self.data_x), 300)
        plt.plot(x_smooth, linear_theory(x_smooth, *popt_lin), color='#00bcff', label=f'Linear Overlap (R²={r2_lin:.4f})')
        ax = plt.gca(); t = self.themes[self.current_theme]
        ax.set_facecolor(t["bg"]); plt.gcf().patch.set_facecolor(t["bg"])
        plt.legend(); plt.grid(True, color='#444444'); plt.show()

    def compute_text(self):
        self.current_statement = self.text_box.get("1.0", tk.END).strip()
        proposition = self.current_statement.lower()
        dictionary = {
            "Empiricism (Sensory)": ["sensory", "observ", "data", "experi", "evidence"],
            "Rationalism (Logic)": ["logic", "reason", "mind", "thought", "intellect"],
            "Determinism (Fatalism)": ["predetermine", "caus", "dictat", "fate", "inevitable"],
            "Existentialism (Agency)": ["choice", "freedom", "free will", "exist", "create purpose"],
            "Nihilism (Void Matrix)": ["no objective", "intrinsic meaning", "meaningless", "indifferent", "void", "nothingness"],
            "Stoicism (Resilience)": ["emotional control", "hardship", "calm", "stoic", "endur", "fortitude"],
            "Utilitarianism (Consequence)": ["utility", "greatest good", "consequence", "maximize happiness", "welfare"],
            "Deontology (Duty Matrix)": ["duty", "obligation", "rule", "categorical imperative", "absolute law"],
            "Absurdism (Defiance)": ["absurd", "rebellion", "meaningless conflict", "sisyphus", "embrace the chaos"],
            "Virtue Ethics (Character)": ["virtue", "character", "moral excellence", "flourish", "wisdom", "temperance"]
        }
        scores = {}
        total_hits = 0
        for school, keywords in dictionary.items():
            count = sum(len(re.findall(rf"{word}", proposition)) for word in keywords)
            scores[school] = count
            total_hits += count
        self.percentages = {k: (v / total_hits * 100) if total_hits > 0 else 0.0 for k, v in scores.items()}
        
        report = "--- SPECTRUM SCORES ---\n\n"
        for school, pct in self.percentages.items():
            if pct > 0: report += f" • {school}: {pct:.1f}%\n"
        messagebox.showinfo("Evaluation Metric Summary", report)
        self.report_btn.configure(state="normal")
        self.on_theme_changed(None)
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open("matrix_analysis_history.log", "a") as f:
            f.write(f"\n[{timestamp}]\nContext: \"{self.current_statement}\"\n")
            for school, pct in self.percentages.items():
                if pct > 0: f.write(f" - {school}: {pct:.1f}%\n")
                
        csv_file = "matrix_comprehensive_ledger.csv"
        file_exists = os.path.exists(csv_file)
        with open(csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "Evaluated Proposition"] + list(dictionary.keys()))
            row_data = [timestamp, self.current_statement]
            for school in dictionary.keys():
                row_data.append(f"{self.percentages.get(school, 0.0):.1f}%")
            writer.writerow(row_data)

    def compile_local_report(self):
        doc_title = self.entries["Custom Document Title:"].get().strip()
        auditor = self.entries["Target Auditor Initials:"].get().strip()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"Matrix_Report_{timestamp}.txt"
        try:
            with open(filename, "w") as f:
                f.write("="*60 + "\n" + f"  {doc_title.upper()}\n" + "="*60 + "\n")
                f.write(f"Generated On : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Compiled By  : Auditor [{auditor}]\n" + "-"*60 + "\n\n")
                f.write(f"EVALUATED PROPOSITION TARGET CONTEXT:\n\"{self.current_statement}\"\n\n")
                f.write("COMPUTED METRIC PROFILE ANALYSIS:\n")
                for school, pct in self.percentages.items():
                    if pct > 0: f.write(f"  * {school:<30} : {pct:.1f}%\n")
                f.write("\n" + "="*60 + "\n  STATUS: SYNCHRONIZED TO Master LEDGER\n" + "="*60 + "\n")
            messagebox.showinfo("Report Compiled", f"Success! Master discovery file safely generated:\n\n'{filename}'")
        except Exception as e: messagebox.showerror("Export Fault", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = EnterpriseValidatorApp(root)
    root.mainloop()