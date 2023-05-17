from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from main.models import BaseRate
from main.modules.base_module import BaseViewModule


@method_decorator(login_required(), name='view')
class RatesListModule(BaseViewModule):
    def process_logic(self):
        self.your_rates = BaseRate.objects.filter(user=self.request.user)
        self.rates_from_you = BaseRate.objects.filter(author=self.request.user)

    def process_context(self):
        self.context['your_rates'] = self.your_rates
        self.context['rates_from_you'] = self.rates_from_you

    def process_view(self):
        return render(self.request, "pages/your_rates.html", self.context)
