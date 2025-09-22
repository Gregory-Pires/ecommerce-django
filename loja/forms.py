from django import forms
from .models import NotaAvaliacao

class ReviewForm(forms.ModelForm):
    class Meta:
        model = NotaAvaliacao
        fields = ['assunto', 'avaliação', 'nota']