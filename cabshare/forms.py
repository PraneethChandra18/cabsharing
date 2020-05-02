from django import forms
from .models import Booking,Chat
import datetime


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class BookingForm(forms.ModelForm):
    date_of_journey = forms.DateField(widget=DateInput,initial=datetime.date.today)
    time = forms.TimeField(widget=TimeInput)

    class Meta:
        model = Booking
        fields = ['date_of_journey','time','destination','amount_of_luggage','budget','special_note']

    def clean(self):
        cleaned_data = super(BookingForm,self).clean()
        date = cleaned_data.get("date_of_journey")
        time = cleaned_data.get("time")
        if date <= datetime.date.today() and time <= datetime.datetime.now().time():
            raise forms.ValidationError('The date must be after or today')

class ChatForm(forms.ModelForm):

    class Meta:
        model = Chat
        fields = ['message']


# datetime.now()+timedelta(days=30)
