from django import forms 
from . import models
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    class Meta:
        model=models.Category
        fields='__all__'


class EventForm(forms.ModelForm):
    class Meta:
        model=models.Event
        exclude=('user',)

class UserChange(UserChangeForm):
    password=None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


