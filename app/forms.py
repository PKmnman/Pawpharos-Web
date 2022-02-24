"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

import app.models as models

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

    def is_valid(self) -> bool:
        if not super().is_valid():
            return False
        if not self.user_exists():
            self.add_error('username', forms.ValidationError('An account with this username already exists!'))
            return False
        return True

    def user_exists(self):
        # Check that the user accound doesn't already exist
        login_name = self.cleaned_data['username']
        return User.objects.filter(username=login_name).count() > 0

    def register_user(self):
        # Register the user account
        if self.is_valid():
            user = self.save()
            user.refresh_from_db()
            
            # load the profile instance created by the signal
            profile = models.UserProfile.objects.create()

            # Associate the profile with the user account
            user.profile = profile
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            # Save the changes to the database
            profile.save()
            user.save()

            return True

        # Return False on failure to register
        return False


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
            'onchange': 'onDeviceChange()'
        }),
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
        max_length=36,
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': 'snff-XXXX-XXXX-XXXX',
        })
    )

    is_master = forms.BooleanField(
        label=_('Is Master?'),
        widget= forms.CheckboxInput(),
        initial=False,
        required=False
    )

    def add_device(self, user):
        # Associate the device with the user
        code = self.cleaned_data['code']
        name = self.cleaned_data['name']

        # Switch model based on device type
        if self.cleaned_data['device_type'] == "B":
            device = models.BeaconDevice(
                uuid=code,
                device_name=name,
                user=user
            )
        else:
            device = models.Sniffer(
                name=name,
                reg_code=code,
                is_master=self.cleaned_data['is_master'],
                owner=user
            )

        device.save()

form_class = {
    'AddDeviceForm': AddDeviceForm,
    'RegistrationForm': RegistrationForm,
}