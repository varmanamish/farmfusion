from django.shortcuts import render
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Wallet
# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"] # username is the name of the input field in the form
        password = request.POST["password"] # password is the name of the input field in the form
        user = authenticate(request, username=username, password=password) # authenticate() is a built-in function provided by Django   
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid email or password !!"
            })
    else:
        return render(request, "login.html")

    
def logout_view(request):
    logout(request)
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        profile_img = request.FILES.get("profileimage")
        is_farmer = request.POST.get("is_farmer") == "T"  # Convert to boolean
        phno = request.POST["phone"]
        dob=request.POST["dob"]
        if CustomUser.objects.filter(username=username).exists():
                return render(request,'register.html',{"error":'Username unavailable'})
        elif CustomUser.objects.filter(email=email).exists():
                return render(request,'register.html',{"error":'Email already used'})
        elif CustomUser.objects.filter(phno=phno).exists():
                return render(request,'register.html',{"error":'phone number has been used'})
        else:
            if password != confirmation:
                return render(request, "register.html", {"message": "Passwords must match."})

            try:
                user = CustomUser.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password,
                    profile_pic=profile_img,
                    is_farmer=is_farmer,
                    phno=phno,
                    dob=dob
                )
            except IntegrityError:
                return render(request, "register.html", {"message": "Username already taken."})

            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    
    return render(request, "register.html")

@login_required
def profile(request):
    try:
        print('START')
        user_profile= request.user
        print(user_profile)
        context = {
            'profile': user_profile,
        }           
        
        print('sent')
        print(context)
        return render(request, 'profile.html', context)
    except Exception as e:
        print(e)
        return render(request,"profile.html")
@login_required
def addmoney(request):
    """Adds money to the user's wallet."""
    if request.method == "POST":
        user_wallet = request.user.wallet
        amount = int(request.POST.get("amount", 0))  

        if amount > 0:
            user_wallet.wallet_amount += amount
            user_wallet.free_amount += amount 
            user_wallet.save()
            return JsonResponse({"success": True, "message": "Money added successfully!"})
        return JsonResponse({"success": False, "message": "Invalid amount!"})

    return JsonResponse({"success": False, "message": "Invalid request method!"})

@login_required
def withdraw(request):
    if request.method == "POST":
        user_wallet = request.user.wallet
        amount = int(request.POST.get("amount", 0))

        if user_wallet.is_locked:
            return JsonResponse({"success": False, "message": "Wallet is locked!"})

        if amount > 0 and user_wallet.free_amount >= amount:
            user_wallet.wallet_amount -= amount
            user_wallet.free_amount -= amount
            user_wallet.save()
            return JsonResponse({"success": True, "message": "Withdrawal successful!"})
        
        return JsonResponse({"success": False, "message": "Insufficient funds!"})

    return JsonResponse({"success": False, "message": "Invalid request method!"})

@login_required
def check(request):
    user_wallet = request.user.wallet
    data = {
        "wallet_amount": user_wallet.wallet_amount,
        "free_amount": user_wallet.free_amount,
        "is_locked": user_wallet.is_locked,
    }
    return JsonResponse(data)
