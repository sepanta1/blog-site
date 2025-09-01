from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib import messages

from .forms import Contact_form, Newsletter_form


def home(request):
    return render(request, 'website/index.html')


def about(request):
    return render(request, 'website/about.html')
# Create your views here.


def contact(request):
    form = Contact_form(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
    else:
        form = Contact_form()
    return render(request, 'website/contact.html', {'form': form})


def newsletter(request):
    
    if request.method == 'POST':
        form = Newsletter_form(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Email added to the newsletter.")
            return redirect('/')  
        else:
            messages.add_message(request, messages.ERROR, "This email already exists!")
    
    form = Newsletter_form()
    return HttpResponseRedirect('/')
    # return render(request, 'base.html', {'form': form})
