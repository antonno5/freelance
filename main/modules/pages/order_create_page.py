from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from main.decorators.spec_types_check import executor_only, customer_only
from main.forms.order_form import OrderForm
from main.modules.base_module import BaseViewModule


@method_decorator(customer_only, name='view')
class OrderCreateModule(BaseViewModule):
    def process_logic(self):
        if self.request.method == 'POST':
            self.form = OrderForm(self.request.POST)
            if self.form.is_valid():
                order = self.form.save(commit=False)
                order.customer = self.request.user.get_spec_type_object()
                order.save()
                messages.add_message(self.request, messages.SUCCESS, 'Successfully created')
                return redirect('order_market')
        else:
            self.form = OrderForm()

    def process_context(self):
        self.context['order_create_form'] = self.form

    def process_view(self):
        return render(self.request, "pages/order_create.html", self.context)
