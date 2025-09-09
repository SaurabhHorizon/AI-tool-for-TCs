import streamlit as st
import pandas as pd
from core.parser import parse_input_text, read_docx
from core.generator import materialize_cases
from core.exporter import to_excel_bytes

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="AI Test Case Generator", page_icon="✅", layout="wide")
st.title("AI Test Case Generator")
st.caption("Paste BR/US or upload a file. Get categorized, exportable test cases in real time.")

input_mode = st.radio("Input Mode", ["Paste Text", "Upload File"], horizontal=True)
raw_text = ""

if input_mode == "Paste Text":
    raw_text = st.text_area("Business Requirement / User Stories", placeholder="Paste requirements here...", height=240)
else:
    uploaded = st.file_uploader("Upload .docx or .txt", type=["docx", "txt"])
    if uploaded:
        if uploaded.name.endswith(".txt"):
            raw_text = uploaded.read().decode("utf-8", errors="ignore")
        else:
            raw_text = read_docx(uploaded)

style = st.selectbox("Output Style", ["Manual", "Gherkin (Given-When-Then)"])
generate = st.button("Generate Test Cases")

if generate and raw_text.strip():
    reqs = parse_input_text(raw_text)
    df = materialize_cases(reqs, style)

    st.success(f"Generated {len(df)} test cases from {len(reqs)} requirements")
    st.dataframe(df, use_container_width=True)

    # Download buttons
    st.download_button("⬇️ Download CSV", df.to_csv(index=False).encode("utf-8"),
                       file_name="testcases.csv", mime="text/csv")

    st.download_button("⬇️ Download Excel", to_excel_bytes(df),
                       file_name="testcases.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
