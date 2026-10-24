# document-automator/create_documents.py
# Helper script: creates the sample input PDFs in the 'documents' folder.
# Requires: pip install reportlab
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "documents")
os.makedirs(BASE, exist_ok=True)

ARTICLE_PAGES = [
    [
        ("Introduction to Automation", 16),
        ("", 11),
        ("Automation is the creation and application of technology to produce and deliver goods", 11),
        ("and services with minimal human intervention. The implementation of automation", 11),
        ("technologies, techniques, and processes improves the efficiency, reliability, and speed", 11),
        ("of many tasks that were previously performed manually.", 11),
        ("", 11),
        ("This leads to increased productivity, reduced costs, and improved quality.", 11),
    ],
    [
        ("Benefits of Automation", 16),
        ("", 11),
        ("1. Increased Efficiency: Tasks are completed faster and with higher throughput.", 11),
        ("2. Cost Reduction: Lower labor costs and reduced waste.", 11),
        ("3. Improved Accuracy: Minimizes human error.", 11),
        ("4. Enhanced Safety: Dangerous tasks can be automated.", 11),
        ("5. Greater Consistency: Uniform quality in output.", 11),
        ("", 11),
        ("Conclusion", 16),
        ("", 11),
        ("Automation is transforming industries globally. Embracing these technologies is", 11),
        ("crucial for future competitiveness.", 11),
    ],
]


def write_pdf(path, pages):
    c = canvas.Canvas(path, pagesize=A4)
    _, height = A4
    for lines in pages:
        y = height - 72
        for text, size in lines:
            c.setFont("Helvetica-Bold" if size > 11 else "Helvetica", size)
            c.drawString(72, y, text)
            y -= size + 8
        c.showPage()
    c.save()
    print(f"Created: {path}")


write_pdf(os.path.join(BASE, "input_article.pdf"), ARTICLE_PAGES)
write_pdf(os.path.join(BASE, "dummy_doc1.pdf"), [[("This is Dummy Document 1 for merging test.", 11)]])
write_pdf(os.path.join(BASE, "dummy_doc2.pdf"), [[("This is Dummy Document 2 for merging test.", 11)]])
