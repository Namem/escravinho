from django.urls import path
from . import views

urlpatterns = [
    path('abrir/', views.abrir_chamado, name='abrir_chamado'),
    path('listar/', views.lista_chamados, name='lista_chamados'),
    path('detalhar/<int:chamado_id>/', views.detalhar_chamado, name='detalhar_chamado'),
    path('fechar/<int:chamado_id>/', views.fechar_chamado, name='fechar_chamado'),
    path('editar/<int:chamado_id>/', views.editar_chamado, name='editar_chamado'),
    path('excluir/<int:chamado_id>/', views.excluir_chamado, name='excluir_chamado'),



]

