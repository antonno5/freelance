from django.http import HttpResponseNotFound
from django.shortcuts import render

from main.models import User, ExecutorRate, CustomerRate
from main.modules.base_module import BaseViewModule


class ProfilePageModule(BaseViewModule):
    def __init__(self, request, user_id):
        super().__init__(request)
        self.user_id = user_id

    def process_logic(self):
        try:
            self.user = User.objects.get(pk=self.user_id)
        except User.DoesNotExist:
            return HttpResponseNotFound()
        self.spec_type = self.user.get_spec_type_object()
        if self.user.is_executor():
            self.rate = ExecutorRate.count_all_rates(self.user)
        else:
            self.rate = CustomerRate.count_all_rates(self.user)

    def process_context(self):
        self.context['page_user'] = self.user
        self.context['page_spec_type'] = self.spec_type
        self.context['rate'] = self.rate

    def process_view(self):
        return render(self.request, 'pages/profile.html', self.context)