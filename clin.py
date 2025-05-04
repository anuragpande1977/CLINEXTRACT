import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Study Summary Extractor")

text = st.text_area("Paste your study summary here:", height=300)

if st.button("Extract and Download"):
    columns = ["NAME OF STUDY", "AUTHOR", "YEAR", "RESULT", "PROTOCOL", "PRODUCT", "SUMMARY", "DOSAGE", "NOTES"]
    df = pd.DataFrame([[None]*len(columns)], columns=columns)
    df["SUMMARY"] = text

    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    st.download_button("Download Excel", buffer.getvalue(), "study_summary.xlsx", mime="application/vnd.ms-excel")
