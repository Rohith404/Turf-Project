from django import forms
from django.forms.widgets import PasswordInput
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

GENDER= [
    ('female', 'female'),
    ('male', 'male'),
    ('others', 'others'),
]

class UserForm(UserCreationForm):
    username=forms.CharField(help_text=None,label='username')
    email=forms.EmailField(label='email')
    phone=forms.CharField(label='Phone')
    address= forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    gender= forms.CharField(label='select gender', widget=forms.Select(choices=GENDER))
    password1=forms.CharField(help_text=None,widget=PasswordInput,label='Password')
    password2=forms.CharField(help_text=None,widget=PasswordInput,label='Confirm Password')
    are_you_turf_owner = forms.BooleanField(required = False)

    class Meta:
        model=User
        fields=('username','email','phone','address','gender','password1','password2')

class TurfForm(forms.ModelForm):
    class Meta:
        model = models.Turf
        exclude = ('id', 'images')
        widgets = {
            'owner': forms.HiddenInput(),
        }
        
class DateInput(forms.DateInput):
    input_type = 'date'

class BookingForm(forms.ModelForm):
    class Meta:
        model = models.Bookings
        exclude = ('id', )
        widgets = {
            'user': forms.HiddenInput(),
            'turf': forms.HiddenInput(),
            'date': DateInput(),
            # 'time_from': forms.TimeInput(attrs={'type': 'time'}),
            # 'time_to': forms.TimeInput(attrs={'type': 'time'}),
            'time_from': forms.HiddenInput(),
            'time_to': forms.HiddenInput(),
            'razorpay_order_id': forms.HiddenInput(),
            'razorpay_payment_id': forms.HiddenInput(),
            'razorpay_signature': forms.HiddenInput(),
            'order_id': forms.HiddenInput(),
        }

