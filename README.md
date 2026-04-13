# 🛡️ Software Fault Identification System

> **Intelligent Quality Analytics (IQA) — Early defect detection powered by Machine Learning on NASA CM1 dataset**

---

## 📌 Overview

The **Software Fault Identification System** is an end-to-end ML-powered application that predicts software defects at the **module level** using static code metrics. It leverages the NASA CM1 dataset and a trained **Random Forest classifier** to assess fault probability — enabling teams to prioritize code reviews and prevent bugs before they reach production.

The system consists of:
- A **FastAPI** REST backend serving the trained ML model
- A **Streamlit** interactive web UI for real-time fault analysis
- A **SQA pipeline** combining Pylint linting, Halstead/cyclomatic metrics, and ML-based risk scoring

---

## 🧠 How It Works

1. The user enters **6 core code metrics** (LOC, cyclomatic complexity, Halstead metrics) via the UI.
2. The backend **derives 15 additional features** from the inputs to match the CM1 feature space.
3. The data is **scaled** using a pre-trained `StandardScaler`.
4. The **Random Forest model** predicts: fault probability (%), risk label (`High Risk` / `Stable`), and a binary defect flag.

---

## 📊 Dataset

| Dataset | Source | Records | Features |
|---------|--------|---------|----------|
| CM1     | NASA MDP | ~498 modules | 21 code metrics |
| JM1     | NASA MDP | ~10,878 modules | 22 code metrics |

**Key features used:** `loc`, `v(g)`, `ev(g)`, `iv(g)`, `n`, `v` (Halstead Length & Volume)

---

## 🏗️ Project Structure

```
Software_Fault_Identification_System/
│
├── main.py              # FastAPI backend — /predict endpoint
├── ui.py                # Streamlit frontend — interactive input UI
├── sqa_project.py       # Model training, EDA, evaluation (Colab notebook style)
├── pipeline.py          # Full SQA pipeline (lint + metrics + ML predict)
├── analysis.py          # Code metric computation utilities
├── run_project.py       # One-click launcher (starts backend + UI)
├── run_project.bat      # Windows batch launcher
├── run_project.ps1      # PowerShell launcher
│
├── data/
│   ├── cm1.csv          # NASA CM1 defect dataset
│   └── jm1.csv          # NASA JM1 defect dataset
│
├── models/
│   ├── defect_model.pkl # Trained Random Forest classifier
│   └── scaler.pkl       # Fitted StandardScaler
│
└── requirements.txt     # Python dependencies
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- pip

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/software-fault-identification-system.git
cd software-fault-identification-system
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
```

Activate it:
- **Windows:** `.venv\Scripts\activate`
- **macOS/Linux:** `source .venv/bin/activate`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application

**Option A — One-click launcher (Windows):**
```bash
python run_project.py
```

**Option B — Manual (two terminals):**

Terminal 1 — Start the FastAPI backend:
```bash
uvicorn main:app --port 8000
```

Terminal 2 — Start the Streamlit UI:
```bash
streamlit run ui.py
```

Then open your browser at: **http://localhost:8501**

---

## 🖥️ Usage

1. Open the Streamlit UI at `http://localhost:8501`
2. Enter your module's code metrics in the **sidebar**:
   - **LOC** — Lines of Code
   - **v(g)** — Cyclomatic Complexity
   - **ev(g)** — Essential Complexity
   - **iv(g)** — Design Complexity
   - **n** — Halstead Program Length
   - **v** — Halstead Volume
3. Click **"Analyze Module"**
4. View the **fault probability (%)**, **risk status**, and recommendation

---

## 🔌 API Reference

### `POST /predict`

Predicts software fault probability for a given module.

**Request Body:**
```json
{
  "loc": 120.0,
  "v_g": 5.0,
  "ev_g": 3.0,
  "iv_g": 2.0,
  "n": 80.0,
  "v": 350.0
}
```

**Response:**
```json
{
  "is_defect": true,
  "probability": 76.34,
  "status": "High Risk"
}
```

API docs available at: `http://127.0.0.1:8000/docs`

---

## 📈 Model Performance

| Metric | Value |
|--------|-------|
| Algorithm | Random Forest (200 estimators) |
| Imbalance Handling | SMOTE oversampling |
| Preprocessing | StandardScaler |
| Evaluation | ROC-AUC, Precision, Recall, F1 |
| DRE (Defect Removal Effectiveness) | Computed post-evaluation |

Three models were benchmarked:
- Logistic Regression
- Decision Tree
- **Random Forest** ✅ *(selected — best ROC-AUC)*

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| ML / Data | scikit-learn, pandas, numpy, imbalanced-learn |
| Backend | FastAPI, Uvicorn |
| Frontend | Streamlit |
| Code Quality | Pylint, Radon |
| Model Persistence | Joblib |
| Version Control | GitPython |

---

## 📋 Requirements

```
fastapi
uvicorn
streamlit
joblib
pandas
scikit-learn
requests
imbalanced-learn
pylint
radon
flask
gitpython
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- **NASA Metrics Data Program (MDP)** for the CM1 and JM1 defect datasets
- scikit-learn and the open-source ML community
