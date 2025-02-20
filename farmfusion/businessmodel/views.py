from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
def myinvestment(request):
    return render(request,"myinvestment.html")
def myprojects(request):
    return render(request,"myprojects.html")
