from django import forms
from .models import Booking,Chat,Feedback
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
        fields = ['date_of_journey','time','starting_point','destination','amount_of_luggage','budget','special_note']

    def clean(self):
        cleaned_data = super(BookingForm,self).clean()
        date = cleaned_data.get("date_of_journey")
        time = cleaned_data.get("time")
        starting_point = cleaned_data.get("starting_point")
        destination = cleaned_data.get("destination")
        if date <= datetime.date.today() and time <= datetime.datetime.now().time():
            raise forms.ValidationError('The date must be after or today')
        if starting_point == destination:
            raise forms.ValidationError('The starting point and destination must be different')
    # def __init__(self, *args, **kwargs):
    #         super(MyForm, self).__init__(*args, **kwargs)
    #         self.fields['time'].widget.attrs['class'] = 'clockpicker'


class ChatForm(forms.ModelForm):

    class Meta:
        model = Chat
        fields = ['message']

class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ['feedback']
# datetime.now()+timedelta(days=30)
