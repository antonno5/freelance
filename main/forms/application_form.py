from django.forms import ModelForm

from main.models import Application


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ["comment"]
