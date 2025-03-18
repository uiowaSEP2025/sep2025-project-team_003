from django.http import HttpResponse
from rest_framework.response import Response
from fpdf import FPDF
import io
from rest_framework.decorators import api_view
from hsabackend.models.organization import Organization
from rest_framework import status   
from hsabackend.models.invoice import Invoice


@api_view(["GET"])
def generate_pdf(request, id):
    if not request.user.is_authenticated:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    org = Organization.objects.get(owning_User=request.user.pk)

    invoice_qs = Invoice.objects.filter(
        customer__organization=org.pk,
        pk = id
        )

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