from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generate_report(name, role, score, missing_skills, roadmap, output_path):
    """
    Creates a professional PDF summarizing the gap analysis and recommended courses.
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    Story = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = styles['Heading1']
    title_style.alignment = 1 # Center
    
    h2_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Title
    Story.append(Paragraph("SkillVerseAI - Skill Gap Analysis Report", title_style))
    Story.append(Spacer(1, 20))
    
    # Candidate Info
    Story.append(Paragraph(f"<b>Candidate:</b> {name}", normal_style))
    Story.append(Paragraph(f"<b>Target Role:</b> {role}", normal_style))
    Story.append(Paragraph(f"<b>Match Score:</b> {score}%", normal_style))
    Story.append(Spacer(1, 20))
    
    # Missing Skills
    Story.append(Paragraph("<b>Identified Skill Gaps (Missing Skills):</b>", h2_style))
    if missing_skills:
        for skill in missing_skills:
            Story.append(Paragraph(f"• {skill}", normal_style))
    else:
        Story.append(Paragraph("No missing skills identified! Great match.", normal_style))
    Story.append(Spacer(1, 20))
    
    # Roadmap
    Story.append(Paragraph("<b>Recommended Learning Roadmap:</b>", h2_style))
    if roadmap:
        data = [["Target Skill", "Course Title", "Difficulty"]]
        for item in roadmap:
            data.append([item['skill'], item['course_title'], item['difficulty']])
            
        t = Table(data, colWidths=[100, 250, 100])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        Story.append(t)
    else:
        Story.append(Paragraph("No courses recommended at this time.", normal_style))
        
    doc.build(Story)
