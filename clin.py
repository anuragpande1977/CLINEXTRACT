import streamlit as st
import pandas as pd
import re
from io import BytesIO

st.set_page_config(page_title="Clinical Study Extractor", layout="wide")
st.title("Clinical Study Extractor")

# Template columns
columns = ["NAME OF STUDY", "AUTHOR", "YEAR", "RESULT", "PROTOCOL", "PRODUCT", "SUMMARY", "DOSAGE", "NOTES"]

def extract_fields_from_text(text):
    # Initialize blank row
    row = {col: "" for col in columns}

    # Simple logic to extract common fields if patterns are matched
    if "randomized" in text.lower():
        row["PROTOCOL"] = "Randomized, double-blind, placebo-controlled trial"
    if "serenoa repens" in text.lower():
        row["PRODUCT"] = "Serenoa repens extract"
    if "saw palmetto" in text.lower():
        row["PRODUCT"] = "Saw palmetto extract"
    if "AUASI" in text or "IPSS" in text:
        row["SUMMARY"] = "Study measured changes in AUASI/IPSS scores and urinary outcomes."
    if "psa" in text.lower():
        row["NOTES"] = "PSA level evaluation included"
    if match := re.search(r'(\d{3,4})\s*mg', text):
        row["DOSAGE"] = match.group(0)
    if "placebo" in text.lower():
        row["RESULT"] = "No significant difference vs. placebo"
    else:
        row["RESULT"] = "Positive outcome"

    row["SUMMARY"] = text.strip().replace("\n", " ")[:400]  # Condensed summary
    row["NAME OF STUDY"] = "Extracted Study"

    return row

uploaded_file = st.file_uploader("Upload your study summary text file (.txt)", type=["txt"])

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
    row_data = extract_fields_from_text(text)
    df = pd.DataFrame([row_data], columns=columns)
    st.dataframe(df)

    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    st.download_button("Download as Excel", data=buffer.getvalue(), file_name="study_extracted.xlsx")

