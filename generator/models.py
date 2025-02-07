from django.db import models

# Create your models here.
from django.db import models

class PDFDocument(models.Model):
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class GeneratedQuestion(models.Model):
    document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE)
    question = models.TextField()
    question_type = models.CharField(max_length=50)  # QCM, Oui/Non, Réponse courte
    options = models.JSONField(default=list, blank=True)  # Pour les QCM