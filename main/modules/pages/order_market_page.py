from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from main.models import Order
from main.modules.base_module import BaseViewModule


class OrderMarketModule(BaseViewModule):
    def process_logic(self):
        self.orders = Order.objects.filter(state=Order.OrderStates.OPEN)

    def process_context(self):
        self.context['orders'] = self.orders

    def process_view(self):
        return render(self.request, "pages/order_market.html", self.context)
