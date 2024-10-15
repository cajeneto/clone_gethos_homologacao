from django.shortcuts import render
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests



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
    return render(request, 'home.html')



def create_account(request):
    return render(request, 'create_account.html')



def dashboard_auth(request):
        
    return render(request, 'dashboard_auth.html', context= {
        'listContacts': contatos,
    })





# configuração de url para login de usuário
def login_user(request):
    return HttpResponse('teste login usuário')



# configuração de url para login de administrador
def login_admin(request):
    return HttpResponse('teste login administrador')
 



