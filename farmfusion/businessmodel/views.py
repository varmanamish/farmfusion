from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Farmer, Investor ,InvestmentModel , Investment
from accounts.models import CustomUser,Wallet
# Create your views here.

def myprojects(request):
        far = Farmer.objects.get(user_id=request.user.id)
        previous_projects = InvestmentModel.objects.filter(farmer=far)
        print(previous_projects)
        return render(request,"myprojects.html",context={"previous_projects": previous_projects})


@login_required
def createinvestmentmodel(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            capital = int(request.POST.get("capital"))
            farmer_share = int(request.POST.get("farmerShare"))
            working_share = int(request.POST.get("workingShare"))
            estimated_time = request.POST.get("estimatedTime")
            farmer = request.user.farmer

            # Ensure farmer share does not exceed total capital
            if farmer_share > capital:
                return JsonResponse({"error": "Farmer share cannot exceed total capital."}, status=400)

            # Create the investment model
            investment_model = InvestmentModel.objects.create(
                name=name,
                farmer=farmer,
                capital=capital,
                farmer_share=farmer_share,
                working_share=working_share,
                estimated_time=estimated_time
            )

            return JsonResponse({"message": "Investment proposal created successfully!", "id": investment_model.id})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)




from django.http import JsonResponse
from businessmodel.models import Investment, InvestmentModel, Investor
from accounts.models import Wallet

def invest(request):
    if request.method == "POST":
        try:
            # Retrieve form data
            investamount = int(request.POST.get("investamount", 0))
            modelid = int(request.POST.get("modelid", 0))

            # Validate input
            if investamount <= 0 or modelid <= 0:
                return JsonResponse({"error": "Invalid investment amount or model ID"}, status=400)

            # Fetch the investment model
            try:
                mlid = InvestmentModel.objects.get(id=modelid)
            except InvestmentModel.DoesNotExist:
                return JsonResponse({"error": "Investment model not found"}, status=404)

            # Fetch the investor and wallet
            try:
                wallet = Wallet.objects.get(user=request.user)
                inv = Investor.objects.get(user=request.user)
            except Wallet.DoesNotExist:
                return JsonResponse({"error": "Wallet not found"}, status=404)
            except Investor.DoesNotExist:
                return JsonResponse({"error": "Investor profile not found"}, status=404)

            # Check if the user has enough funds
            if investamount > wallet.wallet_amount:
                return JsonResponse({"error": "Insufficient funds in wallet"}, status=400)

            # Deduct funds from the wallet
            wallet.wallet_amount -= investamount
            wallet.save()

            # Create the investment
            investment = Investment.objects.create(
                investment_model=mlid,
                investor=inv,
                investment_amount=investamount
            )

            return JsonResponse({"message": "Investment successful", "investment_id": investment.id}, status=200)

        except ValueError:
            return JsonResponse({"error": "Invalid input data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)



def showallmodels(request):
    print("request")
    investor = request.user.id # Get the logged-in investor
    model = InvestmentModel.objects.all()  # Fetch all investment opportunities
    inv=Investor.objects.get(user_id=investor)  # Fetch investments by this investor
    print(model) 
    my_investments = Investment.objects.select_related('investment_model').filter(investor_id=inv.id)
    
    print(my_investments)   
    return render(request, "myinvestment.html", {
        "all_investment_models": model,
        "my_investments": my_investments,
       
    })

def myinvestments(request):
    return render (request, "myinvestment.html")