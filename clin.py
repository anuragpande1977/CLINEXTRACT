import streamlit as st
import re
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Clinical Study Extractor", layout="wide")
st.title("📋 Clinical Study Summary Extractor")

st.markdown("""
Paste one clinical study summary at a time below. The app will extract the following fields:
- **Name of Article**
- **Author Name**
- **Year**
- **Result** (Positive/Negative)
- **Protocol** (e.g. randomized, double-blind)
- **Results Summary**
- **Dosage**

It will output a **tab-separated row** you can **copy and paste directly into Excel**.
""")

input_text = st.text_area("📄 Paste Study Summary Here:", height=400)

def extract_study_data(text):
    # Extract author (first capitalized name followed by et al or year pattern)
    author_match = re.search(r"([A-Z][a-z]+ et al\.|[A-Z][a-z]+,? \d{4})", text)
    author = author_match.group(1).replace(",", "") if author_match else ""

    # Extract year
    year_match = re.search(r"\b(19|20)\d{2}\b", text)
    year = year_match.group(0) if year_match else ""

    # Result
    result = "Positive" if re.search(r"significant improvement|effective|statistically significant", text, re.IGNORECASE) else "Negative" if re.search(r"no significant|did not improve|no improvement", text, re.IGNORECASE) else ""

    # Protocol
    protocol = ""
    if "double-blind" in text.lower(): protocol += "Double-blind, "
    if "placebo" in text.lower(): protocol += "Placebo-controlled, "
    if "randomized" in text.lower(): protocol += "Randomized, "
    if "open-label" in text.lower(): protocol += "Open-label, "
    protocol = protocol.strip(', ')

    # Dosage
    dosage_match = re.search(r"(\d{2,4}\s?mg(?:/[a-z]+)?(?:\s?(once|twice)? daily)?)", text, re.IGNORECASE)
    dosage = dosage_match.group(1) if dosage_match else ""

    # Short summary
    result_summary = re.sub(r"\n+", " ", text)
    result_summary = result_summary.strip()
    result_summary = result_summary[:300] + "..." if len(result_summary) > 300 else result_summary

    return ["", author, year, result, protocol, result_summary, dosage]

if input_text:
    output = extract_study_data(input_text)
    labels = ["Name of Article", "Author Name", "Year", "Result", "Protocol", "Results Summary", "Dosage"]
    tsv_line = "\t".join(output)

    st.markdown("### ✅ Copy-Paste This Row into Excel:")
    st.code(tsv_line, language='tsv')

    with st.expander("📋 Field Breakdown"):
        for label, val in zip(labels, output):
            st.write(f"**{label}:** {val if val else '*blank*'}")

