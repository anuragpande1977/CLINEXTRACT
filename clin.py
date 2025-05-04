def generate_study_title(summary):
    summary_lower = summary.lower()

    if "real-life clinical practice" in summary_lower or "real-world" in summary_lower:
        if "luts" in summary_lower or "bph" in summary_lower:
            return "Real-world study on LUTS/BPH treatment in clinical practice"

    if "double-blind" in summary_lower and "placebo" in summary_lower:
        if "saw palmetto" in summary_lower or "serenoa repens" in summary_lower:
            return "Double-blind placebo-controlled trial on Serenoa repens for BPH"

    if "meta-analysis" in summary_lower:
        return "Meta-analysis of treatments for BPH or LUTS"

    return "Clinical study on LUTS/BPH"

def extract_product(summary):
    if "hexanic extract" in summary.lower():
        return "Hexanic extract of Serenoa repens (HESr)"
    if "serenoa repens" in summary.lower():
        return "Serenoa repens extract"
    if "usplus" in summary.lower():
        return "USPlus®"
    return "Saw palmetto extract"

def generate_result(summary):
    if "improvement" in summary.lower() or "effective" in summary.lower():
        return "Positive for saw palmetto extract"
    return "Neutral or unclear result"

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

# === Example usage ===
if __name__ == "__main__":
    sci_summary = """
    This study evaluated the changes in symptoms and quality of life (QoL) in a large cohort of patients with moderate to severe lower urinary tract symptoms (LUTS) associated with benign prostatic hyperplasia (BPH), managed under real-life clinical practice conditions.

    The researchers found that all medical treatments, including monotherapy with alpha-blockers (AB), 5-alpha-reductase inhibitors (5ARI), or the herbal extract hexanic extract of Serenoa repens (HESr), as well as combination therapies with AB+5ARI and AB+HESr, were associated with significant improvements in both LUTS symptoms and QoL...

    In conclusion, this large, real-world study demonstrates that the various medical treatments for managing moderate to severe LUTS/BPH, including the herbal extract HESr, provide equivalent improvements in symptoms and quality of life, with the herbal extract showing a better safety profile compared to standard pharmacological therapies.
    """

    row_output = create_excel_row(sci_summary)
    print("\nExcel Row Output:\n")
    print(row_output)

