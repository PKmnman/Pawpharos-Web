from django.shortcuts import redirect, render
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.template.loader import render_to_string

import app.models as models
import app.forms as forms

def add_new_device(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        form = forms.AddDeviceForm(request.POST)

        if form.is_valid():
            # Add the device to the user's account
            form.add_device(request.user.profile)

            # Return a JsonResponse to the ajax method that contains a clean form
            return JsonResponse({
                'status': 1,
                'content': render_to_string('app/add-new-device.html', { 'form':forms.AddDeviceForm() })
            })
        else:
            
            return JsonResponse({
                'status': 0,
                'content': render_to_string('app/add-new-device.html', { 'form':form })
            })
    else:
        # Only accept POST request through this view
        return HttpResponseBadRequest()