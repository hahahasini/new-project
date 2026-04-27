import sys
try:
    import docx
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'python-docx'])
    import docx

try:
    from PyPDF2 import PdfReader
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyPDF2'])
    from PyPDF2 import PdfReader

def extract_docx(filepath, out_file):
    out_file.write("--- DOCX CONTENT ---\n")
    doc = docx.Document(filepath)
    for para in doc.paragraphs:
        if para.text.strip():
            out_file.write(f"Style: {para.style.name} | Text: {para.text}\n")

def extract_pdf(filepath, out_file):
    out_file.write("\n--- PDF CONTENT ---\n")
    reader = PdfReader(filepath)
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            out_file.write(f"Page {i+1}:\n{text}\n\n")

if __name__ == '__main__':
    with open('extracted_text.txt', 'w', encoding='utf-8') as f:
        extract_docx('template.docx', f)
        extract_pdf('original repo documentation.pdf', f)
