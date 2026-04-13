import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="IQA System", layout="wide")

st.title("🛡️ Intelligent Quality Analytics System")
st.markdown("### Early Software Fault Identification using NASA CM1 Dataset")

# 2. Sidebar for Input Metrics
st.sidebar.header("Input Code Metrics")

# User Inputs for the NASA CM1 dataset
loc = st.sidebar.number_input("Line Count (loc)", value=1.0)
v_g = st.sidebar.number_input("Cyclomatic Complexity (v(g))", value=1.0)
ev_g = st.sidebar.number_input("Essential Complexity (ev(g))", value=1.0)
iv_g = st.sidebar.number_input("Design Complexity (iv(g))", value=1.0)
n = st.sidebar.number_input("Halstead Length (n)", value=0.0)
v = st.sidebar.number_input("Halstead Volume (v)", value=0.0)

# 3. Main Action Button
if st.button("Analyze Module"):
    # Everything below this line is indented exactly one level
    payload = {
        "loc": loc, 
        "v_g": v_g, 
        "ev_g": ev_g, 
        "iv_g": iv_g, 
        "n": n, 
        "v": v
    }
    
    try:
        with st.spinner('Analyzing...'):
            # Send data to the FastAPI backend
            response = requests.post("http://127.0.0.1:8000/predict", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                # Display Prediction Results
                st.markdown("### Prediction Results")
                st.write("**Risk Score:**", f"{result['probability']}%")
                st.write("**Status:**", result["status"])

                if result["is_defect"]:
                    st.error("⚠️ HIGH RISK: This module is likely to have defects.")
                else:
                    st.success("✅ LOW RISK: This module appears stable.")
            else:
                st.error(f"Backend Error: {response.status_code} - {response.text}")
                
    except Exception as e:
        st.error(f"Connection Error: Is the FastAPI backend running? Details: {e}")