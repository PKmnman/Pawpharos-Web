"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=60,
        label="First Name",
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': 'First Name'}))

    last_name = forms.CharField(
        max_length=160,
        label="Last Name",
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': 'Last Name'}))

    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput({
            'class': 'form-control',
            'type':'email',
            'placeholder':'name@example.com'}))

    username = forms.CharField(
        max_length=254, required=True,
        label="Username",
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': 'User name'}))

    password1 = forms.CharField(
        label=_("Password"), required=True,
        widget=forms.PasswordInput({
            'class': 'form-control',
            'placeholder':'Password'}))

    password2 = forms.CharField(
        label=_("Re-enter Password"), required=True,
        widget=forms.PasswordInput({
            'class': 'form-control',
            'placeholder':'Re-enter Password'}))