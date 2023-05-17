from django import forms
from django.db.models import Choices

from main.models import User


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Password',
        help_text='Password, please, I\'m begging you',
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Repeat password',
        help_text='Just repeat your password',
    )

    class SpecTypes(Choices):
        EXECUTOR = 1
        PRIVATE_CUSTOMER = 2
        CORPORATE_CUSTOMER = 3

    spec_type = forms.ChoiceField(
        choices=SpecTypes.choices,
        label='Role',
    )

    class Meta:
        model = User
        fields = ['email']
