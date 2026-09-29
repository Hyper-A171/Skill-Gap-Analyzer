import pymupdf
import spacy
import json
import re

# Load SpaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If not installed, fallback gracefully
    nlp = None

def extract_text_from_pdf(pdf_file_path):
    """
    Extracts text from a PDF file safely using PyMuPDF.
    """
    text = ""
    try:
        # Check if it's a Streamlit UploadedFile object
        if hasattr(pdf_file_path, 'read'):
            pdf_bytes = pdf_file_path.read()
            doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
        else:
            doc = pymupdf.open(pdf_file_path)
            
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_skills(text, skills_database_path):
    """
    Extracts skills from text based on keys/values in skills_database.json.
    """
    try:
        with open(skills_database_path, 'r', encoding='utf-8') as f:
            skills_db = json.load(f)
    except Exception as e:
        print(f"Error loading skills database: {e}")
        return []

    # Flatten the skills database into a set of lowercased skills
    all_skills = set()
    for category, skills in skills_db.items():
        for skill in skills:
            all_skills.add(skill.lower())

    extracted_skills = set()
    text_lower = text.lower()
    
    # Find exact matches using regex for whole words
    for skill in all_skills:
        # Escape the skill for regex to safely handle C++, C#, .NET
        escaped_skill = re.escape(skill)
        
        # Word boundary \b works for alphanumeric but might fail on C++ or .NET
        # We construct a custom boundary that supports symbols
        pattern = r'(?:^|[\s,;])' + escaped_skill + r'(?:$|[\s,;])'
        
        if re.search(pattern, text_lower):
            extracted_skills.add(skill)
            
    # Format skills back nicely
    formatted_skills = []
    for skill in extracted_skills:
        if skill in ['c++', 'c#', 'php', 'sql', 'html', 'css', 'aws', 'gcp', 'ci/cd', 'api']:
            formatted_skills.append(skill.upper())
        elif skill == 'node.js':
            formatted_skills.append('Node.js')
        elif skill == 'vue.js':
            formatted_skills.append('Vue.js')
        else:
            formatted_skills.append(skill.title())

    return formatted_skills
