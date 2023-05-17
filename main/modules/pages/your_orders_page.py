from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from main.models import Order
from main.modules.base_module import BaseViewModule


@method_decorator(login_required(), name='view')
class OrderListModule(BaseViewModule):
    def process_logic(self):
        if self.request.user.is_customer():
            self.orders_open = Order.objects.filter(state=Order.OrderStates.OPEN, customer=self.request.user.get_spec_type_object())
            self.orders_running = Order.objects.filter(state=Order.OrderStates.RUNNING, customer=self.request.user.get_spec_type_object())
            self.orders_closed = Order.objects.filter(state=Order.OrderStates.CLOSED, customer=self.request.user.get_spec_type_object())
        else:
            self.orders_running = Order.objects.filter(state=Order.OrderStates.RUNNING, executor=self.request.user.get_spec_type_object())
            self.orders_closed = Order.objects.filter(state=Order.OrderStates.CLOSED, executor=self.request.user.get_spec_type_object())

    def process_context(self):
        if self.request.user.is_customer():
            self.context['orders_open'] = self.orders_open
        self.context['orders_running'] = self.orders_running
        self.context['orders_closed'] = self.orders_closed

    def process_view(self):
        return render(self.request, "pages/your_orders.html", self.context)
