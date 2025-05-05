import streamlit as st

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
    name = generate_study_title(summary)
    author = ""
    year = ""
    result = generate_result(summary)
    protocol = "6-month observational study in real-life clinical settings" if "real-life" in summary.lower() else "Clinical protocol not specified"
    product = extract_product(summary)
    summary_text = summary.strip().replace("\n", " ")
    dosage = "Not specified"
    notes = "Better safety profile and good adherence reported" if "safety" in summary.lower() and "adherence" in summary.lower() else ""

    return {
        "NAME OF STUDY": name,
        "AUTHOR": author,
        "YEAR": year,
        "RESULT": result,
        "PROTOCOL": protocol,
        "PRODUCT": product,
        "SUMMARY": summary_text,
        "DOSAGE": dosage,
        "NOTES": notes
    }

# === Streamlit App ===
st.title("🧪 Study Summary to Excel Row Converter")

summary_input = st.text_area("Paste your scientific study summary here:", height=300)

if st.button("Generate Excel Row"):
    if summary_input.strip():
        row_data = create_excel_row(summary_input)
        st.success("✅ Generated Data:")
        st.dataframe([row_data])
        st.download_button("📥 Download as Excel", 
                           pd.DataFrame([row_data]).to_excel(index=False, engine='openpyxl'),
                           file_name="study_row.xlsx")
    else:
        st.warning("⚠️ Please paste a summary before clicking generate.")
