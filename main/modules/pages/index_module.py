from django.shortcuts import render

from main.modules.base_module import BaseViewModule


class IndexPageModule(BaseViewModule):
    def process_view(self):
        return render(self.request, 'pages/index.html')
