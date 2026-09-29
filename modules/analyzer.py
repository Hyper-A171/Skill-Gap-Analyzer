import json
import os
from google import genai
from google.genai import types

def analyze_gap(extracted_skills, target_role_requirements):
    """
    Calls the Gemini model to compare extracted skills with target role requirements
    and returns a structured JSON response.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
        
    client = genai.Client()
    
    prompt = f"""
    You are an expert HR analyst and technical recruiter.
    
    Candidate's Extracted Skills: {', '.join(extracted_skills)}
    Target Role Requirements: {', '.join(target_role_requirements)}
    
    Compare the candidate's skills with the target role requirements.
    Categorize the target role requirements into three lists:
    1. 'matched': Requirements the candidate fully possesses.
    2. 'partial_match': Requirements the candidate partially possesses (e.g., has a related skill but not the exact one).
    3. 'missing': Requirements the candidate completely lacks.
    
    Also, calculate a 'match_score' from 0 to 100 representing how well the candidate fits the role.
    
    Return the output STRICTLY as a JSON object with this exact schema:
    {{
      "matched": ["skill1", "skill2"],
      "partial_match": ["skill3"],
      "missing": ["skill4", "skill5"],
      "match_score": 85
    }}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        result = json.loads(response.text)
        return result
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        # Fallback response in case of API failure
        return {
            "matched": [],
            "partial_match": [],
            "missing": target_role_requirements,
            "match_score": 0
        }
