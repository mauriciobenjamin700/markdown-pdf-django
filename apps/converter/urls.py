from django.urls import path
from apps.converter.views import markdown_to_pdf_view

urlpatterns = [
    path("", markdown_to_pdf_view, name="markdown_to_pdf"),  # agora responde em /converter/
    path("upload/", markdown_to_pdf_view, name="markdown_to_pdf_upload"),
]