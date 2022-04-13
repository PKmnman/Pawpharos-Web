"""
Definition of views.
"""

from datetime import datetime
import sys

from uuid import uuid4
from django.shortcuts import redirect, render
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseNotAllowed, JsonResponse

from django.contrib.auth import login, authenticate

from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from django.template.loader import render_to_string

import app.models as models
import app.forms as forms
from app import LOGGER

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

    if request.method == 'GET':
        # Just open the account details page
        return render(
            request,
            'app/account.html',
            {
                'title':'Pawpharos - Account Details',
                'form': forms.AddDeviceForm()
            }
        )


def register(request):
    LOGGER.info("Received registration request.")
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        LOGGER.debug("Attempting to register user..")
        if form.register_user():
            LOGGER.info("User registered! Logging in...")
            # login user after signing up
            raw_password = form.cleaned_data['password1']
            username = form.cleaned_data['username']
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            LOGGER.info("User [%s] has successfully logged in.", user.get_username())
            # redirect user to home page
            return redirect('home')
        else:
            LOGGER.debug("Failed to register user.")
    else:
        # On GET request, just load the empty form
        form = forms.RegistrationForm()
    return render(request, 'app/register.html', {'form': form})


def remove_device(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        device = request.POST.get("device_id")
        LOGGER.info("Removing device with UUID: %s", device)
        try:
            device_inst = models.BeaconDevice.objects.get(id=device)
            device_inst.delete()
            LOGGER.debug("Device removed!!")
            return HttpResponse(status=200)
        except:
            LOGGER.exception("Failed to remove device!")
    else:
        LOGGER.error("Received GET request for POST function!!")
        return HttpResponseNotAllowed()
        