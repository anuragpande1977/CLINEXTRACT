
import streamlit as st
import pandas as pd
import re

# Function to extract information from pasted study text
def extract_study_info(text):
    result_keywords = {
        "positive": ["significant improvement", "effectively", "better", "improvement", "favorable", "efficacy"],
        "negative": ["no significant difference", "no improvement", "did not", "failed to", "unlikely to", "not superior"]
    }

    def detect_result(text):
        for pos_word in result_keywords["positive"]:
            if pos_word.lower() in text.lower():
                return "Positive"
        for neg_word in result_keywords["negative"]:
            if neg_word.lower() in text.lower():
                return "Negative"
        return "Not specified"

    def extract_dosage(text):
        match = re.search(r'(\d+\s?mg(?:/day)?(?:\s?(?:once|twice) daily)?)', text, re.IGNORECASE)
        return match.group(1) if match else "Not specified"

    def extract_product(text):
        match = re.search(r'(Permixon|PA109|Serenoa repens|saw palmetto|HESr|Hexanic Extract of Serenoa repens)', text, re.IGNORECASE)
        return match.group(1) if match else "Not specified"

    def extract_name_of_study(text):
        lines = text.strip().split('\n')
        for line in lines:
            if "study" in line.lower():
                return line.strip()
        return "Not specified"

    def extract_protocol(text):
        if "double-blind" in text.lower():
            return "Double-Blind Randomized Controlled Trial"
        elif "randomized" in text.lower():
            return "Randomized Controlled Trial"
        elif "observational" in text.lower():
            return "Observational"
        else:
            return "Not specified"

    def extract_summary(text):
        paragraphs = text.strip().split('\n')
        for p in paragraphs:
            if "result" in p.lower() or "conclusion" in p.lower():
                return p.strip()
        return paragraphs[-1].strip() if paragraphs else "Not specified"

    info = {
        "NAME OF STUDY": extract_name_of_study(text),
        "AUTHOR": "",
        "YEAR": "",
        "RESULT": detect_result(text),
        "PROTOCOL": extract_protocol(text),
        "PRODUCT": extract_product(text),
        "SUMMARY": extract_summary(text),
        "DOSAGE": extract_dosage(text),
        "NOTES": ""
    }
    return info

st.title("Clinical Study Summary Extractor")

user_input = st.text_area("Paste the study summary text here:")

if st.button("Extract Information"):
    if user_input:
        info = extract_study_info(user_input)
        df = pd.DataFrame([info])
        output_string = '\t'.join(df.columns.tolist()) + '\n' + '\t'.join(df.iloc[0].astype(str).tolist())
        st.text_area("Copy and paste this into Excel:", output_string, height=200)
    else:
        st.warning("Please paste the study summary text before clicking extract.")
