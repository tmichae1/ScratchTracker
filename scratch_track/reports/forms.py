from django import forms
from.models import DailyReport


class DateInput(forms.DateInput):
    input_type = 'date'

TRUE_FALSE_CHOICES = (
    (False, 'Not Taken'),
    (True, 'Taken')
)


class DailyReportForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        widgets = {'date': DateInput(),
                   'scalp_steroid': forms.Select(choices=TRUE_FALSE_CHOICES)}
        fields = [
                  'date',
                  'ointment_used',
                  'nasal_spray_used',
                  'nostril_used',
                  'scalp_steroid',
                  'antihistamine_120mg',
                  'steroid_tablet',
                  'inhaler',
                  'extra_info']
