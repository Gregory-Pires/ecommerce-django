from django import forms
from .models import NotaAvaliacao

class ReviewForm(forms.ModelForm):
    model = NotaAvaliacao
    fields = ['assunto', 'avaliação', 'nota']