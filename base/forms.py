from django.forms import ModelForm
from .models import Room,User
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MyRegisterUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username','password1','password2','email','name']


class RoomForm(ModelForm):
  class Meta:
    model = Room
    fields = '__all__'
    exclude = ['host','participants']

class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ['avatar','username','first_name','email','bio']
