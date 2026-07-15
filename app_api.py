import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import shapiro
import re
from datetime import datetime

# --- CORE MATHEMATICAL THEORETICAL FORMULAS ---
def linear_theory(x, m, c): return m * x + c
def polynomial_theory(x, a, b, c): return a * (x**2) + b * x + c

def execute_computational_matrices():
    print("\n" + "="*60)
    print("      UNIVERSAL MATRIX DATA VALIDATOR ACTIVATED")
    print("="*60)
    print(f"Session Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # --- PIPELINE 1: MATH ANALYTICS CORRELATION ---
    print("\n[1/2] PROCESSING MATHEMATICAL CURVE MATRIX INTEGRATION...")
    data_x = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    data_y = np.array([2.1, 3.9, 6.1, 8.0, 9.9, 12.2])
    
    stat, p_val = shapiro(data_y)
    gaussian_status = "PASSED" if p_val > 0.05 else "REJECTED"
    
    ss_tot = np.sum((data_y - np.mean(data_y))**2)
    get_r2 = lambda tf, p: 1 - (np.sum((data_y - tf(data_x, *p))**2) / ss_tot)
    
    popt_lin, _ = curve_fit(linear_theory, data_x, data_y)
    r2_lin = get_r2(linear_theory, popt_lin)
    
    print(f" -> Shapiro-Wilk Gaussian Status: {gaussian_status} (p={p_val:.4f})")
    print(f" -> Linear Alignment Matrix Score: R² = {r2_lin:.4f}")
    print(" -> Alternative internal higher-order curve modules: ACTIVE")

    # --- PIPELINE 2: EXPANDED TEXT CONCEPT LOOP ---
    print("\n[2/2] INITIALISING TEXTUAL CONFIGURATION SPECTRUM EVALUATOR...")
    print("Type 'exit' or 'quit' at any time to break the processing loop.")
    
    # Fully expanded, multi-category analytical dictionary matrix
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

    while True:
        print("\n" + "-"*60)
        proposition = input("ENTER TARGET PROPOSITION TEXT TO ANALYSE:\n> ").strip()
        
        if not proposition:
            continue
        if proposition.lower() in ['exit', 'quit']:
            print("\nExiting analytical processing stream. Core matrix offline.")
            print("="*60 + "\n")
            break
            
        scores = {}
        total_hits = 0
        for school, keywords in dictionary.items():
            count = sum(len(re.findall(rf"{word}", proposition.lower())) for word in keywords)
            scores[school] = count
            total_hits += count
            
        print("\n--- MATRIX ALIGNMENT MATCH SPECTRUM SCORES ---")
        if total_hits == 0:
            print(" * Unclassified Spectrum Matrix: 100.0% (No registered keyword hits)")
        else:
            for school, count in scores.items():
                pct = (count / total_hits * 100)
                if pct > 0:
                    print(f" * {school}: {pct:.1f}%")

if __name__ == "__main__":
    execute_computational_matrices()