from django.shortcuts import render
from django.http import HttpResponse
# from django.

# Create your views here.


def home(request):
    return render(request, 'home.html')



def create_account(request):
    return render(request, 'create_account.html')



def dashboard_auth(request):
    return render(request, 'dashboard_auth.html')




# configuração de url para login de usuário
def login_user(request):
    return HttpResponse('teste login usuário')



# configuração de url para login de administrador
def login_admin(request):
    return HttpResponse('teste login administrador')





