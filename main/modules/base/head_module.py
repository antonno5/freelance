from main.modules.base_module import BaseModule


class HeadModule(BaseModule):
    def __init__(self, request, page_name='Freelance'):
        super().__init__(request)
        self.page_name = page_name

    def process_context(self):
        self.context['page_name'] = self.page_name
