from django import forms
from django.forms import ModelForm
from HOME.models import Submission

class CodeForm(ModelForm):
    class Meta:
        model = Submission
        # fields = '__all__'
        fields = ['user_code','language']
        widgets = {'user_code' : forms.Textarea()}