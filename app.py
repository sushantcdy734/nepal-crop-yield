"""
Nepal Crop Yield Prediction — Streamlit App
Predicts crop yield (kg/ha) from rainfall patterns.
"""
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

# ---------- Page config ----------
st.set_page_config(
    page_title="Nepal Crop Yield Predictor",
    page_icon="🌾",
    layout="wide",
)

# ---------- Load model and metadata ----------
@st.cache_resource
def load_model():
    return joblib.load("models/crop_yield_model.joblib")

@st.cache_data
def load_training_data():
    """Load the merged dataset to compute sensible defaults and ranges."""
    return pd.read_csv("data/merged_data.csv")

model = load_model()
df = load_training_data()

# ---------- Sidebar ----------
with st.sidebar:
    st.title("🌾 Crop Yield Predictor")
    st.markdown("""
    Predict crop yield for Nepal based on rainfall patterns.

    Built with **scikit-learn** and **Streamlit**.
    """)
    st.markdown("---")
    st.markdown("**Sushant Chaudhary**")
    st.caption("CS Student · Data Science & AI")
    st.markdown("[Portfolio](https://sushant-ds-portfolio.streamlit.app) · [GitHub](https://github.com/sushantcdy734)")

# ---------- Header ----------
st.title("🌾 Nepal Crop Yield Prediction")
st.markdown("""
Enter rainfall patterns below and predict the expected crop yield.
The model is a **Random Forest** trained on 40+ years of Nepal crop and rainfall data.
""")

st.markdown("---")

# ---------- Inputs ----------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌱 Crop")
    crop = st.selectbox(
        "Which crop?",
        options=sorted(df["crop"].unique()),
        help="Select the crop you want to predict yield for.",
    )

with col2:
    st.subheader("☔ Rainfall")
    total_rainfall = st.number_input(
        "Total yearly rainfall (mm)",
        min_value=float(df["total_rainfall"].min()),
        max_value=float(df["total_rainfall"].max()),
        value=float(df["total_rainfall"].mean()),
        step=1000.0,
        help="Sum of all rainfall in the year across all regions.",
    )

# ---------- Advanced inputs (in expander) ----------
with st.expander("⚙️ Advanced rainfall inputs"):
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        avg_rainfall = st.number_input(
            "Average rainfall per reading (mm)",
            min_value=float(df["avg_rainfall"].min()),
            max_value=float(df["avg_rainfall"].max()),
            value=float(df["avg_rainfall"].mean()),
            step=1.0,
        )
    with col_b:
        max_rainfall = st.number_input(
            "Maximum single reading (mm)",
            min_value=float(df["max_rainfall"].min()),
            max_value=float(df["max_rainfall"].max()),
            value=float(df["max_rainfall"].mean()),
            step=10.0,
        )
    with col_c:
        monsoon_rainfall = st.number_input(
            "Monsoon rainfall (June–Sept, mm)",
            min_value=float(df["monsoon_rainfall"].min()),
            max_value=float(df["monsoon_rainfall"].max()),
            value=float(df["monsoon_rainfall"].mean()),
            step=1000.0,
        )

# ---------- Predict ----------
if st.button("🌾 Predict Yield", type="primary", use_container_width=True):
    input_df = pd.DataFrame([{
        "crop": crop,
        "total_rainfall": total_rainfall,
        "avg_rainfall": avg_rainfall,
        "max_rainfall": max_rainfall,
        "monsoon_rainfall": monsoon_rainfall,
    }])

    prediction = model.predict(input_df)[0]

    st.markdown("---")
    st.subheader("🎯 Prediction")

    col_res1, col_res2 = st.columns([1, 2])

    with col_res1:
        st.metric(
            label=f"Predicted {crop} yield",
            value=f"{prediction:,.0f} kg/ha",
            delta=f"{prediction/1000:.2f} tonnes/ha",
        )

    with col_res2:
        # Show how this compares to the crop's historical average
        crop_avg = df[df["crop"] == crop]["yield_kg_per_ha"].mean()
        diff_pct = ((prediction - crop_avg) / crop_avg) * 100

        if diff_pct > 10:
            st.success(f"📈 **{diff_pct:+.1f}%** above the historical average for {crop} ({crop_avg:,.0f} kg/ha)")
        elif diff_pct < -10:
            st.warning(f"📉 **{diff_pct:+.1f}%** below the historical average for {crop} ({crop_avg:,.0f} kg/ha)")
        else:
            st.info(f"➡️ **{diff_pct:+.1f}%** — close to the historical average for {crop} ({crop_avg:,.0f} kg/ha)")

    st.markdown("---")

    # Show input summary
    with st.expander("📋 See input summary"):
        st.dataframe(input_df.T.rename(columns={0: "Value"}), use_container_width=True)

# ---------- Footer ----------
st.markdown("---")
st.caption("""
**About this model:** Random Forest (200 trees), trained on 220 rows of Nepal crop + rainfall data.
**Cross-validated R²:** 0.776 (5-fold, shuffled).
**Note:** Excludes `year` from features to avoid leakage from technological trends.
The model predicts ~78% of yield variance from rainfall alone.
""")

# ---------- Show model insights ----------
with st.expander("🔍 How the model decides"):
    st.markdown("""
    The model uses **rainfall patterns** and **crop type** to predict yield:

    - **Crop type** — the single biggest factor (Potatoes >> Rice > Maize > Wheat > Millet in yield)
    - **Monsoon rainfall** — the strongest rainfall signal (June–September dominates Nepal's water)
    - **Total & average rainfall** — secondary signals

    **What the model doesn't use:** year, soil quality, fertilizer, or weather timing.
    These are real factors but not in the dataset — they account for the remaining ~22% of variance.
    """)