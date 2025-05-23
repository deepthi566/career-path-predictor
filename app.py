# app.py
import streamlit as st
import os
from resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_skills
from career_mapper import map_career

st.set_page_config(page_title="Career Path Predictor", page_icon="🚀")

st.title("🚀 Career Path Predictor based on Resume")

uploaded_file = st.file_uploader("Upload your Resume", type=["pdf", "docx"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Extract text
    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(uploaded_file.name)
    elif uploaded_file.name.endswith(".docx"):
        resume_text = extract_text_from_docx(uploaded_file.name)
    else:
        st.error("Unsupported file format.")
        resume_text = ""

    # Delete after reading
    os.remove(uploaded_file.name)

    if resume_text:
        st.subheader("📄 Extracted Resume Text")
        st.text_area("", resume_text, height=200)

        # Extract skills
        skills = extract_skills(resume_text)
        st.subheader("🛠 Extracted Skills")
        st.write(skills)

        # Predict careers
        careers = map_career(skills)
        st.subheader("🎯 Recommended Career Paths")
        if careers:
            for career in careers:
                st.success(career)
        else:
            st.warning("No clear career path found. Please update your resume with more skills!")

