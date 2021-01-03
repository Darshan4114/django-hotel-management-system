from django import forms
from datetime import datetime
from django.core.exceptions import ValidationError
from .models import RoomCategory, Person

#  input_formats=["%Y-%m-%dT%H:%M", ],


class AvailabilityForm(forms.Form):
    # CATEGORY_CHOICES = [(x.category, x.category)
    #                     for x in RoomCategory.objects.all()]

    check_in = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M%Z"], widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    check_out = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M%Z"], widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    room_category = forms.ModelChoiceField(
        queryset=RoomCategory.objects.all())
    #  widget=forms.Select(attrs={"class": "mdb-select md-form"})

    def check_working_hours(self, start, end):
        check_in = self.cleaned_data.get('check_in')
        check_out = self.cleaned_data.get('check_out')
        # This ensures that check_in and check_out are between start and end of your working hours.
        if not(check_in < start and check_out < end):
            raise ValidationError(
                "Times beyond working hours, please enter value within working hours")
        else:
            return self.cleaned_data


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
