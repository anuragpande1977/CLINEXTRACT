import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Clinical Study Extractor", layout="wide")

st.title("🧪 Clinical Study Summary Extractor")
st.markdown("Paste the full clinical study text below and click **Extract Information**. Output will be shown in a copyable table format for Excel.")

# --- Extraction functions ---
def extract_name(text):
    lines = text.strip().split('\n')
    for line in lines:
        if 'study' in line.lower():
            return line.strip()
    return "Not specified"

def extract_result(text):
    positive_keywords = ["significant improvement", "effective", "greater", "favorable"]
    negative_keywords = ["no significant difference", "not superior", "did not improve", "unlikely"]
    for kw in positive_keywords:
        if kw in text.lower():
            return "Positive"
    for kw in negative_keywords:
        if kw in text.lower():
            return "Negative"
    return "Not specified"

def extract_protocol(text):
    if "randomized" in text.lower() and "double-blind" in text.lower():
        return "Double-Blind Randomized Controlled Trial"
    elif "randomized" in text.lower():
        return "Randomized Controlled Trial"
    elif "observational" in text.lower():
        return "Observational"
    else:
        return "Other"

def extract_product(text):
    products = ["Permixon", "PA109", "Serenoa repens", "saw palmetto", "HESr", "Hexanic Extract"]
    for p in products:
        if p.lower() in text.lower():
            return p
    return "Not specified"

def extract_dosage(text):
    dosage_pattern = re.findall(r'(\d{2,4}\s?mg(?:/day)?(?:\s?(?:twice daily|once daily))?)', text, re.IGNORECASE)
    return ", ".join(set(dosage_pattern)) if dosage_pattern else "Not specified"

def extract_summary(text):
    # Take 2-3 most relevant lines as a summary based on keywords
    lines = text.split("\n")
    important = [l for l in lines if any(kw in l.lower() for kw in ["result", "improvement", "conclude", "reduction"])]
    return " ".join(important[:3]) if important else text[:300] + "..."

# --- Streamlit input ---
user_input = st.text_area("Paste clinical study summary text here:", height=300)

if st.button("Extract Information"):
    if user_input:
        data = {
            "NAME OF STUDY": extract_name(user_input),
            "AUTHOR": "",
            "YEAR": "",
            "RESULT": extract_result(user_input),
            "PROTOCOL": extract_protocol(user_input),
            "PRODUCT": extract_product(user_input),
            "SUMMARY": extract_summary(user_input),
            "DOSAGE": extract_dosage(user_input),
            "NOTES": ""
        }
        df = pd.DataFrame([data])

        st.subheader("📋 Extracted Study Info (copy and paste into Excel)")
        st.dataframe(df, use_container_width=True)

        st.markdown("---")
        st.markdown("**Excel-friendly Copy** (select below and paste directly into Excel):")
        st.code("\t".join(df.columns) + "\n" + "\t".join(str(v) for v in data.values()), language="tsv")
    else:
        st.warning("Please paste study summary text above.")
