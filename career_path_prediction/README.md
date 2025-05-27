# Career Path Predictor 🎯

The Career Path Predictor is a smart tool that helps users identify potential career options based on their skills, interests, and educational background. By analyzing user input data, it recommends the most suitable career paths, providing insights and guidance for making informed career decisions. This project leverages machine learning techniques to improve prediction accuracy and deliver personalized suggestions.

This is a Python + Streamlit web app that predicts suitable career paths based on your resume.



## 🔧 Features
- Upload resume (PDF or DOCX)
- Extracts text and skills from the resume
- Maps skills to possible career paths

## 🛠️ Tech Stack
- Python
- Streamlit
- PDF & DOCX parsing
- Custom skill mapping logic

## 📂 Files
- `app.py`: Main Streamlit app
- `resume_parser.py`: Extracts text and skills from resumes
- `career_mapper.py`: Maps skills to careers
- `requirements.txt`: Dependencies
- `sample_resume.pdf`: Example resume

## 🚀 How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
