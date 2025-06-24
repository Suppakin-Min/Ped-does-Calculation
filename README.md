import streamlit as st
import pandas as pd
import os

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Pediatric Dose Calculator", layout="centered")
st.title("💊 Pediatric Drug Dose Calculator")

@st.cache_data
def load_drug_data(excel_path):
    df = pd.read_excel(excel_path)
    df = df.dropna()
    return {
        row["Drug Name"]: (row["Min Dose"], row["Max Dose"], row["Unit"])
        for _, row in df.iterrows()
    }

# Path ไปยัง Excel
excel_path = os.path.join(os.path.dirname(__file__), "drug_data.xlsx")

# ปุ่ม reload cache
if st.button("🔁 Reload Drug List"):
    st.cache_data.clear()

try:
    drug_doses = load_drug_data(excel_path)
    drug_names = sorted(drug_doses.keys())
    drug = st.selectbox("Select a drug", drug_names)

    if drug:
        min_dose, max_dose, unit = drug_doses[drug]
        st.info(f"Dosage range: {min_dose} - {max_dose} {unit}")

        # ⏎ ฟอร์มแบบ submit
        with st.form("dose_form", clear_on_submit=False):
            weight = st.number_input("Enter weight (kg):", min_value=0.1, format="%.2f")
            times = st.number_input("Number of doses per day:", min_value=1, step=1)
            submitted = st.form_submit_button("Calculate")  # ⏎ หรือกดปุ่ม

        if submitted:
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

            st.success("✅ Calculation Result:")
            st.markdown(f"""
            **Drug:** {drug}  
            **Weight:** {weight:.2f} kg  
            **Doses/day:** {times}  
            **Unit:** {unit}

            **Per Dose:** {dose_min:.2f} - {dose_max:.2f} mg  
            **Total Daily Dose:** {total_min:.2f} - {total_max:.2f} mg
            """)
except Exception as e:
    st.error(f"❌ Failed to read 'drug_data.xlsx': {e}")
