from django import forms
from .models import NightScratch, Scratch


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class NightScratchForm(forms.ModelForm):

    class Meta:
        model = NightScratch
        widgets = {'date': DateInput()}
        fields = ["date", "time_of_10th_scratch"]


class AddScratchForm(forms.ModelForm):

    class Meta:
        model = Scratch
        widgets = {'date': DateInput(), 'time': TimeInput()}
        fields = ["date", "time"]
