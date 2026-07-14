import matplotlib
matplotlib.use('TkAgg')
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import shapiro
import re, os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def linear_theory(x, m, c): return m * x + c
def polynomial_theory(x, a, b, c): return a * (x**2) + b * x + c

class TheoreticalValidatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Empirical & Philosophical Validator")
        self.root.geometry("550x500")
        self.root.configure(bg="#1e1e1e")
        self.percentages, self.current_statement, self.data_x, self.data_y = {}, "", None, None
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        self.tab1 = tk.Frame(self.notebook, bg="#1e1e1e")
        self.notebook.add(self.tab1, text="Empirical Math Data Validator")
        self.setup_mathematical_tab()
        self.tab2 = tk.Frame(self.notebook, bg="#1e1e1e")
        self.notebook.add(self.tab2, text="Philosophical Concept Tester")
        self.setup_philosophical_tab()

    def setup_mathematical_tab(self):
        tk.Label(self.tab1, text="UNIVERSAL EMPIRICAL THEORETICAL VALIDATOR", bg="#1e1e1e", fg="#00ff66", font=("Helvetica", 11, "bold")).pack(pady=15)
        self.upload_btn = tk.Button(self.tab1, text="1. UPLOAD NUMERIC DATASET (.csv)", command=self.load_data, bg="#2d2d2d", fg="white", font=("Helvetica", 10, "bold"), bd=0, padx=10, pady=5)
        self.upload_btn.pack(pady=10)
        self.status_lbl = tk.Label(self.tab1, text="No numeric data loaded.", bg="#1e1e1e", fg="#cccccc", font=("Helvetica", 9, "italic"))
        self.status_lbl.pack(pady=5)
        self.scan_btn = tk.Button(self.tab1, text="2. VALIDATE MATH MODEL MATRIX", command=self.validate_data, bg="#00ff66", fg="#1e1e1e", font=("Helvetica", 11, "bold"), bd=0, padx=15, pady=8, state="disabled")
        self.scan_btn.pack(pady=15)

    def setup_philosophical_tab(self):
        tk.Label(self.tab2, text="QUANTUM PHILOSOPHICAL THEORY EVALUATOR", bg="#1e1e1e", fg="#00bcff", font=("Helvetica", 11, "bold")).pack(pady=15)
        tk.Label(self.tab2, text="Input Philosophical Proposition Core Text Below:", bg="#1e1e1e", fg="#eeeeee", font=("Helvetica", 10)).pack(anchor="w", padx=25, pady=5)
        self.text_box = tk.Text(self.tab2, height=8, width=55, bg="#2d2d2d", fg="white", insertbackground="white", bd=0, highlightthickness=1, highlightbackground="#444444")
        self.text_box.pack(padx=25, pady=5)
        self.text_box.insert(tk.END, "Life possesses no objective value or intrinsic meaning. The universe is cold and indifferent. Therefore, one must cultivate absolute emotional control, enduring hardship with unshakeable stoic calm.")
        self.phil_btn_frame = tk.Frame(self.tab2, bg="#1e1e1e")
        self.phil_btn_frame.pack(pady=15)
        self.phil_btn = tk.Button(self.phil_btn_frame, text="2. TEST PROPOSITION", command=self.validate_philosophy, bg="#00bcff", fg="#1e1e1e", font=("Helvetica", 11, "bold"), bd=0, padx=15, pady=8)
        self.phil_btn.pack(side="left", padx=5)
        self.pdf_btn = tk.Button(self.phil_btn_frame, text="3. EXPORT COMPLETE PDF REPORT", command=self.export_pdf, bg="#eab308", fg="#1e1e1e", font=("Helvetica", 11, "bold"), bd=0, padx=15, pady=8, state="disabled")
        self.pdf_btn.pack(side="left", padx=5)
    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path: return
        try:
            raw_data = np.loadtxt(file_path, delimiter=",")
            self.data_x, self.data_y = raw_data[:, 0], raw_data[:, 1]
            self.status_lbl.configure(text=f"Loaded successfully: {os.path.basename(file_path)}", fg="#00ff66")
            self.scan_btn.configure(state="normal")
        except Exception as e: messagebox.showerror("Error", str(e))

    def validate_data(self):
        if self.data_x is None: return
        report = "--- CORE THEORETICAL ANALYSIS REPORT ---\n\n"
        ss_tot = np.sum((self.data_y - np.mean(self.data_y))**2)
        stat, p_val = shapiro(self.data_y)
        if p_val > 0.05: report += f"1. Gaussian Curve: PASSED (p={p_val:.4f}).\n\n"
        else: report += f"1. Gaussian Curve: REJECTED (p={p_val:.4f}).\n\n"
        def get_r2(tf, *p): return 1 - (np.sum((self.data_y - tf(self.data_x, *p))**2) / ss_tot)
        popt_lin, _ = curve_fit(linear_theory, self.data_x, self.data_y)
        r2_lin = get_r2(linear_theory, *popt_lin)
        popt_poly, _ = curve_fit(polynomial_theory, self.data_x, self.data_y)
        r2_poly = get_r2(polynomial_theory, *popt_poly)
        report += f"2. Linear Fit: R² = {r2_lin:.4f}\n4. Polynomial Fit: R² = {r2_poly:.4f}\n"
        messagebox.showinfo("Analysis Complete", report)
        plt.figure(figsize=(9, 4))
        plt.scatter(self.data_x, self.data_y, color='white', edgecolors='#00ff66', label='Data')
        x_smooth = np.linspace(min(self.data_x), max(self.data_x), 300)
        if r2_lin > 0: plt.plot(x_smooth, linear_theory(x_smooth, *popt_lin), color='#00bcff', label='Linear')
        if r2_poly > 0: plt.plot(x_smooth, polynomial_theory(x_smooth, *popt_poly), color='#ffaa00', label='Polynomial')
        plt.title("Mathematical Theoretical Curve Analysis Matrix Overlay", color='white')
        ax = plt.gca(); ax.set_facecolor('#1e1e1e'); plt.gcf().patch.set_facecolor('#1e1e1e')
        ax.spines['bottom'].color = 'white'; ax.spines['left'].color = 'white'; ax.tick_params(colors='white')
        plt.legend(); plt.grid(True, color='#333333'); plt.show()

    def validate_philosophy(self):
        self.current_statement = self.text_box.get("1.0", tk.END).strip()
        proposition = self.current_statement.lower()
        dictionary = {
            "Empiricism (Sensory)": ["sensory", "observ", "data", "experi"],
            "Rationalism (Logic)": ["logic", "reason", "mind", "thought"],
            "Determinism (Fatalism)": ["predetermine", "caus", "dictat", "fate"],
            "Existentialism (Agency)": ["choice", "freedom", "free will", "exist"],
            "Nihilism (Void Matrix)": ["no objective", "intrinsic meaning", "meaningless", "indifferent", "void"],
            "Stoicism (Resilience)": ["emotional control", "hardship", "calm", "stoic", "endur"]
        }
        scores = {}
        total_hits = 0
        for school, keywords in dictionary.items():
            count = sum(len(re.findall(rf"{word}", proposition)) for word in keywords)
            scores[school] = count
            total_hits += count
        self.percentages = {k: (v / total_hits * 100) if total_hits > 0 else 0.0 for k, v in scores.items()}
        report = "--- CORE METRIC SPECTRUM SCORES ---\n"
        for school, pct in self.percentages.items():
            if pct > 0: report += f"{school}: {pct:.1f}%\n"
        messagebox.showinfo("Philosophical Alignment Matrix", report)
        self.pdf_btn.configure(state="normal")
        fig = plt.figure(figsize=(8, 3.2))
        categories = [k for k, v in self.percentages.items() if v > 0]
        values = [v for k, v in self.percentages.items() if v > 0]
        if not categories: categories, values = ["Unclassified Spectrum"], [100.0]
        soft_colors = ['#8ea4b4', '#a1b5a5', '#bfa7a1', '#d4c5b9', '#acb6b2', '#c9afba'][:len(categories)]
        bars = plt.barh(categories, values, color=soft_colors, edgecolor='none', height=0.45)
        plt.title("EPISTEMOLOGICAL & METAPHYSICAL CONFIGURATION SPECTRUM", color='#cccccc', pad=15, fontname="Helvetica", fontsize=11, fontweight="bold")
        ax = plt.gca(); ax.set_facecolor('#1e1e1e'); fig.patch.set_facecolor('#1e1e1e')
        ax.spines['bottom'].color = '#444444'; ax.spines['left'].color = '#444444'; ax.tick_params(colors='#cccccc'); plt.xlim(0, 100)
        for bar in bars:
            plt.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, f'{bar.get_width():.1f}%', va='center', color='#cccccc', fontname="Helvetica", fontsize=9)
        plt.grid(True, color='#2d2d2d', linestyle=':', axis='x')
        plt.savefig("/tmp/phil_chart.png", dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
        plt.show()
    def export_pdf(self):
        if not self.percentages: return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Document", "*.pdf")])
        if not save_path: return
        try:
            doc = SimpleDocTemplate(save_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
            styles = getSampleStyleSheet()
            
            # PERFECT SINGLE LINE ENFORCEMENT: Dropped the text bounding tables to force a flat, unbroken text line spanning full page columns
            title_style = ParagraphStyle('TStyle', fontName='Helvetica-Bold', fontSize=15, textColor=colors.HexColor('#3a6073'), spaceAfter=18, alignment=1)
            time_style = ParagraphStyle('TimeStyle', fontName='Helvetica-Oblique', fontSize=9, textColor=colors.HexColor('#7f8c8d'), spaceAfter=15, alignment=1)
            header_style = ParagraphStyle('HStyle', fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor('#2c3e50'), spaceBefore=8, spaceAfter=4, leftIndent=90)
            body_style = ParagraphStyle('BStyle', fontName='Helvetica', fontSize=9.5, leading=14, textColor=colors.HexColor('#2c3e50'))
            quote_style = ParagraphStyle('QStyle', fontName='Helvetica-Oblique', fontSize=9.5, leading=14, textColor=colors.HexColor('#5d6d7e'))
            word_count_style = ParagraphStyle('WCStyle', fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#95a5a6'), alignment=2)
            
            story = []
            story.append(Paragraph("PHILOSOPHICAL AXIS METRIC AUDIT REPORT", title_style))
            current_time_str = datetime.now().strftime("Generated on %A, %B %d, %Y")
            story.append(Paragraph(current_time_str, time_style))
            
            story.append(Paragraph("I. ANALYZED STATEMENT MATRIX PROPOSITION:", header_style))
            word_count = len(self.current_statement.split())
            quote_content = [Paragraph(f'\"{self.current_statement}\"', quote_style), Spacer(1, 4), Paragraph(f"Metrics Tracking Summary  |  Total Word Count: {word_count}", word_count_style)]
            quote_table = Table([[quote_content]], colWidths=[360], hAlign='CENTER')
            quote_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8f9fa')), ('PADDING', (0,0), (-1,-1), 12), ('LINELEFT', (0,0), (0,-1), 4, colors.HexColor('#a1b5a5')), ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
            story.append(quote_table)
            story.append(Spacer(1, 6))
            
            story.append(Paragraph("II. CALCULATED QUANTUM AFFINITY WEIGHTS:", header_style))
            table_data = [[Paragraph("<b>Philosophical Framework Axiom</b>", body_style), Paragraph("<b>Affinity Weight Score</b>", body_style)]]
            for school, pct in self.percentages.items():
                if pct > 0: table_data.append([Paragraph(school, body_style), Paragraph(f"{pct:.1f}%", body_style)])
            grid_table = Table(table_data, colWidths=[240, 120], hAlign='CENTER')
            grid_table.setStyle(TableStyle([('BACKGROUND', (0,0), (1,0), colors.HexColor('#f2f4f4')), ('PADDING', (0,0), (-1,-1), 6), ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7e9')), ('ALIGN', (1,0), (1,-1), 'RIGHT')]))
            story.append(grid_table)
            story.append(Spacer(1, 6))
            
            story.append(Paragraph("III. GRAPHICAL METAPHYSICAL CONFIGURATION SPECTRUM:", header_style))
            if os.path.exists("/tmp/phil_chart.png"):
                chart_table = Table([[Image("/tmp/phil_chart.png", width=360, height=144)]], colWidths=[360], hAlign='CENTER')
                chart_table.setStyle(TableStyle([('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0)]))
                story.append(chart_table)
                
            doc.build(story)
            messagebox.showinfo("Success", f"Report saved successfully to:\n{save_path}")
        except Exception as e: messagebox.showerror("PDF Render Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = TheoreticalValidatorApp(root)
    root.mainloop()
