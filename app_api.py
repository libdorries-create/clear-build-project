import matplotlib
matplotlib.use('TkAgg')
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import shapiro
import re, os, sqlite3
from datetime import datetime

# ReportLab Core PDF Engines
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def linear_theory(x, m, c): return m * x + c
def polynomial_theory(x, a, b, c): return a * (x**2) + b * x + c

# --- ENTERPRISE SQLITE DATABASE INITIALISATION ---
def initialise_database():
    conn = sqlite3.connect("matrix_permanent_vault.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evaluation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            proposition TEXT,
            dominant_classification TEXT,
            risk_statement TEXT,
            empiricism TEXT, rationalism TEXT, determinism TEXT, existentialism TEXT,
            nihilism TEXT, stoicism TEXT, utilitarianism TEXT, deontology TEXT,
            absurdism TEXT, virtue_ethics TEXT, risk_assessment TEXT, legal_political TEXT
        )
    """)
    conn.commit()
    conn.close()

initialise_database()

class EnterpriseValidatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Matrix Platform - Threat Assessment Edition")
        self.root.geometry("640x740")
        
        # --- 12-CATEGORY SEMANTIC BACKGROUND DICTIONARY ---
        self.dictionary = {
            "Empiricism (Sensory)": ["empirical data", "sensory observation", "scientific evidence", "measurable observation", "verifiable data"],
            "Rationalism (Logic)": ["pure reason", "logical deduction", "intellect concept", "mental construct", "rational mind"],
            "Determinism (Fatalism)": ["predetermined fate", "causal chain", "inevitable sequence", "dictated by destiny", "pregestated variables"],
            "Existentialism (Agency)": ["choice", "freedom", "free will", "exist", "create purpose", "absolute freedom", "personal choice", "individual agency", "authentic existence"],
            "Nihilism (Void Matrix)": ["no objective value", "intrinsic meaning", "inherently meaningless", "cold indifference", "cosmic void"],
            "Stoicism (Resilience)": ["emotional control", "hardship", "calm", "stoic", "endur", "fortitude", "unshakeable calm", "enduring hardship", "mental fortitude", "stoic resilience"],
            "Utilitarianism (Consequence)": ["utility", "greatest good", "consequence", "maximize happiness", "welfare", "maximize utility", "maximize happiness", "collective welfare", "consequential outcome"],
            "Deontology (Duty Matrix)": ["duty", "obligation", "rule", "categorical imperative", "absolute law", "absolute moral duty", "rule of law", "binding obligation", "unconditional command"],
            "Absurdism (Defiance)": ["absurd", "rebellion", "meaningless conflict", "sisyphus", "embrace the chaos", "absurd nature", "sisypehean defiance", "rebellion against the void"],
            "Virtue Ethics (Character)": ["virtue", "character", "moral excellence", "flourish", "wisdom", "temperance", "human flourishing", "virtuous character", "practical wisdom", "temperance and justice"],
            "Risk Assessment Profile": ["mitigation protocol", "systemic liability", "severity matrix", "vulnerability index", "threat vector", "risk exposure"],
            "Legal-Political Framework": ["sovereign policy", "regulatory non-compliance", "jurisdictional mandate", "geopolitical instability", "legislative oversight"]
        }
        
        self.themes = {
            "Cyberpunk Matrix": {"bg": "#121212", "card": "#1e1e1e", "text": "#ffffff", "accent": "#00ff66", "secondary": "#00bcff"},
            "High-Contrast Slate": {"bg": "#1a202c", "card": "#2d3748", "text": "#f7fafc", "accent": "#edf2f7", "secondary": "#63b3ed"},
            "Amethyst Purple":  {"bg": "#1a1625", "card": "#2d2438", "text": "#f7fafc", "accent": "#d6bcfa", "secondary": "#9f7aea"},
            "Midnight Blue":   {"bg": "#0f172a", "card": "#1e293b", "text": "#f8fafc", "accent": "#38bdf8", "secondary": "#3b82f6"}
        }
        self.current_theme = "Cyberpunk Matrix"
        self.percentages, self.current_statement, self.data_x, self.data_y = {}, "", None, None
        self.generated_risk_statement = "STABLE GATEWAY: No elevated threat signatures detected."

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)
        self.tab1 = tk.Frame(self.notebook)
        self.tab2 = tk.Frame(self.notebook)
        self.tab3 = tk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Empirical Math Studio")
        self.notebook.add(self.tab2, text="Textual Configuration Matrix")
        self.notebook.add(self.tab3, text="Vault Database History")
        
        self.setup_math_studio()
        self.setup_text_matrix()
        self.setup_history_browser()
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
        self.tab3.configure(bg=t["bg"])
        self.theme_frame.configure(bg=t["bg"])
        self.theme_lbl.configure(bg=t["bg"], fg=t["text"], font=("Helvetica", 9, "bold"))
        self.math_title.configure(bg=t["bg"], fg=t["accent"])
        self.status_lbl.configure(bg=t["bg"], fg=t["text"])
        self.text_title.configure(bg=t["bg"], fg=t["secondary"])
        self.prompt_lbl.configure(bg=t["bg"], fg=t["text"])
        self.report_frame.configure(bg=t["bg"], fg=t["accent"], background=t["bg"])
        self.text_box.configure(bg=t["card"], fg=t["text"], highlightbackground=t["card"])
        self.hist_title.configure(bg=t["bg"], fg=t["accent"])
        
        for lbl in self.form_labels: lbl.configure(bg=t["bg"], fg=t["text"])
        for ent in self.entries.values(): ent.configure(bg=t["card"], fg=t["text"], highlightbackground=t["card"])
        self.upload_btn.configure(bg=t["card"], fg=t["text"], font=("Helvetica", 10, "bold"), bd=0)
        self.math_btn.configure(bg=t["accent"], fg=t["bg"], font=("Helvetica", 11, "bold"), bd=0)
        self.eval_btn.configure(bg=t["secondary"], fg=t["bg"], font=("Helvetica", 11, "bold"), bd=0)
        self.report_btn.configure(bg=t["accent"], fg=t["bg"], font=("Helvetica", 10, "bold"), bd=0)
        self.refresh_btn.configure(bg=t["secondary"], fg=t["bg"], font=("Helvetica", 10, "bold"), bd=0)

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
        self.text_box.insert(tk.END, "We must secure verifiable data from our quarterly user feedback loops to analyze our current market position, using a logical deduction to restructure our software delivery model. Remember that our success follows a causal chain where every growth metric is linked, so our team must find an unshakeable calm, cultivate a virtuous character, and push for a positive consequential outcome for our users.")
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
        self.report_btn = tk.Button(self.report_frame, text="📄 COMPILE MASTER DISCOVERY PDF", command=self.compile_local_report, state="disabled")
        self.report_btn.pack(pady=10)

    def setup_history_browser(self):
        self.hist_title = tk.Label(self.tab3, text="VAULT SYSTEM TRANSACTION LEDGER LOGS", font=("Helvetica", 12, "bold"))
        self.hist_title.pack(pady=15)
        self.grid_frame = tk.Frame(self.tab3)
        self.grid_frame.pack(fill="both", expand=True, padx=25, pady=5)
        
        columns = ("id", "timestamp", "classification", "risk")
        self.tree = ttk.Treeview(self.grid_frame, columns=columns, show="headings", height=14)
        self.tree.heading("id", text="ID")
        self.tree.heading("timestamp", text="Timestamp")
        self.tree.heading("classification", text="Dominant Category")
        self.tree.heading("risk", text="Assessed Risk Level")
        
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("timestamp", width=140, anchor="center")
        self.tree.column("classification", width=180, anchor="w")
        self.tree.column("risk", width=180, anchor="center")
        
        self.scrollbar = ttk.Scrollbar(self.grid_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.refresh_btn = tk.Button(self.tab3, text="🔄 REFRESH LEDGER HISTORY DATA", command=self.load_history_from_vault)
        self.refresh_btn.pack(pady=15)
    def load_history_from_vault(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        try:
            conn = sqlite3.connect("matrix_permanent_vault.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, timestamp, dominant_classification, risk_statement FROM evaluation_history ORDER BY id DESC")
            records = cursor.fetchall()
            for record in records: self.tree.insert("", tk.END, values=record)
            conn.close()
        except Exception as e: messagebox.showerror("Vault Read Error", str(e))

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
        scores = {}
        total_hits = 0
        
        for school, phrases in self.dictionary.items():
            count = sum(len(re.findall(rf"{phrase}", proposition)) for phrase in phrases)
            scores[school] = count
            total_hits += count
            
        self.percentages = {k: (v / total_hits * 100) if total_hits > 0 else 0.0 for k, v in scores.items()}
        
        # --- THREAT SEVERITY ASSESSMENT COMPOTATION LOGIC ---
        risk_pct = self.percentages.get("Risk Assessment Profile", 0.0)
        legal_pct = self.percentages.get("Legal-Political Framework", 0.0)
        combined_threat = risk_pct + legal_pct
        
        if combined_threat >= 40.0:
            self.generated_risk_statement = "CRITICAL EXPOSURE: Systemic liability and operational safety protocols breached."
        elif combined_threat >= 15.0:
            self.generated_risk_statement = "HIGH RISK: Regulatory non-compliance vectors identified. Audit recommended."
        else:
            self.generated_risk_statement = "STABLE GATEWAY: Standard framework limits maintained. Low threat profile."
            
        report = f"--- AUTOMATED RISK & SPECTRUM SUMMARY ---\n\n"
        report += f"RISK MATRIX ASSIGNED:\n-> {self.generated_risk_statement}\n\n"
        dominant_framework = "Unclassified Spectrum"
        max_pct = 0.0
        for school, pct in self.percentages.items():
            if pct > 0: 
                report += f" • {school}: {pct:.1f}%\n"
                if pct > max_pct:
                    max_pct = pct
                    dominant_framework = school
                    
        messagebox.showinfo("Matrix Analytics Summary", report)
        self.report_btn.configure(state="normal")
        self.on_theme_changed(None)
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            conn = sqlite3.connect("matrix_permanent_vault.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO evaluation_history (
                    timestamp, proposition, dominant_classification, risk_statement,
                    empiricism, rationalism, determinism, existentialism,
                    nihilism, stoicism, utilitarianism, deontology,
                    absurdism, virtue_ethics, risk_assessment, legal_political
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                timestamp, self.current_statement, dominant_framework, self.generated_risk_statement,
                f"{self.percentages.get('Empiricism (Sensory)', 0.0):.1f}%", f"{self.percentages.get('Rationalism (Logic)', 0.0):.1f}%",
                f"{self.percentages.get('Determinism (Fatalism)', 0.0):.1f}%", f"{self.percentages.get('Existentialism (Agency)', 0.0):.1f}%",
                f"{self.percentages.get('Nihilism (Void Matrix)', 0.0):.1f}%", f"{self.percentages.get('Stoicism (Resilience)', 0.0):.1f}%",
                f"{self.percentages.get('Utilitarianism (Consequence)', 0.0):.1f}%", f"{self.percentages.get('Deontology (Duty Matrix)', 0.0):.1f}%",
                f"{self.percentages.get('Absurdism (Defiance)', 0.0):.1f}%", f"{self.percentages.get('Virtue Ethics (Character)', 0.0):.1f}%",
                f"{self.percentages.get('Risk Assessment Profile', 0.0):.1f}%", f"{self.percentages.get('Legal-Political Framework', 0.0):.1f}%"
            ))
            conn.commit(); conn.close(); self.load_history_from_vault()
        except Exception as e: print(f"Database sync hitch: {str(e)}")
    def compile_local_report(self):
        doc_title = self.entries["Custom Document Title:"].get().strip()
        auditor = self.entries["Target Auditor Initials:"].get().strip()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = f"Matrix_Report_{timestamp}.pdf"
        chart_filename = f"temp_chart_{timestamp}.png"
        t = self.themes[self.current_theme]
        
        categories = [k for k, v in self.percentages.items() if v > 0]
        values = [v for k, v in self.percentages.items() if v > 0]
        if not categories: categories, values = ["Unclassified Spectrum"], [100.0]
        
        fig, ax = plt.subplots(figsize=(6, 2.2))
        bars = ax.barh(categories, values, color=t["secondary"], height=0.45)
        ax.set_xlim(0, 100)
        ax.set_title("EPISTEMOLOGICAL CONFIGURATION MATRIX SCORES", fontsize=9, fontweight="bold", color=t["text"])
        ax.set_facecolor(t["bg"]); fig.patch.set_facecolor(t["bg"])
        ax.spines['bottom'].color = t["text"]; ax.spines['left'].color = t["text"]
        ax.tick_params(colors=t["text"])
        for bar in bars:
            ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f'{bar.get_width():.1f}%', va='center', fontsize=8, fontweight='bold', color=t["text"])
        plt.tight_layout(); plt.savefig(chart_filename, dpi=200); plt.close()
        
        try:
            doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle('TStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor(t["secondary"]), spaceAfter=12)
            body_style = ParagraphStyle('BStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor(t["text"]), leading=14)
            label_style = ParagraphStyle('LStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor(t["bg"]), fontName="Helvetica-Bold")
            
            story = [
                Paragraph(doc_title.upper(), title_style), Spacer(1, 8),
                Paragraph(f"<b>Generation Timestamp:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", body_style),
                Paragraph(f"<b>Compiled By:</b> Auditor ID [{auditor}]", body_style),
                Paragraph(f"<b>Assigned Risk Statement:</b> <font color='red'><b>{self.generated_risk_statement}</b></font>", body_style),
                Spacer(1, 10), Paragraph(f"<b>Evaluated Target Context:</b><br/><i>\"{self.current_statement}\"</i>", body_style), Spacer(1, 15)
            ]
            
            data = [[Paragraph("Philosophical & Operational Classification Profile", label_style), Paragraph("Match", label_style)]]
            for school, pct in self.percentages.items():
                if pct > 0: data.append([Paragraph(school, body_style), Paragraph(f"{pct:.1f}%", body_style)])
                
            # Direct text string expression to bypass character markdown drops completely
            t_box = Table(data, colWidths=eval("[380" + ", 1" + "00]"))
            t_box.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (1, 0), colors.HexColor(t["accent"])), ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6), ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(t["card"])),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor(t["secondary"])), ('PADDING', (0, 1), (-1, -1), 5)
            ]))
            story.append(t_box); story.append(Spacer(1, 15)); story.append(Image(chart_filename, width=400, height=146))
            
            def draw_background(canvas, document):
                canvas.saveState(); canvas.setFillColor(colors.HexColor(t["bg"]))
                # Plain, explicitly unpacked width and height parameters to resolve the abs() conflict permanently
                pg_w, pg_h = document.pagesize
                canvas.rect(0, 0, pg_w, pg_h, fill=True, stroke=False); canvas.restoreState()
                
            doc.build(story, onFirstPage=draw_background)
            if os.path.exists(chart_filename): os.remove(chart_filename)
            messagebox.showinfo("Adaptive PDF Compiled", f"Success! Risk statement attached and PDF compiled successfully.")
        except Exception as e: messagebox.showerror("PDF Compilation Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = EnterpriseValidatorApp(root)
    root.mainloop()
