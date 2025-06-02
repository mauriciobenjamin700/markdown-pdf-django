import io
import os
import tempfile
import zipfile
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .backend.conversor import markdown_to_pdf

@csrf_exempt  # Remova em produção, use o CSRF corretamente!
def markdown_to_pdf_view(request):
    """
    Converte um arquivo Markdown enviado via POST para PDF e retorna o PDF como resposta HTTP.
    """
    if request.method == "POST" and request.FILES.get("markdown_file"):
        md_file = request.FILES["markdown_file"]
        output_name = request.POST.get("output_name", "output.pdf")
        pdf_buffer = io.BytesIO()

        # Salva o arquivo markdown temporariamente
        temp_md_path = "/tmp/uploaded.md"
        with open(temp_md_path, "wb") as f:
            f.write(md_file.read())


        # Gera o PDF no buffer
        markdown_to_pdf(
            md_file_path=temp_md_path,
            pdf_file_path=pdf_buffer
        )
        pdf_buffer.seek(0)
        response = HttpResponse(pdf_buffer, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{output_name}.pdf"'
        return response

    return render(request, "converter/upload.html")


@csrf_exempt
def markdown_zipped_to_pdf_view(request):
    """
    Converte um arquivo Markdown dentro de um ZIP enviado via POST para PDF e retorna o PDF como resposta HTTP.
    O ZIP deve conter um único arquivo Markdown (.md).
    Se houver mais de um arquivo Markdown, o primeiro encontrado será usado.
    Se não houver arquivo Markdown, retorna um erro 400.
    Se o ZIP não for enviado, renderiza a página de upload.
    """
    if request.method == "POST" and request.FILES.get("zip_file"):
        zip_file = request.FILES["zip_file"]
        output_name = request.POST.get("output_name", "output.pdf")
        pdf_buffer = io.BytesIO()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Extrair ZIP
            zip_path = os.path.join(temp_dir, "upload.zip")
            with open(zip_path, 'wb') as f:
                for chunk in zip_file.chunks():
                    f.write(chunk)
            
            # Descompactar
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Encontrar arquivo markdown
            markdown_file = None
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith('.md'):
                        markdown_file = os.path.join(root, file)
                        break
                if markdown_file:
                    break
            
            if markdown_file:
                # Gerar PDF
                markdown_to_pdf(
                    md_file_path=markdown_file,
                    pdf_file_path=pdf_buffer
                )
                
                pdf_buffer.seek(0)
                response = HttpResponse(pdf_buffer, content_type="application/pdf")
                response["Content-Disposition"] = f'attachment; filename="{output_name}.pdf"'
                return response
            else:
                return HttpResponse("Nenhum arquivo markdown encontrado no ZIP", status=400)

    return render(request, "converter/upload_zip.html")