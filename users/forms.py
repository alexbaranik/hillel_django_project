from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)

    def clean(self):
        self.instance.username = self.cleaned_data['email'].split('@')[0]
        return self.cleaned_data
