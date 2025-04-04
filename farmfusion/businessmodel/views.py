from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect,JsonResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Farmer, Investor ,InvestmentModel , Investment
from accounts.models import CustomUser,Wallet
# Create your views here.

def myprojects(request):
        try :
            far = Farmer.objects.get(user_id=request.user.id)
            previous_projects = InvestmentModel.objects.filter(farmer=far)
            print(previous_projects)
            
            return render(request,"myprojects.html",context={"previous_projects": previous_projects })
        except:
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
            try :
                alp = Investment.objects.get(investment_model=mlid,investor = Investor.objects.get(user=request.user))
                if(alp):
                    investment = Investment.objects.get(investment_model=mlid)
                
                    if(investment.investment_amount+investamount <= mlid.requiredamount):
                        investment.investment_amount+=investamount
                        investment.save()
                        mlid.requiredamount-=investamount
                        mlid.save()
                        return JsonResponse({"message": "Investment successful", "investment_id": investment.id}, status=200)
                    else:
                        return JsonResponse({"error": "Investment amount exeeded"}, status=404)
                
            except Exception as e:
               
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
                    if(investamount>mlid.requiredamount) :
                        return JsonResponse({"error": "Exceeded required limit"}, status=400)
                    else:
                        wallet.wallet_amount -= investamount
                        wallet.save()
                        mlid.requiredamount-=investamount
                        mlid.save()
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

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import VerificationQuery, InvestmentModel, Farmer, verifymodel

def raise_verification_query(request):
    if request.method == "POST":
        farmer = get_object_or_404(Farmer, user=request.user)
        investment_model_id = request.POST.get("investment_model_id")
        reason = request.POST.get("reason")

        investment_model = get_object_or_404(InvestmentModel, id=investment_model_id)

        # Check if there's an existing verification attempt
        verification_entry = verifymodel.objects.filter(investment_model=investment_model, farmer=farmer).first()

        # Create the query
        query = VerificationQuery.objects.create(
            farmer=farmer,
            investment_model=investment_model,
            verifymodel=verification_entry,
            reason=reason
        )

        return JsonResponse({"message": "Query submitted successfully", "query_id": query.id})
from django.shortcuts import get_object_or_404
def submit_verification(request):
    if request.method == "POST":
        try:
            # Get the farmer profile for current user
            farmer = get_object_or_404(Farmer, user=request.user)

            # Extract project ID first
            investment_model_id = request.POST.get("project_id")
            print(f"Received project_id: {investment_model_id}")
            print(f"POST Data: {request.POST}")

            if not investment_model_id:
                return JsonResponse({"error": "Investment model ID is required"}, status=400)

            # Convert to int just to be safe
            try:
                investment_model_id = int(investment_model_id)
            except ValueError:
                return JsonResponse({"error": "Invalid investment model ID"}, status=400)

            # Get the investment model that belongs to this farmer
            investment_model = get_object_or_404(
                InvestmentModel,
                id=investment_model_id,
                farmer=farmer
            )

            # Get the other form data (remove commas!)
            crpimg = request.FILES.get("crpimg")
            iasimg = request.FILES.get("iasimg")
            doc_number = request.POST.get("doc_number")
            articleimg = request.FILES.get("articleimg")
            artlink = request.POST.get("artlink")

            # Create verification record
            verification = verifymodel.objects.create(
                investment_model=investment_model,
                farmer=farmer,
                crpimg=crpimg,
                iasimg=iasimg,
                doc_number=doc_number,
                articleimg=articleimg,
                artlink=artlink,
                is_approved=None  # Pending approval
            )

            return JsonResponse({
                "message": "Verification submitted successfully",
                "verification_id": verification.id
            })

        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=400)

    else:
        far = Farmer.objects.get(user_id=request.user.id)
        projects = InvestmentModel.objects.filter(farmer=far, completed=False)
        
        try :
            verifications = verifymodel.objects.select_related('farmer__user', 'investment_model').all().order_by('-id')
            
            return render(request, "raisequery.html", {"projects": projects,"verifications": verifications})
        except:
            return render(request, "raisequery.html", {"projects": projects})

def showallmodels(request):
    print("request")
    investor = request.user.id # Get the logged-in investor
    model = InvestmentModel.objects.filter(is_disbursed = False)  # Fetch all investment opportunities
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

def mlforms(request):
    return render (request, "mlforms.html")
@login_required
def verification_dashboard(request):
    if not request.user.is_vfc:
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    verifications = verifymodel.objects.all().order_by('-id')
    return render(request, 'verification.html', {'verifications': verifications})

@login_required
def approve_verification(request, verification_id, action):
    if not request.user.is_vfc:
        return HttpResponseForbidden("You don't have permission to perform this action.")
    
    verification = get_object_or_404(verifymodel, id=verification_id)

    if action == "approve":
        verification.is_approved = True
    elif action == "reject":
        verification.is_approved = False
    verification.save()
    
    return redirect('verification_dashboard')
