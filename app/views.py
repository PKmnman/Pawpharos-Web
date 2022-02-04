"""
Definition of views.
"""

from datetime import datetime
import uuid
from django.shortcuts import redirect, render
from django.http import HttpRequest
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.contrib.auth.decorators import login_required

import app.models as models
from app.forms import RegistrationForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Pawpharos',
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

@login_required(login_url='/login/')
def account(request, **kwargs):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/account.html',
        {
            'title':'Pawpharos - Account Details',
            'profile': models.UserProfile.objects.get_or_create(account=request.user)
        }
    )
    
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user: User = form.save()
            user.refresh_from_db()
            
            # load the profile instance created by the signal
            profile: models.UserProfile = models.UserProfile.objects.create()
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            raw_password = form.cleaned_data['password1']
            
            user.profile = profile
            
            profile.save()
            user.save()

            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
 
            # redirect user to home page
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'app/register.html', {'form': form})