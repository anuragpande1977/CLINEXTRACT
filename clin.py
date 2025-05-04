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

def parse_summary(summary_text):
    name = generate_study_title(summary_text)
    result = generate_result(summary_text)
    protocol = "Double-Blind RCT" if "double-blind" in summary_text.lower() else "Observational" if "real-life" in summary_text.lower() else "Unspecified"
    product = extract_product(summary_text)
    dosage = "320 mg" if "320 mg" in summary_text else "Not specified"
    summary = summary_text.strip().replace("\n", " ")
    notes = ""

    return f"{name}\t\t\t{result}\t{protocol}\t{product}\t{summary}\t{dosage}\t{notes}"

# === Example usage ===
if __name__ == "__main__":
    summary_input = """Paste your full SciSummary output here..."""

    print("\n📋 Tab-separated Excel row:\n")
    print(parse_summary(summary_input))

