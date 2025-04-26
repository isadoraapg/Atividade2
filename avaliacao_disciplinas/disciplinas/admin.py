from django.contrib import admin
from .models import Disciplina, Avaliacao

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'professor', 'media_avaliacoes', 'total_avaliacoes')
    search_fields = ('nome', 'codigo', 'professor')

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('disciplina', 'aluno', 'nota', 'anonimo', 'data_criacao')
    list_filter = ('disciplina', 'nota', 'anonimo')
    search_fields = ('disciplina__nome', 'aluno__username', 'comentario')