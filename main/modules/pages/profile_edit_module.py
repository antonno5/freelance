from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator

from main.forms.spec_type_forms import ExecutorTypeForm, PrivateCustomerTypeForm, CorporateCustomerTypeForm
from main.modules.base_module import BaseViewModule


@method_decorator(login_required, name='view')
class ProfileEditPageModule(BaseViewModule):
    def process_logic(self):
        form_cls = None
        if self.request.user.is_executor():
            form_cls = ExecutorTypeForm
        elif self.request.user.is_private_customer():
            form_cls = PrivateCustomerTypeForm
        elif self.request.user.is_corporate_customer():
            form_cls = CorporateCustomerTypeForm

        if self.request.method == "POST":
            self.form = form_cls(self.request.POST, instance=self.request.user.get_spec_type_object())
            if self.form.is_valid():
                self.form.save()
        else:
            self.form = form_cls(instance=self.request.user.get_spec_type_object())

    def process_context(self):
        self.context['form'] = self.form

    def process_view(self):
        return render(self.request, 'pages/profile_edit.html', self.context)