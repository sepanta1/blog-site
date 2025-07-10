from django.shortcuts import render


def home(request):
    return render(request, 'website/index.html')


def about(request):
    return render(request, 'website/about.html')
# Create your views here.
