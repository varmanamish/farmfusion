from django.shortcuts import render
from .models import SupportPost  # No need to import InvestmentModel directly
from businessmodel.models import InvestmentModel
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
def support_posts(request):
    if request.method == "POST":
        # Get form data
        modelid = int(request.POST.get("modelid"))
        investingamount = int(request.POST.get("investingamount"))
        
        # Get the current user and the investment model
        user = request.user
        inv = InvestmentModel.objects.get(id=modelid)
        
        # Create a new SupportPost instance
        alp = inv.requiredamount
        if(user!=inv.farmer.user):
            if(investingamount>alp):
                return JsonResponse({"message": "donation ammount is higher than required amount u can donate to others!!"}, status=200)
            else:
                try:
                    inp=SupportPost.objects.get(user=user,investmodel=inv)
                    if(inp):
                        inp.amount+=investingamount
                        inp.save()
                    return JsonResponse({"message": "redonation successfull!!"}, status=200)
                except Exception as e:
                    support_post = SupportPost.objects.create(
                        amount=investingamount,
                        user=user,
                        investmodel=inv
                    )
                    return JsonResponse({"message": "donation successfull!!"}, status=200)
        else:
            return JsonResponse({"message": "cant donate to ur self!!"}, status=200)
        # Save the SupportPost instance to the database (it's saved by the `create` method already)
        # support_post.save() # No need to call save() explicitly as `create()` saves it.

    # Fetch all investment models where `is_disbursed` is True
    all_investment_models = InvestmentModel.objects.filter(is_disbursed=True)
    
    # Pass the investment models to the template
    return render(request, "support/support_posts.html", context={"all_investment_models": all_investment_models})
