# career_mapper.py

def map_career(skills):
    career_paths = {
        "Data Scientist": ["python", "machine learning", "data analysis", "tensorflow", "sql"],
        "Web Developer": ["html", "css", "javascript", "react", "django", "flutter"],
        "Cloud Engineer": ["cloud", "aws"],
        "Project Manager": ["excel", "project management"],
        "Software Developer": ["java", "c++", "python"]
    }

    matched_careers = []

    for career, needed_skills in career_paths.items():
        if any(skill in skills for skill in needed_skills):
            matched_careers.append(career)

    return matched_careers
