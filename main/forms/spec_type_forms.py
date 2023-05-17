from django import forms

from main.models import ExecutorType, PrivateCustomerType, CorporateCustomerType


class ExecutorTypeForm(forms.ModelForm):
    class Meta:
        model = ExecutorType
        exclude = ['user']


class PrivateCustomerTypeForm(forms.ModelForm):
    class Meta:
        model = PrivateCustomerType
        exclude = ['user']


class CorporateCustomerTypeForm(forms.ModelForm):
    class Meta:
        model = CorporateCustomerType
        exclude = ['user']
