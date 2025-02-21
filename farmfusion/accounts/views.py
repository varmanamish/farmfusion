from django.shortcuts import render,redirect
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Wallet
from businessmodel.models import Farmer, Investor ,InvestmentModel , Investment
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
from django.db import IntegrityError, transaction


from django.db import transaction

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        profile_img = request.FILES.get("profileimage")
        is_farmer = request.POST.get("is_farmer") == "T"
        phno = request.POST["phone"]
        dob = request.POST["dob"]

        print(f"Received POST data: {request.POST}")

        # Check if user already exists
        if CustomUser.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username unavailable"})
        elif CustomUser.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Email already used"})
        elif CustomUser.objects.filter(phno=phno).exists():
            return render(request, "register.html", {"error": "Phone number has been used"})
        elif password != confirmation:
            return render(request, "register.html", {"error": "Passwords must match."})

        try:
            with transaction.atomic():
                # Create user
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
                print(f"User {user.username} created successfully, is_farmer: {is_farmer}")

                # If user is a farmer, create a Farmer object explicitly
                if is_farmer:
                    land_area = request.POST.get("land_area", "").strip()
                    soil_type = request.POST.get("soil_type", "").strip()

                    print(f"DEBUG: Received land_area='{land_area}', soil_type='{soil_type}'")

                    if not land_area:
                        return render(request, "register.html", {"error": "Land area is required for farmers."})

                    try:
                        land_area = int(land_area)  # Convert to integer
                        if land_area <= 0:
                            raise ValueError("Land area must be positive")
                    except ValueError as e:
                        print(f"DEBUG: Land area conversion error: {e}")
                        return render(request, "register.html", {"error": "Invalid land area value."})

                    if not soil_type:
                        return render(request, "register.html", {"error": "Soil type is required for farmers."})

                    # Create Farmer manually
                    farmer = Farmer.objects.create(
                        user=user,
                        land_area=land_area,
                        soil_type=soil_type
                    )
                    print(f"Farmer created: {farmer}")

        except IntegrityError as e:
            print(f"Database error: {str(e)}")
            return render(request, "register.html", {"error": f"Database error: {str(e)}"})

    return render(request, "register.html")



@login_required
def profile(request):
    try:
        print('START')
        user_profile = request.user

        # Fetch the user's wallet, if it exists
        wallet = Wallet.objects.filter(user=request.user).first()

        context = {
            'profile': user_profile,
            'wallet': wallet,  # Pass wallet data to the template
        }           
        
        print('sent')
        print(context)
        return render(request, 'profile.html', context)
    except Exception as e:
        print(e)
        return render(request, 'profile.html', {'error': str(e)})


@login_required
def addmoney(request):
    if request.method == "POST":
        pin = request.POST.get("wallet_pin").strip()
        amount = request.POST.get("amount").strip()

        if not amount.isdigit() or int(amount) <= 0:
            messages.error(request, "Invalid amount.")
            return redirect("profile")

        amount = int(amount)

        try:
            wallet = Wallet.objects.get(user=request.user)

            if wallet.wallet_pin != pin:
                messages.error(request, "Incorrect PIN.")
                return redirect("profile")

            wallet.wallet_amount += amount
            wallet.save()

            messages.success(request, f"Successfully added ${amount} to your wallet.")
        except Wallet.DoesNotExist:
            messages.error(request, "No wallet found.")
    
    return redirect("profile")


@login_required
def withdraw(request):
    if request.method == "POST":
        pin = request.POST.get("wallet_pin").strip()
        amount = request.POST.get("amount").strip()

        if not amount.isdigit() or int(amount) <= 0:
            messages.error(request, "Invalid amount.")
            return redirect("profile")

        amount = int(amount)

        try:
            wallet = Wallet.objects.get(user=request.user)

            if wallet.wallet_pin != pin:
                messages.error(request, "Incorrect PIN.")
                return redirect("profile")

            if wallet.wallet_amount < amount:
                messages.error(request, "Insufficient balance.")
                return redirect("profile")

            wallet.wallet_amount -= amount
            wallet.save()

            messages.success(request, f"Successfully withdrew ${amount} from your wallet.")
        except Wallet.DoesNotExist:
            messages.error(request, "No wallet found.")

    return redirect("profile")


@login_required
def check(request):
    """Returns wallet details as JSON."""
    user_wallet, created = Wallet.objects.get_or_create(user=request.user)
    data = {
        "wallet_amount": user_wallet.wallet_amount,
        "free_amount": user_wallet.free_amount,
        "is_locked": user_wallet.is_locked,
    }
    return JsonResponse(data)
@login_required
def wallet(request):
    """Render the wallet page with CSRF token."""
    return render(request, "wallet.html")
@login_required
def walletverif(request):
    if request.method == "POST":
        confirmpassword = request.POST["password"]
@login_required
def createwallet(request):
        if request.method == "POST":
            passw =   request.POST.get("pasw"," ")
            walletc =Wallet.objects.create(
                 wallet_pin=passw,
                 user_id = request.user.id ,
            )
            print("done")
            walletc.save()
            return redirect('profile')
        return redirect('profile')



def get_user_location(request):
    ip_address = request.META.get('REMOTE_ADDR')  # Get the user's IP
    api_key = settings.IPSTACK_API_KEY  # Store your API key in settings.py
    url = f'http://api.ipstack.com/{ip_address}?access_key={api_key}'
    response = requests.get(url)
    location_data = response.json()

    if location_data and location_data.get('city'):
        # Store the city, region, or any other part of the location
        city = location_data.get('city')
        # Update the user's location field
        user = request.user
        user.location = city
        user.save()
        return JsonResponse({'location': city})
    else:
        return JsonResponse({'error': 'Location not found'})
