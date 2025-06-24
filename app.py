#%%
# app.py
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Pediatric Dose Calculator", layout="centered")
st.title("💊 Pediatric Drug Dose Calculator")

@st.cache_data
def load_drug_data():
    df = pd.read_excel("drug_data.xlsx")
    df = df.dropna()
    return {
        row["Drug Name"]: (row["Min Dose"], row["Max Dose"], row["Unit"])
        for _, row in df.iterrows()
    }

drug_doses = load_drug_data()

drug = st.selectbox("Select Drug", sorted(drug_doses.keys()))

if drug:
    min_dose, max_dose, unit = drug_doses[drug]
    st.info(f"{drug} dosage range: {min_dose} - {max_dose} {unit}")

    weight = st.number_input("Enter weight (kg):", min_value=0.1, format="%.2f")
    times = st.number_input("Number of doses per day:", min_value=1, step=1)

    if st.button("Calculate"):
        if unit == "mg/kg/day":
            total_min = min_dose * weight
            total_max = max_dose * weight
            dose_min = total_min / times
            dose_max = total_max / times
        else:
            dose_min = min_dose * weight
            dose_max = max_dose * weight
            total_min = dose_min * times
            total_max = dose_max * times

        st.success("✅ Result:")
        st.markdown(f"""
        **Drug:** {drug}  
        **Weight:** {weight:.2f} kg  
        **Doses/day:** {times}  
        **Per Dose:** {dose_min:.2f} - {dose_max:.2f} mg  
        **Total Daily Dose:** {total_min:.2f} - {total_max:.2f} mg
        """)

# %%
