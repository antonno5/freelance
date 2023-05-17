from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from main.forms.rate_forms import ExecutorRateForm, CustomerRateForm
from main.models import User, Order, BaseRate, ExecutorRate, CustomerRate
from main.modules.base_module import BaseViewModule


@method_decorator(login_required, name='view')
class RateEditModule(BaseViewModule):
    def __init__(self, request, rate_id):
        super().__init__(request)
        self.rate_id = rate_id

    def process_logic(self):
        rate = None
        form_class = None
        try:
            form_class = ExecutorRateForm
            rate = ExecutorRate.objects.get(baserate_ptr_id=self.rate_id)
        except ExecutorRate.DoesNotExist:
            pass
        try:
            form_class = CustomerRateForm
            rate = CustomerRate.objects.get(baserate_ptr_id=self.rate_id)
        except CustomerRate.DoesNotExist:
            pass
        if rate.author != self.request.user:
            raise PermissionDenied()
        if self.request.method == "POST":
            self.form = form_class(self.request.POST, instance=rate)
            if not self.form.is_valid():
                return None
            self.form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Successfully edited')
            return redirect('order_market')
        else:
            self.form = form_class(instance=rate)

    def process_context(self):
        self.context['rate_edit_form'] = self.form

    def process_view(self):
        return render(self.request, 'pages/rate_edit.html', self.context)
