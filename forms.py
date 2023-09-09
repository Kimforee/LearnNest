from django.forms import ModelForm
from .models import Nest

class NestForm(ModelForm):
    class Meta:
        model = Nest
        fields = '__all__'