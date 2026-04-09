import os
import uuid
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from django.conf import settings

def generate_pdf(text: str, name: str) -> str:
    # 1. Clean Markdown (Stars hataein)
    clean_text = text.replace("**", "").replace("*", "")

    # 2. Media directory setup (Django settings use karein)
    output_dir = os.path.join(settings.MEDIA_ROOT, "applications")
    os.makedirs(output_dir, exist_ok=True)
    
    # Unique Filename
    filename = f"{name.replace(' ', '_')}_{uuid.uuid4().hex[:6]}.pdf"
    file_path = os.path.join(output_dir, filename)

    # 3. PDF Document Setup
    doc = SimpleDocTemplate(file_path, pagesize=A4,
                            rightMargin=inch, leftMargin=inch,
                            topMargin=inch, bottomMargin=inch)

    styles = getSampleStyleSheet()
    style = ParagraphStyle(
        'Custom',
        parent=styles['Normal'],
        fontSize=12,
        leading=18,  # Line spacing thori kam ki hai professional look ke liye
        spaceAfter=12,
    )

    # 4. Content Build
    content = []
    for line in clean_text.split('\n'):
        if line.strip():
            content.append(Paragraph(line, style))
        else:
            # Khali line ke liye thora sa spacer
            content.append(Spacer(1, 12))

    doc.build(content)
    
    # 5. Return Relative Path
    return f"applications/{filename}"