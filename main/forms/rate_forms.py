from django import forms

from main.models import CustomerRate, ExecutorRate


class CustomerRateForm(forms.ModelForm):
    class Meta:
        model = CustomerRate
        exclude = ['author', 'user', 'order']


class ExecutorRateForm(forms.ModelForm):
    class Meta:
        model = ExecutorRate
        exclude = ['author', 'user', 'order']
