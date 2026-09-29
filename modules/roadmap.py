import pandas as pd
import random

def generate_roadmap(missing_skills, coursera_data_path):
    """
    Cross-references missing skills with coursea_data.csv to recommend 3 specific courses.
    """
    try:
        df = pd.read_csv(coursera_data_path)
    except Exception as e:
        print(f"Error loading course data: {e}")
        return []
        
    recommendations = []
    
    import re
    if df.empty:
        return recommendations
        
    for skill in missing_skills:
        skill_lower = skill.lower()
        escaped_skill = re.escape(skill_lower)
        # Search for skill in course title
        matches = df[df['course_title'].str.lower().str.contains(escaped_skill, na=False, regex=True)]
        
        if not matches.empty:
            top_course = matches.iloc[0]
            recommendations.append({
                "skill": skill,
                "course_title": top_course.get('course_title', 'Unknown Course'),
                "organization": top_course.get('course_organization', 'Coursera'),
                "difficulty": top_course.get('course_difficulty', 'Mixed'),
                "link": top_course.get('link', f"https://www.coursera.org/search?query={skill.replace(' ', '%20')}")
            })
        else:
            # Fallback if no exact course matches the skill
            random_course = df.sample(1).iloc[0]
            recommendations.append({
                "skill": skill,
                "course_title": random_course.get('course_title', f'{skill} Fundamentals'),
                "organization": random_course.get('course_organization', 'Coursera'),
                "difficulty": random_course.get('course_difficulty', 'Beginner'),
                "link": random_course.get('link', f"https://www.coursera.org/search?query={skill.replace(' ', '%20')}")
            })
            
    # Limit to 3 specific courses
    return recommendations[:3]
