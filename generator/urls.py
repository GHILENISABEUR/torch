from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('generate/<int:document_id>/', views.generate_questions, name='generate_questions'),
]