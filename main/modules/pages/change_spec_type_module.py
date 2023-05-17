from django.shortcuts import render, redirect

from main.forms.change_spec_type_form import ChangeSpecTypeForm
from main.models import BaseSpecType
from main.modules.base_module import BaseViewModule


class ChangeSpecTypePageModule(BaseViewModule):
    def process_logic(self):
        if self.request.method == 'POST':
            self.form = ChangeSpecTypeForm(self.request.POST)
            if self.form.is_valid():
                BaseSpecType.change_spec_type(
                    self.request.user,
                    ChangeSpecTypeForm.SpecTypes.value_to_spec_type(
                        int(self.form.cleaned_data['spec_type'])
                    )
                )
                return redirect('profile_edit')

        self.form = ChangeSpecTypeForm(initial={
            'spec_type':
                ChangeSpecTypeForm.SpecTypes.spec_type_to_value(
                    self.request.user.get_spec_type_object()
                )
        })

    def process_context(self):
        self.context['form'] = self.form

    def process_view(self):
        return render(self.request, 'pages/change_spec_type.html', self.context)