from django import forms


class AvailabilityForm(forms.Form):
    check_in = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", ])
    check_out = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", ])
