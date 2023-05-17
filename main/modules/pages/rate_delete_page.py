from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from main.decorators.spec_types_check import executor_only, customer_only
from main.forms.order_form import OrderForm
from main.models import Order, BaseRate
from main.modules.base_module import BaseViewModule


@method_decorator(login_required, name='view')
class RateDeleteModule(BaseViewModule):
    def __init__(self, request, rate_id):
        super().__init__(request)
        self.rate_id = rate_id

    def process_logic(self):
        rate = BaseRate.objects.get(pk=self.rate_id)
        if self.request.user == rate.author:
            rate.delete()
            messages.add_message(self.request, messages.SUCCESS, 'Successfully deleted')
            return redirect('order_market')

    def process_context(self):
        pass

    def process_view(self):
        return redirect('order_market')
