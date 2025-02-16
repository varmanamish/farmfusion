from django.shortcuts import render

# Create your views here.
def socialmedia_view(request):
    return render(request, 'socialmedia.html')