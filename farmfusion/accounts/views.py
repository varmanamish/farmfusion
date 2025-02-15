from django.shortcuts import render
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.db import IntegrityError
from django.urls import reverse

# Create your views here.
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"] # username is the name of the input field in the form
        password = request.POST["password"] # password is the name of the input field in the form
        user = authenticate(request, username=username, password=password) # authenticate() is a built-in function provided by Django
        # If authentication successful, log user in
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        # Else, return login page again with new context
        else:
            return render(request, "login.html", {
                "message": "Invalid email or password !!"
            })
    # If method is GET, return login page
    else:
        return render(request, "login.html")

    
def logout_view(request):
    logout(request)
    return render(request, "logout.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        profile_img = request.FILES.get("profileimage")
        is_farmer = request.POST.get("is_farmer") == "T"  # Convert to boolean

        if password != confirmation:
            return render(request, "register.html", {"message": "Passwords must match."})

        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                profile_pic=profile_img,
                is_farmer=is_farmer
            )
        except IntegrityError:
            return render(request, "register.html", {"message": "Username already taken."})

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "register.html")

    
def profile(request):
    return render(request, "profile.html")