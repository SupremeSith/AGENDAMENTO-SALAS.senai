from django.shortcuts import render, redirect

def home(request):
    context = {}
    return render(request, 'home.html', context)

def faq(request):
    context = {}
    return render(request, 'faq.html', context)

def perfil(request):
    return render(request, 'perfil.html')

def salas(request):
    context = {}
    return render(request, 'salas.html', context)


def detalhes(request):
    context = {}
    return render(request, 'detalhes.html', context)