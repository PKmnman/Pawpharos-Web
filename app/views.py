"""
Definition of views.
"""

from datetime import datetime
import logging
from tkinter import N

from uuid import uuid4
from django.shortcuts import redirect, render
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.generic.edit import FormView
from django.views import View

from django.contrib.auth import login, authenticate

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.template.loader import render_to_string

import app.models as models
import app.forms as forms

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
                'profile': models.UserProfile.objects.get(account=request.user)
            }
        )


def register(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid() and form.register_user():

            # login user after signing up
            raw_password = form.cleaned_data['password1']
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
 
            # redirect user to home page
            return redirect('home')
    else:
        # On GET request, just load the empty form
        form = forms.RegistrationForm()
    return render(request, 'app/register.html', {'form': form})


def get_form(request: HttpRequest, form_type):
    try:
        # On a GET request
        if request.method == 'GET':
            # Generate the form and add it to the context
            form = forms.form_class[form_type]
            context = { "form": form }

            # Generate the URL to the template we need to render
            templateURL = f"app/{request.GET.get('t', None)}.html"
            if request.GET.get('t', None) is None:
                raise Http404("Form template not found")

            # Try to open the template URL and render it
            try:
                template = render_to_string(f'app/{request.GET.get("t", None)}.html', context=context)
                return JsonResponse({"formHTML": template})
            except Exception as e:
                logging.exception(
                    "Exception occured during processing of template: %s", templateURL,
                    exc_info=e
                )
                return HttpResponse(status=500)
    except:    
        raise Http404("Error locating form!!")