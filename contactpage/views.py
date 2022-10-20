from django.shortcuts import render

# Create your views here.
def contactpage_view(request):
    return render(request, "contactpage/contactpage.html")