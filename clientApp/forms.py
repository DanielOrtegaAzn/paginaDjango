from django import forms
from nucleo.models import Proyect, Participate
from django.contrib.admin.widgets import AdminDateWidget

class DatePickerInput(forms.DateInput):
    input_type='date'

class pdfForm(forms.Form):
    inicio=forms.DateField(widget=DatePickerInput)
    final=forms.DateField(widget=DatePickerInput)