from django.shortcuts import render




def adicionar_contato(request):
    return render(request, 'cadastro-contato.html')


def visualizar_contato(request):
    return render(request, 'interface-contatos.html')