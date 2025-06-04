import streamlit as st
import fitz  # PyMuPDF
import re

st.title("📄 Carrier Report Analyzer")
st.write("Upload one or more carrier PDF reports to extract key metrics.")

carrier_files = st.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

def extract_metrics_from_text(text):
    loss = re.search(r"Loss Ratio[:\s]+(\-?\d+\.?\d*)%", text, re.IGNORECASE)
    growth = re.search(r"Growth[:\s]+(\-?\d+\.?\d*)%", text, re.IGNORECASE)
    retention = re.search(r"Retention[:\s]+(\-?\d+\.?\d*)%", text, re.IGNORECASE)
    return {
        "Loss Ratio": f"{loss.group(1)}%" if loss else "Not found",
        "Growth %": f"{growth.group(1)}%" if growth else "Not found",
        "Retention %": f"{retention.group(1)}%" if retention else "Not found",
    }

def detect_carrier_name(text):
    known_carriers = ["Texas Mutual", "FCCI", "Liberty Mutual", "Hanover", "EMC", "BITCO"]
    for carrier in known_carriers:
        if carrier.lower() in text.lower():
            return carrier
    return "Unknown Carrier"

if carrier_files:
    st.success(f"{len(carrier_files)} file(s) uploaded.")
    for file in carrier_files:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = "\n".join(page.get_text() for page in doc)
        carrier = detect_carrier_name(text)
        metrics = extract_metrics_from_text(text)

        st.markdown(f"### 📘 {carrier}")
        st.markdown(f"- **Loss Ratio:** {metrics['Loss Ratio']}")
        st.markdown(f"- **Retention %:** {metrics['Retention %']}")
        st.markdown(f"- **Growth %:** {metrics['Growth %']}")
