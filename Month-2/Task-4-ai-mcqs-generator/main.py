import os
import json
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from pypdf import PdfReader

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"  
)

prompt = PromptTemplate(
    template="""
You are a strict JSON generator.

Generate {num} MCQs from the following content.
Difficulty level: {difficulty}

Content:
{content}

Rules:
- Return ONLY valid JSON.
- Do NOT add numbering like 0:, 1:
- Do NOT add explanation text.
- Output must be a pure JSON array.

Format example:

[
  {{
    "question": "Sample question?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Option A"
  }}
]
""",
    input_variables=["content", "num", "difficulty"]
)

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def generate_mcqs(content, num, difficulty):
    formatted_prompt = prompt.format(
        content=content[:3000],  # limit tokens
        num=num,
        difficulty=difficulty
    )

    response = llm.invoke(formatted_prompt)
    raw_content = response.content.strip()

    # Remove markdown code blocks
    raw_content = re.sub(r"```json|```", "", raw_content)

    # Remove index numbering like 0:
    raw_content = re.sub(r'\d+:\s*{', '{', raw_content)

    try:
        mcqs = json.loads(raw_content)
        return mcqs
    except Exception as e:
        print("Parsing Error:", e)
        print("RAW RESPONSE:\n", raw_content)
        return []
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import ListFlowable, ListItem
from reportlab.lib.pagesizes import A4
from reportlab.platypus import PageBreak

def generate_pdf(mcqs, filename="question_paper.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    question_style = styles["Normal"]

    elements.append(Paragraph("<b>MCQs Question Paper</b>", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    for i, mcq in enumerate(mcqs, 1):
        elements.append(Paragraph(f"Q{i}. {mcq['question']}", question_style))
        elements.append(Spacer(1, 0.2 * inch))

        for idx, option in enumerate(mcq["options"]):
            letter = chr(65 + idx)
            elements.append(Paragraph(f"{letter}) {option}", question_style))

        elements.append(Spacer(1, 0.4 * inch))

    elements.append(PageBreak())
    elements.append(Paragraph("<b>Answer Key</b>", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    for i, mcq in enumerate(mcqs, 1):
        correct_letter = chr(65 + mcq["options"].index(mcq["answer"]))
        elements.append(Paragraph(f"Q{i}: {correct_letter}", question_style))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)
    return filename        
