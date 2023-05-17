from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from main.forms.rate_forms import ExecutorRateForm, CustomerRateForm
from main.models import User, Order, BaseRate
from main.modules.base_module import BaseViewModule


@method_decorator(login_required, name='view')
class RatePageModule(BaseViewModule):
    def __init__(self, request, order_id):
        super().__init__(request)
        self.order_id = order_id

    def process_logic(self):
        try:
            self.order = Order.objects.get(pk=self.order_id)
        except Order.DoesNotExist:
            return HttpResponseNotFound()
        if not self.order.is_owner(self.request.user):
            raise PermissionDenied()
        if BaseRate.is_order_rated(self.order, self.request.user):
            messages.add_message(self.request, messages.ERROR, 'You have already rated this order')
            return redirect('order', self.order.pk)
        form_class = None
        if self.order.is_owner_customer(self.request.user):
            form_class = ExecutorRateForm
        else:
            form_class = CustomerRateForm

        if self.request.method == "POST":
            self.form = form_class(self.request.POST)
            if not self.form.is_valid():
                return None
            rate = self.form.save(commit=False)
            rate.order = self.order
            rate.author = self.request.user
            if self.order.is_owner_customer(self.request.user):
                rate.user = self.order.executor.user
            else:
                rate.user = self.order.customer.user
            rate.save()
            return redirect('order', self.order.pk)
        else:
            self.form = form_class()

    def process_context(self):
        self.context['order'] = self.order
        self.context['form'] = self.form

    def process_view(self):
        return render(self.request, 'pages/order_rate.html', self.context)
