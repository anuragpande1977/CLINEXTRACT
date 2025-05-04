
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

    return f"{name}\t{author}\t{year}\t{result}\t{protocol}\t{product}\t{summary_text}\t{dosage}\t{notes}"

# === Usage ===
if __name__ == "__main__":
    print("📋 Paste your SciSummary text below. Press ENTER, then Ctrl+D (Mac/Linux) or Ctrl+Z + Enter (Windows):\n")
    import sys
    sci_summary = sys.stdin.read()

    row_output = create_excel_row(sci_summary)
    print("\n✅ Copy and paste the following into Excel:\n")
    print("=" * 80)
    print(row_output)
    print("=" * 80)
    input("\n🔚 Press Enter to close after copying.")

