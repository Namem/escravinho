from django.shortcuts import render, redirect
from .forms import ChamadoForm
from django.contrib.auth.decorators import login_required
from .models import Chamado 
from django.shortcuts import get_object_or_404

@login_required
def abrir_chamado(request):
    if request.method == 'POST':
        form = ChamadoForm(request.POST)
        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.usuario = request.user
            chamado.save()
            return redirect('lista_chamados')
    else:
        form = ChamadoForm()
    
    return render(request, 'chamados/abrir_chamado.html', {'form': form})

@login_required
def lista_chamados(request):
    if request.user.groups.filter(name='Analista').exists():
        # Analista vê todos os chamados
        chamados_abertos = Chamado.objects.filter(status='aberto').order_by('-data_abertura')
        chamados_fechados = Chamado.objects.filter(status='fechado').order_by('-data_abertura')
    else:
        # Usuário comum vê apenas os próprios
        chamados_abertos = Chamado.objects.filter(usuario=request.user, status='aberto').order_by('-data_abertura')
        chamados_fechados = Chamado.objects.filter(usuario=request.user, status='fechado').order_by('-data_abertura')

    return render(request, 'chamados/lista_chamados.html', {
        'chamados_abertos': chamados_abertos,
        'chamados_fechados': chamados_fechados
    })



@login_required
def detalhar_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id, usuario=request.user)
    return render(request, 'chamados/detalhar_chamado.html', {'chamado': chamado})

@login_required
def fechar_chamado(request, chamado_id):
    # Busca o chamado que pertence ao usuário atual
    chamado = get_object_or_404(Chamado, id=chamado_id, usuario=request.user)

    # Muda o status para "fechado"
    chamado.status = 'fechado'

    # Salva a alteração no banco de dados
    chamado.save()

    # Redireciona de volta para a lista de chamados
    return redirect('lista_chamados')

@login_required
def editar_chamado(request, chamado_id):
    # Busca o chamado do usuário atual
    chamado = get_object_or_404(Chamado, id=chamado_id, usuario=request.user)

    if request.method == 'POST':
        # Atualiza o chamado com os dados do formulário
        form = ChamadoForm(request.POST, instance=chamado)
        if form.is_valid():
            form.save()
            return redirect('detalhar_chamado', chamado_id=chamado.id)
    else:
        # Preenche o formulário com os dados do chamado atual
        form = ChamadoForm(instance=chamado)
    
    # Renderiza a página de edição
    return render(request, 'chamados/editar_chamado.html', {'form': form, 'chamado': chamado})

@login_required
def excluir_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id, usuario=request.user)

    if request.method == 'POST':
        chamado.delete()
        return redirect('lista_chamados')
    
    return render(request, 'chamados/excluir_chamado.html', {'chamado': chamado})
