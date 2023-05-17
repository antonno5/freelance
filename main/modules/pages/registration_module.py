from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect

from main.forms.registration_form import RegistrationForm
from main.models import User, ExecutorType, PrivateCustomerType, CorporateCustomerType
from main.modules.base.head_module import HeadModule
from main.modules.base_module import BaseViewModule, Submodule


class RegistrationPageModule(BaseViewModule):
    required_submodules = {
        'head': Submodule(HeadModule, kwargs={'page_name': 'Sign up'})
    }

    def process_form(self):
        if self.request.method != 'POST':
            self.form = RegistrationForm()
            return None

        self.form = RegistrationForm(self.request.POST)
        if not self.form.is_valid():
            return None
        if self.form.cleaned_data['password1'] != self.form.cleaned_data['password2']:
            self.form.add_error('password2', 'Passwords don\'t match')
            return None

        new_user = User.objects.create_user(self.form.cleaned_data['email'],
                                            self.form.cleaned_data['password1'])
        match int(self.form.cleaned_data['spec_type']):
            case RegistrationForm.SpecTypes.EXECUTOR.value:
                spec_type = ExecutorType.objects.create(user=new_user)
            case RegistrationForm.SpecTypes.PRIVATE_CUSTOMER.value:
                spec_type = PrivateCustomerType.objects.create(user=new_user)
            case RegistrationForm.SpecTypes.CORPORATE_CUSTOMER.value:
                spec_type = CorporateCustomerType.objects.create(user=new_user)
        login(self.request, new_user)
        return redirect('index')

    def process_logic(self):
        form_return = self.process_form()
        if form_return is not None:
            return form_return

    def process_context(self):
        self.context['form'] = self.form

    def process_view(self):
        return render(self.request, 'auth/registration.html', self.context)
