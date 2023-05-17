from django.forms import ModelForm

from main.models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["title", "activity", "description", "stack", "payment"]
