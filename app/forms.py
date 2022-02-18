"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

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


# Form for adding a new device to the account
class AddDeviceForm(forms.Form):

    device_type = forms.ChoiceField(
        choices=[
            ('B', 'Beacon'),
            ('S', 'Sniffer'),
        ],
        label=_('Device Type'),
        widget=forms.Select({
            'class': 'form-select',
            'aria-label': 'Device Type Select',
        })
    )

    name = forms.CharField(
        label=_('Device Name'),
        max_length=64,
        widget=forms.TextInput({
            'class': 'form-control'
        })
    )

    code = forms.CharField(
        label=_('Device Code'),
        max_length=14,
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': 'snff-XXXX-XXXX-XXXX',
        })
    )