from django.db import models
from django.contrib.auth.models import User

class Setor(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Chamado(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_abertura = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('aberto', 'Aberto'),
        ('andamento', 'Em andamento'),
        ('fechado', 'Fechado'),
    ], default='aberto')
    atendido_por = models.ForeignKey(
    User, on_delete=models.SET_NULL,
    null=True, blank=True,
    related_name='chamados_atendidos'
    )


    def __str__(self):
        return f"{self.titulo} - {self.status}"
