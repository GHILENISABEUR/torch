from transformers import pipeline, T5ForConditionalGeneration, T5Tokenizer
import PyPDF2
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from .models import PDFDocument, GeneratedQuestion

# Charger le modèle BERT-QA
qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

# Charger le modèle T5 pour la génération de questions
t5_model_name = "valhalla/t5-small-qa-qg-hl"
t5_tokenizer = T5Tokenizer.from_pretrained(t5_model_name)
t5_model = T5ForConditionalGeneration.from_pretrained(t5_model_name)

def generate_questions_with_t5(text):
    input_text = "generate questions: " + text
    input_ids = t5_tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    outputs = t5_model.generate(input_ids, max_length=100, num_return_sequences=1)
    questions = t5_tokenizer.decode(outputs[0], skip_special_tokens=True)
    return questions.split(';')  # Supposons que les questions sont séparées par des points-virgules

def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf']:
        pdf_file = request.FILES['pdf']
        file_name = default_storage.save(f"pdfs/{pdf_file.name}", pdf_file)
        document = PDFDocument.objects.create(file=file_name)
        return redirect('generate_questions', document_id=document.id)
    return render(request, 'upload.html')

def generate_questions(request, document_id):
    document = PDFDocument.objects.get(id=document_id)
    file_path = document.file.path

    # Extraire le texte du PDF
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()

    # Générer des questions avec T5
    questions = generate_questions_with_t5(text)

    # Sauvegarder les questions générées
    for question in questions:
        if question.strip():  # Ignorer les questions vides
            GeneratedQuestion.objects.create(
                document=document,
                question=question,
                question_type="Réponse courte",  # À adapter
            )

    return render(request, 'questions.html', {'questions': GeneratedQuestion.objects.filter(document=document)})