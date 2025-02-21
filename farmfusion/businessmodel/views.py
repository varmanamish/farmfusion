from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Farmer, Investor ,InvestmentModel , Investment
from accounts.models import CustomUser,Wallet
# Create your views here.
def myinvestment(request):
    return render(request,"myinvestment.html")

def myprojects(request):
    return render(request,"myprojects.html")


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


def showpreviousproj(request):
    cards = InvestmentModel.objects.filter(user=request.user)
    return render(request,"myprojects.html",context={cards})

def invest(request):
    if request.method=="POST":
        investamount = request.POST.get("investamount").strip()
        modelid=request.POST.get("modeilid").strip()
        wallet = Wallet.objects.get(user=request.user)
        if(investamount<=wallet.wallet_amount):
            wallet.wallet_amount=wallet-investamount
            wallet.save()
            Investment.objects.create(
            investment_model = modelid,
            investor = request.user.investor,
            investment_amount = investamount,
            )
        
def showinvestments(request):
    investor = request.user.investor  # Get the logged-in investor

    # Fetch all investments made by the investor
    investments_made = Investment.objects.filter(investor=investor)

    # Get only the InvestmentModels that the investor has invested in
    invested_model_ids = investments_made.values_list("investment_model_id", flat=True)  # Extract IDs
    invested_models = InvestmentModel.objects.filter(id__in=invested_model_ids)  # Fetch models

    return render(request, "investor_dashboard.html", {
        "invested_models": invested_models,
        "investments_made": investments_made
    })


def showallmodels(request):
    investor = request.user.investor  # Get the logged-in investor
    all_investment_models = InvestmentModel.objects.all()  # Fetch all investment opportunities
    investments_made = Investment.objects.filter(investor=investor)  # Fetch investments by this investor

    return render(request, "investor_dashboard.html", {
        "all_investment_models": all_investment_models,
        "investments_made": investments_made
    })
