import streamlit as st
import re
import textwrap

st.set_page_config(page_title="Clinical Study Extractor", layout="wide")
st.title("📋 Clinical Study Summary Extractor")

st.markdown("Paste a study summary below. The app will extract fields and give you a tab-separated row you can copy-paste into Excel.")

input_text = st.text_area("📄 Paste Study Summary Here:", height=400)

def extract_study_fields(text):
    # Initialize default values
    name = ""
    author = ""
    year_match = re.search(r'\b(19|20)\d{2}\b', text)
    year = year_match.group(0) if year_match else ""

    # Determine result
    if "no significant" in text.lower() or "did not improve" in text.lower():
        result = "Negative"
    elif "significant improvement" in text.lower() or "was effective" in text.lower() or "positive outcome" in text.lower():
        result = "Positive"
    else:
        result = ""

    # Determine protocol
    if "double-blind" in text.lower() and "placebo" in text.lower():
        protocol = "Randomized, double-blind, placebo-controlled"
    elif "randomized" in text.lower():
        protocol = "Randomized"
    elif "open-label" in text.lower():
        protocol = "Open-label"
    else:
        protocol = ""

    # Product guess
    if "permixon" in text.lower():
        product = "Permixon"
    elif "hesr" in text.lower():
        product = "HESr"
    elif "saw palmetto" in text.lower():
        product = "Saw Palmetto"
    elif "serenoa repens" in text.lower():
        product = "Serenoa repens"
    else:
        product = ""

    # Dosage
    dosage_match = re.search(r'(\d{2,4}\s?mg(?:/day)?(?:\s?(twice|once)?\s?(daily)?)?)', text.lower())
    dosage = dosage_match.group(1) if dosage_match else ""

    # Summary (shortened version)
    summary = textwrap.shorten(text.replace("\n", " "), width=280, placeholder="...")

    # Notes
    notes = ""

    return [name, author, year, result, protocol, product, summary, dosage, notes]

if input_text:
    extracted = extract_study_fields(input_text)
    tsv_line = "\t".join(extracted)
    
    st.markdown("### ✅ Tab-Separated Row (Copy This to Excel):")
    st.code(tsv_line, language='tsv')
    
    with st.expander("📋 Field Breakdown"):
        labels = ["NAME OF STUDY", "AUTHOR", "YEAR", "RESULT", "PROTOCOL", "PRODUCT", "SUMMARY", "DOSAGE", "NOTES"]
        for label, value in zip(labels, extracted):
            st.write(f"**{label}:** {value if value else '*blank*'}")
