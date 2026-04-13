from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import joblib
import pandas as pd
from pydantic import BaseModel
import traceback

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "defect_model (1).pkl"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"

if MODEL_PATH.exists() and SCALER_PATH.exists():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
else:
    raise FileNotFoundError(
        f"Missing model or scaler in {BASE_DIR / 'models'}: "
        f"{MODEL_PATH.name if not MODEL_PATH.exists() else ''} "
        f"{SCALER_PATH.name if not SCALER_PATH.exists() else ''}"
    )

class SoftwareMetrics(BaseModel):
    loc: float
    v_g: float
    ev_g: float
    iv_g: float
    n: float
    v: float

@app.post("/predict")
def predict_fault(metrics: SoftwareMetrics):
    try:
        # 1. Map input metrics to CM1 dataset column names
        # The scaler was trained on all 20 CM1 features
        # We calculate/derive the missing ones from the 6 inputs
        data_dict = {
            'loc': metrics.loc,
            'v(g)': metrics.v_g,
            'ev(g)': metrics.ev_g,
            'iv(g)': metrics.iv_g,
            'n': metrics.n,
            'v': metrics.v,
            # Fill remaining features with derived or default values
            'l': metrics.v / metrics.n if metrics.n > 0 else 0,  # Program length
            'd': metrics.v / (metrics.iv_g * metrics.ev_g) if (metrics.iv_g * metrics.ev_g) > 0 else 0,  # Difficulty
            'i': metrics.n / (metrics.v_g * metrics.ev_g) if (metrics.v_g * metrics.ev_g) > 0 else 0,  # Intelligence
            'e': metrics.v * metrics.v_g / 10,  # Effort
            'b': metrics.v_g * metrics.ev_g / 20,  # Default effort (Fenton measure)
            't': (metrics.v * metrics.v_g) / (2000),  # Time estimate
            'lOCode': metrics.loc,  # Lines of Code
            'lOComment': metrics.loc * 0.2,  # Estimate comments as 20% of code
            'lOBlank': metrics.loc * 0.1,  # Estimate blank lines as 10% of code
            'locCodeAndComment': metrics.loc * 1.2,  # Code + comments
            'uniq_Op': metrics.v_g * 2,  # Unique operators estimate
            'uniq_Opnd': int(metrics.n * 0.6),  # Unique operands estimate
            'total_Op': int(metrics.n * 0.4),  # Total operators estimate
            'total_Opnd': int(metrics.n * 0.6),  # Total operands estimate
            'branchCount': int(metrics.v_g - 1),  # Branch count from cyclomatic
        }
        
        data = pd.DataFrame([data_dict])
        print(f"Input data (fully expanded): {data.columns.tolist()}")
        
        # 2. Scale the data
        data_scaled = scaler.transform(data)
        print(f"Scaled data shape: {data_scaled.shape}")
        
        # 3. Predict
        prediction = model.predict(data_scaled)
        probability = model.predict_proba(data_scaled)[0][1]
        print(f"Prediction: {prediction}, Probability: {probability}")
        
        return {
            "is_defect": bool(prediction[0]), 
            "probability": round(float(probability) * 100, 2),
            "status": "High Risk" if prediction[0] else "Stable"
        }
    except Exception as e:
        error_msg = f"Prediction Error: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "detail": error_msg}
        )