import streamlit as st
import pandas as pd
import io

# Define the column structure
columns = ["NAME OF STUDY", "AUTHOR", "YEAR", "RESULT", "PROTOCOL", "PRODUCT", "SUMMARY", "DOSAGE", "NOTES"]

# Streamlit app title
st.title("Clinical Study Summary Extractor")

# Input box for pasting the study summary
text_input = st.text_area("Paste the Clinical Study Summary Text Here:", height=400)

if st.button("Extract and Download Excel"):
    if text_input.strip():
        # Dummy placeholder logic - you can replace this with actual NLP extraction rules
        # For now it populates only SUMMARY and leaves others blank for manual entry
        row = ["" for _ in columns]
        row[6] = text_input.strip()  # Put entire pasted text into SUMMARY column

        df = pd.DataFrame([row], columns=columns)

        # Create Excel in memory
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        buffer.seek(0)

        st.download_button(
            label="Download Extracted Excel File",
            data=buffer,
            file_name="clinical_study_extracted.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("Please paste the clinical study summary text before extracting.")


