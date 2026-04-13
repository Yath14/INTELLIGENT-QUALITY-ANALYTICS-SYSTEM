import os
import subprocess
import ast
from collections import Counter
import pandas as pd

def compute_metrics(code_path):
    # Simple LOC
    with open(code_path, 'r') as f:
        lines = f.readlines()
    loc = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
    
    # Cyclomatic complexity approx via AST
    tree = ast.parse(''.join(lines))
    branches = sum(1 for node in ast.walk(tree) if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With)))
    vg = branches + 1
    
    # Pylint score
    try:
        result = subprocess.run(['pylint', code_path], capture_output=True, text=True)
        score = float(result.stdout.split('Your code has been rated at ')[-1].split('/')[0]) if 'rated at' in result.stdout else 0
    except:
        score = 0
    
    return {'loc': loc, 'v_g': vg, 'pylint_score': score}

def load_dataset_stats(csv_path):
    df = pd.read_csv(csv_path)
    df['defective'] = df['defects'].apply(lambda x: 1 if x > 0 else 0)
    risk = pd.read_csv('cm1_defect_risk_results.csv')['defect_risk_score'] if os.path.exists('cm1_defect_risk_results.csv') else None
    return df.describe(), risk.describe() if risk is not None else None

print('Analysis module ready for SQA pipeline.')

