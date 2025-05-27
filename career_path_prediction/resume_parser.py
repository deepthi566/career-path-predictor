# resume_parser.py
import pdfplumber
import docx

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_skills(text):
    # A simple predefined skill set
    skills_list = ["python", "java", "c++", "machine learning", "data analysis", "web development", 
                   "react", "django", "cloud", "aws", "excel", "project management", "sql", "tensorflow", "flutter"]

    extracted_skills = []
    text = text.lower()

    for skill in skills_list:
        if skill in text:
            extracted_skills.append(skill)

    return extracted_skills
