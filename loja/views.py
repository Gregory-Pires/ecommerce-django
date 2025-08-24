from django.shortcuts import render

# Create your views here.

def loja(request):
    return render(request, 'loja/loja.html')