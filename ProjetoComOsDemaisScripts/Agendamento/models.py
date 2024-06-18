from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime

class Senai(models.Model):
    titulo = models.CharField(max_length=50)
    descricao = models.TextField(max_length=1500)
    logo = models.ImageField(upload_to='logo/')

    def __str__(self):
        return self.titulo

class Usuario(models.Model):
    nome = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    idade = models.IntegerField()
    data = models.DateField(default=timezone.now)
    quartos = models.CharField(max_length=50)

class Salas(models.Model):
    salas = models.CharField(max_length=50)
    descricao = models.TextField(max_length=50)
    equipamentos = models.CharField(max_length=50)

    def __str__(self):
        return self.salas

class Agendamentos(models.Model):
    DIAS_DA_SEMANA = [
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
    ]
    
    PERIODOS = [
        ('manhaA', 'Manhã A'),
        ('manhaB', 'Manhã B'),
        ('tardeA', 'Tarde A'),
        ('tardeB', 'Tarde B'),
        ('noiteA', 'Noite A'),
    ]

    sala = models.ForeignKey(Salas, on_delete=models.CASCADE)
    dias = models.DateField(default=datetime.now)
    periodo = models.CharField(max_length=10, choices=PERIODOS)
    agendado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('sala', 'dias', 'periodo')

    def __str__(self):
        return f'{self.sala} - {self.dias} - {self.periodo}'
