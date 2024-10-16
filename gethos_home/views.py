from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, logout



# from django.

# Create your views here.



contatos = [

{
    "id": 1,
    'nomeContato': 'Hostílio de França',
    'email': 'netocajeh@gmail.com',
    'telefone': '5582991326715',
    'empresa': 'Gethos Tecnologia',
    'statusContato': 'Ativo',
    'score': 100,


},

{
    "id": 2,
    'nomeContato': 'Valmiram Oliveira',
    'email': 'valmiram@sefaz.gov.br',
    'telefone': '55829',
    'empresa': 'Sefaz',
    'statusContato': 'Ativo',
    'score': 100,


},
{
    "id": 3,
    'nomeContato': 'Miguel Nicolelis',
    'email': 'miguel@nasa.com',
    'telefone': '55829',
    'empresa': 'NASA TECNOLOGIA',
    'statusContato': 'Inativo',
    'score': 100,


},
{
    "id": 3,
    'nomeContato': 'Miguel Nicolelis',
    'email': 'miguel@nasa.com',
    'telefone': '55829',
    'empresa': 'NASA TECNOLOGIA',
    'statusContato': 'Inativo',
    'score': 100,


},
{
    "id": 3,
    'nomeContato': 'Miguel Nicolelis',
    'email': 'miguel@nasa.com',
    'telefone': '55829',
    'empresa': 'NASA TECNOLOGIA',
    'statusContato': 'Inativo',
    'score': 100,


},
{
    "id": 3,
    'nomeContato': 'Miguel Nicolelis',
    'email': 'miguel@nasa.com',
    'telefone': '55829',
    'empresa': 'NASA TECNOLOGIA',
    'statusContato': 'Inativo',
    'score': 100,


},
{
    "id": 3,
    'nomeContato': 'Miguel Nicolelis',
    'email': 'miguel@nasa.com',
    'telefone': '55829',
    'empresa': 'NASA TECNOLOGIA',
    'statusContato': 'Inativo',
    'score': 100,


},
{
    "id": 3,
    'nomeContato': 'Miguel Nicolelis',
    'email': 'miguel@nasa.com',
    'telefone': '55829',
    'empresa': 'NASA TECNOLOGIA',
    'statusContato': 'Inativo',
    'score': 100,


},
{
    "id": 3,
    'nomeContato': 'Miguel Nicolelis',
    'email': 'miguel@nasa.com',
    'telefone': '55829',
    'empresa': 'NASA TECNOLOGIA',
    'statusContato': 'Inativo',
    'score': 100,


},
{
    "id": 3,
    'nomeContato': 'Miguel Nicolelis',
    'email': 'miguel@nasa.com',
    'telefone': '55829',
    'empresa': 'NASA TECNOLOGIA',
    'statusContato': 'Inativo',
    'score': 100,


},
{
    "id": 3,
    'nomeContato': 'Miguel Nicolelis',
    'email': 'miguel@nasa.com',
    'telefone': '55829',
    'empresa': 'NASA TECNOLOGIA',
    'statusContato': 'Inativo',
    'score': 100,


},
{
    "id": 3,
    'nomeContato': 'Miguel Nicolelis',
    'email': 'miguel@nasa.com',
    'telefone': '55829',
    'empresa': 'NASA TECNOLOGIA',
    'statusContato': 'Inativo',
    'score': 100,


},
{
    "id": 3,
    'nomeContato': 'Miguel Nicolelis',
    'email': 'miguel@nasa.com',
    'telefone': '55829',
    'empresa': 'NASA TECNOLOGIA',
    'statusContato': 'Inativo',
    'score': 100,


},
{
    "id": 3,
    'nomeContato': 'Miguel Nicolelis',
    'email': 'miguel@nasa.com',
    'telefone': '55829',
    'empresa': 'NASA TECNOLOGIA',
    'statusContato': 'Inativo',
    'score': 100,


},
{
    "id": 3,
    'nomeContato': 'Miguel Nicolelis',
    'email': 'miguel@nasa.com',
    'telefone': '55829',
    'empresa': 'NASA TECNOLOGIA',
    'statusContato': 'Inativo',
    'score': 100,


},


]











def home(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # usuario = authenticate(request, acessoUsuario=email, password=password) # valida autenticação

        if email == 'usuario@gethos.com' and password == "senha":
            return redirect('dashboard_auth') #redireciona o usuário para o dashboard_auth (paineil inicial do crm)
        else:
            messages.error(request, 'E-mail ou senha inválidos.')
            return render(request, 'home.html')
    else:
        return render(request, 'home.html')



def create_account(request):
    return render(request, 'create_account.html')



def dashboard_auth(request):
        
    return render(request, 'dashboard_auth.html', context= {
        'listContacts': contatos,
    })





# configuração de view para logout de usuário
def logout_view(request):
    logout(request)
    return redirect('home')  # Redireciona para a página de login (ou qualquer outra página) após o logout



# configuração de url para login de administrador
def login_admin(request):
    return HttpResponse('teste login administrador')
 



