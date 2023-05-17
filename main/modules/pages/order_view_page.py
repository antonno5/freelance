from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from main.decorators.spec_types_check import executor_only, customer_only
from main.forms.order_form import OrderForm
from main.modules.base_module import BaseViewModule


class OrderViewModule(BaseViewModule):
    def __init__(self, request, order_id):
        super().__init__(request)
        self.order_id = order_id

    def process_logic(self):
        pass

    def process_context(self):
        pass

    def process_view(self):
        return render(self.request, "pages/order_create.html", self.context)
