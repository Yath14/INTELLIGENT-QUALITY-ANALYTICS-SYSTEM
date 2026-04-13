import joblib
import pandas as pd
from analysis import compute_metrics
from main import model, scaler
import subprocess
import os

def run_sqa_pipeline(code_path):
    # Step 1: Lint
    pylint_result = subprocess.run(['pylint', code_path], capture_output=True)
    
    # Step 2: Metrics
    metrics = compute_metrics(code_path)
    
    # Step 3: Predict
    data = pd.DataFrame([metrics]).reindex(columns=['loc', 'v_g', 'ev_g', 'iv_g', 'n', 'v'], fill_value=0)
    data_scaled = scaler.transform(data)
    prob = model.predict_proba(data_scaled)[0][1]
    
    # Quality Gate
    gate_pass = prob < 0.5
    return {
        'pylint': pylint_result.stdout,
        'metrics': metrics,
        'fault_prob': prob,
        'quality_gate': gate_pass,
        'recommendation': 'Review if >50% risk' if not gate_pass else 'Pass CI/CD'
    }

if __name__ == '__main__':
    print(run_sqa_pipeline('example.py'))
