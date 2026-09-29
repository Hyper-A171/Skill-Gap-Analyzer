import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

from modules.preprocessing import clean_text
from modules.extractor import extract_text_from_pdf, extract_skills
from modules.analyzer import analyze_gap
from modules.roadmap import generate_roadmap
from modules.pdf_generator import generate_report

# Page Config
st.set_page_config(page_title="SkillVerseAI", layout="wide", page_icon="🚀")

# Load CSS
def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

try:
    load_css("assets/style.css")
except Exception:
    pass

st.title("SkillVerseAI – AI-Powered Skill Gap Analyzer")
st.markdown("Analyze your resume against your dream role and get a personalized learning roadmap.")

# Load Datasets
@st.cache_data
def load_job_roles(path="datasets/job_roles.csv"):
    try:
        df = pd.read_csv(path)
        return df
    except Exception:
        return pd.DataFrame()

job_roles_df = load_job_roles()
if not job_roles_df.empty:
    roles_list = job_roles_df['Job Title'].unique().tolist()
else:
    roles_list = ["Software Engineer", "Data Scientist", "Product Manager"]

# Sidebar
with st.sidebar:
    st.header("Candidate Profile")
    candidate_name = st.text_input("Name", "John Doe")
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    
    target_role = st.selectbox("Select Target Role", roles_list)
    
    st.markdown("---")
    st.header("Settings")
    env_api_key = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6IC-6r_nazYfud8ZFOMthHG-TB_1iLQBBJxdmssN4pLpQ")
    api_key = st.text_input("Gemini API Key", type="password", value=env_api_key)

# Main Logic
if st.button("Generate Analysis"):
    if not uploaded_file:
        st.error("Please upload a PDF resume first.")
    elif not api_key:
        st.error("Please provide your Gemini API Key in the sidebar.")
    else:
        with st.spinner("Analyzing your profile..."):
            # Set API Key
            os.environ["GEMINI_API_KEY"] = api_key
            
            # Get target role requirements
            target_skills = []
            if not job_roles_df.empty:
                role_data = job_roles_df[job_roles_df['Job Title'] == target_role]
                if not role_data.empty:
                    skills_str = role_data.iloc[0]['Required Skills']
                    target_skills = [s.strip() for s in skills_str.split('|')]
            
            if not target_skills:
                target_skills = ["Python", "Machine Learning", "Communication", "Data Analysis"] # Fallback
            
            # 1. Extract Text
            raw_text = extract_text_from_pdf(uploaded_file)
            clean_resume_text = clean_text(raw_text)
            
            # 2. Extract Skills
            extracted_skills = extract_skills(clean_resume_text, "datasets/skills_database.json")
            
            # 3. Analyze Gap
            analysis_result = analyze_gap(extracted_skills, target_skills)
            
            match_score = analysis_result.get("match_score", 0)
            matched = analysis_result.get("matched", [])
            partial = analysis_result.get("partial_match", [])
            missing = analysis_result.get("missing", [])
            
            # Display Score
            st.markdown(f"<div class='metric-card'><h2>Overall Match Score</h2><h1>{match_score}%</h1></div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Display Skills in Columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("✅ Matched Skills")
                for skill in matched:
                    st.markdown(f"<span class='skill-pill matched-skill'>{skill}</span>", unsafe_allow_html=True)
                    
            with col2:
                st.subheader("⚠️ Partial Match")
                for skill in partial:
                    st.markdown(f"<span class='skill-pill partial-skill'>{skill}</span>", unsafe_allow_html=True)
                    
            with col3:
                st.subheader("❌ Missing Skills")
                for skill in missing:
                    st.markdown(f"<span class='skill-pill missing-skill'>{skill}</span>", unsafe_allow_html=True)
                    
            st.markdown("---")
            
            # 4. Generate Roadmap
            st.header("📚 Recommended Learning Roadmap")
            roadmap = generate_roadmap(missing, "datasets/coursea_data.csv")
            
            if roadmap:
                for course in roadmap:
                    st.info(f"**Target Skill:** {course['skill']}  \n**Course:** [{course['course_title']}]({course['link']}) by *{course['organization']}*  \n**Difficulty:** {course['difficulty']}")
            else:
                st.success("No critical skill gaps identified! You are highly qualified for this role.")
                
            # 5. PDF Generation
            pdf_path = f"analysis_report.pdf"
            generate_report(candidate_name, target_role, match_score, missing, roadmap, pdf_path)
            
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📄 Download Analysis Report",
                    data=pdf_file,
                    file_name=f"{candidate_name.replace(' ', '_')}_SkillGapAnalysis.pdf",
                    mime="application/pdf"
                )
