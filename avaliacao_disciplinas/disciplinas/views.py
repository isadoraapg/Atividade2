from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from .models import Disciplina, Avaliacao
from .forms import AvaliacaoForm

@login_required
def lista_disciplinas(request):
    disciplinas = Disciplina.objects.all()
    return render(request, 'disciplinas/lista_disciplinas.html', {
        'disciplinas': disciplinas
    })

@login_required
def detalhes_disciplina(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk)
    avaliacoes = disciplina.avaliacao_set.all()
    ja_avaliou = disciplina.avaliacao_set.filter(aluno=request.user).exists()
    
    return render(request, 'disciplinas/detalhes_disciplina.html', {
        'disciplina': disciplina,
        'avaliacoes': avaliacoes,
        'ja_avaliou': ja_avaliou
    })

@login_required
def avaliar_disciplina(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk)
    
    # Verificar se o aluno já avaliou esta disciplina
    if Avaliacao.objects.filter(disciplina=disciplina, aluno=request.user).exists():
        messages.error(request, "Você já avaliou esta disciplina.")
        return redirect('detalhes_disciplina', pk=pk)
    
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            try:
                avaliacao = form.save(commit=False)
                avaliacao.disciplina = disciplina
                avaliacao.aluno = request.user
                avaliacao.save()
                messages.success(request, "Avaliação registrada com sucesso!")
                return redirect('detalhes_disciplina', pk=pk)
            except IntegrityError:
                messages.error(request, "Você já avaliou esta disciplina.")
    else:
        form = AvaliacaoForm()
    
    return render(request, 'disciplinas/avaliar_disciplina.html', {
        'form': form,
        'disciplina': disciplina
    })

@login_required
def editar_avaliacao(request, pk):
    avaliacao = get_object_or_404(Avaliacao, pk=pk)
    
    # Verificar se o usuário é o autor da avaliação
    if avaliacao.aluno != request.user:
        return HttpResponseForbidden("Você não tem permissão para editar esta avaliação.")
    
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST, instance=avaliacao)
        if form.is_valid():
            form.save()
            messages.success(request, "Avaliação atualizada com sucesso!")
            return redirect('detalhes_disciplina', pk=avaliacao.disciplina.pk)
    else:
        form = AvaliacaoForm(instance=avaliacao)
    
    return render(request, 'disciplinas/editar_avaliacao.html', {
        'form': form,
        'avaliacao': avaliacao
    })

@login_required
def excluir_avaliacao(request, pk):
    avaliacao = get_object_or_404(Avaliacao, pk=pk)
    
    # Verificar se o usuário é o autor da avaliação
    if avaliacao.aluno != request.user:
        return HttpResponseForbidden("Você não tem permissão para excluir esta avaliação.")
    
    disciplina_pk = avaliacao.disciplina.pk
    
    if request.method == 'POST':
        avaliacao.delete()
        messages.success(request, "Avaliação excluída com sucesso!")
        return redirect('detalhes_disciplina', pk=disciplina_pk)
    
    return render(request, 'disciplinas/confirmar_exclusao.html', {
        'avaliacao': avaliacao
    })