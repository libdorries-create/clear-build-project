from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import shapiro
import re
from typing import List, Dict

app = FastAPI(title="Universal Empirical & Philosophical API", version="1.0.0")

# --- CORE MATH MODELS ---
def linear_theory(x, m, c): return m * x + c
def polynomial_theory(x, a, b, c): return a * (x**2) + b * x + c

# --- PYDANTIC SCHEMAS FOR DATA ACCEPATANCE ---
class MathDataPayload(BaseModel):
    x: List[float]
    y: List[float]

class PhilosophyPayload(BaseModel):
    text: str

# --- ENDPOINT 1: DATA VALIDATION & CURVE FITTING ---
@app.post("/api/v1/validate-math")
def validate_math_matrix(payload: MathDataPayload):
    if len(payload.x) != len(payload.y) or len(payload.x) < 3:
        raise HTTPException(status_code=400, detail="X and Y arrays must have identical dimensions and contain at least 3 points.")
    
    data_x = np.array(payload.x)
    data_y = np.array(payload.y)
    
    # Statistical Normality Check
    stat, p_val = shapiro(data_y)
    gaussian_status = "PASSED" if p_val > 0.05 else "REJECTED"
    
    # Curve Fitting Matrix
    ss_tot = np.sum((data_y - np.mean(data_y))**2)
    if ss_tot == 0:
        raise HTTPException(status_code=400, detail="Variance of Y data is zero; cannot compute R².")
        
    def get_r2(tf, *p): return 1 - (np.sum((data_y - tf(data_x, *p))**2) / ss_tot)
    
    try:
        popt_lin, _ = curve_fit(linear_theory, data_x, data_y)
        r2_lin = get_r2(linear_theory, *popt_lin)
    except Exception:
        r2_lin, popt_lin = 0.0, [0.0, 0.0]
        
    try:
        popt_poly, _ = curve_fit(polynomial_theory, data_x, data_y)
        r2_poly = get_r2(polynomial_theory, *popt_poly)
    except Exception:
        r2_poly, popt_poly = 0.0, [0.0, 0.0, 0.0]

    return {
        "shapiro_wilk": {"p_value": float(p_val), "status": gaussian_status},
        "linear_fit": {"r_squared": float(r2_lin), "parameters": [float(n) for n in popt_lin]},
        "polynomial_fit": {"r_squared": float(r2_poly), "parameters": [float(n) for n in popt_poly]}
    }

# --- ENDPOINT 2: PHILOSOPHICAL SPECTRUM PARSER ---
@app.post("/api/v1/validate-philosophy")
def validate_philosophy_matrix(payload: PhilosophyPayload):
    proposition = payload.text.lower()
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
        
    percentages = {k: float(v / total_hits * 100) if total_hits > 0 else 0.0 for k, v in scores.items()}
    
    return {
        "raw_text_length": len(payload.text),
        "total_keyword_hits": total_hits,
        "spectrum_alignment": percentages
    }
