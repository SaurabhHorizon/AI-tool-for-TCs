import re
from docx import Document

def read_docx(file) -> str:
    doc = Document(file)
    return "\n".join(p.text for p in doc.paragraphs)

def parse_input_text(text: str):
    text = text.replace("\r", "\n")
    lines = [clean_text(l) for l in re.split(r'[\n•\-–]', text) if clean_text(l)]
    return lines

def clean_text(t: str) -> str:
    return re.sub(r'\s+', ' ', t or '').strip()
