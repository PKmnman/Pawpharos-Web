
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template.loader import render_to_string

import app.models as models
import app.forms as forms
from app import LOGGER


def get_form(request: HttpRequest, form_type):
    try:
        # On a GET request
        if request.method == 'GET':
            # Generate the form and add it to the context
            form = forms.form_class[form_type]
            context = {'form': form}
            
            # Generate the URL to the template we need to render
            templateURL = f"app/{request.GET.get('t', None)}.html"
            if request.GET.get('t', None) is None:
                raise Http404("Form template not found")

            # Try to open the template URL and render it
            try:
                template = render_to_string(f'app/{request.GET.get("t", None)}.html', context=context, request=request)
                return JsonResponse({"formHTML": template})
            except Exception as e:
                LOGGER.exception(
                    "Exception occured during processing of template: %s", templateURL,
                    exc_info=e
                )
                return HttpResponse(status=500)
    except:    
        raise Http404("Error locating form!!")


def add_new_device(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        LOGGER.debug("Received AddDevice Request.")
        form = forms.AddDeviceForm(request.POST)

        if form.is_valid():
            try:
                # Add the device to the user's account
                LOGGER.debug("Adding device to user account (%s)...", request.user.profile.uuid)
                form.add_device(request.user.profile)
                LOGGER.debug("Device added to user account: %s", request.user.profile.uuid)

                # Return a JsonResponse to the ajax method that contains a clean form
                return JsonResponse({
                    'status': 1,
                    'content': render_to_string('app/add-device-form.html', { 'form':forms.AddDeviceForm() })
                })
            except:
                LOGGER.exception("Exception occured adding device to profile")  
        else:
            LOGGER.debug("Form is invalid: \n%s", form.errors.as_json())
            
            return JsonResponse({
                'status': 0,
                'content': render_to_string('app/add-device-form.html', context={'form':form }, request=request)
            })
    else:
        # Only accept POST request through this view
        return HttpResponseBadRequest()

def beacon_update(request):
    assert isinstance(request, HttpRequest)

    # Process an update request from a sniffer system
    pass