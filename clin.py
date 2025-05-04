import streamlit as st
import pandas as pd
import re

# Updated extraction functions
def detect_result(text):
    positive_keywords = ["significant improvement", "effective", "improved", "benefit", "favorable", "comparable"]
    negative_keywords = ["no improvement", "no significant difference", "not effective", "failed", "unlikely"]
    for word in positive_keywords:
        if word in text.lower():
            return "Positive"
    for word in negative_keywords:
        if word in text.lower():
            return "Negative"
    return "Not specified"

def extract_dosage(text):
    patterns = [
        r'\d+\s?mg(?:\s?/\s?day)?(?:\s?(?:once|twice|three times) daily)?',
        r'\d+\s?mg\s?(?:daily|per day)',
        r'\d+\s?mg(?:\s?x\s?\d+)?',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    return "Not specified"

def extract_product(text):
    products = ["Permixon", "PA109", "Serenoa repens", "saw palmetto", "HESr", "Hexanic Extract of Serenoa repens"]
    for prod in products:
        if prod.lower() in text.lower():
            return prod
    return "Not specified"

def extract_protocol(text):
    if "double-blind" in text.lower():
        return "Double-Blind Randomized Controlled Trial"
    elif "randomized" in text.lower():
        return "Randomized Controlled Trial"
    elif "observational" in text.lower():
        return "Observational Study"
    return "Not specified"

def extract_name_of_study(text):
    lines = text.strip().split('\n')
    for line in lines:
        if "study" in line.lower():
            return line.strip()
    return "Not specified"

def extract_summary(text):
    paragraphs = text.split("\n\n")
    summary = " ".join([p.strip() for p in paragraphs if len(p.strip()) > 50])
    return summary[:1000]  # Trim to first 1000 chars if too long

# Streamlit UI
st.title("Clinical Study Extractor")
st.write("Paste a study summary below to extract key information.")

user_input = st.text_area("Paste the study text here:", height=400)

if st.button("Extract Study Info"):
    if user_input.strip():
        data = {
            "NAME OF STUDY": extract_name_of_study(user_input),
            "AUTHOR": "",
            "YEAR": "",
            "RESULT": detect_result(user_input),
            "PROTOCOL": extract_protocol(user_input),
            "PRODUCT": extract_product(user_input),
            "SUMMARY": extract_summary(user_input),
            "DOSAGE": extract_dosage(user_input),
            "NOTES": ""
        }

        df = pd.DataFrame([data])
        st.markdown("### Extracted Information")
        st.dataframe(df)

        st.markdown("### Copy & Paste Output for Excel")
        row = f"{data['NAME OF STUDY']}\t{data['AUTHOR']}\t{data['YEAR']}\t{data['RESULT']}\t{data['PROTOCOL']}\t{data['PRODUCT']}\t{data['SUMMARY']}\t{data['DOSAGE']}\t{data['NOTES']}"
        st.code(row, language='text')
    else:
        st.warning("Please enter study text to extract.")



