from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from main.decorators.spec_types_check import executor_only, customer_only
from main.forms.application_form import ApplicationForm
from main.models import Application
from main.modules.base_module import BaseViewModule


@method_decorator(executor_only, name='view')
class ApplicationEditModule(BaseViewModule):
    def process_logic(self):
        application = Application.objects.get(pk=self.application_id)
        if self.request.method == 'POST':
            self.form = ApplicationForm(self.request.POST, instance=application)
            if self.form.is_valid():
                self.form.save()
                messages.add_message(self.request, messages.SUCCESS, 'Successfully edited')
                return redirect('order_market')
        else:
            self.form = ApplicationForm(instance=application)

    def process_context(self):
        self.context['application_edit_form'] = self.form

    def process_view(self):
        return render(self.request, "pages/application_edit.html", self.context)
