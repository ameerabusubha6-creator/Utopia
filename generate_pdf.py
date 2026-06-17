import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

def markdown_to_pdf(md_path, pdf_path):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Define custom premium styles (Utopia branding)
    title_style = ParagraphStyle(
        'UtopiaTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#7c3aed'), # Violet
        spaceAfter=15
    )
    
    h2_style = ParagraphStyle(
        'UtopiaH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#4f46e5'), # Indigo
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'UtopiaBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1e293b'), # Dark Slate
        spaceAfter=8
    )
    
    code_style = ParagraphStyle(
        'UtopiaCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0f172a'),
    )
    
    bullet_style = ParagraphStyle(
        'UtopiaBullet',
        parent=body_style,
        leftIndent=20,
        firstLineIndent=-10,
        spaceAfter=4
    )

    story = []
    
    # Split content into parts (handling code blocks separately)
    # Match markdown code blocks: ```[lang] ... ```
    parts = re.split(r'(```[\s\S]*?```)', content)
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        if part.startswith('```'):
            # Code block processing
            lines = part.strip('`').strip().split('\n')
            # Check if first line is language specifier (like json, bash, etc.)
            if lines and lines[0] in ['json', 'bash', 'powershell', 'python']:
                lines = lines[1:]
            
            code_text = "<br/>".join([line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;') for line in lines])
            p_code = Paragraph(code_text, code_style)
            
            # Wrap code block inside a table with a background color for nice formatting
            t = Table([[p_code]], colWidths=[doc.width])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
                ('PADDING', (0,0), (-1,-1), 8),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ]))
            story.append(t)
            story.append(Spacer(1, 10))
        else:
            # Regular text parsing
            lines = part.split('\n')
            for line in lines:
                line_str = line.strip()
                if not line_str:
                    continue
                
                # Check for Horizontal Rule
                if line_str == '---':
                    story.append(Spacer(1, 8))
                    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceBefore=5, spaceAfter=15))
                    continue
                
                # Check for Headers
                if line_str.startswith('# '):
                    title_text = line_str[2:]
                    story.append(Paragraph(title_text, title_style))
                elif line_str.startswith('## '):
                    h2_text = line_str[3:]
                    story.append(Paragraph(h2_text, h2_style))
                elif line_str.startswith('- ') or line_str.startswith('* '):
                    # List item
                    text = line_str[2:]
                    # Convert markdown bold to html bold inside paragraph
                    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
                    story.append(Paragraph(f"&bull; {text}", bullet_style))
                else:
                    # Regular paragraph
                    # Convert markdown bold to html bold
                    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line_str)
                    story.append(Paragraph(text, body_style))
            
            story.append(Spacer(1, 6))

    doc.build(story)
    print(f"PDF successfully generated at: {pdf_path}")

if __name__ == "__main__":
    markdown_to_pdf("WRITEUP.md", "Utopia_Studio_Marketing_Agent_Writeup.pdf")
