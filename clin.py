
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
    return "Positive" if "improvement" in summary.lower() or "effective" in summary.lower() else "Neutral or unclear"

def format_summary_for_excel(summary_text):
    name = generate_study_title(summary_text)
    author = ""
    year = ""
    result = generate_result(summary_text)
    protocol = "Double-Blind RCT" if "double-blind" in summary_text.lower() else "Observational" if "real-life" in summary_text.lower() else "Unspecified"
    product = extract_product(summary_text)
    summary = summary_text.strip().replace("\n", " ")
    dosage = "320 mg" if "320 mg" in summary_text else "Not specified"
    notes = ""

    return f"{name}\t{author}\t{year}\t{result}\t{protocol}\t{product}\t{summary}\t{dosage}\t{notes}"

# === Example ===
if __name__ == "__main__":
    print("Paste your SciSummary text (end with ENTER + CTRL+D on Mac/Linux or ENTER + CTRL+Z on Windows):\n")
    import sys
    summary_input = sys.stdin.read()

    print("\n📋 Copy and paste this line into Excel:\n")
    print(format_summary_for_excel(summary_input))
