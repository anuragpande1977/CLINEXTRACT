import streamlit as st
import pandas as pd
from io import BytesIO

# --- Helper Functions ---

def generate_study_title(summary):
    s = summary.lower()
    if "real-world" in s and "luts" in s and "bph" in s:
        return "Real-world LUTS/BPH treatment study"
    if "double-blind" in s and "placebo" in s and "psa" in s:
        return "Saw palmetto effect on PSA levels"
    if "meta-analysis" in s:
        return "Meta-analysis of LUTS/BPH treatments"
    return "Saw palmetto clinical study"

def extract_product(summary):
    s = summary.lower()
    if "hexanic extract" in s:
        return "Hexanic extract of Serenoa repens (HESr)"
    if "serenoa repens" in s:
        return "Serenoa repens extract"
    if "usplus" in s:
        return "USPlus®"
    return "Saw palmetto extract"

def generate_result(summary):
    return "Positive for saw palmetto extract" if "improvement" in summary.lower() or "effective" in summary.lower() else "Neutral or unclear result"

def create_excel_row(summary):
    return {
        "NAME OF STUDY": generate_study_title(summary),
        "AUTHOR": "",
        "YEAR": "",
        "RESULT": generate_result(summary),
        "PROTOCOL": "6-month observational study in real-life settings" if "real-life" in summary.lower() else "Clinical protocol not specified",
        "PRODUCT": extract_product(summary),
        "SUMMARY": summary.strip().replace("\n", " "),
        "DOSAGE": "Not specified",
        "NOTES": "Better safety profile and good adherence reported" if "safety" in summary.lower() and "adherence" in summary.lower() else ""
    }

# --- Streamlit App ---

st.set_page_config(page_title="Study Summary to Excel", layout="centered")
st.title("📋 Study Summary to Excel Row Converter")

summary = st.text_area("Paste your scientific study summary below:", height=300)

if st.button("Generate Excel Row"):
    if summary.strip():
        row_data = create_excel_row(summary)
        df = pd.DataFrame([row_data])

        st.subheader("✅ Generated Data")
        st.dataframe(df)

        # Save to in-memory Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)

        # Download button
        st.download_button(
            label="📥 Download Excel File",
            data=output,
            file_name="study_summary.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("⚠️ Please enter a summary before generating.")
