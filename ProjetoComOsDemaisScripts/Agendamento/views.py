from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from .models import Senai, Salas, Agendamentos
from .forms import formCadastroUsuario, FormLogin, SalaForm, AdicionarSalaForm, FormAgendamentosSala
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        
        if not username or not email or not password or not first_name or not last_name:
            return Response({"error": "Todos os campos são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Nome de usuário já está em uso."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email já está em uso."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        return Response({"message": "Usuário criado com sucesso."}, status=status.HTTP_201_CREATED)


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not username or not email or not password:
            return Response({"error": "Todos os campos são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Nome de usuário já está em uso."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email já está em uso."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({"message": "Usuário criado com sucesso."}, status=status.HTTP_201_CREATED)

class ObtainTokenView(TokenObtainPairView):
    pass

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = super().post(request, *args, **kwargs).data
        return Response({
            'access': tokens['access'],
            'refresh': tokens['refresh'],
            'user_id': user.id,  # Exemplo de retorno de informações do usuário
            'username': user.username,
            # Adicione outros dados do usuário que você deseja retornar
        })

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)):
                return True
        return False
    return user_passes_test(in_groups)

@login_required
@group_required('Coordenador')
def homepageAdmin(request):
    if not request.user.groups.filter(name='Coordenador').exists():
        return redirect('/')

    if request.method == 'POST':
        if 'delete' in request.POST:
            ids_to_delete = request.POST.getlist('selected_ids')[0].split(',')
            ids_to_delete = [int(id) for id in ids_to_delete]   
            Salas.objects.filter(id__in=ids_to_delete).delete()
            return redirect('/homepageAdmin')

        form = AdicionarSalaForm(request.POST)
        if form.is_valid():
            sala = form.save(commit=False)
            sala.agendamento = 'Disponível'  # Define a disponibilidade padrão
            sala.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"message": "Sala adicionada com sucesso!"})
            return redirect('/homepageAdmin')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"errors": form.errors}, status=400)
    else:
        form = AdicionarSalaForm()

    context = {
        'dadosSenai': Senai.objects.all(),
        'dadosSalas': Salas.objects.all(),
        'form': form
    }
    return render(request, 'homepageAdmin.html', context)


@login_required
@group_required('Professor')
def homepageProfessor(request):
    if not request.user.groups.filter(name='Professor').exists():
        return redirect('/')

    if request.method == 'POST':
        if 'delete' in request.POST:
            ids_to_delete = request.POST.getlist('selected_ids')[0].split(',')
            ids_to_delete = [int(id) for id in ids_to_delete]
            Agendamentos.objects.filter(id__in=ids_to_delete).delete()
            return redirect('/homepageProfessor')

        form = FormAgendamentosSala(request.POST)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.agendado_por = request.user  # Atribui o usuário logado
            agendamento.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"message": "Agendamento realizado com sucesso!"})
            return redirect('/homepageProfessor')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"errors": form.errors}, status=400)
    else:
        form = FormAgendamentosSala()

    context = {
        'dadosSenai': Senai.objects.all(),
        'dadosSalas': Salas.objects.all(),
        'form': form
    }
    return render(request, 'homepageProfessor.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')

def homepage(request):
    context = {}
    dadosSenai = Senai.objects.all()
    context["dadosSenai"] = dadosSenai
    return render(request, 'homepage.html', context)

def cadastroUsuario(request):
    context = {}
    dadosSenai = Senai.objects.all()
    context["dadosSenai"] = dadosSenai
    if request.method == 'POST':
        form = formCadastroUsuario(request.POST)
        if form.is_valid():
            var_nome = form.cleaned_data['first_name']
            var_sobrenome = form.cleaned_data['last_name']
            var_usuario = form.cleaned_data['user']
            var_email = form.cleaned_data['email']
            var_senha = form.cleaned_data['password']

            user = User.objects.create_user(username=var_usuario, email=var_email, password=var_senha)
            user.first_name = var_nome
            user.last_name = var_sobrenome
            user.save()
            return redirect('/login')
    else:
        form = formCadastroUsuario()
        context['form'] = form
    return render(request, 'cadastroUsuario.html', context)

def login(request):
    context = {}
    dadosSenai = Senai.objects.all()
    context["dadosSenai"] = dadosSenai
    if request.method == 'POST':
        form = FormLogin(request.POST)
        if form.is_valid():
            var_usuario = form.cleaned_data['user']
            var_senha = form.cleaned_data['password']
            
            user = authenticate(username=var_usuario, password=var_senha)

            if user is not None:
                auth_login(request, user)
                if user.groups.filter(name='Coordenador').exists():
                    return redirect('/homepageAdmin')
                elif user.groups.filter(name='Professor').exists():
                    return redirect('/homepageProfessor')
                else:
                    return redirect('/')
            else:
                print('Login falhou')
    else:
        form = FormLogin()
        context['form'] = form
    return render(request, 'login.html', context)

def faq(request):
    context = {}
    dadosSenai = Senai.objects.all()
    context["dadosSenai"] = dadosSenai
    return render(request, 'faq.html', context)

def faqAdmin(request):
    context = {}
    dadosSenai = Senai.objects.all()
    context["dadosSenai"] = dadosSenai
    return render(request, 'faqAdmin.html', context)

def faqProfessor(request):
    context = {}
    dadosSenai = Senai.objects.all()
    context["dadosSenai"] = dadosSenai
    return render(request, 'faqProfessor.html', context)

def perfil(request):
    return render(request, 'perfil.html')

def salas(request):
    context = {}
    return render(request, 'salas.html', context)


def detalhes(request):
    context = {}
    return render(request, 'detalhes.html', context)