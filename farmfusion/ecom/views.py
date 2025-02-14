from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def partners(request):
    return render(request, 'partners.html')

def contacts(request):
    return render(request, 'contacts.html')

def services(request):
    return render(request, 'services.html')

def privacy(request):
    return render(request, 'privacy.html')

def products(request):
    return render(request, 'products.html')