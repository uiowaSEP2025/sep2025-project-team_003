from django.http import HttpResponse
from fpdf import FPDF
import io
from rest_framework.decorators import api_view

@api_view(["GET"])
def generate_pdf(request, id):
    # Create a PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Hello, this is a test PDF!", ln=True, align="C")

    # Save PDF to a BytesIO buffer
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)  # Reset buffer position

    # Create an HTTP response with the PDF as an attachment
    response = HttpResponse(pdf_buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="output.pdf"'  # or 'attachment;'
    
    return response