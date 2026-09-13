import fitz
import io

def extract_resume_text(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=io.BytesIO(pdf_bytes), filetype="pdf")
    pages = [page.get_text("text") for page in doc]
    return "\n".join(pages).strip()
