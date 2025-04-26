from django.urls import path
from . import views

urlpatterns = [
    path('disciplinas/', views.lista_disciplinas, name='lista_disciplinas'),
    path('disciplinas/<int:pk>/', views.detalhes_disciplina, name='detalhes_disciplina'),
    path('disciplinas/<int:pk>/avaliar/', views.avaliar_disciplina, name='avaliar_disciplina'),
    path('avaliacao/<int:pk>/editar/', views.editar_avaliacao, name='editar_avaliacao'),
    path('avaliacao/<int:pk>/excluir/', views.excluir_avaliacao, name='excluir_avaliacao'),
]