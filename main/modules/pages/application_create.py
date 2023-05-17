from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from main.decorators.spec_types_check import executor_only, customer_only
from main.forms.application_form import ApplicationForm
from main.models import Order, User
from main.modules.base_module import BaseViewModule


@method_decorator(executor_only, name='view')
class ApplicationCreateModule(BaseViewModule):
    def process_logic(self):
        if self.request.method == 'POST':
            self.form = ApplicationForm(self.request.POST)
            if self.form.is_valid():
                application = self.form.save(commit=False)
                application.author = self.request.user
                application.order = Order.objects.get(pk=self.order_id)
                application.receiver = application.order.customer.user
                application.save()
                messages.add_message(self.request, messages.SUCCESS, 'Successfully created')
                return redirect('order_market')
        else:
            self.form = ApplicationForm()

    def process_context(self):
        self.context['application_create_form'] = self.form

    def process_view(self):
        return render(self.request, "pages/application_create.html", self.context)
