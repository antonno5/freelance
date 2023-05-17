from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from main.models import Application
from main.modules.base_module import BaseViewModule


@method_decorator(login_required(), name='view')
class ApplicationListModule(BaseViewModule):
    def process_logic(self):
        if self.request.user.is_customer():
            self.applications_pending = Application.objects.filter(state=Application.AppStates.PENDING, receiver=self.request.user)
            self.applications_accepted = Application.objects.filter(state=Application.AppStates.ACCEPTED, receiver=self.request.user)
            self.applications_declined = Application.objects.filter(state=Application.AppStates.DECLINED, receiver=self.request.user)
            self.applications_finished = Application.objects.filter(state=Application.AppStates.FINISHED, receiver=self.request.user)
        else:
            self.applications_pending = Application.objects.filter(state=Application.AppStates.PENDING, author=self.request.user)
            self.applications_accepted = Application.objects.filter(state=Application.AppStates.ACCEPTED, author=self.request.user)
            self.applications_declined = Application.objects.filter(state=Application.AppStates.DECLINED, author=self.request.user)
            self.applications_finished = Application.objects.filter(state=Application.AppStates.FINISHED, author=self.request.user)

    def process_context(self):
        self.context['applications_pending'] = self.applications_pending
        self.context['applications_accepted'] = self.applications_accepted
        self.context['applications_declined'] = self.applications_declined
        self.context['applications_finished'] = self.applications_finished

    def process_view(self):
        return render(self.request, "pages/your_applications.html", self.context)
