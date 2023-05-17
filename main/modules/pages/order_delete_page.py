from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from main.decorators.spec_types_check import executor_only, customer_only
from main.forms.order_form import OrderForm
from main.models import Order
from main.modules.base_module import BaseViewModule


@method_decorator(customer_only, name='view')
class OrderDeleteModule(BaseViewModule):
    def process_logic(self):
        order = Order.objects.get(pk=self.application_id)
        if self.request.user.get_spec_type_object() == order.customer.get_down_class():
            order.delete()
            messages.add_message(self.request, messages.SUCCESS, 'Successfully deleted')
            return redirect('order_market')

    def process_context(self):
        pass

    def process_view(self):
        return redirect('order_market')
