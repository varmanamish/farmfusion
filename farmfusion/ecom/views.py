from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse

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
        # Get username, email, password and confirmation password from the form
        username = request.POST["username"] # username is the name of the input field in the form
        email = request.POST["email"] # email is the name of the input field in the form
        password = request.POST["password"] # password is the name of the input field in the form
        confirmation = request.POST["confirmation"] # confirmation is the name of the input field in the form
        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password) # create_user() is a built-in function provided by Django
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    # If method is GET, return register page
    else:
        return render(request, "register.html")