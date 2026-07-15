import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import shapiro
import re
from datetime import datetime

def linear_theory(x, m, c): return m * x + c
def polynomial_theory(x, a, b, c): return a * (x**2) + b * x + c

def execute_computational_matrices():
    print("\n" + "="*50)
    print("      UNIVERSAL MATRIX DATA VALIDATOR ACTIVATED")
    print("="*50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # --- PIPELINE 1: MATH ANALYTICS DATA ---
    print("[1/2] RUNNING MATHEMATICAL THEORETICAL CURVE FITTING...")
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
    
    # --- PIPELINE 2: TEXT CONCEPT ANALYSIS ---
    print("\n[2/2] RUNNING PHILOSOPHICAL CONFIGURATION EVALUATION...")
    proposition = "Life possesses no objective value or intrinsic meaning. The universe is cold and indifferent. Therefore, one must cultivate absolute emotional control, enduring hardship with unshakeable stoic calm."
    print(f" Target Text: \"{proposition[:60]}...\"")
    
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
        count = sum(len(re.findall(rf"{word}", proposition.lower())) for word in keywords)
        scores[school] = count
        total_hits += count
        
    print("\n--- MATRIX ALIGNMENT MATCH SPECTRUM SCORES ---")
    for school, count in scores.items():
        pct = (count / total_hits * 100) if total_hits > 0 else 0.0
        if pct > 0:
            print(f" * {school}: {pct:.1f}%")
    print("="*50 + "\n")

if __name__ == "__main__":
    execute_computational_matrices()
