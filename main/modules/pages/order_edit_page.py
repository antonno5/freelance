from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from main.decorators.spec_types_check import executor_only, customer_only
from main.forms.order_form import OrderForm
from main.models import Order
from main.modules.base_module import BaseViewModule


@method_decorator(customer_only, name='view')
class OrderEditModule(BaseViewModule):
    def process_logic(self):
        order = Order.objects.get(pk=self.order_id)
        if self.request.method == 'POST':
            self.form = OrderForm(self.request.POST, instance=order)
            if self.form.is_valid():
                self.form.save()
                messages.add_message(self.request, messages.SUCCESS, 'Successfully edited')
                return redirect('order_market')
        else:
            self.form = OrderForm(instance=order)

    def process_context(self):
        self.context['order_edit_form'] = self.form

    def process_view(self):
        return render(self.request, "pages/order_edit.html", self.context)
