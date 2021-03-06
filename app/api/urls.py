
"""
Definition of API specific urls for Pawpharos app
"""


from django.urls import path
import app.views as views
import app.ajax_views as ajax_views
import app.api.views as api_views
from rest_framework.authtoken import views as rest_views

urlpatterns = [
    path("forms/<str:form_type>", ajax_views.get_form, name="get_form"),
    path('ajax/add-device', ajax_views.add_new_device, name="api-add-device"),
    path('device/remove', views.remove_device, name="remove-device"),
    path('users/', api_views.list_users, name="list_users"),
    path('users/add-device', api_views.create_sniffer, name="register-device"),
    path('api-token-auth/', rest_views.obtain_auth_token),
    path('events/', api_views.TrackingEventAPIView.as_view(), name="event-view")
]