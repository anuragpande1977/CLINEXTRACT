import pandas as pd

# === Core functions ===
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
    if "improvement" in summary.lower() or "effective" in summary.lower():
        return "Positive"
    return "Neutral or unclear"

def parse_summary(summary_text):
    return {
        "Name of Study": generate_study_title(summary_text),
        "Author": "",
        "Year": "",
        "Results": generate_result(summary_text),
        "Study Protocol": "Double-Blind Randomized Controlled Trial" if "double-blind" in summary_text.lower() else "Observational" if "real-life" in summary_text.lower() else "Unspecified",
        "Product": extract_product(summary_text),
        "Summary": summary_text.strip().replace("\n", " "),
        "Dosage": "320 mg" if "320 mg" in summary_text else "Not specified",
        "Notes": ""
    }

# === Store multiple summaries ===
all_summaries = []

# === Example usage for multiple studies ===
if __name__ == "__main__":
    # Paste each summary here one by one
    summaries = [
        """This study evaluated the changes in symptoms and quality of life (QoL) in a large cohort...""",
        """A randomized, double-blind, two-arm trial involving 369 men aged 45 and above assessed the effects..."""
    ]

    for s in summaries:
        all_summaries.append(parse_summary(s))

    # === Export to ONE Excel file ===
    df = pd.DataFrame(all_summaries)
    df.to_excel("All_SawPalmetto_Studies.xlsx", index=False)
    print("✅ All summaries exported to 'All_SawPalmetto_Studies.xlsx'")

