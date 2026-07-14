import matplotlib
matplotlib.use('TkAgg')

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import shapiro
import re
import os
import shutil
import sqlite3
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image as ReportLabImage

def linear_theory(x, m, c): return m * x + c
def polynomial_theory(x, a, b, c): return a * (x**2) + b * x + c
def cubic_theory(x, a, b, c, d): return a * (x**3) + b * (x**2) + c * x + d
def exponential_theory(x, a, b): return a * np.exp(b * x)
def logarithmic_theory(x, a, b): return a * np.log(x) + b

class HardenedValidatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secured Multi-Discipline Analytical Validation Engine")
        self.root.geometry("640x550")
        self.root.configure(bg="#1a1a1a")
        
        self.percentages, self.econ_percentages = {}, {}
        self.current_statement, self.current_econ_statement = "", ""
        self.data_x, self.data_y, self.math_report_txt = None, None, ""

        self.execute_secure_backup()
        self.initialize_hardened_ledger()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab1 = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(self.tab1, text="Empirical Math Data Validator")
        self.setup_mathematical_tab()

        self.tab2 = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(self.tab2, text="Philosophical Concept Tester")
        self.setup_philosophical_tab()

        self.tab3 = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(self.tab3, text="Macro-Economic Cycle Tester")
        self.setup_economic_tab()
        
        self.tab4 = tk.Frame(self.notebook, bg="#1a1a1a")
        self.notebook.add(self.tab4, text="UI Matrix Theme Manager")
        self.setup_theme_tab()

    def execute_secure_backup(self):
        try:
            b_dir = os.path.expanduser("~/Desktop/Workspace_Backups")
            os.makedirs(b_dir, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.copy("launch_matrix.py", f"{b_dir}/safe_snap_{ts}.py")
        except: pass

    def initialize_hardened_ledger(self):
        try:
            self.conn = sqlite3.connect("project_archive.db", check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS math_scans (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, summary TEXT)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS philosophy_scans (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, text_blob TEXT, weights TEXT)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS economic_scans (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, text_blob TEXT, weights TEXT)")
            self.conn.commit()
        except: pass

    def setup_mathematical_tab(self):
        tk.Label(self.tab1, text="SECURED MATHEMATICAL MODEL MATRIX SECTOR", bg="#1a1a1a", fg="#00ff66", font=("Helvetica", 11, "bold")).pack(pady=15)
        self.u_btn = tk.Button(self.tab1, text="1. INJECT NUMERIC DATA DATASET (.csv)", command=self.load_data, bg="#2d2d2d", fg="white", font=("Helvetica", 10, "bold"), bd=0, padx=10, pady=5)
        self.u_btn.pack(pady=10)
        self.status_lbl = tk.Label(self.tab1, text="Isolated boundary clear. No data loaded.", bg="#1a1a1a", fg="#888888", font=("Helvetica", 9, "italic"))
        self.status_lbl.pack(pady=5)
        self.m_frame = tk.Frame(self.tab1, bg="#1a1a1a")
        self.m_frame.pack(pady=15)
        self.scan_btn = tk.Button(self.m_frame, text="2. VALIDATE CURVES", command=self.validate_data, bg="#00ff66", fg="#1a1a1a", font=("Helvetica", 11, "bold"), bd=0, padx=15, pady=8, state="disabled")
        self.scan_btn.pack(side="left", padx=5)
        self.math_pdf_btn = tk.Button(self.m_frame, text="3. EXPORT AUDIT PDF", command=self.export_math_pdf, bg="#eab308", fg="#1a1a1a", font=("Helvetica", 11, "bold"), bd=0, padx=15, pady=8, state="disabled")
        self.math_pdf_btn.pack(side="left", padx=5)
        
        tk.Label(self.tab1, text="Select Mathematical Target Model:", bg="#1a1a1a", fg="white", font=("Helvetica", 9)).pack(pady=(10,0))
        self.model_choice = ttk.Combobox(self.tab1, values=["Polynomial (Best Fit)", "Cubic High-Order", "Linear", "Exponential", "Logarithmic"], state="readonly", width=25)
        self.model_choice.set("Polynomial (Best Fit)")
        self.model_choice.pack(pady=5)

    def setup_philosophical_tab(self):
        tk.Label(self.tab2, text="QUANTUM PHILOSOPHICAL THEORY EVALUATOR", bg="#1a1a1a", fg="#00bcff", font=("Helvetica", 11, "bold")).pack(pady=15)
        self.text_box = tk.Text(self.tab2, height=7, width=55, bg="#2d2d2d", fg="white", insertbackground="white", bd=0, highlightthickness=1, highlightbackground="#333333")
        self.text_box.pack(padx=25, pady=5)
        self.text_box.insert(tk.END, "Our logical contemplation and pure reason allow the mind to map out the universe, yet we cannot ignore the raw empirical data provided by sensory observations.")
        self.p_frame = tk.Frame(self.tab2, bg="#1a1a1a")
        self.p_frame.pack(pady=15)
        tk.Button(self.p_frame, text="2. TEST PROPOSITION", command=self.validate_philosophy, bg="#00bcff", fg="#1a1a1a", font=("Helvetica", 11, "bold"), bd=0, padx=15, pady=8).pack(side="left", padx=5)
        self.pdf_btn = tk.Button(self.p_frame, text="3. EXPORT PHILOSOPHY PDF", command=self.export_philosophy_pdf, bg="#eab308", fg="#1a1a1a", font=("Helvetica", 11, "bold"), bd=0, padx=15, pady=8, state="disabled")
        self.pdf_btn.pack(side="left", padx=5)

    def setup_economic_tab(self):
        tk.Label(self.tab3, text="HISTORICAL MACROECONOMIC CYCLE VALIDATOR", bg="#1a1a1a", fg="#ffaa00", font=("Helvetica", 11, "bold")).pack(pady=15)
        self.econ_text_box = tk.Text(self.tab3, height=7, width=55, bg="#2d2d2d", fg="white", insertbackground="white", bd=0, highlightthickness=1, highlightbackground="#333333")
        self.econ_text_box.pack(padx=25, pady=5)
        self.econ_text_box.insert(tk.END, "Central banking systems trigger inflationary expansion through aggressive money printing and monetary stimulus.")
        self.e_frame = tk.Frame(self.tab3, bg="#1a1a1a")
        self.e_frame.pack(pady=15)
        tk.Button(self.e_frame, text="2. RUN MACRO ANALYSIS", command=self.validate_economics, bg="#ffaa00", fg="#1a1a1a", font=("Helvetica", 11, "bold"), bd=0, padx=15, pady=8).pack(side="left", padx=5)
        self.econ_pdf_btn = tk.Button(self.e_frame, text="3. EXPORT ECONOMIC PDF", command=self.export_economic_pdf, bg="#eab308", fg="#1a1a1a", font=("Helvetica", 11, "bold"), bd=0, padx=15, pady=8, state="disabled")
        self.econ_pdf_btn.pack(side="left", padx=5)

    def setup_theme_tab(self):
        tk.Label(self.tab4, text="CHART THEME AND PALETTE SYSTEM CONFIGURATOR", bg="#1a1a1a", fg="#a855f7", font=("Helvetica", 11, "bold")).pack(pady=15)
        tk.Label(self.tab4, text="Select Active Colorway Profile:", bg="#1a1a1a", fg="white", font=("Helvetica", 9)).pack(pady=5)
        self.theme_choice = ttk.Combobox(self.tab4, values=["Matrix Dark (Default)", "Cyberpunk Neon", "Classic Slate"], state="readonly", width=25)
        self.theme_choice.set("Matrix Dark (Default)")
        self.theme_choice.pack(pady=5)
        tk.Button(self.tab4, text="APPLY INTERFACE CONFIG", command=self.apply_theme_profile, bg="#a855f7", fg="white", font=("Helvetica", 10, "bold"), bd=0, padx=15, pady=8).pack(pady=20)
        self.theme_status = tk.Label(self.tab4, text="Current Style Profile: Stable", bg="#1a1a1a", fg="#888888", font=("Helvetica", 9, "italic"))
        self.theme_status.pack()

    def apply_theme_profile(self):
        profile = self.theme_choice.get()
        bg, fg, accent = ("#1a1a1a", "#00ff66", "#00ff66") if profile == "Matrix Dark (Default)" else (("#0f172a", "#f43f5e", "#38bdf8") if profile == "Cyberpunk Neon" else ("#334155", "#cbd5e1", "#f1f5f9"))
        for w in [self.root, self.tab1, self.tab2, self.tab3, self.tab4]: w.configure(bg=bg)
        self.theme_status.configure(text=f"Applied Layout Palette Scheme: {profile}", fg=accent)
        messagebox.showinfo("Matrix Styles Modified", f"Interface re-mapped cleanly to: {profile}")

    def load_data(self):
        fp = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not fp: return
        try:
            self.data_x, self.data_y = np.loadtxt(fp, delimiter=",", skiprows=1, unpack=True)
            self.status_lbl.configure(text=f"Secure Matrix Locked: {os.path.basename(fp)}", fg="#00ff66")
            self.scan_btn.configure(state="normal")
        except:
            try:
                self.data_x, self.data_y = np.loadtxt(fp, delimiter=",", unpack=True)
                self.status_lbl.configure(text=f"Secure Matrix Locked: {os.path.basename(fp)}", fg="#00ff66")
                self.scan_btn.configure(state="normal")
            except:
                messagebox.showerror("Security Rejection", "Data parse check failed.\nMake sure your CSV has exactly two numeric columns.")

    def validate_data(self):
        if self.data_x is None: return
        ss = np.sum((self.data_y - np.mean(self.data_y))**2)
        _, p_v = shapiro(self.data_y)
        g_txt = "PASSED" if p_v > 0.05 else "REJECTED"
        def get_r2(tf, *p): return max(0.0, 1 - (np.sum((self.data_y - tf(self.data_x, *p))**2) / ss))
        
        try: p_lin, _ = curve_fit(linear_theory, self.data_x, self.data_y, maxfev=5000); r2_lin = get_r2(linear_theory, *p_lin)
        except: r2_lin = 0.0
        try: p_poly, _ = curve_fit(polynomial_theory, self.data_x, self.data_y, maxfev=5000); r2_poly = get_r2(polynomial_theory, *p_poly)
        except: r2_poly = 0.0
        try: p_cub, _ = curve_fit(cubic_theory, self.data_x, self.data_y, maxfev=5000); r2_cub = get_r2(cubic_theory, *p_cub)
        except: r2_cub = 0.0
        try: p_exp, _ = curve_fit(exponential_theory, self.data_x, self.data_y, p0=[1, -0.01], maxfev=5000); r2_exp = get_r2(exponential_theory, *p_exp)
        except: r2_exp = 0.0
        try: p_log, _ = curve_fit(logarithmic_theory, self.data_x, self.data_y, maxfev=5000); r2_log = get_r2(logarithmic_theory, *p_log)
        except: r2_log = 0.0
        
        self.math_report_txt = f"Gaussian Curve Evaluation: {g_txt} (p={p_v:.4f})\nLinear Model Precision: R2 = {r2_lin:.4f}\nPolynomial Model Precision: R2 = {r2_poly:.4f}\nCubic High-Order Precision: R2 = {r2_cub:.4f}"
        
        try:
            self.cursor.execute("INSERT INTO math_scans (timestamp, summary) VALUES (?, ?)", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.math_report_txt))
            self.conn.commit()
            self.math_pdf_btn.configure(state="normal")
            
            chosen = self.model_choice.get()
            plt.figure("Model Curve Performance Visualizer", figsize=(6, 4))
            plt.style.use('dark_background')
            plt.scatter(self.data_x, self.data_y, color='#00ff66', edgecolors='white', s=80, label='Raw Data')
            xs = np.linspace(min(self.data_x), max(self.data_x), 300)
            
            if chosen == "Linear": plt.plot(xs, linear_theory(xs, *p_lin), '#eab308', label=f'Linear (R2={r2_lin:.2f})')
            elif chosen == "Cubic High-Order": plt.plot(xs, cubic_theory(xs, *p_cub), '#a855f7', label=f'Cubic (R2={r2_cub:.2f})')
            elif chosen == "Exponential" and r2_exp > 0: plt.plot(xs, exponential_theory(xs, *p_exp), '#f43f5e', label=f'Exp (R2={r2_exp:.2f})')
            elif chosen == "Logarithmic" and r2_log > 0: plt.plot(xs, logarithmic_theory(xs, *p_log), '#38bdf8', label=f'Log (R2={r2_log:.2f})')
            else: plt.plot(xs, polynomial_theory(xs, *p_poly), '#00bcff', label=f'Polynomial (R2={r2_poly:.2f})')
            
            plt.title("Empirical Data Curve Fit Breakdown")
            plt.grid(True, linestyle=':', alpha=0.3)
            plt.legend()
            plt.tight_layout()
            
            messagebox.showinfo("Analysis Complete", self.math_report_txt)
            plt.show()
        except Exception as e:
            messagebox.showerror("Ledger Write Failure", str(e))

    def validate_philosophy(self):
        txt = self.text_box.get("1.0", tk.END)
        self.current_statement = txt
        rationalism = len(re.findall(r'(reason|logic|contemplation|mind|universe|priori|deductive)', txt, re.I))
        empiricism = len(re.findall(r'(empirical|data|sensory|observations|experiment|posteriori|induction)', txt, re.I))
        stoicism = len(re.findall(r'(control|enduring|hardship|calm|stoic|void|destiny|providence)', txt, re.I))
        existentialism = len(re.findall(r'(absurd|angst|meaningless|choice|authentic|freedom|existence)', txt, re.I))
        nihilism = len(re.findall(r'(nothing|rejection|void|meaning|morality|futile|illusion)', txt, re.I))
        idealism = len(re.findall(r'(spirit|mind|consciousness|ideas|perception|immaterial|absolute)', txt, re.I))
        tot = max(1, rationalism + empiricism + stoicism + existentialism + nihilism + idealism)
        self.percentages = {"Rationalism": round((rationalism/tot)*100, 2), "Empiricism": round((empiricism/tot)*100, 2), "Stoicism": round((stoicism/tot)*100, 2), "Existentialism": round((existentialism/tot)*100, 2), "Nihilism": round((nihilism/tot)*100, 2), "Idealism": round((idealism/tot)*100, 2)}
        try:
            self.cursor.execute("INSERT INTO philosophy_scans (timestamp, text_blob, weights) VALUES (?, ?, ?)", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), txt, str(self.percentages)))
            self.conn.commit()
            
            # Sync graph aesthetics directly with active UI dropdown profile choice
            theme = self.theme_choice.get()
            bar_color = '#00ff66' if theme == "Matrix Dark (Default)" else ('#f43f5e' if theme == "Cyberpunk Neon" else '#475569')
            bg_color = '#1a1a1a' if theme == "Matrix Dark (Default)" else ('#0f172a' if theme == "Cyberpunk Neon" else '#f8fafc')
            text_color = 'white' if theme in ["Matrix Dark (Default)", "Cyberpunk Neon"] else 'black'
            
            fig, ax = plt.subplots(figsize=(6, 3.5))
            fig.patch.set_facecolor(bg_color)
            ax.set_facecolor(bg_color)
            
            schools = list(self.percentages.keys())
            weights = list(self.percentages.values())
            
            bars = ax.barh(schools, weights, color=bar_color, edgecolor=text_color, height=0.6)
            ax.set_title("Discipline Composition Spectrum Analysis", color=text_color, fontsize=11, fontweight='bold', pad=10)
            ax.set_xlabel("Percentage Weight (%)", color=text_color, fontsize=9)
            
            # Explicitly lock axis label ticks to prevent font drop out
            ax.set_yticks(range(len(schools)))
            ax.set_yticklabels(schools, color=text_color, fontsize=9)
            ax.set_xticklabels([f"{int(x)}%" for x in ax.get_xticks()], color=text_color, fontsize=8)
            
            ax.spines['bottom'].set_color(text_color)
            ax.spines['left'].set_color(text_color)
            for spine in ['top', 'right']: ax.spines[spine].set_visible(False)
            ax.grid(True, axis='x', linestyle=':', alpha=0.3, color=text_color)
            
            plt.tight_layout()
            plt.savefig("temp_phil_chart.png", dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
            plt.close()
            
            self.pdf_btn.configure(state="normal")
            messagebox.showinfo("Conceptual Analysis Matrix Verified", f"Theory Breakdown Metrics:\n{self.percentages}")
        except Exception as e: print("Phil chart error:", e)

    def validate_economics(self):
        txt = self.econ_text_box.get("1.0", tk.END)
        self.current_econ_statement = txt
        austrian = len(re.findall(r'(malinvestment|artificial|printing|stimulus|credit|inflationary|hayek|mises|calculation)', txt, re.I))
        classical = len(re.findall(r'(productivity|manufacturing|industrial|trade|commodity|smith|ricardo|supply)', txt, re.I))
        keynesian = len(re.findall(r'(multiplier|aggregate|intervention|spending|deficit|fiscal|liquidity|demand)', txt, re.I))
        tot = max(1, austrian + classical + keynesian)
        self.econ_percentages = {"Austrian School": round((austrian/tot)*100, 2), "Classical/Production": round((classical/tot)*100, 2), "Keynesian/Aggregate": round((keynesian/tot)*100, 2)}
        try:
            self.cursor.execute("INSERT INTO economic_scans (timestamp, text_blob, weights) VALUES (?, ?, ?)", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), txt, str(self.econ_percentages)))
            self.conn.commit()
            
            theme = self.theme_choice.get()
            bg_color = '#1a1a1a' if theme == "Matrix Dark (Default)" else ('#0f172a' if theme == "Cyberpunk Neon" else '#f8fafc')
            text_color = 'white' if theme in ["Matrix Dark (Default)", "Cyberpunk Neon"] else 'black'
            colors_list = ['#00ff66', '#00bcff', '#a855f7'] if theme == "Matrix Dark (Default)" else (['#f43f5e', '#38bdf8', '#eab308'] if theme == "Cyberpunk Neon" else ['#475569', '#94a3b8', '#cbd5e1'])
            
            fig, ax = plt.subplots(figsize=(5, 4))
            fig.patch.set_facecolor(bg_color)
            ax.set_facecolor(bg_color)
            
            wedges, texts, autotexts = ax.pie(
                list(self.econ_percentages.values()), 
                labels=list(self.econ_percentages.keys()), 
                autopct='%1.1f%%', 
                colors=colors_list, 
                startangle=140,
                textprops=dict(color=text_color, fontsize=9)
            )
            for autotext in autotexts: autotext.set_color('black' if theme == "Classic Slate" else 'white')
            
            ax.set_title("Macroeconomic Cycle Fit Breakdown", color=text_color, fontsize=11, fontweight='bold', pad=10)
            plt.tight_layout()
            plt.savefig("temp_econ_chart.png", dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
            plt.close()
            
            self.econ_pdf_btn.configure(state="normal")
            messagebox.showinfo("Macro-Economic Mapping Active", f"Model Fit Indices:\n{self.econ_percentages}")
        except Exception as e: print("Econ chart error:", e)

    def export_math_pdf(self):
        fp = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not fp: return
        doc = SimpleDocTemplate(fp, pagesize=letter)
        story = [Paragraph("Empirical Math Data Validation Audit Report", getSampleStyleSheet()['Title']), Spacer(1, 12), Paragraph(self.math_report_txt.replace('\n', '<br/>'), getSampleStyleSheet()['BodyText'])]
        doc.build(story); messagebox.showinfo("Export Successful", "PDF generated.")

    def export_philosophy_pdf(self):
        fp = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not fp: return
        try:
            doc = SimpleDocTemplate(fp, pagesize=letter)
            story = [
                Paragraph("Quantum Philosophical Proposition Ledger", getSampleStyleSheet()['Title']),
                Spacer(1, 15),
                Paragraph(f"<b>Analyzed Structural Matrix Sequence:</b><br/>{self.current_statement}", getSampleStyleSheet()['BodyText']),
                Spacer(1, 20),
                ReportLabImage("temp_phil_chart.png", width=400, height=200),
                Spacer(1, 15)
            ]
            doc.build(story)
            if os.path.exists("temp_phil_chart.png"): os.remove("temp_phil_chart.png")
            messagebox.showinfo("Export Successful", "Philosophy report chart printed to PDF.")
        except Exception as e: messagebox.showerror("PDF Render Failure", str(e))

    def export_economic_pdf(self):
        fp = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not fp: return
        try:
            doc = SimpleDocTemplate(fp, pagesize=letter)
            story = [
                Paragraph("Macroeconomic Cycle Fit Assessment", getSampleStyleSheet()['Title']),
                Spacer(1, 15),
                Paragraph(f"<b>Source Parameters Scanned:</b><br/>{self.current_econ_statement}", getSampleStyleSheet()['BodyText']),
                Spacer(1, 25),
                ReportLabImage("temp_econ_chart.png", width=350, height=280)
            ]
            doc.build(story)
            if os.path.exists("temp_econ_chart.png"): os.remove("temp_econ_chart.png")
            messagebox.showinfo("Export Successful", "Macroeconomic report chart printed to PDF.")
        except Exception as e: messagebox.showerror("PDF Render Failure", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = HardenedValidatorApp(root)
    root.mainloop()
