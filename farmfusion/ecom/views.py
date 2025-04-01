from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from businessmodel.models import InvestmentModel
# Create your views here.

def index(request):
    top_three_required = InvestmentModel.objects.order_by('-requiredamount')[:3]

    for proj in top_three_required:
        if proj.requiredamount > 0:
            proj.progress = min(int(( proj.requiredamount/proj.capital ) * 100), 100)
        else:
            proj.progress = 0  # Avoid division by zero

    return render(request, 'index.html', {"top": top_three_required})

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

