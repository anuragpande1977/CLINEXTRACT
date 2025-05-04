import streamlit as st
import pandas as pd
import re

st.title("Clinical Study Extractor for BPH")
st.write("Paste your clinical study summary below. The tool will extract key fields and display them in a format ready to paste into Excel.")

user_input = st.text_area("Paste study summary text here:", height=400)

# Helper functions for extraction
def detect_result(text):
    positive_keywords = ["significant improvement", "effective", "improved", "positive outcome", "successfully"]
    negative_keywords = ["no significant difference", "no improvement", "not effective", "failed to"]
    
    for word in positive_keywords:
        if word.lower() in text.lower():
            return "Positive"
    for word in negative_keywords:
        if word.lower() in text.lower():
            return "Negative"
    return "Not specified"

def extract_protocol(text):
    if "double-blind" in text.lower():
        return "Double-blind randomized controlled trial"
    elif "randomized" in text.lower():
        return "Randomized controlled trial"
    elif "observational" in text.lower():
        return "Observational study"
    return "Not specified"

def extract_product(text):
    products = ["Permixon", "PA109", "Serenoa repens", "saw palmetto", "HESr", "Hexanic Extract of Serenoa repens", "finasteride"]
    for product in products:
        if product.lower() in text.lower():
            return product
    return "Not specified"

def extract_dosage(text):
    matches = re.findall(r'(\d+\s?mg(?:/day)?(?:\s?twice daily)?)', text, re.IGNORECASE)
    return ", ".join(matches) if matches else "Not specified"

def extract_summary(text):
    paragraphs = text.split('\n')
    summary_parts = [p.strip() for p in paragraphs if p.strip() and not p.lower().startswith("study overview")]
    return " ".join(summary_parts)[:600] + "..."

if st.button("Extract and Format"):
    if user_input.strip():
        row = {
            "NAME OF STUDY": "Comparative Study of Permixon\u00ae and Finasteride in BPH Treatment",
            "AUTHOR": "",
            "YEAR": "",
            "RESULT": detect_result(user_input),
            "PROTOCOL": extract_protocol(user_input),
            "PRODUCT": extract_product(user_input),
            "SUMMARY": extract_summary(user_input),
            "DOSAGE": extract_dosage(user_input),
            "NOTES": ""
        }
        df = pd.DataFrame([row])
        formatted = "\t".join(df.columns.tolist()) + "\n" + "\t".join(df.iloc[0].astype(str).tolist())
        st.text_area("Copy this row into Excel: ", formatted, height=200)
        st.success("Extraction complete. You can now copy and paste into Excel.")
    else:
        st.warning("Please paste a study summary first.")
