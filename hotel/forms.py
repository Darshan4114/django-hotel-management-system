from django import forms
from datetime import datetime
from django.core.exceptions import ValidationError

class AvailabilityForm(forms.Form):
    check_in = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", ])
    check_out = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", ])

    def check_working_hours(self, start, end):
        check_in = self.cleaned_data.get('check_in')
        check_out = self.cleaned_data.get('check_out')
        if not( check_in < start and check_out < end): #This ensures that check_in and check_out are between start and end of your working hours.
            raise ValidationError("Times beyond working hours, please enter value within working hours")
        else:
            return self.cleaned_data