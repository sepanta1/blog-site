from django.shortcuts import render
from .forms import Contact_form


def home(request):
    return render(request, 'website/index.html')


def about(request):
    return render(request, 'website/about.html')
# Create your views here.

def contact(request):
    
    if request.method =='POST':
        form= Contact_form()
        if form.is_valid():
            form.save()
   
    form= Contact_form()
    return render(request,'website/contact.html',{'form':form})
    