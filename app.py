#%%
# app.py
import streamlit as st
import pandas as pd
import os

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Pediatric Dose Calculator", layout="centered")
st.title("💊 Pediatric Drug Dose Calculator")

# โหลดข้อมูลจาก Excel พร้อม cache
@st.cache_data
def load_drug_data(excel_path):
    df = pd.read_excel("drug_data.xlsx")
    df = df.dropna()
    drug_dict = {
        row["Drug Name"]: (row["Min Dose"], row["Max Dose"], row["Unit"])
        for _, row in df.iterrows()
    }
    return drug_dict

# โหลดไฟล์ drug_data.xlsx จากโฟลเดอร์เดียวกัน
excel_path = os.path.join(os.path.dirname(__file__), "drug_data.xlsx")

try:
    drug_doses = load_drug_data(excel_path)
    drug_names = sorted(drug_doses.keys())
    drug = st.selectbox("Select a drug", drug_names)

    if drug:
        min_dose, max_dose, unit = drug_doses[drug]
        st.info(f"Dosage range: {min_dose} - {max_dose} {unit}")

        weight_required = unit != "mg"  # ถ้าหน่วยเป็น mg ไม่ต้องป้อนน้ำหนัก

        if weight_required:
            weight = st.number_input("Enter weight (kg):", min_value=0.1, format="%.2f")
        else:
            weight = None  # ไม่ต้องใช้

        times = st.number_input("Number of doses per day:", min_value=1, step=1)

        if st.button("Calculate"):
            if unit == "mg/kg/day":
                total_min = min_dose * weight
                total_max = max_dose * weight
                dose_min = total_min / times
                dose_max = total_max / times

                st.success("✅ Result (mg/kg/day):")
                st.markdown(f"""
                **Drug:** {drug}  
                **Weight:** {weight:.2f} kg  
                **Doses/day:** {times}  
                **Per Dose:** {dose_min:.2f} - {dose_max:.2f} mg  
                **Total Daily Dose:** {total_min:.2f} - {total_max:.2f} mg
                """)

            elif unit == "mg/kg/dose":
                dose_min = min_dose * weight
                dose_max = max_dose * weight
                total_min = dose_min * times
                total_max = dose_max * times

                st.success("✅ Result (mg/kg/dose):")
                st.markdown(f"""
                **Drug:** {drug}  
                **Weight:** {weight:.2f} kg  
                **Doses/day:** {times}  
                **Per Dose:** {dose_min:.2f} - {dose_max:.2f} mg  
                **Total Daily Dose:** {total_min:.2f} - {total_max:.2f} mg
                """)

            elif unit == "mg":
                dose_min = min_dose
                dose_max = max_dose
                total_min = dose_min * times
                total_max = dose_max * times

                st.success("✅ Result (mg):")
                st.markdown(f"""
                **Drug:** {drug}  
                **Doses/day:** {times}  
                **Per Dose:** {dose_min:.2f} - {dose_max:.2f} mg  
                **Total Daily Dose:** {total_min:.2f} - {total_max:.2f} mg
                """)
            else:
                st.warning(f"⚠️ Unrecognized unit: {unit}")

except Exception as e:
    st.error(f"❌ Failed to read 'drug_data.xlsx': {e}")
