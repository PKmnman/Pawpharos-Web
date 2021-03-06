"""
Definition of urls for PetBeaconWebsite.
"""

from datetime import datetime
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views, ajax_views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls, name='admin'),
    path('features/', views.features, name='features'),
    path('account/', views.account, {'account_id':None}, name='account'),
    path('tracking/', views.event_list, name='event-list'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('app.api.urls')),
]
