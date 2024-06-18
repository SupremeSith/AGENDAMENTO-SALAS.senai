from django.urls import path
from . import views
from .views import ObtainTokenView
from .views import SignupView

urlpatterns = [
    path('', views.homepage, name="home"),         # Inclui as urls do app blog
    path('cadastroUsuario', views.cadastroUsuario, name='cadastroUsuario'),
    path('login', views.login, name='login'),
    path('faq', views.faq, name="faq"),
    path('faqAdmin', views.faqAdmin, name="faqAdmin"),
    path('faqProfessor', views.faqProfessor, name="faqProfessor"),
    path('homepageAdmin', views.homepageAdmin, name='homepageAdmin'),
    path('homepageProfessor', views.homepageProfessor, name='homepageProfessor'),
    path('logout', views.logout_view, name='logout'),
    path('api/token/', ObtainTokenView.as_view(), name='token_obtain'),
    path('api/signup/', SignupView.as_view(), name='signup'),   
    path('perfil/', views.perfil, name="perfil"),
    path('salas/', views.salas, name="salas"),
    path('detalhes/', views.detalhes, name='detalhes'),
]
