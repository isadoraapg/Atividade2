from django import forms
from .models import Avaliacao

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nota', 'comentario', 'anonimo']
        widgets = {
            'nota': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'comentario': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'nota': 'Nota (de 1 a 5)',
            'comentario': 'Comentário (opcional)',
            'anonimo': 'Manter avaliação anônima',
        }