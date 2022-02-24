

from django.urls import path
import app.views as views
import app.ajax_views as ajax_views

urlpatterns = [
    path("forms/<str:form_type>", ajax_views.get_form, name="get_form"),
    path('ajax/add-device', ajax_views.add_new_device, name="api-add-device"),
]