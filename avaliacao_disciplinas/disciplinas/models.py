from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20)
    descricao = models.TextField(blank=True)
    professor = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}"
    
    def media_avaliacoes(self):
        avaliacoes = self.avaliacao_set.all()
        if avaliacoes:
            return sum(av.nota for av in avaliacoes) / len(avaliacoes)
        return 0
    
    def total_avaliacoes(self):
        return self.avaliacao_set.count()

class Avaliacao(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField(blank=True)
    anonimo = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['disciplina', 'aluno']
    
    def __str__(self):
        return f"Avaliação de {self.aluno.username} para {self.disciplina.nome}"