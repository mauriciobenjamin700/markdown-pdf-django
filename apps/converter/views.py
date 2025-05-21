import io
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .backend.conversor import markdown_to_pdf

@csrf_exempt  # Remova em produção, use o CSRF corretamente!
def markdown_to_pdf_view(request):
    if request.method == "POST" and request.FILES.get("markdown_file"):
        md_file = request.FILES["markdown_file"]
        css_file = request.FILES.get("css_file")
        pdf_buffer = io.BytesIO()

        # Salva o arquivo markdown temporariamente
        temp_md_path = "/tmp/uploaded.md"
        with open(temp_md_path, "wb") as f:
            f.write(md_file.read())

        temp_css_path = None
        if css_file:
            temp_css_path = "/tmp/uploaded.css"
            with open(temp_css_path, "wb") as f:
                f.write(css_file.read())

        # Gera o PDF no buffer
        markdown_to_pdf(
            md_file_path=temp_md_path,
            pdf_file_path=pdf_buffer,
            css_file_path=temp_css_path,
        )
        pdf_buffer.seek(0)
        response = HttpResponse(pdf_buffer, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="output.pdf"'
        return response

    return render(request, "converter/upload.html")