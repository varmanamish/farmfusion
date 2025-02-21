from django.shortcuts import render
from .models import SupportPost  # No need to import InvestmentModel directly

def support_posts(request):
    # Fetch all support posts
    support_posts = SupportPost.objects.all()
    
    # Render the HTML template with the support posts
    return render(request, 'support/support_posts.html', {
        'support_posts': support_posts,
    })
