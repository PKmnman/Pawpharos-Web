"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import redirect, render
from django.http import HttpRequest
from django.views.generic.edit import FormView

from app.forms import RegistrationForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Fur-Tector',
            'year':datetime.now().year,
        }
    )

def features(request):
    assert isinstance(request, HttpRequest)
    return redirect('/')

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def account(request, account_id):
    assert isinstance(request, HttpRequest)
    if account_id is None:
        return redirect()
    return render(
        request,
        'app/account.html',
        {
            'title':'Fur-Tector - Account Details',
            'account_id':account_id
        }
    )

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  
            # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
 
            # login user after signing up
            # user = authenticate(username=user.username, password=raw_password)
            # login(request, user)
 
            # redirect user to home page
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'app/register.html', {'form': form})