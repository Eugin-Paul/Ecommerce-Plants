from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta :
        model = User
        fields = ['username','email','password1','password2']

class PincodeForm(forms.Form):
    pincode = forms.IntegerField()

class AddressForm(forms.Form):
    name = forms.CharField(widget = forms.TextInput(attrs = {
      'placeholder': 'Name',
      'id': 'text_form'
    }))
    email = forms.CharField(widget = forms.TextInput(attrs = {
      'placeholder': 'Email',
      'id': 'text_form'
    }))
    address = forms.CharField(widget = forms.TextInput(attrs = {
      'placeholder': 'Address',
      'id': 'text_form_address'
    }))
    city = forms.CharField(widget = forms.TextInput(attrs = {
      'placeholder': 'City',
      'id': 'text_form'
    }))
    state = forms.CharField(widget = forms.TextInput(attrs = {
      'placeholder': 'State',
      'id': 'text_form'
    }))
    landmark = forms.CharField(widget = forms.TextInput(attrs = {
      'placeholder': 'Landmark',
      'id': 'text_form'
    }))
    phonenumber = forms.CharField(widget = forms.TextInput(attrs = {
      'placeholder': 'Phone Number',
      'id': 'text_form'
    }))
